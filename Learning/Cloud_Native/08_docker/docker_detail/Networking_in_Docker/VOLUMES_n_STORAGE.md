# Docker Volumes & Persistent Storage

## What are Docker Volumes?

Docker Volumes are **Docker-managed persistent storage** used to store container data outside the container's writable layer. Unlike container storage, volume data is **not deleted** when a container is removed.

---

## Why Use Docker Volumes?

- Persist data across container restarts and recreation.
- Store databases safely (MySQL, PostgreSQL, MongoDB, etc.).
- Share data between multiple containers.
- Improve data management by separating application code from data.

---

## Docker Storage Types

### 1. Named Volume (Recommended)
Managed entirely by Docker.

```bash
docker volume create mysql-data-vol
```

Mount it into a container:

```bash
docker run -d \
  --name mysql \
  -v mysql-data-vol:/var/lib/mysql \
  mysql:8.0
```

---

### 2. Bind Mount

Maps a host directory to a container.

```bash
docker run -v $(pwd):/app node
```

Useful during development because changes on the host are instantly reflected inside the container.

---

### 3. Anonymous Volume

Docker automatically creates a volume with a random name.

```bash
docker run -v /app/data nginx
```

---

# Docker Volume Lifecycle

Create a volume:

```bash
docker volume create mysql-data-vol
```

Inspect the volume:

```bash
docker volume inspect mysql-data-vol
```

Example output:

```json
{
  "Driver": "local",
  "Mountpoint": "/var/lib/docker/volumes/mysql-data-vol/_data",
  "Name": "mysql-data-vol"
}
```

The **Mountpoint** is the physical location where Docker stores the volume data on the host machine.

---

## Using a Volume with MySQL

Run MySQL with a persistent volume:

```bash
docker run -d \
  --name mysql \
  -v mysql-data-vol:/var/lib/mysql \
  --network two-tier-network \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=devops \
  mysql:8.0
```

Volume mapping:

```
Docker Volume
mysql-data-vol
        │
        ▼
/var/lib/docker/volumes/mysql-data-vol/_data
        │
        ▼
Container
/var/lib/mysql
```

Since MySQL stores all databases inside `/var/lib/mysql`, the database files are now stored in the Docker volume instead of the container.

---

# Data Persistence Demonstration

1. Create a Docker volume.
2. Start a MySQL container using that volume.
3. Create databases or tables.
4. Stop and remove the MySQL container.
5. Create a new MySQL container using the **same volume**.
6. All previously created databases remain available.

This demonstrates that Docker volumes preserve data independently of containers.

---

# Useful Docker Volume Commands

Create a volume:

```bash
docker volume create mysql-data-vol
```

List volumes:

```bash
docker volume ls
```

Inspect a volume:

```bash
docker volume inspect mysql-data-vol
```

Remove a volume:

```bash
docker volume rm mysql-data-vol
```

Remove unused volumes:

```bash
docker volume prune
```

Inspect mounted volumes of a container:

```bash
docker inspect mysql
```

---

# Container Management Commands

Stop a container:

```bash
docker stop mysql
```

Remove a stopped container:

```bash
docker rm mysql
```

Stop and remove in one command:

```bash
docker stop mysql && docker rm mysql
```

Or force remove:

```bash
docker rm -f mysql
```

> **Note:** Avoid using `&` between `docker stop` and `docker rm`. The `&` runs the stop command in the background, causing `docker rm` to execute before the container has fully stopped.

---

# Key Takeaways

- Docker volumes provide persistent storage independent of containers.
- Deleting a container **does not delete** its attached volumes.
- A new container can reuse the same volume and access previously stored data.
- Named volumes are the recommended storage option for databases and production workloads.
- Volumes are managed by Docker and stored under:

```text
/var/lib/docker/volumes/
```
