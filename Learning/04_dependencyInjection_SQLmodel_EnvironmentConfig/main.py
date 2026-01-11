from fastapi import FastAPI
import uvicorn
from sqlmodel import Session, select
from fastapi import Depends
from db_schema import engine

from db_schema import Task


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI(title="Dependency Injection with SQLModel and Environment Config")



@app.post("/tasks")
def create_task(task: Task, session: Session = Depends(get_session)):

    session.add(task)
    session.commit()
    session.refresh(task)

    return {"task": task}


@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()

    return {"tasks": tasks}


@app.get("/tasks/{task_id}")
def get_single_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}
    return {"task": task}

