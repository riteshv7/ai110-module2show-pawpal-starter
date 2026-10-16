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