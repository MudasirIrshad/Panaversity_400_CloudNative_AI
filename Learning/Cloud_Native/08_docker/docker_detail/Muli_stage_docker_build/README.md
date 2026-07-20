# Docker Multi-Stage Build (Complete Beginner's Guide)

# Project
Flask Two-Tier Application using Multi-Stage Docker Build

---

# What is a Multi-Stage Docker Build?

A **Multi-Stage Docker Build** is a Docker feature that allows us to use **multiple `FROM` instructions** inside a single Dockerfile.

Each `FROM` instruction creates a **new stage**.

Instead of putting everything (build tools, dependencies, source code, runtime) into one large Docker image, we split the build into multiple stages.

Usually:

- **Stage 1** → Build the application
- **Stage 2** → Create a lightweight production image

Only the files needed to run the application are copied into the final image.

---

# Why was Multi-Stage Build Introduced?

Before Docker 17.05, developers usually created a Docker image like this:

```
Python
│
├── Source Code
├── pip
├── gcc
├── build-essential
├── compilers
├── temporary files
├── cache
├── debugging tools
└── application
```

Everything remained inside the image.

Result:

- Huge image size
- Slow deployments
- Poor security
- Wasted storage
- Longer download time

Docker introduced **Multi-Stage Builds** to solve this problem.

---

# Why Do We Need Multi-Stage Builds?

Imagine you are building a house.

To build the house you need:

- Cement mixer
- Drilling machine
- Hammer
- Ladder
- Workers

After the house is completed, do you leave all these tools inside the house?

No.

You remove all construction tools and only keep the finished house.

Docker works exactly the same way.

Stage 1 is the construction phase.

Stage 2 is the finished house.

---

# Problems Solved by Multi-Stage Builds

## Smaller Images

Only the runtime files are copied.

Example

Without Multi-Stage

```
Image Size = 1.2 GB
```

With Multi-Stage

```
Image Size = 180 MB
```

---

## Better Security

Compilers like

```
gcc
g++
make
build-essential
```

are not included in the production image.

An attacker cannot misuse build tools because they simply do not exist.

---

## Faster Downloads

Smaller images mean

- Faster pull
- Faster push
- Faster deployment

---

## Lower Storage Usage

Instead of storing a 1 GB image,

you may only store a 150 MB image.

---

## Cleaner Production Environment

Production only contains:

- Application
- Runtime
- Required libraries

Nothing else.

---

# How Does Multi-Stage Build Work?

Docker executes the Dockerfile from top to bottom.

Every time Docker sees

```dockerfile
FROM
```

it starts a completely new stage.

Example

```dockerfile
FROM python:3.9 AS builder
```

↓

Stage 1 starts.

Later

```dockerfile
FROM python:3.9-slim
```

↓

Stage 2 starts.

Anything not copied from Stage 1 disappears.

---

# General Structure

```
Stage 1
--------
Build Application

↓

Copy required files

↓

Stage 2
--------
Run Application
```

---

# Your Dockerfile Explained

---

# Stage 1

```dockerfile
FROM python:3.9 AS builder
```

## What is happening?

Docker downloads

```
python:3.9
```

This becomes the base image for Stage 1.

The stage is named

```
builder
```

The name allows us to copy files later.

---

```dockerfile
WORKDIR /app
```

Creates

```
/app
```

inside the container.

Every command after this runs inside

```
/app
```

Equivalent to

```
cd /app
```

---

```dockerfile
RUN apt-get update
```

Downloads the latest package information.

---

```dockerfile
RUN apt-get upgrade -y
```

Updates installed packages.

---

```dockerfile
RUN apt-get install -y gcc default-libmysqlclient-dev pkg-config
```

Installs build tools.

### gcc

GNU C Compiler

Needed because

```
mysqlclient
```

contains C extensions.

---

### default-libmysqlclient-dev

Provides

- MySQL header files
- Client libraries

Needed to compile

```
mysqlclient
```

---

### pkg-config

Helps locate installed libraries.

Without it,

compilation may fail.

---

```dockerfile
COPY requirements.txt .
```

Copies

```
requirements.txt
```

into

```
/app
```

---

```dockerfile
RUN pip install mysqlclient
```

Installs

```
mysqlclient
```

---

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

Installs all Python packages.

The option

```
--no-cache-dir
```

prevents pip from storing cache,

making the image smaller.

---

```dockerfile
COPY . .
```

Copies the entire project into

