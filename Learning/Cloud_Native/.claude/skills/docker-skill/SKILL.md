---
name: docker-skill
description: |
  Comprehensive Docker skill for containerization, image building, container management, and orchestration.
  Provides educational content for beginners while offering practical functionality for Docker tasks.
  Use when users need help with: (1) Learning Docker fundamentals, (2) Creating Dockerfiles,
  (3) Building and managing containers, (4) Docker Compose orchestration, (5) Container optimization,
  (6) Troubleshooting Docker issues, or (7) Best practices and security considerations.
license: MIT
---

# Docker Skill for Claude Code

## Overview
Docker is a platform that enables developers to automate the deployment, scaling, and management of applications in lightweight, portable containers. This skill provides comprehensive guidance for Docker tasks, from basic concepts to advanced containerization techniques.

## Table of Contents
1. [Introduction & Fundamentals](#introduction--fundamentals)
2. [Getting Started](#getting-started)
3. [Docker Images & Containers](#docker-images--containers)
4. [Dockerfile Mastery](#dockerfile-mastery)
5. [Docker Compose](#docker-compose)
6. [Advanced Topics](#advanced-topics)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices Summary](#best-practices-summary)

## Introduction & Fundamentals

### What is Docker?
Docker is a containerization platform that packages applications and their dependencies into standardized units called containers. Unlike traditional virtual machines, containers share the host operating system kernel, making them lightweight and efficient.

### Key Concepts
- **Container**: A lightweight, standalone, executable package that includes everything needed to run a piece of software
- **Image**: A read-only template with instructions for creating a Docker container
- **Dockerfile**: A text document that contains instructions for building a Docker image
- **Registry**: A storage and distribution system for Docker images (e.g., Docker Hub)

### Docker Architecture
- **Docker Client**: Command-line interface that communicates with the Docker daemon
- **Docker Daemon**: Background process that manages Docker objects
- **Docker Objects**: Images, containers, networks, and volumes

### Benefits of Docker
- **Consistency**: Applications run the same way regardless of the infrastructure
- **Portability**: Move applications between environments seamlessly
- **Efficiency**: Lighter than VMs with faster startup times
- **Scalability**: Easy to scale applications horizontally
- **Isolation**: Secure isolation between applications

## Getting Started

### Prerequisites
- Docker installed on your system
- Basic understanding of command line interfaces
- Text editor for creating Dockerfiles

### Installation
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Follow installation instructions for your OS
3. Verify installation with:
   ```bash
   docker --version
   docker run hello-world
   ```

### First Container
Try running your first container:
```bash
docker run -it ubuntu bash
```
This command downloads the Ubuntu image and runs a bash shell inside a container.

## Docker Images & Containers

### Managing Images
```bash
# List images
docker images

# Pull an image
docker pull nginx:latest

# Remove an image
docker rmi <image-id>

# Build an image from Dockerfile
docker build -t my-app .
```

### Managing Containers
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Run a container
docker run -d --name my-container nginx

# Stop a container
docker stop my-container

# Start a stopped container
docker start my-container

# Remove a container
docker rm my-container

# Execute commands in running container
docker exec -it my-container bash

# View container logs
docker logs my-container
```

### Container Networking
```bash
# Run container with port mapping
docker run -p 8080:80 nginx

# Create a custom network
docker network create my-network

# Run container on specific network
docker run --network my-network my-app
```

## Dockerfile Mastery

### Basic Dockerfile Structure
```dockerfile
# Use a base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Define the command to run the application
CMD ["npm", "start"]
```

### Common Dockerfile Instructions
- **FROM**: Sets the base image
- **WORKDIR**: Sets the working directory
- **COPY**: Copies files from host to container
- **ADD**: Similar to COPY but with additional features
- **RUN**: Executes commands during image build
- **CMD**: Default command when container starts
- **ENTRYPOINT**: Configures container to run as executable
- **EXPOSE**: Documents the port to expose
- **ENV**: Sets environment variables
- **VOLUME**: Creates mount point for volumes
- **LABEL**: Adds metadata to the image

### Best Practices for Dockerfiles
1. **Use specific image tags**: Avoid using `latest` tag in production
2. **Minimize layers**: Combine RUN commands when possible
3. **Multi-stage builds**: Use multiple FROM statements to optimize size
4. **Security**: Use non-root users when possible
5. **Layer caching**: Order instructions to leverage caching
6. **Clean up**: Remove unnecessary files to reduce image size

### Multi-stage Builds Example
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

## Docker Compose

### Docker Compose Overview
Docker Compose is a tool for defining and running multi-container Docker applications using YAML files.

### Basic docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
    environment:
      - NODE_ENV=development

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Common Docker Compose Commands
```bash
# Start services
docker-compose up

# Start services in detached mode
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Scale services
docker-compose up --scale web=3

# Execute command in service
docker-compose exec web bash
```

### Environment Variables
Create a `.env` file:
```
POSTGRES_DB=myapp
POSTGRES_USER=user
POSTGRES_PASSWORD=password
NODE_ENV=development
```

Reference in docker-compose.yml:
```yaml
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

## Advanced Topics

### Security Considerations
1. **Non-root users**: Run containers as non-root users
2. **Minimal images**: Use distroless or alpine-based images
3. **Scan images**: Regularly scan for vulnerabilities
4. **Resource limits**: Set CPU and memory limits
5. **Seccomp profiles**: Limit system calls

### Optimization Techniques
1. **Layer caching**: Order Dockerfile instructions optimally
2. **Multi-stage builds**: Reduce final image size
3. **.dockerignore**: Exclude unnecessary files
4. **Slim images**: Use smaller base images
5. **Build cache**: Use cache mounts for build tools

### CI/CD Integration
```yaml
# Example GitHub Actions workflow
name: Build and Deploy
on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Build the Docker image
      run: docker build . --file Dockerfile --tag my-image:${{ github.sha }}

    - name: Push the Docker image
      run: docker push my-image:${{ github.sha }}
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: Port Already Allocated
**Solution**: Check for running containers using the same port
```bash
docker ps
docker port <container-name>
```

#### Issue: Permission Denied
**Solution**: Add user to docker group (Linux)
```bash
sudo usermod -aG docker $USER
```

#### Issue: Out of Disk Space
**Solution**: Clean up unused Docker objects
```bash
# Remove unused containers, networks, images
docker system prune

# Remove unused volumes
docker volume prune

# Remove unused images
docker image prune
```

#### Issue: Container Keeps Restarting
**Solution**: Check container logs
```bash
docker logs <container-name>
```

### Debugging Strategies
1. **Check logs**: Always start with `docker logs`
2. **Interactive mode**: Use `docker run -it` for debugging
3. **Health checks**: Implement health checks in Dockerfile
4. **Environment verification**: Ensure environment variables are set correctly

## Best Practices Summary

### Image Creation
- Use official base images when possible
- Pin versions instead of using `latest`
- Minimize image size with multi-stage builds
- Scan images for security vulnerabilities
- Use .dockerignore to exclude unnecessary files

### Container Management
- Set resource limits to prevent resource exhaustion
- Use health checks to monitor container status
- Implement proper logging strategies
- Use volumes for persistent data
- Implement graceful shutdown handling

### Security
- Run containers as non-root users
- Use minimal base images
- Regularly update base images
- Implement network segmentation
- Apply security scanning in CI/CD pipelines

### Performance
- Optimize layer caching
- Use appropriate storage drivers
- Monitor container resource usage
- Implement proper monitoring and alerting
- Use Docker Swarm or Kubernetes for orchestration at scale

## Level-Based Learning Path

### Level 1: Docker Basics
- Understanding containers vs VMs
- Running basic Docker commands
- Pulling and running images
- Basic container management

### Level 2: Dockerfile Creation
- Writing effective Dockerfiles
- Understanding layers and caching
- Multi-stage builds
- Optimizing image size

### Level 3: Container Orchestration
- Docker Compose basics
- Multi-container applications
- Networking between containers
- Volume management

### Level 4: Advanced Topics
- Security best practices
- CI/CD integration
- Monitoring and logging
- Production deployment strategies

## Quick Reference Commands

| Purpose | Command |
|---------|---------|
| Run container | `docker run -d --name <name> <image>` |
| Build image | `docker build -t <name> .` |
| List containers | `docker ps -a` |
| Stop container | `docker stop <container>` |
| Remove container | `docker rm <container>` |
| List images | `docker images` |
| Remove image | `docker rmi <image>` |
| View logs | `docker logs <container>` |
| Execute in container | `docker exec -it <container> <command>` |
| Compose up | `docker-compose up` |
| Compose down | `docker-compose down` |

## Common Mistakes to Avoid

1. **Using 'latest' tag in production**: Always pin to specific versions
2. **Running as root**: Use USER instruction to switch to non-root user
3. **Large images**: Optimize image size with multi-stage builds
4. **No health checks**: Implement health checks for production
5. **Not cleaning up**: Regularly clean unused Docker objects
6. **Hardcoded environment variables**: Use environment files or compose files
7. **Exposing too many ports**: Only expose necessary ports
8. **No logging strategy**: Implement proper logging

This Docker skill provides comprehensive coverage of Docker concepts, from basic to advanced topics, with practical examples and best practices. Use this skill whenever you need help with Docker-related tasks, learning Docker fundamentals, or implementing containerization strategies.