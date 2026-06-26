# API Design & Protocols — Overview

APIs are the contracts between systems. Design them well and they last for years. Design them poorly and every integration is a firefight. This vault covers REST, GraphQL, gRPC, WebSocket, WebHook — plus the security and operations that keep them running.

---

## Topics

### 01 API Design

> [[01 REST API Design]] — Resources, HTTP verbs, status codes, versioning, HATEOAS, pagination
> [[01 OpenAPI & Documentation]] — Swagger/OpenAPI, auto-generated docs, developer portals

### 02 API Protocols

> [[02 GraphQL]] — Queries, mutations, subscriptions, schema-first design, vs REST
> [[02 gRPC]] — Protobuf, streaming, HTTP/2, code generation, vs REST
> [[02 WebSocket]] — Persistent connections, real-time use cases, vs polling
> [[02 WebHook]] — Event-driven callbacks, idempotency, retry, vs polling
> [[02 SOAP, MQTT & AMQP]] — Legacy enterprise, IoT messaging, wire-level protocol reference

### 03 API Security

> [[03 Authentication]] — JWT, OAuth2, API keys, session vs token, mTLS
> [[03 Authorization & Rate Limiting]] — RBAC, scopes, claims, throttling, quotas

### 04 API Operations

> [[04 API Monitoring]] — Metrics, error tracking, alerting, SLAs
> [[04 API CI-CD]] — Testing, contract testing, versioning, deployment strategies

---

## Protocol Decision Guide

| Need | Use |
|------|-----|
| CRUD, web/mobile clients, caching | **REST** |
| Flexible queries, many client types, complex nested data | **GraphQL** |
| High-performance service-to-service, microservices | **gRPC** |
| Real-time bidirectional (chat, live feed, gaming) | **WebSocket** |
| Server-to-server event notifications (GitHub → CI, Stripe → app) | **WebHook** |

---

## How to Read

| Goal | Path |
|------|------|
| **Designing a new API** | 01 API Design → pick a protocol from 02 |
| **Choosing between REST/GraphQL/gRPC** | Read all 4 protocol files in 02, compare |
| **Securing an existing API** | 03 API Security |
| **Deploying to production** | 04 API Operations |

---

## Sources

- Fielding, Roy. *Architectural Styles and the Design of Network-based Software Architectures*, 2000. (REST dissertation)
- GraphQL Spec — https://spec.graphql.org/
- gRPC — https://grpc.io/
