# Spring Boot API Gateway Checklist

> Spring Cloud Gateway-specific companion to the general [API Gateway Checklist](api-gateway.md).
> Covers Boot 4.0+ (Spring Framework 7, Spring Cloud 2025.x, Security 7 reactive, modular starters).
> Last updated: 2026-06-11

---

## 1. Project Setup & Dependencies

- [ ] **Spring Boot version** — Boot 4.x + Spring Cloud 2025.x release train. Check [compatibility matrix](https://spring.io/projects/spring-cloud) — Boot 4 requires Spring Cloud 2025.x+.
- [ ] **Gateway starter** — `spring-cloud-starter-gateway`. Reactive (WebFlux/Netty) stack only. Do NOT add `spring-boot-starter-webmvc` — it conflicts. `spring-boot-starter-webflux` only.
- [ ] **Modular starter awareness** — Boot 4 modularization applies. Security on gateway: `spring-boot-starter-security` (reactive auto-config). Redis: `spring-boot-starter-data-redis-reactive`. Actuator: `spring-boot-starter-actuator`. Jackson 3: package is `tools.jackson`.
- [ ] **No embedded Tomcat for gateway** — Gateway runs on Netty (reactive). Servlet-based starters don't belong here.
- [ ] **BOM** — Spring Cloud BOM in dependency management.
- [ ] **JSON serialization** — Jackson 3 is default. Custom Jackson code: update imports to `tools.jackson`. Gateway error responses, route config processing all go through Jackson.

## 2. Route Configuration

- [ ] **Choose: YAML or programmatic** — `application.yml` for static/simple routes. `RouteLocator` beans (`@Bean public RouteLocator customRouteLocator(RouteLocatorBuilder builder)`) for dynamic/complex routes. YAML for clean separation, programmatic for conditional routes or multi-environment variance.
- [ ] **Route structure in YAML**:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service          # lb:// for load-balanced
          predicates:
            - Path=/api/v1/users/**
          filters:
            - StripPrefix=1               # removes /api from path before forwarding
            - name: RequestRateLimiter    # named filter with args
              args:
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 200
```

- [ ] **Predicates** — `Path`, `Method`, `Host`, `Header`, `Query`, `Cookie`, `Before`/`After`/`Between` (time-based), `Weight` (canary routing), `RemoteAddr` (IP filtering). Chain predicates: all must match (AND logic).
- [ ] **Route ordering** — `order` property. Lower number = higher precedence. Default is 0. Be explicit: admin routes `order: -1`, catch-all `order: 100`.
- [ ] **Catch-all for unknown routes** — `- id: fallback` with `Path=/**` and `order: 9999`. Returns standardized 404 JSON. Not blank Netty error page.
- [ ] **`lb://` for service discovery** — `uri: lb://service-name`. Requires `spring-cloud-starter-loadbalancer`. Uses Spring Cloud LoadBalancer (not the deprecated Netflix Ribbon).

## 3. Filters — The Real Power

- [ ] **`GatewayFilter` vs `GlobalFilter`** — `GatewayFilter` per-route (rate limit, rewrite path, add header). `GlobalFilter` applies to all routes (auth check, trace ID propagation, logging). Know when to use which.
- [ ] **Built-in filters you'll actually use**:
  - `StripPrefix` — removes `/api` before forwarding to upstream
  - `PrefixPath` — adds prefix (e.g., upstream expects `/users` not just `/`)
  - `AddRequestHeader` — `X-User-Id`, `X-Trace-Id`
  - `RemoveRequestHeader` — strip internal headers before forwarding
  - `AddResponseHeader` — `X-Response-Time`, HSTS, CORS
  - `RewritePath` — regex path transformation
  - `SetStatus` — force specific response status (e.g., on maintenance mode)
  - `Retry` — retry failed requests to upstream (only idempotent methods)
  - `CircuitBreaker` — Resilience4j integration
  - `RequestRateLimiter` — Redis-backed rate limiting
  - `RequestSize` — max request body size
- [ ] **Custom filters** — `implements GatewayFilter, Ordered` or `implements GlobalFilter, Ordered`. For logic not covered by built-in filters. `Ordered` determines execution order — auth filters first (0-100), logging after (1000+).
- [ ] **Filter ordering matters** — `Ordered.getOrder()`. Typical chain: Security (0) → Rate Limiter (1) → Routing (Gateway's own at `Integer.MAX_VALUE`) → Logging (after routing). Test the filter sequencing.

## 4. Authentication at the Gateway (Security 7 Reactive)

- [ ] **Spring Security with WebFlux** — `spring-boot-starter-security` (reactive variant auto-configured). `SecurityWebFilterChain` bean, not `SecurityFilterChain`. `ServerHttpSecurity` config. `authorizeHttpRequests()` removed — use the lambda DSL.
- [ ] **CSRF — enabled by default for APIs** — Spring Security 7 enables CSRF for ALL endpoints. Gateway APIs must explicitly disable if stateless: `.csrf(ServerHttpSecurity.CsrfSpec::disable)`. Or configure `CsrfWebFilter` for cookie-based scenarios.
- [ ] **JWT validation at edge** — `spring-boot-starter-security-oauth2-resource-server` (reactive, renamed in Boot 4). `spring.security.oauth2.resourceserver.jwt.issuer-uri`. Gateway validates JWT → forwards claims as headers (`X-User-Id`, `X-User-Roles`) to downstream services.
- [ ] **Header passthrough** — After JWT validation: extract claims → add headers → strip `Authorization` header. Downstream services trust headers from gateway only (mTLS or internal network).
- [ ] **Custom `Principal` extraction** — `ReactiveAuthenticationManager` + `ServerSecurityContextRepository` if not using OAuth2 Resource Server. `ServerWebExchange` for accessing request context.
- [ ] **Unauthenticated routes** — Permit health checks, public endpoints: `.pathMatchers("/actuator/**", "/api/v1/public/**").permitAll()`. Everything else: `.anyExchange().authenticated()`.
- [ ] **API key auth** — Custom `AuthenticationWebFilter` in filter chain. Validate API key from header → set `SecurityContext` with service principal.

## 5. Service Discovery & Load Balancing

- [ ] **Service discovery** — Eureka (`spring-cloud-starter-netflix-eureka-client`) or Consul (`spring-cloud-starter-consul-discovery`). Or Kubernetes-native: just use `kube-dns` service names with `lb://`.
- [ ] **K8s without service discovery server** — If you don't need Eureka/Consul: `uri: http://service-name.namespace.svc.cluster.local:8080` works. Trade-off: static routing, no automatic instance tracking. Good enough for simple setups.
- [ ] **LoadBalancer** — `spring-cloud-starter-loadbalancer`. Replaces Ribbon. `@LoadBalanced` for `WebClient.Builder`. `lb://service-name` URIs. Health-check based instance selection.
- [ ] **Sticky sessions** — Spring Cloud LoadBalancer supports `SpringCloudLoadBalancer` hint-based. But prefer stateless services. Sticky sessions at gateway mean you can't freely scale upstream instances.

## 6. Rate Limiting

- [ ] **Redis-backed** — `spring-boot-starter-data-redis-reactive`. `RequestRateLimiter` GatewayFilter requires Redis. Configure `ReactiveRedisConnectionFactory` bean. Redis cluster or sentinel for production.
- [ ] **Rate limiter configuration** — `redis-rate-limiter.replenishRate` (tokens per second), `redis-rate-limiter.burstCapacity` (max burst). `redis-rate-limiter.requestedTokens` (how many tokens each request consumes, default 1).
- [ ] **Key resolver** — `KeyResolver` bean: by principal name, IP, API key, or composite. `exchange -> Mono.just(exchange.getRequest().getRemoteAddress().getHostName())`. Custom key resolver for per-tenant rate limiting.
- [ ] **Rate limit exceeded response** — Custom `WebFilter` or `ServerCodecConfigurer` to return standardized 429 JSON. Default response is empty 429 — not helpful.
- [ ] **Rate limit headers** — `X-RateLimit-Remaining`, `X-RateLimit-Replenish-Rate`, `X-RateLimit-Burst-Capacity`. Set in response via custom filter. Clients need to see their limits.

## 7. Circuit Breaker & Resilience

- [ ] **Resilience4j** — `spring-cloud-starter-circuitbreaker-reactor-resilience4j`. Not Hystrix (EOL). Circuit breaker on gateway routes: `CircuitBreaker` GatewayFilter.
- [ ] **Circuit breaker config** — `slidingWindowSize`, `failureRateThreshold` (%), `waitDurationInOpenState` (half-open probe delay), `permittedNumberOfCallsInHalfOpenState`. Tune per downstream service.
- [ ] **Fallback response** — `fallbackUri: forward:/fallback/user-service` when circuit is open. Create a `@RestController` on `/fallback/**` returning degraded response. Better than 504 timeout.
- [ ] **Retry** — `Retry` GatewayFilter. Only for idempotent methods (GET, PUT, DELETE). `retries: 3`, `statuses: BAD_GATEWAY, SERVICE_UNAVAILABLE, GATEWAY_TIMEOUT`. Exponential backoff in series.
- [ ] **Timeout** — `spring.cloud.gateway.httpclient.response-timeout: 30s`. Global default. Per-route override via metadata or custom filter. Shorter than client timeout.

## 8. CORS at the Gateway

- [ ] **Global CORS** — `spring.cloud.gateway.globalcors.cors-configurations.[/**].allowedOrigins: "https://app.example.com"`. Not `"*"`. One place, all routes.
- [ ] **Or programmatic CORS** — `CorsConfigurationSource` bean. But the `globalcors` YAML config is cleaner for declarative setups.
- [ ] **Credentials** — `allowCredentials: true` only if needed. Must NOT be combined with `allowedOrigins: "*"` (browser rejects this combination).

## 9. Observability

- [ ] **Actuator on gateway** — `/actuator/gateway/routes` — list all routes. `/actuator/gateway/globalfilters`. `/actuator/gateway/routefilters`.
- [ ] **Route refresh** — `/actuator/gateway/refresh` — reload routes without restart. Works with dynamic route sources (Redis, database).
- [ ] **OpenTelemetry starter** — `spring-boot-starter-opentelemetry` (new in Boot 4). First-party observability for gateway. Traces, metrics, logs to OTel collector.
- [ ] **Trace ID propagation** — Generate `traceparent` at gateway. Gateway is the root span for all external requests.
- [ ] **Metrics** — `spring-boot-starter-micrometer-metrics` + Prometheus. Gateway-specific: `spring.cloud.gateway.requests` timer (tagged by routeId, status, outcome).
- [ ] **Structured logging** — JSON logs with routeId, method, path, status, latency. `ReactiveWebFilter` for request/response logging. Log bodies on error only (never auth headers).

## 10. Security (Gateway-Specific)

- [ ] **No admin endpoints on public port** — Gateway actuator `/actuator/gateway/**` must NOT be externally accessible. Separate management port (`management.server.port: 8081`) or restrict to internal IPs.
- [ ] **Strip sensitive headers** — `RemoveRequestHeader` filter: `Authorization`, `Cookie`, `X-Internal-*` before forwarding from external clients. Never leak internal headers to clients either.
- [ ] **Request size limits** — `RequestSize` GatewayFilter: `maxSize: 10MB`. Or `spring.codec.max-in-memory-size`. Prevents memory exhaustion from oversized requests.
- [ ] **DDoS considerations** — Rate limiting is your first line. `spring.cloud.gateway.httpclient.max-headers-size`, `max-initial-line-length` for header bomb protection. WAF at edge (before gateway) for volumetric attacks.
- [ ] **mTLS between gateway and upstream** — `spring.cloud.gateway.httpclient.ssl.*` for configuring trust store. Upstream services verify gateway's client certificate. Defense in depth.

## 11. Testing Gateway Routes

- [ ] **`@SpringBootTest` with `webEnvironment = RANDOM_PORT`** — Full integration: real Netty server, real routes. `TestRestTemplate` or `WebTestClient` (reactive) for making requests.
- [ ] **`WebTestClient`** — `@SpringBootTest` + `@AutoConfigureWebTestClient`. Bind to running server: `webTestClient = WebTestClient.bindToServer().baseUrl("http://localhost:" + port).build()`. Then `webTestClient.get().uri("/api/v1/users").exchange().expectStatus().isOk()`.
- [ ] **Route-specific tests** — Test route matching: valid path → 200, invalid path → 404. Test predicates: Method predicate (POST vs GET), Header predicate. Test filter chains: rate limiting, auth checks.
- [ ] **Mock upstream** — WireMock or MockServer as fake upstream. Gateway routes to `http://localhost:${wiremock.port}` instead of real service. Full control over upstream responses.
- [ ] **Circuit breaker tests** — Upstream returns 500 for N consecutive requests → gateway opens circuit → subsequent requests get fallback response. Verify `Retry-After` header or fallback body.
- [ ] **Rate limit tests** — Send N+1 requests where N = burst capacity → N+1 gets 429. Wait for replenish → request succeeds. Verify rate limit headers.

## 12. Deployment

- [ ] **Stateless** — All state in Redis (rate limits, sessions). Gateway instances are fully disposable. Horizontal scaling: just add replicas.
- [ ] **Resource limits** — Gateway is CPU-bound (TLS handshake, routing, JSON parsing). Memory mostly for connection buffers. Start: 1 CPU, 512Mi. Monitor and tune.
- [ ] **Anti-affinity** — Spread gateway pods across K8s nodes. PodAntiAffinity with `topologyKey: kubernetes.io/hostname`.
- [ ] **Graceful shutdown** — `server.shutdown: graceful`. Drain active connections before Netty shutdown. `spring.lifecycle.timeout-per-shutdown-phase: 30s`.

## 13. Route Management at Scale

- [ ] **Dynamic routes for multi-team** — Don't hardcode 50 team routes in `application.yml`. Use `RedisRouteDefinitionRepository` (routes stored in Redis, live-reloadable). Or custom `RouteDefinitionRepository` backed by DB.
- [ ] **Route versioning strategy** — Route `/v1/**` → v1 services, `/v2/**` → v2. Gateway handles version routing, services stay simple. Or header-based: `X-API-Version: 2024-01-01`.
- [ ] **Canary routing** — `Weight` predicate: `- Weight=group1, 95` and `- Weight=group2, 5`. 5% traffic to canary group. Promoted gradually via config change.
- [ ] **Route documentation** — Every route explicated: what it does, what auth it requires, rate limits, which team owns it. Gateway route table IS your API documentation index.

---

## Quick Sanity Check Before Launch

- [ ] No `spring-boot-starter-webmvc` on classpath (WebFlux/Netty only)
- [ ] CSRF explicitly configured for API endpoints (enabled or disabled with clear reasoning)
- [ ] All routes have explicit `order` set — no reliance on declaration order
- [ ] Auth filter validates JWT before any request reaches an upstream
- [ ] `Authorization` header stripped before forwarding to internal services
- [ ] Rate limiting configured and tested with Redis (reactive Redis client)
- [ ] Circuit breaker opens on upstream failure (tested with Resilience4j)
- [ ] `/actuator/gateway/**` not accessible from external network
- [ ] CORS allows specific origins, not `*`
- [ ] Trace ID generated on every request, propagated to upstream (W3C traceparent)
- [ ] Structured logging with routeId, traceId, latency
- [ ] Graceful shutdown tested (rolling restart with zero errors)
- [ ] Catch-all route returns standardized 404 JSON (not Netty default)
- [ ] Gateway is stateless — no local state that breaks on restart
- [ ] Jackson 3 imports verified if custom filters serialize/deserialize JSON

---

## Common Gotchas (Updated for Boot 4)

- ❌ **Mixing Web MVC and WebFlux** — Adding `spring-boot-starter-webmvc` alongside Gateway = `IllegalStateException`. Gateway is reactive-only.
- ❌ **CSRF blocking all API calls** — Spring Security 7 enables CSRF for APIs by default. Stateless APIs return 403 until `.csrf().disable()` is added.
- ❌ **`authorizeRequests()` removed** — Security 7 fully removes `authorizeRequests()`. Use the lambda DSL: `.authorizeHttpRequests(auth -> auth.pathMatchers(...).permitAll())`.
- ❌ **Blocking in filters** — `Thread.sleep()` or blocking JDBC calls in a GatewayFilter = reactor thread blocked. All gateway filters must be non-blocking. Use `.flatMap()`, `.then()`, reactive Redis, reactive HTTP clients.
- ❌ **`@EnableEurekaClient`** — Not needed. Auto-configured. Adding it manually can break service registration.
- ❌ **`lb://` without LoadBalancer** — `lb://user-service` requires `spring-cloud-starter-loadbalancer`. Without it: `UnknownHostException`.
- ❌ **Rate limiter without Redis** — `RequestRateLimiter` requires Redis. Without it: `BeanCreationException` or silent failure.
- ❌ **Order confusion** — `Ordered.getOrder()` returns int. LOWER numbers execute FIRST. `Ordered.HIGHEST_PRECEDENCE = Integer.MIN_VALUE`.
- ❌ **Forgetting `- StripPrefix`** — Route: `Path=/api/v1/users/**`, upstream: `/users`. Without `StripPrefix=1`, request reaches upstream as `/api/v1/users/123` → 404.
- ❌ **Jackson 3 import mismatch** — Custom filters with `com.fasterxml.jackson` imports compile but may fail at runtime. Update to `tools.jackson`.
