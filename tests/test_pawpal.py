from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def make_owner():
    owner = Owner(name="Jordan")
    dog = Pet(name="Biscuit", species="Dog")
    cat = Pet(name="Mochi", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat


# ---- Phase 2 basics ----
def test_mark_complete_changes_status():
    task = Task("Walk", "08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="Dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", "08:00"))
    assert len(pet.tasks) == 1


def test_add_task_sets_pet_name():
    pet = Pet(name="Biscuit", species="Dog")
    task = Task("Walk", "08:00")
    pet.add_task(task)
    assert task.pet_name == "Biscuit"


# ---- Sorting ----
def test_sort_by_time_is_chronological():
    owner, dog, cat = make_owner()
    dog.add_task(Task("Evening walk", "18:00"))
    cat.add_task(Task("Breakfast", "08:00"))
    dog.add_task(Task("Lunch", "12:30"))
    result = Scheduler(owner).sort_by_time(owner.get_all_tasks())
    assert [t.time for t in result] == ["08:00", "12:30", "18:00"]


def test_todays_schedule_spans_multiple_pets_and_excludes_other_days():
    owner, dog, cat = make_owner()
    dog.add_task(Task("Walk", "09:00"))
    cat.add_task(Task("Feed", "07:00"))
    cat.add_task(Task("Tomorrow thing", "06:00",
                      due_date=date.today() + timedelta(days=1)))
    schedule = Scheduler(owner).get_todays_schedule()
    assert [t.description for t in schedule] == ["Feed", "Walk"]


# ---- Recurrence ----
def test_daily_task_creates_next_day_task():
    owner, dog, _ = make_owner()
    task = Task("Walk", "08:00", frequency="daily")
    dog.add_task(task)
    new_task = Scheduler(owner).mark_task_complete(task)
    assert task.completed is True
    assert new_task is not None
    assert new_task.due_date == task.due_date + timedelta(days=1)
    assert new_task.completed is False
    assert new_task in dog.tasks
    assert len(dog.tasks) == 2


def test_weekly_task_creates_task_seven_days_later():
    owner, dog, cat = make_owner()
    task = Task("Flea meds", "08:00", frequency="weekly")
    cat.add_task(task)
    new_task = Scheduler(owner).mark_task_complete(task)
    assert new_task.due_date == task.due_date + timedelta(days=7)


def test_one_time_task_does_not_recur():
    owner, dog, _ = make_owner()
    task = Task("Vet", "10:00", frequency="once")
    dog.add_task(task)
    assert Scheduler(owner).mark_task_complete(task) is None
    assert len(dog.tasks) == 1


def test_completing_twice_does_not_duplicate_recurrence():
    owner, dog, _ = make_owner()
    task = Task("Walk", "08:00", frequency="daily")
    dog.add_task(task)
    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)
    assert scheduler.mark_task_complete(task) is None
    assert len(dog.tasks) == 2


# ---- Conflicts ----
def test_detect_conflicts_flags_same_time():
    owner, dog, cat = make_owner()
    dog.add_task(Task("Walk", "08:00"))
    cat.add_task(Task("Feed", "08:00"))
    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflict_for_different_times():
    owner, dog, cat = make_owner()
    dog.add_task(Task("Walk", "08:00"))
    cat.add_task(Task("Feed", "09:00"))
    assert Scheduler(owner).detect_conflicts() == []


def test_completed_tasks_do_not_conflict():
    owner, dog, cat = make_owner()
    done = Task("Walk", "08:00")
    dog.add_task(done)
    cat.add_task(Task("Feed", "08:00"))
    done.mark_complete()
    assert Scheduler(owner).detect_conflicts() == []


# ---- Filtering ----
def test_filter_by_pet_and_status():
    owner, dog, cat = make_owner()
    walk = Task("Walk", "08:00")
    dog.add_task(walk)
    cat.add_task(Task("Feed", "09:00"))
    walk.mark_complete()
    scheduler = Scheduler(owner)
    assert [t.description for t in scheduler.filter_tasks(pet_name="Mochi")] == ["Feed"]
    assert scheduler.filter_tasks(completed=True) == [walk]
    assert len(scheduler.filter_tasks(completed=False)) == 1


# ---- Edge cases ----
def test_pet_with_no_tasks_and_empty_owner():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)
    assert scheduler.get_todays_schedule() == []
    owner.add_pet(Pet(name="Biscuit", species="Dog"))
    assert scheduler.get_todays_schedule() == []
    assert scheduler.detect_conflicts() == []


def test_invalid_time_is_rejected():
    with pytest.raises(ValueError):
        Task("Walk", "9:00")
    with pytest.raises(ValueError):
        Task("Walk", "25:00")


def test_duplicate_pet_name_is_rejected():
    owner = Owner(name="Jordan")
    owner.add_pet(Pet(name="Biscuit", species="Dog"))
    with pytest.raises(ValueError):
        owner.add_pet(Pet(name="biscuit", species="Cat"))


def test_get_all_tasks_returns_copy():
    owner, dog, _ = make_owner()
    dog.add_task(Task("Walk", "08:00"))
    owner.get_all_tasks().clear()
    assert len(dog.tasks) == 1