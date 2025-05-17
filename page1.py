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

        # Display user data
        st.title(f"Welcome back, {username}!")
        st.write(f"**EXP**: {user_data.get('exp', 0)}")
        st.write(f"**ELO**: {user_data.get('elo', 0)}")
        st.write(f"**Joined**: {user_data.get('date_created', '').strftime('%Y-%m-%d')}")


    except Exception as e:
        st.error(f"Error loading user data: {e}")
else:
    st.error("Error decrypting username. Please log in again.")

if st.button("Logout"):
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
