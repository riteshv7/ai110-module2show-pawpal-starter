# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML has four classes: Task, Pet, Owner, and Scheduler.

Three core actions a user should be able to do:
1. Add a pet to their profile.
2. Schedule a task (walk, feeding, medication, appointment) for a pet.
3. View today's schedule, sorted by time, with warnings for conflicts.

- **Task** (dataclass): represents one activity. It holds a description,
  time ("HH:MM"), frequency (once/daily/weekly), due date, completion
  status, and the pet it belongs to. It can mark itself complete.
- **Pet** (dataclass): stores the pet's name, species, and its list of
  tasks. It can add and remove tasks.
- **Owner** (dataclass): holds the owner's name and list of pets. It can add
  pets and return every task across all pets through get_all_tasks().
- **Scheduler**: the "brain." It takes an Owner and reads tasks through
  owner.get_all_tasks(), so it works across all pets. It builds the daily
  schedule, sorts, filters, detects conflicts, and handles completing tasks.

Relationships: an Owner has many Pets, a Pet has many Tasks, and the
Scheduler reads from the Owner. I kept data (Task, Pet, Owner) separate from
logic (Scheduler) so the scheduling rules live in one place.

**b. Design changes**

I asked my AI assistant to review my skeleton. It gave 16 suggestions, and
I accepted a few and rejected most.

Accepted:
- Pet.add_task() now sets task.pet_name automatically. The AI pointed out
  that a plain string can be left empty or drift from Pet.name, so the Pet
  now fills it in.
- I added duration_minutes and priority to Task, because the README asks
  for them and sorting or dropping tasks needs them.
- I kept time as an "HH:MM" string but will validate the format, because
  "9:00" would sort after "10:00" as text. I rejected switching to
  datetime.time because string sorting works fine for zero-padded times.
- Recurrence will live in Scheduler.mark_task_complete(), not in Task,
  so the logic is in one place.

Rejected:
- Owner constraints, a Plan class that explains itself, and task IDs.
  These add classes or fields beyond the scope of this project.
- Duration-based overlap detection. I'll check exact same-time matches
  only, which is simpler.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers four things: the time of day, the due date, whether
a task is already completed, and which pet the task belongs to.

- **Time:** Tasks are sorted by their "HH:MM" time, so the owner always
  sees what to do next first.
- **Due date:** Today's schedule only shows tasks due today, and
  recurring tasks get a new due date when completed.
- **Completion status:** Completed tasks are not flagged as conflicts, and
  the schedule can be filtered to show only pending or completed tasks.
- **Pet:** The scheduler reads tasks across all pets through
  owner.get_all_tasks(), and tasks can be filtered by pet name.

I decided time mattered most because the main problem for a busy pet owner
is knowing what to do and when. Conflicts also depend on time, so sorting
and conflict detection both build on it. Tasks also store priority and
duration_minutes, but my scheduler does not use them yet. I kept the scope
to sorting, filtering, conflicts, and recurrence, and left priority-based
scheduling as a possible extension.

**b. Tradeoffs**

My scheduler only detects a conflict when two pending tasks have exactly
the same date and time. It does not check overlapping durations, so a
30-minute walk at 08:00 and a feeding at 08:15 are not flagged, even
though the owner could not do both at once.

This is reasonable for this project because exact-match detection is
simple to read, simple to test, and cannot crash. The detect_conflicts
method groups tasks into date-and-time slots and warns about any slot with
more than one task. Checking overlaps would mean tracking each task's
start and end time and comparing neighbors, which adds complexity and more
edge cases. When I asked my AI assistant about simplifying
detect_conflicts, it suggested overlap detection as a bigger improvement,
and I chose not to add it. Since tasks already store duration_minutes,
overlap detection would be a natural next step.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI assistant for design review, code generation, and testing
help. Early on I wrote my own class list (Task, Pet, Owner, Scheduler),
then asked the AI to review my skeleton and list problems without
rewriting the code. That prompt worked best because it gave me a list of
options to judge instead of code I would have just pasted in. I also used
it to explain the plan for each phase, and I used separate chat sessions
for design review and implementation so the conversations stayed focused.

**b. Judgment and verification**

The AI's review gave 16 suggestions, and I did not accept them all. I
rejected adding owner constraints, a separate Plan class that explains
itself, and unique task IDs, because they add classes or fields beyond what
this project needs. I accepted a few changes: Pet.add_task() now sets
task.pet_name automatically, Task has duration_minutes and priority fields,
and times are validated as zero-padded "HH:MM" strings. I kept times as
strings instead of switching to datetime.time because sorting works fine
for zero-padded strings and it keeps the code simpler.

I verified the result by running main.py and checking the printed schedule,
conflict warning, and recurrence message by eye, and by running pytest
(python -m pytest), where both tests passed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
