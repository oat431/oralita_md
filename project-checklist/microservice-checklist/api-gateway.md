# API Gateway Checklist

> The gateway is the front door to your system. Get it right, and everything behind it can be simpler.
> Last updated: 2026-06-11

---

## 1. Purpose & Scope — Decide What the Gateway Owns

- [ ] **Define gateway boundaries** — The gateway handles cross-cutting concerns. It does NOT contain business logic. Routing, auth, rate limiting, logging: yes. Order validation, payment processing: no.
- [ ] **Single entry point** — All external traffic flows through the gateway. No service exposes its port directly to the internet. Internal service-to-service can bypass (mesh) or go through (centralized).
- [ ] **North-south vs east-west** — Gateway handles north-south (external → internal). Service mesh (Istio, Linkerd, Consul Connect) handles east-west (internal → internal). Don't force internal traffic through the external gateway unless you have a specific reason.

## 2. Technology Choice

- [ ] **Evaluate against your stack** — Spring Cloud Gateway if you're in the Spring ecosystem. Kong if you want plugin marketplace + Lua extensibility. Traefik if you want auto-discovery + containers. Envoy if you need maximum performance + xDS control plane. NGINX if you want battle-tested simplicity. KrakenD if you want stateless + high performance.
- [ ] **Deployment model** — Sidecar proxy per service, standalone gateway cluster, or both? Sidecar = more operational overhead but better isolation. Centralized = simpler ops but single point of failure.
- [ ] **Configuration model** — Static config (YAML/JSON), dynamic config (API/admin endpoint), or GitOps (declarative in repo)? Dynamic is essential for zero-downtime route changes. GitOps gives audit trail.
- [ ] **High availability** — At least 2 instances behind a load balancer. Stateless (or shared state via Redis) so any instance can handle any request. If the gateway has state (rate limit counters), it must survive instance failure.

## 3. Routing & Service Discovery

- [ ] **Route definition strategy** — Path-based (`/api/users/**` → user-service), header-based, subdomain-based, or a combination. Path is most common and most readable.
- [ ] **Service discovery integration** — Consul, Eureka, Kubernetes DNS, or static host list. Gateway must pick up new instances and drop dead ones automatically. No manual IP lists.
- [ ] **Route ordering & precedence** — Define explicit ordering rules. More specific routes before wildcards. `/api/users/admin` before `/api/users/**`. Test route matching table.
- [ ] **Route versioning** — `/v1/**` → v1 services, `/v2/**` → v2 services. Or header-based: `Accept: application/vnd.api.v2+json`. Decide before v1 ships.
- [ ] **Catch-all route** — 404 handler that returns standardized error format. Not a blank page or raw nginx 404.
- [ ] **Route testing** — Automated tests that verify every route resolves to the correct upstream. Part of CI pipeline.

## 4. Authentication & Authorization

