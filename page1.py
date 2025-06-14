import streamlit as st
import time
from utils.cookies.cookieManager import delete_cookie
from utils.encryption import decrypt_message
from firebase_admin import firestore

# Initialize variables
db = firestore.client()

cookies = st.session_state.get("cookies")
username = decrypt_message(cookies.get("username") if cookies else None)

if username:
    try:
        # get user data from the database
        users_ref = db.collection("users")
        query = users_ref.where("username", "==", username).limit(1).stream()
        for doc in query:
            user_data = doc.to_dict()
            break
        
        # Load user data into session state
        st.session_state.cleared_questions = set(user_data.get("cleared_questions", []))
        st.session_state.points = user_data.get('exp', 0)
        st.session_state.username = username
        st.session_state.elo = user_data.get('elo', 0)

        # Display home page content
        
        st.title(f"Welcome back, {username}!")
        st.write("Whether you’ve never written a line of code or you’re looking to sharpen your Python skills, this platform is built for you. Learn at your own pace, test your knowledge, and experiment freely—all in one place")
        
        with st.expander("Learn Python One Topic At a Time", icon="👨‍🏫"):
            st.write("Dive into structured chapters that break down Python concepts step by step. Each section teaches a key topic, where you can learn about it and test your knowledge through an exercise. When your done, you may go to the next one - or if you know it already you can always skip it and go to one more complex topic. You can always go back to sections you already done to refresh your knowledge. ")
            if st.button("Go check the topics!", use_container_width=True):
                st.switch_page("chapter_menu.py")
        with st.expander("Challenge Yourself Through Our Quizzes", icon="✍️"):
            st.write("Put your knowledge to the test with our chapter-based puzzles! Choose from different difficulty levels and solve coding tasks tailored to each concept you learn. After completing a quiz, you can see the points you gained and you can do it again to increase them. The more you practice, the sharper your skills become!")
            if st.button("Go check the quizzes!", use_container_width=True):
                st.switch_page("task.py")
        with st.expander("Code Freely In Our Playground Editor", icon="👨‍💻"):
            st.write("Experiment freely in our interactive code editor - your personal sandbox for Python exploration! Write code, test ideas, and see instant results without any restrictions.")
            if st.button("Go check the playground!", use_container_width=True):
                st.switch_page("playground.py")
        with st.expander("Get Instant Help From Our ChatBot", icon="🤖"):
            st.write("Stuck on a quiz question? Need help with playground code? Our AI assistant is here for you 24/7. It can explain tricky concepts, recommend helpful Python tutorials, and even debug your code - making it the perfect learning companion for every step of your coding journey.")
            if st.button("Go check the agent!", use_container_width=True):
                st.switch_page("agent.py")
    except Exception as e:
        st.error(f"Error loading user data: {e}")
else:
    st.error("Error decrypting username. Please log in again.")

if st.button("Logout", use_container_width=True):
    # Clear session state
    st.session_state.user = None
    st.session_state.cookies = None
    st.session_state.user_token = None

    # Clear cookies
    delete_cookie("user_token")
    delete_cookie("refresh_token")
    delete_cookie("username")

    # Give time for the cookies to be deleted
    time.sleep(0.5)

    # Rerun the app to send the user to the login page
    st.rerun()
