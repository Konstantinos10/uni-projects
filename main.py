import streamlit as st
import time
from utils.firebase import auth
from utils.logger import log
from utils.cookies.cookieManager import get_cookies, set_cookie
from utils.encryption import encrypt_message, decrypt_message

st.set_page_config(layout="wide")

# get user cookies
if "cookies" not in st.session_state or st.session_state.cookies == None:
    cookies = get_cookies()
    if cookies == None:
        st.stop() #don't run app until cookies are set
    st.session_state.cookies = cookies
cookies = st.session_state.cookies


#Initialize session state + try to get logged in user using cookies
if 'user' not in st.session_state or st.session_state.user == None:
    st.session_state.user = token = None
    if "user_token" in cookies: token = decrypt_message(cookies["user_token"])

    #user can be logged in if token is set
    if token:
        # get user with token
        try:
            user = auth.get_account_info(token)
            st.session_state.user = user

        except: 
            # if token is invalid, try to refresh it
            try:
                refresh_token = decrypt_message(cookies["refresh_token"])   # get refresh token from cookies
                user = auth.refresh(refresh_token)                          # use refresh token to get new user token
                set_cookie("user_token", encrypt_message(user["idToken"]))  # set new user token in cookies(remember to encrypt it)
                time.sleep(0.5)                                             # Give time for the cookie to be set
                st.session_state.user = user
            except Exception as e:
                log("Couldn't get user with refresh token, going to login page: " + str(e))
                st.session_state.user = None


# set available pages based on login status
if st.session_state.user:
    pages = {
    "" : [st.Page("page1.py", title="home"),
          st.Page("question.py", title="Question")]
          }
else:
    pages = [st.Page("login.py", title="Login Page")]

pg = st.navigation(pages)
pg.run()