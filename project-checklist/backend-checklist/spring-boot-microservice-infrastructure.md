# Spring Boot Microservice Infrastructure — Integration Overview

> How Service Discovery, Load Balancing, and Open Authentication wire together in a Spring Boot 4.x homelab.
> Boot 4.0+ (Spring Framework 7, Spring Cloud 2025.x, Security 7).
> Last updated: 2026-06-12

---

## Architecture Diagram

```
                          ┌──────────────────────┐
                          │   nginx / Traefik     │  ← Edge LB, TLS, domain routing
                          │   (Load Balancing)     │     Pick one — both work.
                          └──────┬───────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
           ┌────────▼────────┐      ┌────────▼────────┐
           │ Spring Cloud     │      │ Keycloak         │
           │ Gateway          │      │ (Open Auth)      │
           │                  │      │ auth.panomete.com│
           │ OAuth2 Client    │      └──────────────────┘
           │ Resource Server  │
           │ Eureka Client    │
           │ LoadBalancer     │
           └──┬──────┬──────┬─┘
              │      │      │
    ┌─────────▼┐ ┌───▼──┐ ┌▼─────────┐
    │ Service A │ │ Svc B│ │ Service C │  ← Eureka Clients + Resource Servers
    └───────────┘ └──────┘ └───────────┘
              │      │      │
              └──────┼──────┘
                     │
          ┌──────────▼──────────┐
          │   Eureka Server      │  ← Service Discovery
          │ eureka.panomete.local│
          └─────────────────────┘
```

---

## Docker Compose — Full Stack

```yaml
version: "3.9"

services:
  # ═══ INFRASTRUCTURE ═══
  postgres:
    image: postgres:17
    container_name: postgres
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - microservices-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s; timeout: 5s; retries: 5

  # ── Service Discovery ──
  eureka-server:
    build: ./eureka-server
    container_name: eureka-server
    environment:
      SERVER_PORT: "8761"
    networks:
      - microservices-net
    healthcheck:
      test: "curl -f http://localhost:8761/actuator/health || exit 1"
      interval: 15s; timeout: 5s; retries: 5

  # ── Open Authentication ──
  keycloak:
    image: keycloak/keycloak:27.0
    container_name: keycloak
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
      KC_DB_USERNAME: admin
      KC_DB_PASSWORD: ${DB_PASSWORD}
      KC_HOSTNAME: auth.panomete.com
      KC_PROXY_HEADERS: xforwarded
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: ${KC_ADMIN_PASSWORD}
    command: start
    networks:
      - microservices-net
    depends_on:
      postgres:
        condition: service_healthy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.keycloak.rule=Host(`auth.panomete.com`)"
      - "traefik.http.routers.keycloak.entrypoints=websecure"
      - "traefik.http.routers.keycloak.tls=true"
      - "traefik.http.routers.keycloak.tls.certresolver=letsencrypt"
      - "traefik.http.services.keycloak.loadbalancer.server.port=8080"

  # ═══ APPLICATION ═══
  api-gateway:
    build: ./api-gateway
    container_name: api-gateway
    environment:
      EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eureka-server:8761/eureka/
      SPRING_SECURITY_OAUTH2_CLIENT_PROVIDER_KEYCLOAK_ISSUER_URI: https://auth.panomete.com/realms/homelab
      SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_ISSUER_URI: https://auth.panomete.com/realms/homelab
      KEYCLOAK_GATEWAY_SECRET: ${KC_GATEWAY_SECRET}
    networks:
      - microservices-net
    depends_on:
      eureka-server:
        condition: service_healthy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.gateway.rule=Host(`api.panomete.com`)"
      - "traefik.http.routers.gateway.entrypoints=websecure"
      - "traefik.http.routers.gateway.tls=true"
      - "traefik.http.routers.gateway.tls.certresolver=letsencrypt"
      - "traefik.http.services.gateway.loadbalancer.server.port=8080"

  user-service:
    build: ./user-service
    environment:
      EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eureka-server:8761/eureka/
      SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_ISSUER_URI: https://auth.panomete.com/realms/homelab
    networks:
      - microservices-net
    depends_on:
      eureka-server:
        condition: service_healthy

  # ═══ EDGE ═══
  # ── Load Balancing ──
  traefik:
    image: traefik:v3.4
    container_name: traefik
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik/config:/etc/traefik
      - ./traefik/certs:/certs
      - ./traefik/dynamic:/dynamic
    networks:
      - microservices-net

networks:
  microservices-net:
    driver: bridge

volumes:
  postgres_data:
```

