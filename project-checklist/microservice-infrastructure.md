# Microservice Infrastructure Checklist

> Service Discovery, Load Balancing, and Open Authentication — the three pillars that turn a collection of services into a system.
> Framework-agnostic. For Spring Boot implementation, see [Spring Boot Microservice Infrastructure](./spring-boot-microservice-infrastructure.md).
> Last updated: 2026-06-11

---

## Why These Three?

You have services. They work in isolation. But in production:

- **Service A needs to call Service B** — but Service B has 3 instances on random ports. Hardcoding `http://localhost:8082` breaks the moment you scale or restart. → **Service Discovery**
- **Traffic arrives at your domain** — which instance handles it? What if that instance is overloaded? What if it dies mid-request? → **Load Balancing**
- **A request hits your API** — who is this? Should they see this data? Is that token real or forged? → **Open Authentication**

These three aren't optional at scale. They're the difference between a demo and a system.

---

## Part 1: Service Discovery

> The problem: services need to find each other without hardcoded addresses.

### 1.1 The Core Problem

- [ ] **You cannot hardcode service locations** — IPs change on redeploy. Ports are dynamic. Instances come and go. A service registry is the single source of truth for "what's running and where."
- [ ] **Registration** — Every service announces itself on startup: "I'm user-service, I'm at 10.0.1.5:8080, I'm healthy."
- [ ] **Deregistration** — Every service says goodbye on shutdown. If it crashes, the registry detects it via heartbeat timeout.
- [ ] **Discovery** — Services query the registry: "Give me all healthy instances of order-service." The list is always current.

### 1.2 Client-Side vs Server-Side Discovery

- [ ] **Client-side discovery** — The calling service queries the registry directly, picks an instance, and calls it. The caller owns the load-balancing decision.
  - **Pros:** No extra network hop. No load balancer SPOF (single point of failure). Simpler infrastructure.
  - **Cons:** Every service needs discovery client logic. Load balancing code duplicated across services. Tight coupling to the registry technology.
  - **Tools:** Netflix Eureka, Consul (with client library), Kubernetes DNS + client-side LB.
- [ ] **Server-side discovery** — The caller sends the request to a load balancer, which queries the registry and forwards the request. The caller doesn't know about the registry at all.
  - **Pros:** Caller is simpler (just send to a known LB). Centralized load balancing logic. Registry technology hidden from services.
  - **Cons:** Extra network hop (caller → LB → service). The load balancer becomes a critical component (needs HA). More infrastructure to manage.
  - **Tools:** AWS ALB, Traefik, NGINX Plus, Envoy + xDS control plane.
- [ ] **Hybrid** — Gateway for external traffic (server-side), client-side LB for internal service-to-service. This is the most common pattern and what most Spring Cloud setups use.

### 1.3 Key Decisions for Service Discovery

- [ ] **Self-hosted or cloud-managed?** — Cloud: AWS Cloud Map, GCP Service Directory. Self-hosted: Eureka, Consul, Zookeeper, Etcd. Self-hosted gives you control and zero per-request cost. Cloud-managed is less ops.
- [ ] **AP or CP?** — In distributed systems, you choose between Availability and Consistency during a network partition (CAP theorem).
  - **AP (Eureka):** Always available, might return stale data briefly. Better for runtime service lookup — slightly stale is better than no response.
  - **CP (Consul, Zookeeper, Etcd):** Strong consistency, might be unavailable during leader election. Better for configuration and locks than runtime routing.
- [ ] **Registry replication** — Single registry = SPOF. Production: at least 2-3 registry nodes. Eureka uses peer-to-peer replication. Consul uses Raft consensus. Know your registry's HA model.
- [ ] **Health checking** — Who checks health? The registry pinging services (server-side health check), or services reporting their own health (client-side heartbeat)? Heartbeats are lighter on the registry but slower to detect failures. Active health checks are faster to detect but add load.
- [ ] **Self-preservation** — When the registry can't reach many services, should it evict them (and potentially take down everything) or preserve the registry state (and risk routing to dead instances)? Eureka defaults to self-preservation mode. Know what your registry does under network partition.

### 1.4 Service Discovery Checklist

