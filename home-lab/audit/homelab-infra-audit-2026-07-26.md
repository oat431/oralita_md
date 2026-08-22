# Homelab Infrastructure Audit — `flowero@192.168.1.121`

> **Date:** 2026-07-26 (UTC+7)
> **Checklist:** [[Homelab-Infra-Checklist]]
> **Status:** Infrastructure + databases + platform + monitoring + apps deployed

---

## System Overview

| Item | Value |
|------|-------|
| **OS** | Ubuntu 26.04 LTS (resolute) |
| **Kernel** | 7.0.0-28-generic |
| **Hardware** | Intel i7-7700HQ (4C/8T), 34GB RAM, 98GB NVMe |
| **Disk** | 31GB used / 63GB available (33%) |
| **RAM** | 5.9GB used / 28GB available |
| **Uptime** | 7 days, 2 hours |
| **LAN IP** | 192.168.1.121 (DHCP) |
| **Tailscale IP** | 100.73.143.25 |
| **Hostname** | flowero |

---

## 1. Hardware & Base Platform

| Item | Status | Notes |
|------|--------|-------|
| Hardware | ✅ | i7-7700HQ, 34GB RAM |
| Storage | ✅ | 98GB NVMe, 33% used |
| UPS | ❌ | No UPS protection |
| Base OS | ✅ | Ubuntu 26.04 LTS, headless |
| Docker | ✅ | 29.6.2 + Compose v5.3.1 |

---

## 2. Networking

| Item | Status | Notes |
|------|--------|-------|
| Static IP | ⚠️ | DHCP on LAN. Tailscale IP stable |
| Local DNS | ✅ | AdGuard Home, router DNS set |
| Reverse proxy | ✅ | Nginx — 16 sites enabled |
| TLS/SSL | ✅ | Cloudflare edge |
| Firewall | ✅ | UFW active — default deny |
| Tailscale | ✅ | Server + Windows PC (direct connection) |
| Cloudflare Tunnel | ✅ | `homelab` active, 4 connections |

---

## 3. Remote Access & Exposure

| Item | Status | Notes |
|------|--------|-------|
| Cloudflare Tunnel | ✅ | `*.panomete.com` routed |
| Tailscale | ✅ | Mesh VPN active, direct peer connection |
| SSH hardened | ✅ | Password disabled, root blocked, AllowUsers flowero |
| fail2ban | ✅ | **4245 failed, 705 banned** since install |
| No public IP | ✅ | Zero attack surface |

---

## 4. Container Management

| Item | Status | Notes |
|------|--------|-------|
| Docker + Compose | ✅ | 29.6.2 + 5.3.1 |
| Containers | ✅ | **23 running** |
| Portainer | ✅ | `container.panomete.com` |
| Network isolation | ✅ | `db-network` for databases |

---

## 5. Storage & Backups

| Item | Status | Notes |
|------|--------|-------|
| rclone | ✅ | v1.74.4, OneDrive configured |
| Backup automation | ❌ | No cron job yet |
| Database backups | ❌ | No scripts yet |

---

## 6. Monitoring & Observability

| Item | Status | Notes |
|------|--------|-------|
| Grafana | ✅ | `grafana.panomete.com`, healthy |
| Prometheus | ✅ | Metrics collection, healthy |
| Loki | ✅ | Log aggregation, healthy |
| Promtail | ✅ | Log shipper |
| Uptime Kuma | ✅ | `status.panomete.com`, **healthy** (fixed) |

---

## 7. Security

| Item | Status | Notes |
|------|--------|-------|
| Auto security updates | ✅ | `unattended-upgrades` active |
| SSH key-only | ✅ | Password disabled |
| fail2ban | ✅ | 705 IPs banned |
| Firewall | ✅ | UFW default deny |
| Secret management | ✅ | Infisical deployed |
| One-time secrets | ✅ | OTS deployed |

---

## 8. Services Running

### Infrastructure (4 containers + systemd)

| Service | Container | Status | Health |
|---------|-----------|--------|--------|
| AdGuard Home | `adguard` | ✅ Up 7 days | — |
| Portainer | `portainer` | ✅ Up 6 days | — |
| Cloudflared | (systemd) | ✅ Active | — |
| Nginx | (systemd) | ✅ Active | — |

### Platform Services (3 containers)

| Service | Container | Status | Health | Access |
|---------|-----------|--------|--------|--------|
| Flowero Gate | `flowero-gate` | ✅ Up 47h | healthy | `api.panomete.com` |
| Flowero Discover | `flowero-discover` | ✅ Up 47h | healthy | `discovery.panomete.com` |
| Flowero Guard (Keycloak) | `flowero-guard` | ✅ Up 47h | healthy | `auth.panomete.com` |

### Monitoring Stack (5 containers)

| Service | Container | Status | Health | Access |
|---------|-----------|--------|--------|--------|
| Grafana | `grafana` | ✅ Up 2 days | healthy | `grafana.panomete.com` |
| Prometheus | `prometheus` | ✅ Up 47h | healthy | — |
| Loki | `loki` | ✅ Up 2 days | healthy | — |
| Promtail | `promtail` | ✅ Up 2 days | — | — |
| Uptime Kuma | `uptime-kuma` | ✅ Up 6m | **healthy** ✅ | `status.panomete.com` |

