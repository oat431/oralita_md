---
tags:
- clean-architecture
- software-design
- software-engineering
---

# The Missing Chapter

> *Source: Clean Architecture by Robert C. Martin, Chapter 34 — Written by Simon Brown (pp. 225–240)*

---

## Core Principle

> **Your best design intentions are destroyed in a flash if you ignore implementation details. Use your programming language's access modifiers and the compiler to enforce architectural boundaries — not discipline, code reviews, or post-compilation tooling.**

Architectural styles (layered, ports and adapters, feature-based) look different on whiteboards but collapse into identical code when types are marked `public` indiscriminately. The missing chapter fills the gap between architectural diagrams and code: how to organize packages so the compiler — not trust — keeps dependencies clean.

---

## The Four Approaches to Code Organization

### 1. Package by Layer (Horizontal Slicing)

The traditional layered architecture groups code by technical function: `web`, `service`, `repository`. A web controller (`OrdersController`) depends on a service interface (`OrdersService`), which is implemented by `OrdersServiceImpl`, which depends on a repository interface (`OrdersRepository`), implemented by `JdbcOrdersRepository`. Dependencies always point downward.

**Strengths:**
- Fastest way to get a project running. Minimal upfront complexity.
- Most tutorials, books, and sample code default to this approach.

**Weaknesses:**
- Doesn't scream anything about the business domain. Put two layered architectures from different domains side by side — they look identical: `web`, `services`, `repositories`.
- As the system grows, three large buckets become insufficient; further modularization becomes necessary but unnatural.
- **Critical flaw:** Nothing prevents a controller from bypassing the service layer and calling the repository directly (the "relaxed layered architecture" problem). A new developer sees `OrdersRepository` is public, injects it into `OrdersController`, and skips business logic — creating a path that may bypass authorization, validation, or audit rules.

```
web/
  OrdersController         (public — depends on service interface)
service/
  OrdersService            (public — interface, needed by web)
  OrdersServiceImpl        (package-private possible — implementation detail)
repository/
  OrdersRepository         (public — interface, needed by service impl)
  JdbcOrdersRepository     (package-private possible — implementation detail)
```

> Everything needed across boundaries must be `public`, opening the door to bypassing layers.

---

### 2. Package by Feature (Vertical Slicing)

Organize code by domain concept, feature, or aggregate root. All types for a single use case live in one Java package named after the concept.

```
orders/
  OrdersController         (public — sole entry point)
  OrdersService            (package-private possible)
  OrdersServiceImpl        (package-private possible)
  OrdersRepository         (package-private possible)
  JdbcOrdersRepository     (package-private possible)
```

**Strengths:**
- The top-level organization screams the business domain. You immediately see this codebase deals with "orders."
- Easier to find all code related to a feature when changes are needed.
- Only the controller must be `public`; everything else can be `package-private` — better encapsulation.

**Weaknesses:**
- Nothing outside this package can access order-related information except through the controller. This may or may not be desirable depending on the use case.
- Still suboptimal for larger systems. It's a simple refactoring from "package by layer" but doesn't address the fundamental coupling problem at the architectural level.

> Many teams realize horizontal layering fails and switch to vertical layering — both are suboptimal compared to what comes next.

---

### 3. Ports and Adapters (Hexagonal Architecture)

Separate code into an **inside** (domain) and an **outside** (infrastructure). The outside depends on the inside — never the other way around. Domain code is independent of frameworks, databases, and delivery mechanisms.

```
domain/                   ← Inside (zero external dependencies)
  OrdersService           (public — interface)
  OrdersServiceImpl       (package-private — implementation)
  Orders                  (public — domain entity, named in ubiquitous language)

web/                      ← Outside (depends on domain)
  OrdersController        (public)

database/                 ← Outside (depends on domain)
  JdbcOrdersRepository    (package-private)
```

**Key observations:**
- The repository interface is renamed `Orders` (not `OrdersRepository`), using the ubiquitous domain language. In conversation you say "orders," not "orders repository."
- Domain interfaces (`OrdersService`, `Orders`) are `public` because they have inbound dependencies from outside packages.
- Implementation classes (`OrdersServiceImpl`, `JdbcOrdersRepository`) can be `package-private` and dependency-injected at runtime.
- This is a simplified diagram — real implementations include interactors, boundary objects, and DTOs for crossing dependency boundaries.

---

### 4. Package by Component (Simon Brown's Preferred Approach)

Bundle all responsibilities related to a single coarse-grained component into one Java package. The user interface stays separate. A component encapsulates its business logic and persistence behind a clean interface — consumers see only the interface, not the internals.

