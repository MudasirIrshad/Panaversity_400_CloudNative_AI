# Docker Concepts Deep Dive

## Core Concepts

### Container vs Virtual Machine

#### Virtual Machines (VMs)
- Full operating system for each application
- Hypervisor layer abstracts hardware
- Heavyweight (GBs of space)
- Minutes to boot up
- Resource intensive

#### Containers
- Share host OS kernel
- No hypervisor overhead
- Lightweight (MBs of space)
- Seconds to start up
- Efficient resource utilization

#### Comparison Table
| Aspect | VM | Container |
|--------|----|-----------|
| Boot Time | Minutes | Seconds |
| Size | GBs | MBs |
| Resource Usage | High | Low |
| Isolation | Complete | Process-level |
| Performance | Lower | Near-native |
| Portability | Moderate | High |

### Docker Architecture

#### Components
1. **Docker Client**: Command-line tool (CLI) that communicates with Docker daemon
2. **Docker Host**: Machine running the Docker daemon
3. **Docker Daemon**: Background process managing Docker objects
4. **Docker Registry**: Storage for Docker images (Docker Hub, private registries)
5. **Docker Objects**: Images, containers, networks, volumes, plugins

#### Interaction Flow
```
User -> Docker Client -> Docker Daemon -> Docker Registry
                      -> Docker Objects
```

### Docker Images

#### Definition
- Read-only template with instructions for creating a Docker container
- Built using a Dockerfile
- Consists of multiple layers forming a union filesystem

#### Layers Explained
```
Base Image Layer (Ubuntu 20.04)
    ↓
Dependencies Layer (Node.js, Python)
    ↓
Application Layer (Source code)
    ↓
Configuration Layer (Environment variables)
```

#### Image Properties
- Immutable: Once created, images cannot be changed
- Reusable: Multiple containers can run from the same image
- Versioned: Tagged with version identifiers
- Portable: Can be shared across platforms

### Docker Containers

#### Lifecycle
```
Created → Running → Paused/Stopped → Deleted
```

#### States
- **Running**: Active container with running processes
- **Paused**: Frozen container (resources preserved)
- **Stopped**: Inactive container (resources released)
- **Exited**: Container that has completed execution

#### Container Properties
- Isolated process with its own filesystem
- Limited resource allocation (CPU, memory, disk)
- Network connectivity options
- Volume mounting for persistent data

## Dockerfile Instructions

### FROM
- Specifies base image
- Can be used multiple times for multi-stage builds
```dockerfile
FROM ubuntu:20.04
FROM node:18-alpine AS builder
```

### RUN
- Executes commands during image build
- Creates new layer for each RUN instruction
```dockerfile
RUN apt-get update && apt-get install -y package
RUN npm install
```

### CMD
- Default command when container starts
- Can be overridden at runtime
- Only one CMD per Dockerfile (last one wins)
```dockerfile
CMD ["npm", "start"]
CMD ["/bin/bash"]
```

### ENTRYPOINT
- Sets executable command for container
- Arguments can be passed at runtime
```dockerfile
ENTRYPOINT ["./entrypoint.sh"]
ENTRYPOINT ["nginx", "-g", "daemon off;"]
```

### COPY
- Copies files from host to container
- More secure than ADD for local files
```dockerfile
COPY package*.json ./
COPY . /app
```

### ADD
- Like COPY but with additional features
- Can extract tar files and download URLs
```dockerfile
ADD archive.tar.gz /app/
ADD http://example.com/file.txt /app/
```

### WORKDIR
- Sets working directory for subsequent instructions
- Creates directory if it doesn't exist
```dockerfile
WORKDIR /app
WORKDIR /src/app
```

### ENV
- Sets environment variables
- Available during build and runtime
```dockerfile
ENV NODE_ENV=production
ENV PATH=$PATH:/app/node_modules/.bin
```

### EXPOSE
- Documents which ports are exposed
- Does not actually publish ports
```dockerfile
EXPOSE 3000
EXPOSE 80 443
```

### VOLUME
- Creates mount point for volumes
- Enables data persistence
```dockerfile
VOLUME ["/data"]
VOLUME ["/var/log", "/var/db"]
```

### LABEL
- Adds metadata to image
- Key-value pairs for documentation
```dockerfile
LABEL maintainer="user@example.com"
LABEL version="1.0"
```

## Docker Networking

### Network Types

#### Bridge Network (Default)
- Private internal network
- Containers connected to same bridge can communicate
- Accessible from host via port mapping
```bash
docker run -p 8080:80 nginx
```

#### Host Network
- No network isolation
- Container shares host's network stack
```bash
docker run --network host nginx
```

