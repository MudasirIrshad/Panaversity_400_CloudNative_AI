from fastapi import Response, Request
from argon2 import hash_password
from fastapi import FastAPI, HTTPException
import uvicorn
from sqlmodel import Session, select
from fastapi import Depends
from db_schema import User, UserCreate, engine
from password_hashing import hash_password, verify_password
from db_schema import Task
from auth_token import create_access_token, decode_token


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

@app.post("/user/signup")
def signup_user(user_data: UserCreate, session: Session = Depends(get_session)):

    existing = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail={"error": "User already exists"})

    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User created successfully", "user": [user.name, user.email]}

@app.post("/user/login")
def login_user(
    user_data: UserCreate, 
    response: Response,
    session: Session = Depends(get_session)
    ):
    
    user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail={"error": "Invalid credentials"})
    
    token = create_access_token({"user_id": str(user.id), "user_email": str(user.email)})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,   # JS cannot read it
        secure=True,     # HTTPS only (set False for local dev)
        samesite="lax"
    )

    return {
        "message": "Login successful",
        "user": [user.name, user.email]
    }

@app.get("/users/{user_email}")
def get_user(
    request: Request,
    session: Session = Depends(get_session)):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail={"error": "Not authenticated"})
    token_data = decode_token(access_token)
    if not token_data:
        raise HTTPException(status_code=401, detail={"error": "Invalid token"})
    
    user = session.exec(
        select(User).where(User.email == token_data.get("user_email"))
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail={"error": "User not found"})
    
    return {"user": [user.name, user.email]}