import streamlit as st
import asyncio
from dotenv import load_dotenv
import os

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
)
from openai import AsyncOpenAI

# =========================
# LOAD ENV
# =========================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# =========================
# OPENAI CLIENT (GEMINI)
# =========================
client = AsyncOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

llm = OpenAIChatCompletionsModel(
    model="deepseek-v3.1:671b-cloud",
    openai_client=client
)

# =========================
# TOOLS (UNCHANGED)
# =========================
@function_tool
def get_task_list() -> str:
    import requests
    response = requests.get("http://127.0.0.1:8000/get_tasks")
    return response.json() if response.status_code == 200 else "Error fetching tasks"


@function_tool
def create_task(title: str, description: str) -> str:
    import requests
    response = requests.post(
        "http://127.0.0.1:8000/create_task",
        json={"title": title, "description": description},
    )
    return "Task created successfully" if response.status_code == 200 else "Error creating task"


@function_tool
def delete_task(task_id: int) -> str:
    import requests
    response = requests.delete(f"http://127.0.0.1:8000/tasks/{task_id}")
    return "Task deleted successfully" if response.status_code == 200 else "Error deleting task"


@function_tool
def update_task(task_id: int, title: str | None = None, description: str | None = None) -> str:
    import requests
    body = {}
    if title:
        body["title"] = title
    if description:
        body["description"] = description

    response = requests.put(
        f"http://127.0.0.1:8000/tasks/{task_id}",
        json=body
    )
    return "Task updated successfully" if response.status_code == 200 else "Error updating task"


# =========================
# AGENT (UNCHANGED)
# =========================
agent = Agent(
    name="Task Assistant",
    instructions="""
You are an AI task management assistant.
You help users create, update, delete, and fetch tasks.
Use the provided tools whenever required.
""",
    model=llm,
    tools=[get_task_list, create_task, delete_task, update_task],
)

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="AI Task Manager", page_icon="🧠")
st.title("🧠 AI Task Manager")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """👋 **Welcome to AI Task Manager**

You can:
• Create tasks  
• Update tasks  
• Delete tasks  
• View task list  

Examples:
- Create a task to learn FastAPI
- Show my tasks
- Delete task 2
"""
        }
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your task request...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant thinking
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            result = Runner.run_sync(
                starting_agent=agent,
                input=user_input,
            )
            response_text = f"✅ **Result:**\n\n{result.final_output}"
            st.markdown(response_text)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )
