# Homelab Infrastructure Audit — `flowero@192.168.1.121`

> **Date:** 2026-07-20 (end of day)
> **Checklist:** [[Homelab-Infra-Checklist]]
> **Status:** Infrastructure + databases + platform services deployed

---

## System Overview

| Item | Value |
|------|-------|
| **OS** | Ubuntu 26.04 LTS (resolute) |
| **Kernel** | 7.0.0-28-generic |
| **Hardware** | Intel i7-7700HQ (4C/8T), 34GB RAM, 98GB NVMe |
| **Disk** | 19GB used / 75GB available (20%) |
| **RAM** | 3.0GB used / 31GB available |
| **Uptime** | 4 days, 2 hours |
| **LAN IP** | 192.168.1.121 (DHCP) |
| **Tailscale IP** | 100.73.143.25 |
| **Hostname** | flowero |

---

## 1. Hardware & Base Platform

| Item | Status | Notes |
|------|--------|-------|
| Hardware | ✅ | i7-7700HQ, 34GB RAM |
| Storage | ✅ | 98GB NVMe, 20% used |
| UPS | ❌ | No UPS protection |
| Base OS | ✅ | Ubuntu 26.04 LTS, headless |
| Docker | ✅ | 29.6.2 + Compose v5.3.1 |
| Resource monitoring | ❌ | Not set up |

---

## 2. Networking

| Item | Status | Notes |
|------|--------|-------|
| Static IP | ⚠️ | DHCP on LAN. Tailscale IP stable |
| Local DNS | ✅ | AdGuard Home, router DNS set |
| Reverse proxy | ✅ | Nginx — 8 sites enabled |
| TLS/SSL | ✅ | Cloudflare edge |
| Firewall | ✅ | UFW active — default deny |
| Port forwarding | ✅ | None — no public IP |
| Tailscale | ✅ | Server + Windows PC |
| Cloudflare Tunnel | ✅ | `homelab` active, 3 connections |

---

## 3. Remote Access & Exposure

| Item | Status | Notes |
|------|--------|-------|
| Cloudflare Tunnel | ✅ | `*.panomete.com` routed |
| Tailscale | ✅ | Mesh VPN active |
| SSH hardened | ✅ | Password disabled, root blocked, AllowUsers flowero |
| fail2ban | ✅ | **4159 failed, 697 banned** since install |
| No public IP | ✅ | Zero attack surface |

---

## 4. Container Management

| Item | Status | Notes |
|------|--------|-------|
| Docker + Compose | ✅ | 29.6.2 + 5.3.1 |
| Containers | ✅ | **12 running** |
| Portainer | ✅ | `container.panomete.com` |
| Network isolation | ✅ | `db-network` for databases |

---

## 5. Storage & Backups

| Item | Status | Notes |
|------|--------|-------|
| rclone | ✅ | v1.74.4, OneDrive configured |
| Backup automation | ❌ | No cron job yet |
| Database backups | ❌ | No scripts yet |
| Config backup | ❌ | Not in git |

---

## 6. Monitoring & Observability

| Item | Status | Notes |
|------|--------|-------|
| System metrics | ❌ | Not set up |
| Uptime monitoring | ❌ | Not set up |
| Alerting | ❌ | Not set up |
| Health checks | ✅ | Flowero Gate, Flowero Discover, PostgreSQL, Valkey, MongoDB |

---

## 7. Security

| Item | Status | Notes |
|------|--------|-------|
| Auto security updates | ✅ | `unattended-upgrades` active |
| SSH key-only | ✅ | Password disabled |
| fail2ban | ✅ | 697 IPs banned |
| Firewall | ✅ | UFW default deny |
| No public exposure | ✅ | Via Cloudflare Tunnel |
| Public vs Private | ✅ | Admin panels Tailscale-only |

---

## 8. Services Running

### Infrastructure (4 containers)

| Service | Container | Status | Health |
|---------|-----------|--------|--------|
| AdGuard Home | `adguard` | ✅ Up 4 days | — |
| Portainer | `portainer` | ✅ Up 3 days | — |
| Cloudflared | (systemd) | ✅ Active | — |
| Nginx | (systemd) | ✅ Active | — |

### Platform Services (3 containers)

