# Spring Boot OAuth — Open Authentication Checklist

> OAuth2 / OpenID Connect with Keycloak + Spring Security for Spring Boot 4.x microservices.
> Covers Boot 4.0+ (Spring Framework 7, Security 7, modular OAuth2 starters). Docker-focused for self-hosted homelabs.
> Read the concept-level [Microservice Infrastructure Checklist](microservice-infrastructure.md) (Part 3) first for grant types, patterns, and build vs adopt decisions.
> Last updated: 2026-06-11

---

## Architecture

```
Browser ──→ Traefik ──→ Spring Cloud Gateway ──→ Service A (Resource Server)
                          │    │                      │
                          │    │ OAuth2 Client         │ Validates JWT
                          │    │ (handles login)       │ (JWKS key cache)
                          │    │                       │
                          │    │ Resource Server       │
                          │    │ (validates JWT)       │
                          │    │                       │
                          └────┼───────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │      Keycloak        │
                    │  (Token Issuer)      │
                    │  auth.panomete.com   │
                    └─────────────────────┘
```

- **Gateway** is both OAuth2 Client (redirects unauthenticated users to Keycloak) and Resource Server (validates JWT before routing).
- **Services** are Resource Servers (validate JWT independently via cached JWKS keys).
- **Keycloak** issues JWTs. Services never call Keycloak directly per request.

---

## Part 1: Keycloak Server Setup

### 1.1 Docker — Production Mode

> Keycloak's `start-dev` command uses H2 in-memory database. Restart = everything gone. Never in production.

```yaml
keycloak:
  image: keycloak/keycloak:27.0        # Check for latest stable
  container_name: keycloak
  restart: unless-stopped
  environment:
    KC_DB: postgres
    KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
    KC_DB_USERNAME: keycloak
    KC_DB_PASSWORD: ${KC_DB_PASSWORD}
    KC_HOSTNAME: auth.panomete.com
    KC_PROXY_HEADERS: xforwarded       # ⚠️ Critical behind Traefik
    KEYCLOAK_ADMIN: admin
    KEYCLOAK_ADMIN_PASSWORD: ${KC_ADMIN_PASSWORD}
  command: start                       # NOT start-dev
  networks:
    - microservices-net
  depends_on:
    postgres:
      condition: service_healthy
```

- [ ] **`KC_HOSTNAME`** — Must match the public domain users access Keycloak at. This is what Keycloak puts in redirect URIs, issuer claims, and OIDC discovery endpoints.
- [ ] **`KC_PROXY_HEADERS: xforwarded`** — Behind Traefik (or any reverse proxy), Keycloak sees internal IPs. This tells Keycloak to trust `X-Forwarded-*` headers for constructing correct redirect URIs. Without it: login redirects to `http://172.18.0.5:8080/...` instead of `https://auth.panomete.com/...`.
- [ ] **Dedicated PostgreSQL database** — Create a `keycloak` database on your existing Postgres container. Keycloak manages its own schema.
- [ ] **Production checklist**:
  - Admin password in env var or Docker secret (NEVER in `docker-compose.yml`)
  - Database backups: Keycloak DB IS your user store. Back it up.
  - Export realms periodically: `docker exec keycloak kc.sh export --realm homelab --file /tmp/realm.json`
  - Plan for admin password rotation

### 1.2 Traefik Route for Keycloak

```yaml
keycloak:
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.keycloak.rule=Host(`auth.panomete.com`)"
    - "traefik.http.routers.keycloak.entrypoints=websecure"
    - "traefik.http.routers.keycloak.tls=true"
    - "traefik.http.routers.keycloak.tls.certresolver=letsencrypt"
    - "traefik.http.services.keycloak.loadbalancer.server.port=8080"
    # ⚠️ Restrict admin console
    - "traefik.http.routers.keycloak-admin.rule=Host(`auth.panomete.com`) && PathPrefix(`/admin`)"
    - "traefik.http.routers.keycloak-admin.middlewares=admin-ipwhitelist"
```

- [ ] **Restrict `/admin`** — The Keycloak admin console should not be publicly accessible. IP whitelist it to your home/office network, or add basic auth middleware.

