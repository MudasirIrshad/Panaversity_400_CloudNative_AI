from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    # SQL Model should create tables 
    print("\nStarting up...\n")
    yield
    # Shutdown code
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/hello")
async def read_root():
    return {"message": "Hello, World!"}