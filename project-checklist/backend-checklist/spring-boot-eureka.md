# Spring Boot Eureka — Service Discovery Checklist

> Service Discovery implementation with Spring Cloud Netflix Eureka for Spring Boot 4.x microservices.
> Covers Boot 4.0+ (Spring Framework 7, Spring Cloud 2025.x). Docker-focused for self-hosted homelabs.
> Read the concept-level [Microservice Infrastructure Checklist](microservice-infrastructure.md) (Part 1) first for patterns and decisions.
> Last updated: 2026-06-11

---

## 1. Eureka Server Setup

> The registry. One project, one job: track which services are alive and where.

- [ ] **Separate Spring Boot project** — Eureka server is its own codebase. Don't embed it in another service. It has one dependency, one config file, one job.
- [ ] **Dependency**:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

- [ ] **`@EnableEurekaServer`** — on the main class. That's it. No other annotations needed.
- [ ] **Standalone mode** — For homelab: single Eureka server, no peer replication needed. If you grow to multiple hosts, add a peer. But start with one.

```yaml
# application.yml
server:
  port: 8761

spring:
  application:
    name: eureka-server

eureka:
  instance:
    hostname: eureka.panomete.local
    prefer-ip-address: true
  client:
    register-with-eureka: false       # Don't register yourself
    fetch-registry: false             # No peers to fetch from
  server:
    enable-self-preservation: true
    eviction-interval-timer-in-ms: 5000
```

- [ ] **Why `prefer-ip-address: true`?** — In Docker, container hostnames are random (`a3f9c2bd1e8f`) and unresolvable between containers. IP addresses on a shared Docker network work reliably.
- [ ] **Self-preservation explained** — When Eureka can't heartbeat with >15% of registered instances, it stops evicting anyone. This prevents a network blip from nuking your entire registry. Instances may appear UP but be dead — always check `/actuator/health` on the actual service, not just the dashboard.
- [ ] **Dashboard** — `http://eureka-server:8761` shows all registered instances, their status, uptime, and last heartbeat. Your first debugging stop for "why can't X reach Y?"

### 1.1 Eureka Server Security

- [ ] **Add basic auth** — `spring-boot-starter-security` on the Eureka server. Restrict `/eureka/**` endpoints.

```java
@Bean
public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    return http
        .csrf(CsrfConfigurer::disable)
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/actuator/health/**").permitAll()
            .requestMatchers("/eureka/**").authenticated()
            .anyRequest().authenticated()
        )
        .httpBasic(Customizer.withDefaults())
        .build();
}
```

- [ ] **Client credentials** — Services include credentials in `eureka.client.serviceUrl.defaultZone`: `http://user:pass@eureka-server:8761/eureka/`.

### 1.2 Eureka Server in Docker

```yaml
eureka-server:
  build: ./eureka-server
  container_name: eureka-server
  environment:
    SERVER_PORT: "8761"
  networks:
    - microservices-net
  healthcheck:
    test: "curl -f http://localhost:8761/actuator/health || exit 1"
    interval: 15s
    timeout: 5s
    retries: 5
```

- [ ] **No host port mapping** — Eureka stays internal. Only Traefik gets public ports. Services on the same Docker network reach it at `http://eureka-server:8761`.
- [ ] **Health check** — `curl` the actuator endpoint. Docker Compose `depends_on` with `condition: service_healthy` ensures services wait for Eureka to be ready.

---

## 2. Eureka Client Setup (Every Service)

- [ ] **Dependency** — `spring-cloud-starter-netflix-eureka-client` on every service that should be discoverable or needs to discover others.
- [ ] **No `@EnableEurekaClient`** — Auto-configured since Spring Cloud 2020.x. Adding it manually can double-register the service or break deregistration on shutdown.
- [ ] **Client config**:

```yaml
spring:
  application:
    name: user-service           # ← This becomes the service ID in Eureka.
                                 #   Must match lb://user-service in Gateway routes.
eureka:
  instance:
    prefer-ip-address: true
    instance-id: ${spring.application.name}:${random.value}
    lease-renewal-interval-in-seconds: 30
    lease-expiration-duration-in-seconds: 90
  client:
    service-url:
      defaultZone: http://eureka-server:8761/eureka/
    registry-fetch-interval-seconds: 30
```