#### None Network
- No network connectivity
- Disables all networking
```bash
docker run --network none busybox
```

#### Overlay Network
- Multi-host networking
- Used with Docker Swarm
```bash
docker network create --driver overlay my-overlay-net
```

### Container Communication
```
Container A ↔ Bridge Network ↔ Container B
              ↓
        Host Machine ↔ External Network
```

### Port Mapping
- Maps container ports to host ports
- Syntax: `-p HOST_PORT:CONTAINER_PORT`
```bash
# Map port 3000 to 8080
docker run -p 8080:3000 my-app

# Map to specific host IP
docker run -p 127.0.0.1:8080:3000 my-app
```

## Docker Volumes

### Volume Types

#### Named Volumes
- Managed by Docker
- Persistent data storage
- Recommended for databases
```bash
docker volume create my-volume
docker run -v my-volume:/data mysql
```

#### Anonymous Volumes
- No explicit name
- Removed with container unless referenced
```bash
docker run -v /data mysql
```

#### Bind Mounts
- Maps host directory to container
- Direct access to host files
```bash
docker run -v /host/path:/container/path my-app
```

#### tmpfs Mounts
- Stores data in host memory only
- Not persisted to host filesystem
```bash
docker run --tmpfs /tmp my-app
```

### Volume Best Practices
- Use named volumes for important data
- Don't rely on anonymous volumes for persistent data
- Use bind mounts carefully in production
- Regular backup of named volumes

## Docker Compose

### Service Definition
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    environment:
      - ENV=production
```

### Networks in Compose
```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - frontend
      - backend

  db:
    image: postgres
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

### Volumes in Compose
```yaml
version: '3.8'
services:
  db:
    image: postgres
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
    driver: local
```

### Environment Configuration
```yaml
version: '3.8'
services:
  app:
    image: my-app
    env_file:
      - .env
    environment:
      - NODE_ENV=production
```

## Security Concepts

### Root User Problem
- Containers often run as root by default
- Security risk: compromised container has elevated privileges
- Solution: Create and use non-root user

### Non-Root User Setup
```dockerfile
# Create user during build
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser
```

### Security Scanning
- Scan base images for vulnerabilities
- Use minimal base images (alpine, distroless)
- Regular updates of base images
- Tools: Trivy, Clair, Docker Scout

### Resource Limits
```bash
# Limit memory and CPU
docker run --memory=512m --cpus=1.0 my-app

# In Docker Compose
services:
  app:
    image: my-app
    mem_limit: 512m
    mem_reservation: 256m
    cpus: 1.0
```

## Multi-Stage Builds

### Purpose
- Reduce final image size
- Separate build and runtime dependencies
- Security: don't include build tools in final image

### Example: Node.js Application
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
EXPOSE 3000
CMD ["npm", "start"]
```

### Example: Go Application
```dockerfile
# Build stage
FROM golang:1.19 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

# Final stage
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/myapp .
CMD ["./myapp"]
```

## Layer Caching

### Caching Principles
- Docker caches each layer
- Cache invalidation happens when layer content changes
- Order matters: stable layers first

### Optimized Layer Ordering
```dockerfile
# Good: Dependencies rarely change
FROM node:18
WORKDIR /app
COPY package*.json ./        # Copy package files first
RUN npm install             # Install dependencies
COPY . .                    # Copy source code last
CMD ["npm", "start"]

# Less efficient: Source changes frequently
FROM node:18
WORKDIR /app
COPY . .                    # Copy everything first
RUN npm install             # Dependencies rebuild when source changes
CMD ["npm", "start"]
```

### Cache Optimization Techniques
- Pin specific base image versions
- Group related RUN instructions
- Use .dockerignore to exclude unnecessary files
- Leverage build cache with --cache-from

## Health Checks

### Purpose
- Monitor container health
- Automated restart of unhealthy containers
- Better orchestration decisions

### Health Check Definition
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

### Health States
- **starting**: Container is starting up
- **healthy**: Health check passed
- **unhealthy**: Health check failed
- **none**: No health check defined

### Docker Compose Health Check
```yaml
version: '3.8'
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Best Practices Summary

### Image Creation
- Use official base images
- Pin to specific versions
- Implement multi-stage builds
- Remove unnecessary packages
- Use non-root users
- Scan for vulnerabilities

### Container Management
- Set resource limits
- Implement health checks
- Use proper logging
- Handle graceful shutdown
- Use volumes for persistent data

### Security
- Run as non-root user
- Use minimal base images
- Apply least privilege principle
- Regular security scanning
- Use read-only root filesystem when possible

### Performance
- Optimize layer caching
- Minimize image size
- Use appropriate storage drivers
- Monitor resource usage
- Implement proper networking