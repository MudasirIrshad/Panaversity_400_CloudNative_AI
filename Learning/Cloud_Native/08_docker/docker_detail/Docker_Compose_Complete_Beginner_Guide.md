# Docker Compose -- Complete Beginner's Guide

> This README is a beginner-friendly guide to Docker Compose.

## What is Docker Compose?

Docker Compose is a tool that lets you define and run **multi-container
Docker applications** using a single YAML file (`compose.yml` or
`docker-compose.yml`).

Instead of many `docker run` commands, you describe your application
once and start everything with:

``` bash
docker compose up
```

## Why use Docker Compose?

Without Compose you manually: - Build images - Create networks - Create
volumes - Start every container - Pass environment variables - Connect
containers

Compose automates all of this.

## Compose File Structure

``` yaml
services:
  app:
    ...

volumes:
  ...

networks:
  ...
```

## YAML Basics

-   Indentation uses **spaces only** (never tabs).
-   Child keys must be aligned.
-   Lists begin with `-`.

Example:

``` yaml
environment:
  MYSQL_DB: devops
ports:
  - "5000:5000"
```

## Services

A service describes one container.

``` yaml
services:
  mysql:
    image: mysql:8.0
```

## image vs build

`image:` downloads an image.

``` yaml
image: mysql:8.0
```

`build:` creates an image from a Dockerfile.

``` yaml
build:
  context: .
```

## Ports

``` yaml
ports:
  - "5000:5000"
```

Format:

    HOST:CONTAINER

## Environment Variables

``` yaml
environment:
  MYSQL_HOST: mysql
  MYSQL_USER: root
```

## Volumes

Persist data outside containers.

``` yaml
volumes:
  - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

## Networks

Allow containers to communicate.

``` yaml
networks:
  - backend

networks:
  backend:
```

Services on the same network communicate using service names.

## depends_on

``` yaml
depends_on:
  - mysql
```

Starts MySQL before the application.

> It **does not** guarantee MySQL is ready.

## Health Checks

Health checks allow Docker to determine whether a container is actually
healthy.

``` yaml
healthcheck:
  test: ["CMD","mysqladmin","ping","-h","localhost"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 30s
```

-   **test**: command to run
-   **interval**: how often
-   **timeout**: max wait
-   **retries**: failures allowed
-   **start_period**: grace period

Container states:

    starting
       ↓
    healthy
       ↓
    unhealthy

## Restart Policies

``` yaml
restart: always
```

Options:

-   no
-   always
-   unless-stopped
-   on-failure

## env_file

Instead of hardcoding:

``` yaml
env_file:
  - .env
```

Example `.env`

    MYSQL_USER=root
    MYSQL_PASSWORD=root

## command

Override the default command.

``` yaml
command: python app.py
```

## entrypoint

Override the image entrypoint.

``` yaml
entrypoint: ["python"]
```

## Logging

``` yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

## Resource Limits

``` yaml
deploy:
  resources:
    limits:
      cpus: "1"
      memory: 512M
```

(Primarily used with Docker Swarm.)

## Profiles

``` yaml
profiles:
  - dev
```

Run:

``` bash
docker compose --profile dev up
```

## Complete Example

``` yaml
services:
  mysql:
    image: mysql:8.0
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: devops
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
    healthcheck:
      test: ["CMD","mysqladmin","ping","-h","localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - backend

  flask:
    build:
      context: .
    ports:
      - "5000:5000"
    depends_on:
      - mysql
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: root
      MYSQL_DB: devops
    restart: unless-stopped
    networks:
      - backend

volumes:
  mysql-data:

networks:
  backend:
```

## Useful Commands

``` bash
docker compose up
docker compose up -d
docker compose down
docker compose down -v
docker compose ps
docker compose logs
docker compose logs -f
docker compose build
docker compose restart
docker compose exec mysql bash
docker compose config
```

## Best Practices

-   Use named volumes for databases.
-   Store secrets in `.env`.
-   Add health checks.
-   Prefer service names over IP addresses.
-   Remove the obsolete `version:` key.
-   Keep one responsibility per container.

## Common Mistakes

-   Wrong YAML indentation.
-   Using tabs.
-   Forgetting top-level `volumes:` or `networks:`.
-   Assuming `depends_on` waits for readiness.
-   Exposing unnecessary ports.

## Summary

Docker Compose lets you define your infrastructure as code. One file
describes your containers, networks, storage, configuration, and startup
process, making applications reproducible, portable, and easy to manage.
