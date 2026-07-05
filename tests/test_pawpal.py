"""
tests/test_pawpal.py

Pytest suite for PawPal+. Covers:
- Basics: marking a task complete, adding a task to a pet.
- Sorting correctness: tasks come back in priority (then time) order.
- Recurrence: completing a daily task produces a correctly-dated next one.
- Conflict detection: overlapping fixed-time tasks are flagged; flexible
  and non-overlapping tasks are not.
- A couple of edge cases: a pet with no tasks, and two tasks at the exact
  same time.
"""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


# ---------------------------------------------------------------------------
# Basics
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------

def test_sort_by_priority_orders_high_before_medium_before_low():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)

    low = Task(description="Brushing", duration_minutes=15, priority="low")
    high = Task(description="Walk", duration_minutes=20, priority="high")
    medium = Task(description="Feeding", duration_minutes=10, priority="medium")

    ordered = scheduler.sort_by_priority([low, high, medium])

    assert [t.priority for t in ordered] == ["high", "medium", "low"]


def test_sort_by_priority_breaks_ties_by_time():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)

    later = Task(description="Evening walk", duration_minutes=20, priority="high", time="18:00")
    earlier = Task(description="Morning walk", duration_minutes=20, priority="high", time="08:00")

    ordered = scheduler.sort_by_priority([later, earlier])

    assert [t.description for t in ordered] == ["Morning walk", "Evening walk"]


# ---------------------------------------------------------------------------
# Recurrence
# ---------------------------------------------------------------------------

def test_mark_complete_on_daily_task_creates_next_day_occurrence():
    start = date(2026, 7, 4)
    task = Task(
        description="Play time",
        duration_minutes=20,
        priority="medium",
        frequency="daily",
        start_date=start,
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.start_date == start + timedelta(days=1)
    assert next_task.description == task.description


def test_mark_complete_on_once_task_returns_none():
    task = Task(description="Vet visit", duration_minutes=30, priority="high", frequency="once")

    next_task = task.mark_complete()

    assert next_task is None


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_detect_conflicts_flags_overlapping_fixed_time_tasks():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)

    a = Task(description="Morning walk", duration_minutes=30, priority="high", time="08:00")
    b = Task(description="Feeding", duration_minutes=10, priority="high", time="08:15")

    warnings = scheduler.detect_conflicts([a, b])

    assert len(warnings) == 1


def test_detect_conflicts_flags_exact_same_time():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)

    a = Task(description="Morning walk", duration_minutes=30, priority="high", time="08:00")
    b = Task(description="Feeding", duration_minutes=10, priority="high", time="08:00")

    warnings = scheduler.detect_conflicts([a, b])

    assert len(warnings) == 1


def test_detect_conflicts_ignores_non_overlapping_and_flexible_tasks():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)

    a = Task(description="Morning walk", duration_minutes=30, priority="high", time="08:00")
    b = Task(description="Feeding", duration_minutes=10, priority="high", time="09:00")
    flexible = Task(description="Brushing", duration_minutes=15, priority="low")  # time=""

    warnings = scheduler.detect_conflicts([a, b, flexible])

    assert warnings == []


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_pet_with_no_tasks_returns_empty_plan():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    plan = scheduler.build_daily_plan()

    assert plan == []


def test_get_tasks_returns_a_copy_not_the_live_list():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Walk", duration_minutes=20, priority="high"))

    tasks = pet.get_tasks()
    tasks.append(Task(description="Extra", duration_minutes=5, priority="low"))

    assert len(pet.get_tasks()) == 1  # internal list unaffected by the mutation above