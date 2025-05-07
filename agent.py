import os
from typing import Annotated, Sequence, TypedDict
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from google.api_core.exceptions import ResourceExhausted

# === Load API Key ===
try:
    with open("private/agents/agentKey.txt", "r") as f:
        api_key = f.read().strip()
except FileNotFoundError:
    st.error("API key file not found. Please ensure 'private/agentKey.txt' exists.")
    st.stop()

# === Define Agent State ===
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]  # visible chat history
    filtered_messages: Annotated[Sequence[BaseMessage], add_messages]  # used for LLM
    number_of_steps: int

# === Setup Gemini Model ===
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    #model="gemini-2.5-pro-exp-03-25",
    temperature=0.7,
    max_retries=2,
    google_api_key=api_key,
)
model = llm

# === Classifier Node ===
def is_python_question(state: AgentState):
    history = "\n".join(
        f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
        for m in state["messages"]
    )

    classification_prompt = f"""
    You are a strict classifier. Based on the following conversation history, determine if the user is asking about Python programming.

    Respond only with "Yes" or "No".

    Conversation:
    {history}
    """
    try:
        result = model.invoke([HumanMessage(content=classification_prompt)])
        response = result.content.strip().lower()

        if response == "yes":
            # Append message to filtered history
            return {
                "messages": state["messages"],
                "filtered_messages": add_messages(state["filtered_messages"], [state["messages"][-1]]),
                "number_of_steps": state["number_of_steps"]
            }
        else:
            # Add warning, but don't add to filtered messages
            warning = AIMessage(content="I'm a Python tutor. Please ask a Python-related question.")
            return {
                "messages": add_messages(state["messages"], [warning]),
                "filtered_messages": state["filtered_messages"],
                "number_of_steps": state["number_of_steps"] + 1
            }
    except Exception as e:
        return {
            "messages": add_messages(state["messages"], [AIMessage(content=f"Classification error: {str(e)}")]),
            "filtered_messages": state["filtered_messages"],
            "number_of_steps": state["number_of_steps"] + 1
        }

# === LLM Node ===
def call_model(state: AgentState):
    try:
        response = model.invoke(state["filtered_messages"])
        new_messages = [response]
        return {
            "messages": add_messages(state["messages"], new_messages),  # show response to user
            "filtered_messages": add_messages(state["filtered_messages"], new_messages),  # keep response for context
            "number_of_steps": state["number_of_steps"] + 1
        }
    except ResourceExhausted as e:
        return {
            "messages": add_messages(state["messages"], [AIMessage(content=f"Quota exceeded: {str(e)}. Please try again later or check your Gemini API plan.")]),
            "filtered_messages": state["filtered_messages"],
            "number_of_steps": state["number_of_steps"] + 1
        }

# === Build LangGraph ===
workflow = StateGraph(AgentState)
workflow.add_node("classifier", is_python_question)
workflow.add_node("llm", call_model)
workflow.set_entry_point("classifier")

workflow.add_conditional_edges(
    "classifier",
    lambda state: "llm" if isinstance(state["messages"][-1], HumanMessage) and len(state["filtered_messages"]) > 0 and state["filtered_messages"][-1] == state["messages"][-1] else END
)
workflow.add_edge("llm", END)

graph = workflow.compile()

# === Streamlit UI ===
st.title("Python Tutor Agent")
st.markdown("Ask any Python-related question, and the agent will respond clearly and concisely!")

if "message_history" not in st.session_state:
    st.session_state.message_history = [
        SystemMessage(content="You're a helpful Python tutor agent. Answer clearly and concisely.")
    ]
if "filtered_history" not in st.session_state:
    st.session_state.filtered_history = [
        SystemMessage(content="You're a helpful Python tutor agent. Answer clearly and concisely.")
    ]
if "number_of_steps" not in st.session_state:
    st.session_state.number_of_steps = 0

history_container = st.container()

with history_container:
    for msg in st.session_state.message_history:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)

with st.form(key="question_form", clear_on_submit=True):
    user_question = st.text_input("Ask a Python question (or type 'exit' to reset):")
    submit_button = st.form_submit_button("Submit")

if submit_button and user_question:

    # For *resetting* the session - reload in an amateur way
    if user_question.lower() in ["exit", "quit"]:
        st.session_state.message_history = [
            SystemMessage(content="You're a helpful Python tutor agent. Answer clearly and concisely.")
        ]
        st.session_state.filtered_history = [
            SystemMessage(content="You're a helpful Python tutor agent. Answer clearly and concisely.")
        ]
        st.session_state.number_of_steps = 0
        st.success("Session reset. Ask a new question!")

    else:
        st.session_state.message_history.append(HumanMessage(content=user_question))

        inputs = {
            "messages": st.session_state.message_history,
            "filtered_messages": st.session_state.filtered_history,
            "number_of_steps": st.session_state.number_of_steps
        }

        for state in graph.stream(inputs, stream_mode="values"):
            st.session_state.message_history = state["messages"]
            st.session_state.filtered_history = state["filtered_messages"]
            st.session_state.number_of_steps = state["number_of_steps"]

            with history_container:
                last_msg = state["messages"][-1]
                role = "assistant" if isinstance(last_msg, AIMessage) else "user"
                with st.chat_message(role):
                    st.write(last_msg.content)
