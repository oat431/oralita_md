# Spring Boot Load Balancing Checklist

> Edge Load Balancing with nginx or Traefik v3 + Internal Load Balancing with Spring Cloud LoadBalancer for Spring Boot 4.x microservices.
> Covers Boot 4.0+ (Spring Framework 7, Spring Cloud 2025.x). Docker-focused for self-hosted homelabs.
> Choose your edge LB — both are production-grade. nginx is simpler if you already run it; Traefik adds Docker auto-discovery.
> Read the concept-level [Microservice Infrastructure Checklist](microservice-infrastructure.md) (Part 2) first for algorithms and patterns.
> Last updated: 2026-06-12

---

## Two Layers, Two Jobs

```
Internet ──→ nginx/Traefik ──→ Gateway ──→ Service A
               │                         │
               │  Edge LB                │  Internal LB
               │  (external→internal)    │  (service→service)
               │                         │
               TLS termination           Eureka-powered
               HTTP→HTTPS redirect       @LoadBalanced WebClient
               Security headers          lb:// URIs
               Rate limiting
```

- **nginx / Traefik:** The front door. Everything from the outside world hits the edge LB first. TLS, domain routing, security headers. Pick one — both do the job well.
- **Spring Cloud LoadBalancer:** Internal traffic. When the Gateway (or any service) calls another service, LoadBalancer picks the healthiest instance. Client-side = zero extra hops.

---

## Part 1: Choose Your Edge Load Balancer

> You need ONE edge load balancer. Not both. nginx if you already run it and want zero new services. Traefik if you want Docker auto-discovery and built-in Let's Encrypt.

| Factor | nginx | Traefik |
|--------|-------|---------|
| **Best if** | Already running nginx, want simplicity | Container-native, want auto-discovery |
| **Config style** | Static config files (`.conf`) | Static file + Docker labels |
| **Docker awareness** | Manual `proxy_pass` to containers | Auto-discovers via Docker socket |
| **Let's Encrypt** | Manual certbot or separate setup | Built-in, auto-renew |
| **Learning curve** | Widest-known syntax on the web | YAML-based, smaller community |
| **Operational overhead** | Same (one binary, one config) | Same |

### Option A: Traefik

> Best for: starting fresh, container-native setups, auto-TLS without certbot. Every section below has an nginx equivalent.

### Option B: nginx

> Best for: you already run nginx, want zero new services, prefer the most battle-tested web server on earth.

---

## Part 1-A: Traefik — Edge Load Balancer

### 1.1 Why Traefik?

- **Docker auto-discovery** — New containers with `traefik.enable=true` labels are automatically routed. No config reload. No restart.
- **Let's Encrypt built-in** — TLS certificates auto-requested and auto-renewed. No certbot cron jobs.
- **Middleware chain** — Rate limiting, IP whitelisting, security headers, authentication — all composable.
- **Single binary, single config file** — No external database needed. Stateless.

### 1.2 Traefik Docker Compose

```yaml
traefik:
  image: traefik:v3.4
  container_name: traefik
  restart: unless-stopped
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro   # Docker provider (read-only)
    - ./traefik/config:/etc/traefik                   # Static config
    - ./traefik/certs:/certs                          # TLS certs (persist across restarts)
    - ./traefik/dynamic:/dynamic                      # Dynamic config (middleware, etc.)
  networks:
    - microservices-net
```

- [ ] **`/var/run/docker.sock:ro`** — Read-only. Traefik watches Docker events to discover containers. Security: if Traefik is compromised, read-only socket limits blast radius.
- [ ] **Cert storage** — Mount `/certs` as a volume so Let's Encrypt certificates survive container restarts. Without it, every restart requests new certs (rate limits apply).

### 1.3 Static Configuration

```yaml
# traefik/config/traefik.yml
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false           # ⚠️ Critical: only expose labeled containers
    network: microservices-net
  file:
    directory: /dynamic
    watch: true

certificatesResolvers:
  letsencrypt:
    acme:
      email: your-email@example.com
      storage: /certs/acme.json
      tlschallenge: true              # TLS-ALPN-01 on port 443
```

