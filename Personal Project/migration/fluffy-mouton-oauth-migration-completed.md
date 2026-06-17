# Fluffy Mouton — OAuth2 Migration: Completed Summary

> **Date:** 2026-06-18  
> **Status:** ✅ API + Web ready for deployment  
> **PRs:** [API #23](https://github.com/oat431/fluffy-mouton-api/pull/23) · [Web #19](https://github.com/oat431/fluffy-mouton-web/pull/19)

---

## What Changed

### Architecture Shift

```
BEFORE (Monolith JWT)                    AFTER (OAuth2 + Gateway)
─────────────────────────                ──────────────────────────
Frontend → POST /auth/login              Frontend → Gateway OAuth2 → Keycloak
         ← JWT in localStorage                     ← Session cookie
         → Bearer token on every call              → Cookie sent automatically
                                                   
API: HS256 secret key, tb_auth table     API: RS256 JWKS validation, zero local auth tables
```

### API (fluffy-mouton-api) — 34 files changed

| Action | Files | Notes |
|--------|-------|-------|
| **Added** | `pkg/utils/keycloak_jwt.go` | JWKS-based Keycloak JWT validation (`keyfunc/v3`) |
| **Added** | `internal/middleware/oauth_middleware.go` | Dual-mode auth: gateway headers + direct JWKS |
| **Modified** | `cmd/api/main.go` | InitJWKS on startup |
| **Modified** | `internal/bootstrap/api_container.go` | Removed all auth dependencies |
| **Modified** | `internal/router/main_router.go` | Removed CORS config, auth routes; added dev-mode CORS toggle |
| **Modified** | `internal/router/short_link_router.go` | `JWTMiddleware` → `OAuthMiddleware`, `/short-link` → `/short` |
| **Modified** | `internal/controller/short_link_controller.go` | `c.Locals("auth_id")` → `c.Locals("user_id")` |
| **Modified** | `docker-compose.*.yml` | Network: `microservices-net`, container: `shortlink-service` |
| **Modified** | `.env`, `.env.example` | Added `OAUTH_ISSUER_URI`; removed `SECRET`, `SMTP_*` |
| **Removed** | 19 old auth files | Controllers, services, repos, models, middleware, payloads, utils |

### Web (fluffy-mouton-web) — 11 files changed

| Action | Files | Notes |
|--------|-------|-------|
| **Rewritten** | `AuthContext.tsx` | Session + Bearer hybrid; dev vs prod mode |
| **Rewritten** | `LoginPage.tsx` | OAuth2 redirect (prod) / token paste (dev) |
| **Rewritten** | `APIClient.ts` | Gateway URL (prod) / localhost (dev) |
| **Rewritten** | `ProfilePage.tsx` | Simplified — OAuth2 status display |
| **Updated** | `ShortLinkService.ts` | `/short-link/` → `/short/` paths |
| **Removed** | `RegisterPage.tsx`, `VerifyEmailPage.tsx` | Keycloak handles these |
| **Stubbed** | `AuthService.ts` | No more local auth endpoints |

### Gateway (flowerogate) — 6 files changed

| Action | Files | Notes |
|--------|-------|-------|
| **Added** | `OAuth2RedirectParamFilter.java` | Stores `redirect_uri` from frontend in session |
| **Added** | Dep: `spring-boot-starter-oauth2-client` | Enables browser login redirect |
| **Modified** | `SecurityConfig.java` | OAuth2 login + SameSite=None + entry point |
| **Modified** | `CorsConfig.java` | Reads `CORS_ALLOWED_ORIGINS` env var |
| **Modified** | `application.yaml` | Added shortlink route + forward-headers |
| **Modified** | `application-prod.yaml` | OAuth2 client registration + CORS |

---

## How It Works

### Prod Flow (Gateway + Session Cookie)

```
Browser → https://short.panomete.com/short-link
  │  GET /api/v1/short/ → Gateway (session cookie)
  │  If no session: 302 → Keycloak login
  │  If session: validates → strips Auth → adds X-User-Id → forwards
  ▼
shortlink-service receives X-User-Id header → OAuthMiddleware Path 1
```

### Dev Flow (Direct API + Bearer Token)

```
localhost:3000 → GET localhost:8004/api/v1/short/
  │  Authorization: Bearer <keycloak-token>
  ▼
API: OAuthMiddleware Path 2 → JWKS validation → authenticated
```

### Auth Middleware Decision

```
OAuthMiddleware(c)
  ├─ X-User-Id header present? → Path 1: trust gateway headers
  └─ Authorization: Bearer?     → Path 2: validate JWT via JWKS
       └─ Neither?              → 401
```

---

## Pre-Deploy Checklist

### 1. Database

- [x] `fk_short_link_auth` constraint dropped
- [x] `tb_short_links.own_by` migrated to Keycloak UUID
- [ ] Verify: `SELECT own_by, COUNT(*) FROM tb_short_links GROUP BY own_by;`

### 2. Keycloak (`auth.panomete.com`)

- [x] Realm `flowerogate` exists
- [x] Client `flowero-gateway` (confidential, used by gateway)
- [x] Client `service-shortlink` (confidential, service accounts enabled)
- [x] User `panomete` created
- [ ] **Redirect URIs for `flowero-gateway` must include:**
  - `https://gateway.panomete.com/login/oauth2/code/*`
  - `http://localhost:3000/*` ← for local dev
- [ ] **Web origins for `flowero-gateway` must include:**
  - `https://gateway.panomete.com`
  - `http://localhost:3000` ← for local dev
- [ ] **Direct access grants** enabled on `service-shortlink` (for dev token)

### 3. Gateway (`gateway.panomete.com`)

- [ ] Code pushed + pulled on server
- [ ] Rebuild: `./gradlew clean bootJar`
- [ ] Env vars set:
  - `KEYCLOAK_GATEWAY_SECRET=<secret>`
  - `CORS_ALLOWED_ORIGINS=https://short.panomete.com,https://gateway.panomete.com,http://localhost:3000`
  - `JWT_ISSUER_URI=https://auth.panomete.com/realms/flowerogate`
  - `JWT_JWK_SET_URI=https://auth.panomete.com/realms/flowerogate/protocol/openid-connect/certs`
- [ ] Route exists: `Path=/api/v1/short/**` → `http://shortlink-service:8080`
- [ ] Container restarted with new JAR

### 4. API (shortlink-service)

- [ ] PR #23 merged to `dev`
- [ ] Docker image built + deployed
- [ ] Container on `microservices-net`, name: `shortlink-service`
- [ ] Env vars set:
  - `OAUTH_ISSUER_URI=https://auth.panomete.com/realms/flowerogate`
  - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- [ ] Health check: `curl http://shortlink-service:8080/api/v1/health/check`

### 5. Web (`short.panomete.com`)

- [ ] PR #19 merged to `dev`
- [ ] Production build: `bun install && bun run build`
- [ ] Docker image built + deployed
- [ ] Nginx pointed at build output
- [ ] Env: no `FLUMOU_API_URL` needed (defaults to gateway)

### 6. End-to-End Test

- [ ] Visit `short.panomete.com` → redirected to Keycloak login
- [ ] Login with `panomete` → redirected back to app
- [ ] ShortLink page loads with links
- [ ] Create/edit/delete links work
- [ ] Logout → redirected back to login page

### 7. Post-Deploy Cleanup (after 24h of stable operation)

- [ ] Drop old tables: `tb_auth`, `tb_refresh_tokens`, `tb_verify_tokens`
- [ ] Remove old gateway `globalcors` config (already done)
- [ ] Remove old API CORS config (already done)
