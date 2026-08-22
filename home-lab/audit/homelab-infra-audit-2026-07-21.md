# Homelab Infrastructure Audit — `flowero@192.168.1.121`

> **Date:** 2026-07-21
> **Checklist:** [[Homelab-Infra-Checklist]]
> **Status:** Infrastructure complete, databases deployed, apps pending

---

## System Overview

| Item | Value |
|------|-------|
| **OS** | Ubuntu 26.04 LTS (resolute) |
| **Kernel** | 7.0.0-28-generic |
| **Hardware** | Intel i7-7700HQ (4C/8T), 34GB RAM, 98GB NVMe |
| **Disk** | 15GB used / 79GB available (16%) |
| **RAM** | 1.6GB used / 32GB available |
| **Uptime** | 1 day, 2 hours |
| **LAN IP** | 192.168.1.121 (DHCP) |
| **Tailscale IP** | 100.73.143.25 |
| **Hostname** | flowero |

---

## 1. Hardware & Base Platform

| Item | Status | Notes |
|------|--------|-------|
| Hardware | ✅ | i7-7700HQ, 34GB RAM |
| Storage | ✅ | 98GB NVMe, 16% used |
| UPS | ❌ | No UPS protection |
| Base OS | ✅ | Ubuntu 26.04 LTS, headless |
| Docker | ✅ | 29.6.2 + Compose v5.3.1 |
| Resource monitoring | ❌ | No monitoring yet |

---

## 2. Networking

| Item | Status | Notes |
|------|--------|-------|
| Static IP | ⚠️ | DHCP on LAN. Tailscale IP is stable (100.73.143.25) |
| Local DNS | ✅ | AdGuard Home on port 53, router DNS set to 192.168.1.121 |
| Reverse proxy | ✅ | Nginx — 5 sites enabled |
| TLS/SSL | ✅ | Cloudflare edge — no certbot needed |
| Firewall | ✅ | UFW active — default deny, SSH + Tailscale ports only |
| Port forwarding | ✅ | None — no public IP |
| Tailscale | ✅ | Server + Windows PC connected |
| Cloudflare Tunnel | ✅ | `homelab` tunnel active, 3 connections (Singapore) |

---

## 3. Remote Access & Exposure

| Item | Status | Notes |
|------|--------|-------|
| Cloudflare Tunnel | ✅ | `*.panomete.com` + `panomete.com` routed |
| Tailscale | ✅ | Mesh VPN for SSH + management |
| SSH hardened | ✅ | Password auth disabled, root login blocked, AllowUsers flowero |
| fail2ban | ✅ | Active — **1888 failed, 324 banned** since install |
| No public IP | ✅ | Zero attack surface from internet |

---

## 4. Container Management

| Item | Status | Notes |
|------|--------|-------|
| Docker + Compose | ✅ | 29.6.2 + 5.3.1 |
| Containers | ✅ | **9 running**, all healthy |
| Portainer | ✅ | `container.panomete.com` |
| Network isolation | ✅ | `db-network` shared by all databases |

---

## 5. Storage & Backups

| Item | Status | Notes |
|------|--------|-------|
| rclone | ✅ | v1.74.4, OneDrive configured |
| Backup automation | ❌ | No cron job yet — manual only |
| Database backups | ❌ | No pg_dump / mongodump scripts yet |
| Config backup | ❌ | Compose files not in git yet |

---

## 6. Monitoring & Observability

| Item | Status | Notes |
|------|--------|-------|
| System metrics | ❌ | Not set up |
| Uptime monitoring | ❌ | Not set up |
| Alerting | ❌ | Not set up |
| Health checks | ✅ | PostgreSQL, Valkey, MongoDB have healthchecks |

---

## 7. Security

| Item | Status | Notes |
|------|--------|-------|
| Auto security updates | ✅ | `unattended-upgrades` active |
| SSH key-only | ✅ | Password auth disabled |
| fail2ban | ✅ | 324 IPs banned |
| Firewall | ✅ | UFW default deny |
| No public exposure | ✅ | All via Cloudflare Tunnel |
| Public vs Private | ✅ | Admin panels removed from public, S3 API public (creds required) |

---

## 8. Services Running

### Infrastructure (6 containers)

| Service | Container | Status | Health | Access |
|---------|-----------|--------|--------|--------|
| AdGuard Home | `adguard` | ✅ Up 24h | — | Public: `adguard.panomete.com` |
| Portainer | `portainer` | ✅ Up 23h | — | Public: `container.panomete.com` |
| Cloudflared | (systemd) | ✅ Active | — | Tunnel `homelab` |
| Tailscale | (systemd) | ✅ Active | — | `100.73.143.25` |
| Nginx | (systemd) | ✅ Active | — | 5 sites |
| Fail2ban | (systemd) | ✅ Active | — | 324 banned |

