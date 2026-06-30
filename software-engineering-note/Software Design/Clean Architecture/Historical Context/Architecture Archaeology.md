---
tags:
- clean-architecture
- software-design
- software-engineering
---

# Architecture Archaeology

> *Source: Clean Architecture by Robert C. Martin, Appendix A (pp. 242–274)*

---

## Core Principle

> **Good architecture is not discovered in theory — it is discovered through pain. Every lesson in this journey was paid for with a failure: a modem that couldn't be replaced, a database that couldn't be extracted, a fork that couldn't be merged, a 3000-line function that became a monument to chaos. These scars teach what no textbook can: isolate what changes, invert dependencies toward policy, and never let a detail poison the core.**

A 45-year autobiographical journey through 13 major projects, from bare-metal assembler on machines without operating systems to layered C++ frameworks and micro-service architectures. Each project illustrates one or more architectural insights earned the hard way. The same principles — boundaries, dependency inversion, isolation of details — recur across radically different technologies and decades.

---

## The Journey

### 1. Union Accounting System (1971) — Assembler boundaries on bare metal

The Datanet-30 had no operating system, no file system, no high-level language — just an assembler and 16K of core. The replacement Varian 620/f (32K) introduced a preemptive supervisor with overlay swapping.

**Two clean boundaries emerged from raw necessity:**

- **Character output boundary (dependency-normal):** Applications passed strings to the supervisor; the supervisor managed terminal buffers, 30-cps output, and memory swapping. Applications had zero knowledge of the output device. Dependencies pointed with the flow of control.
- **Supervisor-to-application boundary (dependency-inverted):** Every application started by jumping to the **exact same memory address** in the overlay area. The supervisor had no compile-time dependency on any application — only knowledge of a starting point. This was polymorphic dispatch before polymorphism had a name.

> **Insight:** Clean architectural boundaries are possible even in assembler on a machine with no OS. The mechanism doesn't matter — the direction of dependencies matters.

---

### 2. Laser Trim System (1973) — The cost of soft boundaries

A monolithic M365 assembler program with three nominal layers (MOP operating kernel, utility layer for hardware control, isolation layer with a domain-specific language) — but boundaries were unenforced. The MOP called back into the utility layer. Couplings were everywhere. The DSL provided a "simpler" interface but was deeply coupled to the hardware below.

> **Insight:** Layers without enforced boundaries are not layers. Naming something a "layer" or a "DSL" doesn't create isolation — dependency direction and compile-time enforcement do. This was typical of early 1970s software, but the pain is still relevant today.

---

### 3. Aluminum Die-Cast Monitoring (1975) — Concurrency before threads

An interrupt-driven real-time assembler system on an IBM System/7. The machine had a `Set Program Interrupt (SPI)` instruction that allowed a running task to yield the processor so lower-priority interrupts could be serviced. Martin notes: "Nowadays, in Java we call this `Thread.yield()`."

> **Insight:** Concurrency primitives predate modern languages by decades. The concepts — yielding, priority levels, interrupt handling — are timeless; only the syntax changes.

---

### 4. 4-TEL Telephone Testing System (1976–1988) — A masterclass in lessons learned

The longest-running project in the journey. Four critical architectural lessons:

#### 4.1 The SAC/COLT Split — Separate what changes at different rates

Originally, COLTs (Central Office Line Testers) did everything: dialing, measuring, analysis, UI. Dial-up connections at 30 cps made testing painfully slow. The solution: **separate dial/measure (COLT) from analyze/report (SAC)**. A simple DSL of short command packets ("DIAL XXXX", "MEASURE") crossed the boundary. Result: faster terminals, smaller COLT memory footprint, independently deployable components.

> **Insight:** When parts of a system change at different rates, separate them with a clean boundary and a minimal protocol. This is the essence of the Single Responsibility Principle at the architectural level.

#### 4.2 EPROM Vectorization — Plugin architecture and polymorphic dispatch, invented from necessity

The COLT firmware was burned onto 30 EPROM chips (one 30K binary, divided into 1K segments). **Every code change required replacing all 30 chips** — a field-service nightmare.

