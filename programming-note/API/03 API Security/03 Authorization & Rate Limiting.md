# 03 Authorization & Rate Limiting

Authentication tells you WHO. Authorization tells you what they CAN DO. Rate limiting prevents abuse. Together they're the gatekeepers of your API.

---

## Authorization Models

### RBAC (Role-Based Access Control)

Users have roles. Roles have permissions.

```
User → has role → "admin" → has permissions → [read, write, delete]
User → has role → "customer" → has permissions → [read_own]
```

```java
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/orders/{id}")
public void deleteOrder(@PathVariable String id) { ... }

@PreAuthorize("hasRole('CUSTOMER') and #userId == authentication.name")
@GetMapping("/orders")
public List<Order> getMyOrders(@RequestParam String userId) { ... }
```

### ABAC (Attribute-Based Access Control)

Decisions based on attributes — user, resource, action, context.

```
Allow IF:
  user.department == resource.department
  AND action IN ["read", "write"]
  AND time BETWEEN 09:00 AND 17:00
```

### Scopes (OAuth2)

Fine-grained permissions attached to tokens.

```
JWT payload:
{
  "sub": "123",
  "scope": "orders:read orders:write users:read"
}
```

```java
@PreAuthorize("hasAuthority('SCOPE_orders:write')")
@PostMapping("/orders")
public Order createOrder(@RequestBody Order order) { ... }
```

---

## Rate Limiting

Protect your API from abuse, accidents, and DDoS.

### Algorithms

| Algorithm | How It Works | Best For |
|-----------|-------------|----------|
| **Fixed Window** | N requests per time window (e.g., 100/min) | Simple, but burst at window edges |
| **Sliding Window** | Smooth the window to avoid edge bursts | More accurate |
| **Token Bucket** | Tokens refill at rate R. Each request consumes 1 token. | Burst-friendly, most common |
| **Leaky Bucket** | Requests queue. Processed at fixed rate. | Strict rate enforcement |

### Implementation

```yaml
# Spring Boot + Bucket4j
bucket4j:
  filters:
    - cache-name: rate-limit-buckets
      url: /api/.*
      rate-limits:
        - bandwidths:
            - capacity: 100
              time: 1
              unit: minutes
```

```java
// Per-user rate limit
@GetMapping("/orders")
@RateLimiter(name = "ordersApi", fallbackMethod = "rateLimitFallback")
public List<Order> getOrders() { ... }

public List<Order> rateLimitFallback(Exception e) {
    throw new ResponseStatusException(HttpStatus.TOO_MANY_REQUESTS, 
        "Rate limit exceeded. Try again in 60 seconds.");
}
```

---

## Response Headers

Always tell clients their rate limit status:

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 67
X-RateLimit-Reset: 1716123456
Retry-After: 60
```

When rate limited:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 45
X-RateLimit-Reset: 1716123500
```

---

## Sources

- OAuth2 Scopes — https://oauth.net/2/scope/
- Bucket4j — https://bucket4j.com/
- Spring Security Authorization — https://docs.spring.io/spring-security/reference/servlet/authorization/
