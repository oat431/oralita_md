# Microservice Launch Checklist

> Tick every box before a multi-service system hits production. Assumes you've already done the [[Backend Launch]] checklist for each individual service.

---

## Service Discovery

- [ ] All services find each other without hardcoded URLs → [[06 Service Discovery]]
- [ ] New instances register on startup, deregister on graceful shutdown
- [ ] Dead instances evicted from registry within 90s
- [ ] Registry itself is highly available (≥2 nodes for production)
- [ ] Registry secured (at minimum, basic auth on management endpoints)
- [ ] No business data stored in the registry

---

## Load Balancing

- [ ] Edge LB is the ONLY entry point from the internet → [[07 Containers & Orchestration]]
- [ ] TLS terminated at the edge with auto-renewed certificates → [[03 Network & TLS]]
- [ ] Health checks active on all upstream instances → [[05 Health Checks]]
- [ ] Unhealthy instances removed from pool automatically
- [ ] Algorithm chosen with documented reasoning (round-robin default) → [[03 Load Balancing & Proxies]]
- [ ] Sticky sessions avoided unless specifically justified
- [ ] Edge LB itself is not a SPOF

---

## API Gateway

- [ ] Gateway is the single entry point — no direct service exposure → [[02 API Gateway]]
- [ ] Routes configured for all services (YAML or programmatic)
- [ ] Rate limiting per client/service at the gateway → [[03 API Security]]
- [ ] Request/response logging at gateway (audit trail)
- [ ] CORS handled at gateway, not in individual services
- [ ] Gateway validates JWT before forwarding to services → [[03 Authentication]]

---

## Authentication (System-Wide)

- [ ] Dedicated auth server (Keycloak/Auth0/Okta) — never embedded in an app → [[03 Authentication]]
- [ ] Authorization Code + PKCE for user-facing login flows
- [ ] Client Credentials for service-to-service calls
- [ ] Access tokens: short-lived (≤15 min), signed (RS256/ES256)
- [ ] Refresh tokens: long-lived, rotated on each use
- [ ] JWKS endpoint available, keys cached by resource servers
- [ ] Every service validates JWT independently (not just gateway) → [[03 API Security]]

---

## Resilience (System-Wide)

- [ ] Circuit breaker on every service-to-service call → [[04 Circuit Breaker]]
- [ ] Bulkheads: isolate critical services (separate thread pools/instances) → [[04 Bulkhead Pattern]]
- [ ] Retry + timeout on all inter-service calls → [[04 Retry & Timeout]]
- [ ] Fallback responses for degraded dependencies
- [ ] No cascading failures possible (one service down ≠ system down)

---

## Data & Messaging

- [ ] Each service owns its database — no shared DB access → [[03 Database per Service]]
- [ ] Async communication via events where synchronous isn't needed → [[02 Event-Driven Architecture]]
- [ ] Dead letter queue for failed messages → [[02 Messaging Patterns]]
- [ ] Saga pattern for distributed transactions (not 2PC) → [[03 Saga Pattern]]
- [ ] Idempotent consumers (duplicate messages don't cause duplicate effects)

---

## Observability (System-Wide)

- [ ] Distributed tracing across all services → [[05 Distributed Tracing]]
- [ ] Centralized logging (ELK stack, Grafana Loki, or equivalent) → [[05 Logging & Monitoring]]
- [ ] Service dashboard: per-service health, circuit states, error rates
- [ ] Alert on: any circuit open, any service down, inter-service latency spike

---

## Deployment

- [ ] Infrastructure as Code (Docker Compose for dev, Terraform/Pulumi for prod)
- [ ] Service startup order handled (dependencies start first, or services retry)
- [ ] Rolling deployments with health checks — no downtime
- [ ] Feature toggles for cross-service changes → [[06 Configuration Management]]
- [ ] Service mesh considered (mTLS, traffic splitting) → [[07 Service Mesh]]

---

## Sources

- Distilled from: [[Microservice Overview]], [[Cybersecurity Overview]], [[API Overview]].
- Original deep reference: `../microservice-infrastructure.md`
