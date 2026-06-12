# Backend Project Checklist

> Practical, no-fluff checklist for production backend services.
> Last updated: 2026-06-11

---

## 1. Language & Runtime

- [ ] **Language choice** — Go, Rust, TypeScript/Node, Python, Java/Kotlin, C#. Pick what the team knows, not what's trending.
- [ ] **Runtime version pinned** — `.nvmrc`, `.go-version`, `.python-version`, `rust-toolchain.toml`. CI and dev must match.
- [ ] **Package manager locked** — `package-lock.json`, `Cargo.lock`, `go.sum`, `poetry.lock`, `Pipfile.lock`. Commit lockfiles.

## 2. Project Structure

- [ ] **Layered architecture** — Handler/Controller → Service/UseCase → Repository/DataAccess. No business logic in HTTP handlers.
- [ ] **Domain-driven where it matters** — Not every project needs DDD. But core domain logic should be framework-agnostic and testable in isolation.
- [ ] **Dependency injection & wiring** — Constructor injection over service locators. Interfaces for every external boundary (DB, cache, queue, HTTP client). This is the difference between testable and untestable code.
- [ ] **Shared kernel** — Types, errors, constants in a shared package if monorepo. No circular dependencies.
- [ ] **Migrations directory** — Versioned, never edited after merge. Up and down migrations.

## 3. Containerization

- [ ] **Dockerfile** — Multi-stage builds. Build stage has dev dependencies + compiler. Run stage has only the binary + runtime. Final image: minimal base (distroless, alpine, scratch). Non-root user.
- [ ] **`.dockerignore`** — Exclude `node_modules`, `.git`, `target/`, `*.log`, `.env*`. Smaller build context, no secret leaks into image.
- [ ] **Image size conscious** — < 50MB for Go/Rust binaries, < 150MB for Node/Python. Large images = slow deploys, more attack surface.
- [ ] **No secrets in image layers** — `COPY .env .` in Dockerfile commits secrets to a layer. Use build args only for non-sensitive data. Runtime secrets via env vars, mounted volumes, or secrets manager — never in the image.
- [ ] **Health check in container** — `HEALTHCHECK` instruction or K8s probe. Don't rely on the process being alive — check it can actually serve.
- [ ] **Docker Compose for local dev** — Spin up service + dependencies (DB, Redis, queue) with one command. New dev runs `docker compose up` and has a working environment in minutes.

## 4. API Design

- [ ] **REST or gRPC or GraphQL** — REST for most things. gRPC for internal service-to-service. GraphQL only if the client genuinely needs flexible queries.
- [ ] **gRPC specifics (if using)** — Protobuf linting in CI (`buf lint`). Backward-compatible changes only (no field renumbering, no removing reserved fields). `buf breaking` check in CI. Use `grpc-gateway` or `connect` for REST-to-gRPC translation if needed.
- [ ] **Consistent error format** — `{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }`. RFC 7807 (Problem Details) or JSON API style.
- [ ] **HTTP status codes used correctly** — 200/201/204 for success. 400 validation, 401 unauth'd, 403 forbidden, 404 not-found, 409 conflict, 422 unprocessable, 429 rate-limit, 500 internal (and never leak stack traces). 202 Accepted for async/long-running operations with a status endpoint.
- [ ] **API versioning strategy** — URL prefix (`/v1/`), header, or content negotiation. Decide before v1 ships.
- [ ] **Pagination** — Cursor-based for large/infinite lists, offset for small/skip-navigate. Standardize: `{ "data": [...], "cursor": "...", "hasMore": true }`.
- [ ] **Conditional requests** — ETag + If-None-Match for GET (304 Not Modified saves bandwidth). If-Match for optimistic concurrency on PUT/PATCH.
- [ ] **Long-running operations** — Return `202 Accepted` with a status endpoint (`/operations/{id}`). Client polls or receives webhook on completion. Not holding HTTP connections open for minutes.
- [ ] **Request validation** — Validate at the boundary. Reject invalid input before it touches domain logic. Use schema validation (Zod, Pydantic, `go-playground/validator`).
- [ ] **OpenAPI/Swagger spec** — Generated from code, not hand-written. `swaggo` (Go), `@nestjs/swagger`, FastAPI auto-docs, `utoipa` (Rust).

