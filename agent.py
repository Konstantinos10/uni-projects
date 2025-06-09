from typing import Annotated, Sequence, TypedDict
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from google.api_core.exceptions import ResourceExhausted
import firebase_admin
from firebase_admin import credentials, firestore
from questions import chapters
from agent_utils import get_username, get_user_data, explain_task, run_code, read_playground, write_playground, python_videos

# === Initialize Firebase ===
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")  # Update with your Firebase credentials path
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Failed to initialize Firebase: {str(e)}")
        st.stop()
db = firestore.client()

# === Load API Key ===
try:
    with open("private/agents/agentKey.txt", "r") as f:
        api_key = f.read().strip()
except FileNotFoundError:
    st.error("API key file not found. Please ensure 'private/agentKey.txt' exists.")
    st.stop()

# === Define Agent State ===
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]  # chat history
    number_of_steps: int
    username: str  # track username to avoid redundant calls

# === Setup Gemini Model with Tools ===
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    max_retries=2,
    google_api_key=api_key,
)
tools = [get_username, get_user_data, explain_task, run_code, read_playground, write_playground, python_videos]
model = llm.bind_tools(tools)

system_message = f"""You're a helpful Python tutor agent. Answer clearly and concisely.
        When the user asks to learn Python or start a lesson, call get_username to retrieve their username,
        then call get_user_data to fetch their completed chapters (e.g. 1.1, 1.2). Use the following chapter information to suggest
        appropriate topics based on completed chapters:

        {chapters}

        For each chapter (e.g. 1.1, 1.2, 1.3), the dictionary provides the title, description, and question topics
        (e.g. 1.1 is 'Hello World!', 1.2 is 'Variables'). If chapters are completed, suggest the next topics or chapters,
        referencing the chapter titles and question topics. If no chapters are completed or data is unavailable,
        recommend starting with Chapter 1: Basic Concepts (covering Hello World!, Variables, Comments, Arithmetic operators, Lists).
        Use the tools only when necessary and avoid redundant calls if the username is already known.

        When the user asks for help with a task (e.g. 'help me with task fib1'), call the explain_task tool with the appropriate
        task_id and task_type to retrieve and explain the task, including its details and the correct answer with reasoning.
        fib - fill in the blank
        mc - multiple choice
        co - code output
        You always have to explain why the answer you gave is the right one.
        
        If at any point you need to run code, use the run_code tool. It takes a string of python code as input and returns the
        standard output and error output in a dictionary. You should have no problem running any python code, the tool is designed
        to handle errors and automatically stops after 1 second
        
        The user also has access to a playground code editor where they can test their own python code. You can read the content of this
        editor and it's standard/error output with the read_playground tool. The tool usually returns a dictionary with just the editor content,
        but if the code was run and not modified, it will return the standard and error output as well. You can write to the editor with the write_playground tool
        but always read the content before writing to it. If you write to it make sure to rewrite the entire content of the editor, not just the new code.
        You should also suggest the user to use the playground and encourage them to test their code there.

        When you are going to reccomend a video to the user you will take this steps.
        1. Call the python_videos tool and get the URL from it
        2. Return ONLY the URL at the ToolMessage without any other descriptive text.
        """

# === Tool Node ===
def call_tool(state: AgentState):
    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, "tool_calls", [])
    if not tool_calls:
        return state

    results = []
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call.get("id", tool_name)

        # Find and invoke the tool
        for tool in tools:
            if tool.name == tool_name:
                try:
                    result = tool.invoke(tool_args)
                    results.append(ToolMessage(content=str(result), tool_call_id=tool_id, name=tool_name))
                    # Update username in state if get_username was called
                    if tool_name == "get_username" and isinstance(result, str) and "Error" not in result and "not found" not in result:
                        state["username"] = result
                    # Update username in state if get_user_data was called
                    elif tool_name == "get_user_data" and isinstance(result, dict) and "username" in result:
                        state["username"] = result["username"]
                except Exception as e:
                    results.append(ToolMessage(content=f"Error in {tool_name}: {str(e)}", tool_call_id=tool_id, name=tool_name))
                break

    return {
        "messages": add_messages(state["messages"], results),
        "number_of_steps": state["number_of_steps"] + 1,
        "username": state.get("username", "")
    }

