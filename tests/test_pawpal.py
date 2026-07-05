"""
tests/test_pawpal.py

Initial pytest suite for PawPal+ (Phase 2). Covers the two basics:
1. Marking a task complete actually changes its status.
2. Adding a task to a Pet increases that pet's task count.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task(description="Feeding", duration_minutes=10, priority="high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task(description="Morning walk", duration_minutes=30, priority="high"))

    assert len(pet.get_tasks()) == 1