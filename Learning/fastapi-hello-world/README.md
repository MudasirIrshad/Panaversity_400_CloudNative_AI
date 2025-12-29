# FastAPI Hello World

A minimal FastAPI "Hello World" application to get started with FastAPI.

## Running the Application

To run the application, use the following command:

```bash
cd fastapi-hello-world
uv run uvicorn main:app --reload
```

Then open your browser and go to:
- `http://127.0.0.1:8000` - Returns "Hello World"
- `http://127.0.0.1:8000/items/1?q=test` - Example with path and query parameters

## Dependencies

- FastAPI
- Uvicorn (ASGI server)