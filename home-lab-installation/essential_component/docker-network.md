# Docker Network

> Shared network for database and application containers.
> Last updated: 2026-07-20

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
