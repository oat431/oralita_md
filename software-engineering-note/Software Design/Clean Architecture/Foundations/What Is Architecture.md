# What Is Architecture?

> *Source: Clean Architecture by Robert C. Martin, Chapter 15 (pp. 117–124)*

---

## Core Principle

> **The primary purpose of architecture is to support the life cycle of the system — development, deployment, operation, and maintenance — by keeping as many options open as possible, for as long as possible. A good architect maximizes the number of decisions NOT made.**

Architecture is the shape of a system: the division into components, their arrangement, and how they communicate. Its goal is not to make the system work (terrible architectures can work just fine) but to minimize lifetime cost and maximize programmer productivity. The strategy is simple: separate policy from detail, then defer all decisions about details until you have enough information to make them properly.

---

## The Rules / Key Concepts

### 1. The Architect Is a Programmer

**A software architect is, and continues to be, a programmer. Never fall for the lie that architects pull back from code to focus on higher-level issues.**

Architects are the best programmers on the team. They continue taking programming tasks because they cannot do their jobs properly without experiencing the problems they create for other programmers. They may write less code than others, but they stay in the trenches.

### 2. Architecture Is the Shape of the System

**Architecture is defined by three things: (1) the division of the system into components, (2) the arrangement of those components, and (3) the ways those components communicate with each other.**

This shape is created by those who build the system. The purpose of that shape is to facilitate development, deployment, operation, and maintenance. The strategy behind that facilitation is to leave as many options open as possible, for as long as possible.

### 3. Architecture Has Little Bearing on Whether the System Works

**The architecture of a system has very little bearing on whether that system works. Many systems with terrible architectures work just fine.**

Their troubles lie not in operation but in deployment, maintenance, and ongoing development. Architecture's role in supporting proper behavior is passive and cosmetic, not active or essential. There are few, if any, behavioral options that architecture can leave open. The primary purpose is the life cycle of the system, not its feature checklist.

### 4. Development: Architecture Must Match Team Structure

**A small team of five can effectively develop a monolithic system without well-defined components; a system developed by five teams of seven each cannot make progress unless the system is divided into well-defined components with reliably stable interfaces.**

Different team structures demand different architectural decisions. The "component-per-team" architecture that naturally emerges under schedule pressure is unlikely to be optimal for deployment, operation, and maintenance. Architecture must serve the team structure, but not at the cost of the other three perspectives.

### 5. Deployment: Aim for Single-Action Deployment

**The higher the cost of deployment, the less useful the system. Architecture should make the system easily deployable with a single action.**

Deployment strategy is rarely considered during initial development. A micro-service architecture may make development easy (firm component boundaries, stable interfaces), but when deployment arrives, the sheer number of services becomes daunting. Configuring inter-service connections and startup timing becomes a huge source of errors. Early consideration of deployment constraints might have led to fewer services or a hybrid approach.

### 6. Operation: Architecture Communicates Operational Needs

**Hardware is cheap and people are expensive. Architectures that impede operation are less costly than architectures that impede development, deployment, and maintenance.**

Almost any operational difficulty can be resolved by throwing more hardware at the system without drastically changing the architecture. But architecture serves operation in a deeper way: a good architecture communicates the operational needs of the system. It elevates use cases, features, and required behaviors to first-class entities — visible landmarks that make the system readily apparent to developers, simplifying understanding and aiding development and maintenance.

### 7. Maintenance: Architecture Mitigates Spelunking and Risk

**Maintenance is the most costly aspect of a software system. The primary cost is spelunking (digging through existing code to find the right place for a change) and risk (the likelihood of introducing inadvertent defects).**

A carefully thought-through architecture vastly mitigates these costs. By separating the system into components and isolating them through stable interfaces, it illuminates the pathways for future features and greatly reduces the risk of inadvertent breakage.

### 8. Keeping Options Open: Separate Policy from Details

