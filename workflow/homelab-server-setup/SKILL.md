---
name: homelab-server-setup
description: Setting up and managing a homelab server — SSH hardening, Docker, Cloudflare Tunnel, Tailscale, Nginx reverse proxy, database containers, and service deployment patterns.
triggers:
  - homelab setup
  - server setup
  - cloudflare tunnel
  - tailscale
  - nginx reverse proxy
  - docker compose for databases
  - self-hosted services
---

# Homelab Server Setup

Patterns for building a production-ready homelab from scratch. Covers the full stack: SSH, firewall, Docker, networking, reverse proxy, tunnels, databases, and object storage.

## Architecture: No Public IP

```
Public (anyone)    → Cloudflare Tunnel → Nginx (:80) → service
Private (you only) → Tailscale → direct access or SSH tunnel
```

- Cloudflare Tunnel handles HTTP/HTTPS only — no TCP/UDP
- Tailscale handles everything else (SSH, game servers, custom ports)
- DNS: `*.domain.com` wildcard CNAME to tunnel — no per-subdomain DNS setup needed

## SSH on Windows (Git Bash/MSYS2)

### Password auth via SSH_ASKPASS

When `sshpass` isn't available on Windows Git Bash:

```bash
# Create password script
cat > /tmp/ssh_pass.sh << 'SCRIPT'
#!/bin/bash
echo 'yourpassword'
SCRIPT
chmod +x /tmp/ssh_pass.sh

# Connect
SSH_ASKPASS=/tmp/ssh_pass.sh SSH_ASKPASS_REQUIRE=force DISPLAY=:0 \
  ssh -o StrictHostKeyChecking=no user@server "command"
```

⚠️ **Clean up the password file after use.**

### Ed25519 key signing failure on Windows

Windows Git Bash (OpenSSH 9.x) can fail with ed25519 keys — server "accepts key" but then "we did not send a packet, disable method". RSA keys work fine. Use RSA for automation keys on Windows:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_homelab -N ""
```

### Host key mismatch after OS reinstall

```bash
ssh-keygen -R <server-ip>
ssh -o StrictHostKeyChecking=accept-new user@server "echo ok"
```

## Nginx Reverse Proxy Pitfalls

### HTTP vs HTTPS proxy_pass

Check if the backend uses HTTP or HTTPS **before** writing the config:

```nginx
# HTTP services (most: SeaweedFS, AdGuard, custom apps)
proxy_pass http://127.0.0.1:PORT;

# HTTPS services (Portainer on 9443, Keycloak on 8443)
proxy_pass https://127.0.0.1:PORT;
proxy_ssl_verify off;  # self-signed certs
```

**Common mistake:** Using `https://` for HTTP services → "Client sent an HTTP request to an HTTPS server"

### Static files from /home/ — permission denied

Nginx runs as `www-data`, home dirs are `750`:

```bash
sudo usermod -aG flowero www-data
chmod -R g+rX /home/flowero/path/to/site/
sudo systemctl restart nginx  # MUST restart, not reload (group change)
```

⚠️ `systemctl reload` is NOT enough after `usermod -aG` — workers keep old group memberships until restarted.

### server_tokens off

Default is `server_tokens build` (shows version). Fix:

```bash
sudo sed -i 's/server_tokens build;/server_tokens off;/' /etc/nginx/nginx.conf
```

### Catch-all for unknown hosts

```nginx
server {
    listen 80 default_server;
    server_name _;
    return 444;  # drop connection
}
```

## Admin Panel Security

**Rule:** Admin UIs without built-in auth should NOT be exposed via Cloudflare Tunnel.

| Public (Cloudflare) | Private (Tailscale only) |
|---------------------|--------------------------|
| Blog, resume, API | Portainer, AdGuard |
| S3 API (has creds) | SeaweedFS Filer/Master |
| Keycloak | Database admin UIs |

For admin panels accessed via Tailscale, either:
1. SSH tunnel: `ssh -L PORT:localhost:PORT flowero@100.x.x.x`
2. Open port with UFW scoped to Tailscale: `sudo ufw allow from 100.73.0.0/16 to any port PORT`

## Docker Database Compose Pattern

All databases share one external network:

```bash
docker network create db-network
```

```yaml
# In every database/app compose file
networks:
  shared-network:
    external: true
    name: db-network
```

Apps connect by container name: `postgres://user:pass@local-postgres:5432/db`

⚠️ **Always check latest image versions** before deploying. Use Docker Hub API:
```bash
curl -s "https://hub.docker.com/v2/repositories/library/postgres/tags/?page_size=5&ordering=last_updated&name=18" | python3 -c "import sys,json; [print(r['name']) for r in json.load(sys.stdin)['results']]"
```

## SeaweedFS v4.40 Configuration

### S3 gateway flag change

v4.40 changed `-master` to `-filer` for the S3 command:
```yaml
# Old (broken)
command: s3 -port=8333 -master=master:9333
# New (correct)
command: s3 -port=8333 -filer=filer:8888
```

### IAM signing key required

v4.40 requires `security.toml` with JWT signing keys. Without it: "Failed to load IAM configuration: no signing key found for STS service"

Create `security.toml`:
```toml
[jwt.filer_signing]
key = "your-signing-key"
[jwt.filer_signing.read]
key = "your-signing-key"
[jwt.signing]
key = "your-signing-key"
```

Mount in both filer and s3 containers:
```yaml
volumes:
  - ./security.toml:/etc/seaweedfs/security.toml:ro
```

### Filer gRPC port

S3 gateway needs filer's gRPC port (18888) accessible. If S3 shows "connection refused" to filer:18888, ensure the filer container exposes it (Docker internal networking handles this if on the same compose network).

## Cloudflare Tunnel Setup (headless server)

```bash
# Install binary directly (when apt repo doesn't support OS version)
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /tmp/cloudflared
sudo install -m 755 /tmp/cloudflared /usr/local/bin/cloudflared

# Auth (gives URL for browser)
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create homelab

# Configure ~/.cloudflared/config.yml
# Route DNS
cloudflared tunnel route dns homelab "*.domain.com"

# Install as systemd service
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/
sudo cp ~/.cloudflared/<tunnel-id>.json /etc/cloudflared/
sudo cloudflared service install
sudo systemctl enable cloudflared
```

⚠️ `cloudflared service install` looks for config in `/etc/cloudflared/`, not `~/.cloudflared/`. Copy files there first.

## rclone OneDrive (headless server)

The OAuth flow requires running `rclone authorize "onedrive"` on a machine with a browser (your PC), then copying the token to the server.

**Critical:** The token alone isn't enough. You also need `drive_id`:

```bash
curl -s -H "Authorization: Bearer ACCESS_TOKEN" \
  'https://graph.microsoft.com/v1.0/me/drive' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])"
```

Config format:
```ini
[onedrive]
type = onedrive
token = {"access_token":"...","refresh_token":"...","expiry":"..."}
drive_id = XXXXXXXXXXXX
drive_type = personal
```

⚠️ Without `drive_id`, rclone v1.74+ fails with "unable to get drive_id and drive_type"
