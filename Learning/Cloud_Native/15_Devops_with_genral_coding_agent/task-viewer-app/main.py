# task-viewer/main.py
from fastapi import FastAPI, HTTPException
import httpx
import os
from typing import Dict

app = FastAPI(title="Task Viewer API", description="Fetch tasks from Task Manager Service")

# Task Manager API base URL (use environment variable or default localhost)
TASK_MANAGER_API_URL = os.getenv("TASK_MANAGER_URL", "http://localhost:8000")

@app.get("/")
def read_root():
    return {"message": "Task Viewer API"}

@app.get("/tasks/", response_model=Dict)
def get_all_tasks():
    """Fetch all tasks from Task Manager Service"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{TASK_MANAGER_API_URL}/tasks/")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Error fetching tasks")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Task Manager: {e}")

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    """Fetch a task by ID from Task Manager Service"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{TASK_MANAGER_API_URL}/tasks/{task_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            else:
                raise HTTPException(status_code=response.status_code, detail="Error fetching task")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Task Manager: {e}")

@app.get("/tasks/search/{title}", response_model=Dict)
def get_tasks_by_title(title: str):
    """Fetch tasks by title (case-insensitive partial match) from Task Manager Service"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{TASK_MANAGER_API_URL}/tasks/")
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error fetching tasks")

            all_tasks = response.json()
            matching_tasks = {
                task_id: task
                for task_id, task in all_tasks.items()
                if title.lower() in task["title"].lower()
            }

            if not matching_tasks:
                raise HTTPException(status_code=404, detail="No tasks found with the specified title")

            return matching_tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Task Manager: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)