**All software systems decompose into two elements: policy (business rules and procedures — where the true value lives) and details (IO devices, databases, web systems, frameworks, protocols — things that enable communication with the policy but don't impact its behavior).**

The goal of the architect is to create a shape where policy is the most essential element and details are made irrelevant to that policy. This allows decisions about details to be delayed and deferred. For example:

- You don't need to choose a database early — high-level policy shouldn't care if it's relational, distributed, hierarchical, or flat files.
- You don't need to choose a web server early — high-level policy shouldn't know it's being delivered over the web.
- You don't need to adopt REST, micro-services, or SOA frameworks early — high-level policy should be agnostic about the interface to the outside world.
- You don't need a dependency injection framework early — high-level policy shouldn't care how dependencies are resolved.

The longer you wait to make decisions, the more information you have, and the more experiments you can run.

### 9. Even Pre-Made Decisions Should Be Treated as Deferrable

**What if your company has already committed to a certain database, web server, or framework? A good architect pretends the decision has not been made, and shapes the system such that those decisions can still be deferred or changed for as long as possible.**

The maxim: **a good architect maximizes the number of decisions not made.**

### 10. Device Independence: The Junk Mail Example

**In the 1960s, programmers bound code directly to IO devices. When magnetic tape replaced punched cards, every program had to be rewritten. The lesson: decouple policy from the device.**

Operating systems evolved to abstract IO devices into software functions — programs invoked OS services for abstract unit-record devices, and operators could connect those abstractions to card readers, magnetic tape, or any other device without changing the code. This was the Open–Closed Principle born before it was named.

In the junk mail example, a company printed personalized advertisements using an IBM 360. Their programs didn't care about devices because they used IO abstractions. Switching from a line printer to magnetic tape required no code changes — the tape was written in 10 minutes, then mounted on five offline printers running 24/7, producing hundreds of thousands of letters weekly.

**The lesson:** The policy was formatting names and addresses. The detail was the device. The decision about which device to use was deferred. The shape of the program disconnected policy from detail.

### 11. Physical Addressing: The Disk Drive Example

**In the early 1970s, a team hard-wired cylinder/head/sector numbers directly into their business logic for an accounting system. When the disk drive needed upgrading, everything broke.**

Every business rule knew the physical disk structure in detail. Upgrading to a new disk required a special translation program AND changes to all the hard-wired code everywhere. A more experienced programmer advised using relative addresses: treat the disk as a single linear array of sequential integers, with a small conversion routine that translated relative addresses to physical cylinder/head/sector numbers on the fly.

**The lesson:** Change the high-level policy to be agnostic about the physical structure of the disk. Decouple the decision about disk drive structure from the application. The policy stays clean; only the conversion layer changes when hardware changes.

### 12. The Principle in the Large

**Good architects carefully separate details from policy, and then decouple the policy from the details so thoroughly that the policy has no knowledge of the details and does not depend on the details in any way. Good architects design the policy so that decisions about the details can be delayed and deferred for as long as possible.**

The junk mail and disk drive stories are small-scale examples of the principle architects employ at scale. Separate policy from detail. Decouple them completely. Defer all detail decisions. This is what makes software soft.

---

## Summary Checklist

- [ ] Is the architect still writing code and experiencing the same problems as the rest of the team?
- [ ] Is the system shaped into well-defined components with stable interfaces — matching team structure without compromising deployment, operation, and maintenance?
- [ ] Can the system be deployed with a **single action**?
- [ ] Does the architecture reveal operational needs — are use cases and behaviors elevated to first-class visible landmarks?
- [ ] Are components isolated through stable interfaces to minimize **spelunking** (finding where to make a change) and **risk** (inadvertent breakage)?
- [ ] Is **policy** (business rules) cleanly separated from **details** (database, web, frameworks, protocols)?
- [ ] Is the high-level policy agnostic about the database technology (relational, distributed, flat file)?
- [ ] Is the high-level policy agnostic about delivery mechanism (web, desktop, console)?
- [ ] Is the high-level policy agnostic about the interface to the outside world (REST, SOA, micro-services)?
- [ ] Is the high-level policy agnostic about dependency injection or framework choices?
- [ ] Are decisions about details **deferred** for as long as possible — until you have the maximum information to make them?
- [ ] Are pre-existing company commitments treated as **deferrable** — does the architecture allow changing them later?
- [ ] Is the architecture maximizing the **number of decisions NOT made**?

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[Screaming Architecture]]
- [[Boundaries]]
- [[Architectural Independence]]
- [[Policy and Business Rules]]
- [[SOLID Design Principles]]
