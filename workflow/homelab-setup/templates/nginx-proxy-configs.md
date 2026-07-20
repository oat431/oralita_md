# Nginx Proxy Templates

## HTTP Service (most services)

```nginx
server {
    server_name SERVICE.panomete.com;

    location / {
        proxy_pass http://127.0.0.1:PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## HTTPS Service (Portainer, Keycloak, etc.)

```nginx
server {
    server_name SERVICE.panomete.com;

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

## Static Files

```nginx
server {
    server_name SITE.panomete.com;

    root /home/flowero/path/to/site;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## Catch-all (drops unknown hosts)

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 444;
}
```

## Enable Pattern

```bash
sudo nano /etc/nginx/sites-available/SERVICE.panomete.com
# paste config above
sudo ln -s /etc/nginx/sites-available/SERVICE.panomete.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

## Cloudflare Tunnel Note

No additional config needed for new subdomains — the wildcard `*.domain.com` in the tunnel config catches everything. Just add the Nginx config.