### Self-hosted Apps (6 containers)

| Service | Container | Status | Access |
|---------|-----------|--------|--------|
| Infisical | `infisical-backend` | ✅ Up 25m | `secret.panomete.com` |
| OTS | `ots-app-1` | ✅ Up 25m | `ots.panomete.com` |
| ByteStash | `bytestash-bytestash-1` | ✅ Up 22m | `snippet.panomete.com` |
| SearXNG | `searxng-core` | ✅ Up 43m | `search.panomete.com` |
| Stirling PDF | `stirling-pdf` | ✅ Up 1h | `pdf-tools.panomete.com` |
| Homarr | `homarr` | ✅ Up 2h | `overview.panomete.com` |

### Databases (7 containers)

| Service | Container | Status | Health | Port |
|---------|-----------|--------|--------|------|
| PostgreSQL 18 | `local-postgres` | ✅ Up 6 days | healthy | 127.0.0.1:5432 |
| Valkey 9 | `local-valkey` | ✅ Up 6 days | healthy | 127.0.0.1:6379 |
| MongoDB 8 | `local-mongodb` | ✅ Up 6 days | healthy | 127.0.0.1:27017 |
| SeaweedFS Master | `seaweedfs-master` | ✅ Up 6 days | — | 0.0.0.0:9333 |
| SeaweedFS Volume | `seaweedfs-volume` | ✅ Up 6 days | — | internal |
| SeaweedFS Filer | `seaweedfs-filer` | ✅ Up 6 days | — | 0.0.0.0:8888 |
| SeaweedFS S3 | `seaweedfs-s3` | ✅ Up 6 days | — | 127.0.0.1:8333 |

### Nginx Sites (16 enabled)

| Site | Target |
|------|--------|
| `00-catch-all` | return 444 |
| `panomete.com` | Static profile site |
| `api.panomete.com` | Flowero Gate |
| `auth.panomete.com` | Keycloak |
| `discovery.panomete.com` | Flowero Discover |
| `grafana.panomete.com` | Grafana |
| `status.panomete.com` | Uptime Kuma |
| `overview.panomete.com` | Homarr |
| `secret.panomete.com` | Infisical |
| `ots.panomete.com` | OTS |
| `snippet.panomete.com` | ByteStash |
| `search.panomete.com` | SearXNG |
| `pdf-tools.panomete.com` | Stirling PDF |
| `adguard.panomete.com` | AdGuard |
| `container.panomete.com` | Portainer |
| `s3.panomete.com` | SeaweedFS S3 |

---

## 9. Maintenance & Operations

| Item | Status | Notes |
|------|--------|-------|
| Runbook | ✅ | Full docs in `home-lab-installation/` vault |
| Update schedule | ⚠️ | OS auto ✅, containers TBD |
| Disaster recovery | ⚠️ | Backup cron pending |

---

## Sanity Check

| Check | Status |
|-------|--------|
| SSH key-only auth | ✅ |
| Firewall default-deny | ✅ |
| fail2ban active | ✅ (705 banned) |
| Docker working | ✅ (23 containers) |
| Tailscale connected | ✅ |
| Cloudflare Tunnel running | ✅ |
| Nginx configured | ✅ (16 sites) |
| No public IP | ✅ |
| DNS (AdGuard) working | ✅ |
| Databases healthy | ✅ |
| Platform services healthy | ✅ |
| Monitoring healthy | ✅ |
| Uptime Kuma healthy | ✅ (fixed) |
| Secret management | ✅ (Infisical + OTS) |
| Backups | ⚠️ (configured, no cron) |

---

## Progress Timeline

| Item | Jul 19 | Jul 23 | Jul 24 | Jul 26 |
|------|--------|--------|--------|--------|
| Containers | 0 | 12 | 17 | **23** |
| Databases | 0 | 3 | 3 | **3** |
| Platform services | 0 | 3 | 3 | **3** |
| Monitoring | 0 | 0 | 5 | **5** |
| Self-hosted apps | 0 | 2 | 2 | **8** |
| Nginx sites | 0 | 8 | 10 | **16** |
| fail2ban bans | 0 | 697 | 705 | **705** |
| RAM used | 1.0GB | 3.0GB | 3.8GB | **5.9GB** |
| Disk used | 12GB | 19GB | 23GB | **31GB** |

---

## Summary

**23 containers running. All healthy. All monitored.**

**New since last audit:**
- ✅ Uptime Kuma fixed (now healthy)
- ✅ Infisical — secret management (`secret.panomete.com`)
- ✅ OTS — one-time secret sharing (`ots.panomete.com`)
- ✅ ByteStash — code snippets (`snippet.panomete.com`)
- ✅ SearXNG — private search (`search.panomete.com`)
- ✅ Stirling PDF — PDF tools (`pdf-tools.panomete.com`)
- ✅ Homarr — dashboard (`overview.panomete.com`)
- ✅ 6 new Nginx sites (8 → 16)

**Remaining:**
- ❌ Backup cron (rclone → OneDrive)
- ❌ Business services (6 apps from spec)
