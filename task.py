import streamlit as st
from task_utils import initialize_or_next_task, display_completion_page, display_fill_in_the_blank, display_multiple_choice, display_code_output, clear_quiz
from task_utils import get_suggestion

st.title("Pylearn quiz!")

st.sidebar.header("Progress")
st.sidebar.write(f"Points: {st.session_state.get('points', -1)}")
st.sidebar.write(f"ELO: {st.session_state.get('elo', -1)}")

if not st.session_state.get("quiz_started", False):

    CHAPTER_MAP = {
        "All Chapters": None,
        "Chapter 1 – Basic Concepts": 1,
        "Chapter 2 – Basic Data Types": 2,
        "Chapter 3 – If-Else": 3,
        "Chapter 4 – Loops": 4,
    }

    DIFFICULTY_MAP = {
        "Easy": "Easy",
        "Medium": "Medium",
        "Hard": "Hard"
    }

    chapter_options    = list(CHAPTER_MAP.keys())
    difficulty_options = list(DIFFICULTY_MAP.keys())
    default_ch_index   = 0
    default_diff_index = 0

    try:
        suggested_ch, suggested_diff = get_suggestion()

        # map chapter suggestion → index in chapter_options
        for i, key in enumerate(chapter_options):
            ch_val = CHAPTER_MAP[key]
            if (suggested_ch == 0 and ch_val is None) or ch_val == suggested_ch:
                default_ch_index = i
                break

        # map difficulty suggestion → index in difficulty_options
        for i, key in enumerate(difficulty_options):
            if key == suggested_diff:
                default_diff_index = i
                break
    except Exception as e:
        print("Suggestion error:", e)

    choice = st.selectbox(
        "Select a chapter:",
        chapter_options,
        index=default_ch_index,
        key="chapter_selector_main",
    )

    choice2 = st.selectbox(
        "Select difficulty:",
        difficulty_options,
        index=default_diff_index,
        key="difficulty_selector_main",
    )

    selected_chapter = CHAPTER_MAP[choice]
    selected_difficulty = DIFFICULTY_MAP[choice2]

    # Save selection so the quiz engine can see it later
    st.session_state.active_chapter = selected_chapter
    st.session_state.active_difficulty = selected_difficulty

    # Intro text
    if selected_chapter is None:
        st.markdown("### Test your skills on everything you’ve learned!")
    else:
        st.markdown(f"### Test your skills on Chapter {selected_chapter}")

    if st.button("Start Quiz", type="primary"):
        st.session_state.quiz_started = True
        initialize_or_next_task()      # first question
        st.rerun()                     # rebuild page without the intro

    st.stop()  # don’t render anything else until the quiz starts

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

    if st.button("Exit Quiz", type="primary"):
        clear_quiz()
        st.rerun()