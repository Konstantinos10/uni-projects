import streamlit as st
from streamlit_ace import st_ace
import subprocess
import tempfile
import os

def run_code(code: str) -> tuple[str, str]:
    """
    Run the provided code by executing it and capturing stdout and stderr.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
        tmp_file.write(code)
        tmp_file_path = tmp_file.name
    try:
        result = subprocess.run(
            ["python", tmp_file_path],
            capture_output=True,
            text=True,
            timeout=1
        )
        stderr = result.stderr.replace("C:\\Users\\KONSTA~1\\AppData\\Local\\", "")  # Replace newlines with spaces in stderr
        return result.stdout, stderr
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out."
    finally:
        os.remove(tmp_file_path)


def setup_code_editor():
    
    #if requested, create a new key for the editor to force it to reload(usefull in case we want to set the editor content(there's probably a better way to do this but I haven't found it yet(TODO:find one)))
    if st.session_state.get("reload_editor", False):
        st.session_state.editor_key_counter = st.session_state.get("editor_key_counter", 0) + 1
        st.session_state.reload_editor = False

    col1, col2 = st.columns([0.6, 0.4])  # Adjust ratios as needed

    with col1:
        # Spawn and initialize a new Ace editor
        content = st_ace(
            value=st.session_state.get("editor_content", ""),
            placeholder="Write your code here...",
            height=300,
            language="python",
            theme=st.session_state.get("editor_theme", "dracula"),
            wrap=True,
            auto_update=True,
            key="ace_editor" + str(st.session_state.get("editor_key_counter", 0)) # required for the editor content to persist reruns
        )

    with col2:
        # Display the output of the code execution
        output = str(st.session_state.get('stdout', "")) +\
                str(st.session_state.get('stderr', ""))
        st.code(output, language=None, height=300)


    colA, colB, colC, colD = st.columns([0.15, 0.60, 0.1, 0.15]) #ratios are assuming previous column set in 0.6-0.4

    # editor theme selector
    with colA:
        options = ["dracula", "chrome", "terminal", "solarized_light"] # list of available themes
        index = options.index(st.session_state.get("editor_theme", "dracula")) # index of current theme in the list(needed so the editor keeps the same theme after a page change)

        # selectbox to choose a theme
        theme = st.selectbox(label="selectbox", options=options, index=index, label_visibility="collapsed")

        # if the selected theme is different from the current theme, the user has changed it and a rerun is needed
        if theme != st.session_state.get("editor_theme", "dracula"):
            st.session_state.editor_theme = theme
            st.rerun() # reload the editor with the new theme
        
        st.session_state.editor_theme = theme
        
    # button to execute user code
    with colC:
        if st.button("Run Code", use_container_width=True):
            st.session_state.stdout, st.session_state.stderr = run_code(content)
            st.rerun()  # Rerun the app to update the output area(becomes redundant the file is refactored and the output area is defined below the editor)
