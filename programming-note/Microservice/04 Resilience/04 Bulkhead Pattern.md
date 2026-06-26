# 04 Bulkhead Pattern

In a ship, bulkheads are walls that seal off compartments. If one compartment floods, the ship stays afloat. In microservices, bulkheads isolate failures so one bad service doesn't sink the whole system.

---

## The Pattern

> **Partition resources so that a failure in one part doesn't exhaust resources for another.**

```
❌ No Bulkhead:
  All services share one thread pool (100 threads)
  PaymentService goes slow → uses all 100 threads
  OrderService, UserService → blocked, no threads available
  Entire system = dead

✅ With Bulkhead:
  Payment pool: 20 threads
  Order pool:    40 threads
  User pool:     40 threads
  PaymentService goes slow → only uses its own 20
  OrderService, UserService → unaffected
```

---

## Types of Bulkheads

### 1. Thread Pool Bulkhead

Assign a dedicated thread pool per downstream service.

| Service | Max Threads | Max Queue |
|---------|:----------:|:---------:|
| Payment | 10 | 5 |
| Inventory | 10 | 5 |
| Shipping | 5 | 3 |

### 2. Semaphore Bulkhead

Limit concurrent calls with a semaphore. Simpler than thread pools — no extra thread management.

```java
@Bulkhead(name = "paymentService", type = Bulkhead.Type.SEMAPHORE,
          maxConcurrentCalls = 10, fallbackMethod = "fallback")
public PaymentResponse charge(Order order) { ... }
```

### 3. Connection Pool Bulkhead

Limit database connections per service pool. Prevents one service from exhausting all DB connections.

---

## Resilience4j Configuration

```yaml
resilience4j:
  bulkhead:
    instances:
      paymentService:
        maxConcurrentCalls: 10
        maxWaitDuration: 100ms
  thread-pool-bulkhead:
    instances:
      paymentService:
        maxThreadPoolSize: 10
        coreThreadPoolSize: 5
        queueCapacity: 20
```

---

## Bulkhead + Circuit Breaker = Defense in Depth

```
Request → Bulkhead (limits concurrency) → Circuit Breaker (stops on failure) → Service
```

| Layer | What It Protects Against |
|-------|------------------------|
| **Bulkhead** | Resource exhaustion (slow service hogging threads) |
| **Circuit Breaker** | Repeated failure (cascading errors) |
| **Timeout** | Hanging requests (never returning) |
| **Retry** | Transient failures (network blip) |

---

## Sources

- Nygard, Michael. *Release It!*, 2nd ed., Pragmatic Bookshelf, 2018.
- Resilience4j — https://resilience4j.readme.io/docs/bulkhead
