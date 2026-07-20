---
name: homelab-infrastructure
description: Set up and maintain a homelab server from bare metal to production-ready — SSH hardening, UFW, Docker, reverse proxy, Cloudflare Tunnel, Tailscale, databases, and service deployment.
triggers:
  - homelab setup
  - server configuration
  - reverse proxy setup
  - cloudflare tunnel
  - tailscale setup
  - docker compose for self-hosted
  - nginx subdomain config
  - database container setup
---

# Homelab Infrastructure

Set up a homelab server from fresh Ubuntu install to production-ready stack. Covers SSH hardening, firewall, Docker, reverse proxy, Cloudflare Tunnel, Tailscale, databases, and service deployment.

## Architecture Pattern

```
Public (anyone)    → Cloudflare Tunnel → Nginx (:80) → service
Private (you only) → Tailscale → direct access by port
```

- Cloudflare Tunnel handles HTTP/HTTPS only (no TCP/UDP)
- Tailscale handles SSH, management UIs, game servers, any port
- Nginx routes by Host header, all services bind to `127.0.0.1`
- DNS wildcard (`*.domain.com`) → tunnel — no per-subdomain DNS changes needed

## Setup Order

1. SSH key setup (no passphrase for automation keys)
2. SSH hardening (`PasswordAuthentication no`, `PermitRootLogin no`, `AllowUsers`)
3. UFW firewall (default deny, allow SSH only)
4. Fail2ban
5. Docker + Docker Compose
6. Tailscale (install on server + all client devices)
7. Cloudflare Tunnel (`cloudflared tunnel create`, wildcard routing)
8. Nginx reverse proxy (one config per subdomain)

## Key Pitfalls

### SSH ed25519 with passphrase fails for automation
On Windows MINGW64, ed25519 keys with passphrase fail silently in non-interactive mode (`sign_and_send_pubkey: we did not send a packet`). Use RSA with `-N ""` for automation keys.

### SSH_ASKPASS for password-based SSH on Windows
```bash
cat > /tmp/ssh_pass.sh << 'SCRIPT'
#!/bin/bash
echo 'password'
SCRIPT
chmod +x /tmp/ssh_pass.sh
export SSH_ASKPASS="/tmp/ssh_pass.sh" SSH_ASKPASS_REQUIRE=force DISPLAY=":0"
ssh -o StrictHostKeyChecking=no user@host "command" < /dev/null
```

### Nginx can't read files in /home/user
Nginx runs as `www-data`. Home directory is `750` (owner-only).
```bash
sudo usermod -aG flowero www-data
chmod -R g+rX /home/flowero/path/to/site
# MUST restart nginx (not reload) for group change to take effect
sudo systemctl restart nginx
```

### HTTPS vs HTTP proxy_pass
- Portainer (9443) = HTTPS → `proxy_pass https://` + `proxy_ssl_verify off`
- Most services = HTTP → `proxy_pass http://`
- SeaweedFS, AdGuard, etc. = HTTP → `proxy_pass http://`

### Cloudflare Tunnel only does HTTP/HTTPS
Game servers, custom TCP/UDP ports → use Tailscale directly, not Cloudflare Tunnel.

### DNS for game servers / custom ports
Create A record → Tailscale IP, **proxy OFF** (DNS only / gray cloud). Orange cloud breaks non-HTTP traffic.

### SeaweedFS v4.40 breaking changes
- `-master` flag on S3 gateway changed to `-filer`
- `security.toml` with JWT signing key causes "wrong jwt" on Filer UI
- Solution: remove security.toml, use simple s3.json config without signing key

### AWS CLI v2.36 + Python 3.14 bug
`expected string or bytes-like object, got 'NoneType'` with non-AWS S3 endpoints. Use rclone or MinIO client (`mc`) instead.

### Group membership needs nginx restart
`usermod -aG` + `systemctl reload nginx` is NOT enough. Must `systemctl restart nginx` for group changes to take effect (workers keep old groups until restarted).

## Port Convention

| Range | Purpose |
|-------|---------|
| 7000–8000 | Self-hosted apps (AdGuard, Portainer) |
| 8000–9000 | Personal projects (Gateway, Keycloak) |
| Default ports | Databases (Postgres 5432, Valkey 6379, MongoDB 27017) |

## Docker Network Pattern

Create one shared network for databases:
```bash
docker network create db-network
```

In every compose file:
```yaml
networks:
  shared-network:
    external: true
    name: db-network
```

Apps connect to databases by container name: `postgres://user@local-postgres:5432/db`

## Nginx Subdomain Template

```nginx
server {
    server_name service.domain.com;
    location / {
        proxy_pass http://127.0.0.1:PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable: `sudo ln -s /etc/nginx/sites-available/service.conf /etc/nginx/sites-enabled/ && sudo nginx -t && sudo systemctl reload nginx`

## References

- `references/cloudflare-tunnel-setup.md` — install, config, service setup, pitfalls
- `references/rclone-onedrive-setup.md` — OAuth token flow, drive_id, usage commands

## Public vs Private Decision

| Service has... | Route via |
|----------------|----------|
| Its own auth (login page) | Cloudflare Tunnel (public) |
| No auth | Tailscale only (private) |
| Database | SSH tunnel (localhost binding) |
| S3 API | Cloudflare (credentials in code) |
