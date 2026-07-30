---
name: homelab-server-setup
description: Set up a homelab server from scratch — SSH hardening, firewall, Docker, VPN (Tailscale), Cloudflare Tunnel, reverse proxy, backups, monitoring. Includes documentation patterns for Obsidian vaults.
triggers:
  - homelab setup
  - server provisioning
  - bare metal install
  - cloudflare tunnel setup
  - tailscale setup
  - infrastructure checklist
  - ssh hardening
  - ufw firewall
  - fail2ban
---

# Homelab Server Setup

End-to-end guide for provisioning a homelab server. Covers base OS through to Cloudflare Tunnel + Tailscale with zero public IP exposure.

## Workflow (Execute in Order)

1. **SSH Key Setup** — generate key pair, copy to server, enable passwordless sudo
2. **SSH Hardening** — disable password auth, block root login, whitelist users
3. **UFW Firewall** — default deny incoming, allow SSH only
4. **Fail2ban** — ban IPs after failed login attempts
5. **Docker + Compose** — container runtime for all services
6. **Tailscale** — mesh VPN for remote access (needs user auth)
7. **Cloudflare Tunnel** — expose web services without open ports (needs user auth)
8. **Nginx** — reverse proxy, routes by subdomain to localhost services
9. **Backups** — rclone to Backblaze B2
10. **Monitoring** — Uptime Kuma + Beszel

## Documentation Pattern (User Preference)

When documenting setup guides in the user's Obsidian vault:

- **Split into numbered files**: `01-Step-Name.md`, `02-Step-Name.md`, etc.
- **Create an index file** with `[[wikilinks]]` to each step
- **Every command gets a table** explaining each flag/argument
- **Every section has a "Why" paragraph** — not just what, but why
- **Anonymize project-specific names** in team-facing docs (use "Service A", "Service B")
- Keep personal project names only in the private vault

## SSH Automation from Windows (MINGW64/Git Bash)

See `references/ssh-automation-windows.md` for pitfalls and workarounds.

## Tailscale Setup

See `references/tailscale-setup.md` for the full workflow: install → auth → verify → DNS alias for SSH.

Key points:
- Tailscale IPs are stable per device (never change)
- SSH goes through Tailscale (Cloudflare Tunnel is HTTP/HTTPS only)
- Each device gets its own SSH key pair — never share private keys
- DNS A record for SSH alias must be **DNS only** (gray cloud), not proxied

## Ubuntu 26.04 "resolute" Compatibility

See `references/ubuntu-2604-compat.md` for known issues with package repos.

## Cloudflare Tunnel Setup

See `references/cloudflare-tunnel-setup.md` for the full workflow: auth → create tunnel → config → DNS routing → service install.

Key points:
- Wildcard CNAME (`*.example.com`) covers all subdomains — no per-subdomain DNS changes needed
- When migrating from public IP, delete old A/MX/SPF/DMARC records first before routing DNS to tunnel
- Service installer looks in `/etc/cloudflared/`, NOT `~/.cloudflared/`

## Nginx Configuration

- TLS terminates at Cloudflare edge — Nginx listens on **HTTP only** (port 80)
- Always create a catch-all server that returns 444 for unknown hosts:
  ```nginx
  server {
      listen 80 default_server;
      server_name _;
      return 444;
  }
  ```
- Name it `00-catch-all` so it loads first
- Each service gets its own config in `sites-available/` with a symlink to `sites-enabled/`
- Always `nginx -t` before `systemctl reload nginx`
- Set `server_tokens off;` in `nginx.conf` to hide version

### Proxy Patterns

See `references/nginx-proxy-patterns.md` for full configs. Summary:

| Service Type | `proxy_pass` | Extra directive |
|-------------|-------------|-----------------|
| HTTP service | `http://127.0.0.1:PORT` | none |
| HTTPS service (Portainer, Keycloak) | `https://127.0.0.1:PORT` | `proxy_ssl_verify off;` |
| Static files | `root /path/to/site;` + `try_files` | `usermod -aG <user> www-data` + `chmod -R g+rX` |

### Static File Serving Pitfall

Nginx runs as `www-data`. Home directories are `750` (owner-only). Nginx gets 404/403.

**Fix:**
```bash
sudo usermod -aG <user> www-data
chmod -R g+rX /home/<user>/path/to/site/
sudo systemctl restart nginx  # MUST restart, not reload — group membership changes need full restart
```

**PITFALL: `reload` does NOT pick up group membership changes.** Nginx workers keep old groups until restarted.

## Key Pitfalls

### Sudo over SSH (non-interactive)
- `sudo -S` (pipe password via stdin) is blocked by security tooling
- **Solution**: Set up NOPASSWD sudoers drop-in BEFORE automation:
  ```bash
  echo 'user ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/user
  ```
- Revoke later with `sudo rm /etc/sudoers.d/user`

### Cloudflare Tunnel service install
- `cloudflared service install` looks for config in `/etc/cloudflared/`, NOT `~/.cloudflared/`
- Copy both `config.yml` and the tunnel credential JSON to `/etc/cloudflared/` before installing

### Docker repo in SSH commands
- Variable expansion (`$VERSION_CODENAME`) breaks when embedded in SSH heredocs with escaping
- **Solution**: Write the repo file in a separate SSH command using `echo "..." | sudo tee`
- Or compute variables server-side: `ARCH=$(dpkg --print-architecture) && CODENAME=$(lsb_release -cs)`

### Service binding
- All services should bind to `127.0.0.1` in compose files
- Nginx handles external routing via subdomain
- Never expose service ports directly on `0.0.0.0`
- **Exception**: DNS (port 53) needs `0.0.0.0` if other LAN devices should use it

### DNS server conflict with systemd-resolved
- `systemd-resolved` occupies port 53 by default
- Must disable before running AdGuard Home or any DNS server:
  ```bash
  sudo systemctl disable --now systemd-resolved
  echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf  # temporary
  # After DNS server is running:
  echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf  # point to local DNS
  ```

## Architecture Template

```
Internet (no public IP)
├── Cloudflare Tunnel → Nginx (localhost:80) → services
├── Tailscale → SSH (port 22)
└── UFW (default deny, SSH only)

Docker Compose Stack
├── Infrastructure: Keycloak, API Gateway, Service Discovery, Load Balancer
├── Applications: Service A, B, C, ...
├── Databases: PostgreSQL, MongoDB, Redis, MinIO
└── Monitoring: Uptime Kuma, Beszel
```
