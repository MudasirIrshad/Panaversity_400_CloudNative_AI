from fastapi import FastAPI, HTTPException, Request, Response

app = FastAPI()

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     print(f"\nProcessing request: {[request.method], [request.url.path]}\n")
#     response = await call_next(request)
#     print(f"\nCompleted request: {[request.method], [request.url.path]}\n")
#     return response



# CORS middleware example (commented out)
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
async def read_main():
    print("Hello World endpoint called")
    return {"message": "Hello World"}