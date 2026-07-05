"""
pawpal_system.py

Logic layer for PawPal+. Defines the core domain classes: Task, Pet, Owner,
and Scheduler.

Design decisions (see reflection.md 1b):
- Task.pet_name is stamped automatically by Pet.add_task().
- Task.start_date anchors recurrence so next_occurrence() can compute a
  real next date for "daily"/"weekly" tasks.
- Scheduler.build_daily_plan() uses a GREEDY-BY-PRIORITY fit-to-budget
  strategy (not optimal knapsack packing) — simple and explainable.
- Scheduler.detect_conflicts() compares time INTERVALS
  [time, time + duration), not just equal start times. Flexible tasks
  (time == "") are excluded from conflict checks.
- get_tasks() / get_all_tasks() return copies.
- Recurrence + completion: each occurrence is its own Task instance.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta


# Priority rank used for sorting (lower = higher priority = scheduled first).
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """A single pet-care activity (feeding, walk, medication, appointment)."""

    description: str
    duration_minutes: int
    priority: str = "medium"  # "high" | "medium" | "low"
    time: str = ""  # optional fixed "HH:MM" time; "" means flexible
    frequency: str = "once"  # "once" | "daily" | "weekly"
    start_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: str = ""  # stamped by Pet.add_task(), not set directly

    def mark_complete(self):
        """Mark this occurrence completed. If this task recurs, also
        return a new Task representing the next occurrence. Returns None
        if the task does not recur (frequency == "once")."""
        self.completed = True
        return self.next_occurrence()

    def next_occurrence(self):
        """Return a new Task for the next occurrence, or None if 'once'."""
        if self.frequency == "daily":
            delta = timedelta(days=1)
        elif self.frequency == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            time=self.time,
            frequency=self.frequency,
            start_date=self.start_date + delta,
            completed=False,
            pet_name=self.pet_name,
        )


@dataclass
class Pet:
    """A pet belonging to an Owner, with its own list of tasks."""

    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a Task to this pet's task list, stamping task.pet_name
        with this pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self):
        """Return a copy of this pet's task list."""
        return list(self.tasks)


@dataclass
class Owner:
    """The pet owner, who manages multiple pets and has daily time constraints."""

    name: str
    pets: list = field(default_factory=list)
    available_minutes_per_day: int = 60

    def add_pet(self, pet: Pet):
        """Add a Pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return a flat copy of every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The 'brain' that builds a daily plan from an Owner's pets and tasks."""

    def __init__(self, owner: Owner):
        """Create a Scheduler bound to the given Owner whose tasks it will plan."""
        self.owner = owner

    def build_daily_plan(self):
        """Build today's plan using a greedy-by-priority strategy.

        Returns a list of (task, explanation) tuples for tasks that made
        it into the plan, in the order they'll be done.
        """
        today = date.today()
        candidates = [
            t
            for t in self.owner.get_all_tasks()
            if not t.completed and t.start_date <= today
        ]
        ordered = self.sort_by_priority(candidates)

        plan = []
        minutes_used = 0
        budget = self.owner.available_minutes_per_day

        for task in ordered:
            if minutes_used + task.duration_minutes <= budget:
                minutes_used += task.duration_minutes
                reason = (
                    f"{task.priority} priority, fits in remaining budget "
                    f"({budget - (minutes_used - task.duration_minutes)} min left before this task)"
                )
                plan.append((task, reason))
            # else: skipped silently for now — Phase 4 will add explicit
            # "skipped, out of time" messaging if needed.

        return plan

    def sort_by_priority(self, tasks):
        """Return tasks sorted by priority rank, then by time (flexible
        tasks, time == "", sort after fixed-time tasks within the same
        priority)."""

        def sort_key(task):
            rank = PRIORITY_RANK.get(task.priority, 1)
            minutes = self._parse_time(task.time)
            # Flexible tasks (None) sort after any fixed time in same priority
            minutes_for_sort = minutes if minutes is not None else 24 * 60
            return (rank, minutes_for_sort)

        return sorted(tasks, key=sort_key)

    def filter_tasks(self, status=None, pet_name=None):
        """Return tasks filtered by completion status and/or pet name.

        status: True (completed only), False (incomplete only), or None (all)
        pet_name: a pet's name, or None (all pets)
        """
        tasks = self.owner.get_all_tasks()
        if status is not None:
            tasks = [t for t in tasks if t.completed == status]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        return tasks

    def detect_conflicts(self, tasks):
        """Return a list of warning messages for tasks whose fixed-time
        intervals overlap. Flexible tasks (time == "") are excluded."""
        fixed = [t for t in tasks if t.time]
        warnings = []

        for i in range(len(fixed)):
            for j in range(i + 1, len(fixed)):
                a, b = fixed[i], fixed[j]
                a_start = self._parse_time(a.time)
                b_start = self._parse_time(b.time)
                a_end = a_start + a.duration_minutes
                b_end = b_start + b.duration_minutes

                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"Conflict: '{a.description}' ({a.time}, "
                        f"{a.duration_minutes} min) overlaps with "
                        f"'{b.description}' ({b.time}, {b.duration_minutes} min)"
                    )

        return warnings

    def _parse_time(self, time_str):
        """Parse an 'HH:MM' string into minutes-since-midnight. Returns
        None if time_str is empty (flexible task)."""
        if not time_str:
            return None
        hours, minutes = time_str.split(":")
        return int(hours) * 60 + int(minutes)