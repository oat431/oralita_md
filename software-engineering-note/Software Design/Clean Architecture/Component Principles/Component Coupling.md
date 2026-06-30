---
tags:
- clean-architecture
- software-design
- software-engineering
---

# Component Coupling

> *Source: Clean Architecture by Robert C. Martin, Chapter 14 (pp. 98–116)*

---

## Core Principle

> **Dependencies between components must be managed as a directed acyclic graph where arrows point from unstable, concrete components toward stable, abstract components. Any cycle in this graph creates a monolithic blob that reintroduces integration hell.**

Component coupling is the sibling of component cohesion. While the three cohesion principles (REP, CCP, CRP) govern *what classes belong together inside* a component, the three coupling principles (ADP, SDP, SAP) govern the *relationships between* components. The forces at play are technical, political, and volatile—the component dependency structure is not a top-down functional decomposition but a map of buildability and maintainability that jitters and grows with the system.

---

## The Principles

### 1. ADP: Acyclic Dependencies Principle

**Allow no cycles in the component dependency graph.** If there are cycles, every component in the cycle becomes one de facto monolith—all developers on any of those components experience the "morning after syndrome" again, because they must all use exactly the same release of one another's code. There is no way to isolate, unit-test, or release any single component independently.

**The "Morning After Syndrome."** You work all day, get your code working, go home, and arrive the next morning to find it broken. Someone stayed later and changed something you depend on. In small teams this is manageable. As the project grows, weeks can pass without a stable build—everyone keeps changing their code to catch up with everyone else's changes.

**The Weekly Build.** A historical mitigation: developers isolate for four days, then integrate everything on Friday. The integration penalty grows with project size until it overflows into Saturday, then Thursday, then the entire week. Lengthening the build cycle to biweekly buys time but increases project risk—integration and testing get harder, and rapid feedback is lost.

**The Real Solution: Releasable Components.** Partition the system into components that are the responsibility of a single developer or team. When a component is working, it gets a release number and is placed in a shared directory. Other teams decide *when* to adopt the new release. No team is at the mercy of any other. Integration happens in small, incremental steps rather than at a single catastrophic point.

**The Dependency Graph as a DAG.** For this to work, the component dependency structure must be a Directed Acyclic Graph (DAG). In a DAG, regardless of which component you start at, you can never follow dependency arrows around a cycle back to where you began. When the team working on *Presenters* releases, you follow arrows backward to find who is affected (*View* and *Main*). When *Main* releases, nothing else is affected—its impact is small. System-wide releases proceed bottom-up in a clear, predictable order: *Entities* first, then *Database* and *Interactors*, then *Presenters*, *View*, *Controllers*, *Authorizer*, and *Main* last.

**What a Cycle Does.** If *Entities* depends on *Authorizer* (creating a cycle through *Interactors* → *Authorizer* → *Entities*), then *Entities*, *Authorizer*, and *Interactors* become one large component. Testing *Entities* now requires building and integrating *Authorizer* and *Interactors*. You suddenly need "so many different libraries and so much of everybody else's stuff just to run a simple unit test." Build issues grow geometrically, and in languages like Java that read declarations from compiled binary files, there may be no correct build order at all.

**Breaking Cycles.** Two mechanisms:
1. **Apply the Dependency Inversion Principle (DIP).** Create an interface with the needed methods, put it in the depended-on component (*Entities*), and implement it in the dependent component (*Authorizer*). This inverts the arrow.
2. **Create a new component.** Move the classes that both components depend on into a shared new component that both now point to.

**The "Jitters" and Top-Down Design.** The component structure is volatile in the presence of changing requirements—it jitters and grows. It *cannot* be designed top-down at the start of a project. There is no software to build or maintain yet, so there is no need for a build-and-maintenance map. The structure evolves as modules accumulate: first SRP and CCP drive class collocation, then CRP drives reusable elements, and finally ADP breaks cycles as they appear. One overriding concern: **isolating volatility**—preventing frequently-changing components (GUIs, reports) from affecting stable high-value components (business rules, high-level policies).

---

### 2. SDP: Stable Dependencies Principle

**Depend in the direction of stability.** A component expected to be volatile must not be depended on by a component that is difficult to change—otherwise the easy-to-change component becomes hard to change through no change in its own code.

**What Stability Means.** Stability is not about frequency of change; it is about the *amount of work required to change*. A penny standing on its side is not changing, but it is unstable because it takes almost no work to topple. A table is stable because turning it over requires considerable effort. A software component is made stable by having many incoming dependencies—the more components that depend on it, the more work is required to reconcile any change with all of them.

**Measuring Stability: The I Metric.**

| Metric | Definition |
|--------|------------|
| **Fan-in** | Number of classes *outside* the component that depend on classes *inside* the component (incoming dependencies) |
| **Fan-out** | Number of classes *inside* the component that depend on classes *outside* the component (outgoing dependencies) |
| **I (Instability)** | `I = Fan-out / (Fan-in + Fan-out)` — range [0, 1] |

- **I = 0** → Maximally stable. No outgoing dependencies (independent); many incoming dependencies (responsible).
- **I = 1** → Maximally unstable. No incoming dependencies (irresponsible); many outgoing dependencies (dependent).