## 5. Database

- [ ] **Migration tool** — golang-migrate, Flyway, Alembic, Prisma Migrate. Run automatically in CI/deploy, never manually.
- [ ] **Connection pooling** — PgBouncer or built-in pool. Configure max connections, timeout, idle timeout. Ensure pool size ≈ `(core_count * 2) / number_of_service_instances`.
- [ ] **Connection security** — DB credentials never in code or plain config. Vault/secrets manager, or at minimum env vars. Rotate regularly. Use TLS for DB connections in production.
- [ ] **N+1 query detection** — Query logging in dev, `bullet` gem (Rails), `gorm` log mode, Prisma query log. Eager-load associations. DataLoader pattern for GraphQL.
- [ ] **Index strategy** — Query patterns drive indexes. Covering indexes for hot queries. `EXPLAIN ANALYZE` before shipping. Monitor slow query log. Know the difference between B-tree, GIN, GiST, BRIN — they solve different problems.
- [ ] **Read replicas strategy** — Read/write split if needed. Write to primary, read from replicas. Be aware of replication lag. ORM/query builder should support routing reads to replicas.
- [ ] **Soft deletes?** — Decide early. Soft deletes complicate every query (WHERE deleted_at IS NULL). User data → GDPR considerations (soft delete may not satisfy "right to erasure").
- [ ] **UUID vs auto-increment** — UUIDv7 (time-ordered) for distributed systems. BigInt auto-increment for single-DB simpler setups.
- [ ] **Seed data** — Dev and test environments seed deterministically. Production seeds only for reference/lookup data. Seed scripts are versioned and idempotent.

## 6. Authentication & Authorization

- [ ] **Auth protocol** — JWT (stateless) or opaque token (stateful). JWT: short expiry (15min) + refresh token (7-30 days). Never store sensitive data in JWT claims.
- [ ] **OAuth2 / OpenID Connect** — If integrating with third-party login (Google, GitHub, etc.): authorization code flow + PKCE. State parameter to prevent CSRF. Token refresh handled server-side. Never expose refresh tokens to the browser.
- [ ] **Password hashing** — bcrypt, argon2id. Never SHA/MD5. Cost factor tuned: target ~250ms hash time. Re-hash on login if cost factor increases.
- [ ] **Session management** — Track active sessions per user. Session revocation capability (logout, password change, suspicious activity). Concurrent session limits if sensitive. Session listing for user.
- [ ] **Rate limiting** — Login endpoints: strict (5/min per IP+email). Password reset: strict. 2FA/MFA endpoint: strict. General API: token bucket per user/IP.
- [ ] **Authorization model** — RBAC for most apps. ABAC for complex. Claims-based for microservices. Enforce at middleware/gateway layer, not in every handler.
- [ ] **Multi-tenancy authorization** — If SaaS: tenant context in every request. Never rely on client-provided tenant ID without authorization. User must belong to the requested tenant. Data isolation enforced at query layer (WHERE tenant_id = $ctx.tenantId).
- [ ] **API keys** — For service-to-service. Hashed in DB (like passwords). Prefix for identification (`sk_live_...`). Scoped, revocable. Rotate on fixed schedule.

## 7. Security

