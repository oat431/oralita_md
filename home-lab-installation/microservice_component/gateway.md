# Flowero Gate

> API Gateway for the Panomete Platform.
> Last updated: 2026-07-24

---

## Deployment Status

> **Deployed:** 2026-07-23 | **Verified:** Healthy
>
> - Container: `flowero-gate` — Up, healthy
> - Health: `status: UP`
> - 401 rejection: Working (unauthenticated requests correctly rejected)
> - Eureka registration: `FLOWERO-GATE` — 1 instance registered
> - External access: `https://api.panomete.com` — HTTP 200
> - Routes: blog, short, todo (all `lb://` via Eureka)

---

## What & Why

Flowero Gate is the **API gateway** — all business API traffic flows through it. It handles:

- **JWT validation** — validates tokens locally using cached JWKS from Guard (zero per-request calls to Keycloak)
- **Rate limiting** — Valkey-backed, per-IP, survives restarts
- **Route resolution** — `lb://` URIs resolved via Eureka service discovery
- **Claim forwarding** — extracts `X-User-Id`, `X-User-Roles` from JWT and forwards to backends
- **Structured logging** — JSON logs with method, path, status, latency, trace ID

Gate does NOT handle:
- TLS (Cloudflare handles it)
- Foundation service routing (Guard and Discover have their own subdomains via Nginx)
- Business logic (that's the backend services' job)

---

## Setup

**Compose:** `/home/flowero/platform/docker-compose.platform.yml`

| Item | Value |
|------|-------|
| Image | `platform-flowero-gate:latest` (built from source) |
| Container | `flowero-gate` |
| Port | `127.0.0.1:8000` |
| Network | `db-network` |
| Domain | `api.panomete.com` (via Nginx) |
| Database | None — stateless |
| Dependencies | Guard (JWKS), Discover (Eureka), Valkey (rate limiting) |

---

## Prerequisites

- Docker + Compose installed
- `db-network` exists
- **Guard running** — JWKS endpoint must be reachable
- **Discover running** — Eureka registry must be available
- **Valkey running** — rate limiting backend
- Nginx configured for `api.panomete.com`
- `.env` has `VALKEY_PASSWORD`, `KEYCLOAK_GATEWAY_SECRET`, `POST_LOGIN_REDIRECT_URL`
- `flowero-gateway` OAuth2 client registered in Keycloak `panomete` realm

---

## Deploy

### Step 1: Clone the repository

```bash
cd /home/flowero/platform
git clone https://github.com/oat431/flowerogate.git flowerogate
```

### Step 2: Add Nginx server block

```bash
sudo tee /etc/nginx/sites-available/api.panomete.com > /dev/null << 'NGINX'
server {
    server_name api.panomete.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/api.panomete.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### Step 3: Verify dependencies

```bash
echo "Guard:" && curl -sf http://localhost:8001/health/ready > /dev/null && echo " ✅" || echo " ❌"
echo "Discover:" && curl -sf http://localhost:8999/actuator/health > /dev/null && echo " ✅" || echo " ❌"
echo "Valkey:" && docker exec local-valkey valkey-cli -a "$VALKEY_PASSWORD" ping 2>/dev/null && echo "" || echo " ❌"
```

### Step 4: Compose service definition

```yaml
  flowero-gate:
    build:
      context: ./flowerogate
      dockerfile: Dockerfile
    container_name: flowero-gate
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      SERVER_PORT: "8000"
      MANAGEMENT_SERVER_PORT: "8000"
      SPRING_PROFILES_ACTIVE: prod
      JWT_ISSUER_URI: https://auth.panomete.com/realms/panomete
      JWT_JWK_SET_URI: https://auth.panomete.com/realms/panomete/protocol/openid-connect/certs
      REDIS_HOST: local-valkey
      REDIS_PORT: "6379"
      REDIS_PASSWORD: ${VALKEY_PASSWORD}
      REDIS_SSL: "false"
      SPRING_AUTOCONFIGURE_EXCLUDE: org.springframework.cloud.circuitbreaker.resilience4j.Resilience4JAutoConfiguration
      EUREKA_CLIENT_ENABLED: "true"
      EUREKA_URI: http://flowero-discover:8999/eureka
      OTLP_ENABLED: "false"
      LOGGING_LEVEL_ROOT: INFO
      LOGGING_LEVEL_PANOMETE_FLOWEROGATE: DEBUG
      APP_POST_LOGIN_REDIRECT_URL: ${POST_LOGIN_REDIRECT_URL}
      KEYCLOAK_GATEWAY_SECRET: ${KEYCLOAK_GATEWAY_SECRET}
    networks:
      - shared-network
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:8000/actuator/health/liveness || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 30s
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### Step 5: Build and deploy

