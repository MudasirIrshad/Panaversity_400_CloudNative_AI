---
name: fastapi-skill
description: |
  This skill helps users create FastAPI applications from Hello World to professional level.
  It provides comprehensive guidance for building APIs, implementing security, testing, and deploying FastAPI applications.
  This skill should be used when users ask to create FastAPI applications, implement API endpoints, add authentication,
  create models, test APIs, or deploy FastAPI applications.
---

# FastAPI Skill

This skill provides comprehensive guidance for creating FastAPI applications from basic Hello World examples to professional-level implementations.

## Core FastAPI Concepts

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python based on standard Python type hints. It emphasizes high performance, ease of use, and production readiness, built on top of Starlette (for web functionality) and Pydantic (for data validation).

### Key Features
- Fast performance (on par with NodeJS and Go)
- Increases development speed by 200-300%
- Reduces ~40% of human-induced errors
- Full type safety with Python type hints
- Automatic validation and error handling
- Automatic documentation generation
- Standards-based (OpenAPI and JSON Schema compatible)

## Progressive Implementation Levels

### Level 1: Hello World
Basic FastAPI application with minimal setup:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### Level 2: Intermediate
Adding request bodies, Pydantic models, and validation:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
```

### Level 3: Professional
Advanced features including dependencies, security, and structured responses:

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
```

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI structure, patterns, conventions to integrate with |
| **Conversation** | User's specific requirements, constraints, preferences |
| **Skill References** | Domain patterns from `references/` (library docs, best practices, examples) |
| **User Guidelines** | Project-specific conventions, team standards |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

## Routing and Request Handling

### Path Parameters
```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### Query Parameters
```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}
```

### Request Body with Pydantic Models
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

## Dependency Injection System

### Basic Dependency Example
```python
from typing import Annotated
from fastapi import Depends

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

### Sharing Dependencies
```python
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/items/")
async def read_items(commons: CommonsDep):
    return commons
```

## Security and Authentication

### OAuth2 with Password Flow
```python
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

### JWT Token Authentication
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

## Response Models

### Separating Input and Output Models
```python
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str  # Don't expose this
    email: str

class UserOut(BaseModel):
    username: str
    email: str
    # password is excluded

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> UserOut:
    return user  # password automatically filtered out
```

## Testing with TestClient

### Basic Testing Example
```python
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

## Middleware Implementation

### Creating Middleware
```python
from fastapi import FastAPI
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Error Handling

### Custom HTTP Exceptions
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = ["Foo", "Bar", "Baz"]

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id >= len(items):
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
```

## Production Deployment

### ASGI Server Configuration
```bash
# Install with performance optimizations
pip install "uvicorn[standard]"

# Run manually
uvicorn main:app --host 0.0.0.0 --port 80

# Run with reload for development
uvicorn main:app --reload
```

### Production Considerations
- Don't use `--reload` in production
- Consider security (HTTPS)
- Plan for running on startup
- Implement restart strategies
- Plan for replication and memory management

## Best Practices

1. **Type-Driven Development:** Use standard Python type hints for all data models and parameters
2. **Security First:** Create separate input and output models to prevent data exposure
3. **Dependency Injection:** Use the dependency injection system for shared logic
4. **Validation:** Leverage Pydantic for automatic validation and documentation
5. **Testing:** Write comprehensive tests using TestClient
6. **Documentation:** Take advantage of automatic API documentation
7. **Performance:** Use Uvicorn with the standard extra for performance optimizations

## Project Structure for Professional Applications

```
my-fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application instance and configuration
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── users.py
│   │           └── items.py
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/             # Database schemas (if using SQLAlchemy)
│   │   ├── __init__.py
│   │   └── ...
│   ├── database/            # Database connection and session management
│   │   ├── __init__.py
│   │   └── session.py
│   ├── dependencies/        # Dependency injection functions
│   │   ├── __init__.py
│   │   └── deps.py
│   ├── core/                # Core configuration and utilities
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── ...
├── tests/                   # Test files
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_main.py
│   └── api/
│       └── test_users.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
└── docker-compose.yml
```

## Common FastAPI Patterns

### CRUD Operations Template
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Model definitions
class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    title: str | None = None

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# CRUD endpoints
@router.post("/", response_model=Item)
def create_item(item: ItemCreate):
    # Implementation here
    pass

@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100):
    # Implementation here
    pass

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int):
    # Implementation here
    pass

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    # Implementation here
    pass

@router.delete("/{item_id}")
def delete_item(item_id: int):
    # Implementation here
    pass
```

### Configuration Management
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Application"
    admin_email: str
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```