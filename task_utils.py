from datetime import datetime
import streamlit as st
import json
import time
from random import shuffle
from firebase_admin import firestore

db = firestore.client()

# Task files
TASK_FILES = {
    "fill_in_the_blank": "fill_in_the_blank.json",
    "multiple_choice": "multiple_choice.json",
    "code_output": "code_output.json"
}

def difficulty_from_elo(elo: int) -> str:
    """Map an Elo number → 'Easy' | 'Medium' | 'Hard'."""
    if elo < 1400:
        return "Easy"
    elif elo < 1700:
        return "Medium"
    return "Hard"

def update_elo(correct: bool, question_difficulty: str):
    username = st.session_state.get("username")
    diff_to_rating = {"easy": 1200, "medium": 1500, "hard": 1800}
    opp_rating     = diff_to_rating[question_difficulty]

    users_ref = db.collection("users")
    user_doc  = next(users_ref.where("username", "==", username).limit(1).stream(), None)
    if not user_doc:
        return

    old_elo   = st.session_state.get("elo")

    # ----- Elo math -----
    k       = 15
    score   = 1 if correct else 0
    expected= 1 / (1 + 10 ** ((opp_rating - old_elo) / 400))
    new_elo = round(old_elo + k * (score - expected))

    # ----- persist ------
    users_ref.document(user_doc.id).update({"elo": new_elo})
    st.session_state.elo = new_elo
    st.session_state.elo_updated = True

CHAPTER_TOTALS = {1: 5, 2: 5, 3: 6, 4: 6}

# suggest chapter and difficulty
def get_suggestion():
    """
    Suggest (chapter_int, difficulty_str).

    • Chapter  = the one with the **highest % of cleared_questions**
                 (floats like 1.2 → chapter 1, sub-chapter 2).
      – ties: pick the *larger* chapter number.
    • Difficulty = mapped from user's Elo.
    """
    username = st.session_state.get("username")

    users_ref = db.collection("users")
    user_doc  = next(users_ref.where("username", "==", username).limit(1).stream(), None)

    data            = user_doc.to_dict()
    elo             = st.session_state.get("elo")
    cleared_entries = data.get("cleared_questions", [])

    completed = {ch: 0 for ch in CHAPTER_TOTALS}

    for entry in cleared_entries:
        try:
            ch = int(float(entry))
        except (ValueError, TypeError):
            continue                        # skip malformed entries
        if ch in completed:
            completed[ch] += 1

    # if user has ≥3 cleared in every chapter, suggest all chapters
    if all(count >= 2 for count in completed.values()):
        return 0, difficulty_from_elo(elo)   # 0 means all chapters

    percent_done = {
        ch: (completed[ch] / CHAPTER_TOTALS[ch]) * 100
        for ch in CHAPTER_TOTALS
    }

    # if user has ≥60% cleared in every chapter, suggest all chapters
    #if all(pct >=40 for pct in percent_done.values()):
        #return 0, difficulty_from_elo(elo)

    suggested_chapter = max(
        percent_done,
        key=lambda c: (percent_done[c], -c)
    )

    return suggested_chapter, difficulty_from_elo(elo)

# Updates the score, puzzles_played and unique puzzles of the user.
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
        st.session_state.points = st.session_state.get('points', 0) + points_to_add

    except Exception as e:
        print(f"Failed to update EXP or puzzle stats: {e}")

# Load and combine tasks
def load_tasks(chapter: int | None = None):
    all_tasks = []
    for task_type, file_path in TASK_FILES.items():
        with open(file_path, "r") as f:
            tasks = json.load(f)

        for task in tasks:
            task["task_type"] = task_type

            # CHAPTER FILTER
            task_chapter = task.get("chapter")
            if chapter is not None:
                if isinstance(task_chapter, list):
                    if chapter not in task_chapter:
                        continue
                elif task_chapter != chapter:
                    continue

            # (existing per-type validation goes here)

            all_tasks.append(task)      # ← only the vetted task

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
    chapter = st.session_state.get("active_chapter")
    st.session_state.task_start_time = time.time()
    st.session_state.show_next_button = False
    if "task_queue" not in st.session_state or not st.session_state.task_queue:
        tasks = load_tasks(chapter)
        if not tasks:
            st.session_state.completed = True
            return None
        task_queue = [(task["id"], task["task_type"]) for task in tasks]
        shuffle(task_queue)
        task_queue = task_queue[:5]
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
        if cols[i].button(option, key=f"btn_{task['id']}_{i}", disabled=st.session_state.get("show_next_button", False)):
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

    if st.button("Submit Answer", disabled=st.session_state.get("show_next_button", False)):
        is_correct = st.session_state.selected_words == task["correct_sequence"]

        if not st.session_state.get("elo_updated", False):
            update_elo(
                correct = is_correct,
                question_difficulty = task.get("difficulty")
            )

        if is_correct:    
            update_user_exp(task['points'], puzzle_id=task['id'])
            st.session_state.show_next_button = True

        else:
            #st.error(f"Incorrect.")
            st.session_state.last_answer_incorrect = True
            st.session_state.show_toast = True
            st.session_state.selected_words = [None] * num_blanks
            st.session_state.active_buttons = [False] * len(options)
        
        st.rerun()

    # Show toast (incorrect message) if wrong answer was submitted
    if st.session_state.get("show_toast", False):
        st.session_state.show_toast = False
        st.toast("Incorrect")

    # Show Explain button if wrong answer was submitted
    if st.session_state.get("last_answer_incorrect", False):
        if st.button("Explain", key=f"explain_{task['id']}", help="Get help from the agent for this task", disabled=st.session_state.get("show_next_button", False)):
            st.session_state.explain_task = task["id"]
            st.session_state.last_answer_incorrect = False
            st.switch_page("agent.py")

    # Show Next button if correct answer was submitted
    if st.session_state.get("show_next_button", False):
        st.success(f"Correct! +{task['points']} points")
        if st.button("Next"):
            st.session_state.selected_words = [None] * num_blanks
            st.session_state.active_buttons = [False] * len(options)
            st.session_state.last_answer_incorrect = False
            st.session_state.elo_updated = False
            initialize_or_next_task()
            st.rerun()

