---
tags:
- clean-architecture
- software-design
- software-engineering
---

# Boundaries

> *Source: Clean Architecture by Robert C. Martin, Chapters 17–18 (pp. 133–148)*

---

## Core Principle

> **Software architecture is the art of drawing lines — boundaries — that separate software elements and restrict knowledge on one side from knowing about the other. The goal is to defer decisions that don't matter (frameworks, databases, web servers) for as long as possible, keeping the core business logic unpolluted by premature choices.**

The cost of coupling to premature decisions is enormous — multiplied development effort, fragile systems, and person-hours flushed into architectural rabbit holes. A good architecture treats I/O, databases, GUIs, and frameworks as *plugins* to the business rules. The dependency arrows always point inward — from details toward the core. This single rule, applied consistently, creates firewalls across which changes cannot propagate.

---

## Drawing Lines (Ch17)

### 1. Premature Decisions Are the Enemy

**Decisions that are premature are those that have nothing to do with the business requirements — the use cases.**

Frameworks, databases, web servers, dependency injection libraries, utility toolkits — these are *details*. A good system architecture makes these decisions ancillary and deferrable. You should be able to swap them out at the latest possible moment without significant impact. The architect's goal is to minimize human resources; coupling to premature decisions is what saps that resource.

The history of software is littered with architectures that bet on the wrong technology too early. The cost isn't just the initial wrong choice — it's the compounding tax of every feature built on top of that premature commitment.

### 2. The Sad Story of Company P — Three-Tier Gone Wrong

**A monolithic desktop app was "webified" by architects who prematurely committed to a distributed three-tier topology before the business needed it.**

In the late 1990s, the architects decreed that every domain object would have three instantiations — one in the GUI tier, one in the middleware tier, one in the database tier — living on different machines. Method invocations between tiers were serialized and marshaled across the wire. Adding a simple field to a record required:

- Adding the field to classes in **all three tiers**
- Designing **four message protocols** (data traveled both ways)
- Building **eight protocol handlers** (send + receive per protocol)
- Rebuilding **three executables**, each with updated business objects, messages, and handlers

The developers ran all three executables on a **single machine** for years — instantiating objects, serializing, marshaling, socket-communicating — despite never needing a server farm. Company P *never sold a system that required one*. Every deployed system was a single server, but the development tax had already been paid in full, multiplied across every feature.

**Lesson:** Premature topological decisions multiply development effort enormously. A three-tier topology is not an architecture; it's a deployment detail. Good architecture defers it.

### 3. The Sad Story of Company W — SOA Madness

**A small business managing company-car fleets was saddled with an enterprise-scale, service-oriented "architecture" that turned simple operations into Kafkaesque rituals.**

Adding a contact name, address, and phone number to a sales record required: looking up the service ID in a `ServiceRegistry`, sending a `CreateContact` message with dozens of fields the programmer didn't have data for (so they faked it), jamming the new contact ID into the sales record, then sending an `UpdateContact` message. Testing required firing up every service, the message bus, the BPEL server, and waiting through propagation delays.

Adding a new feature meant changing coupled services, updating WSDLs, and redeploying everything.

**Lesson:** There is nothing intrinsically wrong with service-oriented systems. The error was the *premature adoption and enforcement* of a massive suite of domain object services. The cost was person-hours in droves — flushed into the SOA vortex.

### 4. The FitNesse Success Story — Defer to Nonexistence

**FitNesse, the acceptance-testing wiki, drew boundaries early and deferred decisions into irrelevance.**

Key early decisions:

- **Web server:** Wrote their own bare-bones web server instead of adopting a framework. A basic web server is trivially simple to write, and this postponed any web-framework decision for years. (Velocity was eventually slipped in much later.)
- **Database:** Put an interface `WikiPage` between all data accesses and the actual storage. For three months, they worked on wiki-text-to-HTML translation with a `MockWikiPage` that left data access stubbed. When stubs became insufficient, they wrote `InMemoryPage` using a hash table in RAM. This powered an entire year of features — creating pages, linking, wiki formatting, even running FIT tests — without any persistence.
- **Persistence:** When the time came, they wrote `FileSystemWikiPage` to flush the hash tables to flat files. Three months later, flat files were deemed good enough. MySQL was abandoned entirely.
- **Surprise:** A customer later needed MySQL. Using the `WikiPage` interface, he wrote a `MySqlWikiPage` derivative and had the whole system working in a day.

**The payoff:** 18 months of development without schema issues, query issues, database server issues, password issues, connection timeouts. All tests ran fast — no database to slow them down. The boundary line between business rules and the database saved enormous time and headaches.

### 5. Where to Draw the Lines — GUI, Business Rules, Database

**Draw boundaries between things that matter and things that don't — and between things that matter to each other.**

Three critical boundaries:

| Boundary | Why |
|---|---|
| **Business Rules ↔ Database** | Business rules only need functions to fetch/save data. They don't need schemas, query languages, or connection details. Put the database behind an interface. |
| **Business Rules ↔ GUI** | The GUI doesn't matter to the business rules. The model would happily execute without any display. The IO is irrelevant. |
| **GUI ↔ Database** | The GUI doesn't care about the database, and the database doesn't care about the GUI. |

The boundary line is drawn across the **inheritance relationship**, just below the interface. The `DatabaseInterface` lives in the `BusinessRules` component. The `DatabaseAccess` implementation lives in the `Database` component. The arrow points from `Database` → `BusinessRules`. This means:

- The `Database` knows about (depends on) the `BusinessRules`
- The `BusinessRules` do **not** know about the `Database`
- The `Database` cannot exist without the `BusinessRules`, but the reverse is not true

This directional dependency means the business rules can use Oracle, MySQL, flat files, or anything else — they don't care. The database decision can be deferred until the business rules are written and tested.

### 6. I/O Is Irrelevant

**Developers and customers often confuse the system with its interface. The GUI is not the system; the model behind it is.**

Consider a video game. Your experience is dominated by the screen, mouse, buttons, and sounds. But behind that interface is a model — a sophisticated set of data structures and functions — that would happily execute all game events without ever being displayed. The interface does not matter to the business rules.

This means the GUI is a plugin. It plugs into the business rules, not the other way around. The GUI component depends on the `BusinessRules` component; the `BusinessRules` component is completely independent.

### 7. Plugin Architecture — The Universal Pattern

**Treating the database and GUI as plugins creates a pattern that generalizes to all optional or swappable components.**

The core business rules sit at the center. Around them, a ring of plugin components — GUI, database, frameworks, external services — all depend on the core. The core depends on nothing outside itself.

Because the GUI is a plugin, you can swap web-based, client-server, console, or any other UI technology. Because the database is a plugin, you can swap SQL, NoSQL, file-system, or any other storage technology. These replacements aren't trivial, but the plugin structure makes them *practical* rather than impossible.

### 8. The Plugin Argument — Asymmetric Immunity

**The dependency structure determines who can damage whom.**

Consider ReSharper (JetBrains, Russia) and Visual Studio (Microsoft, Redmond). ReSharper's source code depends on Visual Studio's source code. The ReSharper team can do nothing to disturb the Visual Studio team, but the Visual Studio team could completely disable ReSharper if they desired.

This deeply asymmetric relationship is exactly what we want in our own systems:

- **Business rules should be immune to GUI changes.** A web-page format change shouldn't break business logic.
- **Business rules should be immune to database changes.** A schema change shouldn't ripple into the core.
- **Components on one side of a boundary** change at different rates and for different reasons than components on the other side.

This is the **Single Responsibility Principle** applied at the architectural level. SRP tells us *where* to draw boundaries: wherever there is an axis of change. GUIs change at different rates than business rules. Business rules change for different reasons than dependency injection frameworks. Every axis of change deserves a boundary.

### 9. Drawing the Boundaries — The Method

**The process for drawing architectural boundaries:**

1. **Partition the system into components.** Identify which are core business rules and which are plugins — functions not directly related to the core business.
2. **Arrange the code** so dependency arrows point in one direction: **toward the core business.**
3. **Apply the Dependency Inversion Principle** and the **Stable Abstractions Principle**: dependency arrows point from lower-level details to higher-level abstractions.

The result is a plugin architecture where changes cannot propagate across firewalls. A change in a database implementation detail cannot break a business rule. A change in a GUI widget cannot corrupt a use case.

---

## Boundary Anatomy (Ch18)

### 10. Boundary Crossing — Managing Source Code Dependencies

**At runtime, a boundary crossing is just a function call with data. The trick is managing the *source code dependencies* — because when one module changes, others may need recompilation and redeployment.**

There are two fundamental patterns for boundary crossing:

**Pattern A: Same-direction crossing (low-level → high-level).** The flow of control crosses from a low-level client to a high-level service. Both runtime and compile-time dependencies point toward the higher-level component. The data structure is defined on the *called* side. Simple function call — no inversion needed.

**Pattern B: Against-the-flow crossing (high-level → low-level).** A high-level client needs to invoke a low-level service. Dynamic polymorphism inverts the compile-time dependency against the flow of control. The high-level `Client` calls `f()` on a `Service` interface; the low-level `ServiceImpl` implements that interface. All dependencies cross from right to left — toward the higher-level component. The data structure is defined on the *calling* side.

This is the same Dependency Inversion Principle from SOLID, scaled up to the architectural level.

### 11. The Dreaded Monolith — Source-Level Boundaries

**The simplest boundary has no physical representation — just disciplined segregation of functions and data within a single process, single address space, single executable.**

This is the *source-level decoupling mode*. The deployment is one file: a statically linked C/C++ executable, a Java jar, a .NET EXE. But the boundaries are still real and meaningful — independent development and marshaling of components for final assembly is immensely valuable.

