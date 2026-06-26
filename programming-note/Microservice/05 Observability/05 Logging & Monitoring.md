# 05 Logging & Monitoring

You can't fix what you can't see. In a monolith, you check one log file. In microservices, a single user request touches 5+ services — you need centralized logging and metrics to understand what's happening.

---

## The Three Pillars of Observability

| Pillar | Question It Answers | Tool Examples |
|--------|-------------------|---------------|
| **Logging** | What happened? | ELK (Elasticsearch, Logstash, Kibana), Loki |
| **Metrics** | How much / how fast? | Prometheus + Grafana, Datadog |
| **Tracing** | Where did it go? | Jaeger, Zipkin, OpenTelemetry |

---

## Centralized Logging

Every service writes structured logs (JSON). A log aggregator collects, indexes, and makes them searchable.

```
Service A ─┐
Service B ─┼── Log Aggregator (Elasticsearch / Loki) ── Kibana / Grafana
Service C ─┘
```

### Structured Logging

| ❌ Unstructured | ✅ Structured (JSON) |
|----------------|---------------------|
| `User 123 placed order 456` | `{"level":"INFO","service":"order","userId":"123","orderId":"456","action":"order_placed","timestamp":"..."}` |

### What Every Log Entry Needs

| Field | Why |
|-------|-----|
| **traceId** | Ties all logs for one request across services |
| **service** | Which service wrote this |
| **timestamp** | When (UTC, ISO 8601) |
| **level** | INFO, WARN, ERROR |
| **message** | Human-readable description |

---

## Metrics — The Four Golden Signals

From Google's SRE book:

| Signal | What It Measures | Alert When |
|--------|-----------------|------------|
| **Latency** | How long requests take | p99 > 500ms |
| **Traffic** | Request rate (RPS) | Sudden 2x spike or drop |
| **Errors** | Error rate (5xx) | > 1% of requests |
| **Saturation** | How "full" the service is | CPU > 80%, thread pool queue > 100 |

### RED Method (Request-Oriented)

| R | Rate | Requests per second |
| E | Errors | Failed requests |
| D | Duration | Latency distribution (p50, p95, p99) |

### USE Method (Resource-Oriented)

| U | Utilization | % of resource used |
| S | Saturation | Queue depth, backlog |
| E | Errors | Hardware/software errors |

---

## Dashboards

Every service gets a dashboard:

| Row | What |
|-----|------|
| **Top** | Request rate, error rate, p95 latency |
| **Middle** | Circuit breaker state, thread pool usage |
| **Bottom** | JVM/Go metrics: heap, GC, goroutines |

> If a metric matters enough to measure, it matters enough to alert on. No dashboard-only metrics — every metric has an alert threshold.

---

## Sources

- Beyer, Betsy et al. *Site Reliability Engineering*, O'Reilly, 2016.
- Prometheus — https://prometheus.io/
- Grafana — https://grafana.com/
