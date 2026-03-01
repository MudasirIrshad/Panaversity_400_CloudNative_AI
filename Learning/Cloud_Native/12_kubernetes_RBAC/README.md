# 📘 Kubernetes RBAC – Complete Hands-On Guide

## 📌 Objective

Learn how to:

* Create a `Role`
* Create a `ServiceAccount`
* Bind them using `RoleBinding`
* Attach ServiceAccount to a Pod
* Test permissions using `kubectl auth can-i`

---

# 🧠 RBAC Architecture

```
Role (WHAT is allowed)
        ↓
RoleBinding (CONNECT)
        ↓
ServiceAccount (WHO)
        ↓
Pod (USES identity)
```

---

# 1️⃣ Create Namespace

```bash
kubectl create namespace task-management
```

Verify:

```bash
kubectl get namespaces
```

---

# 2️⃣ Create Role

📄 **role.yaml**

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: task-management-deployer
  namespace: task-management
rules:
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["services", "pods"]
    verbs: ["get", "list"]
```

### Apply Role

```bash
kubectl apply -f role.yaml
```

Verify:

```bash
kubectl get roles -n task-management
```

---

# 3️⃣ Create ServiceAccount

📄 **serviceaccount.yaml**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: taskmanager
  namespace: task-management
```

### Apply ServiceAccount

```bash
kubectl apply -f serviceaccount.yaml
```

Verify:

```bash
kubectl get serviceaccounts -n task-management
```

---

# 4️⃣ Create RoleBinding

📄 **rolebinding.yaml**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: deployer-binding
  namespace: task-management
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: task-management-deployer
subjects:
- kind: ServiceAccount
  name: taskmanager
  namespace: task-management
```

### Apply RoleBinding

```bash
kubectl apply -f rolebinding.yaml
```

Verify:

```bash
kubectl get rolebindings -n task-management
```

---

# 5️⃣ Test Permissions

### Check if ServiceAccount can create deployments

```bash
kubectl auth can-i create deployments \
  -n task-management \
  --as=system:serviceaccount:task-management:taskmanager
```

Expected Output:

```
yes
```

---

# 6️⃣ Attach ServiceAccount to Pod

Delete existing pod (if needed):

```bash
kubectl delete pod task-management-pod -n task-management
```

Run new pod with ServiceAccount:

```bash
kubectl run task-management-pod \
  -n task-management \
  --image=nginx \
  --restart=Never \
  --serviceaccount=taskmanager
```

Verify:

```bash
kubectl describe pod task-management-pod -n task-management
```

Check:

```
Service Account: taskmanager
```

---

# 🔎 Important Commands Summary

### List all RBAC resources

```bash
kubectl get roles -n task-management
kubectl get rolebindings -n task-management
kubectl get serviceaccounts -n task-management
```

---

### Delete Resources

```bash
kubectl delete role task-management-deployer -n task-management
kubectl delete rolebinding deployer-binding -n task-management
kubectl delete serviceaccount taskmanager -n task-management
kubectl delete namespace task-management
```

---

# ⚠️ Important RBAC Rules

* Resource names must be **plural** (`deployments`, not `deployment`)
* Role is namespace-scoped
* ClusterRole is cluster-scoped
* Pods NEVER get permissions directly
* Pods inherit permissions from ServiceAccount
* Always follow **Least Privilege Principle**

---

# 🔥 Difference Summary

| Component          | Purpose                                         |
| ------------------ | ----------------------------------------------- |
| Role               | Defines permissions inside one namespace        |
| ClusterRole        | Defines permissions cluster-wide                |
| ServiceAccount     | Identity used by Pod                            |
| RoleBinding        | Connect Role to ServiceAccount (namespace only) |
| ClusterRoleBinding | Connect ClusterRole cluster-wide                |

---

# 🎯 Final Learning Outcome

After this session you should understand:

* How Kubernetes controls API access
* How to securely grant permissions
* How to debug permission issues
* How to test RBAC using `kubectl auth can-i`

---

# 🚀 GitHub Repository

📂 Folder: `12_kubernetes_RBAC`  
Includes:

* role.yaml
* serviceaccount.yaml
* rolebinding.yaml
* RBAC testing commands

---

# ✅ Production Mindset

Always remember:

```
Security first.
Grant minimum required permissions.
```