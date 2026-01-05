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

