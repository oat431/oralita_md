---
name: homelab-infra-setup
description: Set up a homelab server from bare metal — SSH hardening, UFW, fail2ban, Docker, Tailscale, Cloudflare Tunnel, Nginx reverse proxy. Works on Ubuntu LTS.
triggers:
  - "set up a homelab server"
  - "configure a new server"
  - "harden SSH"
  - "set up cloudflare tunnel"
  - "set up tailscale on server"
  - "reverse proxy with nginx"
  - "bare metal server setup"
  - "set up database containers"
  - "docker compose for databases"
  - "seaweedfs setup"
  - "rclone onedrive backup"
  - "adguard home setup"
  - "homelab audit"
---

# Homelab Infrastructure Setup

Complete server setup from bare metal to production-ready. Designed for Ubuntu LTS (tested on 24.04 and 26.04).

## Execution Order

Execute in this exact order. Each step depends on the previous.

### 1. SSH Key Setup

```bash
# On local machine
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keygen -t ed25519 -C "label@server" -f ~/.ssh/id_homelab -N ""
ssh-copy-id -i ~/.ssh/id_homelab user@server-ip
ssh -o BatchMode=yes user@server-ip "echo ok"
```

**Pitfall:** On Windows Git Bash, ed25519 keys with passphrases fail to sign (`we did not send a packet`). Use RSA or generate ed25519 without passphrase (`-N ""`) for automation.

**Pitfall:** If `ssh-copy-id` fails with stdin issues, use:
```bash
PUB_KEY=$(cat ~/.ssh/id_homelab.pub)
ssh user@server "echo '$PUB_KEY' >> ~/.ssh/authorized_keys"
```

**Pitfall:** After reinstalling a server, old host keys block SSH. Fix: `ssh-keygen -R <server-ip>`

### 2. Enable Passwordless Sudo (for automation)

```bash
# On the server
echo 'user ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/user
```

Revoke later: `sudo rm /etc/sudoers.d/user`

### 3. SSH Hardening

```bash
sudo tee /etc/ssh/sshd_config.d/hardened.conf > /dev/null << 'EOF'
PasswordAuthentication no
PermitRootLogin no
AllowUsers youruser
EOF
sudo systemctl restart sshd
```

### 4. UFW Firewall

```bash
sudo apt update && sudo apt install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
echo 'y' | sudo ufw enable
```

### 5. Fail2ban

```bash
sudo apt install -y fail2ban
sudo systemctl enable --now fail2ban
```

### 6. Docker

```bash
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

ARCH=$(dpkg --print-architecture)
CODENAME=$(. /etc/os-release && echo $VERSION_CODENAME)
echo "deb [arch=$ARCH signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $CODENAME stable" | sudo tee /etc/apt/sources.list.d/docker.list

sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo groupadd docker 2>/dev/null
sudo usermod -aG docker user
```

**Pitfall:** The repo line must use the actual codename (e.g., `resolute` for 26.04). When running via SSH, variable expansion can break — write the line in a separate SSH command, not inline with escaping.

### 7. Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up  # prints auth URL — user clicks it
sudo systemctl enable tailscaled
```

Tailscale assigns a stable IP per device (100.x.x.x). Doesn't change on reboot, ISP change, or server move.

### 8. Cloudflare Tunnel

```bash
# Install binary directly (apt repo may not have newest Ubuntu)
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /tmp/cloudflared
sudo install -m 755 /tmp/cloudflared /usr/local/bin/cloudflared

# Authenticate
cloudflared tunnel login  # prints URL — user clicks it, selects domain

# Create tunnel
cloudflared tunnel create homelab

# Configure
cat > ~/.cloudflared/config.yml << EOF
tunnel: <tunnel-id>
credentials-file: /home/user/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: '*.yourdomain.com'
    service: http://localhost:80
  - hostname: yourdomain.com
    service: http://localhost:80
  - service: http_status:404
EOF

# Route DNS
cloudflared tunnel route dns homelab '*.yourdomain.com'
cloudflared tunnel route dns homelab yourdomain.com

# Install as service
sudo mkdir -p /etc/cloudflared
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/
sudo cp ~/.cloudflared/<tunnel-id>.json /etc/cloudflared/
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```

**Pitfall:** `cloudflared tunnel route dns` fails if a conflicting DNS record already exists. Delete old A/CNAME records first.

**Pitfall:** `cloudflared service install` can't find config if it's only in `~/.cloudflared/`. Copy to `/etc/cloudflared/` first.

**Pitfall:** Cloudflare's apt repo may not have packages for newest Ubuntu releases. Use direct binary download instead.

### 9. Nginx Reverse Proxy

```bash
sudo apt install -y nginx
sudo systemctl enable --now nginx

# Hide version
sudo sed -i 's/server_tokens build;/server_tokens off;/' /etc/nginx/nginx.conf

# Catch-all (drop unknown hosts)
sudo tee /etc/nginx/sites-available/00-catch-all > /dev/null << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 444;
}
EOF
sudo ln -sf /etc/nginx/sites-available/00-catch-all /etc/nginx/sites-enabled/00-catch-all
sudo rm -f /etc/nginx/sites-enabled/default

