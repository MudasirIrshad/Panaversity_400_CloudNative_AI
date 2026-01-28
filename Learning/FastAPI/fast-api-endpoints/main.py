from fastapi import FastAPI
app = FastAPI()
@app.get("/todo")
def todo() -> list[dict[str, int | str]]:
    return [
        {
            "id": 1,
            "task": "Implement FastAPI application"
        },
        {
            "id": 2,
            "task": "Create endpoints for CRUD operations"
        }
    ]

@app.get("/todo/{todo_id}")
def todo1(todo_id: int, add_detail: bool = False):
    if add_detail:
        return {
            "id": todo_id,
            "task": "Implement FastAPI application",
            "detail": "This task involves setting up the FastAPI framework and creating necessary endpoints."
        }
    if todo_id < 1 :
        return {
            "error": "Invalid task ID"
        }
    # Return a single todo item based on the ID
    return {
        "id": todo_id,
        "task": f"Task with ID {todo_id}"
    }
       


@app.get("/todo/2")
def todo2():
    return [
        {
            "id": 1,
            "task": "Implement FastAPI application"
        },
        {
            "id": 2,
            "task": "Create endpoints for CRUD operations"
        }
    ]
