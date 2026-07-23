# Home Lab Server

> A personal server that can host many applications.
> Last updated: 2026-07-23

---

## Personal Project : 8000-9000 (BE) | 3000-4000 (FE)

| Service | Sub Domain | Code Name | Port BE | Port FE | Status |
|---------|-----------|-----------|---------|---------|--------|
| Gateway | api | Flowero Gate | 8000 | - | ✅ |
| Service Discovery | discovery | Flowero Discover | 8999 | 3999 | ✅ |
| Keycloak | auth | Flowero Guard | 8001 | 3001 | ✅ |
| Url Shortener | short | Fluffy Mouton | 8002 | 3002 | ❌ |
| Todo List | todo | Tiny Mchwa | 8003 | 3003 | ❌ |
| Ledger | ledger | Big Schwein | 8004 | 3004 | ❌ |
| Blog | blog | Cute Gufo | 8005 | 3005 | ❌ |
| Cook Book | recipe | Shy Ardilla | 8006 | 3006 | ❌ |
| Hora | hora | White Jelen | 8007 | 3007 | ❌ |

## Home Lab Self-hosted App : 7000-8000

| Name | Sub Domain | Port | Source | Status |
|------|-----------|------|--------|--------|
| AdGuard Home | adguard | 7000 | [adguard/adguardhome](https://hub.docker.com/r/adguard/adguardhome) | ✅ |
| Portainer | container | 7001 | [portainer/portainer-ce](https://hub.docker.com/r/portainer/portainer-ce) | ✅ |
| it-tools | it-tools | 7002 | [CorentinTh/it-tools](https://github.com/CorentinTh/it-tools) | ❌ |
| Homarr | overview | 7003 | [homarr.dev/docs](https://homarr.dev/docs/getting-started/installation/docker) | ❌ |
| SearXNG | search | 7004 | [searxng/searxng](https://github.com/searxng/searxng) | ❌ |
| Infisical | secret | 7005 | [Infisical/infisical](https://github.com/Infisical/infisical) | ❌ |
| OTS | ots | 7006 | [Luzifer/ots](https://github.com/Luzifer/ots) | ❌ |
| Stirling PDF | pdf-tools | 7007 | [stirlingpdf.com](https://docs.stirlingpdf.com/Installation/Docker%20Install) | ❌ |
| Byte Stash | snippet | 7008 | [jordan-dalby/ByteStash](https://github.com/jordan-dalby/ByteStash) | ❌ |

## Home Lab Database : Default Ports

| DB | Sub Domain | Port | Status |
|----|-----------|------|--------|
| PostgreSQL 18 | — | 5432 | ✅ |
| Valkey 9 | — | 6379 | ✅ |
| MongoDB 8 | — | 27017 | ✅ |
| SeaweedFS S3 | s3 | 8333 | ✅ |
| SeaweedFS Filer | — | 8888 | ✅ |
| SeaweedFS Master | — | 9333 | ✅ |

## Infrastructure

| Component | Status |
|-----------|--------|
| SSH (key auth only) | ✅ |
| UFW Firewall | ✅ |
| Fail2ban | ✅ |
| Docker + Compose | ✅ |
| Tailscale | ✅ |
| Cloudflare Tunnel | ✅ |
| Nginx Reverse Proxy | ✅ |
| Backups (rclone → OneDrive) | ✅ (configured, no cron yet) |
| Monitoring | ❌ |
