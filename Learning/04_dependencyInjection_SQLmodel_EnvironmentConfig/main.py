from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel, Field


app = FastAPI(title="Dependency Injection with SQLModel and Environment Config")


class TASK(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str


@app.get("/")
def read_root():
    return {"Hello": "World"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
