# Public vs Private Access

> Which services are public (Cloudflare) vs private (Tailscale).
> Last updated: 2026-07-20

---

## Public — Cloudflare Tunnel (anyone can access)

| Service | Subdomain | Auth |
|---------|-----------|------|
| Profile site | `panomete.com` | — |
| API Gateway | `gateway.panomete.com` | — |
| S3 API | `s3.panomete.com` | S3 credentials required |
| AdGuard | `adguard.panomete.com` | AdGuard admin password |
| Portainer | `container.panomete.com` | Portainer admin password |

## Private — Tailscale only

| Service | URL | Notes |
|---------|-----|-------|
| SSH | `100.73.143.25:22` | Key auth only |
| SeaweedFS Filer | `100.73.143.25:8888` | No auth — don't expose |
| SeaweedFS Master | `100.73.143.25:9333` | No auth — don't expose |
| Databases | `localhost:5432/6379/27017` | SSH tunnel through Tailscale |

## Rule of Thumb

| If the service... | Access via |
|-------------------|-----------|
| Has its own auth (login page) | Cloudflare Tunnel (public) |
| Has no auth | Tailscale only (private) |
| Is a database | SSH tunnel (localhost binding) |
| Is an S3 API | Cloudflare (credentials in code) |

## How to make a service private

Remove Nginx config from `sites-enabled`:
```bash
sudo rm /etc/nginx/sites-enabled/service.conf
sudo nginx -t && sudo systemctl reload nginx
```

Access via Tailscale: `http://100.73.143.25:PORT`

## How to open a port for Tailscale only

```bash
sudo ufw allow from 100.73.0.0/16 to any port PORT comment 'Service - Tailscale only'
```