# === LLM Node ===
def call_model(state: AgentState):
    try:
        response = model.invoke(state["messages"])
        new_messages = [response]
        return {
            "messages": add_messages(state["messages"], new_messages),
            "number_of_steps": state["number_of_steps"] + 1,
            "username": state["username"]
        }
    except ResourceExhausted as e:
        return {
            "messages": add_messages(state["messages"], [AIMessage(content=f"Quota exceeded: {str(e)}. Please try again later or check your Gemini API plan.")]),
            "number_of_steps": state["number_of_steps"] + 1,
            "username": state["username"]
        }

# === Build LangGraph ===
workflow = StateGraph(AgentState)
workflow.add_node("llm", call_model)
workflow.add_node("tool", call_tool)
workflow.set_entry_point("llm")
workflow.add_conditional_edges(
    "llm",
    lambda state: "tool" if hasattr(state["messages"][-1], "tool_calls") and state["messages"][-1].tool_calls else END
)
workflow.add_edge("tool", "llm")
graph = workflow.compile()

# === Streamlit UI ===
st.title("Python Tutor Agent")
st.markdown("Ask any Python-related question, or get help with specific tasks!")

# Initialize session state
if "message_history" not in st.session_state:
    st.session_state.message_history = [ 
        SystemMessage(content=system_message)
    ]
if "number_of_steps" not in st.session_state:
    st.session_state.number_of_steps = 0
if "username" not in st.session_state:
    st.session_state.username = st.session_state.get("username")

# Container for chat history
history_container = st.container()

# Check for st.session_state.explain_task to handle task explanation
if "explain_task" in st.session_state and st.session_state.explain_task and not any(isinstance(msg, HumanMessage) and f"help me with task {st.session_state.explain_task}" in msg.content.lower() for msg in st.session_state.message_history):
    task_id = st.session_state.explain_task
    # Add a human message to simulate user input
    st.session_state.message_history.append(HumanMessage(content=f"help me with task {task_id}"))
    # Process the message immediately through the LangGraph workflow
    inputs = {
        "messages": st.session_state.message_history,
        "number_of_steps": st.session_state.number_of_steps,
        "username": st.session_state.username
    }
    for state in graph.stream(inputs, stream_mode="values"):
        st.session_state.message_history = state["messages"]
        st.session_state.number_of_steps = state["number_of_steps"]
        st.session_state.username = state["username"]
    # Clear st.session_state.explain_task to prevent re-triggering
    st.session_state.explain_task = None

#elif any(isinstance(msg, HumanMessage) and f"help me with task {st.session_state.explain_task}" in msg.content.lower() for msg in st.session_state.message_history):
    #st.session_state.explain_task = None
    #st.toast("Answered already")

# Display chat history after processing explain_task
with history_container:
    for msg in st.session_state.message_history:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                    st.write(msg.content)
        elif isinstance(msg, ToolMessage):
            with st.chat_message("assistant"):
                if msg.name == "python_videos" and "youtube.com" in msg.content:
                    st.video(msg.content)
                else:
                    st.write(msg.content)
                
                

with st.form(key="question_form", clear_on_submit=True):
    user_question = st.text_area("Ask a Python question (or type 'exit' to reset):")
    submit_button = st.form_submit_button("Submit")

if submit_button and user_question:
    # For resetting the session
    if user_question.lower() in ["exit", "quit"]:
        st.session_state.message_history = [ 
            SystemMessage(content=system_message)
        ]
        st.session_state.number_of_steps = 0
        st.session_state.username = st.session_state.get("username")
        st.session_state.explain_task = None
        st.success("Session reset. Ask a new question!")
    else:
        st.session_state.message_history.append(HumanMessage(content=user_question))

        inputs = {
            "messages": st.session_state.message_history,
            "number_of_steps": st.session_state.number_of_steps,
            "username": st.session_state.username
        }

        for state in graph.stream(inputs, stream_mode="values"):
            st.session_state.message_history = state["messages"]
            st.session_state.number_of_steps = state["number_of_steps"]
            st.session_state.username = state["username"]

            with history_container:
                last_msg = state["messages"][-1]
                if isinstance(last_msg, HumanMessage):
                    role = "user"
                elif isinstance(last_msg, AIMessage):
                    role = "assistant"
                elif isinstance(last_msg, ToolMessage):
                    role = "assistant"
                with st.chat_message(role):
                     if isinstance(last_msg, ToolMessage) and last_msg.name == "python_videos" and "youtube.com" in last_msg.content:
                         st.video(last_msg.content)
                     else:
                         st.write(last_msg.content)
