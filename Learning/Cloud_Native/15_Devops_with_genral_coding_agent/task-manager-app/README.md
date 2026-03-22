# Task Manager App

This is a FastAPI application that provides functionality to add, update, and delete tasks.

## Features

- Add new tasks
- Update existing tasks
- Delete tasks
- View all tasks

## Setup

1. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

2. Run the application:
```bash
uv run python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

- `GET /` - Health check endpoint
- `POST /tasks/` - Create a new task
- `PUT /tasks/{task_id}` - Update an existing task
- `DELETE /tasks/{task_id}` - Delete a task
- `GET /tasks/` - Get all tasks

## Data Storage

Tasks are stored in memory and will be lost when the application restarts.