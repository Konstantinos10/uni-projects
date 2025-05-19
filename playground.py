import streamlit as st
from streamlit_ace import st_ace
from code_editor import run_code

st.header("Playground")
st.write("This is an editor where you can write and run any Python code you want, so feel free to expiriment.\n" \
        "You may also ask the chatbot to explain or modify the code it as you wish.")

#if requested, create a new key for the editor to force it to reload(usefull in case we want to set the editor content(there's probably a better way to do this but I haven't found it yet(TODO:find one)))
if st.session_state.get("reload_playground", False):
    st.session_state.editor_key_counter = st.session_state.get("playground_key_counter", 0) + 1
    st.session_state.reload_playground = False

col1, col2 = st.columns([0.6, 0.4])  # Adjust ratios as needed

with col1:
    # Spawn and initialize a new Ace editor
    content = st_ace(
        value=st.session_state.get("playground_content", ""),
        placeholder="Write your code here...",
        height=600,
        language="python",
        theme=st.session_state.get("editor_theme", "dracula"),
        wrap=True,
        auto_update=True,
        key="playground_editor" + str(st.session_state.get("playground_key_counter", 0)) # required for the editor content to persist reruns
    )
    if content != st.session_state.get("playground_content", ""):
        st.session_state.missmatched_output = True
    st.session_state.playground_content = content

with col2:
    # Display the output of the code execution
    output = str(st.session_state.get('p_stdout', "")) +\
            str(st.session_state.get('p_stderr', ""))
    st.code(output, language=None, height=600)


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
        st.session_state.p_stdout, st.session_state.p_stderr = run_code(content)
        st.session_state.missmatched_output = False
        st.rerun()  # Rerun the app to update the output area(becomes redundant the file is refactored and the output area is defined below the editor)