```
orders/
  OrdersComponent         (public — interface, one entry point)
  OrdersServiceImpl       (package-private — implementation detail)
  OrdersRepository        (package-private — implementation detail)
  JdbcOrdersRepository    (package-private — implementation detail)

web/
  OrdersController        (depends on OrdersComponent interface only)
```

**Simon Brown's definition of a component:**
> *"A grouping of related functionality behind a nice clean interface, which resides inside an execution environment like an application."*

This differs from Uncle Bob's definition (units of deployment / jar files). Whether each component lives in a separate jar is an orthogonal concern.

**Key benefits:**
- One place to go for anything orders-related: `OrdersComponent`.
- The compiler enforces architectural boundaries. Code outside the package **cannot** access `OrdersRepository` or `OrdersServiceImpl` directly — they're package-private. No static analysis tools, no code review discipline, no trust required.
- A stepping stone to micro-services. Well-defined components in a monolith can be extracted later into separate services.
- The separation of concerns (business logic vs. persistence) is preserved *inside* the component as an implementation detail.

---

## Organization vs. Encapsulation

> *The critical insight that makes or breaks all four approaches.*

If all types in a Java application are marked `public`, packages become **mere organization mechanisms** (like folders) rather than **encapsulation boundaries**. When everything is reachable from anywhere, all four architectural styles become syntactically identical — they collapse into a traditional layered architecture, regardless of what you call them.

The table below shows which types *must* be `public` for each approach:

| Approach | Must Be `public` | Can Be `package-private` |
|---|---|---|
| Package by Layer | `OrdersService`, `OrdersRepository` (interfaces) | `OrdersServiceImpl`, `JdbcOrdersRepository` |
| Package by Feature | `OrdersController` (sole entry) | Everything else |
| Ports and Adapters | `OrdersService`, `Orders` (domain interfaces) | `OrdersServiceImpl`, `JdbcOrdersRepository` |
| **Package by Component** | `OrdersComponent` (interface only) | **Everything else** |

**Package by Component** minimizes the number of public types — and therefore minimizes the attack surface for inappropriate dependencies. Fewer public types = fewer potential dependency violations = stronger compiler-enforced boundaries.

> *"If you ignore the packages, it doesn't really matter which architectural style you're aspiring to create."*

The difference between a clean architecture and a big ball of mud is **whether you use your language's access modifiers to enforce boundaries at compile time.**

---

## Other Decoupling Modes

### Module Systems (OSGi, Java 9 Modules)

Module frameworks distinguish between types that are `public` and types that are **published**. You can create an `Orders` module where all types are `public` internally but only a small subset is exported for external consumption. Java 9's module system brings this distinction natively to the language.

### Separate Source Code Trees

Split code across build modules/projects with compile-time dependencies:

**Ideal approach (one tree per component):**
```
domain/src         → OrdersService, OrdersServiceImpl, Orders
web/src            → OrdersController (compile-depends on domain)
persistence/src    → JdbcOrdersRepository (compile-depends on domain)
```

This enforces dependencies at the build tool level (Maven, Gradle, MSBuild). Domain code knows nothing about web or persistence.

**Pragmatic two-tree approach:**
```
domain/src         → All domain code (the "inside")
infrastructure/src → Web, database, external APIs (the "outside")
```

This maps cleanly to the Ports and Adapters diagram, with infrastructure depending on domain at compile time.

### ⚠️ The Périphérique Anti-Pattern

Named after the Boulevard Périphérique ring road in Paris (which lets you circumnavigate the city without entering it): having all infrastructure code in a single source tree means a web controller can directly call a database repository without going through the domain. This is the same bypass problem from the "relaxed layered architecture" — now at the source tree level. If you forget to apply access modifiers, the ring road becomes an expressway to chaos.

---

## Summary Checklist

- [ ] Understand that all four organizational approaches collapse into the same thing if everything is `public`
- [ ] Prefer **Package by Component** — one interface per component, everything else package-private
- [ ] Use the compiler to enforce architectural boundaries, not discipline or code reviews
- [ ] Minimize `public` types to minimize the attack surface for inappropriate dependencies
- [ ] Separate infrastructure code from domain code at the source tree level where practical
- [ ] Watch for the Périphérique anti-pattern — infrastructure code bypassing the domain
- [ ] Treat well-defined components in a monolith as stepping stones to micro-services
- [ ] Appreciate Java 9 module systems (`public` vs. `published`) as an additional enforcement tool
- [ ] The devil is in the implementation details — architectural intent means nothing without correct access modifiers

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[Component Cohesion]]
- [[Component Coupling]]
- [[Boundaries]]
- [[Architectural Independence]]
- [[Layers and Boundaries]]
