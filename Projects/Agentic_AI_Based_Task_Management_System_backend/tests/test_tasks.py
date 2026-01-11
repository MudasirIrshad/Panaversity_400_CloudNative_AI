import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

def test_create_task(client: TestClient, session: Session):
    response = client.post("/create_task", json={
        "title": "Test task",
        "description": "Test description"
    })
    assert response.status_code == 200

    data = response.json()
    assert "Following task is created: " in data
    task_data = data["Following task is created: "]
    assert task_data["title"] == "Test task"
    assert task_data["description"] == "Test description"
    assert "id" in task_data


def test_get_tasks(client: TestClient, session: Session):
    # Create a task first
    client.post("/create_task", json={
        "title": "Test task",
        "description": "Test description"
    })

    response = client.get("/get_tasks")
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1
    # Find the task we just created
    created_task = next((task for task in data if task["title"] == "Test task"), None)
    assert created_task is not None


def test_get_single_task(client: TestClient, session: Session):
    # Create a task first
    create_response = client.post("/create_task", json={
        "title": "Single task",
        "description": "Single task description"
    })
    # The create response contains the task in a nested dict, so we need to extract the ID
    task_data = create_response.json()["Following task is created: "]
    task_id = task_data["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Single task"
    assert data["description"] == "Single task description"


def test_update_task(client: TestClient, session: Session):
    # Create a task first
    create_response = client.post("/create_task", json={
        "title": "Update task",
        "description": "Update task description"
    })
    task_data = create_response.json()["Following task is created: "]
    task_id = task_data["id"]

    response = client.put(f"/tasks/{task_id}", json={
        "id": task_id,
        "title": "Updated task",
        "description": "Updated description"
    })
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated task"
    assert data["description"] == "Updated description"


def test_delete_task(client: TestClient, session: Session):
    # Create a task first
    create_response = client.post("/create_task", json={
        "title": "Delete task",
        "description": "Delete task description"
    })
    task_data = create_response.json()["Following task is created: "]
    task_id = task_data["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # Verify the task is deleted by trying to get it again
    # We expect this to fail, but let's just make sure the delete worked
    response_after_delete = client.get(f"/tasks/{task_id}")
    assert response_after_delete.status_code == 404


def test_get_nonexistent_task(client: TestClient, session: Session):
    response = client.get("/tasks/999")
    assert response.status_code == 404