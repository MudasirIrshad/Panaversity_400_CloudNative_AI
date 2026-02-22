# Docker Best Practices Guide

## Security Best Practices

### 1. Use Non-Root Users
Always run containers as a non-root user when possible:

```dockerfile
# Create a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser
```

### 2. Use Minimal Base Images
Choose minimal base images to reduce attack surface:
- Use `alpine` variants when possible
- Consider `distroless` images for production
- Pin to specific versions instead of using `latest`

```dockerfile
# Good
FROM python:3.11-slim
FROM node:18-alpine

# Avoid
FROM python:latest
FROM ubuntu:latest
```

### 3. Scan Images for Vulnerabilities
Regularly scan your images using tools like:
- Trivy
- Clair
- Docker Scout
- Snyk

### 4. Limit Resource Usage
Set resource limits to prevent resource exhaustion:

```bash
# At runtime
docker run --memory=512m --cpus=1.0 my-app

# In Docker Compose
services:
  app:
    image: my-app
    mem_limit: 512m
    mem_reservation: 256m
    cpus: 1.0
```

## Image Optimization Best Practices

### 1. Leverage Layer Caching
Order Dockerfile instructions to maximize cache reuse:

```dockerfile
# Copy dependencies first (they change less frequently)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code last (it changes more frequently)
COPY . .
```

### 2. Multi-Stage Builds
Use multi-stage builds to reduce final image size:

```dockerfile
# Build stage
FROM golang:1.19 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

# Production stage
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/myapp .
CMD ["./myapp"]
```

### 3. Clean Up During Build
Remove unnecessary files during the build process:

```dockerfile
RUN apt-get update && apt-get install -y package \
    && rm -rf /var/lib/apt/lists/*
```

### 4. Use .dockerignore
Exclude unnecessary files with a `.dockerignore` file:

```
.git
.gitignore
README.md
Dockerfile
.dockerignore
*.md
.env
node_modules
```

## Container Management Best Practices

### 1. Proper Logging
Configure proper logging strategies:

```dockerfile
# Log to stdout/stderr for Docker to capture
CMD ["python", "-u", "app.py"]  # -u for unbuffered output
```

### 2. Health Checks
Implement health checks for better orchestration:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

### 3. Graceful Shutdown
Handle signals for graceful shutdown:

```dockerfile
# In your application code, handle SIGTERM
import signal
import sys

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    # Cleanup code here
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
```

## Networking Best Practices

### 1. Custom Networks
Use custom networks for better isolation:

```bash
# Create custom network
docker network create my-network

# Run containers on same network
docker run --network my-network --name db postgres
docker run --network my-network --name web my-app
```

### 2. Port Exposure
Only expose necessary ports:

```dockerfile
# Document the port but don't publish by default
EXPOSE 8080

# Publish only when needed
docker run -p 8080:8080 my-app
```

## Docker Compose Best Practices

### 1. Environment Variables
Use environment files for configuration:

```yaml
# docker-compose.yml
services:
  app:
    image: my-app
    env_file:
      - .env
    environment:
      - NODE_ENV=production

# .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
```

### 2. Named Volumes
Use named volumes for persistent data:

```yaml
services:
  db:
    image: postgres
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
    driver: local
```

### 3. Resource Limits
Define resource limits in compose files:

```yaml
services:
  app:
    image: my-app
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Performance Best Practices

### 1. Choose Appropriate Storage Drivers
- Use overlay2 on Linux (default)
- Use appropriate drivers for your platform

### 2. Optimize Volume Mounting
- Use named volumes for persistent data
- Use bind mounts carefully in production
- Consider using Docker Desktop WSL2 backend on Windows

### 3. Image Layering
- Combine RUN instructions to reduce layers
- Clean up in the same RUN instruction
- Remove unnecessary packages and cache

## CI/CD Best Practices

### 1. Build Cache Optimization
Use build cache in CI/CD pipelines:

```bash
# In CI/CD pipeline
docker build --cache-from my-app:latest -t my-app:new .
```

### 2. Image Tagging Strategy
Use semantic versioning or commit hashes:

```bash
# Tag with commit hash
docker build -t my-app:$(git rev-parse --short HEAD) .

# Tag with semantic version
docker build -t my-app:v1.2.3 .
```

### 3. Security Scanning in Pipeline
Integrate security scanning:

```bash
# Scan image before pushing
trivy image my-app:latest
docker scan my-app:latest
```

## Common Anti-Patterns to Avoid

### 1. Running as Root
```dockerfile
# Bad
USER root

# Good
USER appuser
```

### 2. Using Latest Tags in Production
```dockerfile
# Bad for production
FROM node:latest

# Good
FROM node:18.17.0-alpine
```

### 3. Large Images
```dockerfile
# Bad
FROM ubuntu:latest
RUN apt-get install -y python3 python3-pip git vim wget curl

# Better
FROM python:3.11-slim
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*
```

### 4. No Health Checks
```dockerfile
# Missing
HEALTHCHECK ...

# Included
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

Following these best practices will help you create more secure, efficient, and maintainable Docker deployments.