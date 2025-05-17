import streamlit as st
from questions import chapters
from streamlit_extras.stylable_container import stylable_container
from question import load_chapter_question

def load_chapter_menu():

    width_ratio = 0.8
    _, col, _ = st.columns([(1-width_ratio)/2, width_ratio, (1-width_ratio)/2])

    with col:
            
        st.title("Learn Python")

        # Dropdown in main page
        selected_chapter = st.selectbox(
            "select chapter",
            options=[chapters[i]["title"] for i in chapters.keys()],
            index=0,
            key="chapter_select"
        )
        chapter_index = {chapters[i]["title"]: i for i in chapters.keys()}[selected_chapter]

        # Show selected chapter content
        st.subheader(selected_chapter)
        st.write(chapters[chapter_index]["description"])


    width_ratio = 0.5
    _, col, _ = st.columns([(1-width_ratio)/2, width_ratio, (1-width_ratio)/2])

    with col:
        for i in chapters[chapter_index]["questions"].keys():
            question = chapters[chapter_index]["questions"][i]

            # using stylable_container to make to button green if it's first on the list
            color = "background-color: #76C776;" if float(str(chapter_index) + "." + str(i)) in st.session_state.cleared_questions else ""

            with stylable_container(
                key=f"button{i}", 
                css_styles="""
                    button {"""
                        +color+\
                        """
                        border-radius: 20px;
                    }
                """
                ):
                st.button(f"{i}. {question}", key=f"button_{i}", on_click=load_question, args=(chapter_index, i), use_container_width=True)


def load_question(chapter: int, question: int):
    st.session_state.chapter_menu = False
    st.session_state.current_chapter = chapter
    st.session_state.current_question = question
    st.session_state.max_question = len(chapters[chapter]["questions"])
    

if st.session_state.get("chapter_menu", True):
    load_chapter_menu()
else:
    load_chapter_question()