---
tags:
- book-summary
- craftsmanship
- professionalism
- software-engineering
- uncle-bob
---

# 12 Harm — The Programmer's Oath

Ethics isn't optional. Programmers hold power over systems that affect lives, money, and safety. With that power comes a solemn obligation: **First, do no harm.**

---

## First, Do No Harm

> The first rule of professional programming: don't make things worse.

This sounds obvious. It's not. Every time you ship a bug, you harm someone. Every time you leave messy code, you harm the next developer. Every shortcut you take harms the system's future.

---

## No Harm to Society

Software runs the world. Banking, healthcare, transportation, communication, defense. Bugs kill people. They crash planes, misdiagnose patients, lose life savings.

> Ask yourself: "Could this code harm someone?" If the answer is yes — or even maybe — you have a moral obligation to get it right.

---

## Harm to Function

> The software must work. Not "mostly work." Not "work on my machine." WORK.

Every defect is harm. Every bug that reaches production is a failure of professionalism. The goal is zero defects — and while you may never reach it, you must never stop striving.

---

## No Harm to Structure

> Messy code harms the next developer. And the next. And the one after that.

Structural harm is invisible to users — but it compounds. Every messy module makes the next change harder. Every shortcut makes the next developer's job more painful. The Boy Scout Rule isn't optional. It's an ethical obligation.

### Soft

> Software is called "soft" because it's meant to be easy to change. Hard-to-change software has been turned into hardware. The developer who writes rigid code has violated the fundamental premise of the medium.

---

## Tests

> Code without tests is unethical. You're asking others to trust code you can't prove works.

Tests are not optional. They're the proof that your code does what you claim. Without them, you're asking for trust you haven't earned.

---

## Best Work

> You must always do your best work. Not your best given the circumstances. Your BEST.

| Excuse | Reality |
|--------|---------|
| "The deadline was too tight." | You should have said no, or reduced scope. |
| "The requirements were unclear." | You should have asked for clarification. |
| "Management made me cut corners." | You should have explained the consequences. |
| "Someone else wrote that mess." | It's yours now. Clean it. |

---

## Making It Right

When you find a bug, you fix it. When you see messy code, you clean it. When you realize a design is wrong, you refactor it. Not "later." Not "when there's time." Now.

> The professional does not walk past a problem. The professional stops and fixes it.

---

## Eisenhower's Matrix for Code

| | Urgent | Not Urgent |
|---|:---:|:---:|
| **Important** | 🔴 Critical bugs, security fixes | 🟡 Refactoring, improving structure |
| **Not Important** | 🟠 Interruptions, meetings | ⚪ Minor cosmetic issues |

> The tragedy of our industry: we prioritize urgent-but-unimportant (meetings, interruptions) over important-but-not-urgent (refactoring, improving structure). The professional reverses this.

---

## Sources

- Martin, Robert C. *Clean Craftsmanship*, Chapter 12.
