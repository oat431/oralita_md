# PostgreSQL

> Relational database. Primary DB for most applications.
> Last updated: 2026-07-20

---

## Setup

**Compose:** `/home/flowero/database/postgres/compose.yml`

| Item | Value |
|------|-------|
| Image | `postgres:18` |
| Container | `local-postgres` |
| Port | `127.0.0.1:5432` |
| Network | `db-network` |
| Volume | `postgres_data` |

## Access

**From server (Docker container):**
```
postgres://postgres:***@local-postgres:5432/dbname
```

**From PC (DBeaver / pgAdmin):**
1. Host: `localhost`, Port: `5432`
2. SSH tab: Host `100.73.143.25`, User `flowero`, Key `id_rsa` or `id_homelab`

## Common Commands

```bash
# Connect
docker exec -it local-postgres psql -U postgres

# Backup
docker exec local-postgres pg_dumpall -U postgres > backup.sql

# Restore
cat backup.sql | docker exec -i local-postgres psql -U postgres
```
