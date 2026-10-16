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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
