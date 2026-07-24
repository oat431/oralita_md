# Observability Stack

> Prometheus + Grafana + Loki + Promtail for the Panomete Platform.
> Last updated: 2026-07-24

---

## Deployment Status

> **Deployed:** 2026-07-24 | **Verified:** All targets UP
>
> - Prometheus: ✅ Healthy, 4 targets scraping (gate, discover, guard, self)
> - Grafana: ✅ Healthy, 3 dashboards loaded, Discord webhook configured
> - Loki: ✅ Healthy, receiving logs from Promtail
> - Promtail: ✅ Running, tailing all container logs
> - Alert rules: ✅ 3 rules (service down, high memory, disk space)

---

## Architecture

```
┌─────────────┐     scrape      ┌─────────────┐
│ flowero-gate │ ◄────────────── │             │
│ :8000        │                 │  Prometheus  │
├─────────────┤     scrape      │  :9090       │
│flowero-disc. │ ◄────────────── │             │
│ :8999        │                 └──────┬──────┘
├─────────────┤     scrape             │
│flowero-guard │ ◄──────────────      │ query
│ :9000        │                 ┌──────▼──────┐
└─────────────┘                 │   Grafana   │
                                │   :3000     │
┌─────────────┐    push logs    │ grafana.    │
│  Promtail   │ ──────────────► │ panomete.com│
│  (agent)    │    ┌──────┐    └──────┬──────┘
└─────────────┘    │ Loki │           │ alerts
                   │:3100 │    ┌──────▼──────┐
                   └──────┘    │  Discord    │
                               │  Webhook    │
                               └─────────────┘
```

---

## Services

### Prometheus

| Item | Value |
|------|-------|
| Container | `prometheus` |
| Port | `127.0.0.1:9090` |
| Domain | Internal only (not exposed) |
| Data retention | 15 days |
| Config | `/home/flowero/platform/observability/prometheus/prometheus.yml` |

**Scrape targets:**

| Job | Target | Metrics Path | Status |
|-----|--------|-------------|:------:|
| flowero-gate | `flowero-gate:8000` | `/actuator/prometheus` | ✅ UP |
| flowero-discover | `flowero-discover:8999` | `/actuator/prometheus` | ✅ UP |
| flowero-guard | `flowero-guard:9000` | `/metrics` | ✅ UP |
| prometheus | `localhost:9090` | `/metrics` | ✅ UP |

> **Note:** Guard metrics are on management port 9000, not main port 8080.

### Grafana

| Item | Value |
|------|-------|
| Container | `grafana` |
| Port | `127.0.0.1:3000` |
| Domain | `grafana.panomete.com` |
| Admin user | `admin` |
| Admin password | From `~/platform/.env` (`GRAFANA_ADMIN_PASSWORD`) |
| Config | Provisioning via `/home/flowero/platform/observability/grafana/` |

**Dashboards:**

| Dashboard | UID | Panels |
|-----------|-----|--------|
| Platform Overview | `panomete-overview` | Service health, request rate, error rate, p95 latency |
| JVM Health | `panomete-jvm` | Heap memory, thread count, GC pauses |
| Gate Traffic | `panomete-gate-traffic` | Requests by status/route, 401/429 counts |

**Datasources:**

| Name | Type | URL |
|------|------|-----|
| Prometheus | prometheus | `http://prometheus:9090` |
| Loki | loki | `http://loki:3100` |

### Loki

| Item | Value |
|------|-------|
| Container | `loki` |
| Port | `127.0.0.1:3100` |
| Domain | Internal only |
| Config | `/home/flowero/platform/observability/loki/loki-config.yml` |
| Ingestion rate | 16 MB/s |

### Promtail

| Item | Value |
|------|-------|
| Container | `promtail` |
| Port | None (agent) |
| Config | `/home/flowero/platform/observability/promtail/promtail-config.yml` |
| Log source | `/var/lib/docker/containers/*/*.log` |
| Destination | `http://loki:3100/loki/api/v1/push` |

