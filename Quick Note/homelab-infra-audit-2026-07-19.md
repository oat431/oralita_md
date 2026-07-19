# Homelab Infrastructure Audit — `flowero@remote.panomete.com`

> **Date:** 2026-07-19
> **Checklist:** [[Homelab-Infra-Checklist]]
> **Server:** `panomete` — Ubuntu 24.04.4 LTS, kernel 6.8.0-124
> **Hardware:** Intel i7-7700HQ (4C/8T @ 2.8GHz), 36GB RAM, 98GB LVM root (NVMe)
> **Uptime:** 42 days
> **IP:** `192.168.1.121` (eth) / `192.168.1.108` (wifi) — both DHCP

---

## 1. Hardware & Base Platform

| Item | Status | Notes |
|------|--------|-------|
| Hardware | ✅ | i7-7700HQ, 36GB RAM — solid for a homelab |
| Storage | ⚠️ | Single NVMe, **58% used** (54GB/98GB). No separate data drive, no RAID/ZFS |
| UPS | ❌ | **No UPS protection.** No `apcupsd`, `nut`, or any power management |
| Base OS | ✅ | Ubuntu 24.04 LTS, headless, SSH access |
| Proxmox | ➖ | Not using — bare metal + Docker (valid choice) |
| Docker | ✅ | Docker 29.5.3 + Compose v5.1.4 |
| Resource monitoring | ⚠️ | No `lm-sensors` (no temp monitoring). Netdata compose exists but **not running** |

### 🔴 Priority: UPS
Power loss = filesystem corruption on that NVMe. Even a small APC UPS with auto-shutdown is worth it.

---

## 2. Networking

| Item | Status | Notes |
|------|--------|-------|
| Static IP | ❌ | **Both interfaces are DHCP** (`dynamic`). Server IP could change |
| Local DNS | ❌ | No Pi-hole, no AdGuard Home, no dnsmasq. No local DNS resolution |
| VLAN segmentation | ❓ | Cannot verify from SSH — need router access |
| Reverse proxy | ✅ | **Nginx** with 25+ subdomains (`*.panomete.com`) |
| Wildcard TLS/SSL | ✅ | **Certbot/Let's Encrypt** per-subdomain certs. All HTTPS with HTTP→HTTPS redirect |
| Firewall | ⚠️ | `ufw` exists but status check requires root (likely **not configured**) |
| No port forwarding | ❌ | **Ports 80, 443, 22 are open.** No Cloudflare Tunnel or Tailscale detected |
| Tailscale/WireGuard | ❌ | **Neither installed.** Remote access relies entirely on port-forwarded SSH + Nginx |

### 🔴 Priority: Static IP
Set a DHCP reservation on your router for `192.168.1.121` (or switch to static config). If that IP drifts, all Nginx proxying to `127.0.0.1:*` still works, but DNS and any port forwards break.

### ⚠️ Priority: Local DNS
With 25+ services, remembering ports is painful. Pi-hole or AdGuard Home gives you `service.panomete.lan` locally + network-wide ad blocking.

---

## 3. Remote Access & Exposure

| Item | Status | Notes |
|------|--------|-------|
| Cloudflare Tunnel | ❌ | `cloudflared` not installed |
| Tailscale | ❌ | Not installed |
| SSH hardened | ⚠️ | `PasswordAuthentication` is **commented out** (defaults to `yes` on Ubuntu). `fail2ban` is active ✅ |
| Direct public exposure | 🔴 | **Server is directly internet-facing** via port-forwarded 80/443/22 |

### 🔴 Critical: SSH Password Auth
```
#PasswordAuthentication yes  ← commented = enabled by default
```
Anyone can brute-force SSH with passwords. `fail2ban` helps but isn't enough.

**Fix immediately:**
```bash
# /etc/ssh/sshd_config.d/hardened.conf
PasswordAuthentication no
PermitRootLogin no
AllowUsers flowero
```
Then `sudo systemctl restart sshd`

### 🔴 Critical: Direct Public Exposure
Your server is directly reachable from the internet. Consider:
- **Cloudflare Tunnel** — zero open ports, DDoS protection, free
- **Tailscale** — for admin/management access (SSH, Portainer, Grafana)
- At minimum, **close port 22** to the internet and use Tailscale for SSH

