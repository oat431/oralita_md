---
tags:
- architecture
- microservices
- programming
---

# 05 Health Checks

Kubernetes and load balancers need to know: is this service alive and ready to receive traffic? Health checks answer that. Without them, traffic routes to dead instances.

---

## Three Types of Health Checks

| Type | Question | Failing = |
|------|----------|-----------|
| **Liveness** | "Am I running?" | Restart the container |
| **Readiness** | "Can I serve traffic?" | Remove from load balancer |
| **Startup** | "Am I initialized?" | Wait before checking liveness/readiness |

---

## Liveness vs Readiness

```
Liveness:  "My process is alive"          → /health/liveness
Readiness: "My dependencies are healthy"  → /health/readiness
```

| Scenario | Liveness | Readiness |
|----------|:--------:|:---------:|
| App is running, DB is down | ✅ Alive | ❌ Not Ready |
| App is deadlocked | ❌ Dead | ❌ Not Ready |
| App is starting, warming caches | ✅ Alive | ❌ Not Ready |
| Everything is fine | ✅ Alive | ✅ Ready |

> Liveness fails = Kubernetes **restarts** the pod. Readiness fails = Kubernetes **stops sending traffic** but doesn't restart.

---

## Spring Boot Actuator

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info
  endpoint:
    health:
      show-details: always
      probes:
        enabled: true
  health:
    livenessstate:
      enabled: true
    readinessstate:
      enabled: true
```

```json
// GET /actuator/health
{
  "status": "UP",
  "components": {
    "livenessState": { "status": "UP" },
    "readinessState": { "status": "UP" },
    "db": { "status": "UP", "details": { "database": "PostgreSQL", "validationQuery": "isValid()" } },
    "redis": { "status": "UP" },
    "diskSpace": { "status": "UP", "details": { "free": "10GB" } }
  }
}
```

---

## Custom Health Indicators

```java
@Component
public class PaymentServiceHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        try {
            boolean isHealthy = paymentClient.ping();
            if (isHealthy) return Health.up().withDetail("latency", "50ms").build();
            return Health.down().withDetail("error", "timeout").build();
        } catch (Exception e) {
            return Health.down(e).build();
        }
    }
}
```

---

## Kubernetes Probes

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
```

---

## Sources

- Spring Boot Actuator — https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html
- Kubernetes — https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
