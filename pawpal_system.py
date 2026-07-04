"""
pawpal_system.py

Logic layer for PawPal+. Defines the core domain classes: Task, Pet, Owner,
and Scheduler. This file starts as a skeleton (Phase 1) and gets fleshed
out with real behavior in Phase 2.

Design decisions locked in after AI code review (see reflection.md 1b):
- Task.pet_name is stamped automatically by Pet.add_task() (not set
  independently). Pet names are assumed unique within an Owner.
- Task.start_date anchors recurrence so next_occurrence() can compute a
  real next date for "daily"/"weekly" tasks.
- Scheduler.build_daily_plan() uses a GREEDY-BY-PRIORITY fit-to-budget
  strategy (not optimal knapsack packing) — simple and explainable.
- Scheduler.detect_conflicts() compares time INTERVALS
  [time, time + duration), not just equal start times. Flexible tasks
  (time == "") are excluded from conflict checks.
- get_tasks() / get_all_tasks() return copies, so callers can't mutate
  internal state by accident.
- Recurrence + completion: each occurrence is its own Task instance.
  mark_complete() marks that instance done and, if it recurs, creates the
  next occurrence via next_occurrence().
"""

from dataclasses import dataclass, field
from datetime import date


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
        return a new Task representing the next occurrence (caller is
        responsible for adding it to the pet's task list)."""
        pass

    def next_occurrence(self):
        """Return a new Task for the next occurrence (start_date advanced
        by 1 day for 'daily' or 7 days for 'weekly'), or None if 'once'."""
        pass


@dataclass
class Pet:
    """A pet belonging to an Owner, with its own list of tasks."""

    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a Task to this pet's task list, stamping task.pet_name
        with this pet's name so the link doesn't depend on caller
        discipline."""
        pass

    def get_tasks(self):
        """Return a COPY of this pet's task list (safe to mutate)."""
        pass


@dataclass
class Owner:
    """The pet owner, who manages multiple pets and has daily time constraints."""

    name: str
    pets: list = field(default_factory=list)
    available_minutes_per_day: int = 60

    def add_pet(self, pet: Pet):
        """Add a Pet to this owner's list of pets."""
        pass

    def get_all_tasks(self):
        """Return a flat COPY of every task across all of this owner's pets."""
        pass


class Scheduler:
    """The 'brain' that builds a daily plan from an Owner's pets and tasks,
    respecting priority and the owner's available time, and explaining
    why each task was included."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def build_daily_plan(self):
        """Build today's plan using a greedy-by-priority strategy:
        1. Get all incomplete tasks for today.
        2. Sort by priority (see sort_by_priority).
        3. Walk the sorted list, adding tasks to the plan while tracking
           a running total of minutes used, skipping any task that would
           exceed available_minutes_per_day.
        4. Return a list of (task, explanation_string) tuples, where the
           explanation says why each task was included or skipped.
        """
        pass

    def sort_by_priority(self, tasks):
        """Return tasks sorted by priority rank (PRIORITY_RANK), then by
        time for tasks that share a priority."""
        pass

    def filter_tasks(self, status=None, pet_name=None):
        """Return tasks filtered by completion status and/or pet name."""
        pass

    def detect_conflicts(self, tasks):
        """Return a list of warning messages for tasks whose fixed-time
        intervals [time, time + duration_minutes) overlap. Tasks with
        time == "" (flexible) are excluded from this check."""
        pass

    def _parse_time(self, time_str):
        """Shared helper: parse an 'HH:MM' string into minutes-since-
        midnight (int) for comparison/sorting. Returns None if time_str
        is empty (flexible task)."""
        pass
