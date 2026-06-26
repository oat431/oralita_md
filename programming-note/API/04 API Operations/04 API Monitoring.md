# 04 API Monitoring

If your API is down and you don't know before your users do, you're flying blind. API monitoring catches errors, measures performance, and alerts before customers complain.

---

## Key Metrics

### RED Method (Request-Oriented)

| Metric | What | Alert When |
|--------|------|------------|
| **Rate** | Requests per second | Sudden 2x spike or 50% drop |
| **Errors** | 4xx + 5xx percentage | > 1% error rate |
| **Duration** | Latency (p50, p95, p99) | p99 > 500ms |

### API-Specific Metrics

| Metric | Why It Matters |
|--------|---------------|
| **Requests per endpoint** | Which endpoints are hot? Where to optimize? |
| **Status code distribution** | 2xx vs 4xx vs 5xx — are errors client or server? |
| **Response size** | Are payloads bloating over time? |
| **Auth failures** | 401 spike = expired tokens or attack? |
| **Rate limit hits** | Are users hitting limits? Raise limits or optimize? |
| **Dependency latency** | How long do downstream calls take? |

---

## Spring Boot Actuator + Micrometer

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus
  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: order-service
```

```java
// Custom metric
@RestController
public class OrderController {
    
    private final Counter ordersCreated = Counter.builder("orders.created")
        .description("Number of orders created")
        .register(Metrics.globalRegistry);
    
    @PostMapping("/orders")
    public Order createOrder(@RequestBody Order order) {
        Order created = orderService.create(order);
        ordersCreated.increment();
        return created;
    }
}
```

---

## Alerting Rules

| Alert | Condition | Severity |
|-------|-----------|:--------:|
| **API down** | Health check fails for 1 min | 🔴 Critical |
| **High error rate** | 5xx > 5% for 5 min | 🟡 Warning |
| **Slow responses** | p95 > 1s for 10 min | 🟡 Warning |
| **Auth failures spike** | 401 > 10% of requests for 5 min | 🟡 Warning |
| **Certificate expiring** | < 7 days until expiry | 🔴 Critical |

---

## SLAs, SLOs, SLIs

| Term | Meaning | Example |
|------|---------|---------|
| **SLI** (Indicator) | What you measure | p99 latency |
| **SLO** (Objective) | The target | p99 < 200ms |
| **SLA** (Agreement) | The promise to customers | 99.9% uptime, or credits |

```
SLI:  p99 latency = 187ms
SLO:  p99 latency must be < 200ms (over 30-day rolling window)
SLA:  If uptime < 99.9% in a month → 10% credit
```

---

## Sources

- Prometheus — https://prometheus.io/
- Micrometer — https://micrometer.io/
- Google SRE Book — https://sre.google/books/