- [ ] **`spring.application.name` is critical** — This is the service ID. If Gateway routes to `lb://user-service` but your service is named `user-svc`, it fails with `UnknownHostException`. Be consistent.
- [ ] **`instance-id: ${spring.application.name}:${random.value}`** — Uniquely identifies each instance. Without `random.value`, running 2 instances of the same service with the same default instance-id = only one shows in Eureka.
- [ ] **Heartbeat timing** — `lease-renewal-interval-seconds: 30` (service says "I'm alive" every 30s). `lease-expiration-duration-in-seconds: 90` (Eureka evicts if no heartbeat for 90s). 3 missed heartbeats = eviction. Adjust for your network reliability.

### 2.1 Graceful Lifecycle

- [ ] **Health check awareness** — `eureka.client.healthcheck.enabled: true`. Eureka reads `/actuator/health`. Status `DOWN` = removed from registry. This prevents routing to a service that's running but can't serve traffic (DB down, Redis unreachable).
- [ ] **Graceful registration** — Service registers on `ApplicationReadyEvent`, not during bean initialization. This means all beans are wired, DB connections are pooled, caches are warm before the service accepts traffic.
- [ ] **Graceful deregistration** — On shutdown, the service tells Eureka "I'm leaving" so it's removed immediately instead of waiting for heartbeat timeout.

```java
// Optional explicit deregistration. Spring Cloud auto-handles this,
// but if you have custom shutdown logic:
@PreDestroy
public void deregister() {
    eurekaClient.shutdown();
}
```

- [ ] **Graceful shutdown timeout** — Align Spring's shutdown with Docker's:

```yaml
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s

server:
  shutdown: graceful
```

### 2.2 Using Service Discovery for Inter-Service Calls

- [ ] **`@LoadBalanced` WebClient** — The clean way to call other services by logical name:

```java
@Configuration
public class WebClientConfig {
    @Bean
    @LoadBalanced
    public WebClient.Builder loadBalancedWebClientBuilder() {
        return WebClient.builder();
    }
}
```

Usage: `webClientBuilder.build().get().uri("http://user-service/api/v1/users/123")`.

- [ ] **How resolution works** — `user-service` → Spring Cloud LoadBalancer intercepts → queries Eureka for `user-service` instances → picks one (round-robin) → resolves to actual `10.0.1.5:8080`. Zero hardcoded URLs.
- [ ] **Requires `spring-cloud-starter-loadbalancer`** — Without it, `lb://` or `@LoadBalanced` calls fail with `UnknownHostException`.

### 2.3 Client in Docker

```yaml
user-service:
  build: ./user-service
  environment:
    EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eureka-server:8761/eureka/
  networks:
    - microservices-net
  healthcheck:
    test: "curl -f http://localhost:8080/actuator/health || exit 1"
    interval: 30s
    timeout: 10s
    retries: 3
  depends_on:
    eureka-server:
      condition: service_healthy
```

- [ ] **Env var override** — `EUREKA_CLIENT_SERVICEURL_DEFAULTZONE` overrides `application.yml`. Useful per-environment. But don't rely on env vars for everything — keep sensible defaults in YAML.
- [ ] **`depends_on: condition: service_healthy`** — Service waits for Eureka to be healthy before starting. Without this, the service starts, fails to register, and retries (it recovers, but startup logs are noisy).

---

## 3. Eureka in Gateway Routes

