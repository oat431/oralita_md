# Home Lab Installation

> Complete guide for setting up a homelab server from scratch.
> Last updated: 2026-08-22

---

## Steps

1. [[01-SSH-Key-Setup]]
   - [[01.1-Allow-Other-Devices]]
2. [[02-SSH-Hardening]]
3. [[03-Firewall-UFW]]
4. [[04-Fail2ban]]
5. [[05-Docker-Install]]
6. [[06-Tailscale]]
7. [[07-Cloudflare-Tunnel]]
8. [[08-Reverse-Proxy-Nginx]]
   - [[08.1-Add-Subdomain]]
   - [[08.2-Serve-Static-Files]]
9. [[09-Backups]]
10. [[10-Monitoring]]

---

## Quick Sanity Check

After completing all steps, verify:

- [ ] SSH key-only auth (password login fails)
- [ ] `sudo ufw status` shows default deny
- [ ] `fail2ban` is active
- [ ] `docker run hello-world` works
- [ ] `tailscale status` shows your server
- [ ] `cloudflared` tunnel is running
- [ ] Nginx proxies to your services

## Components

- [[home-lab-apps]] — app / subdomain / port registry
- [[db-network-integration-guide]] — shared database network
- [[docker-network]] · [[port-convention]] · [[public-vs-private]]

## Obsidian LiveSync (self-hosted)

1. [[01-full-setup]] — server side: CouchDB → Nginx → CORS
2. [[02-connection-guide]] — client side: connect a vault
3. [[03-couchdb-user-management]] — add users

## Audit Trail

- [[Homelab-Infra-Checklist]] — index of all infrastructure audits
