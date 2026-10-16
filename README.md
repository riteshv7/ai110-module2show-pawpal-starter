# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

- **Multi-pet management:** one owner, many pets, each with its own tasks
- **Sorting by time:** schedules always display in chronological order
- **Filtering:** view tasks by pet or by pending/completed status
- **Conflict warnings:** pending tasks at the same date and time are
  flagged with a readable warning instead of an error
- **Daily and weekly recurrence:** completing a recurring task
  automatically creates the next occurrence
- **Input validation:** malformed times, unknown frequencies or priorities,
  and duplicate pet names are rejected
- **Streamlit UI:** forms to add pets and tasks, a sorted schedule table,
  and a mark-complete button

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

````
=== Today's Schedule for Jordan (2026-10-16) ===

Sorted by time
--------------------------------------------------------------
  07:30  [ ]  Biscuit  Morning walk           daily  high
  08:00  [ ]  Mochi    Breakfast              daily  medium
  08:00  [ ]  Mochi    Flea medication        weekly high
  14:15  [ ]  Mochi    Vet appointment        once   medium
  18:00  [ ]  Biscuit  Evening walk           daily  high

Conflict check:
  WARNING: Conflict on 2026-10-16 at 08:00: Breakfast (Mochi), Flea medication (Mochi)

Filter: Mochi's tasks
--------------------------------------------------------------
  08:00  [ ]  Mochi    Breakfast              daily  medium
  08:00  [ ]  Mochi    Flea medication        weekly high
  14:15  [ ]  Mochi    Vet appointment        once   medium

Completed 'Morning walk'. Next occurrence created for 2026-10-17.

Filter: completed tasks
--------------------------------------------------------------
  07:30  [x]  Biscuit  Morning walk           daily  high

Filter: pending tasks (all dates)
--------------------------------------------------------------
  07:30  [ ]  Biscuit  Morning walk           daily  high
  08:00  [ ]  Mochi    Breakfast              daily  medium
  08:00  [ ]  Mochi    Flea medication        weekly high
  14:15  [ ]  Mochi    Vet appointment        once   medium
  18:00  [ ]  Biscuit  Evening walk           daily  high
  ````
  ### Implementation summary

PawPal+ is built from four classes. `Task`, `Pet`, and `Owner` are dataclasses that hold the data: an Owner has Pets, and a Pet has Tasks.
`Scheduler` holds the logic and reads every pet's tasks through `owner.get_all_tasks()`, so it works across all pets. `main.py` is a CLI demo that checks this logic in the terminal before any UI is connected.

## 🧪 Testing PawPal+

Run the test suite with:

```
python -m pytest
```

**What the tests cover:**
- Task completion and adding tasks to a pet
- Sorting tasks chronologically by time
- Today's schedule across multiple pets (excludes other days)
- Recurrence: daily tasks create a next-day task, weekly tasks add 7 days,
  one-time tasks don't repeat, and completing twice doesn't duplicate
- Conflict detection: same-time tasks are flagged, different times and
  completed tasks are not
- Filtering by pet name and completion status
- Edge cases: empty owner or pet with no tasks, invalid time format,
  duplicate pet names, and get_all_tasks() returning a copy

**Sample test output:**

```
======================================================================= test session starts =======================================================================
platform darwin -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/riteshverma/Desktop/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 17 items                                                                                                                                                

tests/test_pawpal.py .................                                                                                                                      [100%]

======================================================================= 17 passed in 0.03s =============================================================
```

**Confidence Level:** ⭐⭐⭐⭐ (4/5). All tests pass and cover the core
behaviors, but conflict detection only checks exact times, not overlapping
durations, and the Streamlit UI is tested only by hand.

## 📐 Smarter Scheduling

| Feature           | Method(s)                          | Notes |
| ----------------- | ---------------------------------- | ----- |
| Task sorting      | `Scheduler.sort_by_time()`         | Sorts tasks by their "HH:MM" time string using `sorted()` with a lambda key. Works because times are zero-padded. |
| Filtering         | `Scheduler.filter_tasks()`         | Filters by pet name and/or completion status. Can also filter an existing list through its `tasks` argument. |
| Conflict handling | `Scheduler.detect_conflicts()`     | Groups pending tasks by date and time and returns warning strings for any slot with 2+ tasks, across all pets. Never raises an error. |
| Recurring tasks   | `Scheduler.mark_task_complete()`   | Completing a daily task creates a copy due tomorrow; weekly adds 7 days (via `timedelta`). One-time tasks don't repeat. |

## 📸 Demo Walkthrough

**Main UI features:** add a pet, schedule tasks with a time, repeat
frequency, priority and duration, view today's schedule, filter it, and
mark tasks complete.

**Example workflow:**
1. Run `streamlit run app.py` and add a pet named Biscuit.
2. Schedule a daily "Morning walk" at 07:30 for Biscuit.
3. Add a second pet, Mochi, and schedule two tasks at 08:00.
4. View today's schedule: tasks appear sorted by time, and a warning
   shows the 08:00 conflict.
5. Mark the morning walk complete: a new walk is scheduled for tomorrow.

**Key Scheduler behaviors shown:** sorting (`sort_by_time`), conflict
warnings (`detect_conflicts`), filtering (`filter_tasks`), and daily
recurrence (`mark_task_complete`).

**Sample CLI output from `main.py`:**

```
=== Today's Schedule for Jordan (2026-10-16) ===

Sorted by time
--------------------------------------------------------------
  07:30  [ ]  Biscuit  Morning walk           daily  high
  08:00  [ ]  Mochi    Breakfast              daily  medium
  08:00  [ ]  Mochi    Flea medication        weekly high
  14:15  [ ]  Mochi    Vet appointment        once   medium
  18:00  [ ]  Biscuit  Evening walk           daily  high

Conflict check:
  WARNING: Conflict on 2026-10-16 at 08:00: Breakfast (Mochi), Flea medication (Mochi)

Completed 'Morning walk'. Next occurrence created for 2026-10-17.
```