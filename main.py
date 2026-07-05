"""
main.py

CLI demo for PawPal+. Creates an Owner with two Pets, adds several Tasks
with different priorities/times, and prints today's plan to the terminal.
This is the "testing ground" for pawpal_system.py before wiring up the
Streamlit UI.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(plan):
    """Print a readable version of the daily plan."""
    if not plan:
        print("  (no tasks scheduled)")
        return
    for task, reason in plan:
        time_label = task.time if task.time else "flexible"
        print(f"  [{time_label}] {task.description} "
              f"({task.duration_minutes} min, {task.priority} priority)")
        print(f"      -> {reason}")


def main():
    # Create an owner with a daily care-time budget
    owner = Owner(name="Jordan", available_minutes_per_day=90)

    # Create two pets
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Add tasks with different priorities and times (some fixed, some flexible)
    mochi.add_task(Task(description="Morning walk", duration_minutes=30,
                         priority="high", time="08:00"))
    mochi.add_task(Task(description="Feeding", duration_minutes=10,
                         priority="high", time="08:15"))  # overlaps on purpose
    mochi.add_task(Task(description="Brushing", duration_minutes=15,
                         priority="low"))  # flexible, no fixed time

    luna.add_task(Task(description="Feeding", duration_minutes=10,
                        priority="high", time="09:00"))
    luna.add_task(Task(description="Litter box cleaning", duration_minutes=10,
                        priority="medium"))
    luna.add_task(Task(description="Play time", duration_minutes=20,
                        priority="medium", frequency="daily"))

    scheduler = Scheduler(owner)

    print(f"=== Today's Plan for {owner.name} "
          f"(budget: {owner.available_minutes_per_day} min) ===")
    plan = scheduler.build_daily_plan()
    print_schedule(plan)

    print("\n=== Conflict Warnings ===")
    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
    if conflicts:
        for warning in conflicts:
            print(f"  ! {warning}")
    else:
        print("  (no conflicts detected)")

    print("\n=== Filter Demo: Mochi's tasks only ===")
    mochi_tasks = scheduler.filter_tasks(pet_name="Mochi")
    for task in mochi_tasks:
        print(f"  - {task.description} ({task.priority})")

    print("\n=== Recurring Task Demo ===")
    daily_task = luna.tasks[-1]  # "Play time", frequency="daily"
    print(f"  Before: '{daily_task.description}' completed={daily_task.completed}, "
          f"start_date={daily_task.start_date}")
    next_task = daily_task.mark_complete()
    print(f"  After marking complete: completed={daily_task.completed}")
    if next_task:
        luna.add_task(next_task)
        print(f"  Next occurrence created: start_date={next_task.start_date}, "
              f"completed={next_task.completed}")


if __name__ == "__main__":
    main()