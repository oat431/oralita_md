---
name: homelab-setup
description: "Set up homelab server infrastructure from scratch — SSH hardening, UFW, Docker, Tailscale, Cloudflare Tunnel, Nginx reverse proxy, DNS, backups."
triggers:
  - "homelab setup"
  - "server setup"
  - "new server"
  - "infrastructure from scratch"
  - "self-hosted"
---

# Homelab Setup

Complete homelab server setup from a fresh Ubuntu install. Designed for servers with no public IP — uses Cloudflare Tunnel for web services and Tailscale for management/game servers.

## Architecture

```
Public (anyone)    → Cloudflare Tunnel → Nginx → service
Private (you only) → Tailscale → direct access
```

| Service Type | Access Method |
|-------------|--------------|
| Web apps (HTTP/HTTPS) | Cloudflare Tunnel → Nginx → service |
| SSH / management | Tailscale |
| Game servers / custom TCP/UDP | Tailscale (direct connection) |

## Steps (execute in order)

### 1. SSH Key Setup

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keygen -t ed25519 -C "label" -f ~/.ssh/id_homelab -N ""
ssh-copy-id -i ~/.ssh/id_homelab user@server-ip
ssh -o BatchMode=yes user@server-ip "echo ok"
```

Then enable passwordless sudo (on server):
```bash
echo 'user ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/user
```

⚠️ **Windows/Git Bash pitfall:** ed25519 keys with passphrases fail silently — "Server accepts key" then "we did not send a packet, disable method". Use `-N ""` (no passphrase) for automation keys, or use RSA: `ssh-keygen -t rsa -b 4096`.

⚠️ **SSH_ASKPASS for scripted SSH:** On Windows MINGW64, use:
```bash
cat > /tmp/ssh_pass.sh << 'SCRIPT'
#!/bin/bash
echo 'password'
SCRIPT
chmod +x /tmp/ssh_pass.sh
SSH_ASKPASS=/tmp/ssh_pass.sh SSH_ASKPASS_REQUIRE=force DISPLAY=:0 ssh user@host "command" < /dev/null
```

### 2. SSH Hardening

```bash
sudo tee /etc/ssh/sshd_config.d/hardened.conf << 'EOF'
PasswordAuthentication no
PermitRootLogin no
AllowUsers flowero
EOF
sudo systemctl restart sshd
```

### 3. UFW Firewall

```bash
sudo apt install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
echo 'y' | sudo ufw enable
```

### 4. Fail2ban

```bash
sudo apt install -y fail2ban
sudo systemctl enable --now fail2ban
```

### 5. Docker + Compose

```bash
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
ARCH=$(dpkg --print-architecture)
CODENAME=$(. /etc/os-release && echo $VERSION_CODENAME)
echo "deb [arch=$ARCH signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $CODENAME stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

⚠️ New Ubuntu versions may not have Docker repo yet — check `apt-cache policy docker-ce` first.

### 6. Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up  # gives browser URL to authenticate
sudo systemctl enable tailscaled
```

### 7. Cloudflare Tunnel

Install (binary download if repo unavailable):
```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /tmp/cloudflared
sudo install -m 755 /tmp/cloudflared /usr/local/bin/cloudflared
```

Create and configure:
```bash
cloudflared tunnel login        # browser auth
cloudflared tunnel create homelab
```

Config file (`~/.cloudflared/config.yml`):
```yaml
tunnel: <tunnel-id>
credentials-file: /home/user/.cloudflared/<tunnel-id>.json
ingress:
  - hostname: '*.domain.com'
    service: http://localhost:80
  - hostname: domain.com
    service: http://localhost:80
  - service: http_status:404
