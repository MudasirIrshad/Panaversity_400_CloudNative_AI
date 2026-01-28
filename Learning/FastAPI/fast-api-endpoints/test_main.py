"""
Test file for FastAPI endpoints
This file contains pytest tests for the FastAPI application endpoints
"""

# Import necessary modules for testing
import pytest
from fastapi.testclient import TestClient
from main import app

# Create a test client for our FastAPI application
client = TestClient(app)

def test_todo_endpoint():
    """
    Test the /todo endpoint
    This test checks if the endpoint returns the expected list of todos
    """
    # Make a GET request to the /todo endpoint
    response = client.get("/todo")

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response contains the expected data
    expected_data = [
        {
            "id": 1,
            "task": "Implement FastAPI application"
        },
        {
            "id": 2,
            "task": "Create endpoints for CRUD operations"
        }
    ]

    # Compare the response JSON with expected data
    assert response.json() == expected_data

def test_todo2_endpoint():
    """
    Test the /todo/2 endpoint
    This test checks if the endpoint returns a single todo with ID 2
    Note: This endpoint actually calls the /todo/{todo_id} function with todo_id=2
    """
    # Make a GET request to the /todo/2 endpoint
    response = client.get("/todo/2")

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response contains the expected data for todo ID 2
    expected_data = {
        "id": 2,
        "task": "Task with ID 2"
    }

    # Compare the response JSON with expected data
    assert response.json() == expected_data

def test_todo_id_endpoint():
    """
    Test the /todo/{todo_id} endpoint with a valid ID
    This test checks if the endpoint returns the expected todo item
    """
    # Make a GET request to the /todo/1 endpoint
    response = client.get("/todo/1")

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response contains the expected data for a single todo
    expected_data = {
        "id": 1,
        "task": "Task with ID 1"
    }

    # Compare the response JSON with expected data
    assert response.json() == expected_data

def test_todo_id_endpoint_with_detail():
    """
    Test the /todo/{todo_id} endpoint with add_detail parameter
    This test checks if the endpoint returns detailed information when requested
    """
    # Make a GET request to the /todo/1 endpoint with add_detail=True
    response = client.get("/todo/1?add_detail=true")

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response contains detailed information
    expected_data = {
        "id": 1,
        "task": "Implement FastAPI application",
        "detail": "This task involves setting up the FastAPI framework and creating necessary endpoints."
    }

    # Compare the response JSON with expected data
    assert response.json() == expected_data

def test_todo_id_endpoint_invalid_id():
    """
    Test the /todo/{todo_id} endpoint with an invalid ID (less than 1)
    This test checks if the endpoint returns an error for invalid IDs
    """
    # Make a GET request to the /todo/0 endpoint (invalid ID)
    response = client.get("/todo/0")

    # Check that the response status code is 200 (OK) - note: this should probably return 404 or 400
    assert response.status_code == 200

    # Check that the response contains an error message
    expected_data = {
        "error": "Invalid task ID"
    }

    # Compare the response JSON with expected data
    assert response.json() == expected_data

def test_todo_id_endpoint_negative_id():
    """
    Test the /todo/{todo_id} endpoint with a negative ID
    This test checks if the endpoint handles negative IDs correctly
    """
    # Make a GET request to the /todo/-1 endpoint (negative ID)
    response = client.get("/todo/-1")

    # Check that the response status code is 200 (OK) - note: this should probably return 404 or 400
    assert response.status_code == 200

    # Check that the response contains an error message
    expected_data = {
        "error": "Invalid task ID"
    }

    # Compare the response JSON with expected data
    assert response.json() == expected_data

if __name__ == "__main__":
    # This allows running the tests directly with Python
    pytest.main()