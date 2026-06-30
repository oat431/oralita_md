---
tags:
- clean-code
- overview
- software-design
- software-engineering
---

# Clean Code — Overview

> *"Writing clean code is what you must do in order to call yourself a professional."*
> — Robert C. Martin

A handbook of Agile software craftsmanship. This book is not "feel good" theory — it demands you sweat through case studies, read bad code, and watch it get refactored step-by-step.

---

## Structure

The book has three parts:
1. **Chapters 1–13:** Principles, patterns, and practices
2. **Chapters 14–16:** Case studies (line-by-line refactoring walkthroughs)
3. **Chapter 17:** Smells & Heuristics — a reference catalog of 66 code smells

---

## Chapter Map

### Part I: Principles & Practices

| # | Topic | Key Takeaway |
|---|-------|--------------|
| 1 | [[Clean Code Principles]] | The cost of mess, Boy Scout Rule, code-sense, masters' definitions |
| 2 | [[Naming Conventions]] | Intention-revealing names, avoid disinformation, pronounceable, searchable |
| 3 | [[Function Design]] | Small! Do one thing, minimize arguments, no side effects, DRY |
| 4 | [[Comment Patterns]] | Good vs bad comments — 26 types catalogued. Comments are failures to express in code |
| 5 | [[Formatting Style]] | Newspaper metaphor, vertical/horizontal rules, team conventions over personal style |
| 6 | [[Objects vs Data Structures]] | Data/object anti-symmetry, Law of Demeter, DTOs, Active Records |
| 7 | [[Error Handling]] | Exceptions over return codes, try-catch-first, Special Case pattern, never return/pass null |
| 8 | [[Boundaries & Dependencies]] | Wrapping third-party APIs, learning tests, adapter pattern for unwritten code |
| 9 | [[Unit Testing]] | Three Laws of TDD, BUILD-OPERATE-CHECK, F.I.R.S.T., clean tests enable change |
| 10 | [[Class Design & SOLID]] | SRP, OCP, DIP, high cohesion, organizing for change, isolating from change |
| 11 | [[System Architecture]] | Separate construction from use, dependency injection, AOP, DSLs, defer decisions |
| 12 | [[Emergent Design]] | Kent Beck's 4 rules: tests, no duplication, expressiveness, minimal classes |
| 13 | [[Concurrency]] | Defense principles, execution models, keep synchronized sections small, test ruthlessly |

### Part II: Case Studies

| # | Case Study | What You'll Learn |
|---|-----------|-------------------|
| 14 | [[Case Study - Args Parser]] | Full refactoring journey (9 phases): boolean → string → integer → polymorphic marshalers. The cost of incremental mess and the discipline of incremental cleanup |
| 15 | [[Case Study - JUnit Internals]] | Refactoring ComparisonCompactor: rename → extract methods → reorganize conditionals → separate concerns |
| 16 | [[Case Study - SerialDate]] | Cleaning a real open-source library: enums over ints, factory pattern, removing magic numbers, improving inheritance |

### Part III: Reference

| # | Topic | Key Takeaway |
|---|-------|--------------|
| 17 | [[Code Smells Catalog]] | 66 heuristics across 7 categories: Comments (5), Environment (2), Functions (4), General (36), Names (7), Java (3), Tests (9) |

---

## Core Philosophy

- **The Boy Scout Rule:** Leave the campground cleaner than you found it. Every check-in, improve something.
- **Code is read 10x more than written** — optimize for reading, even if it makes writing slightly harder.
- **The only way to go fast is to keep it clean.** Cutting corners slows you down instantly.
- **Small things matter.** Consistent naming, indentation, and formatting aren't trivial — they're the fabric of professionalism.
- **Bad code is your fault.** Not the schedule's, not the manager's. Professionals defend code with the same passion managers defend deadlines.
- **Craftsmanship = knowledge + practice.** Reading isn't enough. You must sweat through the case studies.
- **Tests are non-negotiable.** Code without tests is not clean, no matter how elegant.

---

## How to Use This Vault

1. **New to Clean Code?** Start with [[Clean Code Principles]] → then read chapters 2–13 in order
2. **Want to learn refactoring?** Jump straight to the three case studies (14–16) — watch bad code become clean step by step
3. **Code review checklist?** Open [[Code Smells Catalog]] — 66 things to scan for
4. **Preparing a talk/course?** Each file is self-contained with code examples, checklists, and cross-links
5. **Open Obsidian graph view** to see how all concepts interconnect through `[[wikilinks]]`

---

## Sources

- Martin, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall, 2009. ISBN 0-13-235088-2.
