# Details - Database, Web, Frameworks

> *Source: Clean Architecture by Robert C. Martin, Chapters 30–32 (pp. 209–219)*

---

## Core Principle

> **The database, the web, and frameworks are all implementation details in the outermost architectural circle. None of them rises to the level of an architectural element. The data model matters—the database does not. The use cases matter—the delivery mechanism does not. Your business rules matter—the framework does not.**

The architecture of a software system should be driven by use cases and business rules, not by storage technologies, delivery mechanisms, or third-party frameworks. Each of these three concerns belongs behind a boundary, treated as a plugin that can be swapped without touching the core. Defer decisions about databases, web frameworks, and application frameworks until the use-case architecture is solid.

---

## The Rules / Key Concepts

### 1. The Database Is an I/O Device

The database is a piece of software—a utility that provides access to data. It is not the data model. The structure you give to data within your application (the data model) is architecturally significant; the technology that moves data on and off a disk is not. Relational databases are an excellent storage technology, but arranging data into rows and tables is still just a low-level mechanism. Passing database rows and tables around the system as objects is an architectural error—it couples use cases, business rules, and even the UI to the relational structure of the data.

### 2. Data Model ≠ Data Access

Knowledge of tabular structures, SQL queries, and database schema should be restricted to the lowest-level utility functions in the outer circles of the architecture. The use cases of your application should neither know nor care how data is stored. In RAM, programmers reorganize data into linked lists, trees, hash tables, stacks, and queues—not tables. The database is nothing more than a bucket of bits for long-term storage; the form it takes on disk is irrelevant to the architecture.

### 3. Why RDBMS Dominated: Disks Are Slow

The dominance of Oracle, MySQL, and SQL Server came from one fact: rotating magnetic disks are slow. Disk access takes milliseconds—a million times slower than processor cycle times. To mitigate this, we built indexes, caches, optimized query schemes, and entire data management systems. File systems (document-based, good for storing/retrieving files by name) and RDBMS (content-based, good for finding records by content) are both products of disk slowness. When disks disappear and all data lives in RAM, the need for relational tables and SQL evaporates.

### 4. Performance Is an Encapsulated Concern

Data storage performance can be entirely encapsulated and separated from business rules. Getting data in and out of the data store quickly is a low-level concern addressed by data access mechanisms—it has nothing to do with the overall architecture. A good architect does not allow low-level mechanisms to pollute the system architecture.

### 5. The Web Is an I/O Device

The web is a GUI. The GUI is a detail. Therefore, the web is a detail. The computing industry has been oscillating between centralized and distributed power since the 1960s—mainframes with dumb terminals, client-server, web browsers with server farms, AJAX/JavaScript heavy clients, Node.js pulling logic back to servers. The web changed nothing; it was simply one more swing of the pendulum. As an architect, you must look at the long term and push these oscillations away from your core business rules.

### 6. The Pendulum of UI Architecture

The endless back-and-forth—fat clients, thin clients, browser apps, server-rendered pages—is a short-term issue. Your architecture should survive all of them because it doesn't care about the delivery mechanism. Company Q built a popular desktop finance app, then a "marketing genius" made it look like a browser; users hated it, and they reverted. Had the architects decoupled business rules from the UI, the whole ordeal would have been a trivial skin swap. Never let a marketing decision force you to rewrite your core.

### 7. Abstracting the Use Case from the UI

The chatty interaction between a GUI and an application is hard to abstract completely—the dance between a browser and a web app differs from that of a desktop GUI. But use cases can be abstracted: the complete input data and resultant output data can be placed into data structures and used as inputs and outputs for a use case process. This treats the UI as an I/O device in a device-independent manner. The boundary between input completion → use case execution → output delivery is where the abstraction lives.

### 8. Frameworks Are Details, Not Architectures

Frameworks are powerful and useful, but they are not architectures—though some try to be. Framework authors write frameworks to solve their own problems, not yours. There may be overlap, which is why frameworks are popular, but the author has no commitment to you. The architecture decisions belong to you, not to the framework.

### 9. The Asymmetric Marriage

When you adopt a framework, you make a huge commitment—you wrap your architecture around it, derive from its base classes, and couple your business objects to its facilities. The framework author makes no corresponding commitment to you. They have absolute control over their framework; coupling to it is no risk for them. But once you are coupled, breaking away is extremely difficult. The framework author urges tight coupling because nothing is more validating than users inextricably deriving from their base classes. This is a one-directional marriage: you take all the risk and burden; the author takes none.

### 10. The Risks of Framework Takeover

Frameworks tend to violate the Dependency Rule—they ask you to inherit their code into your Entities, coupling themselves into the innermost circle. Once in, that framework is not coming back out. Additional risks: the framework may help with early features but be outgrown as your product matures; the framework may evolve in directions that don't help you, deprecating features you rely on; a better framework may emerge that you cannot switch to because you are locked in.

### 11. Treat Frameworks as Plugins Behind Interfaces

The solution: don't marry the framework. Use it, but don't couple to it. Keep it at arm's length in the outer circles. If the framework wants you to derive business objects from its base classes, say no—derive proxies instead and keep those proxies in plugin components. Don't sprinkle framework annotations throughout business objects; limit framework knowledge to the Main component (the dirtiest, lowest-level component where wiring belongs). For example, use Spring to auto-wire dependencies in Main, but never annotate business objects with `@autowired`.

### 12. Conscious Commitment When Marriage Is Unavoidable

Some frameworks you must marry—STL in C++, the standard library in Java. This is normal, but it must still be a decision. Understand that when you marry a framework, you are stuck with it for the entire lifecycle of the application: for better or worse, for richer or poorer, in sickness and in health. This is not a commitment to be entered into lightly. Date the framework first. Keep it behind an architectural boundary for as long as possible. Get the milk without buying the cow if you can.

---

## Summary Checklist

- [ ] Data model is architecturally significant; the database is a detail—treat it as an I/O device behind an abstraction
- [ ] Never pass database rows, tables, or ORM objects through your business logic—keep knowledge of storage format in the outermost circles
- [ ] Defer the choice of database technology until use cases and business rules are solid
- [ ] Encapsulate data storage performance concerns in low-level data access mechanisms, not in the architecture
- [ ] The web is a GUI, and the GUI is a detail—architecture should not care about the delivery mechanism
- [ ] Decouple business rules from the UI so that pendulum swings (thin client, fat client, browser, mobile) don't force rewrites
- [ ] Abstract use cases behind input/output data structures so the UI becomes a device-independent I/O channel
- [ ] Frameworks are not architectures; never let a framework dictate your system's architectural shape
- [ ] Recognize the asymmetric marriage: framework authors take no risk, you take all of it
- [ ] Keep frameworks in the outer circles—derive proxies, not business objects, from framework base classes
- [ ] Limit framework-specific annotations and imports to the Main/wiring component
- [ ] When you must marry a framework (stdlib, STL), do it consciously and understand the lifetime commitment
- [ ] Date before you marry: keep frameworks behind architectural boundaries as long as possible

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[Screaming Architecture]]
- [[Policy and Business Rules]]
- [[Presenters and Humble Objects]]
- [[Main Component and Services]]
- [[Boundaries]]
