# Nginx Proxy Patterns

Three patterns for proxying services behind Nginx + Cloudflare Tunnel.

## 1. HTTP Service (most services)

For services that listen on plain HTTP (e.g., Uptime Kuma, Grafana, custom apps).

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

## 2. HTTPS Service (self-signed cert)

For services that run HTTPS internally with self-signed certs (e.g., Portainer on 9443, Keycloak on 8443).

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

**Why `proxy_ssl_verify off`?** The service uses a self-signed cert. Without this directive, Nginx rejects the cert and returns 502.

## 3. Static Files

For serving HTML/CSS/JS sites directly from the filesystem.

```nginx
server {
    server_name site.domain.com;

    root /home/user/path/to/site;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**PITFALL: Permission denied when files are in /home/**

Nginx runs as `www-data`. Home directories are `750` (owner-only). Nginx returns 403 or 404 silently.

```bash
# Fix: grant www-data access to the user's files
sudo usermod -aG <user> www-data
chmod -R g+rX /home/<user>/path/to/site/

# MUST restart (not reload) — group membership changes need full worker restart
sudo systemctl restart nginx
```

**Alternative:** Copy files to `/var/www/` instead:
```bash
sudo cp -r /home/user/site /var/www/mysite
sudo chown -R www-data:www-data /var/www/mysite
```

## Enabling a Site

```bash
# Create config
sudo nano /etc/nginx/sites-available/service.domain.com

# Enable (symlink)
sudo ln -s /etc/nginx/sites-available/service.domain.com /etc/nginx/sites-enabled/

# Test and apply
sudo nginx -t && sudo systemctl reload nginx
```

## Disabling a Site

```bash
sudo rm /etc/nginx/sites-enabled/service.domain.com
sudo nginx -t && sudo systemctl reload nginx
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Client sent HTTP request to HTTPS server` | Service runs HTTPS, config uses `http://` | Change to `proxy_pass https://` + `proxy_ssl_verify off` |
| `403 Forbidden` on static files | Nginx can't read files in /home/ | `usermod -aG` + `chmod -R g+rX` + restart |
| `404 Not Found` on static files (file exists) | Same — permission issue | Same fix |
| `502 Bad Gateway` | Service not running or wrong port | Check `docker ps` and port mapping |
| `conflicting server name` warning | Duplicate config for same domain | Remove duplicate from sites-enabled |
