"""PawPal+ logic layer: Task, Pet, Owner and Scheduler."""

import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional

TIME_PATTERN = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
VALID_FREQUENCIES = ("once", "daily", "weekly")
VALID_PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    """A single pet care activity."""

    description: str
    time: str                          # zero-padded "HH:MM"
    frequency: str = "once"            # "once", "daily", "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: str = ""
    priority: str = "medium"           # "low", "medium", "high"
    duration_minutes: int = 30

    def __post_init__(self) -> None:
        """Validate the time format, frequency and priority."""
        if not TIME_PATTERN.match(self.time):
            raise ValueError(f"time must be zero-padded HH:MM, got {self.time!r}")
        if self.frequency not in VALID_FREQUENCIES:
            raise ValueError(f"frequency must be one of {VALID_FREQUENCIES}")
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}")

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet and record the pet's name on it."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove this exact task object from the pet's list."""
        self.tasks = [t for t in self.tasks if t is not task]


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet, rejecting duplicate names."""
        if any(p.name.lower() == pet.name.lower() for p in self.pets):
            raise ValueError(f"A pet named {pet.name!r} already exists")
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return a new list holding every task from every pet."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The brain: organizes tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_todays_schedule(self, today: Optional[date] = None) -> List[Task]:
        """Return tasks due today (all pets), sorted by time."""
        today = today or date.today()
        due_today = [t for t in self.owner.get_all_tasks() if t.due_date == today]
        return self.sort_by_time(due_today)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by their HH:MM time (earliest first)."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(self, pet_name: Optional[str] = None,
                     completed: Optional[bool] = None,
                     tasks: Optional[List[Task]] = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        result = self.owner.get_all_tasks() if tasks is None else list(tasks)
        if pet_name is not None:
            result = [t for t in result if t.pet_name.lower() == pet_name.lower()]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Return warning messages for pending tasks sharing a date and time."""
        pool = self.owner.get_all_tasks() if tasks is None else tasks
        slots = defaultdict(list)
        for task in pool:
            if task.completed:
                continue
            slots[(task.due_date, task.time)].append(task)

        warnings = []
        for (due, time), group in sorted(slots.items()):
            if len(group) > 1:
                names = ", ".join(f"{t.description} ({t.pet_name})" for t in group)
                warnings.append(f"Conflict on {due} at {time}: {names}")
        return warnings

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Complete a task; for daily/weekly tasks, schedule the next one.

        Returns the newly created task, or None if no recurrence was needed.
        """
        if task.completed:
            return None
        task.mark_complete()

        if task.frequency == "once":
            return None

        step = timedelta(days=1 if task.frequency == "daily" else 7)
        next_task = Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            due_date=task.due_date + step,
            priority=task.priority,
            duration_minutes=task.duration_minutes,
        )
        for pet in self.owner.pets:
            if any(t is task for t in pet.tasks):
                pet.add_task(next_task)
                return next_task
        return None