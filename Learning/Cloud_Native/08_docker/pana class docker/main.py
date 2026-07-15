from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Todo_Item(BaseModel):
    item_id: int
    title: str
    description: str
    completed: bool = False

todo_items = []

@app.get("/")
def read_root():
    return {"Hello": "Mudasir Irshad"}

@app.get("/todo")
def get_todo():
    if not todo_items:
        raise HTTPException(status_code=404, detail="No todo items found")
    return todo_items

@app.post("/todo")
def create_todo(item: Todo_Item):
    todo_items.append(item)
    return {"message": "Todo item created", "item": item}

@app.patch("/todo/{item_id}/{completed}")
def update_todo(item_id: int, completed: bool):

    if item_id >= len(todo_items) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    todo_items[item_id].completed = completed
    
    return {"message": "Todo item updated", "item": todo_items[item_id]}

@app.delete("/todo/{item_id}")
def delete_todo(item_id: int):

    for i in range(len(todo_items)):
        if i == item_id:
            deleted_item = todo_items.pop(item_id)
            return {"message": "Todo item deleted", "item": deleted_item}
    
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/todo/{item_id}")
def replace_todo(item_id: int, item: Todo_Item):
    for i in range(len(todo_items)):
        if i == item_id:
            todo_items[item_id] = item
            return {"message": "Todo item replaced", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
