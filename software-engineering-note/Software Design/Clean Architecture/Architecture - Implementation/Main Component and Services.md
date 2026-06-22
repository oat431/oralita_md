# Main Component and Services

> *Source: Clean Architecture by Robert C. Martin, Chapters 26–27 (pp. 181–191)*

---

## Core Principle

> **Main is the ultimate detail — the dirtiest component in the outermost circle. Services are not architectures; architectural boundaries run through components, not between services.**

Main is the entry point that wires everything together, injects dependencies, and hands control to high-level policy. Services are just function calls across process boundaries — useful, but not architecturally significant in themselves. Cross-cutting concerns can only be managed by applying SOLID principles and the Dependency Rule to the components inside services.

---

## The Rules / Key Concepts

### 1. Main Is the Ultimate Detail

Main is the lowest-level policy in the system. It is the initial entry point, and nothing (except the operating system) depends on it. Its sole job is to create all factories, strategies, and global facilities, then hand control over to the high-level abstract portions of the system. **Main is the dirtiest of all the dirty components** — and that's by design.

### 2. Dependency Injection Belongs in Main

Dependencies should be injected by a DI framework into Main. Once Main has them, it should distribute those dependencies normally — without using the framework elsewhere. The framework stays contained in the outermost circle where it belongs.

### 3. Main Is a Plugin

Think of Main as a plugin to the application — one that sets up initial conditions, gathers outside resources, and hands control to the high-level policy. Since it's a plugin, you can have **many Main components**: one for Dev, one for Test, one for Production, and even one per country, jurisdiction, or customer. When Main sits behind an architectural boundary, configuration becomes straightforward.

### 4. Services Do Not Define Architecture

Using services is not, by itself, an architecture. Architecture is defined by **boundaries that separate high-level policy from low-level detail and follow the Dependency Rule**. Services that merely separate application behaviors are little more than expensive function calls. Some services are architecturally significant; most are not. The label "service-oriented architecture" is misleading.

### 5. The Decoupling Fallacy

Services appear strongly decoupled because they run in separate processes and can't access each other's variables. This is only partially true. Services remain **coupled through shared resources** (processors, networks) and, more critically, through **shared data**. If a field is added to a data record passed between services, every service operating on that field must change. Service interfaces, meanwhile, are no more rigorous or well-defined than function interfaces.

### 6. The Fallacy of Independent Development and Deployment

The belief that each service can be independently developed, deployed, and operated by a dedicated team is also only partially true. Large enterprise systems can be built from monoliths and component-based systems too — services are not the only path to scalability. More importantly, to the extent that services are coupled by shared data or behavior, their development and deployment **must be coordinated**.

### 7. The Kitty Problem — Cross-Cutting Concerns Expose the Weakness

Imagine a taxi aggregator built from micro-services: TaxiUI, TaxiFinder, TaxiSelector, and TaxiDispatcher, each owned by a separate team. Now marketing wants a kitten delivery feature — selecting nearby taxis to pick up kittens and deliver them, with rules for allergic drivers and customers. The question: **how many services must change? All of them.** Every service touches taxi selection and dispatch logic. The feature cannot be developed or deployed independently. This is the problem with cross-cutting concerns: functional decomposition by service makes every new cross-cutting feature a coordinated nightmare.

### 8. Objects Solve Cross-Cutting Concerns with Polymorphism

In a component-based architecture, SOLID principles prompt you to create classes that can be **polymorphically extended**. The original logic stays in base classes; ride-specific logic extracts into a `Rides` component; kitten logic goes into a `Kittens` component. Both override the base classes using Template Method or Strategy. Only the **UI must change** when adding the Kitty feature — everything else is a new JAR or DLL, dynamically loaded at runtime, conforming to the Open-Closed Principle.

### 9. Services Need Internal Component Architecture

Services don't need to be little monoliths. Apply SOLID principles **inside each service**: define abstract classes in core JAR files, and put feature extensions in separate JAR files that extend those abstractions. Deploying a new feature becomes a matter of adding JAR files to the load path — not redeploying the entire service. The services still exist, but each has its own internal component design.

### 10. Architectural Boundaries Run Through Services, Not Between Them

The critical insight: architectural boundaries **do not fall between services**. They run through services, dividing them into components. The components within services define the architectural boundaries — not the services themselves. A service might contain a single component fully surrounded by a boundary, or multiple components separated by boundaries.

---

## Summary Checklist

- [ ] Place Main in the outermost circle — treat it as the dirtiest low-level detail
- [ ] Confine dependency injection frameworks to Main; distribute dependencies normally elsewhere
- [ ] Design Main as a replaceable plugin (Dev, Test, Production, per-customer)
- [ ] Do not confuse services with architecture — architecture is boundaries, not process/platform boundaries
- [ ] Recognize the decoupling fallacy: services are coupled through shared data and behavior
- [ ] Anticipate cross-cutting concerns — they will force coordinated changes across all services
- [ ] Apply SOLID principles and polymorphism inside services to handle cross-cutting features
- [ ] Design services with internal component architectures that follow the Dependency Rule
- [ ] Use the Open-Closed Principle: add new features as dynamically loaded components, not service rewrites
- [ ] Draw architectural boundaries through services via components, not between services

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[Boundaries]]
- [[Architectural Independence]]
- [[Layers and Boundaries]]
- [[Details - Database, Web, Frameworks]]
- [[Presenters and Humble Objects]]