```bash
cd /home/flowero/platform
docker compose -f docker-compose.platform.yml up -d --build flowero-gate
```

> First build takes ~60 seconds. Subsequent builds are faster due to Docker layer caching.

### Step 6: Verify

```bash
# Wait for startup (JWKS fetch + Eureka registration)
sleep 35

# Health check
curl -sf http://localhost:8000/actuator/health && echo " ✅"

# Rejects unauthenticated requests
curl -sf -o /dev/null -w '%{http_code}' https://api.panomete.com/api/blog/posts
# Expected: 401

# Registered in Eureka
curl -sf -H 'Accept: application/json' http://localhost:8999/eureka/apps | python3 -c "import sys,json; d=json.load(sys.stdin); [print(a.get('name')) for a in d.get('applications',{}).get('application',[])]"

# External access
curl -sf -o /dev/null -w '%{http_code}' https://api.panomete.com/actuator/health
# Expected: 200
```

---

## Access

| Resource | URL |
|----------|-----|
| API base | `https://api.panomete.com` |
| Health | `http://localhost:8000/actuator/health` |
| Liveness | `http://localhost:8000/actuator/health/liveness` |
| Gateway routes | `http://localhost:8000/actuator/gateway/routes` |
| Prometheus metrics | `http://localhost:8000/actuator/prometheus` |

---

## Common Commands

```bash
# Health check
curl -sf http://localhost:8000/actuator/health

# Test 401 rejection (no token)
curl -sf -o /dev/null -w '%{http_code}' https://api.panomete.com/api/blog/posts

# View logs
docker logs -f flowero-gate

# Restart
cd ~/platform && docker compose -f docker-compose.platform.yml restart flowero-gate

# Check Eureka registration
curl -sf -H 'Accept: application/json' http://localhost:8999/eureka/apps | python3 -c "import sys,json; d=json.load(sys.stdin); [print(a.get('name')) for a in d.get('applications',{}).get('application',[])]"

# Check Valkey connection
docker exec local-valkey valkey-cli -a "$VALKEY_PASSWORD" ping
```

---

## Configuration

### Routes (application.yaml)

| Route ID | Path | Backend | Auth | Rate Limit |
|----------|------|---------|:---:|:---:|
| `blog` | `/api/blog/**` | `lb://cute-gufo` | JWT | 100/min |
| `short` | `/api/short/**` | `lb://fluffy-mouton` | JWT | 100/min |
| `todo` | `/api/todo/**` | `lb://tiny-mchwa` | JWT | 100/min |
| `fallback-404` | `/**` | `forward:/fallback/not-found` | — | — |

> Future routes (Phase 2+): `ledger`, `recipe`, `hora` — commented out in `application.yaml`

### Security

| Feature | Implementation |
|---------|---------------|
| JWT validation | OAuth2 Resource Server, local JWKS cache |
| 401 response | JSON body for API requests, redirect to Keycloak for browser |
| 403 response | JSON body for insufficient roles |
| 429 response | JSON body with rate limit details |
| CORS | `https://*.panomete.com` allowed |
| CSRF | Disabled (stateless JWT) |

### Key Environment Variables

| Variable | Source | Purpose |
|----------|--------|---------|
| `VALKEY_PASSWORD` | `.env` | Rate limiting backend auth |
| `KEYCLOAK_GATEWAY_SECRET` | `.env` | OAuth2 client secret (browser login flow) |
| `POST_LOGIN_REDIRECT_URL` | `.env` | Where to redirect after Keycloak login |
| `JWT_ISSUER_URI` | compose | Keycloak realm issuer URL |
| `EUREKA_URI` | compose | Eureka server for `lb://` resolution |

---

## Troubleshooting

### 502 Bad Gateway for all API requests

**Cause:** Backend business service not registered in Eureka.

```bash
# Check what's registered
curl -sf -H 'Accept: application/json' http://localhost:8999/eureka/apps | python3 -c "import sys,json; d=json.load(sys.stdin); [print(a.get('name')) for a in d.get('applications',{}).get('application',[])]"

# If empty or missing expected service:
# 1. Check if the business service container is running
docker ps | grep -E 'cute-gufo|fluffy-mouton|tiny-mchwa'

# 2. Check if it registered with Eureka
docker logs <service> 2>&1 | grep -i "eureka\|register"
```

> This is expected in Phase 1 — no business services are deployed yet.

### All requests return 401 (even with valid token)

**Cause:** JWKS cache stale or Guard is down.

```bash
# Check Guard health
curl -sf http://localhost:8001/health/ready

# Check JWKS endpoint
curl -sf https://auth.panomete.com/realms/panomete/protocol/openid-connect/certs | jq '.keys | length'
# Expected: 2

# Restart Gate to refresh JWKS cache
docker compose -f docker-compose.platform.yml restart flowero-gate
```

