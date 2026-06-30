# Flowero Guard — OAuth2 / OpenID Connect Authentication System

> **Code Name:** Flowero guardian  
> **Domain:** auth.panomete.com  
> **Status:** ✅ Completed | ✅ Deployed  
> **Stack:** Keycloak 27.x + Spring Cloud Gateway (OAuth2 Client/Resource Server) + PostgreSQL  
> **Document Purpose:** Complete project specification and integration guide for all downstream microservices.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Tech Stack](#3-tech-stack)
4. [Infrastructure Setup](#4-infrastructure-setup)
5. [Keycloak Realm & Client Configuration](#5-keycloak-realm--client-configuration)
6. [JWT Token Specification](#6-jwt-token-specification)
7. [Gateway — OAuth2 Integration](#7-gateway--oauth2-integration)
8. [Downstream Service Integration](#8-downstream-service-integration)
9. [Service-to-Service Authentication](#9-service-to-service-authentication)
10. [Integration Checklist (for New Services)](#10-integration-checklist-for-new-services)
11. [Security & Operations](#11-security--operations)
12. [Troubleshooting & Gotchas](#12-troubleshooting--gotchas)

---

## 1. Overview

### What Flowero Guard Does

Flowero Guard is the centralized authentication and authorization backbone for all flowerogate microservices. It provides:

- **User authentication** — Login via Keycloak's login page (OIDC Authorization Code flow with PKCE)
- **Token issuance** — JWTs signed by Keycloak, validated by every service independently
- **Role-based access control** — Realm roles (`ROLE_USER`, `ROLE_ADMIN`) embedded in JWT claims
- **Service-to-service auth** — Client Credentials grant for programmatic service identity
- **Session management** — Refresh token rotation, configurable token lifespans
- **Single Sign-On** — One login works across all flowerogate services

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Keycloak** (not custom auth) | Battle-tested OIDC provider; built-in admin UI, user management, federation |
| **JWT validation at every service** | Defense in depth — a compromised gateway doesn't bypass auth |
| **Gateway strips Authorization header** | Downstream services never see raw tokens; prevents token harvesting |
| **Claims forwarded as X-User-\* headers** | Services don't have to parse JWTs in every controller |
| **15-min access token lifespan** | Short-lived = stolen token window minimized; refresh rotation handles UX |
| **Client Credentials for service-to-service** | No user impersonation; service identity is explicit via `sub` claim |

---

## 2. Architecture

```
                        ┌─────────────────────────────────────┐
                        │         External Requests            │
                        │   (Browser, Mobile, 3rd-party API)   │
                        └──────────────┬──────────────────────┘
                                       │ HTTPS
                                       ▼
                        ┌──────────────────────────────┐
                        │        Nginx (Edge)           │
                        │   TLS termination, routing     │
                        │   gateway.panomete.com         │
                        │   auth.panomete.com            │
                        └──────────┬──────────┬────────┘
                                   │          │
                          ┌────────▼──┐  ┌───▼──────────────┐
                          │  Keycloak │  │  Spring Cloud    │
                          │   :18080  │  │  Gateway          │
                          │           │  │  :8000            │
                          │  Token    │  │                   │
                          │  Issuer   │  │  OAuth2 Client    │
                          │           │  │  + Resource Srv   │
                          └─────┬─────┘  └────────┬──────────┘
                                │                  │
                                │ Postgres         │ JWT validated
                                │ (keycloak DB)    │ Claims → headers
                                │                  │
                                │          ┌───────┴──────────┐
                                │          │                  │
                                │    ┌─────▼──────┐   ┌──────▼─────┐
                                │    │ Service A  │   │ Service B  │
                                │    │ (ledger)   │   │ (shortlink)│
                                │    │ Resource   │   │ Resource   │
                                │    │ Server     │   │ Server     │
                                │    └────────────┘   └────────────┘
                                │          │                  │
                                │    JWKS cache         JWKS cache
                                │    (JWT validation    (JWT validation
                                │     w/out Keycloak     w/out Keycloak
                                │     call per req)      call per req)
                                │          │                  │
                                └──────────┴──────────────────┘
                                     (on startup only —
                                      fetches public key,
                                      caches indefinitely)
```

### Flow Summary

1. **Unauthenticated user** hits `https://gateway.panomete.com/api/v1/users`
2. **Gateway** (OAuth2 Client) → 302 redirect to `https://auth.panomete.com/realms/flowerogate/protocol/openid-connect/auth`
3. **User logs in** via Keycloak login page
4. **Keycloak** → 302 redirect back to `https://gateway.panomete.com/login/oauth2/code/keycloak?code=...`
5. **Gateway** exchanges authorization code for tokens (access + refresh)
6. **Gateway** stores session, validates JWT on subsequent requests
7. **Gateway** extracts claims → strips `Authorization` header → adds `X-User-Id`, `X-User-Name`, `X-User-Roles` headers → forwards to upstream service
8. **Upstream service** validates JWT independently (via cached JWKS key) OR trusts gateway headers (config-dependent)

---

## 3. Tech Stack

| Component | Technology | Version | Notes |
|-----------|-----------|---------|-------|
| Identity Provider | Keycloak | 27.x | Production mode (`start`, not `start-dev`) |
| Database | PostgreSQL | 16+ | Dedicated `keycloak` database |
| Gateway OAuth2 Client | Spring Security 7 (reactive) | Boot 4.x | `spring-boot-starter-security-oauth2-client` |
| Gateway Resource Server | Spring Security 7 | Boot 4.x | JWT validation via JWKS |
| Service Resource Server | Spring Security 7 (servlet) | Boot 4.x | `spring-boot-starter-security-oauth2-resource-server` |
| Service-to-Service | OAuth2 Client Credentials | — | `spring-boot-starter-security-oauth2-client` on caller |
| Token Format | JWT (RS256) | — | Asymmetric signing (public/private key pair) |
| Container | Docker Compose | — | All services on `microservices-net` |

---

## 4. Infrastructure Setup

### 4.1 Keycloak Docker Compose

```yaml
keycloak:
  image: keycloak/keycloak:27.0
  container_name: keycloak
  restart: unless-stopped
  environment:
    KC_DB: postgres
    KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
    KC_DB_USERNAME: keycloak
    KC_DB_PASSWORD: ${KC_DB_PASSWORD}
    KC_HOSTNAME: auth.panomete.com
    KC_PROXY_HEADERS: xforwarded       # ⚠️ Critical behind Nginx
    KEYCLOAK_ADMIN: admin
    KEYCLOAK_ADMIN_PASSWORD: ${KC_ADMIN_PASSWORD}
  command: start                       # ⚠️ NOT start-dev
  networks:
    - microservices-net
  depends_on:
    postgres:
      condition: service_healthy
  ports:
    - "18080:18080"                     # Internal only; Nginx routes external traffic
```

### 4.2 Nginx Reverse Proxy for Keycloak

```nginx
# Nginx reverse proxy config for Keycloak
server {
    listen 443 ssl http2;
    server_name auth.panomete.com;

    ssl_certificate     /etc/nginx/ssl/auth.panomete.com/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/auth.panomete.com/privkey.pem;

    # Restrict admin console to internal IPs
    location /admin {
        allow 192.168.1.0/24;
        allow 127.0.0.1;
        deny all;

        proxy_pass http://keycloak:18080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://keycloak:18080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4.3 Critical Environment Variables

| Variable | Purpose | Notes |
|----------|---------|-------|
| `KC_HOSTNAME` | Public-facing hostname | Must match `auth.panomete.com` — used in redirect URIs, issuer claims, OIDC discovery |
| `KC_PROXY_HEADERS` | Trust reverse proxy headers | `xforwarded` — Without this, login redirects to internal IP |
| `KEYCLOAK_ADMIN_PASSWORD` | Admin console password | Store in `.env`, never commit |
| `KC_DB_PASSWORD` | Postgres password | Store in `.env`, never commit |

---

## 5. Keycloak Realm & Client Configuration

### 5.1 Realm: `flowerogate`

All flowerogate services share one realm. A realm is a security boundary — users in realm A cannot access clients in realm B.

**Token Settings:**
- **Access Token Lifespan:** 5 minutes (300 seconds)
- **Refresh Token Lifespan:** 30 minutes (1800 seconds) — with rotation enabled, each use invalidates old token
- **SSO Session Idle:** 12 hours
- **SSO Session Max:** 72 hours

### 5.2 Client Registry

| Client ID | Type | Access Type | Purpose | Secret |
|-----------|------|-------------|---------|--------|
| `flowero-gateway` | OpenID Connect | Confidential | Gateway handles user login (auth code + PKCE) + owns `gateway-admin` resource role | `${KEYCLOAK_GATEWAY_SECRET}` |
| `service-ledger` | OpenID Connect | Confidential | Service-to-service auth (client credentials) | `${LEDGER_SERVICE_SECRET}` |
| `service-shortlink` | OpenID Connect | Confidential | Service-to-service auth | `${SHORTLINK_SERVICE_SECRET}` |
| `frontend-app` | OpenID Connect | Public | SPA/Nuxt (auth code + PKCE, no client secret) | *(none — public client)* |

> **Note:** The `flowero-gateway` client has a `gateway-admin` resource role under `resource_access.flowero-gateway.roles`.

### 5.3 Gateway Client (`flowero-gateway`) Settings

```
Client authentication: Client ID and Secret (confidential)
Valid redirect URIs:
  https://gateway.panomete.com/login/oauth2/code/*
  http://localhost:8000/login/oauth2/code/*  (local dev)
Valid post logout redirect URIs:
  https://gateway.panomete.com/
Web origins:
  https://gateway.panomete.com
  http://localhost:8000
```

### 5.4 Service Client (`service-<name>`) Settings

```
Client authentication: Client ID and Secret
Service accounts roles: Enabled (required for client credentials grant)
Redirect URIs: (none — services don't handle browser redirects)
```

### 5.5 Roles & Authorization

Flowero Guard uses **resource-level roles** (not realm roles) for service-specific authorization:

**Realm-level roles** (assigned to all users):
| Role | Source | Purpose |
|------|--------|---------|
| `offline_access` | `realm_access.roles` | Enables refresh token (offline token) |
| `default-roles-flowerogate` | `realm_access.roles` | Default realm role for all users |
| `uma_authorization` | `realm_access.roles` | User-Managed Access authorization |

**Resource-level roles** (service-specific):
| Role | Source | Purpose |
|------|--------|---------|
| `gateway-admin` | `resource_access.flowero-gateway.roles` | Gateway administrative access |

Example from actual JWT:

```json
{
  "realm_access": {
    "roles": ["offline_access", "default-roles-flowerogate", "uma_authorization"]
  },
  "resource_access": {
    "flowero-gateway": {
      "roles": ["gateway-admin"]
    },
    "account": {
      "roles": ["manage-account", "manage-account-links", "view-profile"]
    }
  }
}
```

Assign roles to users via Keycloak Admin UI → Users → Role Mapping.

### 5.6 Client Secret Management

1. **Retrieve:** Keycloak Admin → Clients → `<client-id>` → Credentials tab → Client Secret
2. **Store:** Environment variable (`.env` file), referenced as `${VARIABLE_NAME}` in `application.yml`
3. **Rotate:** Quarterly. Keycloak supports regenerating secrets. Update env vars + restart services.
4. **Never commit secrets** to source control.

---

## 6. JWT Token Specification

### 6.1 Token Structure

```json
{
  "iss": "https://auth.panomete.com/realms/flowerogate",
  "sub": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "aud": "flowero-gateway",
  "exp": 1718592000,
  "iat": 1718591100,
  "auth_time": 1718591000,
  "preferred_username": "panomete",
  "email": "oat431@outlook.com",
  "email_verified": true,
  "realm_access": {
    "roles": ["ROLE_USER", "ROLE_ADMIN"]
  },
  "scope": "openid profile email"
}
```

### 6.2 Key Claims Used by Services

| Claim | Path | Contains | Used By |
|-------|------|----------|---------|
| `sub` | `sub` | User UUID (Keycloak internal ID) | `X-User-Id` header |
| `preferred_username` | `preferred_username` | Human-readable username | `X-User-Name` header |
| `realm_access.roles` | `realm_access.roles` | `["ROLE_USER", "ROLE_ADMIN"]` | `X-User-Roles` header, `hasAuthority()` |
| `iss` | `iss` | Issuer URL | JWT validation (must match config) |
| `exp` | `exp` | Expiry timestamp | JWT validation (auto-checked by Spring) |
| `aud` | `aud` | Intended audience (client ID) | JWT validation (if enabled) |

### 6.3 Token Validation (How Services Verify)

Every downstream service validates JWTs **independently**:

1. Service reads `issuer-uri` from config → `https://auth.panomete.com/realms/flowerogate`
2. Spring Security fetches `/.well-known/openid-configuration` from issuer → discovers JWKS endpoint
3. Fetches Keycloak's public key from JWKS endpoint → **caches it**
4. Every request: validates JWT signature using cached public key → **zero network calls per request**
5. When Keycloak rotates keys, new key is fetched on next cache miss → automatic

---

## 7. Gateway — OAuth2 Integration

The Spring Cloud Gateway has a **dual role**:
- **OAuth2 Client** — Redirects unauthenticated users to Keycloak login
- **Resource Server** — Validates JWT on API requests

### 7.1 Gateway Dependencies

```xml
<!-- Spring Security (reactive, auto-configured for WebFlux) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<!-- OAuth2 Client (handles login flow) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-oauth2-client</artifactId>
</dependency>
```

### 7.2 Gateway OAuth2 Configuration

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak:
            client-id: flowero-gateway
            client-secret: ${KEYCLOAK_GATEWAY_SECRET}
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
            scope: openid,profile,email
        provider:
          keycloak:
            issuer-uri: https://auth.panomete.com/realms/flowerogate
            user-name-attribute: preferred_username
      resourceserver:
        jwt:
          issuer-uri: https://auth.panomete.com/realms/flowerogate
```

### 7.3 Gateway Security Filter Chain

```java
@Configuration
@EnableWebFluxSecurity
public class GatewaySecurityConfig {

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        return http
            // Security 7: CSRF enabled by default → disable for stateless JWT APIs
            .csrf(ServerHttpSecurity.CsrfSpec::disable)

            .authorizeHttpRequests(auth -> auth
                // Public: health checks, OAuth2 endpoints, public API
                .pathMatchers("/actuator/health/**").permitAll()
                .pathMatchers("/login/**", "/oauth2/**").permitAll()
                .pathMatchers("/api/v1/public/**").permitAll()
                // Everything else: authenticated
                .anyExchange().authenticated()
            )

            // OAuth2 login — redirects to Keycloak when unauthenticated
            .oauth2Login(Customizer.withDefaults())

            // JWT resource server — validates bearer tokens
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(Customizer.withDefaults())
            )

            .build();
    }
}
```

### 7.4 JWT Claim Propagation (Critical)

The gateway MUST:
1. Validate JWT via Spring Security
2. Extract user claims
3. Forward claims as `X-User-*` headers
4. **Strip `Authorization` header** before forwarding to upstream

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE + 10)
public class JwtClaimHeaderFilter implements GlobalFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        return ReactiveSecurityContextHolder.getContext()
            .map(ctx -> ctx.getAuthentication())
            .flatMap(auth -> {
                if (auth instanceof JwtAuthenticationToken jwtAuth) {
                    Jwt jwt = jwtAuth.getToken();

                    String userId = jwt.getSubject();
                    String username = jwt.getClaimAsString("preferred_username");

                    // Extract realm roles
                    Map<String, Object> realmAccess = jwt.getClaim("realm_access");
                    String roles = "";
                    if (realmAccess != null && realmAccess.get("roles") instanceof List<?> roleList) {
                        roles = roleList.stream()
                            .map(Object::toString)
                            .collect(Collectors.joining(","));
                    }

                    // Forward claims as headers
                    var request = exchange.getRequest().mutate()
                        .header("X-User-Id", userId)
                        .header("X-User-Name", username)
                        .header("X-User-Roles", roles)
                        .build();

                    // Strip Authorization header
                    var cleanedRequest = stripAuthorizationHeader(request);

                    return chain.filter(exchange.mutate().request(cleanedRequest).build());
                }
                return chain.filter(exchange);
            });
    }
}
```

**⚠️ Why strip `Authorization`?** If a downstream service is compromised, the attacker could harvest valid access tokens for every user whose requests passed through. Stripping the header at the gateway prevents this.

### 7.5 Downstream Headers (What Services Receive)

| Header | Example Value | Type |
|--------|--------------|------|
| `X-User-Id` | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` | UUID (Keycloak `sub`) |
| `X-User-Name` | `panomete` | String |
| `X-User-Roles` | `ROLE_USER,ROLE_ADMIN` | Comma-separated |

**No `Authorization` header.** Raw JWT is never forwarded.

---

## 8. Downstream Service Integration

### 8.1 Integration Mode Decision

Choose how your service handles auth:

| Mode | How It Works | Security | Complexity |
|------|-------------|----------|------------|
| **Option A: Trust Gateway Headers** | Read `X-User-*` headers; no JWT validation | ❌ Lower — if service is accidentally exposed directly, no auth | 🟢 Simplest |
| **Option B: Validate JWT (Recommended)** | Service validates JWT via JWKS key cache | ✅ Defense in depth | 🟡 Moderate |
| **Option C: Both (Pragmatic)** | Validate JWT for security; also read `X-User-*` for convenience | ✅ Best of both | 🟡 Moderate |

**Recommendation:** Option B or C. Always validate JWT independently. Trust headers only for convenience in controller code.

### 8.2 Dependencies (Spring Boot 4.x)

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-oauth2-resource-server</artifactId>
</dependency>
```

### 8.3 Resource Server Configuration

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.panomete.com/realms/flowerogate
```

That's it. Spring does the rest:
1. Discovers JWKS endpoint from issuer
2. Fetches and caches public key
3. Validates every JWT signature automatically
4. Handles key rotation transparently

### 8.4 Security Filter Chain (Servlet)

```java
@Configuration
@EnableWebSecurity
public class ResourceServerConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            // Security 7: CSRF on by default — disable for stateless APIs
            .csrf(CsrfConfigurer::disable)

            .authorizeHttpRequests(auth -> auth
                // Health check: no auth needed
                .requestMatchers("/actuator/health/**").permitAll()
                // Admin endpoints: ROLE_ADMIN only
                .requestMatchers("/api/v1/admin/**").hasAuthority("ROLE_ADMIN")
                // Everything else: authenticated
                .anyRequest().authenticated()
            )

            // JWT resource server
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(Customizer.withDefaults())
            )

            .build();
    }
}
```

### 8.5 Role Mapping

Map Keycloak realm roles to Spring Security authorities:

```java
@Bean
public JwtAuthenticationConverter jwtAuthenticationConverter() {
    JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter =
        new JwtGrantedAuthoritiesConverter();
    // Where roles live in Keycloak JWT
    grantedAuthoritiesConverter.setAuthoritiesClaimName("realm_access.roles");
    // Prefix: ROLE_USER, ROLE_ADMIN
    grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");

    JwtAuthenticationConverter jwtConverter = new JwtAuthenticationConverter();
    jwtConverter.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);
    return jwtConverter;
}
```

### 8.6 Accessing User Info in Controllers

**From SecurityContext (Option B/C):**

```java
@GetMapping("/api/v1/profile")
public ResponseEntity<?> getProfile(@AuthenticationPrincipal Jwt jwt) {
    String userId = jwt.getSubject();
    String username = jwt.getClaimAsString("preferred_username");
    // ...
}
```

**Or from Gateway headers (Option C):**

```java
@GetMapping("/api/v1/profile")
public ResponseEntity<?> getProfile(
        @RequestHeader("X-User-Id") String userId,
        @RequestHeader("X-User-Name") String username,
        @RequestHeader(value = "X-User-Roles", defaultValue = "") String roles) {
    // ...
}
```

### 8.7 Unauthenticated Endpoints

For public endpoints within an authenticated service:

```java
.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/v1/public/**").permitAll()
    .requestMatchers("/actuator/health/**").permitAll()
    .anyRequest().authenticated()
)
```

---

## 9. Service-to-Service Authentication

When Service A calls Service B programmatically (not on behalf of a user, but as itself), use the **Client Credentials Grant**.

### 9.1 Caller Service Configuration (Service A)

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak-service:
            client-id: service-ledger
            client-secret: ${LEDGER_SERVICE_SECRET}
            authorization-grant-type: client_credentials
            scope: openid
        provider:
          keycloak-service:
            token-uri: https://auth.panomete.com/realms/flowerogate/protocol/openid-connect/token
```

### 9.2 WebClient with Auto-Token Management

```java
@Configuration
public class ServiceToServiceConfig {

    @Bean
    public WebClient serviceWebClient(
            ReactiveClientRegistrationRepository clientRegistrations,
            ReactiveOAuth2AuthorizedClientService authorizedClients) {

        var filter = new ServletOAuth2AuthorizedClientExchangeFilterFunction(
            new AuthorizedClientServiceReactiveClientRegistrationRepository(clientRegistrations),
            authorizedClients
        );
        filter.setDefaultClientRegistrationId("keycloak-service");

        return WebClient.builder()
            .filter(filter)  // Automatically adds Bearer token + refreshes before expiry
            .build();
    }
}
```

### 9.3 Receiver Service (Service B) — No Changes

The receiver validates the JWT exactly the same way as user JWTs. The only difference:
- **User JWT:** `sub` = user UUID, `preferred_username` = username
- **Service JWT:** `sub` = service client ID (e.g., `service-ledger`)

Use the same `ResourceServerConfig` from [Section 8.4](#84-security-filter-chain-servlet).

### 9.4 Identifying the Caller

```java
@GetMapping("/api/v1/internal/data")
public ResponseEntity<?> getData(@AuthenticationPrincipal Jwt jwt) {
    String caller = jwt.getSubject(); // "service-ledger"
    // Validate caller is allowed
    // ...
}
```

---

## 10. Integration Checklist (for New Services)

Use this when adding a new microservice to the flowerogate.

### Step 1: Keycloak Client Registration

- [ ] Create new client in Keycloak (`service-<name>`)
- [ ] Type: OpenID Connect, Access: Confidential
- [ ] Service accounts roles: **Enabled** (required for client credentials)
- [ ] Copy client secret → add to `.env` as `SERVICE_<NAME>_SECRET`
- [ ] No redirect URIs needed (service doesn't handle browser redirects)

### Step 2: Spring Boot Dependencies

- [ ] Add `spring-boot-starter-security`
- [ ] Add `spring-boot-starter-security-oauth2-resource-server`

### Step 3: Application Configuration

- [ ] Add `spring.security.oauth2.resourceserver.jwt.issuer-uri` pointing to `https://auth.panomete.com/realms/flowerogate`
- [ ] If calling other services: add OAuth2 client registration for client credentials
- [ ] Store secrets in environment variables, reference as `${VAR}`

### Step 4: Security Filter Chain

- [ ] Create `SecurityFilterChain` bean
- [ ] Disable CSRF (stateless JWT APIs)
- [ ] Configure path-based access control
- [ ] Enable `oauth2ResourceServer().jwt()`
- [ ] Add `JwtAuthenticationConverter` for role mapping

### Step 5: Roles & Authorization

- [ ] Define which endpoints need which roles
- [ ] Use `hasAuthority("ROLE_ADMIN")` in security config
- [ ] Use `@PreAuthorize("hasAuthority('ROLE_ADMIN')")` for method-level auth (if needed)

### Step 6: Service Registration

- [ ] Add Nginx reverse proxy config for routing
- [ ] Add service to Docker Compose
- [ ] Place on `microservices-net` network
- [ ] Register route in Spring Cloud Gateway (see [Flowero Gate](./Flowero%20Gate.md))

### Step 7: Testing

- [ ] Unauthenticated request → 302 redirect to Keycloak (via gateway) or 401 (direct)
- [ ] Valid JWT → 200 with correct response
- [ ] Expired JWT → 401
- [ ] Wrong role → 403
- [ ] Service-to-service call with client credentials → 200

---

## 11. Security & Operations

### 11.1 Security Hardening

- [ ] **Admin console restricted** — Keycloak `/admin` path behind IP whitelist or basic auth
- [ ] **TLS everywhere** — All endpoints HTTPS. Nginx terminates TLS with Let's Encrypt
- [ ] **Short access tokens** — 5 minutes; reduces stolen token window
- [ ] **Refresh token rotation** — Enabled in Keycloak; each use invalidates old token
- [ ] **Authorization header stripped** — Gateway never forwards raw JWT to downstream
- [ ] **Client secrets rotated quarterly** — Documented procedure, automated if possible
- [ ] **No secrets in source code** — All in `.env`, `.gitignore` enforced

### 11.2 Database Backups

The Keycloak PostgreSQL database **IS your user store**. Back it up:

```bash
# Backup
docker exec postgres pg_dump -U keycloak keycloak > keycloak_backup_$(date +%Y%m%d).sql

# Restore
docker exec -i postgres psql -U keycloak keycloak < keycloak_backup.sql
```

Also export realms periodically:

```bash
docker exec keycloak kc.sh export --realm flowerogate --file /tmp/realm.json
```

### 11.3 Monitoring

- Keycloak health: `https://auth.panomete.com/health/ready`
- Gateway auth metrics: Track 401/403 rate, token refresh rate, login success/failure rate
- Alert on: Keycloak down, spike in 401s (possible attack), certificate expiry < 30 minutes

### 11.4 Disaster Recovery

1. Restore PostgreSQL from backup
2. Start Keycloak container → auto-migrates schema
3. Import realm if needed: `kc.sh import --file realm.json`
4. Verify: `https://auth.panomete.com/realms/flowerogate/.well-known/openid-configuration` returns 200
5. Restart gateway + all services → they fetch fresh JWKS keys on startup

---

## 12. Troubleshooting & Gotchas

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Login redirects to internal IP | `KC_PROXY_HEADERS` not set | Set `KC_PROXY_HEADERS: xforwarded` |
| All users gone after restart | `start-dev` mode (H2 in-memory) | Use `command: start` + PostgreSQL |
| 401 on every API call | `issuer-uri` doesn't match JWT `iss` claim | Must be exactly `https://auth.panomete.com/realms/flowerogate` |
| 403 on all API calls | CSRF enabled (Security 7 default) | Add `.csrf().disable()` |
| `authorizeHttpRequests()` not found | Using old `authorizeRequests()` | Use lambda DSL: `.authorizeHttpRequests(auth -> ...)` |
| `principal.getName()` returns UUID | Default `sub` is UUID | Set `user-name-attribute: preferred_username` |
| Roles not appearing in JWT | No role mapper configured | Add "realm roles" mapper in client scopes |
| `hasRole("ADMIN")` never matches | Wrong prefix | Use `hasAuthority("ROLE_ADMIN")` or check converter prefix |
| Gateway returns blank 500 after adding Web MVC starter | Reactive/Servlet conflict | Gateway is WebFlux only — never add `spring-boot-starter-webmvc` |

### Keycloak Gotchas

- ❌ **`start-dev`** = H2 in-memory DB. Restart = everything lost.
- ❌ **No `KC_PROXY_HEADERS`** = broken redirect URIs behind reverse proxy.
- ❌ **Access token lifespan > 30 min** = can't revoke without introspection.
- ❌ **Leaking `Authorization` to downstream** = token harvesting risk.
- ❌ **Admin console public** = full Keycloak control exposed.
- ❌ **No DB backups** = user store is gone on failure.

### Spring Security Gotchas

- ❌ **Mixing reactive and servlet** — Gateway is WebFlux (`SecurityWebFilterChain`), services are Web MVC (`SecurityFilterChain`). Never mix.
- ❌ **`@EnableWebSecurity` adding duplicate filters** — Spring Boot auto-configures security. Manual `@EnableWebSecurity` can double-register filters. Optional in Boot 4.
- ❌ **`authorizeRequests()` (Security 7)** — Removed. Only `.authorizeHttpRequests(auth -> ...)` works.
- ❌ **No role mapper** — Keycloak doesn't auto-include realm roles in JWT. Add a mapper.

### Verification Commands

```bash
# Check Keycloak health
curl https://auth.panomete.com/health/ready

# Fetch OIDC discovery (verify issuer)
curl https://auth.panomete.com/realms/flowerogate/.well-known/openid-configuration | jq .issuer

# Get JWKS keys
curl https://auth.panomete.com/realms/flowerogate/protocol/openid-connect/certs | jq

# Test unauthenticated → should redirect to Keycloak
curl -v https://gateway.panomete.com/api/v1/users

# Test authenticated → get a token first, then:
curl -H "Authorization: Bearer <token>" https://gateway.panomete.com/api/v1/users
```

---

## Related Documents

- [Flowero Gate](./Flowero%20Gate.md) — API Gateway specification
- [Spring Boot API Gateway Checklist](../project-checklist/spring-boot-flowero-gateway.md)
- [Spring Boot OAuth Checklist](spring-boot-oauth.md)
- [Web app for flowerogate](./Web%20app%20for%20flowerogate.md) — Project index

---

*Last updated: 2026-06-16*
