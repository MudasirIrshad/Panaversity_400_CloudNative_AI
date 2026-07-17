# Docker Command Cheat Sheet

This README contains the most commonly used Docker commands for building, running, managing, and debugging Docker images and containers.

---

# 1. Check Docker Version

```bash
docker --version
```

Displays the installed Docker version.

Example:

```text
Docker version 28.x.x
```

---

# 2. Check Docker Information

```bash
docker info
```

Displays detailed information about Docker Engine.

Shows:

- Number of containers
- Number of images
- Storage driver
- Docker root directory
- CPU
- Memory

---

# 3. Download an Image

```bash
docker pull <image-name>
```

Example:

```bash
docker pull node:22
docker pull python:3.12
docker pull mysql:8.0
```

Downloads an image from Docker Hub.

---

# 4. List Images

```bash
docker images
```

Shows all downloaded images.

Example:

```text
REPOSITORY   TAG       IMAGE ID       SIZE

node         22        a123bc...      1.2GB
python       3.12      d456ef...      980MB
mysql        8.0       98af12...      620MB
```

---

# 5. Remove an Image

```bash
docker rmi <image-name>
```

Example:

```bash
docker rmi node:22
```

or

```bash
docker rmi image_id
```

---

# 6. Build an Image

```bash
docker build -t my-app .
```

Explanation:

```
docker build
```

Creates a Docker image.

```
-t
```

Assigns a name (tag) to the image.

```
my-app
```

Image name.

```
.
```

Current directory (Docker looks for Dockerfile here and uses this directory as the build context).

---

# 7. Build using another Dockerfile

```bash
docker build -f dev.Dockerfile -t my-app .
```

Useful when multiple Dockerfiles exist.

---

# 8. Run a Container

```bash
docker run my-app
```

Creates and starts a container from an image.

---

# 9. Run Container in Background

```bash
docker run -d my-app
```

```
-d
```

Detached mode.

Container runs in the background.

---

# 10. Run Container Interactively

```bash
docker run -it ubuntu bash
```

```
-i
```

Interactive mode.

```
-t
```

Allocates a terminal.

```
bash
```

Starts the Bash shell.

---

# 11. Give a Container a Name

```bash
docker run --name my-container my-app
```

Instead of random names like

```
happy_tesla
```

Docker creates

```
my-container
```

---

# 12. Publish a Port

```bash
docker run -p 8000:8000 my-app
```

Syntax

```
-p HOST_PORT:CONTAINER_PORT
```

Example

```
localhost:8000
↓

Docker Container

↓

Port 8000
```

---

# 13. Run in Background with Name and Port

```bash
docker run -d \
-p 8000:8000 \
--name node-app \
node-proj
```

Explanation

```
-d
```

Run in background.

```
-p 8000:8000
```

Expose port.

```
--name node-app
```

Container name.

```
node-proj
```

Image name.

---

# 14. View Running Containers

```bash
docker ps
```

Shows only running containers.

---

# 15. View All Containers

```bash
docker ps -a
```

Shows

- Running
- Stopped
- Exited containers

---

# 16. Stop a Container

```bash
docker stop container_name
```

Example

```bash
docker stop node-app
```

---

# 17. Start a Container

```bash
docker start node-app
```

Starts an existing stopped container.

---

# 18. Restart a Container

```bash
docker restart node-app
```

---

# 19. Remove a Container

Container must be stopped first.

```bash
docker rm node-app
```

Force remove

```bash
docker rm -f node-app
```

---

# 20. Execute Commands Inside a Running Container

```bash
docker exec -it node-app bash
```

Enters the running container.

Python example

```bash
docker exec -it python-container python
```

MySQL example

```bash
docker exec -it mysql-container mysql -uroot -proot
```

---

# 21. View Logs

```bash
docker logs node-app
```

Follow logs

```bash
docker logs -f node-app
```

---

# 22. Inspect Container

```bash
docker inspect node-app
```

Displays

- IP Address
- Mounts
- Network
- Volumes
- Environment Variables

---

# 23. Copy Files

Host → Container

```bash
docker cp app.js node-app:/app
```

Container → Host

```bash
docker cp node-app:/app/app.js .
```

---

# 24. View Resource Usage

```bash
docker stats
```

Shows

- CPU
- RAM
- Network
- Disk

---

# 25. Show Docker Processes

```bash
docker top node-app
```

Shows Linux processes running inside container.

---

# 26. Show Image History

```bash
docker history my-app
```

Displays image layers.

---

# 27. Save an Image

```bash
docker save -o node-app.tar node-proj
```

Exports an image.

---

# 28. Load an Image

```bash
docker load -i node-app.tar
```

Imports an image.

---

# 29. Remove Unused Containers

```bash
docker container prune
```

Removes stopped containers.

---

# 30. Remove Unused Images

```bash
docker image prune
```

---

# 31. Remove Everything Unused

```bash
docker system prune
```

Remove everything including images

```bash
docker system prune -a
```

---

# 32. View Volumes

```bash
docker volume ls
```

---

# 33. Remove Volume

```bash
docker volume rm volume_name
```

---

# 34. List Networks

```bash
docker network ls
```

---

# 35. Remove Network

```bash
docker network rm network_name
```

---

# 36. Login to Docker Hub

```bash
docker login
```

---

# 37. Push an Image

```bash
docker push username/my-app
```

---

# 38. Pull an Image

```bash
docker pull username/my-app
```

---

# 39. Tag an Image

```bash
docker tag my-app username/my-app:v1
```

---

# 40. Search Docker Hub

```bash
docker search nginx
```

---

# Common Docker Workflow

## Step 1

Write your application.

```
app.js
```

---

## Step 2

Create

```
Dockerfile
```

---

## Step 3

Build image

```bash
docker build -t node-proj .
```

---

## Step 4

Verify image

```bash
docker images
```

---

## Step 5

Run container

```bash
docker run -d \
-p 8000:8000 \
--name node-app \
node-proj
```

---

## Step 6

Check running containers

```bash
docker ps
```

---

## Step 7

Open application

```
http://localhost:8000
```

---

## Step 8

View logs

```bash
docker logs node-app
```

---

## Step 9

Enter the container

```bash
docker exec -it node-app bash
```

---

## Step 10

Stop container

```bash
docker stop node-app
```

---

## Step 11

Start container again

```bash
docker start node-app
```

---

## Step 12

Delete container

```bash
docker rm -f node-app
```

---

# Understanding Docker Terminology

## Dockerfile

A text file that contains instructions to build an image.

Example:

```Dockerfile
FROM node:22

WORKDIR /app

COPY . .

RUN npm install

EXPOSE 8000

CMD ["npm","start"]
```

---

## Image

A blueprint/template used to create containers.

Example:

```
node-proj
```

Think of it as a class in programming.

---

## Container

A running instance of an image.

Example:

```
node-app
```

Think of it as an object created from a class.

---

## Build Context

The folder passed to Docker during build.

Example

```bash
docker build -t node-proj .
```

The `.` means:

- Use the current directory as the build context.
- Look for the `Dockerfile` in the current directory (unless another file is specified with `-f`).
- Make the files in the current directory available to instructions like `COPY` and `ADD`.

---

# Summary

```
Dockerfile
      │
      ▼
docker build
      │
      ▼
Docker Image
      │
docker run
      │
      ▼
Running Container
      │
localhost:8000
```
