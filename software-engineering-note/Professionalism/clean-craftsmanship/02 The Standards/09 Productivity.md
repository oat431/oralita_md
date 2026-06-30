---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 09 Productivity

Your new CTO walks in. She doesn't know the codebase, doesn't know the history, doesn't owe anyone loyalty. She asks one question: **"Are we productive?"** These are the standards she'll judge you by.

---

## We Will Never Ship Shit

> The first standard of productivity: we do not ship bad code.

Shipping bad code is not faster. It's slower. Every shortcut creates technical debt that compounds with interest. The team that "goes fast" by cutting quality is the team that grinds to a halt six months later.

---

## Inexpensive Adaptability

> Software is called "soft" for a reason. It's supposed to be easy to change.

| Sign of Good Adaptability | Sign of Bad Adaptability |
|--------------------------|-------------------------|
| Small change = small effort | Small change = days of work |
| New feature slots in naturally | New feature requires "refactoring first" |
| Architecture welcomes change | Architecture resists change |

If your software is hard to change, it's not soft. It's hard-ware. And you've failed at the one thing that makes software valuable.

---

## We Will Always Be Ready

> At the end of every iteration, the system must be technically deployable.

Not "could be deployed with a week of preparation." Not "the code is done but QA hasn't tested it." **Deployable.** Code clean. Tests passing. Acceptance tests green. Deploying is a business decision — not a technical one.

---

## Stable Productivity

> Productivity should not decline over time. The codebase should not become a swamp that slows everyone down.

| Red Flag | What It Means |
|----------|--------------|
| Velocity declining sprint after sprint | Code rot. Fear of refactoring. |
| "We need a refactoring sprint" | You weren't refactoring continuously. Now you're paying the debt. |
| "The old system is too messy — let's rewrite" | The rewrite will fail. The old system's mess is your only spec. |

The only way to maintain stable productivity is continuous refactoring, continuous testing, and continuous attention to code quality.

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 9.
