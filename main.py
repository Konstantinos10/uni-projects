import streamlit as st

# Session state to track login status
if 'user' not in st.session_state:
    st.session_state.user = None

if st.session_state.user:
    pages = {
    "" : [st.Page("page1.py", title="Home"),
          st.Page("question.py", title="Question")]
          }
else:
    pages = [st.Page("login.py", title="Login Pages")]

pg = st.navigation(pages)
pg.run()