- [ ] **Input sanitization** — Parameterized queries (no string concatenation SQL). Validate and sanitize all user input at boundary. XML parsing: disable external entities (XXE prevention). File uploads: validate MIME type + magic bytes, not just extension.
- [ ] **SQL injection beyond parameterized** — Stored procedures also need parameterization. Dynamic ORDER BY / GROUP BY / table names — use whitelist map, never interpolate user input.
- [ ] **CORS configured** — Specific origins, not `*`. Specific methods, not `*`. Credentials only if needed.
- [ ] **Security headers** — `helmet` (Node), `secure` (Go). CSP, X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security, Referrer-Policy, Permissions-Policy.
- [ ] **HTTPS only** — TLS 1.2+, HSTS (max-age ≥ 1 year, includeSubDomains), redirect HTTP→HTTPS. Let's Encrypt or managed cert.
- [ ] **Secrets management** — Never in code, never in config files, never in env committed to git. Use vault, secrets manager, or at minimum `.env` in `.gitignore`. CI/CD injects secrets from secure store, not from git.
- [ ] **Dependency audit** — `npm audit`, `pip audit`, `go mod tidy` + `govulncheck`, `cargo audit`. Automated in CI. Block builds on high/critical. Auto-merge patch updates via Dependabot/Renovate.
- [ ] **CSRF protection** — If using cookie-based auth. SameSite=Lax minimum, SameSite=Strict better. CSRF token for mutation endpoints. SPA with token in Authorization header is CSRF-immune.
- [ ] **Open redirect prevention** — Never redirect to user-provided URLs without validation. Whitelist allowed redirect destinations. Or use relative redirects only.
- [ ] **Rate limiting by endpoint sensitivity** — Login: 5/min. Password reset: 3/min. Email verification send: 2/min. GraphQL queries: depth + complexity limits to prevent abusive queries.

## 8. Logging & Observability

- [ ] **Structured logging** — JSON logs. `zap` (Go), `pino` (Node), `structlog` (Python). Every log line has: timestamp, level, message, trace_id, span_id, service, tenant_id (if multi-tenant).
- [ ] **Distributed tracing** — OpenTelemetry. Propagate trace context (W3C traceparent) across service boundaries. Jaeger, Tempo, or Datadog backend.
- [ ] **Metrics** — RED metrics (Rate, Errors, Duration) for every endpoint. USE metrics (Utilization, Saturation, Errors) for resources. Prometheus + Grafana. Business metrics (signups, payments) separate namespace from infra metrics.
- [ ] **Dashboards as code** — Grafana dashboards provisioned from JSON in git. Not hand-tweaked in production and never saved. Dashboard changes go through PR review.
- [ ] **SLO/SLI** — Define: 99.9% availability, p95 latency < target. Measure. Track error budget. Alert when burning budget too fast. This is more actionable than "alert on 5xx spike."
- [ ] **Health checks** — `/health` (liveness — is the process alive?), `/ready` (readiness — can it serve traffic? DB connected? Redis reachable?). Kubernetes uses both.
- [ ] **Alerting** — Error rate spike burning budget, latency p95 > SLO threshold, DB connection pool exhaustion, circuit breaker open, dead letter queue growing, disk approaching capacity. Alert on symptoms (user-visible), not causes (CPU high).

## 9. Error Handling

- [ ] **Error wrapping** — Preserve stack trace. `fmt.Errorf("...: %w", err)` (Go), `cause` chain (Node). Don't swallow errors silently.
- [ ] **Error classification** — Not all errors are equal. Validation errors → 400. Not found → 404. Conflict → 409. Downstream failure → 502/503. Unexpected → 500. Log unexpected errors at ERROR level, expected errors at WARN or INFO.
- [ ] **Graceful degradation** — If a downstream service fails, return partial data or cached stale data, not a 500. Feature toggles to disable non-critical features when dependencies are unhealthy.
- [ ] **Retry with backoff** — Exponential backoff + jitter for transient failures (network, deadlock). Only for idempotent operations. Max retries, max total time. Retry budget per request.
- [ ] **Dead letter queue** — Failed async jobs go to DLQ for inspection and replay. Don't just drop them. Alert on DLQ growth. Have a replay mechanism.

## 10. Circuit Breaker & Resilience Patterns

> **When you need it:**  
> 🔄 **Microservices** — ✅ mandatory. Every service-to-service HTTP/gRPC call is a potential cascading failure.  
> 🧱 **Monolith calling external APIs** (payment gateway, email provider, SMS, third-party) — ✅ recommended. External dependencies can fail or slow down.  
> 🧱 **Monolith internal calls** (in-process method invocations) — ❌ unnecessary. No network hop = no thread pool exhaustion. Circuit breakers protect remote calls, not local method calls.
>
> **Framework-specific checklists:** This is the general pattern. For Spring Boot specifics (Resilience4j config, `@CircuitBreaker`, fallback patterns), see [Spring Boot API Checklist](./spring-boot-api.md). For gateway-level circuit breaking, see [API Gateway Checklist](./api-gateway.md) and [Spring Boot API Gateway Checklist](./spring-boot-api-gateway.md).

