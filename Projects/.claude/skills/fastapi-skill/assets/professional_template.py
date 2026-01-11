# Professional FastAPI Project Template

This template provides a structured approach for professional FastAPI applications.

## Project Structure
```
my-fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── users.py
│   │           └── items.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── ...
│   ├── database/
│   │   ├── __init__.py
│   │   └── session.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── deps.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   └── utils/
│       ├── __init__.py
│       └── ...
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_main.py
│   └── api/
│       └── test_users.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
└── docker-compose.yml
```

## Main Application File (app/main.py)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import users, items
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(items.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
```

## Configuration File (app/core/config.py)
```python
from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = []

    # Database settings
    DATABASE_URL: str

    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

## Example API Endpoint (app/api/v1/endpoints/users.py)
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.user import User, UserCreate
from app.dependencies.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    # Implementation here
    pass

@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100):
    # Implementation here
    pass

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int):
    # Implementation here
    pass

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    # Implementation here
    pass

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    # Implementation here
    pass
```

## Example Model (app/models/user.py)
```python
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
```

## Requirements Files

### requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

### requirements-dev.txt
```
-r requirements.txt
pytest==7.4.3
pytest-cov==4.1.0
httpx==0.25.2
black==23.11.0
flake8==6.1.0
mypy==1.7.1
```

## Dockerfile
```
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Compose
```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Test Configuration (tests/conftest.py)
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
```

## Example Test (tests/test_main.py)
```python
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
```