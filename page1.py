import streamlit as st
import time
from utils.cookies.cookieManager import delete_cookie

# Sidebar - User Profile & Navigationwith st.sidebar:
st.title("page title")
st.markdown("### Καλωσόρισες, Μαθητή!")

if st.button("Logout"):
    st.session_state.user = None
    st.session_state.cookies = None
    st.session_state.user_token = None

    delete_cookie("user_token")
    delete_cookie("refresh_token")
    time.sleep(0.5)
    st.rerun()
