import streamlit as st
from questions import get_question_data
from code_editor import setup_code_editor
from firebase_admin import firestore
import time

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
    st.session_state.timer_start = time.time()

    # difficulty handling
    if 'difficulty_new' not in st.session_state: st.session_state.difficulty_new = st.session_state.difficulty
    if st.session_state.difficulty_new != st.session_state.difficulty:
        st.session_state.changed_difficulty = True
        st.session_state.difficulty = st.session_state.difficulty_new
        st.session_state.timer_queue = [] # reset the timer queue when the difficulty is changed to remove irrelevant data

def load_chapter_question():
    if st.session_state.current_chapter == None: raise ValueError("current_chapter is not set. Please set it before loading a question.")
    if st.session_state.current_question == None: raise ValueError("current_question is not set. Please set it before loading a question.")
    if st.session_state.max_question == None: raise ValueError("max_question is not set. Please set it before loading a question.")
    if 'difficulty' not in st.session_state: st.session_state.difficulty = 1  # default to medium difficulty if not set

    if 'timer_start' not in st.session_state: st.session_state.timer_start = time.time()

    # apply possible difficulty change
    if 'changed_difficulty' not in st.session_state: st.session_state.changed_difficulty = False
    if st.session_state.changed_difficulty:
        st.info(f"{st.session_state.difficulty_message} You can always change the learning mode back using the dropdown in the top right corner.")
        st.session_state.difficulty_message = ""
        st.session_state.changed_difficulty = False

    #setup navigation buttons
    colA, colB, _, colD = st.columns([0.2, 0.2, 0.3, 0.3])

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

        # Difficulty selector
        with colD:
            options = ["Begginer", "Normal", "Programmer"]
            st.selectbox(
                "Learning Mode",
                options=options,
                index=st.session_state.difficulty,
                key="difficulty_option",
                on_change=reset_question_state, # reset question related variables when the difficulty is changed
            )
            if st.session_state.difficulty != options.index(st.session_state.difficulty_option):  # check if the difficulty has changed
                st.session_state.difficulty = options.index(st.session_state.difficulty_option)
                st.session_state.difficulty_new = st.session_state.difficulty
                reset_question_state()
                st.rerun()  # rerun the app to update the question data
            
    # get chapter/question data from question.py
    get_question_data(st.session_state.current_chapter, st.session_state.current_question, st.session_state.difficulty)

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
        
        # timer logic to decide posible difficulty changes
        if 'timer_queue' not in st.session_state: st.session_state.timer_queue = []
    
        timer_stop = time.time()  # get the current time
        time_taken = timer_stop - st.session_state.timer_start  # calculate the time taken to complete the question in seconds

        st.session_state.timer_queue.insert(0, time_taken)  # add the time taken to the queue

        # keep the queue size to 3 to only consider the last 3 questions when judging difficulty
        if len(st.session_state.timer_queue) > 3: st.session_state.timer_queue.pop(0)
        
        max_time = max(st.session_state.timer_queue)

        # judge difficulty based on the maximum completion time of the last 3 questions
        if len(st.session_state.timer_queue) == 3:
            if st.session_state.difficulty == 0 and max_time < 60: # difficulty is easy and must be increased
                st.session_state.difficulty_message = "You're moving fast, that's great! We've increased the lessons' complexity a bit to hopefully teach you even more."
                st.session_state.difficulty_new = 1
            elif st.session_state.difficulty == 1 and max_time < 60: # difficulty is medium and must be increased
                st.session_state.difficulty_message = "You seem to already know programming well, so we've adjusted the learning mode to skip the boring stuff and teach you python specifics."
                st.session_state.difficulty_new = 2
            elif st.session_state.difficulty == 1 and max_time > 200: # difficulty is medium and must be decreased
                st.session_state.difficulty_message = "You seem to be struggling a bit. We've simplified the learning mode to help you learn at a more comfortable pace."
                st.session_state.difficulty_new = 0
            elif st.session_state.difficulty == 2 and max_time > 90: # difficulty is hard and must be decreased
                st.session_state.difficulty_message = "This learning mode wasn't meant for you, we've automatically switched you back to the standard one."
                st.session_state.difficulty_new = 1


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