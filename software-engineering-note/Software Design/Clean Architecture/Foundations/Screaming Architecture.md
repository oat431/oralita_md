---
tags:
- clean-architecture
- software-design
- software-engineering
---

# Screaming Architecture

> *Source: Clean Architecture by Robert C. Martin, Chapter 21 (pp. 158–160)*

---

## Core Principle

> **A software architecture should scream the use cases of the system, not the frameworks it uses. When you look at the top-level directory structure and source files, they should say "Health Care System" or "Accounting System"—not "Rails," "Spring," or "ASP."**

Architectures are structures that support the use cases of the application, just as a building's blueprints reveal whether it is a home or a library. Frameworks are tools to be used, not architectures to be conformed to. A good architecture decouples use cases from peripheral concerns, allowing framework, database, and delivery decisions to be deferred and changed with minimal cost.

---

## The Rules / Key Concepts

### 1. Architecture Screams Intent, Not Implementation

The first impression of a codebase should reveal *what the system does*, not *how it is built*. When new programmers open the source repository, they should immediately recognize the domain—health care, accounting, inventory—without any hint of the delivery mechanism or framework.

- Top-level packages and directories should be named after domain concepts (Patient, Claim, Invoice), not framework conventions (Controllers, Models, Views).
- The use cases of the system should be visible in the structure before any technical detail is apparent.
- If a developer asks "Where are the views and controllers?", the answer should be: "Those are details we'll decide later."

> *"Oh, this is a health care system"* is what a new programmer should think—not *"Oh, this is a Spring/Hibernate app."*

### 2. Frameworks Are Tools, Not Ways of Life

Frameworks are powerful, but they come with a cost: they demand that you structure your application *their way*. Framework authors and their disciples write examples from the perspective of true believers, assuming an all-encompassing, let-the-framework-do-everything posture.

**This is not the position you want to take.** Instead:

- Look at every framework with a jaded, skeptical eye. Ask: *What does it cost to adopt this?*
- Develop a strategy that prevents the framework from taking over the architecture.
- Treat frameworks as pluggable implementations behind abstractions, not as the skeleton of your system.
- Use the framework; do not let the framework use you.

The relationship should be tool-to-user, not master-to-disciple.

### 3. Defer Framework, Database, and Environmental Decisions

A good architecture makes it *unnecessary* to commit to Rails, Spring, Hibernate, Tomcat, or MySQL until much later in the project. It also makes it *easy* to change your mind about those decisions later.

- The first concern of the architect is ensuring the system is *usable* (the use cases are met), not ensuring it is made of bricks (a particular framework or database).
- Just as a homeowner can choose bricks, stone, or cedar *later*—after the floor plan is finalized—so should a software project be able to choose infrastructure details after the use-case structure is solid.
- Frameworks are options to be left open, not foundations to build upon.

### 4. The Web Is a Delivery Mechanism, Not an Architecture

The fact that an application is delivered over the web is a *detail*—an I/O device—and should not dominate the system structure. Your architecture should treat the web as one of many possible delivery channels.

- The decision to deliver over the web should be deferrable and reversible.
- The system should be equally deliverable as a console app, a web app, a thick client, or a web service—without undue complication or fundamental architectural change.
- Your architecture should be as ignorant as possible about *how* it is delivered.

### 5. Use-Case-Centered Architectures Are Naturally Testable

When your architecture is centered on use cases and keeps frameworks at arm's length, testability follows naturally:

- **Unit-test all use cases without any framework in place.** No web server running. No database connected.
- **Entity objects** should be plain old objects with no dependencies on frameworks, databases, or ORM annotations.
- **Use case objects** (interactors) coordinate Entity objects through plain interfaces, not framework hooks.
- All of them together should be testable *in situ*, without the complications and startup cost of frameworks.

If you cannot test your business logic without booting Spring, starting a web server, or connecting to a database, your architecture is not screaming its use cases—it is screaming its frameworks.

---

## Summary Checklist

- [ ] Top-level directory structure and package names reflect the domain, not the framework or delivery mechanism
- [ ] Use cases are visible, self-describing, and framework-agnostic
- [ ] Every framework is treated as a tool behind an abstraction, not a way of life
- [ ] Framework, database, and web-server decisions are deferred until the use-case structure is stable
- [ ] The web (or any delivery mechanism) is isolated as a pluggable I/O detail
- [ ] All use-case logic and Entity objects are unit-testable without frameworks, databases, or running servers
- [ ] A newcomer's first impression of the source tree is the *intent* of the system, not its technical stack

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[What Is Architecture]]
- [[Layers and Boundaries]]
- [[Boundaries]]
- [[Presenters and Humble Objects]]
