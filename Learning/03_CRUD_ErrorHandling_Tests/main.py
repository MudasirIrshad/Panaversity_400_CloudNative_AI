from fastapi import FastAPI
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
    return {"Hello": "World"}

@app.get("/todo")
def get_todo():
    return todo_items

@app.post("/todo")
def create_todo(item: Todo_Item):
    todo_items.append(item)
    return {"message": "Todo item created", "item": item}

@app.patch("/todo/{item_id}/{completed}")
def update_todo(item_id: int, completed: bool):
    if item_id >= len(todo_items) or item_id < 0:
        return {"error": "Item not found"}, 404
    todo_items[item_id].completed = completed
    return {"message": "Todo item updated", "item": todo_items[item_id]}

@app.delete("/todo/{item_id}")
def delete_todo(item_id: int):
    for i in range(len(todo_items)):
        if i == item_id:
            deleted_item = todo_items.pop(item_id)
            return {"message": "Todo item deleted", "item": deleted_item}
    return {"error": "Item not found"}, 404

@app.put("/todo/{item_id}")
def replace_todo(item_id: int, item: Todo_Item):
    for i in range(len(todo_items)):
        if i == item_id:
            todo_items[item_id] = item
            return {"message": "Todo item replaced", "item": item}
    return {"error": "Item not found"}, 404




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