- [ ] Registry is highly available (at least 2 nodes for production)
- [ ] Services register on startup, deregister on graceful shutdown
- [ ] Heartbeat or health check interval configured (30s typical)
- [ ] Dead instances evicted within acceptable window (60-90s typical)
- [ ] Services use logical names, not IPs, when calling each other
- [ ] Registry dashboard or API accessible for debugging
- [ ] Registry data is ephemeral — services re-register on restart
- [ ] No business data stored in the registry (it's not a database)
- [ ] Registry secured (at minimum, basic auth on management endpoints)

---

## Part 2: Load Balancing

> The problem: distributing traffic across multiple service instances so no single instance gets overwhelmed.

### 2.1 Two Layers of Load Balancing

- [ ] **Layer 1: Edge (External → Internal)** — Traffic from the internet hits your edge load balancer first. It terminates TLS, applies WAF rules, and routes to your gateway. This is your front door.
  - **Tools:** Traefik, NGINX, HAProxy, Caddy, cloud LBs (ALB/NLB, Cloud Load Balancing).
- [ ] **Layer 2: Internal (Service → Service)** — When Service A calls Service B, which of B's 3 instances gets the request? Internal load balancing distributes inter-service traffic.
  - **Tools:** Client-side libraries (Spring Cloud LoadBalancer, gRPC client LB), sidecar proxies (Envoy, Linkerd), or centralized internal LBs.

### 2.2 Load Balancing Algorithms

- [ ] **Round-robin** — Each instance gets requests in turn. Simple, fair, no coordination needed. Default for most setups. Best when all instances are equal.
- [ ] **Least connections** — Send to the instance with fewest active connections. Better when some requests take longer than others (prevents slow-instance pile-up).
- [ ] **Weighted** — Assign different weights to instances. Use when instances have different sizes (4 vCPU vs 2 vCPU) or during canary deployments.
- [ ] **Consistent hashing** — Same client always goes to the same instance. Needed for sticky sessions. Avoid if possible — it makes instances stateful.
- [ ] **Latency-based** — Route to the fastest-responding instance. Useful for geo-distributed deployments or when instances have varying performance.
- [ ] **Adaptive** — Algorithm adjusts based on real-time metrics (error rate, latency). Complex but powerful for heterogeneous environments.

### 2.3 Health Checks & Failure Detection

- [ ] **Active health checks** — The load balancer periodically pings each instance's health endpoint (`GET /health`). Interval: 5-30s. Timeout: shorter than interval. Failed checks → mark unhealthy, stop routing.
- [ ] **Passive health checks** — The load balancer observes actual request outcomes. Too many 5xx responses → mark unhealthy. No extra traffic generated but slower to detect.
- [ ] **Outlier detection** — Not just "is it up?" but "is it behaving?" If one instance has 10x the latency of its peers, eject it even if it's technically "healthy."
- [ ] **Circuit breaking** — After N consecutive failures, stop sending requests to that instance entirely (open circuit). After a cooldown, send one probe request (half-open). If it succeeds, resume (closed). Prevents cascading failures.

### 2.4 Key Decisions for Load Balancing

- [ ] **Layer 7 (application) or Layer 4 (transport)?** — L7: route by URL path, headers, cookies. Can do auth, rate limiting, transformation. More CPU. L4: route by IP:port only. Faster, simpler, but can't do content-based routing. Edge LB: L7. Internal: L4 is often enough.
- [ ] **Centralized LB or client-side LB?** — Centralized: one load balancer handling all traffic. Simpler to configure, but adds a hop and is a potential bottleneck. Client-side: each service balances its own outgoing requests. More efficient for internal traffic but couples services to the LB library.
- [ ] **TLS termination location** — Terminate at edge LB (simplest, services get plain HTTP). Or pass-through to gateway (end-to-end encryption, but more CPU on each hop). Edge termination is standard; internal traffic over HTTP is acceptable on a trusted network.
- [ ] **Sticky sessions: yes or no?** — Sticky sessions make instances stateful — they break when instances die. Prefer stateless services with shared state in Redis/DB. Only use sticky sessions for legacy protocols (WebSocket without session replication) or specific caching strategies.

### 2.5 Load Balancing Checklist

- [ ] Edge LB is the ONLY entry point from the internet (no direct service exposure)
- [ ] TLS terminated at edge with valid certificates (auto-renewed)
- [ ] Health checks active on all upstream instances
- [ ] Unhealthy instances removed from pool automatically
- [ ] Request retry on connection failure (only for idempotent methods)
- [ ] Connection pooling enabled (HTTP keep-alive to backends)
- [ ] Timeouts configured: connect < read < client timeout
- [ ] Load balancing algorithm chosen with documented reasoning
- [ ] Sticky sessions avoided unless specifically justified
- [ ] Edge LB itself is not a SPOF (at least 2 instances, or cloud-managed HA)

---

## Part 3: Open Authentication (OAuth2 / OpenID Connect)

> The problem: verifying who is making a request, without every service managing its own user database.

### 3.1 The Core Concepts

- [ ] **Authentication (AuthN)** — Who are you? Proving identity: password, JWT, API key, SSO. "This is Panomete."
- [ ] **Authorization (AuthZ)** — What can you do? Permissions, roles, scopes. "Panomete can read users but not delete them."
- [ ] **OAuth2** — A delegation protocol. Allows a client to act on behalf of a user, or on its own behalf, with limited scope. OAuth2 is NOT an authentication protocol (that's OpenID Connect).
- [ ] **OpenID Connect (OIDC)** — A thin identity layer on top of OAuth2. Adds an `id_token` (JWT with user info). When people say "OAuth2 login," they usually mean OIDC.
- [ ] **JWT (JSON Web Token)** — A signed (or encrypted) token carrying claims: who issued it, who it's for, when it expires, what permissions it carries. Self-contained — the resource server validates it without calling the auth server.

### 3.2 OAuth2 Grant Types — Which One When

- [ ] **Authorization Code + PKCE** — User logs in via browser. Most secure for user-facing apps (SPA, mobile, server-rendered). The auth code is exchanged for tokens server-side. PKCE (Proof Key for Code Exchange) prevents authorization code interception. **This is what your Gateway uses when users log in.**
- [ ] **Client Credentials** — Service authenticates as itself (no user involved). Machine-to-machine communication. Service A gets a token, calls Service B. **This is what your services use to call each other.**
- [ ] **Refresh Token** — Long-lived token used to get new access tokens without re-login. Access tokens are short-lived (5-15 min), refresh tokens are long-lived (days/weeks). Refresh token rotation adds security (each refresh invalidates the old refresh token).
- [ ] **Device Code** — For input-constrained devices (TVs, IoT, CLI tools). User visits a URL on another device and enters a code.
- [ ] **Implicit (deprecated)** — Do not use. Tokens returned directly in the redirect URL (exposed to browser history, referrer headers). Use Authorization Code + PKCE instead.
- [ ] **Password (deprecated)** — Do not use. Client collects username/password directly. Defeats the purpose of OAuth2 (user shouldn't give credentials to the client).

### 3.3 Architecture Patterns for Auth

- [ ] **Pattern 1: Gateway does everything** — Gateway validates JWT, extracts claims, forwards as headers (`X-User-Id`, `X-User-Roles`). Downstream services trust the headers. No auth logic in services.
  - **Pros:** Services are simpler. Auth in one place. Easy to change auth strategy.
  - **Cons:** If a service is exposed directly (bypassing gateway), it has no auth. Headers can be spoofed if internal network isn't trusted.
- [ ] **Pattern 2: Every service validates JWT** — Gateway handles login flow, but each downstream service also validates the JWT independently (via JWKS key caching). No trust required between services.
  - **Pros:** Defense in depth. Services are secure even if gateway is bypassed. No header spoofing risk.
  - **Cons:** More configuration per service. Slightly more CPU (token validation is cheap after key is cached). Recommended for production.
- [ ] **Pattern 3: Token introspection** — Instead of JWT validation, services call the auth server's introspection endpoint for every request. The auth server confirms the token is still valid.
  - **Pros:** Can revoke tokens instantly (just mark them invalid at the auth server). No key management on services.
  - **Cons:** Network call to auth server on every request. Auth server becomes a hard dependency for every request. Latency. Use only when immediate token revocation is critical.

### 3.4 Token Management

- [ ] **Access token lifespan** — 5-15 minutes. Short enough that a stolen token can't be used for long. Long enough that refresh traffic doesn't overwhelm the auth server.
- [ ] **Refresh token lifespan** — Days to weeks. With rotation: each use issues a new refresh token and invalidates the old one. If a stolen refresh token is used, the legitimate user's next refresh will fail → detect the theft.
- [ ] **Token storage on client** — SPA: access token in memory (not localStorage — XSS can read it), refresh token in httpOnly secure cookie. Mobile: secure device storage (Keychain/Keystore). Server-rendered: session cookie.
- [ ] **Token revocation** — Can you revoke a token before it expires? JWT validation is stateless — the token is valid until it expires unless you check a revocation list. For immediate revocation, use token introspection or maintain a short-lived revocation list in Redis.
- [ ] **JWKS endpoint** — The auth server exposes its public keys at `/.well-known/openid-configuration/jwks`. Resource servers fetch and cache these keys. Key rotation: the auth server publishes a new key, old one is kept until all tokens signed with it expire. Smooth, no downtime.

### 3.5 Key Decisions for Open Authentication

- [ ] **Build vs Adopt** — Never build your own OAuth2/OIDC server. The specification is complex, the security edge cases are subtle, and getting it wrong means you ship a vulnerability. Use a battle-tested auth server: Keycloak (self-hosted, open-source), Auth0/Okta (SaaS), or cloud-specific (AWS Cognito, Azure AD B2C).
- [ ] **Stateless (JWT) vs Stateful (opaque tokens)** — JWT: services validate locally, no auth server call per request. But can't revoke instantly. Opaque tokens: must call introspection endpoint, but can revoke instantly. For most microservices, JWT + short lifespan is the right tradeoff.
- [ ] **One auth server for all services?** — Yes. One identity provider. One set of users. One login experience. Services differentiate by roles, scopes, and permissions — not by having different user databases.
- [ ] **Social login?** — Google, GitHub, Apple login via your auth server (Keycloak supports identity brokering). Don't implement social login directly in every service.
- [ ] **Multi-tenancy?** — If you serve multiple organizations, each gets an isolated realm/tenant in the auth server. Users from Tenant A cannot see Tenant B's data. Enforce at the auth and application layers.

### 3.6 Open Authentication Checklist

- [ ] Auth server is a dedicated service, not embedded in an application
- [ ] Authorization Code + PKCE for all user-facing login flows
- [ ] Client Credentials for all service-to-service calls
- [ ] Access tokens: short-lived (≤15 min), signed (RS256 or ES256)
- [ ] Refresh tokens: long-lived, rotated on each use
- [ ] JWKS endpoint available, keys cached by resource servers
- [ ] All tokens include: `iss` (issuer), `sub` (subject), `aud` (audience), `exp` (expiry), `iat` (issued at)
- [ ] Resource servers validate: signature, issuer, audience, expiry
- [ ] Roles/permissions encoded in JWT claims, not in a separate service call
- [ ] Auth server database is backed up regularly (it IS your user store)
- [ ] Auth server itself is behind TLS, with proper hostname configured
- [ ] Login events logged for audit trail (who logged in, when, from where)
- [ ] Rate limiting on login endpoints (prevent credential stuffing)
- [ ] No secrets in client-side code (client secrets live on the server)

---

## Part 4: How They Work Together

### 4.1 The Flow

```
1. DNS resolves api.example.com → Edge LB (Traefik/NGINX/cloud LB)
2. Edge LB terminates TLS, forwards to API Gateway
3. Gateway checks: is this request authenticated?
   - NO → redirect to Auth Server login (OAuth2 Authorization Code flow)
   - YES → validate JWT, extract user claims
4. Gateway asks Service Discovery: "where is user-service?"
   → Returns [10.0.1.5:8080, 10.0.1.6:8080, 10.0.1.7:8080] (healthy)
5. Gateway picks an instance (Load Balancing), forwards request + user context headers
6. Service validates JWT independently (JWKS cache), processes request
7. Response flows back: Service → Gateway → Edge LB → Client
```

- [ ] **Gateway is the integration point** — It uses Service Discovery to find backends, Load Balancing to pick healthy instances, and Auth to validate every request. The Gateway is where these three pillars converge.
- [ ] **No pillar is optional** — Without Service Discovery, you're hardcoding URLs. Without Load Balancing, one instance gets all traffic. Without Auth, anyone can call anything. Together they form the minimum viable production infrastructure.

### 4.2 Concerns NOT Covered Here

These are adjacent but separate concerns (covered in other checklists):

- **API Gateway** — Routing, rate limiting, transformation, CORS, versioning → [API Gateway Checklist](./api-gateway.md)
- **Observability** — Logging, metrics, distributed tracing → [Monitoring](../6-maintenance/MONITORING.md)
- **Service Mesh** — mTLS, traffic splitting, advanced routing → (future checklist)
- **Message Queues** — Async communication, event-driven architecture → covered in [API Checklist](./api.md) (Section: Message Queues)

---

## Part 5: Build vs Adopt Decision Matrix

| Concern | Build it yourself? | Why / Why Not |
|---------|-------------------|---------------|
| **Service Registry** | ❌ Don't build | Writing a distributed registry with heartbeats, eventual consistency, and split-brain handling is months of work. Use Eureka, Consul, or Kubernetes DNS. |
| **Client-side LB library** | ❌ Don't build | Framework provides it (Spring Cloud LoadBalancer, gRPC built-in). Writing connection pooling + retry + health checking yourself is reinventing the wheel. |
| **Edge Load Balancer** | ❌ Don't build | NGINX, Traefik, HAProxy, Caddy are battle-tested by billions of requests. Even the simplest self-built reverse proxy will have subtle bugs under load. |
| **OAuth2/OIDC Server** | ❌ NEVER build | OAuth2/OIDC is a security protocol with subtle edge cases: PKCE, token rotation, refresh token replay detection, JWT key rotation, consent screens. One mistake = vulnerability. Use Keycloak, Auth0, Okta, Cognito. |
| **JWT validation in services** | ✅ Use framework | Spring Security, Passport.js, middleware libraries. The validation logic is simple (check signature + claims), but use a well-maintained library — JWT parsing has footguns (alg=none attacks, timing attacks). |
| **Custom auth proxy** | ⚠️ Maybe | If you need a thin layer between your gateway and auth server (e.g., OAuth2 Proxy for legacy apps), tools exist (oauth2-proxy, Pomerium). Only build if nothing fits. |

---

## Technology Comparison

### Service Discovery

| Tool | Type | CAP | Operational Complexity | Best For |
|------|------|-----|------------------------|----------|
| **Netflix Eureka** | Client-side, AP | AP | Low — one Spring Boot app | Spring Boot shops, homelabs, simple setups |
| **HashiCorp Consul** | Both, CP | CP | Medium — agent on every host | Multi-platform, needs service mesh + KV store |
| **Kubernetes DNS + Service** | Server-side, built-in | CP | None (comes with K8s) | Already on Kubernetes |
| **etcd / Zookeeper** | Client-side, CP | CP | High — raw consensus primitive | Custom orchestration systems, not general-purpose SD |
| **AWS Cloud Map** | Server-side, managed | N/A | None (AWS managed) | AWS-only deployments |

### Edge Load Balancing

| Tool | Strength | Weakness | Best For |
|------|----------|----------|----------|
| **Traefik** | Auto-discovery (Docker, K8s), Let's Encrypt built-in, middleware chain | Smaller community than NGINX, less L4 features | Container-native environments |
| **NGINX / OpenResty** | Battle-tested, huge community, Lua scripting | Manual config reload, less auto-discovery | Static configs, advanced Lua scripting |
| **HAProxy** | Maximum L4/L7 performance, rich ACLs | Complex config syntax, steeper learning curve | High-throughput, custom routing rules |
| **Caddy** | Simplest config, auto-HTTPS, modern defaults | Smaller ecosystem, less enterprise adoption | Simple sites, internal tools |
| **Cloud ALB/NLB** | Zero ops, auto-scaling, integrated with cloud ecosystem | Cost at scale, limited customization, vendor lock-in | Cloud-native deployments |

### Authentication / OIDC

| Tool | Type | Cost | Best For |
|------|------|------|----------|
| **Keycloak** | Self-hosted, open-source | Free (your infrastructure) | Homelabs, self-hosted production, any scale |
| **Auth0 / Okta** | SaaS | Per-MAU pricing | Businesses that don't want to manage auth infra |
| **AWS Cognito** | Cloud-managed | Per-MAU (cheap at small scale) | AWS-only, simple use cases |
| **Azure AD B2C** | Cloud-managed | Per-MAU | Microsoft ecosystem, enterprise SSO |
| **ORY Hydra + Kratos** | Self-hosted, open-source | Free | Complex auth flows, OAuth2 purists |
| **Roll your own** | Self-built | Developer time + security risk | Never. Just don't. |

---

## Quick Sanity Check

### Service Discovery
- [ ] Can all services find each other without hardcoded URLs?
- [ ] Do new instances register automatically on startup?
- [ ] Are dead instances removed from the registry within 90s?
- [ ] Is the registry itself highly available?

### Load Balancing
- [ ] Is the edge LB the only thing exposed to the internet?
- [ ] Are unhealthy instances automatically removed from rotation?
- [ ] Is TLS terminated at the edge with auto-renewed certificates?
- [ ] Are timeouts configured at every layer?

### Open Authentication
- [ ] Does every request have a verified identity before reaching business logic?
- [ ] Are tokens short-lived with refresh token rotation?
- [ ] Are credentials and secrets stored outside source code?
- [ ] Is the auth server backed up regularly?

---

## Related Checklists

- [Spring Boot Microservice Infrastructure](./spring-boot-microservice-infrastructure.md) — Concrete implementation with Eureka, Traefik, Keycloak
- [API Gateway Checklist](./api-gateway.md) — Gateway-specific concerns (routing, rate limiting, CORS)
- [Spring Boot API Gateway Checklist](./spring-boot-api-gateway.md) — Spring Cloud Gateway implementation
- [Spring Boot API Checklist](./spring-boot-api.md) — Downstream service implementation
- [API Checklist](./api.md) — General API design patterns and security
