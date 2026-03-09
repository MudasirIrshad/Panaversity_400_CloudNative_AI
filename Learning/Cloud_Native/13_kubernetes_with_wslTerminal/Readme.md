# Cloud Native AI Learning - Kubernetes & FastAPI Session

$ echo "Welcome to Cloud Native AI learning session. Let's go step by step."

---

$ echo "Step 1️⃣: Linux Variables and Command Output"

# Simple variable
$ NAME=Mudasir
$ echo $NAME
Mudasir

# Storing command output in a variable
$ FASTAPI_IP=$(kubectl get pod task-management-pod -n mudasir -o jsonpath="{.status.podIP}")
$ echo $FASTAPI_IP
10.244.0.15

> Note: `$(...)` executes the command and stores its output in the variable for later use.

---

$ echo "Step 2️⃣: Working in WSL"

# Enter your WSL environment
$ wsl
root@DESKTOP:/mnt/c/Users/DEll/Desktop/Cloud_Native$

# Access Windows services (like FastAPI running on Windows localhost)
$ curl http://host.docker.internal:8000/docs
# Output: raw HTML of FastAPI Swagger UI

> Important: Inside WSL, 'localhost' points to WSL itself, not Windows host. Use 'host.docker.internal' to reach Windows.

---

$ echo "Step 3️⃣: Kubernetes Pods Basics"

# Every pod has 3 parts: Metadata, Spec, Status

$ cat <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: example-pod
spec:
  containers:
  - name: app
    image: nginx
status:
  phase: Running
EOF

> Metadata = info about pod (name, labels)  
> Spec = desired state (containers, images, ports)  
> Status = current state (Running, Pending, Failed)

---

$ echo "Step 4️⃣: Test FastAPI Pod inside Kubernetes using BusyBox"

# Use BusyBox pod to test connectivity
$ kubectl run bb --image=busybox --restart=Never --rm -it -- bin/sh -c "wget -qO- $FASTAPI_IP:8000/hello"

# Output example:
{"message":"Hello World"}

---

$ echo "Step 5️⃣: Generate Pod YAML without creating it"

$ kubectl run image \
  --image=task-management:v1 \
  -n mudasir \
  --labels="app=mudasirkhan,stack=python" \
  --dry-run=client -o yaml

> Generates YAML for pod with labels, ready to apply or modify.

---

$ echo "Step 6️⃣: Searching Pods using Labels"

# Find pods by app label
$ kubectl get pods -n mudasir -l app=mudasirkhan

# Find pods by stack label
$ kubectl get pods -n mudasir -l stack=python

# Multiple labels
$ kubectl get pods -n mudasir -l app=mudasirkhan,stack=python -o wide

---

$ echo "Step 7️⃣: Port-Forwarding FastAPI Pod to localhost"

$ kubectl port-forward pod/task-management-pod -n mudasir 8000:8000
Forwarding from 127.0.0.1:8000 -> 8000
Forwarding from [::1]:8000 -> 8000
Handling connection for 8000

# Test endpoints
$ wget -O- http://localhost:8000/docs
$ curl http://localhost:8000/hello
{"message":"Hello World"}

---

$ echo "Step 8️⃣: Summary of Learning Flow"

# Story recap in order:
# 1. Linux variables & command output
# 2. WSL access to Windows localhost
# 3. Pod structure (Metadata, Spec, Status)
# 4. BusyBox pod for internal API testing
# 5. Generate YAML with dry-run
# 6. Label selectors for pods
# 7. Port-forward to localhost for API testing

---

$ echo "Step 9️⃣: Network Flow Diagram (ASCII)"

# Visualize FastAPI pod access from WSL/host

$ cat <<EOF
+-----------------+           +-------------------+         +-------------------------+
| Windows Host /  |           |      WSL Shell     |         |    Kubernetes Pod       |
| Browser / Tools |           | (Linux Terminal)  |         |  task-management-pod    |
+-----------------+           +-------------------+         +-------------------------+
        |                               |                                |
        |  localhost:8000 (browser)     |                                |
        |------------------------------>|                                |
        |                               |  host.docker.internal:8000     |
        |                               |------------------------------->|
        |                               |                                |
        |                               |         Pod IP: 10.244.0.15    |
        |                               |<-------------------------------|
        |                               |                                |
        |  curl / wget request          |                                |
        |-------------------------------------------------------------->|
        |                               |                                |
        |<------------------------------|                                |
        |  API Response JSON / HTML      |                                |
EOF

> This diagram shows the flow: host → WSL → Pod IP → FastAPI → back.

---

$ echo "✅ End of session. You now know Linux variables, WSL access, pod IP, BusyBox testing, port-forwarding, and label selectors in Kubernetes."