**The Stable Dependencies Principle.** A component's I metric should be *larger* than the I metrics of the components it depends on. In other words, I must *decrease* in the direction of dependency. Dependencies must flow from high-I (unstable) to low-I (stable) components.

**Not All Components Should Be Stable.** If every component were maximally stable (I = 0), the system would be unchangeable. The ideal configuration places unstable, changeable components on top and stable components at the bottom. Any arrow pointing *upward* violates the SDP (and later, ADP).

**Fixing an SDP Violation.** When a stable component (*Stable*, low I) depends on an unstable component (*Flexible*, high I), use the DIP: create an interface (`UService`) that declares what *Stable* needs, put it into a new highly-stable abstract component (I = 0), and have *Flexible* implement it. Both *Stable* and *Flexible* now depend on `UService`, and all arrows flow toward decreasing I. In statically-typed languages (Java, C#), abstract components containing nothing but interfaces are very common and necessary. In dynamically-typed languages (Ruby, Python), these abstract components and their dependencies don't exist at all—dependency structures are inherently simpler.

---

### 3. SAP: Stable Abstractions Principle

**A component should be as abstract as it is stable.** Stable components hold high-level policy that should not change often, but stability also makes them hard to change. The OCP resolves this tension: abstract classes and interfaces allow extension without modification. Therefore: stable → abstract (so it can be extended); unstable → concrete (so it can be changed directly).

Together, SDP + SAP = the DIP for components. SDP says dependencies run toward stability; SAP says stability implies abstraction. Therefore dependencies run toward abstraction. But unlike the binary class-level DIP, components can be *partially* abstract and *partially* stable—there are shades of gray.

**Measuring Abstractness: The A Metric.**

| Metric | Definition |
|--------|------------|
| **Nc** | Total number of classes in the component |
| **Na** | Number of abstract classes and interfaces in the component |
| **A (Abstractness)** | `A = Na / Nc` — range [0, 1] |

- **A = 0** → No abstract classes at all (fully concrete).
- **A = 1** → Nothing but abstract classes and interfaces (fully abstract).

**The A–I Graph and the Main Sequence.** Plot A (abstractness) on the vertical axis and I (instability) on the horizontal axis. The two "good" endpoints are:
- **(0, 1)** — Maximally stable and abstract (upper left). High-level policy belongs here.
- **(1, 0)** — Maximally unstable and concrete (lower right). Volatile, easily-changed code belongs here.

The line connecting these two endpoints is called the **Main Sequence**. Components on or near this line are appropriately abstract for their stability and appropriately stable for their abstractness.

**The Zones of Exclusion:**

| Zone | Location | Problem |
|------|----------|---------|
| **Zone of Pain** | Near (0, 0) | Highly stable *and* concrete. Rigid—cannot be extended (no abstractness) and cannot be changed (too many dependents). Examples: database schemas (volatile, concrete, highly depended-on), concrete utility libraries (like `String`—technically here but nonvolatile, so harmless). Volatility is effectively a third axis: the more volatile, the more painful. |
| **Zone of Uselessness** | Near (1, 1) | Maximally abstract *yet* has no dependents. Leftover abstract classes or interfaces that nobody implements or depends on—codebase detritus. |

**Distance from the Main Sequence: The D Metric.**

`D = |A + I − 1|` — range [0, 1]

- **D = 0** → Component sits directly on the Main Sequence (ideal).
- **D = 1** → Component is as far from the Main Sequence as possible (worst).

**Using D in Practice:**
- Calculate D for every component in the design. Any component with D not near zero should be reexamined and restructured.
- Compute mean and variance across all D values. A conforming design should have mean and variance close to zero.
- Use variance to set control limits and flag outliers (e.g., components >1 standard deviation from the mean).
- Plot D for each component over time (release-by-release) to detect creeping decay. When a component's D exceeds a control threshold (e.g., D = 0.1), investigate why it is drifting from the Main Sequence.

---

## Summary Checklist

- [ ] Are there NO dependency cycles between components (ADP)?
- [ ] Can any component be built and tested in isolation without dragging in the entire system?
- [ ] Do dependencies point from unstable to stable components (SDP)?
- [ ] For any given component, is its I metric larger than the I metrics of the components it depends on?
- [ ] Are stable components also appropriately abstract (SAP)?
- [ ] Are unstable components appropriately concrete (easily changed)?
- [ ] Are any components in the Zone of Pain (stable + concrete + volatile)?
- [ ] Are any components in the Zone of Uselessness (abstract + unstable)?
- [ ] Is the D metric (|A + I − 1|) for each component near zero?
- [ ] Are you monitoring D over time to catch components drifting away from the Main Sequence?
- [ ] Is high-level policy placed in stable, abstract components (upper-left of the Main Sequence)?
- [ ] Is volatile code (GUIs, reports, implementations) placed in unstable, concrete components (lower-right)?
- [ ] When a cycle appears, is it broken using DIP or a new shared component?
- [ ] Is the component dependency structure evolving with the system rather than being designed top-down?

---

## Related

- [[Component Cohesion]]
- [[SOLID Design Principles]]
- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[Architectural Independence]]
- [[Boundaries]]