```

Route DNS and install service:
```bash
cloudflared tunnel route dns homelab '*.domain.com'
cloudflared tunnel route dns homelab domain.com
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/
sudo cp ~/.cloudflared/<tunnel-id>.json /etc/cloudflared/
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```

⚠️ `cloudflared service install` looks for config in `/etc/cloudflared/`, not `~/.cloudflared/`. Copy files there first.

### 8. Nginx Reverse Proxy

```bash
sudo apt install -y nginx
sudo systemctl enable --now nginx
```

Create catch-all (drops unknown hosts):
```nginx
server {
    listen 80 default_server;
    server_name _;
    return 444;
}
```

Per-service config (HTTP):
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

Per-service config (HTTPS — e.g., Portainer, Keycloak):
```nginx
server {
    server_name service.domain.com;
    location / {
        proxy_pass https://127.0.0.1:PORT;
        proxy_ssl_verify off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Static file serving:
```nginx
server {
    server_name domain.com;
    root /home/user/path/to/site;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

⚠️ **Nginx + home directory pitfall:** Nginx runs as `www-data`. Home dirs are 750 (`drwxr-x---`). Fix:
```bash
sudo usermod -aG user www-data
chmod -R g+rX /home/user/path/
sudo systemctl restart nginx  # MUST restart, not reload — group changes need full restart
```

⚠️ **HTTPS services:** If you get "Client sent an HTTP request to an HTTPS server", change `proxy_pass http://` to `proxy_pass https://` and add `proxy_ssl_verify off`.

### 9. AdGuard Home (DNS + ad blocking)

⚠️ Port 53 conflict with `systemd-resolved`:
```bash
sudo systemctl disable --now systemd-resolved
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf  # temporary
# Start AdGuard, then: echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf
```

⚠️ DNS ports should bind to `0.0.0.0:53` for LAN access (not 127.0.0.1). Web UI stays on 127.0.0.1.

### 10. rclone OneDrive Backup

Install official version (not apt's older one):
```bash
curl -fsSL https://downloads.rclone.org/rclone-current-linux-amd64.zip -o /tmp/rclone.zip
cd /tmp && unzip rclone.zip && sudo cp rclone-*-linux-amd64/rclone /usr/local/bin/
```

⚠️ **Headless server auth pitfall:** `rclone authorize "onedrive"` gives localhost URL that's inaccessible from your PC. Run `rclone authorize "onedrive"` on your local machine (Windows/Mac), paste the token to the server config.

⚠️ **drive_id required:** Token alone isn't enough for v1.74+. Fetch drive_id:
```bash
curl -s -H "Authorization: Bearer <access_token>" 'https://graph.microsoft.com/v1.0/me/drive' | grep '"id"'
```
Then add `drive_id = <id>` and `drive_type = personal` to rclone.conf.

## Port Convention

| Range | Purpose |
|-------|---------|
| 7000-8000 | Self-hosted apps (AdGuard, Portainer) |
| 8000-9000 | Personal projects (Gateway, Keycloak) |
| Default ports | Databases (Postgres 5432, Valkey 6379, SeaweedFS 8333/9333/8888) |

## Docker Networking: Shared db-network

Create one network for all databases. Apps attach to it and connect by container name.

```bash
docker network create db-network
```

In every database and app compose file:
```yaml
networks:
  shared-network:
    external: true
    name: db-network
```

Apps connect by **container name** (not localhost):
```
postgres://user:pass@local-postgres:5432/dbname
redis://local-valkey:6379
```

No port mapping needed between containers. Port mapping (127.0.0.1:5432:5432) is only for direct host access (SSH tunnel, tools).

## Database Stack Recommendations (2026+)

| Use case | Recommended | Notes |
|----------|-------------|-------|
| Relational | **PostgreSQL 18** | jsonb for document storage, full-text search, extensions |
| Caching/Sessions | **Valkey 9** | Open-source Redis fork (Linux Foundation). Drop-in replacement. Redis changed licensing in 2024. |
| Object Storage | **SeaweedFS** | S3-compatible, Apache 2.0. Lightweight. MinIO is now AGPL with commercial restrictions. |
| Document DB | **MongoDB 8** | Only add if a specific app requires it. PostgreSQL jsonb covers most document use cases. |

## DNS Rules

- **Web services (HTTP/HTTPS):** Automatic via `*.domain.com` CNAME to tunnel. No DNS changes needed per subdomain.
- **Non-HTTP services (game servers, custom ports):** Create A record → Tailscale IP, **proxy off** (DNS only / gray cloud).
- **Tailscale IP is stable** — doesn't change on reboot, ISP change, or server move.

## Documentation Convention

The user documents all homelab setup steps in individual Obsidian files:
- Directory: `F:\obsidian_note\oralita_md\home-lab-installation\`
- Naming: `NN-Step-Title.md` (e.g., `01-SSH-Key-Setup.md`, `08.1-Add-Subdomain.md`)
- Index file: `home-lab-installation.md` with `[[wikilinks]]`
- Each file: command + flag breakdown + "why" explanation
- Audit files: `F:\obsidian_note\oralita_md\home-lab-audit\`

## Reference Files

- `references/database-stack-templates.md` — PostgreSQL, Valkey, SeaweedFS compose templates with db-network
- `references/rclone-onedrive-headless.md` — Headless auth flow, drive_id pitfall, config format
- `references/ssh-windows-pitfalls.md` — ed25519 signing, SSH_ASKPASS, paramiko issues
- `templates/nginx-proxy-configs.md` — HTTP, HTTPS, static, catch-all templates
