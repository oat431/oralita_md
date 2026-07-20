# Valkey

> In-memory cache. Redis-compatible drop-in replacement.
> Last updated: 2026-07-20

---

## Why Valkey over Redis?

Redis changed licensing in 2024 (no longer open source). Valkey is the open-source fork by Linux Foundation — same commands, same protocol, truly free.

## Setup

**Compose:** `/home/flowero/database/valkey/compose.yml`

| Item | Value |
|------|-------|
| Image | `valkey/valkey:9` |
| Container | `local-valkey` |
| Port | `127.0.0.1:6379` |
| Network | `db-network` |
| Volume | `valkey_data` |

## Access

**From server (Docker container):**
```
valkey://:***@local-valkey:6379
```

**From PC:** SSH tunnel + any Redis GUI (RedisInsight, Another Redis Desktop Manager)

## Common Commands

```bash
# Connect
docker exec -it local-valkey valkey-cli -a ***

# Test
docker exec local-valkey valkey-cli -a *** ping
# PONG
```

## Code

Valkey uses the same protocol as Redis — use any Redis client library:

```go
// Go
rdb := redis.NewClient(&redis.Options{
    Addr: "local-valkey:6379",
    Password: "***",
})
```
