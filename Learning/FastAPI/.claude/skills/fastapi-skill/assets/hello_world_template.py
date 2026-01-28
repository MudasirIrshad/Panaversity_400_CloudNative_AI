# FastAPI Hello World Template

This is a basic FastAPI application template to get you started.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

To run this application:
1. Install FastAPI and Uvicorn: `pip install fastapi uvicorn`
2. Save this code as `main.py`
3. Run: `uvicorn main:app --reload`
4. Visit http://localhost:8000 to see the Hello World response
5. Visit http://localhost:8000/docs to see the interactive API documentation