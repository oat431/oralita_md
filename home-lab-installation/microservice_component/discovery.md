# Flowero Discover

> Eureka Service Registry for the Panomete Platform.
> Last updated: 2026-07-24

---

## Deployment Status

> **Deployed:** 2026-07-23 | **Verified:** Healthy
>
> - Container: `flowero-discover` — Up, healthy
> - Health: `status: UP`
> - Dashboard: `https://discovery.panomete.com` — HTTP 200
> - Registry API: `http://localhost:8999/eureka/apps` — working
> - Registered services: `FLOWERO-GATE` (1 instance)

---

## What & Why

Flowero Discover is the **service registry** — every microservice registers itself on startup, and services discover each other by logical name instead of hardcoded URLs. It runs Spring Cloud Netflix Eureka in standalone mode.

- Gate resolves `lb://cute-gufo` → queries Eureka → gets `host:port`
- Services register on boot, send heartbeats every 30s
- Dead instances evicted after 90s of missed heartbeats
- Self-preservation mode keeps the registry intact during network hiccups

---

## Setup

**Compose:** `/home/flowero/platform/docker-compose.platform.yml`

| Item | Value |
|------|-------|
| Image | `platform-flowero-discover:latest` (built from source) |
| Container | `flowero-discover` |
| Port (REST API) | `127.0.0.1:8999` |
| Port (Dashboard) | `127.0.0.1:3999` (maps to container 8999) |
| Network | `db-network` |
| Domain | `discovery.panomete.com` (via Nginx) |
| Database | None — fully in-memory |
| Mode | Standalone (single node) |

> Both host ports 8999 and 3999 map to container port 8999. The dashboard and REST API run on the same Eureka port — the dual-port is a Docker port-mapping convention so Nginx can proxy `discovery.panomete.com` → `:3999` while services register on `:8999`.

---

## Prerequisites

- Docker + Compose installed
- `db-network` exists (`docker network ls | grep db-network`)
- Nginx running
- Cloudflare tunnel active (`*.panomete.com` wildcard)
- Ports 8999 and 3999 free

---

## Deploy

### Step 1: Clone the repository

```bash
cd /home/flowero/platform
git clone https://github.com/oat431/flowero-discovery.git flowerodiscovery
```

### Step 2: Add Nginx server block

```bash
sudo tee /etc/nginx/sites-available/discovery.panomete.com > /dev/null << 'NGINX'
server {
    server_name discovery.panomete.com;

    location / {
        proxy_pass http://127.0.0.1:3999;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/discovery.panomete.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

> No DNS changes needed — `*.panomete.com` wildcard already routes to the Cloudflare tunnel.

### Compose service definition (actual deployed config)

```yaml
  flowero-discover:
    build:
      context: ./flowerodiscovery
      dockerfile: Dockerfile
    container_name: flowero-discover
    ports:
      - "127.0.0.1:8999:8999"   # BE: REST API for service registration / discovery
      - "127.0.0.1:3999:8999"   # FE: Dashboard (Nginx proxies discovery.panomete.com → :3999)
    networks:
      - shared-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8999/actuator/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
    restart: unless-stopped
```

> **Note:** The Dockerfile must install `curl` for the healthcheck to work. See Troubleshooting below.

### Step 4: Build and deploy

```bash
cd /home/flowero/platform
docker compose -f docker-compose.platform.yml up -d --build flowero-discover
```

> First build takes ~60 seconds (Gradle dependency download + compile). Subsequent builds are faster due to Docker layer caching.

### Step 5: Verify

```bash
# Wait for startup
sleep 30

# Health check
curl -sf http://localhost:8999/actuator/health && echo " ✅"

# Dashboard (internal)
curl -sf -o /dev/null -w '%{http_code}' http://localhost:3999/ && echo " ✅"

# Dashboard (external)
curl -sf -o /dev/null -w '%{http_code}' https://discovery.panomete.com/ && echo " ✅"

# Registry API
curl -sf -H 'Accept: application/json' http://localhost:8999/eureka/apps | python3 -c "import sys,json; d=json.load(sys.stdin); print('services:', len(d.get('applications',{}).get('application',[])))"
```

---

## Access

| Resource | URL |
|----------|-----|
| Dashboard | `https://discovery.panomete.com` |
| Health | `http://localhost:8999/actuator/health` |
| Registry API | `http://localhost:8999/eureka/apps` |
| Specific service | `http://localhost:8999/eureka/apps/{SERVICE-NAME}` |

---

## Common Commands

```bash
# Health check
curl -sf http://localhost:8999/actuator/health

# List registered services (JSON)
curl -sf -H 'Accept: application/json' http://localhost:8999/eureka/apps

# List registered services (XML — Eureka default)
curl -sf http://localhost:8999/eureka/apps

# View logs
docker logs -f flowero-discover

# Restart
cd ~/platform && docker compose -f docker-compose.platform.yml restart flowero-discover

# Force deregister a stale service
curl -X DELETE http://localhost:8999/eureka/apps/{SERVICE-NAME}/{INSTANCE-ID}
```

