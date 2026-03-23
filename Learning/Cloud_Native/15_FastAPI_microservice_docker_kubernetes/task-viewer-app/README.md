# Task Viewer App

This is a FastAPI application that provides functionality to view tasks and search for tasks based on specific titles.

## Features

- Get all tasks
- Get tasks based on specific task title
- Get a specific task by ID

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
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## API Endpoints

- `GET /` - Health check endpoint
- `GET /tasks/` - Get all tasks
- `GET /tasks/search/{title}` - Get tasks based on specific task title (case-insensitive partial match)
- `GET /tasks/{task_id}` - Get a specific task by ID

## Data Storage

Tasks are stored in memory and will be lost when the application restarts. For demonstration purposes, the app is initialized with sample data.