# Docker Security Guide

## Security Fundamentals

### Container Isolation
Docker containers provide process isolation but share the host kernel. This creates a security boundary that is stronger than simple processes but weaker than virtual machines.

### Attack Surface Reduction
- Minimize packages and dependencies in images
- Use minimal base images
- Remove unnecessary tools and services
- Disable unused Docker daemon features

## Image Security

### 1. Base Image Security
- Use official images from trusted sources
- Pin to specific versions instead of using `latest`
- Regularly update base images to patch vulnerabilities
- Scan images for known vulnerabilities

```dockerfile
# Good - pinned to specific version
FROM python:3.11.5-slim

# Avoid - latest tag can introduce unexpected changes
FROM python:latest
```

### 2. Vulnerability Scanning
Regularly scan images using security tools:
- **Trivy**: Open-source vulnerability scanner
- **Clair**: CoreOS vulnerability analysis tool
- **Docker Scout**: Docker's built-in security scanning
- **Anchore**: Enterprise container security

Example scanning command:
```bash
# Using Trivy
trivy image my-app:latest

# Using Docker Scout
docker scout cves my-app:latest
```

### 3. Minimize Attack Surface
- Remove unnecessary packages:
```dockerfile
RUN apt-get update && apt-get install -y package \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*
```

## Runtime Security

### 1. Non-Root User Execution
Always run containers as non-root users:

```dockerfile
# Create application user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser
```

Alternative approach using numeric UID:
```dockerfile
# Using numeric UID for compatibility
USER 1000:1000
```

### 2. Read-Only Root Filesystem
Mount the root filesystem as read-only when possible:

```bash
# At runtime
docker run --read-only my-app

# In Docker Compose
services:
  app:
    image: my-app
    read_only: true
    # Mount writable volumes as needed
    tmpfs:
      - /tmp
      - /run
```

### 3. Seccomp and AppArmor Profiles
Use security profiles to restrict system calls:

```bash
# Use default seccomp profile
docker run --security-opt seccomp=default my-app

# Use custom seccomp profile
docker run --security-opt seccomp=./my-profile.json my-app
```

### 4. Capabilities Management
Drop unnecessary Linux capabilities:

```bash
# Drop all capabilities
docker run --cap-drop=ALL my-app

# Drop specific capabilities
docker run --cap-drop=NET_ADMIN --cap-drop=SYS_ADMIN my-app
```

## Network Security

### 1. Network Segmentation
- Use custom networks for service isolation
- Avoid using default bridge network in production
- Implement microsegmentation for sensitive services

```bash
# Create isolated network
docker network create --internal secure-network

# Run sensitive service on isolated network
docker run --network secure-network sensitive-service
```

### 2. Port Exposure
- Only expose necessary ports
- Use host binding to limit exposure
- Implement reverse proxy for additional security

```bash
# Good - bind to localhost only
docker run -p 127.0.0.1:8080:80 my-app

# Less secure - expose to all interfaces
docker run -p 8080:80 my-app
```

## Storage Security

### 1. Volume Security
- Use named volumes instead of bind mounts when possible
- Set appropriate permissions on host volumes
- Encrypt sensitive data at rest

```yaml
# Docker Compose with secure volume configuration
services:
  app:
    image: my-app
    volumes:
      - type: volume
        source: app-data
        target: /app/data
        volume:
          nocopy: true
    read_only: true
    tmpfs:
      - /tmp
      - /run

volumes:
  app-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/app-data
```

### 2. Secrets Management
Never store secrets in Docker images. Use Docker secrets or environment variables:

```bash
# Using Docker secrets (Swarm mode)
echo "my-secret-password" | docker secret create db_password -

# Using environment files
docker run --env-file .env my-app
```

## Docker Daemon Security

### 1. Daemon Configuration
- Don't expose Docker daemon socket to containers
- Use TLS for remote connections
- Limit user access to Docker group

### 2. User Management
- Restrict users in docker group
- Use sudo rules for Docker commands when appropriate
- Implement audit logging for Docker commands

## Best Practices for Secure Dockerfiles

### 1. Layer Security
```dockerfile
# Multi-stage build to minimize attack surface
FROM golang:1.19 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
RUN addgroup -g 65532 nonroot &&\
    adduser -D -u 65532 -G nonroot nonroot
USER nonroot
COPY --from=builder /app/myapp .
CMD ["./myapp"]
```

### 2. Package Management Security
```dockerfile
# Verify package signatures when possible
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*
```

### 3. File Permissions
```dockerfile
# Set appropriate file permissions
COPY --chown=appuser:appgroup . /app
RUN chmod -R 755 /app
RUN chmod 600 /app/config/secrets.conf
```

## Security Tools and Commands

### 1. Docker Bench for Security
Run security benchmarking:
```bash
# Run Docker security benchmark
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docker/docker-bench-security
```

### 2. Security Scanning
```bash
# Scan running containers
docker scan my-app:latest

# Check image history for security issues
docker history --no-trunc my-app:latest
```

### 3. Runtime Security Monitoring
- Use tools like Falco for runtime security monitoring
- Implement container activity logging
- Set up alerts for suspicious activities

## Common Security Misconfigurations

### 1. Privileged Containers
```bash
# NEVER do this unless absolutely necessary
docker run --privileged dangerous-app

# Instead, grant only required capabilities
docker run --cap-add=NET_BIND_SERVICE my-app
```

### 2. Host Network Access
```bash
# Avoid host networking unless required
docker run --network host risky-app

# Use custom networks instead
docker network create my-network
docker run --network my-network my-app
```

### 3. Host Volume Mounts
```bash
# Dangerous - gives container access to host filesystem
docker run -v /:/host my-app

# Better - mount only specific directories
docker run -v /app/data:/data my-app
```

## Compliance Considerations

### 1. PCI DSS
- Encrypt cardholder data in containers
- Implement proper access controls
- Maintain audit logs

### 2. GDPR
- Encrypt personal data at rest
- Implement data retention policies
- Ensure data portability

### 3. SOC 2
- Implement access controls and monitoring
- Maintain security logs
- Regular security assessments

## Incident Response

### 1. Compromised Container Detection
```bash
# Check running containers
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"

# Check container logs
docker logs <container-id>

# Inspect container
docker inspect <container-id>
```

### 2. Containment Procedures
```bash
# Stop compromised container
docker stop <container-id>

# Remove compromised container
docker rm <container-id>

# Pull fresh image if needed
docker pull <image>:<trusted-tag>
```

By following these security practices, you can significantly reduce the risk of security incidents in your Docker deployments. Remember that security is an ongoing process that requires regular updates, monitoring, and assessment.