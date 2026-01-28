# 03_CRUD_ErrorHandling_Tests

A FastAPI-based todo application demonstrating CRUD operations, error handling, and testing practices.

## Overview

This project showcases a complete FastAPI todo application with Create, Read, Update, and Delete (CRUD) functionality. It includes comprehensive error handling and thorough testing with pytest.

## Features

- **Create**: Add new todo items
- **Read**: Retrieve all todo items or specific ones
- **Update**: Modify todo items (partial or full updates)
- **Delete**: Remove todo items
- **Error Handling**: Proper HTTP status codes and error messages
- **Testing**: Comprehensive test coverage with pytest

## Endpoints

### GET /
- **Description**: Root endpoint
- **Returns**: `{"Hello": "World"}`

### GET /todo
- **Description**: Retrieve all todo items
- **Returns**: Array of todo items

### POST /todo
- **Description**: Create a new todo item
- **Request Body**:
```json
{
  "item_id": 1,
  "title": "string",
  "description": "string",
  "completed": false
}
```
- **Returns**: Success message and created item

### PATCH /todo/{item_id}/{completed}
- **Description**: Update the completed status of a todo item
- **Parameters**:
  - `item_id`: ID of the item to update
  - `completed`: New completed status (true/false)
- **Returns**: Success message and updated item

### PUT /todo/{item_id}
- **Description**: Replace an entire todo item
- **Parameters**: `item_id`: ID of the item to replace
- **Request Body**: Same as POST /todo
- **Returns**: Success message and updated item

### DELETE /todo/{item_id}
- **Description**: Delete a todo item
- **Parameters**: `item_id`: ID of the item to delete
- **Returns**: Success message and deleted item

## Project Structure

```
03_CRUD_ErrorHandling_Tests/
├── main.py           # Main FastAPI application
├── test_main.py      # Comprehensive tests
├── TESTING_EXPLANATION.md  # Testing guide
├── README.md         # This file
├── pyproject.toml    # Project dependencies
└── .venv/            # Virtual environment
```

## Setup and Installation

1. **Clone or create the project**
```bash
# If you're using uv (as in the original setup):
uv init 03_CRUD_ErrorHandling_Tests
```

2. **Install dependencies**
```bash
cd 03_CRUD_ErrorHandling_Tests
uv add fastapi uvicorn[standard] pytest pydantic python-multipart httpx
```

3. **Run the application**
```bash
# Direct execution
python main.py

# Or with uvicorn
uvicorn main:app --reload
```

## Running Tests

To run the tests:
```bash
uv run pytest test_main.py -v
```

This will execute all the test cases covering:
- GET, POST, PATCH, PUT, DELETE endpoints
- Error handling scenarios
- Edge cases

## Models

### Todo_Item
- `item_id`: int
- `title`: str
- `description`: str
- `completed`: bool (default: false)

## Error Handling

The application implements proper error handling:
- 404 responses for non-existent items
- Appropriate HTTP status codes
- Descriptive error messages

## Testing Strategy

The test suite includes:
- **Unit tests**: Individual endpoint functionality
- **Integration tests**: Complete request/response cycles
- **Error tests**: Validation of error handling
- **Edge case tests**: Boundary conditions and unexpected inputs

Tests are organized by functionality:
- `test_read_root`: Root endpoint
- `test_get_todo`: Retrieving todo items
- `test_create_todo`: Creating new todo items
- `test_patch_todo`: Partial updates
- `test_put_todo`: Full replacement
- `test_delete_todo`: Deletion functionality
- `test_error_cases`: Error scenarios

## Development

The application is designed for development with:
- Auto-reload capability (`--reload` flag)
- Comprehensive logging
- Structured error responses

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the application
- **Pytest**: Testing framework
- **HTTPX**: HTTP client for testing
- **uv**: Python package installer and resolver

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Submit a pull request