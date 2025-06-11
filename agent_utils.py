import streamlit as st
import json
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, SystemMessage
from firebase_admin import firestore
from code_editor import run_code as code_run #epic way to prevent recursion
import random

# Task files (same as in task.py)
TASK_FILES = {
    "fill_in_the_blank": "fill_in_the_blank.json",
    "multiple_choice": "multiple_choice.json",
    "code_output": "code_output.json"
}

# Initialize Firestore client
db = firestore.client()

@tool
def read_playground() -> str:
    """Read the content of the playground code editor and output terminal.
    If the code has run and is not later changed, the standard output and error output are also returned."""

    if st.session_state.get("missmatched_output", False): return {"playground editor": st.session_state.get("playground_content", "INFO: Playground is empty.")},  
    return {"playground editor": st.session_state.get("playground_content", "INFO: Playground is empty."),
            "playground standard output": str(st.session_state.get('p_stdout', "")),
            "playground standard error": str(st.session_state.get('p_stderr', ""))}

@tool
def write_playground(content: str) -> None:
    """Write content to the playground code editor."""
    st.session_state.playground_content = content
    st.session_state.missmatched_output = True
    st.session_state.reload_playground = True

@tool
def run_code(code: str) -> dict:
    """Run the provided python code and return the output.
    Args:
        code (str): The python code to run.
    Returns:
        dict: A dictionary containing the standard output and error output.
    """
    output, error = code_run(code)
    return {"stdout": output, "stderr": error}

@tool
def get_user_data(username: str) -> dict:
    """Fetch completed chapters for the given username from Firestore."""
    try:
        # Query users collection by username field
        users_ref = db.collection("users")
        query = users_ref.where("username", "==", username).limit(1).stream()
        docs = list(query)
        
        if not docs:
            logger.warning(f"No user document found for username: {username}")
            return {"username": username, "completed_chapters": [], "error": "User document not found."}
        
        # Get the first matching document
        user_doc = docs[0]
        logger.info(f"Found user document: {user_doc.id}")
        
        # Retrieve the cleared_questions array field
        user_data = user_doc.to_dict()
        completed_chapters = user_data.get("cleared_questions", [])
        logger.info(f"Completed chapters for {username}: {completed_chapters}")
        
        return {"username": username, "completed_chapters": completed_chapters}
    except Exception as e:
        logger.error(f"Error fetching user data for {username}: {str(e)}")
        return {"username": username, "completed_chapters": [], "error": f"Error fetching user data: {str(e)}"}

@tool
def explain_task(task_id: str, task_type: str) -> str:
    """Retrieve and explain a specific task based on its ID and type, including the correct answer.
    
    Args:
        task_id (str): The ID of the task (e.g., 'fib_ch1_e1', 'mc_ch1_e1', 'co_ch1_e1')
        task_type (str): The type of task ('fill_in_the_blank', 'multiple_choice', 'code_output')
    
    Returns:
        str: A formatted explanation of the task with its details and answer
    """
    try:
        # Validate task_type
        if task_type not in TASK_FILES:
            return f"Invalid task type: {task_type}. Must be one of {list(TASK_FILES.keys())}."
        
        # Load tasks from the specified JSON file
        with open(TASK_FILES[task_type], 'r') as f:
            tasks = json.load(f)
        
        # Find the task by ID
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return f"Task ID '{task_id}' not found in {task_type} tasks."
        
        # Initialize explanation
        explanation = f"# Task: {task_id}\n\n"
        explanation += f"**Description**: {task.get('description', 'No description provided.')}\n\n"
        
        # Format based on task type
        if task_type == "fill_in_the_blank":
            explanation += "## Task Type: Fill in the Blank\n\n"
            explanation += "### Question Template:\n```python\n" + task["question_template"] + "\n```\n"
            explanation += f"**Options**: {', '.join(task['options'])}\n\n"
        
        elif task_type == "multiple_choice":
            explanation += "## Task Type: Multiple Choice\n\n"
            explanation += "### Question:\n```python\n" + task["question"] + "\n```\n"
            explanation += f"**Options**: {', '.join(task['options'])}\n\n"
        
        elif task_type == "code_output":
            explanation += "## Task Type: Code Output\n\n"
            explanation += "### Code:\n```python\n" + task["code"] + "\n```\n"
        
        return explanation
    
    except FileNotFoundError:
        return f"Error: Task file for {task_type} not found."
    except Exception as e:
        return f"Error retrieving task: {str(e)}"

