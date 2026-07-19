# Home Lab Installation

> Complete guide for setting up a homelab server from scratch.
> Last updated: 2026-07-19

---

## Steps

1. [[01-SSH-Key-Setup]]
2. [[02-SSH-Hardening]]
3. [[03-Firewall-UFW]]
4. [[04-Fail2ban]]
5. [[05-Docker-Install]]
6. [[06-Tailscale]]
7. [[07-Cloudflare-Tunnel]]
8. [[08-Reverse-Proxy-Nginx]]
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
