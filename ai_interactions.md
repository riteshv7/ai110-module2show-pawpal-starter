# AI Interactions Log

## Phase 1: Design review

**Tool:** Claude Code 

**Prompt:** "Review my skeleton in pawpal_system.py for a pet care
scheduler. Are there missing relationships or potential logic bottlenecks?
Don't rewrite the code, just list your suggestions."

**What the AI said:** It gave 16 suggestions, including: the Task-to-Pet
link was only a string, Task had no duration or priority, times stored as
strings can sort wrongly, and recurrence rules were undefined.

**What I accepted:**
- Pet.add_task() sets task.pet_name automatically
- Added duration_minutes and priority to Task
- Validate "HH:MM" times instead of switching to datetime.time

**What I rejected:** Owner constraints, a Plan class that explains itself,
and task IDs, because they add scope this project doesn't need.

## Phase 2: Core implementation

**Prompt:** I asked for a step-by-step guide to the whole project. Then,
once my skeleton was in place, I asked for "the code to add in the
pawpal system," meaning the full method implementations for Task, Pet,
Owner, and Scheduler. I then asked what to do next, and it gave me
main.py and the first two tests.

**What the AI produced:** Full implementations of Task, Pet, Owner, and
Scheduler, plus main.py and two starter tests.

**How I verified it:** Ran `python main.py` and checked the schedule,
conflict warning, and recurrence output. Ran `python -m pytest` and both
tests passed.

## Phase 3: UI and backend integration

**Tool:** Claude (chat)

**Prompt:** I asked for the code to connect app.py to my classes in
pawpal_system.py. I wanted forms for adding pets and tasks, and I needed
the Owner to survive Streamlit's reruns.

**What the AI produced:** A new app.py that imports Owner, Pet, Task, and
Scheduler. It stores the Owner in st.session_state, wires the add-pet form
to owner.add_pet() and the add-task form to pet.add_task(), and displays
the schedule using Scheduler methods.

**Key concept I learned:** Streamlit reruns the whole script on every
click, so an Owner created at the top would be reset to empty each time.
The check `if "owner" not in st.session_state` only creates the Owner the
first time, and later runs reuse the one in the session.

**How I verified it:** I ran `streamlit run app.py` and tested in the
browser. I added a pet named Biscuit and it appeared under "Your pets".
I added two tasks at 08:00 and a yellow conflict warning appeared. I
marked a daily task complete and a message said the next one was
scheduled for tomorrow.

**What I noticed:** Refreshing the browser page resets all the data,
because session_state only lasts for one browser session. I left
persistence out for now because it's an optional extension.

## Phase 4: Algorithmic layer

**Tool:** Claude Code

**Prompt:** "How could `detect_conflicts` be simplified for better
readability or performance?"

**What the AI suggested:** Four readability changes (defaultdict, a list
comprehension, sorting only conflicting slots, and a helper method), plus
a note that true overlap detection using duration_minutes would be a
bigger improvement.

**What I accepted:** defaultdict, because it removes the untyped
`slots = {}` and the `setdefault` call.

**What I rejected:** The list comprehension, because it packs the
grouping, filtering, and message formatting into one expression that is
harder to read. I also rejected overlap detection, because exact-time
matching is easier to test and explain.

**How I verified it:** Re-ran `python -m pytest` and `python main.py` and
confirmed the output matched what I had before.

## Phase 5: Testing and verification

**Tool:** Claude

**Prompt:** I asked for a full test suite for the scheduler covering
sorting, recurrence, conflict detection, and edge cases, building on the
two basic tests I already had.

**What the AI produced:** A replacement for tests/test_pawpal.py with 17
tests. It covers chronological sorting, today's schedule across multiple
pets, daily and weekly recurrence, one-time tasks not repeating, no
duplicate recurrence when a task is completed twice, same-time conflict
detection, completed tasks not conflicting, filtering by pet and status,
and edge cases (an owner with no pets, a pet with no tasks, an invalid
time like "9:00", duplicate pet names, and get_all_tasks() returning a
copy).

**How I verified it:** I ran `python -m pytest` and all 17 tests passed. I
also read each test to check that it asserts real behavior and not just
that the code runs. For example, the recurrence test checks that the new
task's due date is exactly one day later and that it was added to the
pet's list.

**What I noticed:** The tests only check exact-time conflicts, which
matches my design choice in reflection 2b. The Streamlit UI isn't covered
by automated tests, so I tested it by hand in the browser.

## Phase 6: Polish, documentation, and reflection

**Tool:** Claude (chat)

**Prompt:** I asked for help finalizing the project: the final UML
diagram, the README Features and Demo Walkthrough sections, and the
reflection answers.

**What the AI produced:** diagrams/uml_final.mmd (adds priority,
duration_minutes, __post_init__, the new method signatures, and the
Scheduler-to-Task "creates next occurrence" relationship), plus drafts of
the README sections and reflection answers.

**What I changed:** [say what you edited, for example "rewrote the
reflection answers in my own words" or "changed the confidence rating
to 4 stars because the UI is only tested by hand"].

**How I verified it:** I checked that uml_final.mmd matches the final
pawpal_system.py, previewed the README to confirm the code blocks render,
and re-ran `python -m pytest` (17 passed) and `streamlit run app.py`.