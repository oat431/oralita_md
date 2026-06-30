---
tags:
- clean-architecture
- software-design
- software-engineering
---

# Programming Paradigms

> *Source: Clean Architecture by Robert C. Martin, Chapters 3–4, 6 (pp. 38–45, 56–63)*

---

## Core Principle

> **The three programming paradigms impose three constraints: structured programming removes goto, OOP removes function pointers, and functional programming removes assignment. Each constraint removes something — not adds.**

All three paradigms were discovered within a single decade (1958–1968), and no new paradigm has emerged since. Paradigms are *negative* in intent: they tell us what **not** to do, yet these three restrictions — on direct control flow, indirect control flow, and variable mutation — are the *only* tools we have for managing function, component separation, and data in architecture.

---

## The Rules / Key Concepts

### 1. Three Paradigms as Constraints

Each paradigm takes something away rather than giving something new. Together they remove **goto** (structured programming), **function pointers** (OOP), and **assignment** (functional programming). Martin argues there is likely nothing left to remove — these three were all discovered between 1958 and 1968, and no further negative paradigm has appeared since.

These constraints map directly to the three big concerns of architecture:

| Paradigm              | Removes            | Architectural Role                          |
| --------------------- | ------------------ | ------------------------------------------- |
| Structured Programming | `goto`            | Algorithmic foundation of modules           |
| OOP                   | Function pointers  | Mechanism to cross architectural boundaries |
| Functional Programming | Assignment         | Discipline on location of and access to data |

### 2. Structured Programming — The Böhm-Jacopini Proof

In 1966, Böhm and Jacopini proved that **all programs can be constructed from just three control structures**: sequence, selection (`if/then/else`), and iteration (`do/while`).

Dijkstra built on this. He showed that unrestricted `goto` statements prevent modules from being decomposed recursively — they block the divide-and-conquer approach needed for proofs. The subset of `goto` that *didn't* cause this problem mapped exactly to Böhm-Jacopini's three structures.

### 3. Dijkstra's "Goto Considered Harmful"

In 1968, Dijkstra published his famous letter to CACM titled *"Go To Statement Considered Harmful."* It ignited a decade-long war in the programming world. Dijkstra won: `goto` receded from languages until it all but disappeared. Today we are all structured programmers by default — our languages simply don't offer undisciplined direct transfer of control.

> Named breaks in Java or exceptions are *not* `goto` analogs — they are constrained, not the utterly unrestricted jumps of early Fortran or COBOL.

### 4. Functional Decomposition

Structured programming enables modules to be **recursively decomposed into provable units**. This means large problems can be broken into high-level functions, each decomposing into smaller functions — *ad infinitum* — all using only the restricted control structures. This foundation gave rise to structured analysis and structured design throughout the late 1970s and 1980s.

At the architectural level, functional decomposition remains **one of our best practices** — software architects define modules, components, and services that are easily falsifiable (testable) by applying restrictive disciplines at higher levels.

### 5. Testing as Falsifiability (Science, Not Math)

Dijkstra's dream of a Euclidean hierarchy of formal proofs never materialized. But software found a different route: **the scientific method**.

> *"Testing shows the presence, not the absence, of bugs."* — Dijkstra

- **Mathematics** proves provable statements **true**.
- **Science** proves provable statements **false**.
- Software is a **science**, not mathematics. We show correctness by *failing* to prove incorrectness.

A program that is unprovable (due to unrestrained `goto`) can never be deemed correct, no matter how many tests. Structured programming forces programs into small provable units that *can* be tested for falsifiability. After sufficient testing effort that fails to prove incorrectness, we deem the program **correct enough for our purposes**.

### 6. Functional Programming — Immutability as Architecture

> **Variables in functional languages do not vary.**

The practical consequence: **all race conditions, deadlocks, and concurrent update problems are caused by mutable variables.** If nothing mutates, none of these problems can exist. As an architect designing for multi-threaded, multi-processor environments, immutability is the single most powerful concurrency strategy.

The question is whether immutability is practicable. The answer: yes, with infinite storage and processor speed; pragmatically, yes, **with compromises**.

### 7. Segregation of Mutability

Split the application into two kinds of components:

- **Immutable components** — purely functional, no mutable variables. Perform the bulk of processing.
- **Mutable components** — allow state mutation, but protect mutable variables with **transactional memory** (compare-and-swap, retry-based schemes like Clojure's `atom`/`swap!`).

Architects should push **as much processing as possible into immutable components**, and drive code *out* of components that must mutate. The discipline is: mutate only where necessary, and when you must, protect it with transactions.

### 8. Event Sourcing — Store Transactions, Not State

A radical application of immutability: **don't store state at all — store only the transactions**.

| Traditional CRUD    | Event Sourcing (CR) |
| ------------------- | ------------------- |
| Store account balance | Store every deposit/withdrawal |
| Mutate balance       | Replay transactions to compute balance |
| Prone to concurrent update issues | Immutable — no update conflicts |

Shortcuts make this practical: save computed state snapshots periodically (e.g., every midnight), then only replay transactions since the last snapshot. As storage grows trillions of bytes, this becomes viable for the reasonable lifetime of most applications. This is exactly how **source code control systems** work — they store diffs, not the final state.

---

## Summary Checklist

- [ ] Treat paradigms as **constraints** — they remove capabilities, they don't add features
- [ ] Build all modules from the three Böhm-Jacopini structures: sequence, selection, iteration
- [ ] Use functional decomposition to break systems into small, falsifiable (testable) units
- [ ] Prove correctness through **tests that try to prove incorrectness** — this is science, not math
- [ ] Push as much processing as possible into **immutable components** — mutability is the root of all concurrency bugs
- [ ] Protect mutable state with **transactional memory** when mutation is unavoidable
- [ ] Consider **event sourcing** for systems where CRUD conflicts become unmanageable — store transactions, compute state on demand
- [ ] Remember: software is not a rapidly advancing technology — the essence (sequence, selection, iteration, indirection) hasn't changed since 1946

---

## Related

- [[Clean Architecture Overview]]
- [[Object-Oriented Programming]]
- [[SOLID Design Principles]]
- [[Component Cohesion]]
- [[The Clean Architecture]]
