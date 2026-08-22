# Homelab Infrastructure Audit — `flowero@192.168.1.121`

> **Date:** 2026-07-19
> **Checklist:** [[Homelab-Infra-Checklist]]
> **Status:** Fresh install, infrastructure complete, no services deployed yet

---

## System Overview

| Item | Value |
|------|-------|
| **OS** | Ubuntu 26.04 LTS (resolute) |
| **Kernel** | 7.0.0-28-generic |
| **Hardware** | Intel i7-7700HQ (4C/8T), 34GB RAM, 98GB NVMe |
| **Disk** | 12GB used / 82GB available (13%) |
| **RAM** | 1.0GB used / 33GB available |
| **Uptime** | 1h 44m |
| **LAN IP** | 192.168.1.121 (DHCP) |
| **Tailscale IP** | 100.73.143.25 |
| **Hostname** | flowero |

---

## 1. Hardware & Base Platform

| Item | Status | Notes |
|------|--------|-------|
| Hardware | ✅ | i7-7700HQ, 34GB RAM |
| Storage | ✅ | 98GB NVMe, 13% used — plenty of room |
| UPS | ❌ | No UPS protection |
| Base OS | ✅ | Ubuntu 26.04 LTS, headless, SSH only |
| Docker | ✅ | Docker 29.6.2 + Compose v5.3.1 |
| Resource monitoring | ❌ | No lm-sensors, no monitoring yet |

---

## 2. Networking

| Item              | Status | Notes                                                     |
| ----------------- | ------ | --------------------------------------------------------- |
| Static IP         | ⚠️     | Still DHCP on LAN. Tailscale IP is stable (100.73.143.25) |
| Local DNS         | ❌      | No Pi-hole / AdGuard                                      |
| Reverse proxy     | ✅      | Nginx — catch-all (444) + gateway.panomete.com config     |
| TLS/SSL           | ✅      | Handled by Cloudflare at edge — no certbot needed         |
| Firewall          | ✅      | UFW active — default deny, only SSH (22) allowed          |
| Port forwarding   | ✅      | None — no public IP, no ports open on router              |
| Tailscale         | ✅      | Installed, connected, enabled on boot                     |
| Cloudflare Tunnel | ✅      | `homelab` tunnel active, 4 connections (Singapore)        |

---

## 3. Remote Access & Exposure

| Item | Status | Notes |
|------|--------|-------|
| Cloudflare Tunnel | ✅ | `*.panomete.com` + `panomete.com` routed to tunnel |
| Tailscale | ✅ | Server + Windows PC on tailnet |
| SSH hardened | ✅ | Password auth disabled, root login blocked, AllowUsers flowero |
| fail2ban | ✅ | Active on sshd jail — 17 failed attempts, 3 banned (since install) |
| No direct public IP | ✅ | Public IP cancelled — zero attack surface |

---

## 4. Container Management

| Item | Status | Notes |
|------|--------|-------|
| Docker + Compose | ✅ | 29.6.2 + 5.3.1 |
| Containers running | ➖ | None yet — clean slate |
| Compose files | ➖ | None yet — ready for deployment |
| Restart policies | ➖ | N/A |
| Resource limits | ➖ | N/A |
| Network isolation | ➖ | N/A |
| Portainer | ➖ | About to deploy |

---

## 5. Storage & Backups

| Item | Status | Notes |
|------|--------|-------|
| Backup strategy | ❌ | Not set up yet — will configure after services deploy |
| Automated backups | ❌ | Pending |
| Config backup (GitOps) | ❌ | Pending |

---

## 6. Monitoring & Observability

| Item | Status | Notes |
|------|--------|-------|
| System metrics | ❌ | Not set up yet |
| Uptime monitoring | ❌ | Not set up yet |
| Alerting | ❌ | Pending |

---

## 7. Security

| Item | Status | Notes |
|------|--------|-------|
| Auto security updates | ✅ | `unattended-upgrades` active |
| SSH key-only | ✅ | Password auth disabled |
| fail2ban | ✅ | Active, 3 IPs banned so far |
| Firewall | ✅ | UFW default deny, only port 22 |
| No public exposure | ✅ | All traffic via Cloudflare Tunnel |
| Secrets management | ➖ | N/A — no services yet |

---

## 8. Services Running

| Service | Status | Notes |
|---------|--------|-------|
| **Nginx** | ✅ | Reverse proxy, server_tokens off |
| **Cloudflared** | ✅ | Tunnel `homelab`, enabled on boot |
| **Tailscale** | ✅ | Mesh VPN, enabled on boot |
| **Docker** | ✅ | Ready for containers |

---

## 9. Maintenance & Operations

| Item | Status | Notes |
|------|--------|-------|
| Runbook | ✅ | Documented in `home-lab-installation/` vault |
| Update schedule | ⚠️ | OS auto-updates ✅, container updates TBD |
| Disaster recovery | ⚠️ | Reinstall + compose files + DB dumps. Backups pending |

---

## Sanity Check

| Check | Status |
|-------|--------|
| SSH key-only auth | ✅ |
| Firewall default-deny | ✅ |
| fail2ban active | ✅ |
| Docker working | ✅ |
| Tailscale connected | ✅ |
| Cloudflare Tunnel running | ✅ |
| Nginx configured | ✅ |
| No ports open on router | ✅ |
| No public IP | ✅ |
| Backups automated | ❌ (pending services) |
| Monitoring alerts | ❌ (pending services) |
| UPS protection | ❌ |

---

## Summary

Infrastructure is **production-ready**. Clean Ubuntu 26.04 LTS install with:

- ✅ **Security:** SSH hardened, UFW, fail2ban, no public IP
- ✅ **Access:** Tailscale (mesh VPN) + Cloudflare Tunnel (web)
- ✅ **Runtime:** Docker + Docker Compose ready
- ✅ **Proxy:** Nginx with catch-all + subdomain routing
- ✅ **Documentation:** Full runbook in Obsidian vault

**Next:** Deploy services (Portainer → Keycloak → databases → apps)