---

## Alert Rules

| Alert | Condition | Severity | Notification |
|-------|-----------|----------|-------------|
| Service Down | `up{job=~"flowero-.*"} == 0` for 1m | 🔴 Critical | Discord @here |
| High Memory | JVM heap > 80% for 5m | 🟡 Medium | Discord embed |
| Disk Space Low | Disk < 20% free for 5m | 🟠 High | Discord embed |

**Discord webhook:** Configured in Grafana contact points via `DISCORD_WEBHOOK_URL` env var.

---

## Common Commands

```bash
# Check Prometheus targets
curl -sf http://localhost:9090/api/v1/targets | python3 -c "import sys,json; [print(t['scrapePool'], t['health']) for t in json.load(sys.stdin)['data']['activeTargets']]"

# Check Grafana health
curl -sf http://localhost:3000/api/health

# Check Loki ready
curl -sf http://localhost:3100/ready

# View Promtail logs
docker logs promtail --tail 20

# Query Loki for container logs
curl -sf "http://localhost:3100/loki/api/v1/query_range" --data-urlencode 'query={container=~".*"}' --data-urlencode 'limit=10' | python3 -c "import sys,json; [print(r['values'][0][1]) for r in json.load(sys.stdin)['data']['result']]"

# Restart all observability services
cd ~/platform
docker compose -f docker-compose.observability.yml restart

# View Grafana alert rules
curl -sf -u admin:$GRAFANA_ADMIN_PASSWORD http://localhost:3000/api/v1/provisioning/alert-rules | python3 -c "import sys,json; [print(r['title']) for r in json.load(sys.stdin)]"
```

---

## Troubleshooting

### Prometheus target DOWN

```bash
# Check target error
curl -sf http://localhost:9090/api/v1/targets | python3 -c "
import sys,json
for t in json.load(sys.stdin)['data']['activeTargets']:
    if t['health'] != 'up':
        print(f\"{t['scrapePool']}: {t.get('lastError','unknown')}\")"

# Common causes:
# - Service not running → docker ps | grep <service>
# - Wrong port → check prometheus.yml target
# - Wrong metrics path → check service actuator config
```

### Grafana alert errors — "data source not found"

**Cause:** Alert rules reference wrong datasource UID.

**Fix:** Get correct UID:
```bash
curl -sf -u admin:$GRAFANA_ADMIN_PASSWORD http://localhost:3000/api/datasources | python3 -c "import sys,json; [print(d['name'], d['uid']) for d in json.load(sys.stdin)]"
```

Update `alert-rules.yml` with correct UID, restart Grafana.

### Promtail — "ingestion rate limit exceeded"

**Cause:** Loki rate limit too low for container log volume.

**Fix:** Increase in `loki-config.yml`:
```yaml
limits_config:
  ingestion_rate_mb: 16
  ingestion_burst_size_mb: 32
```

Restart Loki + Promtail.

### Promtail — "empty ring"

**Cause:** Loki just restarted and hasn't formed its ring yet.

**Fix:** Wait 30 seconds. Promtail will retry automatically.

---

## Compose File

Observability services are in a **separate compose file** to keep them isolated from the platform services:

```bash
# Location
/home/flowero/platform/docker-compose.observability.yml

# Manage
docker compose -f docker-compose.observability.yml up -d
docker compose -f docker-compose.observability.yml down
docker compose -f docker-compose.observability.yml logs -f
```

---

## Related

- [[github-actions-tailscale]] — CI/CD pipeline (deployed observability via compose)
- [[backup-automation]] — Backup scripts (runs on same server)
- [[../microservice_component/gateway]] — Gate metrics endpoint (`/actuator/prometheus`)
- [[../microservice_component/discovery]] — Discover metrics endpoint (`/actuator/prometheus`)
- [[../microservice_component/keycloak]] — Guard metrics endpoint (`/metrics` on management port 9000)