- [ ] **`exposedByDefault: false`** — Without this, EVERY container with a port becomes publicly routable. This is the #1 Traefik security mistake. Set to `false` and explicitly label which services get exposed.
- [ ] **HTTP→HTTPS redirect** — The `web` entrypoint only redirects. No plaintext traffic reaches your services.
- [ ] **TLS challenge** — `tlschallenge: true` uses TLS-ALPN-01 (port 443 only). Alternative: `httpchallenge` (port 80). TLS challenge is cleaner (no open port 80 needed after redirect), but some firewalls block it. If Let's Encrypt fails, switch to `httpchallenge`.
- [ ] **Dynamic config directory** — Middleware definitions, non-Docker routes, and other config that changes independently of Traefik itself. `watch: true` picks up changes without restart.

### 1.4 Service Labels

- [ ] **Gateway is the only exposed service** — Traefik routes all API traffic to Gateway. Not individual services. Gateway handles auth, routing, and internal LoadBalancing from there.

```yaml
api-gateway:
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.gateway.rule=Host(`api.panomete.com`)"
    - "traefik.http.routers.gateway.entrypoints=websecure"
    - "traefik.http.routers.gateway.tls=true"
    - "traefik.http.routers.gateway.tls.certresolver=letsencrypt"
    - "traefik.http.services.gateway.loadbalancer.server.port=8080"
```

- [ ] **Keycloak gets its own route** — Auth needs its own subdomain:

```yaml
keycloak:
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.keycloak.rule=Host(`auth.panomete.com`)"
    - "traefik.http.routers.keycloak.entrypoints=websecure"
    - "traefik.http.routers.keycloak.tls=true"
    - "traefik.http.routers.keycloak.tls.certresolver=letsencrypt"
    - "traefik.http.services.keycloak.loadbalancer.server.port=8080"
```

- [ ] **Services behind Gateway need NO Traefik labels** — They're only reachable through Gateway, which resolves them via Eureka internally. No public exposure.

### 1.5 Traefik Middleware

- [ ] **Middleware file** (`traefik/dynamic/middleware.yml`):

```yaml
http:
  middlewares:
    # Rate limiting at the edge
    rate-limit:
      rateLimit:
        average: 100
        burst: 200

    # Security headers on every response
    security-headers:
      headers:
        browserXssFilter: true
        contentTypeNosniff: true
        forceSTSHeader: true
        stsIncludeSubdomains: true
        stsPreload: true
        stsSeconds: 31536000
        customFrameOptionsValue: "SAMEORIGIN"
        referrerPolicy: "strict-origin-when-cross-origin"

    # IP whitelist for admin paths
    admin-ipwhitelist:
      ipWhiteList:
        sourceRange:
          - "192.168.1.0/24"       # Your home network
          - "10.0.0.0/8"            # Internal Docker network
```

- [ ] **Apply middleware to routers**:

```yaml
# On Gateway router:
- "traefik.http.routers.gateway.middlewares=rate-limit,security-headers"

# On Keycloak admin:
- "traefik.http.routers.keycloak.middlewares=admin-ipwhitelist"
```

