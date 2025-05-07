import streamlit as st
from questions import chapters

def load_question(chapter: int, question: int):
    st.write(f"Loading question {question} from chapter {chapter}...")


st.title("Κεφάλαια⭐")

# Dropdown in main page
selected_chapter = st.selectbox(
    "Παρακάτω κεφάλαια:",
    options=[chapters[i]["title"] for i in chapters.keys()],
    index=0,
    key="chapter_select"
)
chapter_index = {chapters[i]["title"]: i for i in chapters.keys()}[selected_chapter]


# Show selected chapter content
st.subheader(selected_chapter)

jvs =  """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.stButton > button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            buttons.forEach(btn => {
                btn.style.backgroundColor = '#FFFFFF';
            });
            this.style.backgroundColor = '#C1FFC1';
        });
    });
});
</script>
"""

st.html(jvs)

st.write(chapters[chapter_index]["description"])

for i in chapters[chapter_index]["questions"].keys():
    question = chapters[chapter_index]["questions"][i]
    st.button(f"{i}. {question}", key=f"button_{i}", on_click=load_question, args=(chapter_index, i))

st.html("""
<style>
    .stButton>button {
        width: 80%;
        padding: 10px;
        margin: 2px 0;
        background-color: #FFFFFF;  
        color: #000000; 
        border: 1px solid #76C776;
        transition: all 0.3s ease;  
    }
            .stButton>button:active, .stButton>button:focus {
        background-color: #C1FFC1 !important;
    }
</style>
""")
