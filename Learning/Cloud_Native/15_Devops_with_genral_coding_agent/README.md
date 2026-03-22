# FastAPI Task Applications

This repository contains two separate FastAPI applications that work with in-memory task data.

## Applications

### 1. Task Manager App (`task-manager-app/`)

An application that provides functionality to:
- Add new tasks
- Update existing tasks
- Delete tasks

### 2. Task Viewer App (`task-viewer-app/`)

An application that provides functionality to:
- Get all tasks
- Get tasks based on specific task titles
- Get a specific task by ID

## Setup and Installation

Both applications use `uv` as the package manager.

### Prerequisites

Install `uv` if you haven't already:
```bash
pip install uv
```

### Task Manager App

1. Navigate to the task-manager-app directory:
```bash
cd task-manager-app
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

3. Run the application:
```bash
uv run python main.py
```

The app will be available at http://localhost:8000

### Task Viewer App

1. Navigate to the task-viewer-app directory:
```bash
cd task-viewer-app
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

3. Run the application:
```bash
uv run python main.py
```

The app will be available at http://localhost:8001

## API Documentation

Each application provides interactive API documentation via Swagger UI:
- Task Manager App: http://localhost:8000/docs
- Task Viewer App: http://localhost:8001/docs

## Data Storage

Both applications use in-memory storage, which means data will be lost when the applications are restarted.