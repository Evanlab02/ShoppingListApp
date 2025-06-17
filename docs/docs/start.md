# Getting Started

Welcome to the **ShoppingListApp**! 🎉 Let’s get started!

## Pre-requisites

Before you dive in, make sure you have the following installed on your machine:

- Docker
- Docker Compose

## Running using docker & docker compose

You can use the following compose file to get the shopping list app running via docker on your machine.

```yaml
name: shopping

services:
  pgadmin:
    container_name: shopping-pgadmin
    image: dpage/pgadmin4:9.4.0
    restart: unless-stopped
    env_file:
      - .env
    environment:
      SCRIPT_NAME: /pgadmin
    networks:
      - shopping-network
    volumes:
      - shopping-pgadmin-data:/var/lib/pgadmin
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

  db:
    container_name: shopping-db
    image: postgres:17.5-alpine3.22
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
    env_file:
      - .env
    networks:
      - shopping-network
    volumes:
      - shopping-db-data:/var/lib/postgresql/data
    healthcheck:
      test: [ "CMD", "pg_isready", "-U", "postgres" ]
      interval: 5s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1024M

  redis:
    image: redis:8.0.2-alpine3.21
    container_name: shopping-redis
    volumes:
      - shopping-redis-data:/data
    networks:
      - shopping-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1024M

  admin:
    container_name: shopping-admin
    image: ghcr.io/evanlab02/shopping-admin:latest
    env_file:
      - .env
    networks:
      - shopping-network
    depends_on:
      db:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1024M

  app:
    container_name: shopping-app
    image: ghcr.io/evanlab02/shopping-app:latest
    env_file:
      - .env
    environment:
      - GUNICORN_WORKERS=1
    networks:
      - shopping-network
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    develop:
      watch:
        - action: sync+restart
          path: ./backend/authentication
          target: /backend/authentication
        - action: sync+restart
          path: ./backend/stores
          target: /backend/stores
        - action: sync+restart
          path: ./backend/items
          target: /backend/items
        - action: sync+restart
          path: ./backend/shoppingapp
          target: /backend/shoppingapp
        - action: sync+restart
          path: ./backend/dashboard
          target: /backend/dashboard
        - action: rebuild
          path: ./backend/requirements.txt
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1024M

  web:
    container_name: shopping-web
    restart: unless-stopped
    image: ghcr.io/evanlab02/shopping-web:latest
    expose:
      - "80"
    ports:
      - "8001:80"
    networks:
      - shopping-network
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: sync+restart
          path: ./web/Caddyfile
          target: /etc/caddy/Caddyfile
        - action: sync+restart
          path: ./backend/static
          target: /var/www/html/static/
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

networks:
  shopping-network:
    driver: bridge

volumes:
  shopping-db-data:
    external: false
  shopping-pgadmin-data:
    external: false
  shopping-redis-data:
    external: false
```