---

## 4. Container Management

| Item | Status | Notes |
|------|--------|-------|
| Compose per service | ✅ | 36 compose files, well-organized: `application/`, `database/`, `storage/`, `mq/` |
| Named volumes | ⚠️ | Only 2 named volumes (`minio_data`, `portainer_data`). Most services use bind mounts |
| Restart policy | ⚠️ | Most have `unless-stopped` ✅, but `cupdate` and `sonarqube` compose files have **no restart policy** |
| Resource limits | ❌ | **No `mem_limit` or `cpus` set** on any container. One runaway container = OOM kill |
| Container updates | ⚠️ | No Watchtower or automated update mechanism detected |
| Network isolation | ✅ | Each stack has its own bridge network (20+ networks) |
| Portainer | ✅ | Running at `monitor.panomete.com` |

### ⚠️ Priority: Resource Limits
```yaml
deploy:
  resources:
    limits:
      memory: 1G
      cpus: '2.0'
```
Add this to compose files, especially for Java-heavy services (Keycloak, n8n).

---

## 5. Storage & Backups

| Item | Status | Notes |
|------|--------|-------|
| Backup strategy | 🔴 | **No backups detected.** No cron jobs, no scripts, no backup directories |
| Automated backups | 🔴 | Zero backup automation |
| Docker volume backup | 🔴 | Only 2 named volumes — most data is in bind mounts, unbacked |
| Database backups | 🔴 | PostgreSQL, MongoDB, Redis all running — **no pg_dump, mongodump, or any backup scripts** |
| Config backup (GitOps) | ❌ | Only 4 `.git` repos found (blog, kutt, ots, writefreely). Most compose files are **not in git** |
| Backup testing | 🔴 | Nothing to test |
| Encryption at rest | ❌ | No LUKS or disk encryption |

### 🔴 Critical: No Backups
This is the single biggest risk. If that NVMe dies, **everything is gone** — Keycloak identities, databases, MinIO objects, compose configs.

**Minimum viable backup:**
1. `tar` all compose directories to an external drive/NAS daily
2. `pg_dump` PostgreSQL, `mongodump` MongoDB on cron
3. Push compose configs to a private git repo
4. rclone to Backblaze B2 ($0.005/GB/month) for offsite

---

## 6. Monitoring & Observability

| Item | Status | Notes |
|------|--------|-------|
| System metrics | ⚠️ | Grafana compose exists (`grafana.panomete.com`) but **Prometheus/Node Exporter not running** |
| Container metrics | ❌ | No cAdvisor |
| Dashboards | ⚠️ | Grafana is configured but no data sources visible |
| Log aggregation | ❌ | No Loki, Promtail, or Dozzle |
| Uptime monitoring | ⚠️ | `healthcheck.panomete.com` and `beszel` compose exist, but **neither container is running** |
| Alerting | ❌ | No alerts configured |
| Health checks | ⚠️ | Only 3/9 running containers have healthchecks (flowerogate, keycloak, stirling-pdf) |

### ⚠️ Priority: Get Monitoring Running
You have the compose files for Beszel, Grafana, and Netdata — they just need to be started. Uptime Kuma or Beszel for service health, Grafana + Prometheus for metrics.

---

## 7. Security

| Item | Status | Notes |
|------|--------|-------|
| Auto security updates | ✅ | `unattended-upgrades` installed and active |
| Non-root containers | ❓ | Cannot verify without inspecting each Dockerfile — likely most run as root |
| Default passwords | ❓ | **Cannot verify** — need to check Keycloak, MinIO, Portainer, PostgreSQL, MongoDB, Redis passwords |
| Secrets management | ⚠️ | Need to check if `.env` files are gitignored and chmod 600 |
| fail2ban | ✅ | Active and running (since Jul 8) |
| Crowdsec | ❌ | Not installed |
| Container image scanning | ❌ | No `trivy` or scanning |
| Regular audits | ❌ | No evidence of periodic audits |

### 🔴 Critical: Services Bound to 0.0.0.0
These containers are **directly accessible from the LAN (and potentially internet)** without going through Nginx:

| Service | Port | Risk |
|---------|------|------|
| bytestash | 8201 | Direct access, no auth |
| dashdot | 8090 | System info exposure |
| stirling-pdf | 8091 | Direct access |
| homarr | 7575 | Dashboard, no auth |
| portainer | 9443 | **Full Docker control** |
| minio | 9001, 9002 | Object storage admin |
| it-tools | 6080 | Direct access |

**Fix:** Bind to `127.0.0.1` in compose files since Nginx handles external routing:
```yaml
ports:
  - "127.0.0.1:8090:3001"  # instead of "8090:3001"
```

---

## 8. Services Running

### Currently Active (9 containers)

| Service | Purpose | Status |
|---------|---------|--------|
| **flowerogate** | API Gateway (Spring Boot) | ✅ Healthy |
| **keycloak** | Identity/Auth | ⚠️ **Unhealthy** (JGroups cert errors) |
| **bytestash** | Code snippet manager | ✅ Running |
| **dashdot** | System dashboard | ✅ Running |
| **stirling-pdf** | PDF tools | ✅ Healthy |
| **homarr** | Dashboard | ✅ Running |
| **portainer** | Docker management | ✅ Running |
| **minio** | Object storage | ✅ Running |
| **it-tools** | Dev utilities | ✅ Running |

### Configured but NOT Running (~20+ services)
Grafana, Netdata, Beszel, n8n, Nextcloud, SonarQube, MongoDB, PostgreSQL, Redis, RabbitMQ, cupdate, checkmate, dashlit, kutt, writefreely, rxresume, convertx, submag, slash, OTS, hemmeling

### Other Running Services (non-Docker)
- **Nginx** (reverse proxy, 25+ vhosts)
- **PostgreSQL** (native, port 5432)
- **MongoDB** (native, port 27017, bound to localhost ✅)
- **Redis** (native, port 6379, bound to localhost ✅)
- **Mail server** (ports 25, 110, 143, 587, 993, 995 — SMTP/IMAP/POP3)

### ⚠️ Keycloak Unhealthy
Stack trace in logs suggests JGroups certificate rotation issues. Needs investigation.

---

## 9. Maintenance & Operations

| Item | Status | Notes |
|------|--------|-------|
| Runbook | ❌ | No documentation found |
| Update schedule | ⚠️ | OS auto-updates ✅, but no container update schedule |
| Changelog | ❌ | No change tracking |
| Disaster recovery plan | ❌ | No backups = no recovery plan |
| Power consumption | ❓ | i7-7700HQ laptop-class ~45-65W. Need a Kill-A-Watt to confirm |
| Noise management | ➖ | Depends on form factor |

---

## 🔥 Quick Sanity Check Summary

| Check | Status |
|-------|--------|
| All services via subdomain (not IP:port) | ✅ All 25+ services have `*.panomete.com` |
| HTTPS on all services | ✅ Let's Encrypt, HTTP→HTTPS redirect |
| SSH key-only | ❌ **Password auth still enabled** |
| No ports open on router | ❌ **80, 443, 22 all open** |
| Backups automated & tested | ❌ **No backups at all** |
| Monitoring alerts | ❌ **No monitoring running** |
| Firewall default-deny | ❌ **No firewall configured** |
| All compose files in git | ❌ **Only 4/36 in git** |
| Docker restart policies | ⚠️ Most OK, 2 missing |
| No default passwords | ❓ Cannot verify |
| Disk space monitored | ❌ No alerts |
| UPS protection | ❌ **None** |
| Monthly power cost | ❓ Unknown |

---

## 🎯 Top 5 Actions (Priority Order)

1. **🔒 Harden SSH NOW** — Disable password auth, disable root login, add `AllowUsers flowero`
2. **💾 Set up backups** — At minimum: compose files to git + `pg_dump`/`mongodump` daily + rclone to B2
3. **🛡️ Configure firewall** — `ufw` default deny, allow only 22/80/443, bind containers to `127.0.0.1`
4. **🌐 Tailscale or Cloudflare Tunnel** — Stop exposing SSH directly to the internet
5. **📊 Start monitoring** — You have the compose files, just `docker compose up -d` Beszel + Grafana