- [ ] **Auth at the edge** — Validate JWT tokens, API keys, or OAuth2 tokens at the gateway. Downstream services receive verified claims (`X-User-Id`, `X-User-Roles`), not raw tokens.
- [ ] **JWT validation** — Verify signature, issuer, audience, and expiry. Fetch JWKS from the auth server (with caching). Reject expired/invalid tokens with 401.
- [ ] **Token passthrough decision** — Strip the `Authorization` header before forwarding, or pass it through? Strip for security (downstream can't leak tokens). Pass through if downstream needs to introspect for fine-grained auth.
- [ ] **API key management** — Hashed in DB (like passwords). Identifiable prefix (`gw_`). Scoped to specific services/endpoints. Rotatable and revocable from admin API.
- [ ] **mTLS for service-to-service** — If internal services call each other through the gateway, use mTLS. Client certificates identify the calling service.
- [ ] **OAuth2/OpenID Connect** — If user-facing: authorization code flow with PKCE. Token refresh handled at gateway. Session management at gateway, not in each service.
- [ ] **Role-based access at route level** — `roles: ["admin"]` on admin routes. `roles: ["user"]` on user routes. Reject at gateway, not in 15 different services.

## 5. Rate Limiting & Throttling

- [ ] **Layered rate limiting** — Global (all requests), per-IP, per-user/token, per-endpoint, per-service. Most restrictive wins.
- [ ] **Algorithm choice** — Token bucket (burst-friendly), sliding window (accurate), fixed window (simplest, but edge spikes), or leaky bucket (smooth). Token bucket is the sweet spot for most APIs.
- [ ] **Rate limit headers** — `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`. RFC 6585 `429 Too Many Requests` with standardized body.
- [ ] **Rate limit storage** — Redis (shared across gateway instances) or in-memory (per-instance, looser). Redis for production multi-instance gateways.
- [ ] **Different limits for different clients** — Internal services get higher limits. Free-tier users get lower. Auth endpoint gets strictest (5/min).
- [ ] **Rate limit bypass for health checks** — Don't rate-limit `/health`, `/ready`, or internal monitoring endpoints.

## 6. Load Balancing

- [ ] **Algorithm** — Round-robin for uniform services, least-connections for variable-latency, consistent-hashing for sticky sessions (avoid if possible), weighted for heterogeneous instances.
- [ ] **Health checks** — Active (gateway pings `/health`) and passive (observe failures). Unhealthy instances removed from pool. Healthy instances re-added when they recover.
- [ ] **Sticky sessions** — Avoid if you can (makes instances stateful). If unavoidable (legacy WebSocket app): cookie-based or IP-hash. Document why it's needed.
- [ ] **Connection pooling to upstream** — HTTP keep-alive, connection pool sizing. Don't open a new connection per request.
- [ ] **Timeout tuning** — Connect timeout, read timeout, idle timeout. Shorter than client timeout to avoid hanging connections. Default: connect 3s, read 30s.

## 7. Request/Response Transformation

- [ ] **Header manipulation** — Add `X-Request-Id` (trace ID), `X-Forwarded-For`, `X-Real-IP`, `X-Forwarded-Proto`. Strip internal headers (`X-Internal-*`) before forwarding to clients.
- [ ] **Request body validation** — Basic schema validation at the edge: required fields, content-type, max body size. Reject garbage before it hits your services. But don't duplicate full business validation.
- [ ] **Response transformation** — Strip internal headers. Add `X-Response-Time`. Standardize error response format regardless of which service errored.
- [ ] **Request/response logging** — Log at gateway level: method, path, status, latency, client IP, user ID. Services can log less.

## 8. CORS & Security Headers

- [ ] **CORS at the gateway** — One place, consistent across all services. Specific origins (not `*`). Specific methods. `Access-Control-Allow-Credentials: true` only if needed.
- [ ] **Security headers** — `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 0` (deprecated, use CSP), `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`.
- [ ] **Content-Security-Policy** — Set at gateway for consistency. Start with `Content-Security-Policy-Report-Only` to gather violations before enforcing.
- [ ] **Cache-Control defaults** — Sensible defaults per content type. APIs: `no-store` by default. Override per route where caching is intentional.

## 9. Observability

- [ ] **Trace ID propagation** — Generate or propagate `X-Request-Id` / `traceparent` at the gateway. Every downstream service logs it. Every log line, every error, every metric tagged with it.
- [ ] **Structured logging** — JSON logs. Fields: timestamp, trace_id, method, path, status, latency_ms, client_ip, user_id, upstream_service, upstream_latency_ms.
- [ ] **Metrics (RED)** — Rate (requests/sec), Errors (5xx rate), Duration (p50/p95/p99). Per route, per upstream service, per client. Prometheus endpoint or push to gateway.
- [ ] **Distributed tracing** — OpenTelemetry. Gateway is the root span for external requests. Propagate context to upstream services. Jaeger/Tempo/Grafana for visualization.
- [ ] **Access logs** — Not raw text. Structured, shipping to centralized log system (Loki, ELK, Datadog). Include request body on errors (truncated, never log passwords/tokens).

## 10. Caching

- [ ] **Cacheable responses** — GET requests for static/semi-static resources. Cache-Control headers from upstream or configured at gateway.
- [ ] **Cache invalidation** — Purge by URL pattern. Purge by tag. Admin endpoint or API for CI/CD pipeline (purge on deploy).
- [ ] **Cache storage** — Redis (shared, survives restarts) or in-memory (fastest, lost on restart). Redis for production.
- [ ] **Bypass for authenticated requests** — `Authorization` header present → skip cache (unless explicitly designed for shared cache).
- [ ] **Cache stampede protection** — `LOCK` on cache miss, one request fills, others wait. Or probabilistic early recompute.

## 11. Resilience Patterns

- [ ] **Circuit breaker** — Stop calling a failing upstream after N failures. Open → half-open (probe) → closed (healthy) → open (failing again). Per-service, not global.
- [ ] **Retry with backoff** — Only for idempotent requests (GET, PUT, DELETE). Exponential backoff + jitter. Max retries (3). Max total time (shorter than client timeout).
- [ ] **Timeout per route** — Different services have different SLA expectations. Reports might take 30s, auth should take 200ms.
- [ ] **Bulkhead** — Limit concurrent requests to each upstream. Prevents one slow service from consuming all gateway threads/connections.
- [ ] **Fallback responses** — Cached stale response, degraded response (`{ "status": "degraded" }`), or hard error. Better than a 504 timeout.
- [ ] **Graceful degradation** — If user profile service is down, show homepage without avatar. Gateway can return partial data or stripped response via fallback.

## 12. API Versioning

- [ ] **Versioning at gateway level** — Route `/v1/**` → v1 upstream, `/v2/**` → v2 upstream. Services don't need version-aware routing logic.
- [ ] **Deprecation headers** — `Sunset: Sat, 31 Dec 2026 23:59:59 GMT`, `Deprecation: true`, `Link: <.../v2/docs>; rel="deprecation"`. Warn API consumers before breaking.
- [ ] **API version in metrics** — Track usage by version. Know when v1 traffic drops low enough to retire.
- [ ] **Documentation per version** — Aggregated OpenAPI docs per version at gateway. Developer portal shows all available versions.

## 13. Documentation & Developer Portal

- [ ] **OpenAPI aggregation** — Gateway aggregates specs from all upstream services. Single `/openapi.json` endpoint or developer portal URL.
- [ ] **Developer portal** — API catalog, try-it-out console, API key management, usage analytics. Kong Dev Portal, Tyk Portal, or custom.
- [ ] **Changelog** — Document every route change, deprecation, new version. Automated from CI/CD pipeline or manually maintained.
- [ ] **Onboarding guide** — Quickstart: how to get an API key, make a request, handle errors, find docs. 5 minutes to first successful call.

## 14. Security (Beyond Auth)

- [ ] **TLS termination** — Gateway terminates TLS. Internal traffic over HTTP or mTLS (depending on network trust). Minimum TLS 1.2, prefer 1.3.
- [ ] **Certificate management** — Auto-renew via Let's Encrypt / cert-manager. Expiry alerts. No manual certificate rotation.
- [ ] **Request size limits** — Max body size (e.g., 10MB default, higher for specific upload endpoints). Prevents memory exhaustion.
- [ ] **IP allowlisting/blocking** — Admin endpoints: internal IPs only. Known malicious IPs: blocked at gateway. Geo-blocking if your service is regional.
- [ ] **DDoS protection** — Rate limiting is your first line. WAF rules for common attack patterns (SQLi, XSS). CDN layer (Cloudflare, AWS CloudFront) for volumetric attacks.
- [ ] **Input sanitization** — Basic SQLi/XSS pattern rejection at gateway. Defense in depth — services also sanitize. But catching garbage at the door saves service resources.
- [ ] **Admin API security** — Gateway's own management API: separate port (not internet-facing), mTLS, strong auth. Never expose gateway admin on the public internet.

## 15. Configuration & GitOps

- [ ] **Declarative config in git** — Gateway routes, policies, plugins defined as code. PR review process for changes. Audit trail of who changed what and when.
- [ ] **Environment separation** — dev/staging/production configs. Different rate limits, different upstreams, different TLS certs. Same code, different values.
- [ ] **Config validation** — Schema validation on gateway config. CI step that validates config before merge. Dry-run mode to test config changes.
- [ ] **Zero-downtime config reload** — Changing routes should not drop active connections. Graceful reload, not restart.
- [ ] **Secret management** — TLS certs, API keys, upstream credentials from vault/secrets manager. Never in plain text in gateway config. Reference secrets by path (`${vault:secret/gateway/tls-cert}`).

## 16. Testing

- [ ] **Route tests** — Every route resolves correctly. `GET /api/users/123` → user-service:8080. Test route precedence, wildcards, regex routes.
- [ ] **Auth tests** — Valid token → 200. Expired token → 401. Missing token → 401. Invalid signature → 401. Wrong role → 403.
- [ ] **Rate limit tests** — Burst N requests → N succeed, N+1 gets 429. Wait for window reset → succeeds again. Headers present on all responses.
- [ ] **Circuit breaker tests** — Upstream fails N times → circuit opens → requests fail fast (not timeout waiting). Upstream recovers → circuit half-opens → probe succeeds → circuit closes.
- [ ] **Integration tests** — Gateway + real upstreams (testcontainers or docker-compose). End-to-end request flow: client → gateway → service → DB → response.
- [ ] **Load tests** — k6 or locust. Realistic traffic patterns through gateway. Measure gateway overhead: request through gateway vs direct to service. Should be minimal (<5ms p95).

## 17. Deployment & Operations

- [ ] **Stateless gateway instances** — Shared state (rate limits, sessions) in Redis. Any instance can die without losing data. Horizontal scaling is just adding instances.
- [ ] **Graceful shutdown** — SIGTERM → stop accepting new connections → drain existing connections (up to timeout) → close → exit. Kubernetes `terminationGracePeriodSeconds` aligned with drain timeout.
- [ ] **Resource limits** — CPU and memory limits in K8s. Gateway is CPU-bound (TLS, routing, transformation), not memory-heavy. Start with 1 CPU, 512Mi, adjust from metrics.
- [ ] **Anti-affinity rules** — Spread gateway pods across nodes. If a node dies, you lose only one instance.
- [ ] **Backup & restore** — Gateway config backed up in git (GitOps). Redis data (rate limits, sessions): acceptable to lose on restart or persist + backup for strict SLAs.
- [ ] **Disaster recovery** — Gateway config deploys from git to any environment. Spin up new gateway cluster in minutes, not hours.

## 18. Monitoring & Alerting

- [ ] **Golden signals dashboard** — Latency, traffic, errors, saturation. Per route, per upstream service. Grafana dashboard as code.
- [ ] **Alerts** — 5xx rate > 1%, p95 latency > threshold, upstream health checks failing, circuit breaker open, rate limit hits spike, TLS cert expiring < 7 days, gateway instance count < minimum.
- [ ] **SLO/SLI** — Define: 99.9% availability, p95 latency < 100ms at gateway, < 0.1% error rate. Measure. Alert when burning error budget too fast.
- [ ] **Capacity planning** — Track requests/sec per gateway instance. Know your ceiling. Auto-scale before you hit it.

---

## Quick Sanity Check Before Going Live

- [ ] All routes resolve and return correct upstream
- [ ] Auth is enforced on all non-public routes
- [ ] Rate limiting is active and tested
- [ ] TLS is terminated with valid certificates
- [ ] Health checks work and unhealthy upstreams are removed
- [ ] Structured logs include trace_id on every line
- [ ] Metrics exporting to Prometheus/Datadog
- [ ] Circuit breakers tested (kill an upstream, verify fast-fail)
- [ ] Gateway admin API is NOT internet-facing
- [ ] Config is in git, deployable to a fresh environment
- [ ] Graceful shutdown tested (rolling restart with zero errors)
- [ ] Documentation/developer portal is live

---

## Tech-Specific Quick Reference

### Spring Cloud Gateway (Java)
- Route definition in `application.yml` or `RouteLocator` beans
- `GatewayFilter` for cross-cutting logic (auth, logging, transformation)
- Integrates naturally with Spring Security + OAuth2
- Circuit breaker via Resilience4j
- Rate limiting with `RequestRateLimiter` + Redis
- Service discovery with Eureka or Consul
- Reactive (WebFlux) — make sure your filters are non-blocking

### Kong
- Declarative config (`kong.yml`) or Admin API
- Plugin marketplace: rate limiting, auth, transformations, logging
- Custom plugins in Lua or Go (PDK)
- Built-in developer portal
- DB-less mode for GitOps (config in file, no Postgres)
- Good for multi-team API management

### Traefik
- Auto-discovery from Docker, K8s, Consul, Etcd labels/annotations
- Let's Encrypt auto-TLS
- Middleware chain: rate limit, circuit breaker, headers, auth
- Dashboard with route visualization
- Best for container-native environments

### Envoy
- Maximum performance (C++), designed for high-throughput
- xDS control plane (Istio, consul-connect, custom)
- Rich L7 features: retry, timeout, circuit breaking, outlier detection
- Operational complexity is higher than Kong/Traefik
- Best for service mesh or performance-critical centralized gateway

### NGINX / OpenResty
- Battle-tested, massive community
- Lua scripting via OpenResty for custom logic
- Simple static config or dynamic via NGINX Plus / controller
- Less API-management features out of box (build or buy)
- Best when you want simplicity and trust the most-deployed web server on earth

### KrakenD
- Stateless, no database needed
- Config as single `krakend.json` file
- Built-in aggregation, filtering, transformation
- Good for BFF (Backend for Frontend) patterns
- Lower operational overhead than Kong/Envoy