@tool
def python_videos(name: str = "Basic Concepts", subname: str = None) -> str:                                                                                                                                                                                                           
    """
    This will return a random python video from a specific chapter from pyvids.

    Args:
        name (str): This is the name of the chapter you will choose videos for. The options are :
                            1. Basic Concepts
                            2.Basic Data Types
                            3.If-else statements
                            4.Loops
                            If you can't find a chapter, you will default in "Basic Concepts"
        subname (str): These are a subcategory of the chapters. If the subcategory is not found
        a random video will be choosed.
    
    Returns:
        str: YouTube video URL ONLY.
    """
    pyvids = {
        "Basic Concepts": {
            "Hello World": [
                "https://www.youtube.com/watch?v=hp4pYFASTrc&ab_channel=PortfolioCourses"
            ],
            "Operators": [
                "https://www.youtube.com/watch?v=GEMZpw7ug-k&ab_channel=NesoAcademy"
            ],
            "Comments":[
                "https://www.youtube.com/watch?v=QZ6Ml_CA9PQ&ab_channel=NesoAcademy"
            ],
            "Lists":[
                "https://www.youtube.com/watch?v=9OeznAkyQz4&ab_channel=ProgrammingwithMosh"
            ]
        },
        "Basic Data Types": {
            "Interges And Floats": [
                "https://www.youtube.com/watch?v=77TsTM3XxmA&ab_channel=b001",
                "https://www.youtube.com/watch?v=khKv-8q7YmY&t=195s&ab_channel=CoreySchafer"
            ],
            "General Variables":
            [
               "https://www.youtube.com/watch?v=LKFrQXaoSMQ&ab_channel=BroCode",
               "https://www.youtube.com/watch?v=RSQjxL5WRNM&ab_channel=Telusko"
            ],
            "Strings": [
                "https://www.youtube.com/watch?v=Ctqi5Y4X-jA&ab_channel=ProgrammingwithMosh"
            ],
            "String Concatenation": [
                "https://www.youtube.com/watch?v=28FUVmWU_fA&ab_channel=PortfolioCourses"
            ]
        },
        "If-else statements": {
            "If": [
                "https://www.youtube.com/watch?v=89tgwKTo-rE&ab_channel=NesoAcademy"
            ],
            "If/Else/Elif": [
                "https://www.youtube.com/watch?v=X6TcB0DNLE8&ab_channel=NesoAcademy",
                "https://www.youtube.com/watch?v=FvMPfrgGeKs&ab_channel=BroCode"
            ]
        },
        "Loops": {
            "For Loops": [
                "https://www.youtube.com/watch?v=KWgYha0clzw&t=151s&ab_channel=BroCode",
                "https://www.youtube.com/watch?v=zmIdC0_0BgY&ab_channel=AlexTheAnalyst"
            ],
            "While Loops": [
                "https://www.youtube.com/watch?v=rRTjPnVooxE&ab_channel=BroCode",
                "https://www.youtube.com/watch?v=S_1QiK_RF2o&ab_channel=NesoAcademy"

            ],
            "Break / Continue" : [
                "https://www.youtube.com/watch?v=Rjjgy2QWS98&ab_channel=NesoAcademy",
                "https://www.youtube.com/watch?v=yCZBnjF4_tU&t=2s&ab_channel=Telusko"
            ]
    }
    }

    chapter = pyvids.get(name, pyvids["Basic Concepts"])

    if subname and subname in chapter:
        check = chapter[subname]  
    else:
        check = sum(chapter.values(), [])

    ranvid = random.choice(check)
   
    return ranvid

def skip_message(idx: int, messages: list[BaseMessage]) -> bool:
    msg = messages[idx]

    # keep video tool calls visible
    if isinstance(msg, ToolMessage):
        if getattr(msg, "name", "") == "python_videos":
            return False
        return True

    # hide system prompts.
    if isinstance(msg, SystemMessage):
        return True

    # hide empty/blank messages
    if isinstance(msg, AIMessage) and not str(msg.content).strip():
        return True

    # don't hide/skip
    return False