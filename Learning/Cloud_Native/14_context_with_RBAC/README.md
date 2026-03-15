# Kubernetes Pod & Context Management

This guide briefly covers Kubernetes pod basics, management, and context switching, along with essential RBAC concepts.

## Pod Fundamentals

- **Pod:** Smallest K8s unit, holds 1+ containers.
- **Immutability:** Pod name and namespace are set at creation. Container names are also immutable within a pod spec.
- **Lifecycle:** Pending → Running → Succeeded/Failed. Pods are ephemeral.

## Pod YAML Structure (Key Fields)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod          # Immutable
  namespace: my-namespace  # Immutable
  labels: {}            # Editable
  annotations: {}       # Editable
spec:
  containers:
    - name: my-container     # Immutable
      image: my-app:v1       # Editable (container image can be updated)
      resources: {}          # Editable
      env: []                # Editable
  restartPolicy: Never   # Immutable
```

## Editable vs. Non-Editable Pod Fields

**Editable (while running):**
- `metadata.labels`, `metadata.annotations`
- `spec.containers[*].image` (container restarts)
- `spec.containers[*].resources`, `spec.containers[*].env` (container restarts)
- `spec.tolerations`

**Non-Editable (requires recreation):**
- `metadata.name`, `metadata.namespace`
- `spec.containers[*].name`
- `spec.volumes[*].name`
- `spec.restartPolicy`, `spec.nodeName`

## Pod Management Commands

**View Pods:**
- `kubectl get pods -n <namespace>`
- `kubectl describe pod <pod-name> -n <namespace>`

**Edit Pod (YAML):**
- `kubectl edit pod <pod-name> -n <namespace>`
  - Modifies editable fields directly. Saves & applies changes.

**Update Labels & Annotations:**
- `kubectl label pod <pod-name> <key>=<value> -n <namespace>`
- `kubectl annotate pod <pod-name> <key>=<value> -n <namespace>`

## Updating Pod Images

**Single Pod:**
- `kubectl set image pod/<pod-name> <container-name>=<new-image>:<tag> -n <namespace>`
  - Restarts the container with the new image.

**Deployment-Managed Pods (Recommended):**
- `kubectl set image deployment/<deployment-name> <container-name>=<new-image>:<tag> -n <namespace>`
  - Updates the Deployment, which then performs a rolling update of pods.

## Pod Recreation / "Renaming"

Since pod names are immutable, to "rename" or make structural changes (non-editable fields):

1. **Delete:** `kubectl delete pod <old-pod-name> -n <namespace>`
2. **Modify YAML:** Update `metadata.name` and any other desired fields in your YAML file.
3. **Recreate:** `kubectl apply -f <new-pod-definition.yaml>`

## Kubernetes Context & Namespaces

**Current Context:**
- `kubectl config current-context`

**Switch Context:**
- `kubectl config use-context <context-name>`

**Set Namespace for Current Context:**
- `kubectl config set-context --current --namespace=<namespace>`
  - Subsequent commands will default to this namespace.

## RBAC Basics (Role-Based Access Control)

- **Role:** Defines permissions within a specific **namespace**.
- **ClusterRole:** Defines permissions across the entire **cluster**.
- **RoleBinding:** Grants a **Role** to a user, group, or service account within a namespace.
- **ClusterRoleBinding:** Grants a **ClusterRole** to a user, group, or service account cluster-wide.

**RBAC Examples:**

**1. Create a Namespace-Scoped Role (e.g., `pod-reader` in `mudasir` namespace):**
- `kubectl create role pod-reader --verb=get,list,watch --resource=pods -n mudasir`

**2. Bind the Role to a User (e.g., `mudasir` user in `mudasir` namespace):**
- `kubectl create rolebinding read-pods-binding --role=pod-reader --user=mudasir -n mudasir`

**3. Create a Cluster-Wide Role (e.g., `cluster-pod-reader`):**
- `kubectl create clusterrole cluster-pod-reader --verb=get,list,watch --resource=pods`

**4. Bind the ClusterRole to a User (e.g., `mudasir` user cluster-wide):**
- `kubectl create clusterrolebinding cluster-read-pods-binding --clusterrole=cluster-pod-reader --user=mudasir`
---

This guide provides a concise overview. For production, always leverage **Deployments** for robust pod management and updates.