# Multiple-choice task display
def display_multiple_choice(task):
    st.write("### Multiple Choice Question")
    st.write(f"**Points for this question: {task['points']}**")
    st.info(task.get("description", "Answer the question based on the code below."))
    st.code(task["question"], language="python")
    choice = st.radio("Choose one:", task["options"], key=f"mc_choice_{task['id']}", disabled=st.session_state.get("show_next_button", False))

    if st.button("Submit Answer", disabled=st.session_state.get("show_next_button", False)):
        is_correct = choice == task["correct_answer"]

        if not st.session_state.get("elo_updated", False):
            update_elo(
                correct = is_correct,
                question_difficulty = task.get("difficulty")
            )

        if is_correct:
            update_user_exp(task['points'], puzzle_id=task['id'])
            st.session_state.show_next_button = True

        else:
            #st.error(f"Incorrect")
            st.session_state.last_answer_incorrect = True
            st.session_state.show_toast = True

        st.rerun()

    # Show toast (incorrect message) if wrong answer was submitted
    if st.session_state.get("show_toast", False):
        st.session_state.show_toast = False
        st.toast("Incorrect")

    # Show Explain button if wrong answer was submitted
    if st.session_state.get("last_answer_incorrect", False):
        if st.button("Explain", key=f"explain_{task['id']}", help="Get help from the agent for this task", disabled=st.session_state.get("show_next_button", False)):
            st.session_state.explain_task = task["id"]
            st.session_state.last_answer_incorrect = False
            st.switch_page("agent.py")

        # Show Next button if correct answer was submitted
    if st.session_state.get("show_next_button", False):
        st.success(f"Correct! +{task['points']} points")
        if st.button("Next"):
            st.session_state.last_answer_incorrect = False
            st.session_state.elo_updated = False
            initialize_or_next_task()
            st.rerun()

# Replace the existing display_code_output function with this corrected version
def display_code_output(task):
    st.write("### What would the following code print?")
    st.write(f"**Points for this question: {task['points']}**")
    st.write("#### 📝 Task Instructions:")
    st.info(task.get("description", "Enter the exact output of the code below."))

    # Display the code
    st.code(task["code"], language="python")

    # Initialize session state for user input if not already set
    if "user_output" not in st.session_state or "task_id" not in st.session_state or st.session_state.task_id != task["id"]:
        st.session_state.task_id = task["id"]
        st.session_state.user_output = ""

    # Text input for user's answer
    user_input = st.text_area("Enter the output:", value=st.session_state.user_output, key=f"output_{task['id']}", disabled=st.session_state.get("show_next_button", False))
    st.session_state.user_output = user_input

    if st.button("Submit Answer", disabled=st.session_state.get("show_next_button", False)):
        if st.session_state.get("show_next_button", False):
            pass

        # Normalize user input and correct output (strip whitespace, convert to string)
        user_answer = str(user_input).strip()
        correct_answer = str(task["correct_output"]).strip()
        is_correct = user_answer == correct_answer

        if not st.session_state.get("elo_updated", False):
            update_elo(
                correct = is_correct,
                question_difficulty = task.get("difficulty")
            )

        if is_correct:
            update_user_exp(task['points'], puzzle_id=task['id'])
            st.session_state.show_next_button = True
            
        else:
            st.session_state.last_answer_incorrect = True
            st.session_state.show_toast = True

        st.rerun()

    # Show toast (incorrect message) if wrong answer was submitted
    if st.session_state.get("show_toast", False):
        st.session_state.show_toast = False
        st.toast("Incorrect")

    # Show Explain button if wrong answer was submitted
    if st.session_state.get("last_answer_incorrect", False):
        if st.button("Explain", key=f"explain_{task['id']}", help="Get help from the agent for this task", disabled=st.session_state.get("show_next_button", False)):
            st.session_state.explain_task = task["id"]
            st.session_state.last_answer_incorrect = False
            st.switch_page("agent.py")

    # Show Next button if correct answer was submitted
    if st.session_state.get("show_next_button", False):
        st.success(f"Correct! +{task['points']} points")
        if st.button("Next"):
            st.session_state.user_output = ""
            st.session_state.last_answer_incorrect = False
            st.session_state.elo_updated = False
            initialize_or_next_task()
            st.rerun()

# Completion page
def display_completion_page():
    st.write("### Congratulations!")
    st.write(f"You've completed all tasks!")
    st.balloons()
    if st.button("Return to menu"):
        clear_quiz()

def clear_quiz():
    keys_to_clear = [
        "task", "task_id", "task_type", "task_queue", "completed",
        "selected_words", "active_buttons", "task_start_time",
        "user_output", "show_next_button", "last_answer_incorrect",
        "show_toast", "quiz_started", "active_chapter", 
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()