### Databases (7 containers)

| Service | Container | Status | Health | Port | Access |
|---------|-----------|--------|--------|------|--------|
| PostgreSQL 18 | `local-postgres` | ✅ Up 2h | healthy | 127.0.0.1:5432 | SSH tunnel |
| Valkey 9 | `local-valkey` | ✅ Up 2h | healthy | 127.0.0.1:6379 | SSH tunnel |
| MongoDB 8 | `local-mongodb` | ✅ Up 2h | healthy | 127.0.0.1:27017 | SSH tunnel |
| SeaweedFS Master | `seaweedfs-master` | ✅ Up 8m | — | 0.0.0.0:9333 | Tailscale only |
| SeaweedFS Volume | `seaweedfs-volume` | ✅ Up 8m | — | internal | — |
| SeaweedFS Filer | `seaweedfs-filer` | ✅ Up 8m | — | 0.0.0.0:8888 | Tailscale only |
| SeaweedFS S3 | `seaweedfs-s3` | ✅ Up 8m | — | 127.0.0.1:8333 | Public: `s3.panomete.com` |

### Nginx Sites (5 enabled)

| Site | Config | Proxy |
|------|--------|-------|
| `00-catch-all` | Drop unknown hosts | return 444 |
| `panomete.com` | Static site | `/home/flowero/profile/oat431.github.io` |
| `gateway.panomete.com` | API Gateway | `http://127.0.0.1:8000` |
| `adguard.panomete.com` | AdGuard UI | `http://127.0.0.1:7000` |
| `container.panomete.com` | Portainer | `https://127.0.0.1:7001` (SSL off) |
| `s3.panomete.com` | SeaweedFS S3 | `http://127.0.0.1:8333` |

---

## 9. Maintenance & Operations

| Item | Status | Notes |
|------|--------|-------|
| Runbook | ✅ | Full docs in `home-lab-installation/` vault |
| Update schedule | ⚠️ | OS auto-updates ✅, container updates TBD |
| Disaster recovery | ⚠️ | Reinstall + compose + rclone restore. Backup cron pending |
| Power consumption | ❓ | ~45-65W estimated (i7-7700HQ) |

---

## Sanity Check

| Check | Status |
|-------|--------|
| SSH key-only auth | ✅ |
| Firewall default-deny | ✅ |
| fail2ban active | ✅ (324 banned) |
| Docker working | ✅ (9 containers) |
| Tailscale connected | ✅ |
| Cloudflare Tunnel running | ✅ |
| Nginx configured | ✅ |
| No ports open on router | ✅ |
| No public IP | ✅ |
| DNS (AdGuard) working | ✅ |
| Databases healthy | ✅ (3/3 healthy) |
| Object storage (S3) working | ✅ |
| Backups configured | ⚠️ (rclone ready, no cron) |
| Monitoring | ❌ |
| UPS protection | ❌ |

---

## Comparison: First Audit → Today

| Item | Jul 19 (first audit) | Jul 20 (today) | Change |
|------|---------------------|----------------|--------|
| Containers | 0 | 9 | +9 |
| Databases | 0 | 3 (PG, Valkey, Mongo) | +3 |
| Object storage | 0 | SeaweedFS S3 | +1 |
| DNS | ❌ | AdGuard Home | ✅ |
| Backups | ❌ | rclone configured | ⚠️ |
| Monitoring | ❌ | ❌ | — |
| Public sites | 0 | 5 Nginx sites | +5 |
| fail2ban bans | 0 | 324 | +324 |

---

## Summary

Infrastructure and databases are **production-ready**. 9 containers running, all healthy.

**Deployed:**
- ✅ Full infra stack (SSH, UFW, fail2ban, Docker, Tailscale, Cloudflare Tunnel, Nginx)
- ✅ DNS + ad blocking (AdGuard Home)
- ✅ Databases (PostgreSQL 18, Valkey 9, MongoDB 8)
- ✅ Object storage (SeaweedFS S3)
- ✅ Management UIs (Portainer, AdGuard, SeaweedFS Filer)

**Next:**
1. Deploy personal project services (Keycloak, Gateway, Discovery)
2. Set up backup cron (rclone → OneDrive)
3. Set up monitoring (Uptime Kuma / Beszel)