Monoliths depend on **dynamic polymorphism** (or equivalent) to manage internal dependencies. Without it, architects fall back on function pointers, which most consider too risky, and are forced to abandon component partitioning.

Communication across monolith boundaries is extremely fast and cheap — just function calls. Boundaries can be very chatty. Components are typically delivered as source code and compiled/linked together at deployment time.

### 12. Deployment Components — Dynamically Linked Boundaries

**The simplest physical boundary: a dynamically linked library — .NET DLL, Java jar, Ruby Gem, Unix shared library.**

This is the *deployment-level decoupling mode*. Components are delivered in binary (or equivalent deployable form) rather than as source. Deployment is simply gathering these units together — no compilation step.

Otherwise, deployment components are the same as monoliths: same processor, same address space, same dependency management strategies. Communications are still just function calls, with a possible one-time hit for dynamic linking or runtime loading. Boundaries can remain chatty.

### 13. Threads — Not Boundaries

**Threads are not architectural boundaries or units of deployment.** They are a way to organize the schedule and order of execution. A thread may be wholly contained within a component or spread across many components. Threads do not define architectural separation; they define concurrency.

### 14. Local Processes — Stronger Physical Boundaries

**A local process is a much stronger physical boundary: separate address spaces, memory protection, operating system communication (sockets, message queues, mailboxes).**

Local processes run in the same processor or multicore but in isolated address spaces. Each process may be a statically linked monolith or composed of dynamically linked deployment components. Think of a local process as an *uber-component* — lower-level components within it still manage their dependencies through dynamic polymorphism.

**Same rules apply:** Source code dependencies point toward the higher-level component. The higher-level process's source code must not contain names, physical addresses, or registry keys of lower-level processes. Lower-level processes are plugins to higher-level processes.

**Communication cost:** Operating system calls, data marshaling/de-marshaling, interprocess context switches — moderately expensive. Chattiness should be carefully limited.

### 15. Services — The Strongest Boundary

**The strongest boundary: a service. Services communicate over the network and do not depend on physical location.**

Two communicating services may or may not operate on the same physical processor. They assume all communication crosses a network. Each service is a process, typically started from the command line.

**Same rules apply:** Lower-level services plug into higher-level services. Higher-level service source code must not contain specific physical knowledge (URIs, addresses) of any lower-level service.

**Communication cost:** Turnaround times from tens of milliseconds to seconds — very slow compared to function calls. Chattiness must be avoided. Communications must handle high levels of latency.

### 16. The Boundary Spectrum — Choosing the Right Level

**Most systems use more than one boundary strategy. A service is often a facade for interacting local processes; a local process is either a monolith or composed of deployment components.**

| Boundary Type | Coupling | Communication Cost | Chattiness |
|---|---|---|---|
| **Monolith** (source-level) | Tightest | Function calls — negligible | Can be very chatty |
| **Deployment Components** | Tight | Function calls — negligible + one-time link cost | Can be chatty |
| **Local Processes** | Moderate | OS calls, marshaling, context switches — moderate | Limit chattiness |
| **Services** | Loosest | Network calls — tens of ms to seconds | Avoid chatting |

The boundaries in a real system are typically a mixture: local chatty boundaries for internal component communication, and higher-latency boundaries at the service level for external integration points.

---

## Summary Checklist

- [ ] Are boundaries drawn between business rules and I/O (GUI, database, frameworks)?
- [ ] Do dependency arrows always point from details toward the core business rules?
- [ ] Is the database treated as a plugin behind an interface — unknown to the business rules?
- [ ] Is the GUI treated as a plugin — replaceable without affecting the business rules?
- [ ] Are premature decisions (framework, database vendor, server topology) deferred as long as possible?
- [ ] Does each boundary crossing use dependency inversion when the flow of control goes from high-level to low-level?
- [ ] Are boundary implementations appropriate for the coupling level needed (monolith vs. local process vs. service)?
- [ ] Are chatty boundaries limited to monolith and deployment-component levels where communication is cheap?
- [ ] Do service-level boundaries avoid chattiness and account for high latency?
- [ ] Does the source code of higher-level components contain no knowledge (names, addresses, URIs) of lower-level components?
- [ ] Are boundaries placed wherever there is an axis of change (SRP at the architectural level)?
- [ ] Would a new database, new GUI, or new framework require rewriting business rules? (If yes: boundaries are wrong.)

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[SOLID Design Principles]]
- [[Architectural Independence]]
- [[Main Component and Services]]
- [[Presenters and Humble Objects]]
- [[Policy and Business Rules]]
- [[Component Cohesion]] — How components are grouped determines where boundaries fall
- [[Layers and Boundaries]] — Boundaries compose into layered architectures
- [[Details - Database, Web, Frameworks]] — These are the plugins; boundaries protect the core from them
- [[What Is Architecture]] — Boundaries are the primary tool of the architect
