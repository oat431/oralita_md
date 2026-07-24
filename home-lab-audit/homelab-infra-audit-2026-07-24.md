# Homelab Infrastructure Audit — `flowero@192.168.1.121`

> **Date:** 2026-07-24 (UTC+7)
> **Checklist:** [[Homelab-Infra-Checklist]]
> **Status:** Infrastructure + databases + platform + monitoring deployed

---

## System Overview

| Item | Value |
|------|-------|
| **OS** | Ubuntu 26.04 LTS (resolute) |
| **Kernel** | 7.0.0-28-generic |
| **Hardware** | Intel i7-7700HQ (4C/8T), 34GB RAM, 98GB NVMe |
| **Disk** | 23GB used / 71GB available (24%) |
| **RAM** | 3.8GB used / 30GB available |
| **Uptime** | 5 days, 3 hours |
| **LAN IP** | 192.168.1.121 (DHCP) |
| **Tailscale IP** | 100.73.143.25 |
| **Hostname** | flowero |

---

## 1. Hardware & Base Platform

| Item | Status | Notes |
|------|--------|-------|
| Hardware | ✅ | i7-7700HQ, 34GB RAM |
| Storage | ✅ | 98GB NVMe, 24% used |
| UPS | ❌ | No UPS protection |
| Base OS | ✅ | Ubuntu 26.04 LTS, headless |
| Docker | ✅ | 29.6.2 + Compose v5.3.1 |

---

## 2. Networking

| Item | Status | Notes |
|------|--------|-------|
| Static IP | ⚠️ | DHCP on LAN. Tailscale IP stable |
| Local DNS | ✅ | AdGuard Home, router DNS set |
| Reverse proxy | ✅ | Nginx — 10 sites enabled |
| TLS/SSL | ✅ | Cloudflare edge |
| Firewall | ✅ | UFW active — default deny |
| Tailscale | ✅ | Server + Windows PC |
| Cloudflare Tunnel | ✅ | `homelab` active, 4 connections |

---

## 3. Remote Access & Exposure

| Item | Status | Notes |
|------|--------|-------|
| Cloudflare Tunnel | ✅ | `*.panomete.com` routed |
| Tailscale | ✅ | Mesh VPN active |
| SSH hardened | ✅ | Password disabled, root blocked, AllowUsers flowero |
| fail2ban | ✅ | **4245 failed, 705 banned** since install |
| No public IP | ✅ | Zero attack surface |

---

## 4. Container Management

| Item | Status | Notes |
|------|--------|-------|
| Docker + Compose | ✅ | 29.6.2 + 5.3.1 |
| Containers | ✅ | **17 running** |
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
| Promtail | ✅ | Log shipper (no healthcheck) |
| Uptime Kuma | ⚠️ | `status.panomete.com`, unhealthy — 502 errors on some monitors |
| System metrics | ✅ | Via Prometheus |
| Alerting | ⚠️ | Grafana configured, needs alert rules |

---

## 7. Security

| Item | Status | Notes |
|------|--------|-------|
| Auto security updates | ✅ | `unattended-upgrades` active |
| SSH key-only | ✅ | Password disabled |
| fail2ban | ✅ | 705 IPs banned |
| Firewall | ✅ | UFW default deny |
| No public exposure | ✅ | Via Cloudflare Tunnel |

---

## 8. Services Running

### Infrastructure (3 containers + systemd)

| Service | Container | Status | Health |
|---------|-----------|--------|--------|
| AdGuard Home | `adguard` | ✅ Up 5 days | — |
| Portainer | `portainer` | ✅ Up 5 days | — |
| Cloudflared | (systemd) | ✅ Active | — |
| Nginx | (systemd) | ✅ Active | — |

### Platform Services (3 containers)

