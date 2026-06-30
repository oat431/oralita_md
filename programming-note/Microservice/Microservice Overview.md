---
tags:
- architecture
- microservices
- overview
- programming
---

# Microservice Architecture — Overview

A practical guide to designing, building, and operating microservice systems. From decomposition to deployment — with the patterns, tools, and trade-offs you need in production.

> For the architectural philosophy behind service boundaries, see **[[Boundaries]]** and **[[Main Component and Services]]** in the Clean Architecture vault.

---

## Topics

### 01 Decomposition

> [[01 Decomposition Patterns]] — How to split a monolith: by business capability, subdomain, transaction boundary

### 02 Integration

> [[02 API Gateway]] — Single entry point, routing, auth, rate limiting
> [[02 Event-Driven Architecture]] — Async communication, event bus, pub/sub
> [[02 Messaging Patterns]] — Kafka, RabbitMQ, message ordering, idempotency

### 03 Database

> [[03 Database per Service]] — Isolation, data ownership, shared-nothing
> [[03 Saga Pattern]] — Distributed transactions across services
> [[03 CQRS & Event Sourcing]] — Separate read/write models, audit trails

### 04 Resilience

> [[04 Circuit Breaker]] — Stop cascading failures before they spread
> [[04 Bulkhead Pattern]] — Isolate failures to contained compartments
> [[04 Retry & Timeout]] — When to retry, when to give up, how to degrade

### 05 Observability

> [[05 Logging & Monitoring]] — Centralized logs, metrics, dashboards
> [[05 Distributed Tracing]] — Follow a request across services
> [[05 Health Checks]] — Liveness, readiness, dependency checks

### 06 Cross-Cutting

> [[06 Service Discovery]] — How services find each other at runtime
> [[06 Configuration Management]] — Externalized config, feature flags
> [[06 Security Patterns]] — mTLS, OAuth2, API keys, zero-trust

### 07 Deployment

> [[07 Containers & Orchestration]] — Docker, Kubernetes, pod architecture
> [[07 Deployment Strategies]] — Blue-green, canary, rolling updates
> [[07 Service Mesh]] — Istio, Linkerd, sidecar proxies

---

## My Experiments

| Component | Repository |
|-----------|-----------|
| API Gateway | [try-api-gateway](https://github.com/oat431/try-api-gateway) |
| Service Discovery | [spb3-service-discovery](https://github.com/oat431/spb3-service-discovery) |
| REST Service | [spb3-demo-rest-api](https://github.com/oat431/spb3-demo-rest-api) |
| GraphQL Service | [spb3-demo-graphql-api](https://github.com/oat431/spb3-demo-graphql-api) |
| DB Service | [spb3-dynamic-allowed-cors](https://github.com/oat431/spb3-dynamic-allowed-cors) |

> Home server: Ubuntu 24.04 at [server.panomete.com](https://server.panomete.com)

---

## How to Read

| Goal | Path |
|------|------|
| **Designing a new system** | 01 → 02 → 03 (decompose first, then integrate, then handle data) |
| **System keeps breaking** | 04 (resilience) → 05 (observability — you can't fix what you can't see) |
| **Deploying to production** | 07 → 06 (deployment + cross-cutting concerns) |
| **Quick reference** | Each file is self-contained |

---

## Sources

- Newman, Sam. *Building Microservices*, 2nd ed., O'Reilly, 2021.
- Richardson, Chris. *Microservices Patterns*, Manning, 2018.