---

## Configuration

Key settings in `src/main/resources/application.yaml`:

| Property | Value | Why |
|----------|-------|-----|
| `server.port` | `8999` | REST API port |
| `eureka.client.register-with-eureka` | `false` | Standalone — don't self-register |
| `eureka.client.fetch-registry` | `false` | Standalone — don't fetch from self |
| `eureka.server.enable-self-preservation` | `true` | Keeps registry intact during network hiccups |
| `eureka.server.eviction-interval-timer-in-ms` | `5000` | Evict dead instances every 5s |
| `eureka.server.renewal-percent-threshold` | `0.85` | Self-preservation triggers below 85% heartbeats |

---

## Troubleshooting

### Container shows "unhealthy" in Portainer

**Cause:** The health check uses `curl` but it's not installed in the `eclipse-temurin:25-jre-noble` image.

**Verify:**
```bash
docker exec flowero-discover which curl
# If "not found" → curl is missing
```

**Fix:** Add `curl` to the Dockerfile runtime stage:
```dockerfile
FROM eclipse-temurin:25-jre-noble
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
```

Then rebuild:
```bash
cd ~/platform
docker compose -f docker-compose.platform.yml up -d --build flowero-discover
```

> The service itself is fine — only the health check was broken. The container was running and serving requests normally.

### 502 Bad Gateway on `discovery.panomete.com`

**Most common cause:** Container not running or port not bound.

```bash
# Check container
docker ps | grep flowero-discover

# Check port binding
ss -tlnp | grep -E '8999|3999'

# Check internal response
curl -sf http://localhost:3999/ -o /dev/null -w '%{http_code}'

# Check Nginx
sudo nginx -t
curl -sf -H 'Host: discovery.panomete.com' http://localhost -o /dev/null -w '%{http_code}'
```

### Dashboard shows no services

**Cause:** No services have registered yet, or services are configured to register with a different Eureka URL.

```bash
# Check registry directly
curl -sf -H 'Accept: application/json' http://localhost:8999/eureka/apps | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d, indent=2))"

# If services should be registered but aren't:
# 1. Check if the service container is running
docker ps | grep -E 'flowero-gate|flowero-guard'

# 2. Check service logs for Eureka registration errors
docker logs flowero-gate 2>&1 | grep -i "eureka\|discovery\|register"
```

### Self-preservation mode activated

**Symptom:** Dashboard shows red warning "EMERGENCY! EUREKA MAY BE INCORRECTLY CLAIMING INSTANCES ARE UP WHEN THEY'RE NOT."

**Cause:** Eureka sees a sudden drop in heartbeats (e.g., mass restart, network partition). This is **by design** — it prevents cascading failures.

**Fix:**
1. This is expected behavior — do NOT panic
2. Verify all expected services are actually running
3. Heartbeats will resume and self-preservation will auto-disable
4. If truly stale: force deregister specific instances (see Common Commands)

### Container OOM killed

**Symptom:** `docker ps` shows `Exited (137)`.

```bash
# Check if OOM killed
docker inspect flowero-discover --format '{{.State.OOMKilled}}'

# Increase memory in compose (current: 256MB)
# Add under flowero-discover service:
#   deploy:
#     resources:
#       limits:
#         memory: 384M

# Restart
docker compose -f docker-compose.platform.yml up -d flowero-discover
```

### Build fails — Gradle dependency timeout

```bash
# Retry the build
cd ~/platform
docker compose -f docker-compose.platform.yml build --no-cache flowero-discover

# If persistent, check DNS inside the build container
docker run --rm eclipse-temurin:25-jdk-noble nslookup repo.maven.apache.org
```

### Eureka REST API returns XML instead of JSON

**Cause:** Eureka defaults to XML. Always send `Accept: application/json` header.

```bash
# Wrong (returns XML)
curl http://localhost:8999/eureka/apps

# Right (returns JSON)
curl -H 'Accept: application/json' http://localhost:8999/eureka/apps
```

---

## Project Structure

```
flowerodiscovery/
├── build.gradle              # Gradle build (Java 25 / Boot 4.1 / Cloud 2025.1)
├── settings.gradle           # Project name
├── Dockerfile                # Multi-stage build (JDK build → JRE runtime)
├── docker-compose.fragment.yml  # Standalone compose (for reference)
├── src/
│   ├── main/
│   │   ├── java/panomete/flowerodiscovery/
│   │   │   └── FlowerodiscoveryApplication.java   # @EnableEurekaServer
│   │   └── resources/
│   │       └── application.yaml                    # Eureka config
│   └── test/
│       └── java/panomete/flowerodiscovery/
│           └── FlowerodiscoveryApplicationTests.java  # 5 integration tests
└── README.md
```

---

## Related

- [[keycloak]] — Identity provider (Guard registers health with Discover)
- [[valkey]] — Used by Gate, not Discover
- [[docker-network]] — Why `db-network` and container names matter
- [[08.1-Add-Subdomain]] — How the Nginx block works