- [ ] **Circuit breaker** — Stop calling a failing downstream after N failures within a time window. Three states: closed (normal), open (fail fast, no calls), half-open (probing recovery). Per-downstream, never one global breaker. Libraries: `gobreaker` (Go), `opossum` (Node), `resilience4j` (Java), `circuitbreaker` (Python), `fault-tolerant` (Rust).
- [ ] **Per-destination tuning** — Different downstreams, different thresholds. Payment gateway: tight (fail fast at 30% error rate, wait 60s to recover). Email service: loose (80% error rate tolerated, 15s recovery). Non-critical features: more lenient. One size fits none.
- [ ] **Fallback strategy** — When circuit is open: return cached stale data, default/empty response, degraded view, or a domain error. Never return `null` silently — pushes the problem downstream. Choose per-endpoint: login fallback = hard error, product listing fallback = stale cache.
- [ ] **Half-open probing** — After timeout expires, limited requests probe the downstream. Successes close the circuit; any failure re-opens it immediately. Prevents thundering-herd reconnection.
- [ ] **Exception filtering** — Not all errors should open the circuit. Connectivity/timeout exceptions: yes. Business exceptions (`NotFound`, `ValidationError`): no — those are successful calls that returned expected errors. A 404 from downstream is a response, not a failure.
- [ ] **Retry + Circuit Breaker ordering** — Retry INSIDE circuit breaker. Circuit breaker wraps retry. Why: retries exhaust and still fail → counted as ONE failure. Circuit open → retries fail fast, no wasted waits.
- [ ] **Timeout always paired** — Circuit breaker doesn't stop slow calls — it only counts failures after they happen. Always set connection + read timeouts on every outbound HTTP client. Shorter than the caller's own timeout, or you'll still hang.
- [ ] **Service mesh alternative** — If you have Istio/Linkerd/Consul Connect, circuit breaking can live in the sidecar proxy transparently. No code changes, language-agnostic. Trade-off: operational complexity vs code simplicity. Best for polyglot or ops-managed environments.
- [ ] **Monitoring** — Circuit state metric (closed=0, open=1, half-open=2). Alert when any circuit opens. Track: success/failure/blocked call counts, failure rate per breaker. Dashboard panel: circuit breaker state per downstream service.
- [ ] **Testing circuit breakers** — Integration test: downstream returns 500 for N calls → circuit opens → fallback returned → wait for half-open → successful probe closes circuit. Chaos test: kill a downstream service → verify system degrades gracefully, doesn't cascade.

## 11. Message Queues & Event-Driven Architecture

- [ ] **When to use** — Anything that can be deferred: email, notifications, report generation, image processing. Decouple services: Order service emits `order.created`, Inventory service consumes it. Not just "put it in a queue" — events tell a story.
- [ ] **Message broker choice** — RabbitMQ (routing flexibility, mature), Kafka (event streaming, replay, high throughput), NATS (lightweight, Cloud Native), Redis Streams (if already using Redis, small scale), SQS/GCP PubSub (managed, zero ops).
- [ ] **Idempotent consumers** — Your consumer will receive the same message at least once. Deduplicate by message ID. Idempotency key in database. Processing the same event twice must yield the same result.
- [ ] **Ordering guarantees** — Kafka: per-partition ordering. RabbitMQ: per-queue with single consumer. If order matters, route related events to the same partition/queue (by aggregate ID).
- [ ] **Dead letter queue** — Failed messages → DLQ after max retries. Inspect, fix, replay. Alert on DLQ growth. Never silently drop messages.
- [ ] **Schema evolution** — Avro + Schema Registry, Protobuf, or JSON Schema. Forward and backward compatibility. Don't break consumers when producers evolve.
- [ ] **Observability** — Trace context in message headers. Correlate producer trace with consumer trace. Metrics: publish rate, consume rate, lag, retry count, DLQ size.

