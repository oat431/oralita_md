---
tags:
- design-patterns
- oop
- overview
- software-design
- software-engineering
---

# Design Patterns — Knowledge Base

> *Source: Dive Into Design Patterns by Alexander Shvets, Refactoring.Guru (2022), 411 pages*

A complete Obsidian knowledge base for the 22 Gang of Four design patterns, plus foundational OOP, design principles, and SOLID. Each chapter summarized into a standalone `.md` note with intent, problem/solution, pseudocode examples, pros/cons, and cross-referenced [[wikilinks]].

---

## 📂 Directory Structure

```
Design Pattern/
├── overview.md                          ← You are here
├── 01-Foundations/                      (6 files)
│   ├── how-to-read-this-book.md
│   ├── introduction-to-oop.md
│   ├── introduction-to-design-patterns.md
│   ├── features-of-good-design.md
│   ├── design-principles.md
│   └── solid-principles.md
├── 02-Creational/                       (5 patterns)
│   ├── factory-method.md
│   ├── abstract-factory.md
│   ├── builder.md
│   ├── prototype.md
│   └── singleton.md
├── 03-Structural/                       (7 patterns)
│   ├── adapter.md
│   ├── bridge.md
│   ├── composite.md
│   ├── decorator.md
│   ├── facade.md
│   ├── flyweight.md
│   └── proxy.md
├── 04-Behavioral/                       (10 patterns)
│   ├── chain-of-responsibility.md
│   ├── command.md
│   ├── iterator.md
│   ├── mediator.md
│   ├── memento.md
│   ├── observer.md
│   ├── state.md
│   ├── strategy.md
│   ├── template-method.md
│   └── visitor.md
└── 05-Conclusion/
    └── conclusion.md
```

---

## 📖 Chapter Map

### Foundations — Core Concepts Before Patterns

| # | File | Pages | Description |
|---|------|-------|-------------|
| 1 | [[how-to-read-this-book]] | p. 6 | Navigation guide, 22 GoF patterns, pseudocode convention |
| 2 | [[introduction-to-oop]] | pp. 7–25 | Classes, objects, 4 pillars, 6 object relationships |
| 3 | [[introduction-to-design-patterns]] | pp. 26–31 | Pattern anatomy, classification, GoF history |
| 4 | [[features-of-good-design]] | pp. 32–36 | Code reuse, extensibility, the three drivers of change |
| 5 | [[design-principles]] | pp. 37–50 | Encapsulate What Varies, Program to Interface, Favor Composition |
| 6 | [[solid-principles]] | pp. 51–70 | SRP, OCP, LSP, ISP, DIP |

### Creational Patterns — Object Creation

| # | File | Pages | One-liner |
|---|------|-------|-----------|
| 7 | [[factory-method]] | pp. 74–89 | Delegate object creation to subclasses via a virtual constructor |
| 8 | [[abstract-factory]] | pp. 90–104 | Produce families of related objects without specifying concrete classes |
| 9 | [[builder]] | pp. 105–123 | Construct complex objects step by step |
| 10 | [[prototype]] | pp. 124–137 | Copy existing objects without depending on their classes |
| 11 | [[singleton]] | pp. 138–146 | Ensure a class has only one instance with global access |

### Structural Patterns — Object Composition

| # | File | Pages | One-liner |
|---|------|-------|-----------|
| 12 | [[adapter]] | pp. 150–163 | Make incompatible interfaces collaborate |
| 13 | [[bridge]] | pp. 164–178 | Split abstraction from implementation for independent evolution |
| 14 | [[composite]] | pp. 179–192 | Compose objects into tree structures; treat uniformly |
| 15 | [[decorator]] | pp. 193–210 | Attach new behaviors via wrapper objects |
| 16 | [[facade]] | pp. 211–220 | Simplified interface to a complex subsystem |
| 17 | [[flyweight]] | pp. 221–234 | Share common state to fit more objects in RAM |
| 18 | [[proxy]] | pp. 235–246 | Placeholder that controls access to another object |

### Behavioral Patterns — Object Communication

| # | File | Pages | One-liner |
|---|------|-------|-----------|
| 19 | [[chain-of-responsibility]] | pp. 251–268 | Pass requests along a chain of handlers |
| 20 | [[command]] | pp. 269–289 | Turn requests into standalone objects with undo support |
| 21 | [[iterator]] | pp. 290–304 | Traverse collections without exposing internals |
| 22 | [[mediator]] | pp. 305–320 | Centralize chaotic many-to-many communications |
| 23 | [[memento]] | pp. 321–336 | Save/restore object state without breaking encapsulation |
| 24 | [[observer]] | pp. 337–352 | Subscription mechanism for event notification |
| 25 | [[state]] | pp. 353–368 | Alter behavior when internal state changes |
| 26 | [[strategy]] | pp. 369–381 | Family of interchangeable algorithms |
| 27 | [[template-method]] | pp. 382–393 | Skeleton algorithm with subclass-customizable steps |
| 28 | [[visitor]] | pp. 394–409 | Separate algorithms from the objects they operate on |

### Closing

| # | File | Pages | Description |
|---|------|-------|-------------|
| 29 | [[conclusion]] | p. 410 | Book wrap-up and final thoughts |

---

## 🧭 How to Use This Vault

1. **First-time reader** → Start with `01-Foundations/` in order (how-to-read → OOP → patterns intro → design principles → SOLID).
2. **Pattern lookup** → Jump directly to the pattern in `02-Creational/`, `03-Structural/`, or `04-Behavioral/`. Each file is self-contained.
3. **Cross-reference** → Every pattern file has a `## Related` section with `[[wikilinks]]` to connected patterns and principles.
4. **Quick review** → Each file has a `## Summary Checklist` — run through the checkboxes.
5. **Graph view** → Open Obsidian's Graph View on this folder to see the web of pattern relationships.

---

## 📊 Stats

- **29** markdown files
- **22** design patterns (GoF catalog)
- **6** foundation chapters
- **1** conclusion
- **~50–100K words** total
- Full `[[wikilink]]` cross-referencing between all patterns and principles