---

### nginx on Host (Alternative)

If nginx already runs on your host (serving `panomete.com` etc.), you don't need a Traefik container at all:

```yaml
# docker-compose.yml — NO edge LB container needed
# nginx on the host handles TLS + routing

services:
  gateway:
    ports:
      - "127.0.0.1:8080:8080"    # Only localhost — nginx proxies here

  keycloak:
    ports:
      - "127.0.0.1:8443:8443"    # Only localhost — nginx proxies here

  # No traefik service. No Docker socket mount.
  # nginx config handles: api.panomete.com → 127.0.0.1:8080
  #                        auth.panomete.com → 127.0.0.1:8443
```

See [Spring Boot Load Balancing](spring-boot-loadbalance.md) for the full nginx config file.

---

## Startup Sequence

| Order | Component | Depends On | Healthy When |
|-------|-----------|------------|--------------|
| 1 | PostgreSQL | nothing | pg_isready |
| 2 | Eureka Server | nothing | `/actuator/health` OK |
| 3 | Keycloak | PostgreSQL | Admin console reachable |
| 4 | Services (A, B, C) | Eureka | Registered in Eureka, `/actuator/health` OK |
| 5 | API Gateway | Eureka | Routes resolving, `/actuator/health` OK |
| 6 | Edge LB (nginx/Traefik) | nothing | Port 80/443 listening |

---

## Key Integration Points

- [ ] **Eureka + LoadBalancer** — Gateway uses `lb://service-name`. Services use `@LoadBalanced WebClient`. Both resolve via Eureka lookup.
- [ ] **Gateway + Keycloak** — Gateway is both OAuth2 Client (login redirect) and Resource Server (JWT validation). Both roles in one application.
- [ ] **Services + Keycloak** — Each service validates JWT independently via JWKS key cache. No call to Keycloak per request.
- [ ] **Edge LB + Gateway** — Edge LB (nginx/Traefik) routes all API traffic to Gateway only. Gateway routes to services via Eureka discovery.
- [ ] **Edge LB + Keycloak** — Keycloak gets its own subdomain route (`auth.panomete.com`). Users and services both reach it through the edge LB.
- [ ] **nginx on host** — If nginx runs on the host (not Docker), it reaches Gateway at `127.0.0.1:8080` (Gateway's published port). Gateway reaches nginx at the host IP.

---

## Config Environment Variables

```bash
# .env (in .gitignore)
DB_PASSWORD=your-postgres-password
KC_ADMIN_PASSWORD=your-keycloak-admin-password
KC_GATEWAY_SECRET=gateway-client-secret-from-keycloak
KC_SERVICE_A_SECRET=service-a-client-secret
KC_SERVICE_B_SECRET=service-b-client-secret
```

---

## Per-Concern Deep Dives

| Concern | Checklist | What's Covered |
|---------|-----------|---------------|
| **Service Discovery** | [Spring Boot Eureka](spring-boot-eureka.md) | Eureka server + client setup, Docker config, `@LoadBalanced WebClient`, debugging, 9 gotchas |
| **Load Balancing** | [Spring Boot Load Balancing](spring-boot-loadbalance.md) | nginx or Traefik edge (TLS, domain routing, security headers) + SC LoadBalancer internal, gotchas for both |
| **Open Authentication** | [Spring Boot OAuth](spring-boot-oauth.md) | Keycloak server, realm/client config, Gateway as OAuth2 Client + Resource Server, downstream Resource Servers, client credentials, role mapping, 15+ gotchas |

For concepts, patterns, and build vs adopt decisions (framework-agnostic), read the [Microservice Infrastructure](microservice-infrastructure.md) concept checklist first.

---

## Related Checklists

- [Microservice Infrastructure](microservice-infrastructure.md) — Concepts, patterns, technology comparisons
- [Spring Boot API Gateway](spring-boot-api-gateway.md) — Gateway routes, filters, rate limiting, CORS
- [Spring Boot API](spring-boot-api.md) — Downstream service implementation
- [API Gateway](api-gateway.md) — General gateway concepts
- [API](api.md) — General API design and security
