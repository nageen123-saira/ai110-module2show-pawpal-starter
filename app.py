import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    "Plan your pet's daily care tasks based on priority and how much time you have."
)

# ---------------------------------------------------------------------------
# Session state: create the Owner once, reuse it across reruns.
# Streamlit reruns the whole script on every interaction, so without this
# check, a new (empty) Owner would be created every time the user clicks
# something.
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes_per_day=60)

owner = st.session_state.owner

st.divider()

# ---------------------------------------------------------------------------
# Owner settings
# ---------------------------------------------------------------------------
st.subheader("Owner settings")
owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes_per_day = st.number_input(
    "Available minutes per day for pet care",
    min_value=10,
    max_value=600,
    value=owner.available_minutes_per_day,
    step=10,
)

st.divider()

# ---------------------------------------------------------------------------
# Add a pet
# ---------------------------------------------------------------------------
st.subheader("Add a pet")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", key="new_pet_name")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")

if st.button("Add pet"):
    if new_pet_name.strip():
        owner.add_pet(Pet(name=new_pet_name.strip(), species=new_pet_species))
        st.success(f"Added {new_pet_name}!")
    else:
        st.warning("Please enter a pet name.")

if not owner.pets:
    st.info("No pets yet. Add one above to get started.")
else:
    st.divider()

    # -----------------------------------------------------------------------
    # Add a task to a chosen pet
    # -----------------------------------------------------------------------
    st.subheader("Add a task")
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Which pet?", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    tcol1, tcol2, tcol3 = st.columns(3)
    with tcol1:
        task_description = st.text_input("Task description", value="Morning walk")
    with tcol2:
        task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with tcol3:
        task_priority = st.selectbox("Priority", ["high", "medium", "low"], index=1)

    tcol4, tcol5 = st.columns(2)
    with tcol4:
        has_fixed_time = st.checkbox("Fixed time?", value=False)
        task_time = st.text_input("Time (HH:MM)", value="08:00") if has_fixed_time else ""
    with tcol5:
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        if task_description.strip():
            selected_pet.add_task(
                Task(
                    description=task_description.strip(),
                    duration_minutes=int(task_duration),
                    priority=task_priority,
                    time=task_time,
                    frequency=task_frequency,
                )
            )
            st.success(f"Added '{task_description}' for {selected_pet.name}!")
        else:
            st.warning("Please enter a task description.")

    st.divider()

    # -----------------------------------------------------------------------
    # Current tasks (across all pets)
    # -----------------------------------------------------------------------
    st.subheader("Current tasks")
    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.table(
            [
                {
                    "Pet": t.pet_name,
                    "Task": t.description,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                    "Time": t.time or "flexible",
                    "Frequency": t.frequency,
                    "Completed": t.completed,
                }
                for t in all_tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")

    st.divider()

    # -----------------------------------------------------------------------
    # Generate today's plan
    # -----------------------------------------------------------------------
    st.subheader("Today's plan")
    if st.button("Generate schedule"):
        scheduler = Scheduler(owner)

        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
        for warning in conflicts:
            st.warning(f"⚠️ {warning}")

        plan = scheduler.build_daily_plan()
        if plan:
            for task, reason in plan:
                time_label = task.time if task.time else "Flexible"
                st.success(
                    f"**[{time_label}] {task.description}** "
                    f"({task.pet_name}, {task.duration_minutes} min, {task.priority} priority)\n\n"
                    f"_{reason}_"
                )
        else:
            st.info("No tasks fit in today's plan. Add some tasks above.")
            