```
/app
```

---

At this point Stage 1 contains

```
Python

gcc

MySQL development libraries

pip

requirements

source code

temporary files

compiled packages
```

This stage is **large**.

---

# Stage 2

```dockerfile
FROM python:3.9-slim
```

Docker starts a brand-new stage.

Notice that it uses

```
python:3.9-slim
```

instead of

```
python:3.9
```

Why?

Because

```
python:3.9-slim
```

is much smaller.

Example

```
python:3.9

≈ 900 MB

python:3.9-slim

≈ 120 MB
```

---

```dockerfile
WORKDIR /app
```

Creates

```
/app
```

again.

Remember

Every stage is independent.

---

```dockerfile
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
```

This is the most important command.

It means

Copy

```
/usr/local/lib/python3.9/site-packages
```

from

```
builder
```

to

```
/usr/local/lib/python3.9/site-packages
```

inside the final image.

This copies all installed Python packages.

Without this command,

Flask,

mysqlclient,

and other libraries would not exist.

---

```dockerfile
COPY . .
```

Copies the application source code.

---

```dockerfile
RUN apt-get update && apt-get install -y libmariadb3
```

Why is this needed?

The package

```
mysqlclient
```

depends on

```
libmariadb.so.3
```

Without

```
libmariadb3
```

the application crashes with

```
ImportError

libmariadb.so.3 not found
```

This installs only the runtime library,

not the compiler.

---

```dockerfile
CMD ["python", "app.py"]
```

Starts

```
python app.py
```

when the container runs.

---

# What Does COPY --from Mean?

Syntax

```dockerfile
COPY --from=<stage-name> <source> <destination>
```

Example

```dockerfile
COPY --from=builder /app/build /usr/share/nginx/html
```

Meaning

Copy files

FROM

```
builder
```

TO

the current stage.

---

# Difference Between Stages

## Stage 1

Purpose

Build application

Contains

- gcc
- pip
- compilers
- build tools
- temporary files

Image Size

Large

---

## Stage 2

Purpose

Run application

Contains

- Python
- Application
- Runtime libraries

Image Size

Small

---

# Build the Image

```bash
docker build -t flask-app-mini .
```

Explanation

```
docker build
```

Build an image.

```
-t
```

Assign a tag.

```
flask-app-mini
```

Image name.

```
.
```

Current directory as build context.

---

# Run the Container

```bash
docker run -d --name flask-app -p 5000:5000 flask-app-mini
```

---

# Check Running Containers

```bash
docker ps
```

---

# View Logs

```bash
docker logs flask-app
```

---

# Stop the Container

```bash
docker stop flask-app
```

---

# Remove the Container

```bash
docker rm flask-app
```

---

# List Images

```bash
docker images
```

---

# Inspect Image Layers

```bash
docker history flask-app-mini
```

This shows every layer created during the build.

---

# Advantages of Multi-Stage Builds

- Smaller Docker images
- Faster deployments
- Improved security
- Lower bandwidth usage
- Cleaner production environment
- Easier maintenance
- Better caching
- Faster CI/CD pipelines
- Reduced attack surface
- Production contains only what is needed

---

# Best Practices

- Use `AS <stage-name>` to give stages meaningful names (e.g., `builder`).
- Use lightweight runtime images such as `python:3.9-slim` or Alpine-based images when appropriate.
- Install build tools only in the builder stage.
- Install only runtime libraries (e.g., `libmariadb3`) in the final stage.
- Use `COPY requirements.txt` before `COPY . .` to maximize Docker layer caching.
- Use `pip install --no-cache-dir` to avoid storing pip caches.
- Add a `.dockerignore` file to exclude unnecessary files like `.git`, `__pycache__`, virtual environments, and logs.

---

# Single-Stage vs Multi-Stage

| Feature | Single-Stage Build | Multi-Stage Build |
|----------|--------------------|-------------------|
| Image Size | Large | Small |
| Build Tools Included | Yes | No |
| Security | Lower | Higher |
| Deployment Speed | Slower | Faster |
| Production Ready | Less Ideal | Yes |
| Storage Usage | High | Low |
| Best For | Development | Production |

---

# Conclusion

A Multi-Stage Docker Build separates the **build environment** from the **runtime environment**. The first stage installs compilers, development libraries, and builds the application. The final stage starts with a fresh, lightweight image and copies only the application and its required runtime dependencies. This results in smaller, faster, more secure, and production-ready Docker images.
