# Portainer

> Docker management web UI.
> Last updated: 2026-07-20

---

## Setup

| Item | Value |
|------|-------|
| Image | `portainer/portainer-ce:lts` |
| Container | `portainer` |
| Port | `0.0.0.0:7001` → container `9443` (HTTPS) |
| Network | `portainer_network` |

## Access

| Method | URL |
|--------|-----|
| Public | `https://container.panomete.com` |
| Tailscale | `https://100.73.143.25:7001` |

⚠️ Runs on **HTTPS** (self-signed cert). Nginx config needs `proxy_pass https://` + `proxy_ssl_verify off`.

## Nginx Config

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
