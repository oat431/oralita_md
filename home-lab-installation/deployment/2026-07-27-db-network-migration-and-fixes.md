# Deployment Log — 2026-07-27

## db-network Integration

Migrated 3 services from bundled databases to shared homelab `db-network`.

### SearXNG
- Removed bundled `searxng-valkey` container
- Joined `db-network`, using shared `local-valkey`
- Added `valkey.url` to `core-config/settings.yml` (use `valkey.url` not `redis.url` — deprecation warning)
- Port: `127.0.0.1:7004`

### Infisical
- Removed bundled `infisical-db` (PG14) and `infisical-dev-redis`
- Joined `db-network`, using shared `local-postgres` + `local-valkey`
- Created DB user `infisical` and database `infisical` on shared PostgreSQL
- Port changed: `8080` → `7005`

### OTS (One-Time Secret)
- Removed bundled `ots-valkey` container
- Joined `db-network`, using shared `local-valkey`
- Port changed: `3000` → `7006` (3000 taken by Grafana)

### ByteStash
- No DB integration (uses SQLite)
- Fixed placeholder volume path and JWT secret
- Port: `7008`

---

## Uptime Kuma Healthcheck Fix

Container was `unhealthy` because the Docker image's default healthcheck uses `wget`, which isn't installed in the Uptime Kuma image.

**Fix:** Changed healthcheck in `~/platform/docker-compose.observability.yml`:
```yaml
# Before (broken)
test: ["CMD", "wget", "-qO-", "http://localhost:3001"]

# After (working)
test: ["CMD-SHELL", "curl -sf http://localhost:3001 > /dev/null"]
```

Applied with `docker compose up -d uptime-kuma` (recreate).

---

## Port Summary

| App | Port | Network |
|-----|------|---------|
| SearXNG | 7004 | db-network |
| Infisical | 7005 | db-network |
| OTS | 7006 | db-network |
| ByteStash | 7008 | default |
| Uptime Kuma | 3001 | db-network |

See also: [[db-network-integration-guide]]
