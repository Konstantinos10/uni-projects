from datetime import datetime
import streamlit as st
import json
import time
from random import shuffle
from firebase_admin import firestore

# Task files
TASK_FILES = {
    "fill_in_the_blank": "fill_in_the_blank.json",
    "multiple_choice": "multiple_choice.json"
}

db = firestore.client()

# Initialize points and level
def initialize_points():
    if "points" not in st.session_state:
        username = st.session_state.get("username")
        if username:
            try:
                users_ref = db.collection("users")
                query = users_ref.where("username", "==", username).limit(1).stream()
                for doc in query:
                    user_data = doc.to_dict()
                    break

                st.session_state.points = user_data.get('exp', 0)

            except Exception as e:
                st.error(f"Failed to decrypt username: {e}")

        else:
            st.info("Loading user session...")
            st.rerun()

        st.session_state.incorrect_attempts = {}  # Track incorrect attempts per task

def update_user_exp(points_to_add: int, puzzle_id: str = None):
    username = st.session_state.get("username")
    try:
        users_ref = db.collection("users")
        query = users_ref.where("username", "==", username).limit(1).stream()
        user_doc = next(query, None)

        if not user_doc:
            raise Exception("User not found")

        update_data = {
            "exp": firestore.Increment(points_to_add)
        }

        if puzzle_id:
            start_time = st.session_state.get("task_start_time", time.time())
            duration = round(time.time() - start_time, 2)
            completed_at = datetime.utcnow()

            puzzle_entry = {
                "id": puzzle_id,
                "duration": duration,
                "completed_at": completed_at
            }

            update_data["puzzles_played"] = firestore.ArrayUnion([puzzle_entry])
            update_data["unique_puzzles"] = firestore.ArrayUnion([puzzle_id])

        user_doc.reference.update(update_data)
        update_user_exp_local(points_to_add)

    except Exception as e:
        print(f"❌ Failed to update EXP or puzzle stats: {e}")


def update_user_exp_local(points: int):
    st.session_state.points = st.session_state.get('points', 0) + points

# Load and combine tasks
def load_tasks():
    all_tasks = []
    for task_type, file_path in TASK_FILES.items():
        with open(file_path, 'r') as f:
            tasks = json.load(f)
        # Validate tasks
        for task in tasks:
            task["task_type"] = task_type
            if task["type"] == "fill_in_blank":
                num_blanks = task["question_template"].count("___")
                if num_blanks != len(task["correct_sequence"]):
                    raise ValueError(f"Task ID {task['id']} ({task_type}): Number of blanks ({num_blanks}) does not match correct_sequence length ({len(task['correct_sequence'])})")
            elif task["type"] == "multiple_choice":
                if not (3 <= len(task["options"]) <= 5):
                    raise ValueError(f"Task ID {task['id']} ({task_type}): Number of options ({len(task['options'])}) must be between 3 and 5")
                if task["correct_answer"] not in task["options"]:
                    raise ValueError(f"Task ID {task['id']} ({task_type}): Correct answer ({task['correct_answer']}) not in options")
                if "description" not in task:
                    raise ValueError(f"Task ID {task['id']} ({task_type}): Missing description field")
        all_tasks.extend(tasks)
    # Ensure unique IDs
    seen_ids = set()
    for task in all_tasks:
        if task["id"] in seen_ids:
            raise ValueError(f"Duplicate task ID {task['id']} found")
        seen_ids.add(task["id"])
    return all_tasks

# Get a specific task
def get_task(task_id, task_type):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id and task["task_type"] == task_type:
            return task
    raise ValueError(f"Task ID {task_id} with type {task_type} not found")

# Initialize or get next task
def initialize_or_next_task():
    st.session_state.task_start_time = time.time()
    if "task_queue" not in st.session_state or not st.session_state.task_queue:
        tasks = load_tasks()
        if not tasks:
            st.session_state.completed = True
            return None
        task_queue = [(task["id"], task["task_type"]) for task in tasks]
        shuffle(task_queue)
        st.session_state.task_queue = task_queue
    task_id, task_type = st.session_state.task_queue.pop(0)
    if not st.session_state.task_queue:
        st.session_state.completed = True
    task = get_task(task_id, task_type)
    st.session_state.task = task
    st.session_state.task_id = task["id"]
    st.session_state.task_type = task_type
    return task

