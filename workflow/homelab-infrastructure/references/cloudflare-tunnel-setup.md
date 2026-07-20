# Cloudflare Tunnel Setup

## Install cloudflared (when apt repo doesn't have the release)
```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /tmp/cloudflared
sudo install -m 755 /tmp/cloudflared /usr/local/bin/cloudflared
```

## Create tunnel
```bash
cloudflared tunnel login        # browser auth
cloudflared tunnel create homelab
```

## Config (`/etc/cloudflared/config.yml`)
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

## Route DNS (wildcard — covers all subdomains)
```bash
cloudflared tunnel route dns homelab '*.domain.com'
```

## Install as systemd service
```bash
sudo mkdir -p /etc/cloudflared
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/
sudo cp ~/.cloudflared/<tunnel-id>.json /etc/cloudflared/
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```

## Pitfalls
- `panomete.com` DNS record already exists → delete old A record first, then re-route
- Config file must be in `/etc/cloudflared/` for service install to find it
- Old tunnels can be deleted: `cloudflared tunnel delete <name>`
