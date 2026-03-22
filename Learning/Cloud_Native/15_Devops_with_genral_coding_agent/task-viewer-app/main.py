from fastapi import FastAPI, HTTPException
from typing import Dict, List
import uvicorn
import httpx
from typing import Optional

app = FastAPI(title="Task Viewer API", description="API for viewing tasks with search functionality")

# Task Manager API base URL
TASK_MANAGER_API_URL = "http://localhost:8000"

# In-memory storage for tasks (this would typically be shared with the task-manager-app)
# For demonstration purposes, we'll initialize with some sample data
# NOTE: In the updated version, we'll fetch from the task-manager API instead
sample_tasks = {
    1: {
        "id": 1,
        "title": "Sample Task 1",
        "description": "This is a sample task",
        "completed": False
    },
    2: {
        "id": 2,
        "title": "Sample Task 2",
        "description": "This is another sample task",
        "completed": True
    },
    3: {
        "id": 3,
        "title": "Important Task",
        "description": "This is an important task",
        "completed": False
    }
}

@app.get("/")
def read_root():
    return {"message": "Task Viewer API"}

@app.get("/tasks/", response_model=Dict)
def get_all_tasks():
    """Get all tasks from task-manager service"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{TASK_MANAGER_API_URL}/tasks/")
            if response.status_code == 200:
                return response.json()
            else:
                # Fallback to sample data if task-manager is unavailable
                return sample_tasks
    except Exception as e:
        # Fallback to sample data if task-manager is unavailable
        print(f"Error connecting to task-manager: {e}")
        return sample_tasks

@app.get("/tasks/search/{title}", response_model=Dict)
def get_tasks_by_title(title: str):
    """Get tasks based on specific task title (case-insensitive partial match)"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{TASK_MANAGER_API_URL}/tasks/")
            if response.status_code == 200:
                all_tasks = response.json()
                matching_tasks = {}
                for task_id, task in all_tasks.items():
                    if title.lower() in task["title"].lower():
                        matching_tasks[task_id] = task

                if not matching_tasks:
                    raise HTTPException(status_code=404, detail="No tasks found with the specified title")

                return matching_tasks
            else:
                # Fallback to sample data if task-manager is unavailable
                matching_tasks = {}
                for task_id, task in sample_tasks.items():
                    if title.lower() in task["title"].lower():
                        matching_tasks[task_id] = task

                if not matching_tasks:
                    raise HTTPException(status_code=404, detail="No tasks found with the specified title")

                return matching_tasks
    except Exception as e:
        # Fallback to sample data if task-manager is unavailable
        print(f"Error connecting to task-manager: {e}")
        matching_tasks = {}
        for task_id, task in sample_tasks.items():
            if title.lower() in task["title"].lower():
                matching_tasks[task_id] = task

        if not matching_tasks:
            raise HTTPException(status_code=404, detail="No tasks found with the specified title")

        return matching_tasks

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    """Get a specific task by ID"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{TASK_MANAGER_API_URL}/tasks/{task_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                # Check sample data if not found in task-manager
                if task_id in sample_tasks:
                    return sample_tasks[task_id]
                raise HTTPException(status_code=404, detail="Task not found")
            else:
                # Check sample data for other errors
                if task_id in sample_tasks:
                    return sample_tasks[task_id]
                raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        # Fallback to sample data if task-manager is unavailable
        print(f"Error connecting to task-manager: {e}")
        if task_id in sample_tasks:
            return sample_tasks[task_id]
        raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)