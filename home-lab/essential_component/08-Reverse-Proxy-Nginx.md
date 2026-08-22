# 08 — Reverse Proxy (Nginx)

> Single entry point for all services. Routes by subdomain.

---

## Step 1: Install Nginx

```bash
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

## Step 2: Create a site config

```bash
sudo nano /etc/nginx/sites-available/gateway.panomete.com
```

```nginx
server {
    server_name gateway.panomete.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Step 3: Enable the site

```bash
sudo ln -s /etc/nginx/sites-available/gateway.panomete.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

| Command | What it does |
|---------|-------------|
| `ln -s` | Creates a symbolic link in `sites-enabled` — Nginx only reads configs from this directory |
| `nginx -t` | Tests the config for syntax errors before applying. Always run this before reload |
| `systemctl reload nginx` | Applies the new config without dropping connections (graceful reload) |

**Why:** Nginx sits behind Cloudflare Tunnel. All services bind to `127.0.0.1` — Nginx routes traffic by subdomain. One config file per service.
