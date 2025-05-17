import streamlit as st
from task_utils import initialize_or_next_task, display_completion_page, display_fill_in_the_blank, display_multiple_choice, display_code_output

# UI
st.title("Python Learning Tasks")
st.sidebar.header("Progress")
st.sidebar.write(f"Points: {st.session_state.get('points', -1)}")

# Display current task
if "task" not in st.session_state and "completed" not in st.session_state:
    initialize_or_next_task()

# Display completion page
if "completed" in st.session_state and st.session_state.completed:
    display_completion_page()

elif "task" in st.session_state:
    task = st.session_state.task
    if task["task_type"] == "fill_in_the_blank":
        display_fill_in_the_blank(task)
    elif task["task_type"] == "multiple_choice":
        display_multiple_choice(task)
    elif task["task_type"] == "code_output":
        display_code_output(task)