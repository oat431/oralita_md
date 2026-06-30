---
tags:
- book-summary
- pragmatic-programmer
- professionalism
- software-engineering
---

# 08 Pragmatic Projects (Tips 55–63)

Projects, not programs. Teams, not individuals. How Pragmatic Programmers work together to deliver quality.

---

## Tip 54: Pragmatic Teams — No Broken Windows

> The team as a whole must not tolerate broken windows.

A single developer who ignores quality drags the whole team down. The team must enforce quality collectively. Code reviews, shared standards, collective ownership — these are team responsibilities, not individual options.

### Team Characteristics

| Pragmatic Team | Dysfunctional Team |
|---------------|------------------|
| "We test everything." | "QA will find the bugs." |
| "Let me help you with that." | "Not my code, not my problem." |
| "Our velocity shows we need to adjust." | "We just need to work harder." |
| No broken windows tolerated | Broken windows everywhere |

---

## Tip 55: Ubiquitous Automation

> Automate everything that can be automated. Build, test, deploy, documentation, approvals.

| Manual | Automated |
|--------|----------|
| "Run these 5 commands to build" | `make build` or `./gradlew build` |
| "Test before you commit" | Pre-commit hooks run tests |
| "Email the release notes" | CI generates and publishes release notes |
| "Copy the files to the server" | CI/CD pipeline deploys automatically |

> If a human can do it, a script can do it better. Humans are creative. Machines are consistent. Use each for what they're best at.

---

## Tip 56: Ruthless Testing

> Test your software, or your users will. And they won't be nice about it.

### The Testing Pyramid (Hunt & Thomas version, 1999)

```
         ┌──────────┐
         │  System  │ ← Does the whole thing work?
        ┌┴──────────┴┐
        │ Integration│ ← Do the pieces fit together?
       ┌┴────────────┴┐
       │    Unit      │ ← Does THIS piece work?
       └─────────────┘
```

### What to Test

| Test Type | Tests What |
|-----------|-----------|
| **Unit** | Individual modules in isolation |
| **Integration** | Modules working together |
| **Validation** | Does it meet the requirements? |
| **Resource exhaustion** | What happens at the limits? |
| **Errors** | How does it handle failure? |
| **Performance** | Is it fast enough? |
| **Usability** | Can a human actually use it? |

### Testing Culture
- Tests should be **run automatically** on every build
- A failing test is a **stop-the-line** event
- Test **coverage matters**, but test **quality matters more**
- Every bug gets **two tests**: one that catches it, one that proves the fix

---

## Tip 57: It's All Writing

> Documentation is part of the product. Code comments, READMEs, API docs, design documents — they're all writing. Write well.

| Good Documentation | Bad Documentation |
|-------------------|-----------------|
| Explains WHY, not WHAT | Restates the code, but in English |
| Lives close to the code it documents | Lives in a separate system that nobody reads |
| Updated when code changes | "TODO: update docs" — from 2019 |
| Consistent style, proofread | Typos, mixed tenses, "TODO" sections |

---

## Tip 58: Great Expectations — Manage User Expectations

> The success of a project is measured by how well it meets expectations. Manage expectations actively.

Users don't judge software against perfection. They judge it against what they were told to expect. Under-promise and over-deliver.

---

## Tip 59: Pride and Prejudice — Sign Your Work

> Craftsmen of old signed their work. You should too.

Signing your work means taking ownership. When your name is on it, you have skin in the game. You care about quality. You fix bugs because they have YOUR name on them.

### How to Sign

- **Code reviews** — your name is on the review
- **Commit messages** — be clear, descriptive, and accountable
- **Module ownership** — "I built this. I maintain it. I'm proud of it."

> But: anonymity can also be protection. On team projects, the code is owned collectively. Don't let signing become finger-pointing. The team succeeds or fails together.

---

## Tip 60: Building Pragmatic Teams

A Pragmatic Programmer:
- Takes responsibility
- Doesn't live with broken windows
- Invests in their knowledge portfolio
- Communicates clearly
- DRY, orthogonal, reversible thinking
- Tests ruthlessly
- Automates everything

A team of Pragmatic Programmers is unstoppable.

---

## Sources

- Hunt & Thomas. *The Pragmatic Programmer*, Chapter 8.
