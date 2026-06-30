# Backend Launch Checklist

> Tick every box before a backend service hits production. Framework-agnostic. Deep knowledge: follow the `→` links.

---

## Security

- [ ] All endpoints authenticated unless explicitly public → [[03 Authentication]]
- [ ] Authorization checked on every endpoint (not just at the gateway) → [[03 Authorization & Rate Limiting]]
- [ ] Passwords hashed (bcrypt/argon2, cost ≥ 12) → [[01 Cryptography Basics]]
- [ ] TLS enabled, HTTP redirected to HTTPS, HSTS header set → [[03 Network & TLS]]
- [ ] Secrets in Vault/K8s Secrets/env vars — never in source code → [[02 Secrets Management]]
- [ ] CORS restricted to known origins (not `*`) → [[03 API Security]]
- [ ] Rate limiting on login and public endpoints → [[03 Authorization & Rate Limiting]]
- [ ] JWT: short expiry (≤15 min), RS256/ES256, refresh token rotation → [[03 Authentication]]
- [ ] CSRF: disabled for stateless JWT APIs; enabled for cookie-based auth
- [ ] Security headers: `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`
- [ ] Dependencies scanned for CVEs; criticals patched → [[02 Dependency & Supply Chain]]

---

## API Design

- [ ] Consistent error format across all endpoints → [[01 REST API Design]]
- [ ] Input validated on every endpoint (type, length, range, format) → [[02 Secure Coding Practices]]
- [ ] Pagination on all list endpoints (cursor-based if data changes frequently)
- [ ] API versioned (URL path `/v1/` or header `Accept-Version`)
- [ ] Idempotency keys on POST/PATCH where duplicates would cause harm
- [ ] No stack traces in error responses → [[02 Secure Coding Practices]]
- [ ] OpenAPI spec available (at least for public endpoints) → [[01 OpenAPI & Documentation]]

---

## Database

- [ ] Migrations version-controlled (Flyway/Liquibase), not `ddl-auto: update` → [[03 Migration Backup & Scaling]]
- [ ] `open-in-view: false` (Spring/JPA) — fetch data in service layer
- [ ] N+1 queries hunted down (`JOIN FETCH`, `@EntityGraph`) → [[01 Indexing & Performance]]
- [ ] Connection pool sized correctly (not default unlimited) → [[03 Migration Backup & Scaling]]
- [ ] Transactions: `@Transactional` on service methods that touch multiple repositories → [[01 Transactions & Locking]]
- [ ] Backup strategy exists and restore has been TESTED → [[03 Migration Backup & Scaling]]
- [ ] Indexes on foreign keys and common WHERE/JOIN columns → [[01 Indexing & Performance]]

---

## Resilience

- [ ] Circuit breaker on every external HTTP call (other services, third-party APIs) → [[04 Circuit Breaker]]
- [ ] Timeouts on all external calls (connect + read) → [[04 Retry & Timeout]]
- [ ] Retry with backoff for transient failures → [[04 Retry & Timeout]]
- [ ] Graceful degradation: fallback responses, not crashes → [[04 Bulkhead Pattern]]
- [ ] Graceful shutdown configured (drain in-flight requests) → [[07 Containers & Orchestration]]

---

## Observability

- [ ] Health check endpoint (`/health`) with DB/disk/memory checks → [[05 Health Checks]]
- [ ] Structured logging (JSON in production) → [[05 Logging & Monitoring]]
- [ ] Distributed tracing (trace ID propagated across service calls) → [[05 Distributed Tracing]]
- [ ] Key metrics exported: request rate, error rate, latency, DB pool → [[04 API Monitoring]]
- [ ] Alerts configured for: 5xx spike, high latency, circuit open, DB down
- [ ] Logs never contain secrets, passwords, tokens, PII → [[02 Secure Coding Practices]]

---

## Testing

- [ ] Unit tests for business logic → [[02 Functional Testing]]
- [ ] Integration tests with real database (Testcontainers, not H2) → [[03 Backend Automation]]
- [ ] API contract tests (at least happy path + key error cases) → [[04 API CI-CD]]
- [ ] Circuit breaker behavior tested (downstream killed → circuit opens → recovers)
- [ ] Auth tested: 401 for no auth, 403 for wrong role → [[03 CI-CD & Headless Testing]]

---

## Deployment

- [ ] Build reproducible (pinned deps, lockfile committed)
- [ ] CI pipeline runs tests, lint, and security scan on every commit → [[03 CI-CD & Headless Testing]]
- [ ] Database migrations run automatically in CI/CD pipeline
- [ ] Rollback plan exists and has been practiced
- [ ] Feature flags for risky changes (not long-lived branches) → [[06 Configuration Management]]

---

## Sources

- These items distilled from your vaults: API, Database, Cybersecurity, Microservices, QA, Computer Networks, Operating Systems.
- Original deep-reference checklists: `../spring-boot-api.md`, `../api.md`
