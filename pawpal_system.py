"""
pawpal_system.py

Logic layer for PawPal+. Defines the core domain classes: Task, Pet, Owner,
and Scheduler. This file starts as a skeleton (Phase 1) and gets fleshed
out with real behavior in Phase 2.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet-care activity (feeding, walk, medication, appointment)."""

    description: str
    duration_minutes: int
    priority: str = "medium"  # "high" | "medium" | "low"
    time: str = ""  # optional fixed "HH:MM" time; empty means flexible
    frequency: str = "once"  # "once" | "daily" | "weekly"
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self):
        """Mark this task as completed."""
        pass

    def next_occurrence(self):
        """Return a new Task for the next occurrence, if this task recurs."""
        pass


@dataclass
class Pet:
    """A pet belonging to an Owner, with its own list of tasks."""

    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a Task to this pet's task list."""
        pass

    def get_tasks(self):
        """Return this pet's list of tasks."""
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
        """Return a flat list of every task across all of this owner's pets."""
        pass


class Scheduler:
    """The 'brain' that builds a daily plan from an Owner's pets and tasks,
    respecting priority and the owner's available time, and explaining
    why each task was included."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def build_daily_plan(self):
        """Return today's plan: an ordered list of tasks (with a short
        explanation for each) that fits within available_minutes_per_day."""
        pass

    def sort_by_priority(self, tasks):
        """Return tasks sorted by priority (high first), then by time."""
        pass

    def filter_tasks(self, status=None, pet_name=None):
        """Return tasks filtered by completion status and/or pet name."""
        pass

    def detect_conflicts(self, tasks):
        """Return a list of warning messages for tasks scheduled at the same
        fixed time."""
        pass