| Service | Container | Status | Health | Access |
|---------|-----------|--------|--------|--------|
| Flowero Gate | `flowero-gate` | ✅ Up 9m | healthy | `api.panomete.com` |
| Flowero Discover | `flowero-discover` | ✅ Up 9m | healthy | `discovery.panomete.com` |
| Flowero Guard (Keycloak) | `flowero-guard` | ✅ Up 9m | healthy | `auth.panomete.com` |

### Monitoring Stack (4 containers)

| Service | Container | Status | Health | Access |
|---------|-----------|--------|--------|--------|
| Grafana | `grafana` | ✅ Up 42m | healthy | `grafana.panomete.com` |
| Prometheus | `prometheus` | ✅ Up 28m | healthy | — |
| Loki | `loki` | ✅ Up 42m | healthy | — |
| Promtail | `promtail` | ✅ Up 42m | — | — |
| Uptime Kuma | `uptime-kuma` | ✅ Up 45m | ⚠️ unhealthy | `status.panomete.com` |

### Databases (7 containers)

| Service | Container | Status | Health | Port |
|---------|-----------|--------|--------|------|
| PostgreSQL 18 | `local-postgres` | ✅ Up 4 days | healthy | 127.0.0.1:5432 |
| Valkey 9 | `local-valkey` | ✅ Up 4 days | healthy | 127.0.0.1:6379 |
| MongoDB 8 | `local-mongodb` | ✅ Up 4 days | healthy | 127.0.0.1:27017 |
| SeaweedFS Master | `seaweedfs-master` | ✅ Up 4 days | — | 0.0.0.0:9333 |
| SeaweedFS Volume | `seaweedfs-volume` | ✅ Up 4 days | — | internal |
| SeaweedFS Filer | `seaweedfs-filer` | ✅ Up 4 days | — | 0.0.0.0:8888 |
| SeaweedFS S3 | `seaweedfs-s3` | ✅ Up 4 days | — | 127.0.0.1:8333 |

### Nginx Sites (10 enabled)

| Site | Target |
|------|--------|
| `00-catch-all` | return 444 |
| `panomete.com` | Static profile site |
| `api.panomete.com` | Flowero Gate |
| `auth.panomete.com` | Keycloak |
| `discovery.panomete.com` | Flowero Discover |
| `grafana.panomete.com` | Grafana |
| `status.panomete.com` | Uptime Kuma |
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
| Docker working | ✅ (17 containers) |
| Tailscale connected | ✅ |
| Cloudflare Tunnel running | ✅ |
| Nginx configured | ✅ (10 sites) |
| No public IP | ✅ |
| DNS (AdGuard) working | ✅ |
| Databases healthy | ✅ |
| Platform services healthy | ✅ |
| Monitoring deployed | ✅ |
| Uptime monitoring | ⚠️ (unhealthy — 502 on some monitors) |
| Backups | ⚠️ (configured, no cron) |

---

## Progress: Jul 19 → Jul 23 → Jul 24

| Item | Jul 19 | Jul 23 | Jul 24 |
|------|--------|--------|--------|
| Containers | 0 | 12 | **17** |
| Databases | 0 | 3 | **3** |
| Platform services | 0 | 3 | **3** |
| Monitoring | 0 | 0 | **5** |
| Nginx sites | 0 | 8 | **10** |
| fail2ban bans | 0 | 697 | **705** |
| RAM used | 1.0GB | 3.0GB | **3.8GB** |
| Disk used | 12GB | 19GB | **23GB** |

---

## Summary

**Full monitoring stack deployed:**
- ✅ Grafana — dashboards and visualization
- ✅ Prometheus — metrics collection
- ✅ Loki — log aggregation
- ✅ Promtail — log shipping
- ⚠️ Uptime Kuma — service health (unhealthy, needs attention)

**17 containers running. Infrastructure solid.**

**Issues:**
- ⚠️ Uptime Kuma unhealthy — showing 502 on keycloak/API gateway monitors
- ❌ Backup cron not set up

**Next:**
1. Fix Uptime Kuma health status
2. Set up backup cron (rclone → OneDrive)
3. Deploy application services
