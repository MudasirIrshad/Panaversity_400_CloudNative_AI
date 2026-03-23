from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Task Manager API", description="API for managing tasks with add, update, and delete operations")

# In-memory storage for tasks
tasks = {}
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

@app.get("/")
def read_root():
    return {"message": "Task Manager API"}

@app.post("/tasks/", status_code=201)
def create_task(task: Task):
    global task_id_counter
    task_id = task_id_counter
    tasks[task_id] = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }
    task_id_counter += 1
    return tasks[task_id]

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only provided fields
    if task_update.title is not None:
        tasks[task_id]["title"] = task_update.title
    if task_update.description is not None:
        tasks[task_id]["description"] = task_update.description
    if task_update.completed is not None:
        tasks[task_id]["completed"] = task_update.completed

    return tasks[task_id]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = tasks.pop(task_id)
    return {"message": "Task deleted successfully", "deleted_task": deleted_task}

@app.get("/tasks/")
def get_all_tasks():
    return tasks

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)