## 12. File Storage (if applicable)

- [ ] **Object storage** — S3, MinIO, GCS, Azure Blob. Not the local filesystem (not scalable, lost on restart). Not the database (bloats, expensive).
- [ ] **Presigned URLs** — Generate short-lived upload/download URLs. Client uploads directly to storage, not through your server. Send URL to client, let them stream directly.
- [ ] **File validation** — Max size. Allowed MIME types (whitelist). Magic byte check, not just extension. Virus scan for user uploads (ClamAV or cloud equivalent).
- [ ] **Image processing pipeline** — Generate thumbnails/variants on upload (async, not in request path). Responsive image sizes. WebP/AVIF conversion.
- [ ] **Access control** — Private bucket by default. Presigned URLs for authenticated access. CDN with signed URLs or token auth for public-facing files.
- [ ] **Backup & lifecycle** — Bucket versioning. Lifecycle policies (archive old objects, delete expired). Cross-region replication for critical data.

## 13. Testing

- [ ] **Unit tests** — Business logic, pure functions. Fast, no I/O. Naming: `Method_Scenario_ExpectedResult`.
- [ ] **Integration tests** — Repository with real DB (testcontainers). HTTP handlers with real router. Message queue with test instance. External service mocks at the network level (WireMock, MockServer).
- [ ] **Contract tests** — Between services. Pact or Spring Cloud Contract. "This is what I expect from you." Consumer defines expectations. Provider verifies. Catches breaking API changes before deploy.
- [ ] **Property-based testing** — Test invariants, not examples. "For any valid input, the output passes validation." `quicktest` (Go), `fast-check` (JS), `hypothesis` (Python). Finds edge cases you didn't think of.
- [ ] **Test data factories** — Don't hard-code test data in every test. Factory functions/object mothers generate valid entities with sensible defaults. Override only what the test cares about.
- [ ] **Load tests** — k6 or locust. Target realistic traffic patterns. Run against staging with production-like data volume. Don't just test the happy path at 1x traffic.
- [ ] **Chaos engineering** — Kill a random pod. Does the system recover? Circuit breakers open? Retries work? DLQ catches failed messages? Start small. Don't chaos test in production without experience.

## 14. Performance

- [ ] **Caching strategy** — Redis/Memcached. Cache-aside (app manages) or read-through. Invalidation is the hard part. Cache stampede protection (lock on miss or probabilistic early recompute). Separate cache per data type, don't share TTLs blindly.
- [ ] **Database query optimization** — Use `EXPLAIN ANALYZE`. Covering indexes. Avoid `SELECT *`. Batch inserts/updates. `INSERT ... ON CONFLICT` for upserts. Materialized views for expensive aggregations.
- [ ] **Connection pooling (DB, Redis, external)** — All outbound connections should pool. Max idle, max open, max lifetime (shorter than server-side timeout), connection timeout.
- [ ] **Async processing** — Anything that can be deferred: email, notifications, report generation, image processing. See Section 10 (Message Queues). Return 202 Accepted immediately, process in background.
- [ ] **Pagination and limits** — Every list endpoint has a default and max limit. No `SELECT * FROM huge_table` without pagination. Keyset pagination over offset for large/real-time datasets.
- [ ] **Graceful shutdown** — SIGTERM → stop accepting requests → drain in-flight (with timeout) → close DB pools → close message queue connections → exit. K8s `terminationGracePeriodSeconds` (default 30s) should exceed your drain timeout.
- [ ] **Startup warmup** — Preload caches, establish connection pools, validate config BEFORE reporting healthy. `ReadinessProbe` with `initialDelaySeconds` to allow warmup. Don't route traffic to a half-ready instance.

## 15. CI/CD

