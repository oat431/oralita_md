# Uptime Kuma

> Uptime monitoring and status page for the Panomete Platform.
> Last updated: 2026-07-24

---

## Deployment Status

> **Deployed:** 2026-07-24 | **Status:** Running, needs first-time setup
>
> - Container: `uptime-kuma` — Running (unhealthy until admin account created)
> - Port: `127.0.0.1:3001`
> - Domain: `status.panomete.com`
> - Admin setup: ⬜ Pending (browser task)

---

## What & Why

Uptime Kuma is a lightweight uptime monitor that pings all `*.panomete.com` URLs every 30 seconds and shows a status page. Unlike Grafana (which monitors metrics), Uptime Kuma monitors **availability** — is the service reachable?

---

## Setup

| Item | Value |
|------|-------|
| Container | `uptime-kuma` |
| Port | `127.0.0.1:3001` |
| Domain | `status.panomete.com` |
| Data volume | `uptime_kuma_data` |
| Compose | `/home/flowero/platform/docker-compose.observability.yml` |

---

## First-Time Setup (Browser Task)

1. Go to `https://status.panomete.com`
2. Create admin account (username + password)
3. Add monitors:

| Monitor Name | URL | Expected | Check Type |
|-------------|-----|----------|------------|
| Keycloak (Guard) | `https://auth.panomete.com` | 200 | HTTP |
| Eureka (Discover) | `https://discovery.panomete.com` | 200 | HTTP |
| Gateway (Gate) | `https://api.panomete.com/actuator/health` | 200 | HTTP + keyword `UP` |
| Grafana | `https://grafana.panomete.com` | 200 | HTTP |
| Status Page | `https://status.panomete.com` | 200 | HTTP |

4. Set check interval: 30 seconds
5. Optional: Create a public status page at `https://status.panomete.com/status`

---

## Common Commands

```bash
# Check container status
docker ps --format '{{.Names}} | {{.Status}}' | grep uptime

# View logs
docker logs uptime-kuma --tail 20

# Restart
docker restart uptime-kuma
```

---

## Troubleshooting

### Container shows "unhealthy"

**Cause:** Admin account not created yet. This is normal after first deploy.

**Fix:** Go to `https://status.panomete.com` and create the admin account.

### 502 Bad Gateway

**Cause:** Container not running or port not bound.

```bash
docker ps | grep uptime-kuma
ss -tlnp | grep 3001
```

---

## Related

- [[observability-stack]] — Prometheus + Grafana (metrics monitoring)
- [[../microservice_component/keycloak]] — Keycloak health check
- [[../microservice_component/discovery]] — Discover health check
- [[../microservice_component/gateway]] — Gate health check
