"""CLI demo for PawPal+: verifies the logic layer before the UI."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(title, tasks):
    """Print tasks as a readable table."""
    print(f"\n{title}")
    print("-" * 62)
    if not tasks:
        print("  (nothing scheduled)")
    for t in tasks:
        status = "[x]" if t.completed else "[ ]"
        print(f"  {t.time}  {status}  {t.pet_name:<8} {t.description:<22} "
              f"{t.frequency:<6} {t.priority}")


def main():
    owner = Owner(name="Jordan")
    biscuit = Pet(name="Biscuit", species="Dog")
    mochi = Pet(name="Mochi", species="Cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # Added deliberately out of order
    biscuit.add_task(Task("Evening walk", "18:00", frequency="daily", priority="high"))
    biscuit.add_task(Task("Morning walk", "07:30", frequency="daily", priority="high"))
    mochi.add_task(Task("Breakfast", "08:00", frequency="daily"))
    mochi.add_task(Task("Flea medication", "08:00", frequency="weekly", priority="high"))
    mochi.add_task(Task("Vet appointment", "14:15", priority="medium"))

    scheduler = Scheduler(owner)

    print(f"=== Today's Schedule for {owner.name} ({date.today()}) ===")
    print_schedule("Sorted by time", scheduler.get_todays_schedule())

    print("\nConflict check:")
    conflicts = scheduler.detect_conflicts()
    for warning in conflicts or ["No conflicts found."]:
        print(f"  WARNING: {warning}" if conflicts else f"  {warning}")

    print_schedule("Filter: Mochi's tasks",
                   scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Mochi")))

    # Complete a daily task and show the recurrence
    morning_walk = biscuit.tasks[1]
    new_task = scheduler.mark_task_complete(morning_walk)
    print(f"\nCompleted '{morning_walk.description}'. "
          f"Next occurrence created for {new_task.due_date}.")

    print_schedule("Filter: completed tasks",
                   scheduler.filter_tasks(completed=True))
    print_schedule("Filter: pending tasks (all dates)",
                   scheduler.sort_by_time(scheduler.filter_tasks(completed=False)))


if __name__ == "__main__":
    main()