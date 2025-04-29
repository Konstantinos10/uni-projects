import streamlit as st
from streamlit_ace import st_ace
import subprocess
import tempfile
import os

st.title("Python Learning Apps")

if 'question' not in st.session_state:
    st.session_state.question = "Write a Python script that prints the square of 4."

st.subheader("Question:")
st.write(st.session_state.question)

# Spawn a new Ace editor
content = st_ace(
    language="python",
    theme="dracula",
    keybinding="vscode",
    height=300,
    auto_update=True,
    show_gutter=True,
    show_print_margin=True,
    wrap=True,
    min_lines=10,
    max_lines=20,
)

if st.button("Run Code"):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        result = subprocess.run(
            ["python", tmp_file_path],
            capture_output=True,
            text=True,
            timeout=1
        )
        if result.stdout:
            st.success("Output:")
            st.code(result.stdout, language="python")
        if result.stderr:
            st.error("Error:")
            st.code(result.stderr, language="python")
        if not result.stdout and not result.stderr:
            st.info("No output was produced.")
    except subprocess.TimeoutExpired:
        st.error("Error: Code execution timed out.")
    finally:
        os.remove(tmp_file_path)
