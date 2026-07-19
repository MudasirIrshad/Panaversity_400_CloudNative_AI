# Docker Networking

## What is Docker Networking?

Docker Networking enables isolated containers to communicate with each other, the host machine, and external networks.

---

# Types of Docker Networks

## 1. Bridge Network (Default)

- Default network created by Docker.
- Connects containers running on the same Docker host.
- Communication is usually done using container IP addresses.

**Example**
```
Container A  <------>  Container B
```

---

## 2. User-Defined Bridge Network ⭐ (Most Common)

- Custom bridge network created by the user.
- Allows containers to communicate using **container names (DNS)**.
- More secure and flexible than the default bridge.

**Example**
```
Backend  <------>  MySQL

MYSQL_HOST=mysql
```

Create one:

```bash
docker network create two-tier-network
```

---

## 3. Host Network

- Container shares the host machine's network.
- No separate container IP.

**Example**
```
Container ---> Host Network
```

---

## 4. None Network

- Completely disables networking for the container.

**Example**
```
Container
❌ No Internet
❌ No Container Communication
```

---

## 5. Overlay Network

- Connects containers running on multiple Docker hosts.
- Mainly used with Docker Swarm.

---

## 6. Macvlan Network

- Gives each container its own MAC address and IP.
- Container appears as a physical device on the network.

---

# Note

Nowadays, Docker **Bridge** and **User-Defined Bridge** networks are the most commonly used.

Docker **Overlay** networking is mainly associated with Docker Swarm, while modern Kubernetes clusters use **CNI plugins (Calico, Flannel, Cilium, etc.)** instead.

Macvlan is still useful for specialized networking scenarios.

---

# Networking Commands

## List Networks

```bash
docker network ls
```

Lists all Docker networks.

---

## Create a Network

```bash
docker network create two-tier-network
```

Creates a user-defined bridge network.

---

## Remove a Network

```bash
docker network rm <network-name>
```

Deletes a Docker network.

---

## Inspect a Network

```bash
docker network inspect two-tier-network
```

Displays detailed network information, connected containers, subnet, gateway, and assigned IP addresses.

---

# Two-Tier Application Example

## List Images

```bash
docker images
```

Shows all locally available Docker images.

---

## Run MySQL Container

```bash
docker run -d \
--name mysql \
--network two-tier-network \
-e MYSQL_ROOT_PASSWORD=root \
-e MYSQL_DATABASE=devops \
mysql:8.0
```

Starts a MySQL container attached to the custom network.

---

## Run Backend Container

```bash
docker run -d \
-p 5000:5000 \
--network two-tier-network \
-e MYSQL_HOST=mysql \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD=root \
-e MYSQL_DB=devops \
twotier_backend:latest
```

Starts the backend container and connects it to MySQL using the container name (`mysql`).

---

## List Running Containers

```bash
docker ps
```

Shows all running containers.

---

## View Container Logs

```bash
docker logs <container-id>
```

Displays application logs.

---

## Open a Running Container

```bash
docker exec -it mysql bash
```

Opens an interactive shell inside the MySQL container.

---

## Connect to MySQL

```bash
mysql -u root -p
```

Opens the MySQL client.

---

## Database Commands

```sql
show databases;
```

Lists all databases.

```sql
use devops;
```

Selects the database.

```sql
show tables;
```

Lists all tables.

```sql
select * from messages;
```

Displays all records from the `messages` table.

---

# Key Takeaways

- Containers communicate by connecting to the same Docker network.
- User-defined bridge networks provide automatic DNS resolution using container names.
- `docker network inspect` helps verify network connectivity.
- Applications should connect using container names (e.g., `mysql`) instead of IP addresses.
