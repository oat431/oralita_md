# Database Stack — Docker Compose Templates

## Shared Network

All databases use one external network. Create it first:
```bash
docker network create db-network
```

## PostgreSQL 18

```yaml
services:
  postgres:
    container_name: local-postgres
    image: postgres:18
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      PGDATA: /data/postgres
    volumes:
      - postgres_data:/data/postgres
    ports:
      - "127.0.0.1:5432:5432"
    restart: unless-stopped
    networks:
      - shared-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:

networks:
  shared-network:
    external: true
    name: db-network
```

## Valkey 9 (Redis replacement)

```yaml
services:
  valkey:
    container_name: local-valkey
    image: valkey/valkey:9
    command: valkey-server --requirepass ${VALKEY_PASSWORD:-valkey}
    volumes:
      - valkey_data:/data
    ports:
      - "127.0.0.1:6379:6379"
    restart: unless-stopped
    networks:
      - shared-network
    healthcheck:
      test: ["CMD", "valkey-cli", "-a", "${VALKEY_PASSWORD:-valkey}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  valkey_data:

networks:
  shared-network:
    external: true
    name: db-network
```

## MongoDB 8

```yaml
services:
  mongodb:
    container_name: local-mongodb
    image: mongo:8
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER:-admin}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:-admin}
    volumes:
      - mongodb_data:/data/db
    ports:
      - "127.0.0.1:27017:27017"
    restart: unless-stopped
    networks:
      - shared-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh --quiet
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mongodb_data:

networks:
  shared-network:
    external: true
    name: db-network
```

## SeaweedFS (S3-compatible object storage)

4 services: master (metadata), volume (data), filer (file system), s3 (S3 API).

⚠️ **v4.40+ breaking change:** S3 gateway flag changed from `-master=master:9333` to `-filer=filer:8888`. The S3 gateway connects to the filer, not the master directly.

```yaml
services:
  master:
    container_name: seaweedfs-master
    image: chrislusf/seaweedfs:latest
    command: master -ip.bind=0.0.0.0 -port=9333 -volumeSizeLimitMB=1024
    volumes:
      - master_data:/data
    ports:
      - "127.0.0.1:9333:9333"
    restart: unless-stopped
    networks:
      - shared-network

  volume:
    container_name: seaweedfs-volume
    image: chrislusf/seaweedfs:latest
    command: volume -port=8080 -mserver=master:9333 -dataCenter=dc1 -rack=rack1 -dir=/data -max=0
    volumes:
      - volume_data:/data
    depends_on:
      - master
    restart: unless-stopped
    networks:
      - shared-network

  filer:
    container_name: seaweedfs-filer
    image: chrislusf/seaweedfs:latest
    command: filer -master=master:9333 -port=8888
    ports:
      - "127.0.0.1:8888:8888"
    depends_on:
      - master
    restart: unless-stopped
    networks:
      - shared-network

  s3:
    container_name: seaweedfs-s3
    image: chrislusf/seaweedfs:latest
    command: s3 -port=8333 -filer=filer:8888 -config=/etc/seaweedfs/s3.json
    volumes:
      - ./s3.json:/etc/seaweedfs/s3.json:ro
    ports:
      - "127.0.0.1:8333:8333"
    depends_on:
      - filer
    restart: unless-stopped
    networks:
      - shared-network

volumes:
  master_data:
  volume_data:

networks:
  shared-network:
    external: true
    name: db-network
```

### SeaweedFS S3 config (s3.json)

```json
{
  "identities": [
    {
      "name": "admin",
      "credentials": [
        {
          "accessKey": "admin",
          "secretKey": "admin123"
        }
      ],
      "actions": ["Admin", "Read", "Write"]
    }
  ]
}
```

### SeaweedFS Endpoints

| Service | Port | URL |
|---------|------|-----|
| S3 API | 8333 | `http://localhost:8333` |
| Master UI | 9333 | `http://localhost:9333` |
| Filer UI | 8888 | `http://localhost:8888` |
| Volume | 8080 | (internal, no port mapping) |

## Connection Strings (from other containers on db-network)

```
postgresql://postgres:***@local-postgres:5432/dbname
mongodb://admin:***@local-mongodb:27017
valkey://local-valkey:6379
S3 endpoint: http://seaweedfs-s3:8333
```
