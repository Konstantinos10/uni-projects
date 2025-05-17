import streamlit as st
from questions import get_question_data
from code_editor import setup_code_editor
from firebase_admin import firestore

db = firestore.client()

def check_chapter_completion():
    # create a list of all questions in the chapter
    chapter_questions = [float(str(st.session_state.current_chapter) + "." + str(i)) for i in range(1, st.session_state.max_question + 1)]
    
    # return False if any question in the chapter is not cleared
    for question in chapter_questions:
        if question not in st.session_state.cleared_questions:
            return False

    # if all questions in the chapter are cleared, return True
    return True

def reset_question_state():
    st.session_state.editor_content = ""
    st.session_state.stdout = ""
    st.session_state.stderr = ""
    st.session_state.answer = False
    st.session_state.reload_editor = True

def load_chapter_question():
    if st.session_state.current_chapter == None: raise ValueError("current_chapter is not set. Please set it before loading a question.")
    if st.session_state.current_question == None: raise ValueError("current_question is not set. Please set it before loading a question.")
    if st.session_state.max_question == None: raise ValueError("max_question is not set. Please set it before loading a question.")

    #setup navigation buttons
    colA, colB, _ = st.columns([0.2, 0.2, 0.6])

    with colA:
        # Menu button
        if st.button("Back to Menu", use_container_width=True):
            reset_question_state() # reset question related variables before loading a new question
            st.session_state.chapter_menu = True # set the chapter menu to True so it loads on the next rerun
            st.rerun()

    with colB:
        col1, col2 = st.columns([0.5, 0.5])

        ## Previous page button
        with col1:
            if st.button("Previous", disabled=st.session_state.current_question == 1, use_container_width=True):
                st.session_state.current_question -= 1 # decrement question number
                if st.session_state.current_question < 1: # extra check to make sure the question number is within bounds(needed in case the user clicks the button multiple times before the page disables it)
                    st.session_state.current_question = 1
                reset_question_state() # reset question related variables before loading a new question
                st.rerun() # rerun the app to update button states

        # Next page button
        with col2:
            if st.button("Next", disabled=st.session_state.current_question == st.session_state.max_question, use_container_width=True):
                st.session_state.current_question += 1 # increment question number
                if st.session_state.current_question > st.session_state.max_question: # extra check to make sure the question number is within bounds(needed in case the user clicks the button multiple times before the page disables it)
                    st.session_state.current_question = st.session_state.max_question
                reset_question_state() # reset question related variables before loading a new question
                st.rerun() # rerun the app to update button states

    # get chapter/question data from question.py
    get_question_data(st.session_state.current_chapter, st.session_state.current_question)

    st.divider()

    # setup the code editor
    setup_code_editor()

    # display a message when the question is cleared
    if st.session_state.answer:

        # get the question key(ex. "2.3")
        completed_question = float(str(st.session_state.current_chapter) +"."+ str(st.session_state.current_question))
        
        # show a simple info message if the question has been cleared before
        if completed_question in st.session_state.cleared_questions:
            st.info("Correct!")
            return

        # update the database and show a success message if the question is cleared for the first time
        try:
            # add cleared question to the database
            users_ref = db.collection("users")
            query = users_ref.where("username", "==", st.session_state.username).limit(1).stream()

            for doc in query:
                doc_ref = users_ref.document(doc.id)
                doc_ref.update({"cleared_questions": list(st.session_state.cleared_questions) + [completed_question] })
                break

            # add the question to the session state(note: do this after updating the database to avoid desync issues in case the update fails)
            st.session_state.cleared_questions.add(completed_question)

            # notify the user(also show balloons on chapter completions)
            if check_chapter_completion():
                st.balloons()
                st.success("Congratulations! You have completed this chapter and may move on to the next one.")
            else:
                st.success("Correct! You may move on to the next question.")

        except Exception as e:
            st.error(f"Failed to update user data: {e}")
            st.session_state.answer = False