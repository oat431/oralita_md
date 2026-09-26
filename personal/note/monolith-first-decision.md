---
tags: [architecture, microservices, monolith, decision-notes, tradeoffs, software-engineering]
---

# Monolith First: When NOT to Use Microservices

> **Created:** 2026-09-26
> **Grew out of:** the swe-knowledge checklist gap — `swe-knowledge/checklist/release-checklist/Microservice Launch.md` tells you how to ship microservices safely but can't tell you whether you should have them at all.
> **The question:** Microservices are presented as the "production-grade" default. When are they actively the wrong choice?

## TL;DR

Start with a modular monolith. Split into services only when you have a *proven* reason: independent deploy cadence blocked by coupling, one module needing different scaling, team boundaries outgrowing the codebase, or polyglot/polydata requirements. Microservices convert in-process function calls into network calls, and with that single move you buy: distributed tracing, network failure handling, eventual consistency, contract testing, per-service CI/CD, service discovery, and a harder debugging loop. If your team is under ~10 engineers, those costs almost certainly exceed the benefits.

## 1. What a microservice actually costs

Every checklist in `swe-knowledge/checklist/microservice-checklist/` exists because of these costs — the checklists are the bill, not the menu:

| You gain | You pay |
|---|---|
| Independent deploys per service | N pipelines, N release trains, version-skew between services |
| Fault isolation | Network partitions, timeouts, retries, idempotency, circuit breakers — failure modes that don't exist in-process |
| Scale one module independently | Load balancing, autoscaling policy, per-service capacity planning |
| Team autonomy per service | Contract testing (Pact), schema registries, cross-service coordination for any change that touches two services |
| Polyglot freedom | N language runtimes to staff, secure, and upgrade |
| — | Distributed tracing, centralized logging, service mesh or discovery — observability is now infrastructure, not a library |

A monolith has one deploy, one debugger attach, one database transaction, one stack trace. That simplicity compounds.

## 2. The legitimate splitting forces

Split when you can name the force, not the vibe:

1. **Deploy coupling hurts** — team A ships daily, team B's module forces a full regression every release, and the wait is measurably slowing both.
2. **Scaling profiles diverge** — image transcoding needs 10× the CPU of the API tier; scaling the whole app is wasteful.
3. **Team size exceeds the codebase's communication capacity** — Conway's law: 4+ teams editing one deployable produce merge conflicts and coordination tax. This is the strongest legitimate force, and it's an *organizational* one, not technical.
4. **Isolation for blast radius** — a bug in reporting must never take down checkout. (Achievable in-process too, but a hard boundary makes it structural.)
5. **Genuinely different tech needs** — one module needs GPU workers or a document store while the rest is relational.

Note what's absent: "modern architecture", "resume", "we might need to scale someday". Someday is not a force.

## 3. Decision table

| Situation | Choose |
|---|---|
| New product, unvalidated domain | Modular monolith. You don't know the seams yet — splitting early puts boundaries in the wrong places, and moving a network boundary later is far harder than moving a module boundary |
| < 10 engineers, one product | Monolith. The coordination cost of services exceeds the benefit |
| Domain well understood, modules already clean, team growing past ~2 pizza teams | Start splitting — one service at a time, along the proven seam |
| Different scaling profiles proven by metrics | Split that module only (strangler fig), keep the rest monolithic |
| Org of many independent teams, each owning a product line | Services (or even separate monoliths per team — multiple monoliths beat one microservice mesh at mid scale) |
| Greenfield + "microservices from day one" + small team | Red flag. This is how distributed monoliths are born: all the network costs, none of the independence |

## 4. The modular monolith is the real prerequisite

"Monolith first" does not mean big ball of mud first. The monolith must be **modular**: clear internal module boundaries, dependency direction enforced (no cycles), domain logic separated from framework/transport, one module per bounded context. Then:

- Splitting later is *extracting* a module that already has clean edges — days of work, not months.
- If you can't keep module boundaries clean in one process, you won't keep service boundaries clean across a network. Services amplify whatever discipline you already lack.

This is why the recommendation is "modular monolith → services", never "monolith → services" and never "services first".

## 5. The distributed monolith trap

The worst of both worlds: N services that must deploy together, share a database, call each other synchronously in chains, and are owned by one team. Symptoms:

- A feature change routinely touches 3+ services
- Services share tables or a schema
- Deploys are coordinated releases across all services
- Nobody can explain what each service independently owns

If you see these, you paid microservice costs for monolith outcomes. The fix is usually to merge back — yes, that's allowed and sometimes celebrated (see Amazon Prime Video's 2023 merge of a serverless pipeline into a monolith for ~90% cost reduction).

## Key takeaways

- Default: modular monolith. Split on named forces (deploy cadence, scaling divergence, Conway's law), never on fashion.
- Microservices are an *organizational* solution that happens to be technical — if you don't have the org problem, you don't need the tech.
- Module boundaries in-process are cheap to move; network boundaries are expensive. Earn the seam before you cut it.
- The checklists in `swe-knowledge/checklist/microservice-checklist/` (load balancing, auth, messaging) are the running cost of the decision — read them as the price tag.
- Merging services back into a monolith is a legitimate, sometimes brilliant, move. Architecture is reversible if the boundaries were honest.

## Links

- Checklists this frames: `swe-knowledge/checklist/release-checklist/Microservice Launch.md`, `swe-knowledge/checklist/microservice-checklist/` (swe-knowledge vault)
- Related decision note: [[when-not-to-use-graphql]] — same pattern: adopt the heavier architecture only when a concrete force demands it
