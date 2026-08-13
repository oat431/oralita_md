# Homelab db-network Integration Guide

> How to migrate Docker Compose services from internal/bundled databases
> to the shared homelab `db-network` infrastructure.

## Shared Infrastructure

| Service | Container | Network | Port (localhost) | Credentials |
|---------|-----------|---------|-------------------|-------------|
| PostgreSQL 18 | `local-postgres` | `db-network` | `5432` | user: `postgres` |
| Valkey 9 | `local-valkey` | `db-network` | `6379` | password: see `.env` |
| MongoDB 8 | `local-mongodb` | `db-network` | `27017` | — |

### DNS Aliases on `db-network`

When a container joins `db-network`, it can reach shared services by these hostnames:

| Hostname | Resolves To |
|----------|-------------|
| `postgres` / `local-postgres` | Shared PostgreSQL |
| `valkey` / `local-valkey` | Shared Valkey |
| `mongodb` / `local-mongodb` | Shared MongoDB |

---

## General Migration Pattern

### Step 1: Backup

```bash
cp docker-compose.yml docker-compose.yml.bak
cp .env .env.bak
```

### Step 2: Remove bundled database services

Delete the database service(s) and their volumes from `docker-compose.yml`.

**Before:**
```yaml
services:
  app:
    ...
  postgres:          # ← remove
    image: postgres:14
    volumes:
      - pg_data:/var/lib/postgresql/data
  redis:             # ← remove
    image: redis
    volumes:
      - redis_data:/data

volumes:
  pg_data:           # ← remove
  redis_data:        # ← remove
```

**After:**
```yaml
services:
  app:
    ...
```

### Step 3: Join `db-network`

Add the external network to the app service:

```yaml
services:
  app:
    ...
    networks:
      - db-network

networks:
  db-network:
    external: true
```

### Step 4: Update connection strings

Point to the shared services using their DNS aliases:

**PostgreSQL:**
```
# Before (bundled)
DATABASE_URL=postgres://user:pass@db:5432/mydb

# After (shared)
DATABASE_URL=postgres://user:pass@postgres:5432/mydb
```

**Valkey/Redis (with auth):**
```
# Before (bundled, no auth)
REDIS_URL=redis://redis:6379/0

# After (shared, with auth)
REDIS_URL=redis://:PASSWORD@valkey:6379/0
```

**MongoDB:**
```
# Before (bundled)
MONGO_URL=mongodb://mongo:27017/mydb

# After (shared)
MONGO_URL=mongodb://mongodb:27017/mydb
```

### Step 5: Create database/user (PostgreSQL only)

If the app needs its own database and user:

```bash
# Create user
docker exec local-postgres psql -U postgres -c "CREATE USER myapp WITH PASSWORD 'myapp';"

# Create database
docker exec local-postgres psql -U postgres -c "CREATE DATABASE myapp OWNER myapp;"

# Grant privileges
docker exec local-postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE myapp TO myapp;"
```

### Step 6: Remove `depends_on` for deleted services

If the compose had `depends_on: [db, redis]`, remove them since those
services no longer exist. The shared infra is always running.

### Step 7: Start and verify

```bash
cd ~/application/<app>
docker compose up -d

# Check container is on db-network
docker ps --filter "name=<app>" --format "table {{.Names}}\t{{.Networks}}"

# Check logs for connection errors
docker logs <container> 2>&1 | grep -i "error\|connect\|refused"

# Verify HTTP
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/
```

---

## Completed Migrations

### SearXNG (`~/application/searxng/`)

| Item | Before | After |
|------|--------|-------|
| Valkey | Bundled `searxng-valkey` | Shared `local-valkey` |
| Volume | `valkey-data` | Removed |
| Network | Default | `db-network` |
| Port | `7004` | `7004` (unchanged) |

**Config change:** Added `valkey.url` to `core-config/settings.yml`:
```yaml
valkey:
  url: redis://:PASSWORD@valkey:6379/0
```

**Note:** SearXNG deprecation warning if using `redis.url` — use `valkey.url` instead.

---

### Infisical (`~/application/infisical/`)

| Item | Before | After |
|------|--------|-------|
| PostgreSQL | Bundled `infisical-db` (PG14) | Shared `local-postgres` (PG18) |
| Redis | Bundled `infisical-dev-redis` | Shared `local-valkey` |
| Volumes | `pg_data`, `redis_data` | Removed |
| Network | `infisical` (custom) | `db-network` |
| Port | `80` → `8080` | `7005` → `8080` |

**DB setup:**
```bash
docker exec local-postgres psql -U postgres -c "CREATE USER infisical WITH PASSWORD 'infisical';"
docker exec local-postgres psql -U postgres -c "CREATE DATABASE infisical OWNER infisical;"
```

**Key `.env` changes:**
```
DB_CONNECTION_URI=postgres://infisical:infisical@postgres:5432/infisical
REDIS_URL=redis://:PASSWORD@valkey:6379
```

**Note:** Infisical runs Prisma migrations on startup — PG18 is compatible.

---

### OTS (`~/application/ots/`)

| Item | Before | After |
|------|--------|-------|
| Valkey | Bundled `ots-valkey` | Shared `local-valkey` |
| Volume | `./data` | Removed |
| Network | Default | `db-network` |
| Port | `3000` | `7006` |

**Config change:**
```yaml
REDIS_URL: redis://:PASSWORD@valkey:6379/0
```

---

### ByteStash (`~/application/bytestash/`)

**Cannot integrate.** Uses SQLite (`better-sqlite3`) — file-based, no network database. Stays as-is.

---

### Penpot (`~/application/penpot/`)

| Item | Before | After |
|------|--------|-------|
| PostgreSQL | Bundled `penpot-postgres` (PG15) | Shared `local-postgres` (PG18) |
| Valkey | Bundled `penpot-valkey` (8.1) | Shared `local-valkey` |
| Network | `penpot` (internal) | `db-network` |
| Frontend Port | `9001` | `7009` + `9001` (both) |
| Public URI | `http://localhost:9001` | `https://design.panomete.com` |

**DB setup:**
```bash
docker exec local-postgres psql -U postgres -c "CREATE USER penpot WITH PASSWORD 'penpot';"
docker exec local-postgres psql -U postgres -c "CREATE DATABASE penpot OWNER penpot;"
```

**Key env changes (backend):**
```
PENPOT_DATABASE_URI=postgresql://postgres/penpot
PENPOT_DATABASE_USERNAME=penpot
PENPOT_DATABASE_PASSWORD=penpot
PENPOT_REDIS_URI=redis://:PASSWORD@valkey/0
```

**Notes:**
- Backend, exporter both use shared Valkey for websockets/notifications
- Assets stored in `penpot_assets` volume (filesystem backend)
- mailcatch kept for dev SMTP
- Secret key regenerated (was `change-this-insecure-key`)

---

## Port Allocation Reference

| Port | Service |
|------|---------|
| 3000 | Grafana |
| 5432 | PostgreSQL |
| 6379 | Valkey |
| 7000 | AdGuard |
| 7004 | SearXNG |
| 7005 | Infisical |
| 7006 | OTS |
| 7008 | ByteStash |
| 7009 | Penpot |
| 9001 | Penpot (alt) |
| 9000 | Portainer |
| 9090 | Prometheus |
| 27017 | MongoDB |

---

## Rollback

Each migration keeps `.bak` files:

```bash
cd ~/application/<app>
cp docker-compose.yml.bak docker-compose.yml
cp .env.bak .env  # if exists
docker compose up -d
```
