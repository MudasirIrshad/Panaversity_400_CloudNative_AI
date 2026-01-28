# Multi-stage Dockerfile for Python applications
# This template demonstrates best practices for containerizing Python applications

# Build stage (optional - use only if you need to compile dependencies)
# FROM python:3.11-slim as builder
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
# RUN apt-get update && apt-get install -y \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port (change as needed)
EXPOSE 8000

# Health check (adjust endpoint as needed)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["python", "app.py"]

# Alternative commands depending on your application:
# For Flask applications: CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
# For FastAPI applications: CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# For Django applications: CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Security considerations implemented:
# - Non-root user (appuser)
# - No-cache installation to reduce image size
# - PYTHONDONTWRITEBYTECODE prevents .pyc files
# - PYTHONUNBUFFERED prevents buffering of stdout/stderr
# - Health check for container monitoring
# - Minimal base image (slim variant)

# Optimization tips:
# - Multi-stage builds for smaller final images
# - Leverage Docker layer caching by copying requirements.txt separately
# - Use .dockerignore to exclude unnecessary files
# - Regularly update base image for security patches