- [ ] **Composable order** — Middleware chains execute in the order listed. Rate limiter before security headers makes sense (reject early, don't compute headers for rejected requests).

### 1.6 Traefik Dashboard & Observability

- [ ] **Enable dashboard on management port** (not public):

```yaml
# In traefik.yml
api:
  dashboard: true
  insecure: false         # Don't expose without auth

# Separate entrypoint for internal use
entryPoints:
  traefik:
    address: ":8080"
```

- [ ] **Secure the dashboard** — Basic auth middleware or IP restriction. Never expose Traefik dashboard on the public internet.
- [ ] **Access logs** — Structured JSON logs to stdout. Docker log driver collects them.

---

## Part 1-B: nginx — Edge Load Balancer

> If you already have nginx running on your host (serving `panomete.com`, proxying other services), you don't need Traefik. nginx is a full reverse proxy and handles everything the edge layer needs.

### Why nginx for the Edge?

- **Already running** — You have it. Zero new services, zero new config syntax to learn.
- **Battle-tested** — Powers ~30% of the internet. Every edge case is documented.
- **Simple config** — `server` blocks, `proxy_pass`, `add_header`. No Docker socket access needed.
- **Same capabilities as Traefik** — TLS termination, rate limiting, security headers, load balancing across Gateway instances.

### nginx Config for Microservices

```nginx
# /etc/nginx/sites-available/microservices.conf
# (symlink to /etc/nginx/sites-enabled/ on Debian/Ubuntu)

# ═══ Upstream: Gateway instances (load balance if scaled) ═══
upstream gateway {
    server 127.0.0.1:8080;       # Gateway container
    # Add more when scaling:
    # server 127.0.0.1:8081;
    # server 127.0.0.1:8082;

    # Optional: least_conn, ip_hash, or weighted
    # least_conn;
}

upstream keycloak {
    server 127.0.0.1:8443;       # Keycloak container
}

# ═══ API Gateway ═══
server {
    listen 443 ssl http2;
    server_name api.panomete.com;

    # TLS
    ssl_certificate     /etc/nginx/certs/api.panomete.com/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/api.panomete.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Rate limiting (10 req/s burst 20 per IP)
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # Proxy to Gateway
    location / {
        proxy_pass http://gateway;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";       # WebSocket support
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;
        proxy_send_timeout 30s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 16k;
    }
}

# ═══ Keycloak ═══
server {
    listen 443 ssl http2;
    server_name auth.panomete.com;

    ssl_certificate     /etc/nginx/certs/auth.panomete.com/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/auth.panomete.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # Stricter rate limit on login endpoints
    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;
    limit_req zone=auth_limit burst=10 nodelay;

    # IP-restrict admin paths
    location /admin {
        allow 192.168.1.0/24;        # Your home/office network
        allow 10.0.0.0/8;             # Internal Docker network
        deny all;

        proxy_pass http://keycloak;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://keycloak;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;
        proxy_send_timeout 30s;

        # Disable buffering for server-sent events (Keycloak uses them)
        proxy_buffering off;
    }
}

# ═══ HTTP → HTTPS redirect ═══
server {
    listen 80;
    server_name api.panomete.com auth.panomete.com;
    return 301 https://$host$request_uri;
}
```

- [ ] **`upstream` block** — Defines the Gateway instances. nginx load balances across them (default: round-robin). Add more `server` lines when you scale Gateway.
- [ ] **TLS certs** — Use certbot for Let's Encrypt: `certbot --nginx -d api.panomete.com -d auth.panomete.com`. Auto-renewal via systemd timer.
- [ ] **`X-Forwarded-*` headers** — Critical. Gateway and Keycloak need these to reconstruct the original request URL. Without them, redirect URIs break.
- [ ] **`proxy_buffering off` for Keycloak** — Keycloak uses server-sent events for admin console real-time updates. Buffering breaks SSE.
- [ ] **IP-restrict `/admin`** — Keycloak admin console should not be public. `allow` your network, `deny all` for everything else.
- [ ] **Separate `server` blocks per subdomain** — Cleaner than `if ($host = ...)` logic. One block per domain, clear routing rules.

### nginx + Certbot (Let's Encrypt)

- [ ] **Install certbot** — `apt install certbot python3-certbot-nginx` (Ubuntu/Debian).
- [ ] **Get certificates** — `certbot --nginx -d api.panomete.com -d auth.panomete.com`
- [ ] **Auto-renewal** — certbot installs a systemd timer automatically. Verify: `systemctl status certbot.timer`
- [ ] **Test renewal** — `certbot renew --dry-run`

### nginx Reload (Zero-Downtime)

```bash
# Test config syntax
nginx -t

# Apply without dropping connections
nginx -s reload
```

- [ ] **Always test before reload** — `nginx -t` catches syntax errors. A bad config + `nginx -s reload` = nginx refuses the new config but keeps running with the old one. Safe.

### nginx Docker Compose (If Not on Host)

If nginx isn't installed on the host, run it as a container:

```yaml
nginx:
  image: nginx:1.27
  container_name: nginx
  restart: unless-stopped
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - ./nginx/sites:/etc/nginx/sites-enabled:ro
    - ./nginx/certs:/etc/nginx/certs:ro
  networks:
    - microservices-net
```

---

## Part 2: Spring Cloud LoadBalancer — Internal Load Balancing

### 2.1 Why Not Just Use Traefik for Everything?

- Traefik is edge-only in this architecture. Internal service-to-service calls don't go through Traefik (extra hop, extra latency).
- Spring Cloud LoadBalancer is client-side — the calling service picks the instance. Zero extra network hops. Zero extra infrastructure.

### 2.2 Setup

- [ ] **Dependency** — `spring-cloud-starter-loadbalancer` on Gateway and any service that calls other services.
- [ ] **Gateway routes use `lb://`**:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service       # lb:// triggers LoadBalancer
          predicates:
            - Path=/api/v1/users/**
```

- [ ] **`@LoadBalanced` WebClient** for inter-service calls:

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

```java
// Usage in a service
@Service
public class OrderService {
    private final WebClient webClient;

    public OrderService(@LoadBalanced WebClient.Builder builder) {
        this.webClient = builder.build();
    }

    public UserDto getUser(String userId) {
        return webClient.get()
            .uri("http://user-service/api/v1/users/{id}", userId)
            .retrieve()
            .bodyToMono(UserDto.class)
            .block();
    }
}
```

- [ ] **How resolution works** — `user-service` → LoadBalancer intercepts → queries Eureka → returns `[10.0.1.5:8080, 10.0.1.6:8080]` → picks one (round-robin) → makes HTTP request to the resolved IP:port.

### 2.3 Load Balancing Strategy

- [ ] **Default: round-robin** — Each instance gets requests in turn. Simple, fair. Works for most cases.
- [ ] **Health-aware** — LoadBalancer only routes to instances Eureka marks as UP. Dead instances excluded automatically.
- [ ] **Custom strategy** — If you need weighted, zone-aware, or sticky-session routing:

```java
@Bean
public ReactorServiceInstanceLoadBalancer customLoadBalancer(
        ObjectProvider<ServiceInstanceListSupplier> supplierProvider) {
    return new RoundRobinLoadBalancer(
        supplierProvider,
        "user-service"
    );
    // Replace RoundRobinLoadBalancer with custom implementation
}
```

- [ ] **Retry on failure** — Enable retry for idempotent requests:

```yaml
spring:
  cloud:
    loadbalancer:
      retry:
        enabled: true
```

Combined with Spring Retry, a failed request to one instance is retried on another. Only for GET, PUT, DELETE.

### 2.4 Timeouts & Connection Pooling

- [ ] **Gateway HTTP client timeouts**:

```yaml
spring:
  cloud:
    gateway:
      httpclient:
        connect-timeout: 3000       # 3s to establish connection
        response-timeout: 30s       # 30s for upstream to respond
        pool:
          max-idle-time: 30s
          max-life-time: 60s
```

- [ ] **WebClient timeouts per call** — For services that call other services directly:

```java
WebClient.builder()
    .clientConnector(new ReactorClientHttpConnector(
        HttpClient.create()
            .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 3000)
            .responseTimeout(Duration.ofSeconds(30))
    ))
    .build();
```

- [ ] **Timeout hierarchy** — Client timeout > Gateway timeout > Upstream service timeout. If your SPA times out at 15s but Gateway waits 30s, the user gets a timeout while Gateway is still waiting. Align them.

---

## 3. No Direct Service Exposure

- [ ] **Edge LB is the ONLY entry point** — Whether nginx on the host or Traefik container, port 80/443 goes to the edge LB. Nothing else maps to host ports.
- [ ] **Services on internal Docker network only** — No `ports:` block in Docker Compose for services. Gateway, Eureka, business services all internal-only.
- [ ] **Gateway is the only entry point for APIs** — Edge LB → Gateway → Services. Not edge LB → Service A, edge LB → Service B.
- [ ] **Keycloak gets its own subdomain route** — Users need to reach Keycloak's login page at `auth.panomete.com`. Gateway redirects there for login.

---

## 4. Testing Load Balancing

- [ ] **Distribution test** — Start 2 instances of a service (different ports). Make 100 requests. Verify both received ~50 each.
- [ ] **Failover test** — Kill one instance mid-traffic. Verify requests continue without errors, routed to survivor.
- [ ] **Recovery test** — Restart the killed instance. Verify traffic redistributes to include it.
- [ ] **TLS test** — `curl -vI https://api.panomete.com/actuator/health`. Verify TLS 1.3, valid certificate chain.
- [ ] **HTTP→HTTPS redirect** — `curl -I http://api.panomete.com/actuator/health`. Verify 301/302 to HTTPS.
- [ ] **Security headers** — Check response headers include HSTS, XSS Protection, frame options, content-type options.

---

## 5. Load Balancing Gotchas

### Traefik
- ❌ **`exposedByDefault: true`** — Every container with a port becomes routable. Always set to `false`.
- ❌ **Routing directly to services** — Traefik → Service A, Traefik → Service B. Scatters auth, rate limiting, and routing logic across labels. Route everything through Gateway.
- ❌ **Cert storage not persisted** — `/certs` not mounted as volume → every restart = new Let's Encrypt request → hit rate limits → cert failures.
- ❌ **Wrong Docker network** — `network: microservices-net` in provider config must match the actual network services use.
- ❌ **Dashboard on public port without auth** — Anyone can see your infrastructure and routes. Use separate management port + IP restriction.

### nginx
- ❌ **Not testing config before reload** — `nginx -s reload` with bad syntax = nginx keeps running with old config but doesn't apply changes. Always `nginx -t` first.
- ❌ **Missing `X-Forwarded-*` headers** — Without `proxy_set_header X-Forwarded-Proto $scheme`, Keycloak thinks it's on HTTP and generates wrong redirect URIs. Login breaks.
- ❌ **`proxy_buffering on` for Keycloak** — Keycloak admin console uses server-sent events. Buffering breaks the real-time updates. Set `proxy_buffering off`.
- ❌ **Forgetting `ssl_certificate_key`** — nginx refuses to start if `ssl_certificate` is set but no `ssl_certificate_key`. Certbot handles this automatically, but manual certs need both.
- ❌ **Gateway `upstream` with Docker container name** — If nginx runs on the host (not in Docker), it can't resolve Docker container names. Use `127.0.0.1` with the container's published port, or run nginx inside Docker on the same network.

### Spring Cloud LoadBalancer
- ❌ **`lb://` without `spring-cloud-starter-loadbalancer`** — `UnknownHostException` at runtime. The starter is not auto-included.
- ❌ **`@LoadBalanced` on RestTemplate** — RestTemplate is in maintenance mode. Use WebClient.
- ❌ **Service name mismatch** — `lb://user-service` but Eureka has `user-svc`. The name in `spring.application.name` IS the ID. Case-sensitive.
- ❌ **Blocking calls with WebClient in servlet services** — `.block()` in a servlet controller is fine (there's a thread per request). Don't use `.block()` in WebFlux (Gateway filters).

---

## Quick Sanity Check

### Edge LB (nginx or Traefik — pick one)
- [ ] Edge LB is the ONLY entry point with port 80/443
- [ ] All services on internal Docker network only (no host port mapping)
- [ ] TLS terminated at edge with valid certificates (auto-renew verified)
- [ ] HTTP→HTTPS redirect active
- [ ] Security headers present on all responses (HSTS, XSS, frame options)
- [ ] X-Forwarded-* headers passed to Gateway and Keycloak
- [ ] Keycloak admin paths IP-restricted
- [ ] Edge LB config tested before applying (`nginx -t` or Traefik dry-run)
- [ ] If Traefik: `exposedByDefault: false`
- [ ] If Traefik: dashboard secured (IP-restricted or behind auth)
- [ ] If nginx: `proxy_buffering off` for Keycloak endpoints
- [ ] If nginx: `limit_req_zone` on auth endpoints (prevent brute force)

### Internal Load Balancing
- [ ] Gateway routes use `lb://` URIs
- [ ] `spring-cloud-starter-loadbalancer` on Gateway and inter-service callers
- [ ] `@LoadBalanced` WebClient configured (not RestTemplate)
- [ ] Response timeouts aligned: client > gateway > upstream
- [ ] Connection pooling enabled on Gateway HTTP client
- [ ] No direct edge LB → service routing (all through Gateway)

---

## Related Checklists

- [Microservice Infrastructure](microservice-infrastructure.md) — Concepts: edge vs internal LB, algorithms, health checks
- [Spring Boot Microservice Infrastructure](spring-boot-microservice-infrastructure.md) — Integration overview: architecture diagram, full Docker Compose, startup sequence
- [Spring Boot Eureka](spring-boot-eureka.md) — Service Discovery with Eureka
- [Spring Boot OAuth](spring-boot-oauth.md) — Keycloak + Spring Security OAuth2
- [Spring Boot API Gateway](spring-boot-api-gateway.md) — Gateway filters, rate limiting, CORS
