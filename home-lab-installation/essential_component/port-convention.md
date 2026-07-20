# Port Convention

> Port allocation for homelab services.
> Last updated: 2026-07-20

---

## Port Ranges

| Range | Purpose |
|-------|---------|
| 7000–8000 | Self-hosted apps (AdGuard, Portainer) |
| 8000–9000 | Personal projects (Gateway, Keycloak, Discovery) |
| Default ports | Databases (Postgres 5432, Valkey 6379, MongoDB 27017) |
| 8333, 8888, 9333 | SeaweedFS (S3, Filer, Master) |

## Current Allocation

### Self-hosted Apps (7000–8000)

| Service | Subdomain | Port |
|---------|-----------|------|
| AdGuard Home | `adguard` | 7000 |
| Portainer | `container` | 7001 |

### Personal Projects (8000–9000)

| Service | Subdomain | Port |
|---------|-----------|------|
| API Gateway | `api` / `gateway` | 8000 |
| Keycloak | `auth` | 8001 |
| Service Discovery | `discovery` | 8999 |

### Databases (default ports)

| DB | Subdomain | Port |
|----|-----------|------|
| PostgreSQL | — | 5432 |
| Valkey | — | 6379 |
| MongoDB | — | 27017 |
| SeaweedFS S3 | `s3` | 8333 |
| SeaweedFS Filer | — | 8888 |
| SeaweedFS Master | — | 9333 |

### Infrastructure

| Service | Port | Notes |
|---------|------|-------|
| SSH | 22 | Key auth only |
| Nginx | 80 | HTTP (Cloudflare handles TLS) |
| DNS (AdGuard) | 53 | Open for LAN |

## Adding a New Service

1. Pick an available port in the correct range
2. Bind to `127.0.0.1:PORT` in compose
3. Add Nginx config (see [[08.1-Add-Subdomain]])
4. If Tailscale-only: `sudo ufw allow from 100.73.0.0/16 to any port PORT`
