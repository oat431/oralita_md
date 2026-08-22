# MongoDB

> Document database. For apps that need flexible schema.
> Last updated: 2026-07-20

---

## Setup

**Compose:** `/home/flowero/database/mongodb/compose.yml`

| Item | Value |
|------|-------|
| Image | `mongo:8` |
| Container | `local-mongodb` |
| Port | `127.0.0.1:27017` |
| Network | `db-network` |
| Volume | `mongodb_data` |

## Access

**From server (Docker container):**
```
mongodb://admin:***@local-mongodb:27017/dbname
```

**From PC (MongoDB Compass):**
SSH tunnel: `100.73.143.25:22` → `localhost:27017`

## Common Commands

```bash
# Connect
docker exec -it local-mongodb mongosh -u admin -p ***

# Backup
docker exec local-mongodb mongodump --archive > mongodb.archive

# Restore
cat mongodb.archive | docker exec -i local-mongodb mongorestore --archive
```
