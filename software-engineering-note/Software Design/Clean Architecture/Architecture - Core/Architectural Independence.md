---
tags:
- clean-architecture
- software-design
- software-engineering
---

# Architectural Independence

> *Source: Clean Architecture by Robert C. Martin, Chapter 16 (pp. 125–132)*

---

## Core Principle

> **A good architecture maximizes options by decoupling the system along three axes — horizontal layers, vertical use cases, and operational modes — so that development, deployment, and operation can proceed independently. Decouple to the point where a service *could* be formed, but keep components together as long as practical.**

Independence does not mean micro-services by default. It means the architecture does not *assume* how components communicate, where they live, or which team owns them. The system should be able to start life as a monolith, grow into independently deployable units, then into services — and shrink back down when operational demands subside. Every decoupling decision is a bet against future change; the architect's job is to place the fewest bets possible.

---

## The Rules / Key Concepts

### 1. Four Pillars Architecture Must Support

**A good architecture must simultaneously support (1) use cases, (2) operation, (3) development, and (4) deployment.**

- **Use cases:** The architecture must make the system's intent visible — behavior should be a first-class element at the top level, not buried and hidden.
- **Operation:** The architecture must handle throughput and response-time demands without baking in assumptions about threads, processes, or services.
- **Development:** Conway's Law says system structure mirrors communication structure. Architecture must partition the system so multiple teams can work independently without interference.
- **Deployment:** The goal is *immediate deployment* — a single build, no manual configuration scripts, no directory creation, no property-file tweaks.

These four pillars are indistinct and inconstant goals. They change over time. Architecture must balance them by leaving options open.

### 2. Decoupling Layers — The Horizontal Split

**Separate parts of the system that change at different rates and for different reasons, using the Single Responsibility Principle and the Common Closure Principle.**

The obvious horizontal slices are:

- **UI** — changes for presentation and user-experience reasons, independent of business logic.
- **Application-specific business rules** — validation logic tied closely to this particular application.
- **Application-independent business rules / domain** — core domain rules (interest calculation, inventory counting) that change at the slowest rate.
- **Database and technical details** — schema, query language, persistence mechanics. They change for reasons unrelated to business rules.

Each layer is decoupled so it can change independently without cascading changes through the system.

### 3. Decoupling Use Cases — The Vertical Split

**Use cases are narrow vertical slices that cut through all horizontal layers. Separate them from one another.**

The add-order use case changes at a different rate and for different reasons than the delete-order use case. To achieve this:

- Give each use case its own slice of the UI.
- Give each use case its own slice of application-specific business rules.
- Give each use case its own slice of domain rules and database access.

When use cases are vertically independent, adding a new use case does not interfere with existing ones. The system remains stable under growth.

### 4. Decoupling Mode — The Third Dimension (Operational)

**Decoupling for use cases also serves operations — but only if the *mode* of decoupling matches the operational need.**

If components must run on separate servers for throughput reasons, they cannot depend on being in the same address space. They must be independent services communicating over a network. Sometimes that is necessary. But the architect does not default to services. The *mode* is itself an option to leave open:

| Mode | Communication | Execution |
|---|---|---|
| Source-level | Function calls | Single executable, same address space |
| Deployment-level | Function calls or IPC | Separate jar/DLL/Gem files, same or different processes |
| Service-level | Network packets | Independent executables, separate servers |

### 5. Independent Develop-ability

**When layers and use cases are strongly decoupled, teams can work in parallel without stepping on each other.**

If the business rules don't know about the UI, the UI team cannot accidentally break the business rules team. If the add-order use case is decoupled from delete-order, one team's work does not block the other. The architecture supports any team organization — feature teams, component teams, layer teams — without forcing reorganization when the team structure changes.

### 6. Independent Deployability

**Well-decoupled use cases and layers enable hot-swapping at runtime and zero-downtime deployment.**

Adding a new use case should be as simple as dropping in a few new JAR files or services while leaving the rest of the system untouched. The same applies to upgrading layers independently.

### 7. The Duplication Dilemma — Real vs. Accidental Duplication

**Not all duplication is evil. Knee-jerk elimination of duplicate-looking code is a trap.**

- **True duplication:** Every change to one instance *must* be repeated in every copy. Eliminate it ruthlessly.
- **Accidental duplication:** Two pieces of code look similar today but will evolve along different paths, at different rates, for different reasons. If you unify them now, separating them later will be painful.

Examples:
- Two use cases have similar screen structures → likely accidental. Let them diverge.
- A database record looks identical to a screen view model → don't pass the DB record straight to the UI. Create a separate view model. The small duplication cost buys long-term decoupling.

**The rule: When separating use cases vertically, resist the temptation to couple them over superficial similarity. When separating layers horizontally, resist passing data structures across boundaries just to avoid a small mapping effort. Confirm the duplication is real before removing it.**

### 8. Decoupling Modes — Strategy for Choosing

**Don't decouple at the service level by default. Push decoupling to the point where a service *could* be formed, then keep components together in-process as long as possible.**

Service-level decoupling by default has two problems:
1. **Expensive in development time** — dealing with service boundaries where none are needed is wasted effort.
2. **Encourages coarse-grained decoupling** — no matter how "micro" the micro-services get, the boundaries won't be fine-grained enough.

The pragmatic progression:
1. Start with **source-level** decoupling — a well-structured monolith.
2. If deployment or development friction arises, shift some components to **deployment-level** decoupling (separate DLLs/JARs).
3. As operational needs grow, carefully choose which deployable units to promote to **services**.
4. When operational needs decline, slide back down — services → deployable units → monolith.

A good architecture protects the majority of source code from these mode transitions. The mode should be changeable without rewriting the system.

---

## Summary Checklist

- [ ] Are use cases visible as **first-class elements** at the top level of the architecture, not buried in implementation details?
- [ ] Are **horizontal layers** (UI, application-specific rules, domain rules, database) decoupled so each can change independently?
- [ ] Are **vertical use cases** (add-order, delete-order, etc.) decoupled from one another across all layers?
- [ ] Does the architecture avoid assuming communication means between components — could it transition from in-process calls to network services without major rewrites?
- [ ] Can the system be deployed with a **single action** after build, with no manual configuration scripts?
- [ ] Does the architecture enable **independent team development** — can a team working on one use case proceed without blocking a team on another?
- [ ] Can new use cases be added by dropping in new deployable units (JARs, DLLs, services) without touching the rest of the system?
- [ ] Before eliminating duplicate code, have you confirmed it is **true duplication** (must change together) rather than **accidental** (similar now, will diverge)?
- [ ] Are view models kept separate from database records even when they look identical — to preserve layer decoupling?
- [ ] Is the system decoupled to the point where a **service *could* be formed** — but components remain in-process *as long as practical*?
- [ ] Can the decoupling mode slide down (services → deployable units → monolith) when operational demands decrease?

---

## Related

- [[Clean Architecture Overview]]
- [[What Is Architecture]]
- [[Boundaries]]
- [[The Clean Architecture]]
- [[Component Cohesion]]
- [[Component Coupling]]
- [[Screaming Architecture]]
- [[Layers and Boundaries]]
- [[Main Component and Services]]
