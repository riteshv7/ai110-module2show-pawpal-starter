from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾")
st.title("🐾 PawPal+")
st.caption("A smart pet care planner: sorted schedules, conflict warnings, recurring tasks.")

# Streamlit reruns this script on every click, so keep the Owner in session_state.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
if "flash" not in st.session_state:
    st.session_state.flash = None

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

if st.session_state.flash:
    st.success(st.session_state.flash)
    st.session_state.flash = None

# ---------------------------------------------------------------- Owner
owner.name = st.text_input("Owner name", value=owner.name)

# ----------------------------------------------------------------- Pets
st.subheader("1. Add a pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
    if st.form_submit_button("Add pet"):
        if not pet_name.strip():
            st.error("Please enter a pet name.")
        else:
            try:
                owner.add_pet(Pet(name=pet_name.strip(), species=species))
                st.success(f"Added {pet_name.strip()} the {species.lower()}.")
            except ValueError as err:
                st.error(str(err))

if owner.pets:
    st.write("Your pets: " + ", ".join(f"**{p.name}** ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

# ---------------------------------------------------------------- Tasks
st.subheader("2. Schedule a task")
if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        target = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Task (e.g. Morning walk)")
        col1, col2 = st.columns(2)
        task_time = col1.time_input("Time", value=time(8, 0))
        duration = col2.number_input("Duration (minutes)", 5, 480, 30, step=5)
        col3, col4 = st.columns(2)
        frequency = col3.selectbox("Repeats", ["once", "daily", "weekly"])
        priority = col4.selectbox("Priority", ["low", "medium", "high"], index=1)
        if st.form_submit_button("Add task"):
            if not description.strip():
                st.error("Please describe the task.")
            else:
                pet = next(p for p in owner.pets if p.name == target)
                pet.add_task(Task(
                    description=description.strip(),
                    time=task_time.strftime("%H:%M"),
                    frequency=frequency,
                    priority=priority,
                    duration_minutes=int(duration),
                ))
                st.success(f"Scheduled '{description.strip()}' for {target} at "
                           f"{task_time.strftime('%H:%M')}.")

# ------------------------------------------------------------- Schedule
st.subheader("3. Today's schedule")


def to_rows(tasks):
    """Convert tasks to table rows for st.table."""
    return [{
        "Time": t.time,
        "Pet": t.pet_name,
        "Task": t.description,
        "Repeats": t.frequency,
        "Priority": t.priority,
        "Minutes": t.duration_minutes,
        "Done": "✅" if t.completed else "⬜",
    } for t in tasks]


todays = scheduler.get_todays_schedule()
if not todays:
    st.info("Nothing scheduled for today.")
else:
    # Conflict warnings come straight from Scheduler.detect_conflicts()
    for warning in scheduler.detect_conflicts(todays):
        st.warning(f"⚠️ {warning}. You can't be in two places at once, so consider moving one task.")

    f1, f2 = st.columns(2)
    pet_filter = f1.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
    status_filter = f2.selectbox("Filter by status", ["All", "Pending", "Completed"])

    view = scheduler.filter_tasks(
        pet_name=None if pet_filter == "All" else pet_filter,
        completed={"All": None, "Pending": False, "Completed": True}[status_filter],
        tasks=todays,
    )
    st.table(to_rows(scheduler.sort_by_time(view)))

    pending = [t for t in todays if not t.completed]
    if pending:
        st.markdown("**Mark a task complete**")
        choice = st.selectbox(
            "Task",
            range(len(pending)),
            format_func=lambda i: f"{pending[i].time} - {pending[i].pet_name}: {pending[i].description}",
        )
        if st.button("Mark complete"):
            task = pending[choice]
            new_task = scheduler.mark_task_complete(task)
            msg = f"Completed '{task.description}'."
            if new_task:
                msg += f" Next one scheduled for {new_task.due_date}."
            st.session_state.flash = msg
            st.rerun()
    else:
        st.success("All of today's tasks are done! 🎉")