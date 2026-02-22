# Cloud Native Learning – Docker & Kubernetes

This README documents my **hands-on learning** with Docker and Kubernetes, including commands, explanations, and troubleshooting based on my experiments.  

---

## 1️⃣ Docker

### 1.1 Build Docker Image

```bash
docker build -f Dockerfile.dev -t mudasirshad/task_management_image:dev .
```

- Builds a Docker image from `Dockerfile.dev`  
- `-t` → tags the image  

### 1.2 Run Container (normal)

```bash
docker run -d --name task_management_dev -p 7000:8000 mudasirshad/task_management_image:dev
```

- `-d` → run in background (detached)  
- `--name` → container name  
- `-p 7000:8000` → map host port → container port  
- Uses the Docker image to run the app  

### 1.3 Run Container with Live Code Updates

```bash
docker run -d --name task_management_dev -p 7000:8000 -v ${PWD}:/app mudasirshad/task_management_image:dev
```

- `-v ${PWD}:/app` → mounts your local folder into the container  
- Code changes **on host are reflected instantly** inside container  

### 1.4 Remove all Docker images

```bash
docker rmi -f $(docker images -q)
```

- Deletes all images forcibly  

### 1.5 Remove all Docker containers

```bash
docker rm -f $(docker ps -aq)
```

- Deletes all running and stopped containers  

### 1.6 Interactive terminal (optional)

```bash
docker run -it -v ${PWD}:/app -w /app python:3.12 bash
```

- `-it` → interactive terminal  
- `-w /app` → sets working directory  
- Useful for live testing / running commands interactively  

---

## 2️⃣ Kubernetes (kubectl)

### 2.1 Create Namespace

```bash
kubectl create namespace mudasir
```

- Namespaces = folders for resources in the cluster  
- Helps **organize Pods and resources**  

### 2.2 Create Pod (imperative)

```bash
kubectl run my-pod --image=nginx:alpine --restart=Never -n mudasir
```

- `--restart=Never` → creates **single Pod**, not Deployment  
- `-n mudasir` → namespace  

### 2.3 Get Pods

```bash
kubectl get pods -n mudasir
```

- Shows Pod status in the namespace  

### 2.4 Pod logs

```bash
kubectl logs my-pod -n mudasir
```

- Shows container output  

### 2.5 Describe Pod (debugging)

```bash
kubectl describe pod taskmanagementapp2 -n taskmanagementapp
```

- Detailed info: containers, image, events, errors  
- Useful for **ImagePullBackOff** or other failures  

### 2.6 Get Events

```bash
kubectl get events -n taskmanagementapp
```

- Shows timeline of actions & errors in namespace  
- Always check **correct namespace**, otherwise “No resources found”  

### 2.7 Delete Pod

```bash
kubectl delete pod taskmanagementapp -n taskmanagementapp
```

- Deletes a Pod  
- After deletion, you can **recreate it**  

### 2.8 Get All Namespaces

```bash
kubectl get namespaces
kubectl get ns    # short version
```

- Lists all namespaces in cluster  

### 2.9 Run Local Image in Kubernetes Pod

```bash
kubectl run taskmanagementapp2 -n taskmanagementapp --image=task-management:latest --restart=Never --image-pull-policy=IfNotPresent
```

- Uses **local Docker image**  
- `--image-pull-policy=IfNotPresent` → tells K8s to **use local image**  
- Fixes **ImagePullBackOff** for local images  

### 2.10 Common Issues

#### ImagePullBackOff

- **Cause:** Kubernetes cannot pull the image  
- **Reasons:**
  1. Image exists only locally, not in registry  
  2. Wrong image name or tag  
  3. Private registry without credentials  
  4. Network issues  

- **Fixes:**
  - Use `--image-pull-policy=IfNotPresent` for local images  
  - Push image to Docker Hub and pull in Kubernetes  

### 2.11 Namespace vs Pod Confusion

- **Namespace = folder**  
- **Pod = file inside folder**  
- Commands must always refer to the correct namespace:  

```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -n <namespace>
```

- Using wrong namespace → shows “No resources found”  

### 2.12 Memory Tricks

| Concept           | Memory Tip                                      |
|------------------|------------------------------------------------|
| Namespace         | Folder                                         |
| Pod               | File inside folder                              |
| Image             | Recipe / frozen snapshot                        |
| Container         | Cooked dish / running instance                  |
| ImagePullBackOff  | “I want the image, but can’t fetch it”         |
| Volume Mount      | Live connection to your code                    |

---

This README is **based on my hands-on session** covering:  

- Docker images, containers, live mounts  
- Kubernetes Pods, namespaces, commands  
- Debugging `ImagePullBackOff`  
- Difference between `get pods`, `describe pod`, and `get events`