The solution ("Vectorization"):
1. Split the 30K program into 32 independently compilable source files, each <1K
2. At the start of each file, placed a fixed-size table (40 bytes) containing addresses of all subroutines on that chip
3. Created a RAM "vectors" area holding copies of all 32 tables
4. Changed every subroutine call to an **indirect call through the RAM vector**
5. On boot, scanned each chip and loaded its vector table into RAM

Result: **Independently deployable chips.** A bug fix required replacing only 1–2 chips instead of all 30. Features could be hot-plugged into open chip sockets with automatic menu registration and binding. Remote firmware patching became possible by dialing in and overwriting a RAM vector to point to hand-entered hex machine code.

> **Insight:** This *is* polymorphic dispatch, dependency inversion, and a plugin architecture — built in 1978 assembler on an 8085, years before OO terminology existed. The principles are technology-agnostic. A stable abstract interface (the vector table) decoupled callers from implementations.

#### 4.3 The Dispatch Determination Module — The cost of unreadable code

A brilliant but uncommunicative developer wrote the fault-dispatch logic: "three weeks of staring at the ceiling and two days of code pouring out of every orifice — after which he quit." Nobody understood it. Every modification broke it. Management eventually ordered it **locked down and never modified** — officially *rigid* code.

> **Insight:** Code that cannot be understood cannot be maintained. Clean code is an economic imperative, not an aesthetic preference. When code becomes rigid, it strangles the business value it was built to deliver.

#### 4.4 The Modem Fiasco — The price of smeared concerns

Modem control code was scattered across the entire 60,000-line assembler codebase — no module, no abstraction. When the hardware team designed a new modem with an entirely different control structure (despite explicit pleas to match the old interface), the team had to retrofit a translation layer into the serial bus write subroutine. It had to interpret command sequences at the bit level and translate between entirely different IO addresses, timings, and bit positions.

> **Insight:** Isolate hardware from business rules. Abstract interfaces. When a detail (like a modem) is smeared across the codebase, replacing it becomes a nightmare. This failure directly motivated the Dependency Inversion Principle.

---

### 5. The Grand Redesign Failure (1982–1988) — Why rewrites die

The company launched a "Tiger Team" to rewrite the entire SAC in C and UNIX on new 80286 hardware. The first attempt burned 2–3 man-years with zero deliverables. The second attempt took years and may never have deployed.

Concurrently, a European expansion required forking the codebase for the UK market. After years of divergence, three separate attempts to reintegrate the US and UK forks all failed — the codebases were "too different to reintegrate."

> **Insight:** A rewrite team can almost never catch up to a large team actively maintaining and extending the old system. The old system is a moving target. Forks diverge irreversibly when not continuously integrated. Architecture that permits isolated modification (plugins, clean boundaries) prevents the fork problem entirely.

---

### 6. DLU/DRU (Early 1980s) — Radically different architectures can both succeed

Two developers built the two halves of a remote terminal system independently:

- **DLU (Dataflow/Pipes-and-Filters):** Each task did one small focused job, passed output to the next via queues. Assembly-line model — split, merge, flow.
- **DRU (Monolithic per-terminal):** One task per terminal doing everything. Expert-builder model — identical large tasks, each managing its own terminal.

Both worked well. Both were maintainable.

> **Insight:** Software architectures can be wildly different yet equally effective. There is no single "right" architecture. What matters is that the architecture is appropriate for the problem, the team, and the constraints. Dogma about architectural patterns is misplaced.

---

### 7. VRS — Voice Response System (Mid-1980s) — The database is a detail

Embedded SQL was new and exciting. SQL commands and UNIFY-specific API calls were "smeared throughout the body of that code." Years later, UNIFY was cancelled. The team spent three months trying to extract UNIFY and replace it with a new vendor — then gave up. They had to hire a third party to maintain UNIFY indefinitely at ever-increasing cost.

> **Insight:** Databases are details that must be isolated from business logic. Strong coupling to third-party software creates irreversible technical debt. This experience directly shaped Martin's position that the database is a plugin, not the center of the architecture.

---

### 8. Electronic Receptionist (ER, 1983) — Service-oriented architecture before the term existed

The first voice mail system ever built. Architecture: each telephone line monitored by a listener process; incoming calls passed to handler processes managing state transitions. Messages passed between services via disk files. Each service determined the next service, wrote state to a file, launched the next service via command line, then exited.

