import streamlit as st
from streamlit_ace import st_ace
import subprocess
import tempfile
import os
from utils.logger import log

st.title("Python Learning Apps")

if 'question' not in st.session_state:
    st.session_state.question = "Write a Python script that prints the square of 4."

st.subheader("Question:")
st.write(st.session_state.question)

st.divider()

colA, colB, colC, colD = st.columns([0.15, 0.60, 0.1, 0.15]) #ration are assuming next column set in 0.6-0.4

with colA:
    theme = st.selectbox(label="selectbox", placeholder="editor theme", options=["dracula", "chrome", "terminal", "solarized_light"], label_visibility="collapsed") # allow user to select a theme

with colC:
    # Button to execute user code
    if st.button("Run Code", use_container_width=True):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(st.session_state.ace_editor)
            tmp_file_path = tmp_file.name
        try:
            result = subprocess.run(
                ["python", tmp_file_path],
                capture_output=True,
                text=True,
                timeout=1
            )
            st.session_state['stdout'] = result.stdout
            st.session_state['stderr'] = result.stderr
        except subprocess.TimeoutExpired:
            st.session_state['stdout'] = ""
            st.session_state['stderr'] = "Error: Code execution timed out."
        finally:
            os.remove(tmp_file_path)


col1, col2 = st.columns([0.6, 0.4])  # Adjust ratios as needed

with col1:    
    # Spawn and initialize a new Ace editor
    content = st_ace(
        height=300,
        language="python",
        theme=theme,
        wrap=True,
        auto_update=True,
        key="ace_editor" # required for the editor content to persist reruns
    )

with col2:
    # Display the output of the code execution
    output = str(st.session_state.get('stdout', ""))+"\n" +\
            str(st.session_state.get('stderr', ""))
    st.code(output, language=None, height=300)