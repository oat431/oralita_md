# Docker Network

> Shared network for database and application containers.
> Last updated: 2026-08-24

---

## Network: `db-network`

All databases and apps share one Docker bridge network.

```bash
docker network create db-network
```

## Usage in Compose Files

```yaml
services:
  myservice:
    networks:
      - shared-network

networks:
  shared-network:
    external: true
    name: db-network
```

## Container Name Resolution

Containers on the same network communicate by **container name**:

```go
// Connect to PostgreSQL
dsn := "postgres://postgres:***@local-postgres:5432/mydb"

// Connect to Valkey
addr := "local-valkey:6379"

// Connect to MongoDB
uri := "mongodb://admin:***@local-mongodb:27017/mydb"

// Connect to SeaweedFS S3
endpoint := "http://seaweedfs-s3:8333"
```

No port mapping needed between containers — Docker handles internal routing.

## ⚠️ External DNS Depends on the Host

Container-name resolution above always works — Docker's embedded DNS (`127.0.0.11`) handles that internally regardless of host state. **External** hostname lookups are different: Docker seeds each container's forwarder from the *host's* `/etc/resolv.conf` at container-create time. If that's broken (e.g. a dangling symlink after disabling `systemd-resolved` — see [[adguard]]), containers on `db-network` come up perfectly healthy but can't resolve any external host, and outbound HTTP calls fail silently with connection errors. This bit SearXNG exactly this way on 2026-08-24 — see [[2026-08-24-searxng-dns-outage-fix]].

Check any new `db-network` container with:
```bash
docker exec <container> cat /etc/resolv.conf
```
Real answer looks like `# ExtServers: [host(127.0.0.1) host(1.1.1.1)]`. `# NO EXTERNAL NAMESERVERS DEFINED` means the host's resolver is broken, not the container or the network.

## Current Containers on `db-network`

| Container | Service |
|-----------|---------|
| `local-postgres` | PostgreSQL 18 |
| `local-valkey` | Valkey 9 |
| `local-mongodb` | MongoDB 8 |
| `seaweedfs-master` | SeaweedFS Master |
| `seaweedfs-volume` | SeaweedFS Volume |
| `seaweedfs-filer` | SeaweedFS Filer |
| `seaweedfs-s3` | SeaweedFS S3 API |
