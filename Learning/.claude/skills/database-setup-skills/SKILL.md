---
name: database-setup-skills
description: This skill provides comprehensive guidance for setting up database connections with FastAPI and SQLModel, including Neon PostgreSQL setup, model definitions, and CRUD operations. This skill should be used when users need to implement database functionality with SQLModel in FastAPI applications.
---

# Database Setup Skills

This skill provides comprehensive guidance for setting up database connections with FastAPI and SQLModel, including Neon PostgreSQL setup, model definitions, and CRUD operations.

## Core Concepts

### SQLModel Integration
SQLModel combines the power of SQLAlchemy and Pydantic, allowing you to define data models that work for both database operations and API validation.

### Database Connection Management
Proper database connection management includes engine creation, session handling, and lifecycle management to ensure efficient resource usage.

### Neon PostgreSQL Setup
Neon is a serverless PostgreSQL platform that provides branchable, auto-scaling databases with built-in connection pooling.

## Progressive Implementation Levels

### Level 1: Basic Setup
Setting up the database connection and basic model:

```python
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine
from pydantic_settings import BaseSettings

# Environment Configuration
class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    app_name: str = "My API"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

# Basic Model
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: str
    completed: bool = False

# Database Engine
DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL, echo=settings.debug)
```

### Level 2: Session Management
Implementing proper session management with dependency injection:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Session

# Database setup function
def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)

# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Session dependency
def get_session() -> Session:
    with Session(engine) as session:
        yield session
```

### Level 3: Complete CRUD Implementation
Full CRUD operations with proper error handling:

```python
from fastapi import HTTPException
from sqlmodel import select

# GET - Read all tasks
@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

# POST - Create task
@app.post("/tasks")
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"message": "Task created successfully", "task": task}

# PUT - Update task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return {"message": "Task updated successfully", "task": db_task}

# DELETE - Delete task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully", "task": db_task}
```

## Neon PostgreSQL Setup

### Creating a Neon Account
1. Go to https://neon.tech and sign up for an account
2. Create a new project in the Neon dashboard
3. Get your connection string from the project dashboard

### Environment Configuration
Add your Neon connection string to your `.env` file:

```
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
APP_NAME=My FastAPI App
DEBUG=False
```

### Installing Required Dependencies
```bash
pip install sqlmodel psycopg2-binary python-dotenv pydantic-settings
```

## Model Definition Best Practices

### Field Validation
```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(max_length=1000)
    completed: bool = False
    priority: int = Field(default=1, ge=1, le=5)  # Priority from 1-5
```

### Separate Pydantic Models for API Operations
```python
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
```

## Connection Management Patterns

### Engine Configuration
```python
from sqlmodel import create_engine
import os

# For production with Neon
engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,         # Number of connection pool
    max_overflow=10      # Additional connections beyond pool_size
)
```

### Session Dependency with Error Handling
```python
from contextlib import contextmanager
from sqlmodel import Session

@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI structure, patterns, existing models to integrate with |
| **Conversation** | User's specific requirements, database preferences, deployment environment |
| **Skill References** | SQLModel patterns, Neon setup, best practices for connection management |
| **User Guidelines** | Project-specific conventions, security requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Migration Considerations

For production applications, consider using Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
```

For simple setup during development, `create_all()` is sufficient but requires migration tools for production changes.

## Error Handling

### Common Database Errors
- Connection timeouts
- Unique constraint violations
- Foreign key constraint violations
- Connection pool exhaustion

### Handling Database Errors in FastAPI
```python
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

@app.post("/tasks")
def create_task(task: TaskCreate):
    try:
        db_task = Task.model_validate(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task with this ID already exists"
        )
```

## Security Considerations

1. Never expose database credentials in code
2. Use environment variables for database URLs
3. Implement proper input validation using Pydantic models
4. Use parameterized queries (SQLModel handles this automatically)
5. Limit database connection pool sizes appropriately