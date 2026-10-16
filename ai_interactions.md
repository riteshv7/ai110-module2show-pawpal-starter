# AI Interactions Log

# AI Interactions

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