# Fill-in-the-blank task display
def display_fill_in_the_blank(task):
    st.write("### Complete the code:")
    st.write(f"**Points for this question: {task['points']}**")
    st.write("#### 📝 Task Instructions:")
    st.info(task.get("description", "Fill in the blanks with the correct words."))

    num_blanks = len(task["correct_sequence"])
    options = task["options"]

    # Initialize session state
    if "task_id" not in st.session_state or st.session_state.task_id != task["id"] or "selected_words" not in st.session_state:
        st.session_state.task_id = task["id"]
        st.session_state.selected_words = [None] * num_blanks
        st.session_state.active_buttons = [False] * len(options)
    elif len(st.session_state.selected_words) != num_blanks or len(st.session_state.active_buttons) != len(options):
        st.session_state.selected_words = [None] * num_blanks
        st.session_state.active_buttons = [False] * len(options)

    # Build display
    display_template = task["question_template"]
    parts = display_template.split("___")
    if len(parts) != num_blanks + 1:
        st.error(f"Error: Task ID {task['id']} has {len(parts)-1} blanks but {num_blanks} expected.")
        return

    display_text = ""
    for i in range(num_blanks):
        display_text += parts[i]
        display_text += st.session_state.selected_words[i] if st.session_state.selected_words[i] else "___"
    display_text += parts[-1]
    st.code(display_text, language="python")

    st.write("### Select words:")
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        if cols[i].button(option, key=f"btn_{task['id']}_{i}"):
            if st.session_state.active_buttons[i]:
                if option in st.session_state.selected_words:
                    index = st.session_state.selected_words.index(option)
                    st.session_state.selected_words[index] = None
                st.session_state.active_buttons[i] = False
            else:
                try:
                    slot = st.session_state.selected_words.index(None)
                    st.session_state.selected_words[slot] = option
                    st.session_state.active_buttons[i] = True
                except ValueError:
                    pass
            st.rerun()

    if st.button("Check Answer"):
        is_correct = st.session_state.selected_words == task["correct_sequence"]
        #update_points(task, is_correct)
        if is_correct:
            st.success(f"✅ Correct! +{task['points']} points")
            update_user_exp(task['points'], puzzle_id=task['id'])
            time.sleep(1)
            st.session_state.selected_words = [None] * num_blanks
            st.session_state.active_buttons = [False] * len(options)
            initialize_or_next_task()
            st.rerun()
        else:
            st.error(f"❌ Incorrect.")
            st.session_state.selected_words = [None] * num_blanks
            st.session_state.active_buttons = [False] * len(options)

# Multiple-choice task display
def display_multiple_choice(task):
    st.write("### Multiple Choice Question")
    st.write(f"**Points for this question: {task['points']}**")
    st.write("#### 📝 Task Instructions:")
    st.info(task.get("description", "Answer the question based on the code below."))
    st.code(task["question"], language="python")
    choice = st.radio("Choose one:", task["options"], key=f"mc_choice_{task['id']}")
    if st.button("Submit Answer"):
        is_correct = choice == task["correct_answer"]
        #update_points(task, is_correct)
        if is_correct:
            st.success(f"✅ Correct! +{task['points']} points")
            update_user_exp(task['points'], puzzle_id=task['id'])
            time.sleep(1)
            initialize_or_next_task()
            st.rerun()
        else:
            st.error(f"❌ Incorrect")

# Completion page
def display_completion_page():
    st.write("### 🎉 Congratulations!")
    st.write(f"You've completed all tasks!")
    st.balloons()
    if st.button("Start Over"):
        # Clear all puzzle-related session state
        keys_to_clear = [
            "task", "task_id", "task_type", "task_queue", "completed",
            "selected_words", "active_buttons", "task_start_time"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]

        initialize_or_next_task()
        st.rerun()


# UI
st.title("Python Learning Tasks")
st.sidebar.header("Progress")
st.sidebar.write(f"Points: {st.session_state.get('points', 0)}")

# Initialize points
initialize_points()

# Display completion page or current task
if "task" not in st.session_state and "completed" not in st.session_state:
    initialize_or_next_task()

if "completed" in st.session_state and st.session_state.completed:
    display_completion_page()
elif "task" in st.session_state:
    task = st.session_state.task
    if task["task_type"] == "fill_in_the_blank":
        display_fill_in_the_blank(task)
    elif task["task_type"] == "multiple_choice":
        display_multiple_choice(task)