FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000

LABEL NAME="My FastAPI App" \
      VERSION="1.0.0" \
      DESCRIPTION="A simple FastAPI application running in Docker" \
      AUTHOR="Mudasir Irshad"


CMD [ "uv", "run", "uvicorn", "main:app"]