---

## Part 2: Keycloak Realm & Client Configuration

### 2.1 Realm Setup

- [ ] **Create a realm** — e.g., `homelab`. One realm for all internal services. The realm is the security boundary: users in realm A cannot access clients in realm B.
- [ ] **Realm settings → Tokens**:
  - **Access Token Lifespan:** 5–15 minutes. Short = more secure (stolen token expires quickly), more refresh traffic. 15 is a good default.
  - **Refresh Token Lifespan:** 30 days. With rotation enabled, each use invalidates the old token.
  - **SSO Session Idle/Max:** Sensible for your use case.

### 2.2 Client Configuration

- [ ] **Create clients for each service role**:

| Client ID | Type | Access Type | Purpose |
|-----------|------|-------------|---------|
| `api-gateway` | OpenID Connect | confidential | Gateway handles user login (auth code + PKCE) |
| `service-a` | OpenID Connect | confidential | Service-to-service auth (client credentials) |
| `service-b` | OpenID Connect | confidential | Service-to-service auth |
| `frontend-app` | OpenID Connect | public | SPA/Next.js (auth code + PKCE, no client secret) |

- [ ] **Gateway client (`api-gateway`) settings**:
  - **Client authentication:** Client ID and Secret (confidential)
  - **Valid redirect URIs:** `https://api.panomete.com/login/oauth2/code/*`
  - **Valid post logout redirect URIs:** `https://api.panomete.com/`
  - **Web origins:** `https://api.panomete.com`

- [ ] **Service client (`service-a`) settings**:
  - **Client authentication:** Client ID and Secret
  - **Service accounts roles:** Enabled (required for client credentials grant)
  - **Redirect URIs:** Not needed (services don't handle browser redirects)

- [ ] **Frontend client settings** (if you have an SPA):
  - **Access type:** public (no client secret — it would be exposed in browser)
  - **Valid redirect URIs:** `https://app.panomete.com/callback`
  - **Proof Key for Code Exchange (PKCE):** Required

### 2.3 Roles & Authorization

- [ ] **Define realm roles** — `ROLE_USER`, `ROLE_ADMIN`, etc. These appear in the JWT's `realm_access.roles` claim.
- [ ] **Assign roles to users** — Through the Keycloak admin UI. Roles propagate to Spring Security authorities via the converter (see Part 4).
- [ ] **Groups (optional)** — If you have many users, assign roles to groups, then add users to groups. Easier to manage at scale.

### 2.4 Client Secrets

- [ ] **Get the client secret** — Keycloak admin → Clients → `api-gateway` → Credentials tab → Client Secret.
- [ ] **Store in environment variable** — `KEYCLOAK_GATEWAY_SECRET=abc123...`. Reference as `${KEYCLOAK_GATEWAY_SECRET}` in `application.yml`. Never commit.
- [ ] **Rotate secrets** — Keycloak supports regenerating secrets. Schedule rotation (quarterly is reasonable). Document the procedure in your runbook.

---

## Part 3: Spring Cloud Gateway — OAuth2 Client + Resource Server

### 3.1 Dependencies

```xml
<!-- Spring Security (reactive, auto-configured for WebFlux) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<!-- OAuth2 Client (handles login flow, redirects to Keycloak) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-oauth2-client</artifactId>
</dependency>
<!-- Note: No separate resource-server starter needed on Gateway --
     the client starter includes JWT support. -->
```

### 3.2 Gateway Security Config

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak:
            client-id: api-gateway
            client-secret: ${KEYCLOAK_GATEWAY_SECRET}
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
            scope: openid,profile,email
        provider:
          keycloak:
            issuer-uri: https://auth.panomete.com/realms/homelab
            user-name-attribute: preferred_username
      resourceserver:
        jwt:
          issuer-uri: https://auth.panomete.com/realms/homelab
```

- [ ] **`issuer-uri`** — Spring Security fetches `/.well-known/openid-configuration` from this URL to discover JWKS, token, and authorization endpoints. Must match `KC_HOSTNAME` + realm path.
- [ ] **`redirect-uri`** — The path Keycloak redirects back to after login. Spring handles the OAuth2 callback at `/login/oauth2/code/{registrationId}` automatically.

### 3.3 Security Filter Chain (Boot 4 / Security 7 — Reactive)

```java
@Configuration
@EnableWebFluxSecurity
public class GatewaySecurityConfig {

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        return http
            // ⚠️ Security 7: CSRF enabled by default for ALL endpoints
            // Stateless APIs with JWT don't need CSRF
            .csrf(ServerHttpSecurity.CsrfSpec::disable)

            // Route-level access control
            .authorizeHttpRequests(auth -> auth
                // Public endpoints
                .pathMatchers("/actuator/health/**").permitAll()
                .pathMatchers("/login/**", "/oauth2/**").permitAll()
                .pathMatchers("/api/v1/public/**").permitAll()
                // Everything else needs authentication
                .anyExchange().authenticated()
            )

            // OAuth2 login (redirects to Keycloak when unauthenticated)
            .oauth2Login(Customizer.withDefaults())

            // JWT resource server (validates bearer tokens)
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(Customizer.withDefaults())
            )

            .build();
    }
}
```

- [ ] **Dual role** — Gateway is both OAuth2 Client (redirects users to login) AND Resource Server (validates JWT on API requests). Both configured in the same filter chain.
- [ ] **`authorizeHttpRequests` (NOT `authorizeRequests`)** — Security 7 removed the old method. Only the lambda DSL works: `.authorizeHttpRequests(auth -> auth.pathMatchers(...))`.

### 3.4 JWT Claim Propagation

- [ ] **Add a GlobalFilter** — After validating the JWT, extract claims and forward them as headers to downstream services:

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

                    // Extract claims
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

                    // Forward as headers
                    var request = exchange.getRequest().mutate()
                        .header("X-User-Id", userId)
                        .header("X-User-Name", username)
                        .header("X-User-Roles", roles)
                        .build();

                    // ⚠️ CRITICAL: Strip Authorization header before forwarding
                    // Downstream services should never see raw access tokens
                    var headers = new HttpHeaders();
                    request.getHeaders().forEach((key, values) -> {
                        if (!"Authorization".equalsIgnoreCase(key)) {
                            headers.addAll(key, values);
                        }
                    });

                    var cleanedRequest = exchange.getRequest().mutate()
                        .headers(httpHeaders -> {
                            httpHeaders.clear();
                            httpHeaders.addAll(headers);
                        })
                        .build();

                    return chain.filter(exchange.mutate().request(cleanedRequest).build());
                }
                return chain.filter(exchange);
            });
    }
}
```

