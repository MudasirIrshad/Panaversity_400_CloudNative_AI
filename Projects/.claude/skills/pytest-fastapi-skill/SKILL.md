---
name: pytest-fastapi-skill
description: This skill provides comprehensive guidance for testing FastAPI applications with pytest, including fixtures, test clients, and database testing patterns. This skill should be used when users need to implement, run, or improve tests for FastAPI applications.
---

# Pytest FastAPI Testing Skill

This skill provides comprehensive guidance for testing FastAPI applications with pytest, including fixtures, test clients, and database testing patterns.

## Core Concepts

### Pytest Fixtures for FastAPI
Pytest fixtures provide a way to set up and tear down resources for tests, making test code cleaner and more maintainable.

### TestClient
FastAPI provides TestClient for testing API endpoints without starting a server, allowing for fast and isolated tests.

### Database Testing
Testing with real or mock databases to ensure proper functionality while isolating tests.

## Progressive Implementation Levels

### Level 1: Basic Test Setup
Creating basic pytest tests for FastAPI endpoints:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

### Level 2: Pytest Fixtures
Using pytest fixtures to set up test dependencies:

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from main import app
from db_schema import SQLModel, create_tables

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### Level 3: Complete Test Suite
Full test suite with various test scenarios:

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app, get_db
from db_schema import Task

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_task(client: TestClient, session: Session):
    response = client.post("/tasks", json={"title": "Test task", "description": "Test description"})
    assert response.status_code == 200

    data = response.json()["task"]
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"

    # Verify the task was saved to the database
    tasks = session.query(Task).all()
    assert len(tasks) == 1
    assert tasks[0].title == "Test task"
```

## File Organization Pattern

### tests/conftest.py - Shared Fixtures
```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from db_schema import SQLModel


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### tests/test_main.py - Main Endpoint Tests
```python
import pytest
from fastapi.testclient import TestClient

def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

### tests/test_tasks.py - Task Endpoint Tests
```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

def test_create_task(client: TestClient, session: Session):
    response = client.post("/tasks", json={
        "title": "Test task",
        "description": "Test description"
    })
    assert response.status_code == 200

    data = response.json()["task"]
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"

def test_get_tasks(client: TestClient, session: Session):
    # Create a task first
    client.post("/tasks", json={
        "title": "Test task",
        "description": "Test description"
    })

    response = client.get("/tasks")
    assert response.status_code == 200

    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Test task"
```

## Installation and Setup

### Installing Required Dependencies
```bash
pip install pytest pytest-asyncio httpx
# For database testing: pip install sqlalchemy pytest-postgresql
```

### Pytest Configuration (pytest.ini)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

## Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run specific test
pytest tests/test_main.py::test_read_main

# Run tests and show coverage
pytest --cov=.
```

## Advanced Testing Patterns

### Testing with Different Database States
```python
def test_get_tasks_empty(client: TestClient, session: Session):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()["tasks"]) == 0

def test_get_tasks_with_data(client: TestClient, session: Session):
    # Add sample data
    task = Task(title="Sample task", description="Sample description")
    session.add(task)
    session.commit()

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()["tasks"]) == 1
```

### Testing Error Cases
```python
def test_create_task_missing_title(client: TestClient):
    response = client.post("/tasks", json={"description": "Test description"})
    assert response.status_code == 422  # Validation error

def test_nonexistent_endpoint(client: TestClient):
    response = client.get("/nonexistent")
    assert response.status_code == 404
```

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI structure, patterns, existing models to integrate with |
| **Conversation** | User's specific requirements, testing preferences, current test setup |
| **Skill References** | Pytest patterns, FastAPI testing best practices, database testing approaches |
| **User Guidelines** | Project-specific conventions, security requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Common Test Scenarios

### Authentication Testing
```python
def test_protected_endpoint_without_auth(client: TestClient):
    response = client.get("/protected-endpoint")
    assert response.status_code == 401

def test_protected_endpoint_with_auth(client: TestClient):
    headers = {"Authorization": "Bearer valid-token"}
    response = client.get("/protected-endpoint", headers=headers)
    assert response.status_code == 200
```

### Request/Response Validation
```python
def test_task_response_format(client: TestClient):
    response = client.post("/tasks", json={
        "title": "Test task",
        "description": "Test description"
    })
    assert response.status_code == 200

    data = response.json()
    assert "task" in data
    assert "id" in data["task"]
    assert "title" in data["task"]
    assert "description" in data["task"]
```

## Error Handling in Tests

### Handling Exceptions
```python
def test_database_error(client: TestClient, session: Session):
    # Force a database error scenario
    with pytest.raises(Exception):
        # Code that should raise an exception
        pass
```

### Timeout Handling
```python
import asyncio

@pytest.mark.asyncio
async def test_async_endpoint_timeout():
    with pytest.raises(asyncio.TimeoutError):
        # Test code that should timeout
        pass
```