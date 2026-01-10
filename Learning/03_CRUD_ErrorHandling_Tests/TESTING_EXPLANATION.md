# FastAPI Testing Guide

## What is Testing?
Testing is the process of checking if your code works correctly. Instead of manually testing by visiting URLs, we write code that automatically tests our application.

## Why Test Your Code?
- Ensures your code works as expected
- Catches bugs before users see them
- Makes it safe to change code (regression testing)
- Documents how your code should behave

## FastAPI Testing Components

### 1. TestClient
- A special tool that simulates a web browser
- Sends requests to your FastAPI app without starting a real server
- Returns responses that you can examine in your tests

### 2. Pytest
- A popular Python testing framework
- Uses simple functions to define tests
- Shows which tests pass or fail

## How Our Tests Work

### Basic Test Structure
```python
def test_something():
    # 1. Create a test client
    client = TestClient(app)

    # 2. Send a request to your app
    response = client.get("/")

    # 3. Check if the response is what you expected
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

### HTTP Request Methods in Tests
- `client.get("/path")` - Tests GET requests
- `client.post("/path", json=data)` - Tests POST requests
- `client.patch("/path", params=data)` - Tests PATCH requests
- `client.put("/path", json=data)` - Tests PUT requests
- `client.delete("/path")` - Tests DELETE requests

### What We Check in Tests
1. **Status Code**: `response.status_code == 200` (200 means "OK")
2. **Response Data**: `response.json() == expected_data`
3. **Error Handling**: Testing what happens when things go wrong

## Example Test Breakdown

```python
def test_create_todo():
    # Clear any existing items to start fresh
    todo_items.clear()

    # Define the data we want to send
    new_item = {
        "item_id": 1,
        "title": "Test Todo",
        "description": "This is a test todo item",
        "completed": False
    }

    # Send a POST request with the data
    response = client.post("/todo", json=new_item)

    # Check if the request was successful
    assert response.status_code == 200

    # Get the response data
    response_data = response.json()

    # Check if the response matches what we expected
    assert response_data["message"] == "Todo item created"
    assert response_data["item"]["title"] == "Test Todo"

    # Check if the item was actually added to our list
    assert len(todo_items) == 1
```

## Different Types of Tests

### 1. Happy Path Tests
- Test when everything works correctly
- Example: Creating a todo item successfully

### 2. Error Tests
- Test what happens when things go wrong
- Example: Trying to update a non-existent item

### 3. Edge Case Tests
- Test unusual situations
- Example: Empty lists, invalid data

## Running Tests

To run the tests, use this command:
```bash
uv run pytest test_main.py -v
```

- `pytest`: The testing framework
- `test_main.py`: The file containing tests
- `-v`: Verbose mode (shows details)

## Key Testing Concepts

### Assertions
- Statements that check if something is true
- If the assertion fails, the test fails
- Examples: `assert x == 5`, `assert response.status_code == 200`

### Test Isolation
- Each test should be independent
- Tests shouldn't affect each other
- We clear `todo_items.clear()` to ensure fresh state

### Test Naming
- Use descriptive names like `test_create_todo`
- Makes it clear what is being tested
- Helps when debugging failures

## Common Test Patterns

### Testing Different HTTP Methods
```python
def test_get_request():
    response = client.get("/todo")
    assert response.status_code == 200

def test_post_request():
    response = client.post("/todo", json=data)
    assert response.status_code == 200

def test_patch_request():
    response = client.patch("/todo/0/true")
    assert response.status_code == 200
```

### Testing Error Cases
```python
def test_error_case():
    response = client.get("/nonexistent")
    assert response.status_code == 404  # Not found
```

## Benefits of This Testing Approach

1. **Fast**: Tests run immediately without starting a server
2. **Reliable**: No network dependencies
3. **Comprehensive**: Tests all endpoints and error cases
4. **Automatic**: Can be run as part of deployment
5. **Documentation**: Shows how your API should work

## Writing Good Tests

1. **Test the happy path** - when everything works
2. **Test error cases** - when things go wrong
3. **Test edge cases** - unusual situations
4. **Keep tests simple** - easy to understand and maintain
5. **Test behavior, not implementation** - focus on what the API does, not how it does it