- [ ] **Always strip `Authorization`** — Raw JWT tokens must not leak to downstream services. If a service is compromised, the attacker gets access tokens for all users whose requests passed through.
- [ ] **Header naming** — `X-User-Id`, `X-User-Name`, `X-User-Roles` are conventions. Be consistent across all services.

---

## Part 4: Downstream Services — Resource Servers

### 4.1 Dependencies

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

### 4.2 Resource Server Config

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.panomete.com/realms/homelab
```

- [ ] **How it works** — Spring fetches the JWKS endpoint (`/.well-known/openid-configuration/jwks`), gets Keycloak's public key, caches it, and validates every JWT signature locally. No network call per request. Key rotation is automatic — when Keycloak publishes a new key, Spring fetches it on the next cache miss.

### 4.3 Security Filter Chain (Boot 4 / Security 7 — Servlet)

```java
@Configuration
@EnableWebSecurity
public class ResourceServerConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            // Security 7: CSRF on by default
            .csrf(CsrfConfigurer::disable)

            .authorizeHttpRequests(auth -> auth
                // Health check: no auth needed
                .requestMatchers("/actuator/health/**").permitAll()
                // Admin endpoints: requires ROLE_ADMIN
                .requestMatchers("/api/v1/admin/**").hasAuthority("SCOPE_ROLE_ADMIN")
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

### 4.4 Role Mapping

- [ ] **Custom JwtAuthenticationConverter** — Map Keycloak realm roles to Spring Security authorities:

```java
@Bean
public JwtAuthenticationConverter jwtAuthenticationConverter() {
    JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter =
        new JwtGrantedAuthoritiesConverter();
    // Where roles live in Keycloak JWT
    grantedAuthoritiesConverter.setAuthoritiesClaimName("realm_access.roles");
    // Prefix: ROLE_USER, ROLE_ADMIN (matches hasAuthority() checks)
    grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");

    JwtAuthenticationConverter jwtConverter = new JwtAuthenticationConverter();
    jwtConverter.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);
    return jwtConverter;
}
```

- [ ] **Verify in JWT** — Decode a Keycloak-issued JWT at jwt.io. You should see:

```json
{
  "realm_access": {
    "roles": ["ROLE_USER", "ROLE_ADMIN"]
  }
}
```

### 4.5 Trust Headers or Validate JWT?

- [ ] **Option A: Trust Gateway headers** — Service trusts `X-User-Id`, `X-User-Roles` from Gateway. Simpler, but if the service is accidentally exposed directly (bypassing Gateway), it has zero auth. Acceptable only if you're CERTAIN the service can't be reached externally.
- [ ] **Option B: Validate JWT independently (recommended)** — Service validates the JWT using the JWKS key cache. Defense-in-depth. If Gateway is compromised or bypassed, the service still requires a valid JWT. The performance cost is negligible after key caching.
- [ ] **Option C: Both** — Validate JWT for security, but also read `X-User-*` headers for convenience (avoid parsing the JWT in every controller method). This is the pragmatic approach.

---

## Part 5: Service-to-Service Authentication (Client Credentials)

> When Service A calls Service B programmatically — not on behalf of a user, but as itself.

### 5.1 Service A (Caller) Configuration

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak-service:
            client-id: service-a
            client-secret: ${SERVICE_A_CLIENT_SECRET}
            authorization-grant-type: client_credentials
            scope: openid
        provider:
          keycloak-service:
            token-uri: https://auth.panomete.com/realms/homelab/protocol/openid-connect/token
```

- [ ] **No user involved** — The `sub` claim will be the service's client ID, not a user ID. Service B knows it's Service A calling, not a user.

### 5.2 WebClient with Automatic Token Management

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
            .filter(filter)          // Automatically adds Bearer token
            .build();
    }
}
```

- [ ] **Zero manual token handling** — The filter automatically acquires a token before the first request, caches it, and refreshes it before expiry. Your code just calls the WebClient.

### 5.3 Service B (Receiver) — Same as User Auth

- [ ] **No changes needed** — Service B validates the JWT the same way as user JWTs. Same resource server config, same filter chain. The only difference is the `sub` claim (service client ID vs user ID).

---

## 6. Keycloak Gotchas

- ❌ **`start-dev` in production** — Dev mode = H2 in-memory database. Container restart = all users, realms, clients gone. Use `start`.
- ❌ **Without `KC_PROXY_HEADERS: xforwarded`** — Behind Traefik, Keycloak sees `172.18.0.x` instead of `auth.panomete.com`. Redirect URIs are wrong. Login redirects break.
- ❌ **Access token lifespan too long** — 30+ minute tokens can't be revoked without introspection. 5–15 minutes with refresh rotation is standard.
- ❌ **Leaking `Authorization` header to downstream** — Gateway must strip it. A compromised downstream service could harvest valid tokens.
- ❌ **CSRF blocking API calls (Security 7)** — Security 7 enables CSRF for ALL endpoints. Stateless JWT APIs get 403 until `.csrf().disable()`.
- ❌ **`authorizeRequests()` (Security 7)** — Removed. Only `.authorizeHttpRequests(auth -> ...)` lambda DSL works.
- ❌ **Wrong `issuer-uri`** — Must match exactly what's in the JWT's `iss` claim (`https://auth.panomete.com/realms/homelab`). Missing trailing slash or wrong realm name = 401 on every request.
- ❌ **No client secret rotation** — Secrets should rotate. If a secret leaks, rotating it revokes the old one. Keycloak supports this natively.
- ❌ **Keycloak DB not backed up** — That PostgreSQL database IS your user store. No backup = lost all users on DB failure.
- ❌ **Admin console publicly accessible** — IP-restrict `/admin` paths or put basic auth in front.

### Spring Security Gotchas

- ❌ **Mixing reactive and servlet** — Gateway is WebFlux (reactive). Services are Web MVC (servlet). Filter chains are different types (`SecurityWebFilterChain` vs `SecurityFilterChain`). Don't mix them.
- ❌ **`@EnableWebSecurity` adding duplicate filters** — Spring Boot auto-configures security. Adding `@EnableWebSecurity` manually can cause double filter registration. It's optional in Boot 4.
- ❌ **`principal.getName()` returns UUID** — Keycloak's default `sub` claim is a UUID. If you want username, configure `user-name-attribute: preferred_username` in the Gateway provider config.
- ❌ **JWT not including roles** — By default Keycloak doesn't include realm roles in the JWT. Add a "realm roles" mapper in the client's Client Scopes → Dedicated scopes.
- ❌ **`hasRole()` vs `hasAuthority()`** — `hasRole("ADMIN")` checks for `ROLE_ADMIN` authority. `hasAuthority("SCOPE_ROLE_ADMIN")` checks for scope prefix. Know which one your converter produces.

---

## 7. Testing Auth

- [ ] **Unauthenticated → redirect** — `curl -v https://api.panomete.com/api/v1/users` → 302 to `https://auth.panomete.com/realms/homelab/protocol/openid-connect/auth`
- [ ] **Valid JWT → 200** — Get a token (via login flow or client credentials), `curl -H "Authorization: Bearer <token>" https://api.panomete.com/api/v1/users` → 200
- [ ] **Expired JWT → 401** — Wait for access token to expire (or use a short-lived test client). Same request → 401 with `WWW-Authenticate: Bearer` header.
- [ ] **Invalid signature → 401** — Tamper with the JWT payload. Request → 401.
- [ ] **Wrong audience → 401** — JWT with `aud: "other-client"` → 401 if audience validation is enabled.
- [ ] **Wrong role → 403** — User with `ROLE_USER` hits `/api/v1/admin/**` → 403 Forbidden.
- [ ] **Downstream service directly** — Hit Service A directly (bypassing Gateway) with valid JWT → 200 (if validating JWT). Without JWT → 401.
- [ ] **Service-to-service** — Service A calls Service B with client credentials token → 200. Service B's `sub` claim = `service-a`.

---

## Quick Sanity Check

- [ ] Keycloak running in production mode (`start`, not `start-dev`)
- [ ] PostgreSQL database for Keycloak (not H2)
- [ ] `KC_HOSTNAME` set to public domain
- [ ] `KC_PROXY_HEADERS: xforwarded` configured
- [ ] Realm created, clients configured with correct redirect URIs
- [ ] Gateway: OAuth2 client (login) + resource server (JWT validation)
- [ ] Gateway: CSRF disabled (stateless JWT APIs)
- [ ] Gateway: `Authorization` header stripped before forwarding
- [ ] Gateway: JWT claims propagated as `X-User-*` headers
- [ ] Downstream services: JWT validation enabled (JWKS cache)
- [ ] Role mapping: Keycloak realm roles → Spring Security authorities
- [ ] Client credentials grant for service-to-service calls
- [ ] Client secrets in environment variables, never in source code
- [ ] Keycloak admin console IP-restricted (not public)
- [ ] Keycloak database backed up regularly
- [ ] Access tokens: 5–15 minute lifespan
- [ ] Refresh token rotation enabled
- [ ] No `authorizeRequests()` — Security 7 uses lambda DSL only

---

## Related Checklists

- [Microservice Infrastructure](microservice-infrastructure.md) — Concepts: OAuth2 vs OIDC, grant types, architecture patterns
- [Spring Boot Microservice Infrastructure](spring-boot-microservice-infrastructure.md) — Integration overview: architecture diagram, full Docker Compose, startup sequence
- [Spring Boot Eureka](spring-boot-eureka.md) — Service Discovery
- [Spring Boot Load Balancing](spring-boot-loadbalance.md) — Traefik + SC LoadBalancer
- [Spring Boot API Gateway](spring-boot-api-gateway.md) — Gateway routes, filters, rate limiting
