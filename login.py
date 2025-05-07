import streamlit as st
import time
from utils.firebase import auth
from utils.cookies.cookieManager import set_cookie
from utils.encryption import encrypt_message
from datetime import datetime
from firebase_admin import firestore

db = firestore.client()

# get user cookies
cookies = st.session_state.cookies

st.title("🔑 Login to Python Learning App")

tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pw")
    
    if st.button("Sign In"):
        try:
            user = auth.sign_in_with_email_and_password(email, password) # get user with email and password
            # Get UID from token
            user_info = auth.get_account_info(user["idToken"])
            uid = user_info["users"][0]["localId"]

            # Fetch username from Firestore
            user_doc = db.collection("users").document(uid).get()
            username = user_doc.to_dict().get("username") if user_doc.exists else None
            st.session_state.username = username

            # set user token in cookies(remember to encrypt it)
            set_cookie("user_token", encrypt_message(user["idToken"]))
            set_cookie("refresh_token", encrypt_message(user["refreshToken"]))
            set_cookie("username", encrypt_message(username))
            time.sleep(0.5) # Give time for the cookies to be set
            
            st.session_state.user = user
            st.session_state.cookies["username"] = encrypt_message(username)
            st.rerun()
        
        except Exception as e:
            st.error(f"Login failed: {str(e)}")

with tab_register:
    new_email = st.text_input("Email", key="reg_email")
    new_username = st.text_input("Username", key="reg_username")  # New field
    new_pw = st.text_input("Password", type="password", key="reg_pw")
    confirm_pw = st.text_input("Confirm Password", type="password", key="confirm_pw")
    
    if st.button("Create Account"):
        if new_pw != confirm_pw:
            st.error("Passwords don't match!")
        elif not new_username:
            st.error("Please enter a username.")
        else:
            try:
                user = auth.create_user_with_email_and_password(new_email, new_pw)

                # Get the UID from the ID token
                user_info = auth.get_account_info(user["idToken"])
                uid = user_info["users"][0]["localId"]

                # Save user data to Firestore
                db.collection("users").document(uid).set({
                    "email": new_email,
                    "username": new_username,
                    "date_created": datetime.utcnow(),
                    "exp": 0,
                    "elo": 0,
                    "puzzles_played": [],
                    "unique_puzzles": [],
                    "chapter.question": []
                })

                st.success("Account created! Please login.")
            except Exception as e:
                st.error(f"Registration failed: {str(e)}")