### All requests return 429 (rate limited)

**Cause:** Valkey rate limiter triggered.

```bash
# Check Valkey
docker exec local-valkey valkey-cli -a "$VALKEY_PASSWORD" ping

# Check rate limit keys
docker exec local-valkey valkey-cli -a "$VALKEY_PASSWORD" keys "request_rate_limiter*"

# Flush rate limits (for testing)
docker exec local-valkey valkey-cli -a "$VALKEY_PASSWORD" del $(docker exec local-valkey valkey-cli -a "$VALKEY_PASSWORD" keys "request_rate_limiter*" | tr '\n' ' ')
```

### Gateway won't start — JWKS fetch failed

**Cause:** Guard is down or unreachable.

```bash
# Check Guard
docker ps | grep flowero-guard
curl -sf http://localhost:8001/health/ready

# Fix Guard first, then restart Gate
docker compose -f docker-compose.platform.yml restart flowero-gate
```

### Gateway won't start — Valkey connection failed

**Cause:** Valkey is down or wrong password.

```bash
# Check Valkey
docker exec local-valkey valkey-cli -a "$VALKEY_PASSWORD" ping

# Check .env has VALKEY_PASSWORD
grep VALKEY_PASSWORD ~/platform/.env

# Restart after fixing
docker compose -f docker-compose.platform.yml restart flowero-gate
```

### Gateway won't start — missing environment variable

**Cause:** `app.post-login-redirect-url` not set (SecurityConfig requires it).

```bash
# Check if set
docker exec flowero-gate env | grep POST_LOGIN

# If missing, add to .env
echo "POST_LOGIN_REDIRECT_URL=https://panomete.com" >> ~/platform/.env

# Restart
docker compose -f docker-compose.platform.yml up -d flowero-gate
```

### Nginx returns 502 for api.panomete.com

**Cause:** Gate container down or port not bound.

```bash
# Check container
docker ps | grep flowero-gate

# Check port
ss -tlnp | grep 8000

# Check Nginx config
sudo nginx -t
cat /etc/nginx/sites-available/api.panomete.com
```

---

## Project Structure

```
flowerogate/
├── build.gradle                        # Gradle build (Java 25 / Boot 4.1 / Cloud 2025.1)
├── settings.gradle
├── Dockerfile                          # Multi-stage (JDK → JRE)
├── docker-compose.yml                  # Standalone compose (for reference)
├── gradlew / gradlew.bat
├── src/
│   ├── main/
│   │   ├── java/panomete/flowerogate/
│   │   │   ├── FlowerogateApplication.java
│   │   │   ├── config/
│   │   │   │   ├── SecurityConfig.java           # OAuth2 RS + RC + 401/403 handlers
│   │   │   │   ├── CorsConfig.java
│   │   │   │   ├── RateLimiterConfig.java        # Key resolvers (IP, principal, API-key)
│   │   │   │   ├── ResilientRedisRateLimiter.java # Fail-open rate limiter
│   │   │   │   ├── CircuitBreakerConfig.java
│   │   │   │   └── ObservabilityConfig.java
│   │   │   ├── filter/
│   │   │   │   ├── JwtClaimHeaderFilter.java     # X-User-Id, X-User-Roles headers
│   │   │   │   ├── TraceIdFilter.java            # W3C traceparent + X-Trace-Id
│   │   │   │   ├── RequestLoggingFilter.java     # Structured JSON logging
│   │   │   │   ├── RateLimitResponseFilter.java  # Custom 429 body
│   │   │   │   └── SensitiveDataMasker.java
│   │   │   ├── controller/
│   │   │   │   └── FallbackController.java       # 404 + circuit breaker fallbacks
│   │   │   └── exception/
│   │   │       └── GatewayExceptionHandler.java
│   │   └── resources/
│   │       ├── application.yaml                  # Base config + routes
│   │       ├── application-dev.yaml              # Dev profile
│   │       └── application-prod.yaml             # Prod profile (env-var driven)
│   └── test/
│       └── java/panomete/flowerogate/
│           ├── FlowerogateApplicationTests.java
│           └── gateway/
│               ├── RouteTests.java
│               ├── SecurityTests.java
│               └── TestSecurityConfig.java
└── README.md
```

---

## Related

- [[keycloak]] — Identity provider (Guard issues JWTs, Gate validates them)
- [[discovery]] — Service registry (Gate resolves `lb://` routes via Eureka)
- [[valkey]] — Rate limiting backend
- [[docker-network]] — Why `db-network` and container names matter
- [[08.1-Add-Subdomain]] — How the Nginx block works