- [ ] **Gateway uses `lb://` URIs** — Not `http://host:port`:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service       # ← lb:// not http://
          predicates:
            - Path=/api/v1/users/**
        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/v1/orders/**
```

- [ ] **Gateway is itself a Eureka client** — It needs `spring-cloud-starter-netflix-eureka-client` + `spring-cloud-starter-loadbalancer`. It registers itself (so services can callback to Gateway if needed) and fetches the registry to resolve routes.
- [ ] **Route ID ≠ service name** — The route `id` is for documentation and actuator. The `uri: lb://user-service` is what resolves to actual instances. They don't need to match.

---

## 4. Debugging Service Discovery

- [ ] **Eureka dashboard** — `http://eureka-server:8761`. Shows:
  - **System Status** — UP/DOWN of the Eureka server itself
  - **Instances currently registered** — by `spring.application.name`
  - **Status per instance** — UP, DOWN, STARTING, OUT_OF_SERVICE, UNKNOWN
  - **Last heartbeat** — when each instance last checked in
- [ ] **Gateway actuator** — `/actuator/gateway/routes` shows all routes and whether they resolve. `/actuator/health` includes Eureka client health.
- [ ] **Common symptoms and causes**:

| Symptom | Likely Cause |
|---------|-------------|
| Service not in Eureka dashboard | `prefer-ip-address` missing or wrong. Eureka client dependency missing. `spring.application.name` not set. |
| Service appears but Gateway can't route | `lb://` URI missing `spring-cloud-starter-loadbalancer`. Service name mismatch (`user-service` vs `user-svc`). |
| Service appears UP but requests fail | Health check not enabled. Service registers before beans are ready. Enable `eureka.client.healthcheck.enabled`. |
| All services disappear from dashboard | Eureka self-preservation kicked in (network blip). Check actual `/actuator/health` on services. |
| Multiple instances, but only one shows | `instance-id` not unique. Add `${random.value}`. |

---

## 5. Eureka Gotchas

- ❌ **`@EnableEurekaClient` manually added** — Auto-configured since Spring Cloud 2020.x. Adding it can double-register or prevent deregistration.
- ❌ **Forgetting `prefer-ip-address: true` in Docker** — Services register with container hostnames (`a3f9c2bd1e8f`) that nothing can resolve.
- ❌ **`spring.application.name` mismatch** — The name in `application.yml` IS the service ID. Gateway `lb://user-service` + service named `user-svc` = `UnknownHostException`.
- ❌ **`instance-id` not unique** — Running 2 replicas without `${random.value}` in `instance-id` = only one shows in Eureka.
- ❌ **Not waiting for health** — Service registers and receives traffic before `ApplicationReadyEvent`. Requests fail with 503. Enable `eureka.client.healthcheck.enabled: true`.
- ❌ **Eureka server port conflict** — 8761 is the convention, not a hard rule. But if you change it, update every client's `defaultZone`.
- ❌ **Self-preservation panic** — Seeing instances in dashboard that you know are dead? Self-preservation mode. It's a feature, not a bug. Check actual service health endpoints.
- ❌ **Eureka server in same project as a service** — Don't. Separate project, separate container, separate concerns. The registry is infrastructure, not application code.
- ❌ **Gateway without Eureka client** — Gateway needs `spring-cloud-starter-netflix-eureka-client` to resolve `lb://` URIs. Without it, routes silently fail.

---

## Quick Sanity Check

- [ ] Eureka server running, dashboard accessible at `http://eureka-server:8761`
- [ ] All services have `prefer-ip-address: true`
- [ ] `instance-id` includes `${random.value}` for uniqueness
- [ ] Services appear in Eureka dashboard within 30s of startup
- [ ] Services deregister within 90s of shutdown (or immediately on graceful shutdown)
- [ ] `eureka.client.healthcheck.enabled: true` on all services
- [ ] Gateway routes use `lb://` not `http://`
- [ ] `spring-cloud-starter-loadbalancer` on Gateway and any service using `@LoadBalanced`
- [ ] No `@EnableEurekaClient` manually added anywhere
- [ ] Eureka dashboard secured with basic auth
- [ ] Graceful shutdown configured: `server.shutdown: graceful` + `spring.lifecycle.timeout-per-shutdown-phase`

---

## Related Checklists

- [Microservice Infrastructure](microservice-infrastructure.md) — Concepts: client-side vs server-side discovery, AP vs CP, build vs adopt
- [Spring Boot Microservice Infrastructure](spring-boot-microservice-infrastructure.md) — Integration overview: architecture diagram, full Docker Compose, startup sequence
- [Spring Boot Load Balancing](spring-boot-loadbalance.md) — Traefik + Spring Cloud LoadBalancer
- [Spring Boot OAuth](spring-boot-oauth.md) — Keycloak + Spring Security OAuth2
