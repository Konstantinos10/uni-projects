import streamlit as st
from questions import get_question_data
from code_editor import setup_code_editor


def reset_question_state():
    st.session_state.editor_content = ""
    st.session_state.stdout = ""
    st.session_state.stderr = ""
    st.session_state.answer = False
    st.session_state.reload_editor = True
    st.rerun()

#setup the previous/next page buttons

# temporary hardcoded values, will be replaced later
if "current_chapter" not in st.session_state or "current_question" not in st.session_state:
    st.session_state.current_question = st.session_state.current_chapter = 1
    st.session_state.max_question = 5 # set this to the number of questions in the chapter


colA, colB = st.columns([0.2, 0.8])

with colA:
    col1, col2 = st.columns([0.5, 0.5])

    ## Previous page button
    with col1:
        if st.button("Previous", disabled=st.session_state.current_question == 1):
            st.session_state.current_question -= 1 # decrement question number
            if st.session_state.current_question < 1: # extra check to make sure the question number is within bounds(needed in case the user clicks the button multiple times before the page disables it)
                st.session_state.current_question = 1
            reset_question_state() # reset question related variables before loading a new question

    # Next page button
    with col2:
        if st.button("Next", disabled=st.session_state.current_question == st.session_state.max_question):
            st.session_state.current_question += 1 # increment question number
            if st.session_state.current_question > st.session_state.max_question: # extra check to make sure the question number is within bounds(needed in case the user clicks the button multiple times before the page disables it)
                st.session_state.current_question = st.session_state.max_question
            reset_question_state() # reset question related variables before loading a new question

get_question_data(st.session_state.current_chapter, st.session_state.current_question) # get chapter/question data from question.py

st.divider()

setup_code_editor() # setup the code editor

if st.session_state.answer:
    st.success("Correct! You may move on to the next question.")