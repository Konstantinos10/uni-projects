import streamlit as st
import json
import logging
from langchain_core.tools import tool
from firebase_admin import firestore
from code_editor import run_code as code_run #epic way to prevent recursion

# Setup logging
logger = logging.getLogger(__name__)

# Task files (same as in task.py)
TASK_FILES = {
    "fill_in_the_blank": "fill_in_the_blank.json",
    "multiple_choice": "multiple_choice.json",
    "code_output": "code_output.json"
}

# Initialize Firestore client
db = firestore.client()

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
def get_username(tool_input: dict = None) -> str:
    """Retrieve the username from the current session."""
    if not st.session_state.username:
        return {"username": "username wasn't found"}

    return {"username": st.session_state.username}

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
        
        # Retrieve the chapter.question array field
        user_data = user_doc.to_dict()
        completed_chapters = user_data.get("chapter.question", [])
        logger.info(f"Completed chapters for {username}: {completed_chapters}")
        
        return {"username": username, "completed_chapters": completed_chapters}
    except Exception as e:
        logger.error(f"Error fetching user data for {username}: {str(e)}")
        return {"username": username, "completed_chapters": [], "error": f"Error fetching user data: {str(e)}"}

@tool
def explain_task(task_id: str, task_type: str) -> str:
    """Retrieve and explain a specific task based on its ID and type, including the correct answer.
    
    Args:
        task_id (str): The ID of the task (e.g., 'fib1', 'mc1', 'co1')
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