> **Insight:** The architecture "would today be called service-oriented." Services were independently deployable, lived within their own domain of responsibility, and dependencies ran toward higher-level policy. True boundaries don't require modern frameworks — they require disciplined dependency management.

---

### 9. Craft Dispatch System (CDS, 1985) — Micro-services in 1985

An aggressive evolution of ER's service-oriented approach. Key architectural innovations:

- **Externalized state machine:** The finite state machine for trouble ticket handling lived in a text file. Every event triggered a state transition; the current process started the next process dictated by the state machine, then exited or waited. **Changing application flow required zero code changes** — edit the text file. Hot-swapping was possible while the system was running.
- **3DBB shared memory:** A named-data blackboard for inter-process communication (disk files were too slow for rapid service flip-flopping). Strings and constants passed by name across memory partitions.
- **FLD (Field Labeled Data):** A recursive hierarchical data format — binary trees associating names with data, serializable to/from strings for 3DBB transit. "Nowadays we would call this XML or JSON."

> **Insight:** "There is nothing new under the Sun." Micro-services, externalized configuration, hot-swapping, BPEL, XML/JSON-like data interchange, a shared-memory blackboard — all invented independently in 1985 to solve real problems. The Open-Closed Principle was applied at the architectural level: the system was open for extension (new services, new flows) but closed for modification (no code changes needed).

---

### 10. Clear Communications (1988–1991) — Chaos as cautionary tale

A startup with "no time for architecture." The result: a 3000-line C function (`gi()` — Graphic Interpreter), a full seven-layer ISO stack written from scratch, code "slammed here, shoved there." After three years of furious coding, the product failed to sell.

But this period also produced: immersion in C++ and OO, voracious reading (Booch, Stroustrup, Wirfs-Brock, Coplien), and two years of Usenet debates that laid "the foundations of the SOLID principles." The connection to Grady Booch through Netnews led to joining Rational.

> **Insight:** No architecture → chaos → failure. But the counterpoint: the intellectual capital built during this period (OO design principles, SOLID foundations, network of relationships) outlasted the failed product by decades.

---

### 11. ROSE at Rational (1990–1991) — When great architecture still fails

ROSE had a real architecture: true layers, properly controlled dependencies, releasable and independently deployable components. Three critical mistakes:

1. **Dependency direction was wrong.** Dependencies pointed with the flow of control — GUI → representation → manipulation rules → database. They should have pointed toward high-level policy, not toward the database. "It was this failure to direct our dependencies toward policy that aided the eventual demise of the product."
2. **Object-oriented database.** Chose an OO database for its "magic" (objects appear in RAM on access). Got a "big, slow, intrusive, expensive third-party framework that made our lives hell."
3. **Over-architecture.** Too many layers, each with communication overhead. "Significantly reduced the productivity of the team." The entire tool was eventually scrapped and replaced by a small team with a simple desktop application.

> **Insight:** Good architecture alone doesn't guarantee success. Architecture must be flexible enough to adapt to the size of the problem. Architecting for the enterprise when all you need is a desktop tool is a recipe for failure. The dependency rule from this book — point dependencies toward high-level policy, not toward details like databases — was born from this specific failure.

---

### 12. Architects Registry Exam (Early 1990s) — Frameworks require multiple consumers to be reusable

36 applications (18 GUI vignettes + 18 scoring vignettes) with shared gestures and mathematical techniques. Attempted to build a reusable framework from the first application (Vignette Grande). After one year: 45,000 lines of framework code, 6,000 lines of application code. The framework didn't fit the next applications.

**Second attempt:** Built four vignettes simultaneously, borrowing ideas from the old framework but reworking them to fit all four without modification. Another year, another 45,000 lines, but this time the framework was truly reusable. The remaining applications "started popping out every few weeks."

Architecturally: vignettes were plugins to the framework. GUI policy lived in the framework; scoring policy lived in the vignette (with the scoring framework plugged into it). Dependencies followed the Dependency Rule even though the term "plugin" wasn't used.

> **Insight:** You cannot make a reusable framework until you first make a usable framework. Reusable frameworks require building them in concert with several reusing applications. A framework built from a single use case will be coupled to that use case. Generalization requires multiple concrete examples.

---

## Lessons Learned

