# main.py
import streamlit as st
import pyrebase
from private.firebase_config import firebaseConfig  # Import your config

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Session state to track login status
if 'user' not in st.session_state:
    st.session_state.user = None

# Auth UI
def show_login():
    st.title("🔑 Login to Python Learning App")
    
    tab_login, tab_register = st.tabs(["Login", "Register"])
    
    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pw")
        
        if st.button("Sign In"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")
    
    with tab_register:
        new_email = st.text_input("Email", key="reg_email")
        new_pw = st.text_input("Password", type="password", key="reg_pw")
        confirm_pw = st.text_input("Confirm Password", type="password", key="confirm_pw")
        
        if st.button("Create Account"):
            if new_pw != confirm_pw:
                st.error("Passwords don't match!")
            else:
                try:
                    user = auth.create_user_with_email_and_password(new_email, new_pw)
                    st.success("Account created! Please login.")
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")

# Main App (protected content)
def show_app():
    st.title(f"📚 Welcome, {st.session_state.user['email']}!")
    st.button("Logout", on_click=lambda: st.session_state.clear())
    
    # YOUR ACTUAL APP CONTENT GOES HERE
    st.success("You're now logged in! Add your app content here.")

# Router
if st.session_state.user:
    st.switch_page("main.py")
else:
    show_login()