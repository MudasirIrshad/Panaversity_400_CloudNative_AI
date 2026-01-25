from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print(f"\nProcessing request: {[request.method], [request.url.path]}\n")
    response = await call_next(request)
    print(f"\nCompleted request: {[request.method], [request.url.path]}\n")
    return response


@app.get("/hello")
async def read_main():
    print("Hello World endpoint called")
    return {"message": "Hello World"}