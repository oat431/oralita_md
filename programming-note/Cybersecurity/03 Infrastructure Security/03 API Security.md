---
tags:
- cybersecurity
- programming
- security
---

# 03 API Security

APIs are the front door to your backend. Every public endpoint is an attack surface. Secure the door before worrying about the windows.

---

## The Security Stack for APIs

```
Client → HTTPS → WAF → API Gateway → Auth → Rate Limit → App → DB
```

---

## CORS (Cross-Origin Resource Sharing)

```java
// ❌ Too permissive — allows any site to call your API
@CrossOrigin(origins = "*")

// ✅ Restricted to your domains
@CrossOrigin(origins = {
    "https://app.example.com",
    "https://admin.example.com"
})
```

```yaml
# Spring Security CORS
spring:
  security:
    cors:
      allowed-origins: "https://app.example.com"
      allowed-methods: "GET,POST,PUT,DELETE"
      allowed-headers: "Authorization,Content-Type"
      max-age: 3600
```

---

## Rate Limiting — Resilience4j + Bucket4j

```java
// Per-IP rate limiting
@Bean
public RateLimiter rateLimiter() {
    return RateLimiter.of("api-limiter", RateLimiterConfig.custom()
        .limitRefreshPeriod(Duration.ofMinutes(1))
        .limitForPeriod(100)            // 100 requests per minute
        .timeoutDuration(Duration.ofMillis(500))  // Wait at most 500ms
        .build());
}

@GetMapping("/api/data")
@RateLimiter(name = "api-limiter")
public Data getData() { ... }
```

### Rate Limiting by Tier

| Tier | Requests/Minute | Burst |
|------|:-------------:|:-----:|
| Free | 60 | 10 |
| Pro | 1000 | 50 |
| Enterprise | 10000 | 200 |

---

## GraphQL-Specific Attacks

| Attack | Description | Defense |
|--------|------------|---------|
| **Deep queries** | Nested query causes exponential backend calls | Max query depth (e.g., 7 levels) |
| **Batching attack** | Many queries in one request | Max aliases per request |
| **Field suggestion** | Introspection reveals schema | Disable introspection in production |

```java
// Netflix DGS — query complexity limits
@Configuration
public class GraphQLConfig {
    @Bean
    public MaxQueryDepthInstrumentation maxDepth() {
        return new MaxQueryDepthInstrumentation(7);  // Max 7 levels deep
    }
}
```

---

## API Key Best Practices

```java
// ✅ API key validation
@Component
public class ApiKeyFilter extends OncePerRequestFilter {
    
    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain) {
        String apiKey = request.getHeader("X-API-Key");
        
        if (apiKey == null || !apiKeyService.isValid(apiKey)) {
            response.setStatus(401);
            return;
        }
        
        // Log usage, check rate limits
        apiKeyService.recordUsage(apiKey);
        chain.doFilter(request, response);
    }
}
```

| Rule | Why |
|------|-----|
| **Short, random keys** | `sk_abc123...` — not sequential. Use `UUID` or `SecureRandom`. |
| **Hash before storing** | Like passwords. If DB leaks, keys are still safe. |
| **Scoped** | Key for "read orders" can't "delete orders" |
| **Expirable** | Auto-expire unused keys after 90 days |

---

## API Security Checklist

- [ ] All endpoints behind HTTPS (redirect HTTP → HTTPS)
- [ ] Authentication on every endpoint (or explicitly public)
- [ ] Authorization check on every endpoint
- [ ] Rate limiting on all public endpoints
- [ ] CORS restricted to known origins
- [ ] Request size limits (body max 10MB, headers max 8KB)
- [ ] Response headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`
- [ ] GraphQL: max depth, max aliases, disable introspection in prod

---

## Sources

- OWASP API Security Top 10 — https://owasp.org/www-project-api-security/
- GraphQL Security — https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html