- [ ] **Pipeline stages** — Lint → type-check → unit test → build → integration test → deploy staging → E2E → deploy production. Fast feedback at every stage. Fail fast: lint fails first, don't wait for E2E to fail for a typo.
- [ ] **Build once, deploy many** — Same artifact (Docker image, binary) promoted through environments. Config changes via env vars, not rebuilds. Image tag = git SHA, not `:latest`.
- [ ] **Database migrations in deploy** — Run before new version starts. Backward-compatible: add column (nullable or with default) before old code reads it; remove column after old code stops writing it. Take a DB snapshot before running migrations in production.
- [ ] **Rollback plan** — Can you go back? Tested? Migrations reversible? Feature flags to disable broken features without redeploy? Rollback procedure in runbook.
- [ ] **Blue-green or canary deploy** — Zero-downtime deploys. Shift traffic gradually (canary: 5% → 25% → 50% → 100%). Health check new instances before routing. Auto-rollback on error rate spike.
- [ ] **GitOps** — Declarative config in git. PR merges trigger deploy. Git is the source of truth for what's running. No manual `kubectl edit` in production.

## 16. Documentation

- [ ] **README** — What it does, how to run locally (single command), how to deploy, architecture overview, link to API docs. New team member should be productive in < 30 minutes.
- [ ] **API documentation** — OpenAPI spec rendered (Swagger UI, Scalar, Redoc). Examples for every endpoint. Authentication instructions. Rate limit info. Deprecation notices.
- [ ] **Runbook** — Common operational tasks: restart, scale, run migration manually, revoke user session, rotate secrets, investigate slow queries, replay DLQ messages. Not everything — just the things someone needs at 3 AM.
- [ ] **Architecture Decision Records (ADRs)** — Why you chose PostgreSQL over MongoDB. Why JWT over sessions. Why this message broker, not that one. Date-stamped, immutable. Superseded ADRs link to the replacement.
- [ ] **Runbook testing** — Once a quarter: hand the runbook to someone new. Can they execute each procedure? Fix the gaps. A runbook that's never been tested is a wishlist.

## 17. Production Readiness

- [ ] **Graceful shutdown & startup** — See Section 13 (Performance). Health checks report ready only after warmup. Graceful shutdown drains in-flight requests.
- [ ] **Configuration management** — 12-factor app. Env vars for config. Feature flags (LaunchDarkly, Unleash, or simple DB table) for toggles. Kill broken features without redeploy.
- [ ] **Rate limiting & throttling** — API-level and user-level. Token bucket or sliding window. See Section 7 (Security) for endpoint-specific limits.
- [ ] **Idempotency** — Payment/order/any financial endpoint: idempotency key to prevent double-charge. Server stores key + result (with TTL). Client retries safely with same key. Stripe's `Idempotency-Key` header is the gold standard.
- [ ] **Webhook delivery (if applicable)** — Retry with backoff (4, 16, 64, 256 seconds). Signature verification (HMAC) so receivers can trust payload. Delivery logs visible to API consumer. Manual retry from dashboard.
- [ ] **Data backup & recovery** — Automated backups. Tested restore procedure. RPO (Recovery Point Objective) and RTO (Recovery Time Objective) defined and measured. Restore tested at least once per quarter.
- [ ] **Disaster recovery plan** — Documented. Tested at least once. How long to recover? What's the sequence? Who does what? Contact list with phone numbers. DR test results documented.

---

## Quick Sanity Check Before Launch

- [ ] All endpoints have auth (where needed) — verified by automated test
- [ ] No secrets in code, config, or git history — scanned, not assumed
- [ ] DB migrations run automatically and are reversible — tested rollback
- [ ] Health/ready checks work and are used by K8s/load balancer
- [ ] Logs are structured, include trace IDs, and are shipped to centralized system
- [ ] Alerts are configured and have fired in staging (silent alerts = broken alerts)
- [ ] Load tested at 2x expected peak — no timeouts, no OOM, no pool exhaustion
- [ ] Rollback tested — can you go from v2 to v1 without data loss?
- [ ] Runbook exists and has been tested by someone other than the author
- [ ] Docker image builds from scratch on a clean checkout
- [ ] Graceful shutdown tested (kill -TERM, observe zero errors during rollout)
- [ ] Circuit breaker opens within expected threshold when downstream is killed
- [ ] Idempotency keys prevent duplicate mutations (test: send same request twice)
