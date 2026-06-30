# Flowero Gate — API Gateway

> **Code Name:** Flowero Gate  
> **Domain:** gateway.panomete.com (gateway subdomain routing to all services)  
> **Status:** ✅ Completed | ✅ Deployed  
> **Stack:** Spring Cloud Gateway 2025.x + Spring Boot 4.x + WebFlux/Netty + Redis  
> **Document Purpose:** Complete project specification and integration guide for routing new services through the gateway.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Tech Stack](#3-tech-stack)
4. [Route Configuration](#4-route-configuration)
5. [Filters & Middleware Pipeline](#5-filters--middleware-pipeline)
6. [Authentication & Authorization Flow](#6-authentication--authorization-flow)
7. [Rate Limiting](#7-rate-limiting)
8. [Resilience — Circuit Breaker & Retry](#8-resilience--circuit-breaker--retry)
9. [CORS & Security Headers](#9-cors--security-headers)
10. [Observability](#10-observability)
11. [Deployment & Operations](#11-deployment--operations)
12. [Service Integration Guide](#12-service-integration-guide)
13. [Integration Checklist (for New Services)](#13-integration-checklist-for-new-services)
14. [Troubleshooting & Gotchas](#14-troubleshooting--gotchas)

---

## 1. Overview

### What Flowero Gate Does

Flowero Gate is the single entry point for all homelab microservices. Every external request flows through it. It handles:

- **Routing** — Path-based routing to upstream services (`/api/v1/ledger` → ledger-service)
- **Authentication** — OAuth2/OIDC integration with Flowero Guard (Keycloak). Validates JWT at the edge, strips `Authorization` header, forwards user claims as headers
- **Rate limiting** — Redis-backed token bucket per user/IP/endpoint
- **Resilience** — Circuit breaker, retry with backoff, timeouts per route
- **CORS** — Single configuration point for all services
- **Observability** — Trace ID generation, structured logging, metrics per route
- **Security** — TLS termination, security headers, request size limits

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Spring Cloud Gateway** (not Kong/Nginx) | Native Spring ecosystem; same language as services; programmatic route definition; reactive stack |
| **WebFlux / Netty** (not Tomcat) | Non-blocking I/O for gateway workloads; higher concurrency; lower memory per connection |
| **Stateless + Redis** | Gateway instances are disposable; shared state (rate limits) in Redis; horizontal scaling via replicas |
| **JWT validated at gateway, stripped before forwarding** | Defense in depth — services also validate JWT independently; token harvesting impossible |
| **`lb://` with Spring Cloud LoadBalancer** | Service discovery integration; automatic instance tracking; no hardcoded IPs |
| **Resilience4j** (not Hystrix) | Active maintenance; reactive-native; circuit breaker + retry + bulkhead in one library |

---

## 2. Architecture

```
                        ┌──────────────────────────────────────────┐
                        │           External Requests               │
                        │     (Browser → gateway.panomete.com)          │
                        └──────────────────┬───────────────────────┘
                                           │ HTTPS (TLS 1.3)
                                           ▼
                        ┌──────────────────────────────────────────┐
                        │              Nginx (Edge)               │
                        │     TLS termination, Let's Encrypt        │
                        │     Primary router: gateway.panomete.com      │
                        └──────────────────┬───────────────────────┘
                                           │ HTTP (internal)
                                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Flowero Gate (Spring Cloud Gateway)            │
│                                                                   │
│  ┌─────────┐  ┌───────────┐  ┌────────────┐  ┌────────────────┐ │
│  │ Global   │  │ JWT Claim │  │ Rate        │  │ Route          │ │
│  │ Filters  │  │ Header    │  │ Limiter     │  │ Matching       │ │
│  │ (Trace   │  │ Filter    │  │ (Redis)     │  │ (Path/Method)  │ │
│  │  ID)     │  │           │  │             │  │                │ │
│  └────┬─────┘  └─────┬─────┘  └──────┬──────┘  └───────┬────────┘ │
│       │              │               │                  │          │
│       ▼              ▼               ▼                  ▼          │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    Route-Specific Filters                     │ │
│  │  (StripPrefix, CircuitBreaker, Retry, AddRequestHeader, etc.) │ │
│  └──────────────────────────────────────────────────────────────┘ │
│       │                                                           │
│       ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              Spring Cloud LoadBalancer (lb://)                │ │
│  │         Service discovery → instance selection → forward       │ │
│  └──────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                    │                    │                    │
                    ▼                    ▼                    ▼
          ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
          │ Ledger Svc   │   │ Shortlink Svc│   │   (...more)  │
          │ (Big Schwein)│   │(Fluffy Mouton│   │              │
          └──────────────┘   └──────────────┘   └──────────────┘
                    │                    │
              ┌─────▼─────┐      ┌──────▼─────┐
              │ PostgreSQL│      │ PostgreSQL │
              └───────────┘      └────────────┘

          Sidecar: Redis — shared state (rate limits, session cache)
```

### Flow Summary

1. Request arrives at `https://gateway.panomete.com/api/v1/ledger/transactions`
2. Nginx terminates TLS → forwards HTTP to Gateway
3. Gateway **GlobalFilter chain** executes: Trace ID → JWT Claim Header → ...
4. Gateway matches route: `Path=/api/v1/ledger/**` → `route-ledger`
5. Route-specific filters: `StripPrefix=1` (removes `/api`) → `CircuitBreaker` → `RequestRateLimiter`
6. Spring Cloud LoadBalancer resolves `lb://ledger-service` → selects healthy instance
7. Request forwarded to `http://ledger-service:8080/v1/ledger/transactions` with `X-User-*` headers
8. Response flows back through filter chain → Nginx → client

---

## 3. Tech Stack

| Component | Technology | Version | Notes |
|-----------|-----------|---------|-------|
| Gateway Framework | Spring Cloud Gateway | 2025.x | Reactive (WebFlux/Netty) |
| Base Framework | Spring Boot | 4.x | Java 21+, Spring Framework 7 |
| Security | Spring Security 7 (reactive) | — | OAuth2 Client + Resource Server |
| Rate Limiting | Redis-backed `RequestRateLimiter` | — | Token bucket algorithm |
| Resilience | Resilience4j | — | Circuit breaker, retry, bulkhead |
| Service Discovery | Spring Cloud LoadBalancer | — | `lb://` URI scheme |
| State Store | Redis | 7.x | Reactive client (`ReactiveRedisConnectionFactory`) |
| Observability | OpenTelemetry + Micrometer | — | Traces, metrics, structured logging |
| JSON | Jackson 3 (`tools.jackson`) | — | Package rename in Boot 4 |
| Server | Netty (embedded) | — | Non-blocking, no Tomcat |
| Container | Docker Compose | — | With Nginx for edge routing |

---

## 4. Route Configuration

### 4.1 Route Table

Current registered routes:

| Route ID | Path Pattern | Upstream Service | Auth | Rate Limit | Notes |
|----------|-------------|-----------------|------|------------|-------|
| `route-ledger` | `/api/v1/ledger/**` | `lb://ledger-service` | ✅ JWT | 100 req/s | Big Schwein — Ledger app |
| `route-shortlink` | `/api/v1/short/**` | `lb://shortlink-service` | ✅ JWT | 100 req/s | Fluffy Mouton — URL shortener |
| `route-auth-health` | `/actuator/health/**` | *(gateway itself)* | ❌ Public | ❌ None | Health checks |
| `route-oauth` | `/login/**`, `/oauth2/**` | *(gateway itself)* | ❌ Public | ❌ None | OAuth2 login callback |
| `route-public` | `/api/v1/public/**` | *(varies)* | ❌ Public | 10 req/s | Public API endpoints |
| `route-fallback` | `/**` | *(gateway itself)* | ❌ Public | — | Standardized 404 |

### 4.2 Route Definition (YAML)

```yaml
spring:
  cloud:
    gateway:
      routes:
        # ---- Ledger Service (Big Schwein) ----
        - id: route-ledger
          uri: lb://ledger-service
          order: 0
          predicates:
            - Path=/api/v1/ledger/**
          filters:
            - StripPrefix=1                    # /api/v1/ledger/... → /v1/ledger/...
            - name: CircuitBreaker
              args:
                name: ledgerCircuitBreaker
                fallbackUri: forward:/fallback/ledger
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 200
                redis-rate-limiter.requestedTokens: 1

        # ---- Shortlink Service (Fluffy Mouton) ----
        - id: route-shortlink
          uri: lb://shortlink-service
          order: 0
          predicates:
            - Path=/api/v1/short/**
          filters:
            - StripPrefix=1
            - name: CircuitBreaker
              args:
                name: shortlinkCircuitBreaker
                fallbackUri: forward:/fallback/shortlink
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 200

        # ---- Catch-All / Fallback ----
        - id: route-fallback
          uri: no://op
          order: 9999
          predicates:
            - Path=/**
          filters:
            - SetStatus=404
```

### 4.3 Route Ordering Rules

- **Lower `order` = higher priority** (evaluated first)
- Default `order` is `0`
- Admin routes: `order: -1`
- Catch-all: `order: 9999`
- Be explicit — never rely on declaration order

### 4.4 Available Predicates

| Predicate | Example | Use Case |
|-----------|---------|----------|
| `Path` | `Path=/api/v1/users/**` | Primary routing mechanism |
| `Method` | `Method=GET,POST` | Restrict HTTP methods per route |
| `Host` | `Host=admin.panomete.com` | Subdomain-based routing |
| `Header` | `Header=X-API-Version, 2024-01-01` | API version routing |
| `Query` | `Query=debug, true` | Debug mode routing |
| `Weight` | `Weight=canary, 5` | Canary/traffic splitting |
| `RemoteAddr` | `RemoteAddr=192.168.1.0/24` | IP-based routing (admin endpoints) |
| `Before/After/Between` | `After=2026-01-01T00:00:00+07:00` | Time-based feature flags |

---

## 5. Filters & Middleware Pipeline

### 5.1 GlobalFilter Chain (Execution Order)

```
Order  -100:  TraceIdFilter            — generate/forward W3C traceparent
Order     0:  SecurityWebFilterChain    — Spring Security (auth validation)
Order    10:  JwtClaimHeaderFilter      — extract claims → X-User-* headers, strip Authorization
Order    50:  RequestLoggingFilter      — structured request/response logging
Order   100:  ResponseHeaderFilter      — security headers (HSTS, CSP, etc.)
Order   MAX:  Gateway's internal routing — route matching + forwarding
```

### 5.2 Trace ID Filter

```java
@Component
@Order(-100)
public class TraceIdFilter implements GlobalFilter {

    private static final String TRACE_HEADER = "traceparent";

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String existingTraceId = exchange.getRequest().getHeaders().getFirst(TRACE_HEADER);
        String traceId = existingTraceId != null ? existingTraceId : generateTraceId();

        exchange.getRequest().mutate()
            .header(TRACE_HEADER, traceId)
            .build();

        exchange.getResponse().getHeaders().add(TRACE_HEADER, traceId);

        return chain.filter(exchange)
            .contextWrite(ctx -> ctx.put(TraceContext.class, new TraceContext(traceId)));
    }
}
```

### 5.3 JWT Claim Header Filter

See [Flowero Guard — Section 7.4](./Flowero%20Guard.md#74-jwt-claim-propagation-critical) for the complete implementation.

**What it does:**
1. Extracts `sub`, `preferred_username`, `realm_access.roles` from validated JWT
2. Adds `X-User-Id`, `X-User-Name`, `X-User-Roles` headers
3. **Strips `Authorization` header** (security-critical)
4. Downstream services never see raw tokens

### 5.4 Built-in Route Filters

| Filter | What It Does | When to Use |
|--------|-------------|-------------|
| `StripPrefix` | Removes path segments before forwarding | `/api/v1/ledger/x` → upstream receives `/v1/ledger/x` |
| `PrefixPath` | Adds path prefix | Upstream expects `/api` prefix |
| `AddRequestHeader` | Add static header | `X-Gateway: flowero-gate` |
| `RemoveRequestHeader` | Remove header | Strip internal headers before forwarding |
| `AddResponseHeader` | Add response header | `X-Response-Time`, HSTS |
| `RewritePath` | Regex path transform | `/api/v2/old-path/(?<id>.*)` → `/v2/new-path/${id}` |
| `SetStatus` | Force HTTP status | Maintenance mode, catch-all 404 |
| `Retry` | Retry on failure | GET requests to flaky upstreams |
| `CircuitBreaker` | Resilience4j breaker | Protect against cascading failures |
| `RequestRateLimiter` | Token bucket rate limit | Redis-backed per-user/IP throttling |
| `RequestSize` | Max body size | Prevent memory exhaustion |

### 5.5 Custom Filter Template

```java
@Component
public class CustomGatewayFilter implements GatewayFilter, Ordered {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        // Pre-processing
        ServerHttpRequest request = exchange.getRequest();
        // ...

        return chain.filter(exchange).then(Mono.fromRunnable(() -> {
            // Post-processing
            ServerHttpResponse response = exchange.getResponse();
            // ...
        }));
    }

    @Override
    public int getOrder() {
        return 100; // Lower = earlier
    }
}
```

---

## 6. Authentication & Authorization Flow

Flowero Gate integrates with Flowero Guard for all authentication. The gateway plays a dual role:

- **OAuth2 Client** — Redirects unauthenticated browser requests to Keycloak login
- **Resource Server** — Validates JWT on API requests (bearer tokens)

### 6.1 Flow Diagram

```
Browser → GET https://gateway.panomete.com/api/v1/ledger/transactions
                │
                ▼
         [Has valid session cookie?]
                │
         ┌──────┴──────┐
         │ NO          │ YES
         ▼             ▼
    302 → Keycloak   Gateway validates
    login page       JWT from session
         │             │
         ▼             ▼
    User logs in    Extract claims
         │          → X-User-Id
         ▼          → X-User-Name
    Keycloak →      → X-User-Roles
    302 back to        │
    gateway             ▼
    (with auth      Strip Authorization
     code)          header (security)
         │             │
         ▼             ▼
    Gateway         Forward to
    exchanges code  ledger-service
    for tokens      with X-User-* headers
         │
         ▼
    Store session
         │
         └──────────────┘
                │
                ▼
         Continue to
         upstream service
```

### 6.2 Unauthenticated Routes

These bypass authentication entirely:

- `/actuator/health/**` — Health checks (Nginx, monitoring)
- `/login/**`, `/oauth2/**` — OAuth2 callback endpoints
- `/api/v1/public/**` — Public API (if any)

### 6.3 Service-to-Service Auth via Gateway

When Service A calls Service B through the gateway, it uses the Client Credentials grant:

```
Service A → POST https://auth.panomete.com/realms/homelab/protocol/openid-connect/token
              (with client_id + client_secret)
              ← { access_token: "eyJ...", ... }

Service A → GET https://gateway.panomete.com/api/v1/internal/data
              Authorization: Bearer eyJ...
              ← Gateway validates JWT (sub = "service-a")
              ← Forwards with X-User-Id: service-a
              ← Service B responds
```

See [Flowero Guard — Section 9](./Flowero%20Guard.md#9-service-to-service-authentication) for full setup.

---

## 7. Rate Limiting

### 7.1 Architecture

```
Gateway Instance 1 ─┐
Gateway Instance 2 ─┼──→ Redis (shared counter store)
Gateway Instance 3 ─┘
```

Rate limits are **shared across all gateway instances** via Redis. If one instance fails, the counter persists.

### 7.2 Algorithm: Token Bucket

- **replenishRate:** Tokens added per second (sustained rate)
- **burstCapacity:** Maximum tokens stored (burst allowance)
- **requestedTokens:** Tokens consumed per request (default 1)

### 7.3 Key Resolver

Determines what to rate-limit on:

```java
@Bean
public KeyResolver userKeyResolver() {
    return exchange -> ReactiveSecurityContextHolder.getContext()
        .map(ctx -> ctx.getAuthentication())
        .map(auth -> auth.getName())          // Rate limit by user
        .defaultIfEmpty("anonymous")           // Fallback for unauthenticated
        .cast(String.class);
}
```

Alternative key resolvers:
- **By IP:** `exchange.getRequest().getRemoteAddress().getHostName()`
- **By API key:** `exchange.getRequest().getHeaders().getFirst("X-API-Key")`
- **Composite:** Combine user + endpoint for per-endpoint-per-user limits

### 7.4 Rate Limit Headers

Clients receive these headers on every response:

| Header | Example | Meaning |
|--------|---------|---------|
| `X-RateLimit-Remaining` | `195` | Tokens left in current window |
| `X-RateLimit-Replenish-Rate` | `100` | Tokens added per second |
| `X-RateLimit-Burst-Capacity` | `200` | Maximum burst |
| `Retry-After` | `5` | (on 429) Seconds to wait |

### 7.5 Custom 429 Response

```java
@Bean
public WebFilter rateLimitResponseFilter() {
    return (exchange, chain) -> chain.filter(exchange)
        .onErrorResume(ResponseStatusException.class, e -> {
            if (e.getStatusCode() == HttpStatus.TOO_MANY_REQUESTS) {
                exchange.getResponse().setStatusCode(HttpStatus.TOO_MANY_REQUESTS);
                exchange.getResponse().getHeaders().setContentType(MediaType.APPLICATION_JSON);
                byte[] body = """
                    {"error":"rate_limit_exceeded","message":"Too many requests. Retry after %d seconds."}
                    """.formatted(/* retry-after value */).getBytes();
                return exchange.getResponse()
                    .writeWith(Mono.just(exchange.getResponse().bufferFactory().wrap(body)));
            }
            return Mono.error(e);
        });
}
```

### 7.6 Exemptions

Health checks and monitoring endpoints are **never** rate-limited:

```
/actuator/health/** → No rate limiting
/actuator/prometheus → No rate limiting
```

---

## 8. Resilience — Circuit Breaker & Retry

### 8.1 Resilience4j Circuit Breaker

Per-upstream-service circuit breaker. When upstream fails repeatedly, the breaker opens and requests fail-fast instead of waiting for timeouts.

```yaml
resilience4j:
  circuitbreaker:
    configs:
      default:
        slidingWindowSize: 10              # Last N calls to evaluate
        failureRateThreshold: 50            # % failures to open circuit
        waitDurationInOpenState: 10000      # ms before half-open probe
        permittedNumberOfCallsInHalfOpenState: 3
        automaticTransitionFromOpenToHalfOpenEnabled: true
    instances:
      ledgerCircuitBreaker:
        baseConfig: default
      shortlinkCircuitBreaker:
        baseConfig: default
```

### 8.2 Circuit Breaker States

```
     ┌─────────┐     failures > threshold     ┌─────────┐
     │ CLOSED  │ ─────────────────────────────→│  OPEN   │
     │ (normal)│                                │(fast-fail)│
     └────┬────┘                                └────┬─────┘
          │                                          │
          │ success                                  │ waitDuration expires
          │                                          ▼
          │                                   ┌──────────────┐
          └───────────────────────────────────│ HALF-OPEN    │
              (transition to closed)          │ (probing)    │
                                              └──────┬───────┘
                                                     │
                                          ┌──────────┴──────────┐
                                          │ probe succeeds      │ probe fails
                                          ▼                     ▼
                                     ┌─────────┐          ┌─────────┐
                                     │ CLOSED  │          │  OPEN   │
                                     └─────────┘          └─────────┘
```

### 8.3 Fallback Responses

When circuit is open, route to a fallback endpoint:

```yaml
filters:
  - name: CircuitBreaker
    args:
      name: ledgerCircuitBreaker
      fallbackUri: forward:/fallback/ledger
```

Fallback controller:

```java
@RestController
public class FallbackController {

    @GetMapping("/fallback/ledger")
    public Mono<ResponseEntity<Map<String, Object>>> ledgerFallback() {
        return Mono.just(ResponseEntity
            .status(HttpStatus.SERVICE_UNAVAILABLE)
            .body(Map.of(
                "error", "service_unavailable",
                "message", "Ledger service is temporarily unavailable. Please try again later.",
                "retryAfter", 10
            )));
    }
}
```

### 8.4 Retry Configuration

Only for **idempotent** methods (GET, PUT, DELETE). Never retry POST.

```yaml
filters:
  - name: Retry
    args:
      retries: 3
      statuses: BAD_GATEWAY, SERVICE_UNAVAILABLE, GATEWAY_TIMEOUT
      methods: GET, PUT, DELETE
      backoff:
        firstBackoff: 100ms
        maxBackoff: 2s
        factor: 2
        basedOnPreviousValue: true
```

### 8.5 Timeouts

```yaml
spring:
  cloud:
    gateway:
      httpclient:
        connect-timeout: 3000      # ms to establish connection
        response-timeout: 30s      # max time waiting for upstream response
```

---

## 9. CORS & Security Headers

### 9.1 CORS Configuration

One place, all routes:

```yaml
spring:
  cloud:
    gateway:
      globalcors:
        cors-configurations:
          '[/**]':
            allowedOrigins:
              - "https://app.panomete.com"
              - "https://admin.panomete.com"
            allowedMethods:
              - GET
              - POST
              - PUT
              - DELETE
              - OPTIONS
            allowedHeaders:
              - "Authorization"
              - "Content-Type"
              - "X-Requested-With"
            allowCredentials: true
            maxAge: 3600
```

**⚠️ Never use `allowedOrigins: "*"` with `allowCredentials: true`** — browsers reject this combination.

### 9.2 Security Headers

Added as a GlobalFilter on every response:

```java
@Component
public class SecurityHeadersFilter implements GlobalFilter, Ordered {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        exchange.getResponse().getHeaders().addAll(securityHeaders());
        return chain.filter(exchange);
    }

    private HttpHeaders securityHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
        headers.set("X-Content-Type-Options", "nosniff");
        headers.set("X-Frame-Options", "DENY");
        headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
        headers.set("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
        headers.set("Cache-Control", "no-store"); // Default for APIs
        return headers;
    }

    @Override
    public int getOrder() {
        return 100;
    }
}
```

### 9.3 Request Size Limits

```yaml
spring:
  codec:
    max-in-memory-size: 10MB      # Max request body size
```

Or per-route:

```yaml
filters:
  - name: RequestSize
    args:
      maxSize: 5000000            # 5MB for specific routes
```

---

## 10. Observability

### 10.1 Trace ID Propagation

- **Format:** W3C `traceparent` header (`00-{trace-id}-{span-id}-01`)
- **Generation:** If not present, gateway generates and becomes root span
- **Propagation:** Added to upstream requests and response headers
- **Every service** logs the trace ID in every log line

### 10.2 Structured Logging

Log format (JSON):

```json
{
  "timestamp": "2026-06-16T23:53:00+07:00",
  "level": "INFO",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "span_id": "b7ad6b7169203331",
  "method": "GET",
  "path": "/api/v1/ledger/transactions",
  "status": 200,
  "latency_ms": 45,
  "client_ip": "192.168.1.100",
  "user_id": "panomete",
  "route_id": "route-ledger",
  "upstream": "ledger-service",
  "upstream_latency_ms": 38
}
```

### 10.3 Metrics (Prometheus)

Gateway-specific metrics via Micrometer:

```
spring_cloud_gateway_requests_seconds_count{route_id="route-ledger",status="200"}
spring_cloud_gateway_requests_seconds_sum{route_id="route-ledger",status="200"}
spring_cloud_gateway_requests_seconds_max{route_id="route-ledger",status="200"}

resilience4j_circuitbreaker_state{name="ledgerCircuitBreaker",state="closed"}
resilience4j_circuitbreaker_failed_calls_total{name="ledgerCircuitBreaker"}

redis_rate_limiter_remaining_tokens{route_id="route-ledger"}
```

### 10.4 Gateway Actuator Endpoints

| Endpoint | Purpose | Access |
|----------|---------|--------|
| `/actuator/gateway/routes` | List all routes | Internal only |
| `/actuator/gateway/globalfilters` | List global filters | Internal only |
| `/actuator/gateway/routefilters` | List route filters | Internal only |
| `/actuator/gateway/refresh` | Reload routes without restart | Internal only |
| `/actuator/health` | Gateway health | Public |
| `/actuator/prometheus` | Metrics scrape endpoint | Internal only |

**⚠️ Actuator endpoints MUST NOT be externally accessible.** Either:
- Separate management port (`management.server.port: 8081`)
- Or Nginx middleware IP whitelist on `/actuator/**`

---

## 11. Deployment & Operations

### 11.1 Docker Compose

```yaml
flowero-gate:
  image: flowero-gate:latest
  container_name: flowero-gate
  restart: unless-stopped
  environment:
    SPRING_PROFILES_ACTIVE: production
    KEYCLOAK_GATEWAY_SECRET: ${KEYCLOAK_GATEWAY_SECRET}
    REDIS_HOST: redis
    REDIS_PORT: 6379
  ports:
    - "8000:8000"                      # Internal; Nginx routes from 443
  networks:
    - microservices-net
  depends_on:
    redis:
      condition: service_healthy
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 512M
```

### 11.2 Nginx Reverse Proxy for Gateway

```nginx
# Nginx reverse proxy config for Flowero Gate
server {
    listen 443 ssl http2;
    server_name gateway.panomete.com;

    ssl_certificate     /etc/nginx/ssl/gateway.panomete.com/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/gateway.panomete.com/privkey.pem;

    location / {
        proxy_pass http://flowero-gate:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check for Nginx upstream monitoring
    location /actuator/health {
        proxy_pass http://flowero-gate:8000;
        proxy_set_header Host $host;
    }
}
```

### 11.3 Graceful Shutdown

```yaml
server:
  shutdown: graceful

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

Process: SIGTERM → stop accepting new connections → drain existing (up to 30s) → close → exit.

### 11.4 Resource Guidelines

| Resource | Recommended | Rationale |
|----------|-------------|-----------|
| CPU | 1 core (min) | Gateway is CPU-bound: TLS, routing, JSON parsing |
| Memory | 512 Mi (min) | Connection buffers + filter processing |
| Replicas | 2+ | High availability, rolling restarts |
| Anti-affinity | `kubernetes.io/hostname` | Spread across nodes |

### 11.5 Health Check Endpoints

```nginx
# Nginx upstream health check (requires nginx-plus or nginx-module)
# For open-source nginx, rely on passive health checks or use health check in proxy_pass
# Alternative: use a separate monitoring service to hit /actuator/health

# Basic proxy_pass health check via location block (always available)
# /actuator/health returns 200 when gateway is healthy
```

---

## 12. Service Integration Guide

### How Services Connect Through the Gateway

Every microservice registers with the gateway to receive external traffic. Here's the complete flow:

### 12.1 Service Provides

1. **A service ID** — Used in Docker Compose service name and route config (e.g., `todo-service`)
2. **API endpoints** — REST endpoints the service exposes
3. **Auth requirements** — Public, authenticated, or role-restricted
4. **Rate limit needs** — Expected throughput per endpoint
5. **Timeout expectations** — How long requests typically take

### 12.2 Gateway Configures

1. **Route** — Path pattern → service mapping (e.g., `/api/v1/todo/**` → `lb://todo-service`)
2. **Filters** — StripPrefix, rate limiting, circuit breaker per route
3. **Auth** — Applied automatically via GlobalFilters (services don't configure this)

### 12.3 What the Service Receives

| Item | Description |
|------|-------------|
| **Path** | Stripped of gateway prefix (`/api/v1/todo/items` → `/v1/todo/items`) |
| **Headers** | `X-User-Id`, `X-User-Name`, `X-User-Roles` (comma-separated) |
| **No Authorization** | Stripped by gateway for security |
| **Trace ID** | `traceparent` header for distributed tracing |
| **Rate limiting** | Handled by gateway; service doesn't need to rate-limit externally |

### 12.4 Service Responsibilities

- ✅ Validate JWT independently (or trust gateway headers if on isolated network)
- ✅ Map roles to Spring Security authorities
- ✅ Log trace ID in every log entry
- ✅ Expose `/actuator/health` for gateway health checks
- ❌ Do NOT re-implement rate limiting for external requests (gateway handles it)
- ❌ Do NOT expect `Authorization` header (gateway strips it)
- ❌ Do NOT implement CORS (gateway handles it)

---

## 13. Integration Checklist (for New Services)

Use this when adding a new microservice to route through Flowero Gate.

### Step 1: Service Setup

- [ ] Service has a Docker Compose service name (`<name>-service`)
- [ ] Service is on `microservices-net` network
- [ ] Service exposes `/actuator/health` endpoint
- [ ] Service has Spring Security configured (see [Flowero Guard Section 8](./Flowero%20Guard.md#8-downstream-service-integration))

### Step 2: Route Registration

- [ ] Add route to Gateway `application.yml` under `spring.cloud.gateway.routes`:

```yaml
- id: route-<service-name>
  uri: lb://<service-name>
  order: 0
  predicates:
    - Path=/api/v1/<prefix>/**
  filters:
    - StripPrefix=1
    - name: CircuitBreaker
      args:
        name: <serviceName>CircuitBreaker
        fallbackUri: forward:/fallback/<service-name>
    - name: RequestRateLimiter
      args:
        redis-rate-limiter.replenishRate: 100
        redis-rate-limiter.burstCapacity: 200
```

### Step 3: Resilience Configuration

- [ ] Add circuit breaker config to `application.yml`:

```yaml
resilience4j:
  circuitbreaker:
    instances:
      <serviceName>CircuitBreaker:
        slidingWindowSize: 10
        failureRateThreshold: 50
        waitDurationInOpenState: 10000
        permittedNumberOfCallsInHalfOpenState: 3
```

### Step 4: Fallback Handler

- [ ] Create fallback endpoint:

```java
@RestController
public class FallbackController {
    @GetMapping("/fallback/<service-name>")
    public Mono<ResponseEntity<Map<String, Object>>> serviceFallback() {
        return Mono.just(ResponseEntity
            .status(HttpStatus.SERVICE_UNAVAILABLE)
            .body(Map.of(
                "error", "service_unavailable",
                "message", "<Service> is temporarily unavailable."
            )));
    }
}
```

### Step 5: Rate Limit Key Resolution

- [ ] Ensure `KeyResolver` bean is configured (usually shared — user-based)

### Step 6: Testing

- [ ] Route resolves correctly: `curl https://gateway.panomete.com/api/v1/<prefix>/health` → 200
- [ ] Auth enforced: unauthenticated → 302 redirect to Keycloak
- [ ] Rate limiting works: burst past limit → 429
- [ ] Circuit breaker triggers: kill upstream → gateway returns fallback after threshold
- [ ] StripPrefix correct: request path at service matches expected endpoint
- [ ] Health check: Nginx shows gateway as healthy after service addition

### Step 7: Documentation

- [ ] Update this document's route table (Section 4.1)
- [ ] Document service API endpoints
- [ ] Verify Prometheus metrics appear for new route

---

## 14. Troubleshooting & Gotchas

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| 404 on valid route | Forgot `StripPrefix` or wrong strip count | Upstream receives `/api/v1/x` but expects `/v1/x` |
| 500 `IllegalStateException` | `spring-boot-starter-webmvc` on classpath | Gateway is WebFlux only — remove Web MVC starter |
| `UnknownHostException` with `lb://` | Missing `spring-cloud-starter-loadbalancer` | Add the dependency |
| Rate limiting silently fails | No Redis connection | Check `ReactiveRedisConnectionFactory` bean; check Redis health |
| 403 on all API calls | CSRF enabled (Security 7 default) | Add `.csrf().disable()` |
| `authorizeHttpRequests()` compile error | Using the old `authorizeRequests()` | Use lambda DSL: `.authorizeHttpRequests(auth -> ...)` |
| Routes not updating | Static config (no dynamic source) | Use `/actuator/gateway/refresh` or restart |
| Circuit breaker never opens | Threshold too high or window too large | Reduce `slidingWindowSize`, lower `failureRateThreshold` |
| Jackson serialization errors in custom filters | Importing `com.fasterxml.jackson` in Boot 4 | Update imports to `tools.jackson` |
| High memory usage | Large in-memory buffer for bodies | Set `spring.codec.max-in-memory-size` |
| 504 timeouts | Upstream slower than gateway timeout | Increase `response-timeout` or fix slow upstream |

### Gateway-Specific Gotchas

- ❌ **Mixing Web MVC and WebFlux** — `spring-boot-starter-webmvc` alongside Gateway = `IllegalStateException`. Gateway is 100% reactive.
- ❌ **Blocking in filters** — `Thread.sleep()`, blocking JDBC, blocking HTTP in a GatewayFilter = reactor thread pool exhaustion. Use `.flatMap()`, reactive Redis, reactive HTTP clients.
- ❌ **`@EnableEurekaClient`** — Not needed. Auto-configured. Manual annotation can break registration.
- ❌ **`lb://` without LoadBalancer** — Requires `spring-cloud-starter-loadbalancer`. Without it: `UnknownHostException`.
- ❌ **Rate limiter without Redis** — `RequestRateLimiter` requires Redis. Without it: `BeanCreationException`.
- ❌ **Forgetting routing order** — More specific routes must have lower `order` than wildcards.
- ❌ **Actuator on public port** — Gateway admin endpoints (`/actuator/gateway/**`) must not be internet-facing.
- ❌ **Leaking `Authorization` header** — Must strip before forwarding. Token harvesting risk.
- ❌ **Jackson 3 imports** — Custom filter code using `com.fasterxml.jackson` compiles but fails at runtime. Use `tools.jackson`.

### Verification Commands

```bash
# List all registered routes
curl http://localhost:8000/actuator/gateway/routes | jq

# Refresh routes (if using dynamic route source)
curl -X POST http://localhost:8000/actuator/gateway/refresh

# Test a route directly
curl -v http://localhost:8000/api/v1/ledger/health

# Test auth (should redirect to Keycloak)
curl -v https://gateway.panomete.com/api/v1/ledger/transactions

# Test with token
curl -H "Authorization: Bearer $(get_token)" https://gateway.panomete.com/api/v1/ledger/transactions

# Test rate limiting (send 201 requests quickly)
for i in $(seq 1 201); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -H "Authorization: Bearer $TOKEN" \
    https://gateway.panomete.com/api/v1/ledger/health &
done

# Check circuit breaker state
curl http://localhost:8000/actuator/health | jq .components.circuitBreakers

# Check Redis connectivity
docker exec flowero-gate redis-cli -h redis ping
```

---

## Related Documents

- [Flowero Guard](./Flowero%20Guard.md) — OAuth2 / Keycloak authentication system
- [Spring Boot API Gateway Checklist](spring-boot-api-gateway.md)
- [API Gateway Checklist](../project-checklist/api-gateway.md)
- [Spring Boot OAuth Checklist](spring-boot-oauth.md)
- [Web app for homelab](./Web%20app%20for%20homelab.md) — Project index

---

*Last updated: 2026-06-16*