### 1. Boundaries are technology-agnostic

Clean architectural boundaries were implemented in 1971 assembler (overlay jumping to a fixed address with zero compile-time dependency), in 1978 EPROM vector tables (polymorphic dispatch before OO), and in 1985 externalized state machines (Open-Closed Principle at the architectural level). The mechanism doesn't matter — the discipline of dependency direction matters.

### 2. Dependency Inversion is the single most important architectural principle

- The Union Accounting System supervisor inverting its dependency on applications (1971)
- EPROM vector tables decoupling callers from implementations (1978)
- ROSE's failure when dependencies pointed toward the database instead of toward policy (1990)
- The NCARB framework with vignettes as plugins (1992)

Every success story involved dependencies pointing in the right direction. Every failure story involved dependencies pointing toward details.

### 3. Isolate what changes

The modem fiasco (hardware control smeared everywhere), the VRS database disaster (SQL smeared everywhere), and the European fork failure (divergent codebases that couldn't be merged) all share one root cause: **details that changed were not isolated from the rest of the system.** The Stable Dependencies Principle and the Common Closure Principle are not abstract theory — they are survival mechanisms.

### 4. Third-party coupling is a one-way door

Once UNIFY's embedded SQL was smeared through the VRS codebase, extraction was economically impossible. Once the OO database was baked into ROSE's architecture, it became a permanent drag. Third-party frameworks should be treated as plugins — integrated through abstract interfaces that you control.

### 5. Good code is an economic imperative

The Dispatch Determination module became "officially rigid" — unmodifiable, untouchable, strangling business value. The 3000-line `gi()` function at Clear Communications was a productivity killer. Code that cannot be read cannot be maintained. Cleanliness is not aesthetics; it's economics.

### 6. Architecture must fit the size of the problem

ROSE was over-architected for what should have been a desktop tool. The pCCU was drastically simplified when the real constraints were understood (one week vs. projected man-years). Don't architect for the enterprise when you're building a utility. Don't build a framework for one consumer.

### 7. Rewrites usually fail — evolve instead

The Tiger Team's multi-year rewrite never caught the moving target of the actively-maintained system. The European fork diverged irrecoverably. Architecture that supports incremental evolution (clean boundaries, plugins, isolated concerns) beats big-bang rewrites every time.

### 8. Multiple implementations validate abstraction

The NCARB framework only became reusable when built against four simultaneous consumers. A single consumer produces a coupled framework; multiple consumers force genuine abstraction. This applies to interfaces, frameworks, and architectural boundaries alike.

### 9. Different architectures can solve the same problem equally well

The DLU (dataflow/pipes-and-filters) and DRU (monolithic per-terminal) were architectural opposites — both succeeded. Architectural patterns are tools, not religions.

### 10. Web-scale patterns predate the web

Micro-services (CDS, 1985), XML/JSON-like data interchange (FLD, 1985), hot-swapping configuration (externalized state machine, 1985), service-oriented architecture (ER, 1983), polymorphic plugin architectures (EPROM vectors, 1978), and dependency inversion (Datanet-30 overlay, 1971) were all invented decades before they acquired modern names. The principles are timeless; only the tools change.

---

## Summary Checklist

- [ ] Separate components that change at different rates with clean, minimal interfaces
- [ ] Dependencies must point toward high-level policy, not toward details (databases, hardware, frameworks)
- [ ] Isolate third-party frameworks behind interfaces you control — never smear vendor-specific code through the system
- [ ] Clean code is an economic requirement, not an aesthetic preference — unreadable code becomes rigid code
- [ ] Size the architecture to the problem — over-architecture kills productivity as surely as no architecture
- [ ] Prefer incremental evolution over big-bang rewrites — the old system is always a moving target
- [ ] Build reusable frameworks only after validating against multiple concrete use cases
- [ ] The core architectural principles (boundaries, dependency inversion, isolation of change) are technology-agnostic and timeless
- [ ] Multiple valid architectures can solve the same problem — choose based on team, constraints, and context, not dogma
- [ ] Every new pattern you discover was probably invented decades ago by someone solving a real problem under real constraints

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[What Is Architecture]]
- [[SOLID Design Principles]]
- [[Component Cohesion]]
- [[Component Coupling]]
- [[Programming Paradigms]]
