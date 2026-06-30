---
tags:
- book-summary
- pragmatic-programmer
- professionalism
- software-engineering
---

# 02 A Pragmatic Approach (Tips 11–19)

How to design systems that don't break when you look at them wrong. DRY, orthogonality, reversibility — the principles that make code maintainable.

---

## Tip 11: DRY — Don't Repeat Yourself

> Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

DRY is not just about code duplication. It's about **knowledge duplication.**

| Type of Duplication | Example | Fix |
|-------------------|---------|-----|
| Imposed duplication | Documentation repeats code | Auto-generate docs from code comments |
| Inadvertent duplication | Two classes validate email differently | Extract shared validation |
| Impatient duplication | Copy-paste because "I'll fix it later" | Extract now. Later never comes. |
| Interdeveloper duplication | Two devs write the same utility | Communicate. Shared library. |

> Code generators, build scripts, and configuration files should all pull from a single source of truth. When knowledge changes, ONE place updates.

---

## Tip 12–13: Orthogonality

> Two components are orthogonal if a change in one doesn't affect the other.

Orthogonal systems are easier to develop, test, and maintain. Like the X and Y axes — move along X, Y stays the same.

| Non-Orthogonal | Orthogonal |
|---------------|-----------|
| Database code in UI layer | Separate layers: UI → Service → Repository |
| Configuration hardcoded | External config files |
| Global state everywhere | Explicit dependency injection |
| Monolithic procedures | Small, focused functions with clear contracts |

### How to Stay Orthogonal
- Keep your code decoupled
- Avoid global data
- Avoid similar functions (they probably hide duplication)

---

## Tip 14: Reversibility — There Are No Final Decisions

> Always leave yourself an escape hatch.

You picked PostgreSQL. Great. But don't couple your entire codebase to PostgreSQL-specific features. Write to an interface. If you need to switch to MySQL or MongoDB later, the switch is measured in weeks, not months.

| Coupled Decision | Reversible Decision |
|-----------------|-------------------|
| "We use Oracle" | "We use a relational database behind a repository interface" |
| "We deploy on AWS" | "We deploy on a cloud provider. Currently AWS." |
| "We use React" | "We use a frontend framework." |

---

## Tip 15: Tracer Bullets

> Use "tracer bullets" to find the target. Build a thin, end-to-end skeleton of the system first.

Tracer bullets let you see if you're aiming at the right target before firing the big guns. Build a minimal but functional version that touches every layer of the system. It proves the architecture works, gives you early feedback, and provides a working platform to iterate on.

---

## Tip 16: Prototype to Learn

> Prototypes are designed to answer specific questions. They are THROWN AWAY.

| Prototype | Production Code |
|-----------|----------------|
| Answers a question | Delivers a feature |
| Quick and dirty | Clean and tested |
| Thrown away | Maintained forever |

### What to Prototype
- Architecture feasibility
- New functionality in an existing system
- Third-party integration
- UI design and flow
- Performance characteristics

---

## Tip 17: Domain Languages

> Program close to the problem domain.

Instead of forcing business logic into programming language constructs, create a mini-language that expresses the domain naturally. A simple DSL can be just well-named functions. A complex one might be a full parser.

```ruby
# Not a DSL
if customer.status == :active && customer.balance > 100

# A simple internal DSL
if customer.active? && customer.has_minimum_balance?(100)
```

---

## Tip 18–19: Estimating

> Estimate to avoid surprises. Iterate the schedule with the code.

### How to Estimate

1. Understand what's being asked
2. Build a model of the system
3. Break the model into components
4. Give each component a value — as a **range** (best/worst case)
5. Calculate the delivery range

### What to Say

| Don't Say | Say |
|----------|-----|
| "It'll take 2 weeks." | "Based on what I know, between 10 and 20 days." |
| "I'll be done by Friday." | "I'll know more by Thursday. I'll update you then." |
| "Easy — a few days." | "Let me spend a day investigating and get back to you." |

---

## Sources

- Hunt & Thomas. *The Pragmatic Programmer*, Chapter 2.
