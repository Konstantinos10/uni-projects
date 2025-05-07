import streamlit as st
import time
from utils.cookies.cookieManager import delete_cookie
from utils.encryption import decrypt_message
from utils.cookies.cookieManager import get_cookies
from firebase_admin import firestore

db = firestore.client()

cookies = st.session_state.get("cookies")
encrypted_username = cookies.get("username") if cookies else None
if encrypted_username:
    try:
        username = decrypt_message(encrypted_username)
        users_ref = db.collection("users")
        query = users_ref.where("username", "==", username).limit(1).stream()
        for doc in query:
            user_data = doc.to_dict()
            break

        st.title(f"Welcome back, {username}!")
        st.write(f"**EXP**: {user_data.get('exp', 0)}")
        st.write(f"**ELO**: {user_data.get('elo', 0)}")
        st.write(f"**Joined**: {user_data.get('date_created', '').strftime('%Y-%m-%d')}")

        st.session_state.points = user_data.get('exp', 0)
        st.session_state.username = username

    except Exception as e:
        st.error(f"Failed to decrypt username: {e}")
else:
    st.info("Loading user session...")
    st.rerun()

if st.button("Logout"):
    st.session_state.user = None
    st.session_state.cookies = None
    st.session_state.user_token = None

    delete_cookie("user_token")
    delete_cookie("refresh_token")
    time.sleep(0.5)
    st.rerun()
