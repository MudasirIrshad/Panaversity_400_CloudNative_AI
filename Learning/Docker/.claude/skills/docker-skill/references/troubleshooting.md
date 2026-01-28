# Docker Troubleshooting Guide

## Common Docker Issues and Solutions

### 1. Permission Denied Errors

**Issue**: Permission denied when running Docker commands
```bash
docker: Got permission denied while trying to connect to the Docker daemon socket.
```

**Solution**:
- On Linux, add user to docker group:
```bash
sudo usermod -aG docker $USER
# Then log out and log back in
```
- On Windows/Mac, ensure Docker Desktop is running with appropriate permissions

### 2. Port Already Allocated

**Issue**: Cannot start container due to port conflict
```bash
docker: Error response from daemon: driver failed programming external connectivity on endpoint...
Bind for 0.0.0.0:3000 failed: port is already allocated.
```

**Solutions**:
1. Find what's using the port:
```bash
# Linux/Mac
lsof -i :3000
# Windows
netstat -ano | findstr :3000
```

2. Stop the conflicting process or use a different port:
```bash
docker run -p 3001:3000 my-app
```

3. Stop all containers using the port:
```bash
docker ps -q --filter "publish=3000" | xargs docker stop
```

### 3. Out of Disk Space

**Issue**: Docker commands fail due to insufficient disk space

**Solutions**:
1. Clean up unused Docker objects:
```bash
# Remove unused containers, networks, images
docker system prune

# Remove unused volumes (be careful with this)
docker volume prune

# Remove all unused objects (including volumes)
docker system prune -a --volumes
```

2. Check Docker disk usage:
```bash
docker system df
```

3. Clean up specific objects:
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused networks
docker network prune
```

### 4. Container Keeps Restarting

**Issue**: Container exits immediately or keeps restarting

**Solutions**:
1. Check container logs:
```bash
docker logs <container-name-or-id>
```

2. Run container interactively to debug:
```bash
docker run -it <image-name> /bin/sh
```

3. Check entrypoint/command in Dockerfile:
```dockerfile
# Make sure the command exists and is executable
CMD ["python", "app.py"]
# Ensure app.py exists and has proper shebang if needed
```

4. Check health check configuration:
```dockerfile
# Incorrect health check can cause restarts
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

### 5. Image Build Failures

**Issue**: Docker build fails with various errors

**Solutions**:
1. Check Dockerfile syntax:
```bash
# Validate Dockerfile for syntax errors
docker build --no-cache -t test-image .
```

2. Clear build cache:
```bash
docker builder prune
# Or for older Docker versions
docker system prune -a
```

3. Increase build context timeout:
```bash
# Set higher timeout if build is slow
export DOCKER_BUILDKIT=0  # Sometimes helps with complex builds
```

4. Check for .dockerignore issues:
- Ensure required files aren't excluded
- Make sure dependencies aren't ignored

### 6. Network Connectivity Issues

**Issue**: Containers can't reach each other or external networks

**Solutions**:
1. Check network configuration:
```bash
# List networks
docker network ls

# Inspect specific network
docker network inspect <network-name>
```

2. Connect container to network:
```bash
docker network connect <network-name> <container-name>
```

3. Create custom network:
```bash
docker network create my-network
docker run --network my-network --name my-app my-image
```

4. Check DNS resolution:
```bash
docker run --rm busybox nslookup google.com
```

### 7. Volume Mounting Problems

**Issue**: Data not persisting or files not accessible

**Solutions**:
1. Check volume permissions:
```bash
# On Linux, ensure correct ownership
docker run -v /host/path:/container/path -u $(id -u):$(id -g) my-app
```

2. Use named volumes instead of bind mounts in production:
```bash
# Named volume
docker volume create my-volume
docker run -v my-volume:/data my-app

# Instead of bind mount
docker run -v /local/path:/container/path my-app
```

3. Check path existence:
```bash
# Verify host path exists
ls -la /host/path
```

### 8. Memory and Resource Issues

**Issue**: Container crashes due to memory limits or high CPU usage

**Solutions**:
1. Set resource limits:
```bash
docker run --memory=512m --cpus=1.0 my-app
```

2. Monitor resource usage:
```bash
docker stats
```

3. Optimize application memory usage:
- Check for memory leaks in application
- Adjust JVM/node.js memory limits if applicable

### 9. Docker Compose Issues

**Issue**: Docker Compose fails to start services

**Solutions**:
1. Check compose file syntax:
```bash
docker-compose config
```

2. Build services explicitly:
```bash
docker-compose build
docker-compose up
```

3. Check service dependencies:
```yaml
services:
  web:
    build: .
    depends_on:
      - db
    # Note: depends_on doesn't wait for readiness, use healthchecks
```

4. View logs for specific service:
```bash
docker-compose logs web
docker-compose logs -f web  # Follow logs
```

### 10. Registry Authentication Issues

**Issue**: Can't pull/push images from/to registry

**Solutions**:
1. Login to registry:
```bash
docker login registry.example.com
```

2. Check credentials:
```bash
docker info  # Shows configured registries
```

3. Configure insecure registries (if needed):
```json
{
  "insecure-registries": ["registry.example.com:5000"]
}
```

## Debugging Strategies

### 1. Use Verbose Output
```bash
docker --debug run my-app
docker-compose --verbose up
```

### 2. Shell Access for Debugging
```bash
# Get shell access to running container
docker exec -it <container> /bin/sh

# Start container with shell
docker run -it <image> /bin/sh
```

### 3. Check Docker Daemon Logs
```bash
# Linux
sudo journalctl -u docker.service

# Mac
~/Library/Containers/com.docker.docker/Data/log/vm.log

# Windows
Event Viewer -> Applications and Services Logs -> Docker
```

### 4. Validate Configuration
```bash
# Validate Dockerfile
docker build --no-cache -t test .

# Validate compose file
docker-compose config --dry-run
```

## Diagnostic Commands

### System Information
```bash
# Docker version
docker --version

# Docker system info
docker info

# Docker disk usage
docker system df
```

### Container Diagnostics
```bash
# List containers with detailed info
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Inspect container
docker inspect <container>

# Show running processes
docker top <container>
```

### Network Diagnostics
```bash
# Test connectivity
docker run --rm busybox ping -c 3 google.com

# Check DNS resolution
docker run --rm busybox nslookup google.com

# Test port accessibility
docker run --rm busybox nc -zv <host> <port>
```

## Prevention Tips

### 1. Use .dockerignore
Always include a `.dockerignore` file to exclude unnecessary files:
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

### 2. Implement Health Checks
Add health checks to detect issues early:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

### 3. Set Resource Limits
Prevent resource exhaustion:
```bash
docker run --memory=512m --cpus=1.0 my-app
```

### 4. Use Specific Tags
Avoid using `latest` tag in production:
```dockerfile
FROM node:18.17.0-alpine  # Good
FROM node:latest         # Avoid in production
```

## Emergency Procedures

### 1. Stop All Containers
```bash
docker kill $(docker ps -q)
```

### 2. Remove All Containers
```bash
docker rm $(docker ps -aq)
```

### 3. Remove All Images
```bash
docker rmi $(docker images -q)
```

### 4. Reset Docker
```bash
# Stop Docker service
sudo systemctl stop docker

# Remove Docker data (⚠️ Destructive!)
sudo rm -rf /var/lib/docker

# Start Docker service
sudo systemctl start docker
```

Remember to always check the specific error message and logs when troubleshooting. Many issues can be resolved by carefully reading the error output and taking appropriate action based on the root cause.