# 10 — Monitoring

> Uptime Kuma + Beszel for service health and metrics.

---

## Uptime Kuma (Service Health)

### Step 1: Create compose file

```bash
mkdir -p ~/application/uptime-kuma
nano ~/application/uptime-kuma/compose.yml
```

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - "127.0.0.1:3001:3001"
    volumes:
      - uptime-kuma-data:/app/data

volumes:
  uptime-kuma-data:
```

### Step 2: Start

```bash
cd ~/application/uptime-kuma
docker compose up -d
```

### Step 3: Access

Visit `http://192.168.1.121:3001` (or set up Nginx + Cloudflare Tunnel for `status.panomete.com`)

---

## Beszel (System Metrics)

### Step 1: Create compose file

```bash
mkdir -p ~/application/beszel
nano ~/application/beszel/compose.yml
```

```yaml
services:
  beszel:
    image: henrygd/beszel:latest
    container_name: beszel
    restart: unless-stopped
    ports:
      - "127.0.0.1:8090:8090"
    volumes:
      - beszel-data:/beszel_data

volumes:
  beszel-data:
```

### Step 2: Start

```bash
cd ~/application/beszel
docker compose up -d
```

**Why:** Uptime Kuma monitors service availability and sends alerts (Telegram/Discord/email) when something goes down. Beszel tracks CPU, RAM, disk, and network metrics over time.

_(TODO: Complete with alerting setup)_
