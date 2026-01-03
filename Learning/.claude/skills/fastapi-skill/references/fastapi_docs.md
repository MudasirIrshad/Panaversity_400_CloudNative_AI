# FastAPI Official Documentation Reference

## FastAPI Features

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

### Key Features
- **Very high performance**: On par with Node.js and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
- **Fast to code**: Increase the speed of development of features by about 200% to 300%.
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors.
- **Intuitive**: Great editor support. Completion everywhere. Less time debugging.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Short**: Minimal code duplication. Multiple features from each parameter declaration.
- **Robust**: Get production-ready code. With automatic interactive documentation.
- **Standards-based**: Based on (and fully compatible with) the open standards for APIs: OpenAPI and JSON Schema.

## Type Hints Introduction

Python type hints provide a way to specify the type of a variable, function parameter, or return value. FastAPI uses these type hints to:

- Validate incoming data
- Convert data to the specified type
- Provide automatic documentation
- Enable editor support and autocompletion

### Basic Type Hints
```python
def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name
```

### Advanced Type Hints
```python
from typing import Union

def get_name_with_age(name: str, age: Union[int, None] = None):
    if age:
        return name + " is " + str(age)
    return name
```

## Path Parameters and Number Validation

Path parameters are defined in the path of the URL using curly braces `{}`.

### Basic Path Parameters
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### Path Parameters with Predefined Values
```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    return {"model_name": model_name, "message": "LeCNN all the images"}
```

## Query Parameters and String Validation

Query parameters are the parameters that come after the `?` in the URL.

### Basic Query Parameters
```python
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}
```

### Optional Parameters
```python
from typing import Union

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

### Query Parameters with Validation
```python
from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

## Request Body

A request body is data sent by the client to your API. A response body is the data your API sends to the client.

### Creating Data with Pydantic Models
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Fields with Constraints
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Union[str, None] = Field(default=None, example="A very nice Item")
    price: float = Field(..., gt=0, example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2)
```

## Extra Data Types

FastAPI supports additional data types beyond the basic Python types.

### More Data Types
```python
from datetime import datetime, time, timedelta
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: int,
    start_datetime: Union[datetime, None] = None,
    end_datetime: Union[datetime, None] = None,
    repeat_at: Union[time, None] = None,
    process_after: Union[timedelta, None] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
```

## Bodies of Pure Lists

You can declare a request body as a list of objects.

### List Request Body
```python
from typing import List

@app.post("/index-weights/")
async def create_index_weights(index_weights: List[float]):
    return index_weights
```

## Cookie Parameters

You can access cookie parameters the same way you access query parameters.

### Cookie Parameters
```python
from fastapi import FastAPI, Cookie

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}
```

## Header Parameters

You can access header parameters the same way you access query and cookie parameters.

### Header Parameters
```python
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}
```

## Response Model

You can declare the type used for the response by annotating the return type of your path operation function.

### Response Model
```python
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

### Response Model with Attributes Excluded
```python
class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: str
    full_name: Union[str, None] = None

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> UserOut:
    return user
```

## Extra Models

You might need to use several related models that share some data.

### Multiple Models
```python
class UserBase(BaseModel):
    username: str
    email: str

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

## Response Status Code

You can set the status code to return in the response with the parameter `status_code` in any of your path operations.

### Setting Status Code
```python
from fastapi import FastAPI
from fastapi import status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

## Form Data

When you need to receive form data instead of JSON, you can use `Form`.

### Form Data
```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

## Request Files

You can receive file uploads in your FastAPI application with `File`.

### Upload File
```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

## Multiple Files

You can receive multiple files by using `List` from Python's standard library.

### Multiple Files Upload
```python
from typing import List
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}
```

## Dependencies

FastAPI provides a powerful dependency injection system that allows you to declare dependencies that other dependencies can use.

### Creating Dependencies
```python
from fastapi import Depends, FastAPI

app = FastAPI()

async def common_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

### Classes as Dependencies
```python
class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    return commons
```

## Security

FastAPI provides several built-in security utilities that follow security best practices.

### OAuth2 with Password (and hashing) with Bearer token
```python
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

## Middleware

Middleware is a function that works with every request before it is processed by any specific path operation. And also with every response before returning it.

### Creating Middleware
```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app = FastAPI()
app.add_middleware(CustomMiddleware)
```

### Using Decorator for Middleware
```python
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Testing

FastAPI provides utilities for testing your application using the `TestClient`.

### Testing with TestClient
```python
from fastapi.testclient import TestClient

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

### Testing with Dependencies
```python
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends

app = FastAPI()

def get_user():
    return {"user_id": 123, "name": "John Doe"}

@app.get("/me")
def get_me(user: dict = Depends(get_user)):
    return user

def test_get_me():
    # Override the dependency for testing
    app.dependency_overrides[get_user] = lambda: {"user_id": 999, "name": "Test User"}

    client = TestClient(app)
    response = client.get("/me")
    assert response.status_code == 200
    assert response.json() == {"user_id": 999, "name": "Test User"}

    # Clean up the override
    app.dependency_overrides = {}
```

## Background Tasks

You can define background tasks to be run after returning a response.

### Background Tasks
```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def send_email_task(recipient: str, message: str):
    # Simulate sending an email
    print(f"Sending email to {recipient} with message: {message}")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_task, email, "some notification")
    return {"message": "Notification sent in the background"}
```

## Advanced Dependencies

### Dependencies with yield

Dependencies can also use `yield` to perform cleanup operations after the request is processed.

```python
from contextlib import contextmanager
from fastapi import Depends, FastAPI

app = FastAPI()

@contextmanager
def get_db():
    db = "database_connection"  # Simulate getting a database connection
    try:
        yield db
    finally:
        print("Closing database connection")  # Simulate closing the connection

async def get_db_with_yield():
    db = "database_connection"  # Simulate getting a database connection
    try:
        yield db
    finally:
        print("Closing database connection")  # Simulate closing the connection

@app.get("/items/")
async def read_items(db=Depends(get_db_with_yield)):
    return {"db": db}
```

### Sub-dependencies

Dependencies can have their own dependencies.

```python
from fastapi import Depends, FastAPI

app = FastAPI()

async def dependency_a():
    dep_a = "generator_a"
    print(f"dependency_a yielded {dep_a}")
    try:
        yield dep_a
    finally:
        print(f"dependency_a cleaned up {dep_a}")

async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = "generator_b"
    print(f"dependency_b yielded {dep_b} with dep_a: {dep_a}")
    try:
        yield dep_b
    finally:
        print(f"dependency_b cleaned up {dep_b} with dep_a: {dep_a}")

async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = "generator_c"
    print(f"dependency_c yielded {dep_c} with dep_b: {dep_b}")
    try:
        yield dep_c
    finally:
        print(f"dependency_c cleaned up {dep_c} with dep_b: {dep_b}")

@app.get("/items/")
async def read_items(
    dep_a=Depends(dependency_a),
    dep_c=Depends(dependency_c),
):
    return {"dep_a": dep_a, "dep_c": dep_c}
```