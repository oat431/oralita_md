# Backup Automation

> Automated backup scripts for the Panomete Platform homelab.
> Last updated: 2026-07-24

---

## Deployment Status

> **Deployed:** 2026-07-24 | **Verified:** Working
>
> - Database backup: ✅ Tested (64K dump → OneDrive)
> - Volume backup: ✅ Tested (11M + 4K + 52K → OneDrive)
> - Cron installed: ✅ Daily 3AM DB, Weekly Sunday 4AM volumes
> - rclone OneDrive: ✅ Connected and syncing

---

## What & Why

Two automated backup scripts protect platform data:

- **`backup-db.sh`** — Dumps all PostgreSQL databases daily, retains 7 days locally, syncs to OneDrive
- **`backup-volumes.sh`** — Backs up Docker volumes weekly, retains 4 weeks locally, syncs to OneDrive

Both scripts run via cron on the homelab server.

---

## Scripts

### Database Backup (`backup-db.sh`)

| Item | Value |
|------|-------|
| Path | `/home/flowero/scripts/backup-db.sh` |
| Schedule | Daily at 3:00 AM |
| Method | `pg_dumpall` → gzip → rclone → OneDrive |
| Retention | 7 days local, unlimited on OneDrive |
| Log | `/home/flowero/backups/backup.log` |

**What it backs up:** All PostgreSQL databases (keycloak, eureka, etc.)

### Volume Backup (`backup-volumes.sh`)

| Item | Value |
|------|-------|
| Path | `/home/flowero/scripts/backup-volumes.sh` |
| Schedule | Weekly (Sunday 4:00 AM) |
| Method | Docker volume → tar → gzip → rclone → OneDrive |
| Retention | 4 weeks local, unlimited on OneDrive |
| Log | `/home/flowero/backups/backup.log` |

**Volumes backed up:**

| Volume | Service | Size |
|--------|---------|------|
| `postgres_postgres_data` | PostgreSQL | ~11 MB |
| `valkey_valkey_data` | Valkey | ~4 KB |
| `portainer_data` | Portainer | ~52 KB |

---

## Cron Jobs

```bash
# View cron jobs
crontab -l

# Expected output:
# # Panomete Platform Backups
# 0 3 * * * /home/flowero/scripts/backup-db.sh
# 0 4 * * 0 /home/flowero/scripts/backup-volumes.sh
```

---

## Common Commands

```bash
# View backup log
cat /home/flowero/backups/backup.log

# List local database backups
ls -la /home/flowero/backups/postgres/

# List local volume backups
ls -la /home/flowero/backups/volumes/

# List OneDrive database backups
rclone lsd onedrive:panomete-backups/postgres/

# List OneDrive volume backups
rclone lsd onedrive:panomete-backups/volumes/

# Manual database backup
/home/flowero/scripts/backup-db.sh

# Manual volume backup
/home/flowero/scripts/backup-volumes.sh
```

---

## Restore Procedures

### Restore Database

```bash
# 1. Find the backup file
ls /home/flowero/backups/postgres/pg_dumpall_*.sql.gz

# 2. Stop services that use the database
docker stop flowero-guard

# 3. Restore
gunzip -c /home/flowero/backups/postgres/pg_dumpall_YYYY-MM-DD_HHMMSS.sql.gz | \
  docker exec -i local-postgres psql -U postgres

# 4. Restart services
docker start flowero-guard
```

### Restore Volume

```bash
# 1. Find the backup file
ls /home/flowero/backups/volumes/volume_name_*.tar.gz

# 2. Stop the service
docker stop flowero-guard

# 3. Restore volume
docker run --rm \
  -v volume_name:/target \
  -v /home/flowero/backups/volumes:/backup \
  alpine:latest \
  sh -c "cd /target && tar xzf /backup/volume_name_YYYY-MM-DD_HHMMSS.tar.gz"

# 4. Restart service
docker start flowero-guard
```

---

## Troubleshooting

### Backup script fails — rclone not connected

**Error:** `CRITICAL: couldn't fetch token: invalid_grant`

**Fix:**
```bash
# On your PC
rclone authorize "onedrive"
# Copy the token JSON

# On the server
rclone config reconnect onedrive:
# Paste the token
```

### Backup script fails — pg_dumpall error

**Error:** `pg_dumpall: error: connection to server failed`

**Fix:**
```bash
# Check PostgreSQL container
docker ps | grep local-postgres

# If not running
docker start local-postgres

# Test connection
docker exec local-postgres psql -U postgres -c "SELECT 1;"
```

### Backup script fails — volume not found

**Error:** `Volume xxx does not exist, skipping`

**Fix:** Check the actual volume name:
```bash
docker volume ls
```

Update the `VOLUMES` array in `backup-volumes.sh` with the correct names.

---

## OneDrive Folder Structure

```
onedrive:panomete-backups/
├── postgres/
│   ├── pg_dumpall_2026-07-24_030001.sql.gz
│   ├── pg_dumpall_2026-07-23_030001.sql.gz
│   └── ...
└── volumes/
    ├── postgres_postgres_data_2026-07-21_040001.tar.gz
    ├── valkey_valkey_data_2026-07-21_040001.tar.gz
    └── portainer_data_2026-07-21_040001.tar.gz
```

---

## Related

- [[github-actions-tailscale]] — CI/CD deployment pipeline
- [[../microservice_component/keycloak]] — Keycloak realm backup (version-controlled in git)
- [[../microservice_component/discovery]] — Discover uses no persistent data
- [[../microservice_component/gateway]] — Gateway uses no persistent data