| Service | Container | Status | Health | Port | Access |
|---------|-----------|--------|--------|------|--------|
| Flowero Gate | `flowero-gate` | ✅ Up 44m | healthy | 8000 | `api.panomete.com` |
| Flowero Discover | `flowero-discover` | ✅ Up 2h | healthy | 8999 | `discovery.panomete.com` |
| Flowero Guard (Keycloak) | `flowero-guard` | ✅ Up 3h | — | 8001 | `auth.panomete.com` |

### Databases (7 containers)

| Service | Container | Status | Health | Port |
|---------|-----------|--------|--------|------|
| PostgreSQL 18 | `local-postgres` | ✅ Up 3 days | healthy | 127.0.0.1:5432 |
| Valkey 9 | `local-valkey` | ✅ Up 3 days | healthy | 127.0.0.1:6379 |
| MongoDB 8 | `local-mongodb` | ✅ Up 3 days | healthy | 127.0.0.1:27017 |
| SeaweedFS Master | `seaweedfs-master` | ✅ Up 3 days | — | 0.0.0.0:9333 |
| SeaweedFS Volume | `seaweedfs-volume` | ✅ Up 3 days | — | internal |
| SeaweedFS Filer | `seaweedfs-filer` | ✅ Up 3 days | — | 0.0.0.0:8888 |
| SeaweedFS S3 | `seaweedfs-s3` | ✅ Up 3 days | — | 127.0.0.1:8333 |

### Nginx Sites (8 enabled)

| Site | Target |
|------|--------|
| `00-catch-all` | return 444 |
| `panomete.com` | Static profile site |
| `api.panomete.com` | Flowero Gate (8000) |
| `auth.panomete.com` | Keycloak (8001) |
| `discovery.panomete.com` | Flowero Discover (8999) |
| `adguard.panomete.com` | AdGuard (7000) |
| `container.panomete.com` | Portainer (7001) |
| `s3.panomete.com` | SeaweedFS S3 (8333) |

### Compose Files

| Path | Service |
|------|---------|
| `/home/flowero/platform/flowerogate/docker-compose.yml` | Flowero Gate |
| `/home/flowero/platform/keycloak/compose.yml` | Keycloak |
| `/home/flowero/database/postgres/compose.yml` | PostgreSQL |
| `/home/flowero/database/valkey/compose.yml` | Valkey |
| `/home/flowero/database/mongodb/compose.yml` | MongoDB |
| `/home/flowero/database/seaweedfs/compose.yml` | SeaweedFS |
| `/home/flowero/application/portainer/compose.yml` | Portainer |
| `/home/flowero/dns/compose.yml` | AdGuard |

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
| fail2ban active | ✅ (697 banned) |
| Docker working | ✅ (12 containers) |
| Tailscale connected | ✅ |
| Cloudflare Tunnel running | ✅ |
| Nginx configured | ✅ (8 sites) |
| No ports open on router | ✅ |
| No public IP | ✅ |
| DNS (AdGuard) working | ✅ |
| Databases healthy | ✅ |
| Object storage (S3) working | ✅ |
| Platform services healthy | ✅ |
| Backups | ⚠️ (configured, no cron) |
| Monitoring | ❌ |

---

## Progress: Jul 19 → Jul 20 → Jul 20 (eod)

| Item | Jul 19 | Jul 20 am | Jul 20 eod |
|------|--------|-----------|------------|
| Containers | 0 | 9 | **12** |
| Databases | 0 | 3 | **3** |
| Platform services | 0 | 0 | **3** |
| Nginx sites | 0 | 5 | **8** |
| fail2ban bans | 0 | 324 | **697** |
| RAM used | 1.0GB | 1.6GB | **3.0GB** |
| Disk used | 12GB | 15GB | **19GB** |

---

## Summary

**All 3 platform services deployed and healthy:**
- ✅ Flowero Gate (API Gateway) — `api.panomete.com`
- ✅ Flowero Discover (Service Discovery) — `discovery.panomete.com`
- ✅ Flowero Guard (Keycloak) — `auth.panomete.com`

**Infrastructure solid. 12 containers running. No issues.**

**Next:**
1. Backup cron (rclone → OneDrive)
2. Monitoring (Uptime Kuma / Beszel)
3. Deploy application services (Fluffy Mouton, Big Schwein, etc.)
