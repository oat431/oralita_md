---
tags: [api-design, graphql, rest, decision-notes, tradeoffs, software-engineering]
---

# When NOT to Use GraphQL: A Decision Note

> **Created:** 2026-09-26
> **Grew out of:** the swe-knowledge checklist gap — `swe-knowledge/checklist/api-checklist/api.md` §4 says "GraphQL only if the client genuinely needs flexible queries" but a checkbox can't carry the *why*.
> **The question:** Everyone defaults to "REST vs GraphQL" as a style preference. When is GraphQL actually the wrong choice?

## TL;DR

GraphQL earns its complexity in exactly one situation: **many diverse clients querying overlapping data, where you can't predict their shapes** (public APIs, mobile apps on bad networks, BFF for heterogeneous products). Outside that, REST + good design wins: simpler caching (HTTP cache is free, GraphQL caching is a project), simpler authorization (per-endpoint vs per-field), simpler errors, simpler tooling. The most common GraphQL mistake is adopting it for an internal service-to-service API that gRPC or plain REST would serve better.

## 1. The costs you pay on day one

GraphQL is not free flexibility — every feature has a bill:

| Cost | REST equivalent | Why it matters |
|---|---|---|
| **Caching** | HTTP cache: `Cache-Control`, ETags, CDN — all free | GraphQL is POST to one endpoint. You must build caching: persisted queries, Apollo Client normalization, or a proxy layer (CDN-level GraphQL caching is a product you buy or an infra project you own) |
| **Authorization** | Middleware per route: `/admin/* → admin role` | Must be **per-field, per-resolver**. One query can touch 12 types; each resolver needs its own authz check or you leak data through nested fields |
| **Query cost control** | Rate limit per endpoint | Clients can write O(depth × fanout) queries that melt your DB. You need query depth limits, complexity analysis, persisted-query allowlists |
| **N+1 at the resolver layer** | Joins in SQL | Naive resolvers fire one query per field per object. You must build DataLoader batching — correct but subtle |
| **Error semantics** | HTTP status codes are universal | GraphQL returns `200 OK` with an `errors` array. Clients must inspect the body. Partial success makes error handling genuinely harder |
| **File uploads, streaming, webhooks** | Native HTTP patterns | Bolted-on specs, weaker ecosystem support |
| **Schema maintenance** | Spec drift is your problem anyway | SDL + codegen + resolver wiring + federation (if multi-team) is real ongoing work |

## 2. The one situation where it wins

GraphQL pays off when **the client set is diverse and unpredictable**:

- Public API with third-party developers building unknown UIs
- Mobile apps on constrained networks needing exact field selection (bandwidth)
- One backend feeding web + iOS + Android + partner integrations, each wanting different shapes
- Aggregation layer (BFF) stitching many microservices into one client-facing surface

The keyword is *unpredictable shapes*. If you can enumerate what clients need — and you almost always can for internal systems — REST endpoints named after those needs are simpler and faster.

## 3. Decision table

| Situation | Choose |
|---|---|
| Internal service-to-service | gRPC (typed contracts, streaming, performance) or REST |
| CRUD app, one frontend, one backend | REST + OpenAPI. You're done. |
| Public API, third-party developers, varied clients | **GraphQL** — this is its home turf |
| Mobile + web + tablet on shared data, bandwidth-sensitive | **GraphQL** (field selection) or BFF-per-client with REST |
| Admin dashboard | REST. Nobody is bandwidth-constrained on an internal tool |
| Real-time heavy (chat, presence, feeds) | WebSocket/SSE; GraphQL subscriptions exist but add cost without adding capability |
| Team has zero GraphQL experience, deadline pressure | REST. Learning cost lands exactly when you can least afford it |

## 4. The migration trap

A common failure mode: team adopts GraphQL, then discovers they've rebuilt REST inside it — one query per "endpoint", no nesting, no fragments shared across clients. If your GraphQL schema is a 1:1 map of your old REST routes, you paid all the costs and bought none of the benefits. Conversely, if you're considering GraphQL to "future-proof" the API: you can't future-proof an interface against unknown futures; you can only keep it cheap to change. REST + versioning (or contract tests) is the cheaper thing to change.

## 5. Hybrid is legitimate

You don't choose once, globally:

- REST for CRUD and public docs, GraphQL gateway only at the BFF edge
- GraphQL federation when multiple teams own subgraphs — but only at the org size where independent schema ownership is real
- REST internally, GraphQL externally, same domain layer underneath

## Key takeaways

- GraphQL's value = unpredictable, diverse clients × shared data. Remove either factor and it's mostly cost.
- The three hidden bills: caching, per-field authorization, query cost control. Budget for all three or don't adopt.
- "GraphQL shaped exactly like our old REST routes" is the most common adoption failure — it's a signal the use case wasn't there.
- Default to REST + OpenAPI; let a concrete client-diversity problem pull you to GraphQL, never a trend push you there.

## Links

- Checklist item this explains: `swe-knowledge/checklist/api-checklist/api.md` §4 "API Design" (swe-knowledge vault)
- Related decision note: [[monolith-first-decision]] — same pattern: the architecture must follow the problem, not the fashion