# Per-service config template
sudo tee /etc/nginx/sites-available/service.panomete.com > /dev/null << 'EOF'
server {
    server_name service.panomete.com;
    location / {
        proxy_pass http://127.0.0.1:PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
sudo ln -sf /etc/nginx/sites-available/service.panomete.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

No DNS changes needed — `*.domain.com` wildcard already points to tunnel.

## Adding a New Subdomain (Nginx + Cloudflare Tunnel)

No DNS changes needed — `*.domain.com` wildcard already points to tunnel. Just add Nginx config:

```bash
sudo tee /etc/nginx/sites-available/service.domain.com > /dev/null << 'EOF'
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
EOF
sudo ln -sf /etc/nginx/sites-available/service.domain.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### HTTPS services (e.g., Portainer on 9443)

When a service runs on HTTPS internally with a self-signed cert:

```nginx
server {
    server_name container.panomete.com;
    location / {
        proxy_pass https://127.0.0.1:7001;
        proxy_ssl_verify off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Pitfall:** "Client sent an HTTP request to an HTTPS server" → service expects HTTPS but Nginx sends HTTP. Change `proxy_pass` to `https://` and add `proxy_ssl_verify off`.

## AdGuard Home / Pi-hole DNS Setup

### Port 53 conflict with systemd-resolved

```bash
sudo systemctl disable --now systemd-resolved
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf  # temporary DNS
# ... start AdGuard container ...
echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf  # point to AdGuard
```

### Docker port binding for LAN-wide DNS

```yaml
ports:
  - "127.0.0.1:7000:3000"   # web UI — localhost only
  - "0.0.0.0:53:53/tcp"     # DNS — open for LAN (router can reach it)
  - "0.0.0.0:53:53/udp"     # DNS — open for LAN
```

Web UI on localhost (via Nginx). DNS on `0.0.0.0` so router/devices can use it. Safe behind NAT.

### Router DNS

Point router's **DHCP DNS** (not Static DNS) to server LAN IP. All devices get ad blocking automatically.

## Key Architecture

```
Public (anyone)    → Cloudflare Tunnel → Nginx → service
Private (you only) → Tailscale → direct access (SSH, game servers, admin UIs)
```

- Cloudflare handles TLS at edge — no certbot needed
- Nginx only receives HTTP on localhost
- All services bind to `127.0.0.1` — only accessible via Nginx
- Tailscale for SSH/management — no public IP needed
- Wildcard `*.domain.com` in tunnel config — no per-subdomain DNS changes
- Cloudflare Tunnel is **HTTP/HTTPS only** — TCP/UDP (game servers) go through Tailscale

## Security: Public vs Private Access

| Expose publicly (Cloudflare) | Tailscale only (private) |
|-----------------------------|--------------------------|
| Web apps, blog, resume | SSH, Portainer, AdGuard UI |
| API gateway | Database UIs (SeaweedFS Filer, pgAdmin) |
| S3 API (has credentials) | Grafana, monitoring dashboards |

**Rule:** If it has admin access or no auth → Tailscale only.

## Database Stack (2026+)

| Use case | Recommended | Notes |
|----------|-------------|-------|
| Relational | **PostgreSQL 18** | jsonb, full-text search, extensions |
| Caching/Sessions | **Valkey 9** | Open-source Redis fork. Redis changed licensing 2024. |
| Object Storage | **SeaweedFS 4.x** | S3-compatible, Apache 2.0. MinIO is now AGPL. |
| Document DB | **MongoDB 8** | Only if needed. PostgreSQL jsonb covers most cases. |

### Shared database network

```bash
docker network create db-network
```

```yaml
# Every database and app compose
networks:
  shared-network:
    external: true
    name: db-network
```

Apps connect by container name: `postgres://user:pass@local-postgres:5432/db`

### SeaweedFS S3 gateway pitfall

v4.x changed the flag: `-master=master:9333` → `-filer=filer:8888`:
```yaml
command: s3 -port=8333 -filer=filer:8888 -config=/etc/seaweedfs/s3.json
```

## rclone OneDrive (Headless Server)

Run `rclone authorize "onedrive"` on your **local PC**, paste token to server.

**Pitfall:** v1.74+ requires `drive_id`. Fetch it:
```bash
curl -s -H "Authorization: Bearer <token>" 'https://graph.microsoft.com/v1.0/me/drive' | grep '"id"'
```
Add `drive_id` and `drive_type = personal` to `~/.config/rclone/rclone.conf`.

## Port Convention

| Range | Purpose |
|-------|---------|
| 7000-8000 | Self-hosted apps (AdGuard, Portainer) |
| 8000-9000 | Personal projects (Gateway, Keycloak) |
| Default | Databases (Postgres 5432, Valkey 6379, MongoDB 27017, SeaweedFS 8333/9333/8888) |

## Pitfalls

- **Port 53 conflict with systemd-resolved:** If running AdGuard/Pi-hole, disable systemd-resolved first and set temporary DNS before starting the container.
- **Docker group not active immediately:** User must log out and back in (or start new SSH session) for `docker` group to take effect.
- **server_tokens sed pattern:** Ubuntu 26.04 ships `server_tokens build;` not `server_tokens off;`. The sed pattern must match the actual line.
- **Host key mismatch after reinstall:** Old host keys in `known_hosts` block SSH after server reinstall. Fix: `ssh-keygen -R <server-ip>` before connecting.
- **Nginx HTTPS proxy:** Services on HTTPS (Portainer, etc.) need `proxy_pass https://` + `proxy_ssl_verify off`. Missing this gives "HTTP request to HTTPS server" error.
- **DNS binding for LAN access:** AdGuard/Pi-hole DNS must bind to `0.0.0.0:53` (not `127.0.0.1`) for LAN devices to reach it. Web UI stays on localhost.
- **Admin UIs exposed publicly:** SeaweedFS Filer/Master, Portainer, AdGuard have no auth or weak auth. Don't put Nginx configs for these — access via Tailscale only.
- **Nginx `restart` vs `reload`:** Group membership changes (e.g., `usermod -aG user www-data`) require `systemctl restart nginx`, not `reload`. Workers keep old groups until restarted.
- **Nginx static files in home dir:** Home dirs are 750. Nginx (www-data) can't read them. Fix: `sudo usermod -aG user www-data` + `chmod -R g+rX /path/` + `sudo systemctl restart nginx`.
