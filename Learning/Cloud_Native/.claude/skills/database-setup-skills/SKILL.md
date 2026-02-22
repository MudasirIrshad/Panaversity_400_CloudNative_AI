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
Setting up the database connection and basic models:

```python
from sqlmodel import SQLModel, Field, create_engine, Session
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Get the database URL from environment variables
db_url = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(f"{db_url}", echo=True)

# Basic Models
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None)
    user_id: int

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str

def create_tables():
    print("\nCreating database tables...\n")
    SQLModel.metadata.create_all(engine)
    print("\nTables created successfully.\n")

if __name__ == "__main__":
    create_tables()
```

### Level 2: Session Management
Implementing proper session management with dependency injection:

```python
from fastapi import Depends
from sqlmodel import Session

# Session dependency
def get_session():
    with Session(engine) as session:
        yield session
```

### Level 3: Complete CRUD Implementation
Full CRUD operations with proper error handling:

```python
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from db_schema import Task, User

app = FastAPI(title="Dependency Injection with SQLModel and Environment Config")

# POST - Create task
@app.post("/tasks")
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"task": task}

# GET - Read all tasks
@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return {"tasks": tasks}

# GET - Read single task by ID
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}
    return {"task": task}

# POST - Create user
@app.post("/users")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"user": user}
```

## File Organization Pattern
Separate concerns by organizing code into multiple files:

### db_schema.py - Database Models and Engine
```python
from sqlmodel import SQLModel, Field, create_engine, Session
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Get the database URL from environment variables
db_url = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(f"{db_url}", echo=True)

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None)
    user_id: int

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str

def create_tables():
    print("\nCreating database tables...\n")
    SQLModel.metadata.create_all(engine)
    print("\nTables created successfully.\n")

if __name__ == "__main__":
    create_tables()
```

### main.py - API Endpoints
```python
from fastapi import FastAPI, Depends
import uvicorn
from sqlmodel import Session, select
from fastapi import Depends
from db_schema import User, engine
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

@app.post("/users")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"user": user}
```

## Environment Configuration

### Setting up .env file
Create a `.env` file in your project root:

```
DATABASE_URL=sqlite:///./task_api.db
# For PostgreSQL: postgresql://username:password@localhost/dbname
# For Neon: postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

### Loading Environment Variables
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file
db_url = os.getenv("DATABASE_URL")  # Access the database URL
```

### Installing Required Dependencies
```bash
pip install sqlmodel python-dotenv
# For PostgreSQL: pip install psycopg2-binary
# For async support: pip install asyncpg
```

## Model Definition Best Practices

### Basic Model Structure
```python
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None)
    user_id: int

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
```

### Field Validation
```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    user_id: int

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(regex=r'^[^@]+@[^@]+\.[^@]+$')  # Basic email validation
    password: str = Field(min_length=6)  # At least 6 characters
```

## Connection Management Patterns

### Engine Configuration
```python
from sqlmodel import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(f"{db_url}", echo=True)  # echo=True for debugging
```

### Session Dependency
```python
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session
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

For simple setup during development, `SQLModel.metadata.create_all(engine)` is sufficient:

```python
def create_tables():
    SQLModel.metadata.create_all(engine)
```

For production applications, consider using Alembic for database migrations.

## Error Handling

### Common Database Errors
- Connection timeouts
- Unique constraint violations
- Foreign key constraint violations

### Session Management with Auto-commit/Rollback
```python
# The Session context manager automatically handles commits and rollbacks
def get_session():
    with Session(engine) as session:
        yield session  # FastAPI will handle commits/rollbacks with Depends
```

## Security Considerations

1. Never expose database credentials in code
2. Use environment variables for database URLs
3. Store sensitive data in `.env` files and add `.env` to `.gitignore`
4. Use parameterized queries (SQLModel handles this automatically)