# 🚀 FastAPI Microservices → Docker → Kubernetes (Complete Guide)

This document explains the **full journey** step-by-step:

1. Build FastAPI microservices
2. Containerize using Docker (multi-stage)
3. Run using Docker Compose (networking)
4. Move to Kubernetes (Pods → Services → Debugging)

---

# 🧩 1. Microservices Design (FastAPI)

We created **two services**:

## 1️⃣ Task Manager Service

- Create tasks
- Update tasks
- Delete tasks
- Store data in-memory

## 2️⃣ Task Viewer Service

- Fetch tasks from Task Manager
- Search tasks
- Read-only service

---

## 🔗 Communication Concept

```

Task Viewer → calls → Task Manager API

```

👉 Communication happens via HTTP APIs

---

# 🐳 2. Dockerization (Multi-stage Build)

## Why Docker?

- Isolate apps
- Same environment everywhere
- Easy deployment

---

## Multi-stage Dockerfile (Example)

### 🔹 Stage 1: Builder

```

FROM python:3.13-alpine AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install --system -r pyproject.toml

```

### 🔹 Stage 2: Runtime (lightweight)

```

FROM python:3.13-alpine
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY ./main.py ./
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

---

## ✅ Why Multi-stage?

- Smaller image size
- Faster deployment
- Cleaner production image

---

# 🐳 3. Docker Compose (Microservices Networking)

## Why Compose?

- Run multiple services together
- Automatic networking
- Service discovery

---

## compose.yaml

```

version: "3.9"
services:
task-manager-app:
build:
context: ./task-manager-app
dockerfile: Dockerfile.multistage
image: task-manager-image
ports:
- "8001:8000"
task-viewer-app:
build:
context: ./task-viewer-app
dockerfile: Dockerfile.multistage
image: task-viewer-image
ports:
- "8002:8000"
depends_on:
- task-manager-app
environment:
TASK_MANAGER_URL: [http://task-manager-app:8000](http://task-manager-app:8000)

```

---

## 🔗 Networking in Docker

Docker Compose creates a **shared network automatically**.

```

task-viewer → [http://task-manager-app:8000](http://task-manager-app:8000) ✅

```

---

## 🧠 Important Rule

| Scope             | URL               |
| ----------------- | ----------------- |
| Inside container  | service-name:port |
| Outside (browser) | localhost:port    |

---

# ⚠️ Common Issue (Solved)

❌ Using `localhost` inside container  
✔️ Use service name instead

---

# ☸️ 4. Moving to Kubernetes

Now we move from Docker → Kubernetes

---

# 🧱 5. Pods (First Step)

## Pod YAML (Task Manager)

```

apiVersion: v1
kind: Pod
metadata:
name: task-manager
labels:
run: task-manager
spec:
containers:
- name: task-manager
image: task-manager-image
imagePullPolicy: Never
ports:
- containerPort: 8000

```

---

## Pod YAML (Task Viewer)

```

apiVersion: v1
kind: Pod
metadata:
name: task-viewer
labels:
run: task-viewer
spec:
containers:
- name: task-viewer
image: task-viewer-image
imagePullPolicy: Never
ports:
- containerPort: 8000
env:
- name: TASK_MANAGER_URL
value: [http://task-manager:8000](http://task-manager:8000)

```

---

# ❗ Important Kubernetes Difference

```

Docker → service name works directly
Kubernetes → requires Service object

```

---

# 🌐 6. Service (VERY IMPORTANT)

## Task Manager Service

```

apiVersion: v1
kind: Service
metadata:
name: task-manager
spec:
selector:
run: task-manager
ports:
- port: 8000
targetPort: 8000

```

---

## 🧠 Why Service?

- Provides stable DNS
- Enables pod-to-pod communication
- Load balances traffic

---

## 🔗 Now communication works

```

task-viewer → [http://task-manager:8000](http://task-manager:8000) ✅

```

---

# 🔧 7. Port Forwarding

## Access from local machine

```

kubectl port-forward task-manager 8000:8000
kubectl port-forward task-viewer 8001:8000

```

## Access in browser

```

[http://localhost:8000](http://localhost:8000) → manager
[http://localhost:8001](http://localhost:8001) → viewer

```

---

# 🧪 8. Debugging Issues (Very Important)

---

## ❌ Error: ErrImagePull

### Cause:

- Image not found

### Fix:

```

imagePullPolicy: Never

```

---

## ❌ Error: Connection Refused

### Cause:

- Service not created
- Wrong URL

### Fix:

- Create Service
- Use correct DNS name

---

## ❌ Error: Pod update forbidden

### Cause:

- Pods are immutable

### Fix:

```

kubectl delete pod <name>
kubectl apply -f pod.yaml

```

---

## ❌ Logs not working

```

kubectl logs <pod>

```

👉 If image fails → logs won’t work

---

## 🔍 Debug Commands

```

kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- sh

```

---

# 🧠 9. Key Concepts Learned

---

## 1️⃣ Containers

- Isolated environment
- Same internal port allowed

---

## 2️⃣ Docker Networking

- Service name = DNS
- Automatic communication

---

## 3️⃣ Kubernetes Networking

- Pods need Services to communicate
- DNS via Service name

---

## 4️⃣ Ports

| Level     | Example    |
| --------- | ---------- |
| Container | 8000       |
| Host      | 8001, 8002 |

---

## 5️⃣ Pods vs Deployment

| Pod             | Deployment          |
| --------------- | ------------------- |
| Manual          | Managed             |
| Not scalable    | Scalable            |
| Not recommended | Production standard |

---

# 🎯 Final Architecture

```

Kubernetes Cluster
│
├── Pod: task-manager
│
├── Service: task-manager
│
└── Pod: task-viewer
│
└── calls → [http://task-manager:8000](http://task-manager:8000)

```

---

# 🚀 Final Takeaways

- Microservices communicate via APIs
- Docker Compose provides simple networking
- Kubernetes requires Services for communication
- Pods are immutable → use Deployments in real world
- Debugging is key skill

---

# 🔥 Next Steps (Recommended)

- Convert Pods → Deployments
- Add Services for all apps
- Add Ingress (single entry point)
- Use persistent DB instead of in-memory

---

# ✅ One-Line Summary

**Docker makes microservices easy locally, Kubernetes makes them scalable in production**
