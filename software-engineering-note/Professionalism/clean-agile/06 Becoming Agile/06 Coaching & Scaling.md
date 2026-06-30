---
tags:
- agile
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# 06 Coaching, Scaling & Tools

Coaching keeps the team honest. Scaling keeps Agile working beyond 12 people. Tools should become transparent — not become the process.

---

## Coaching

### Trainer vs Coach

| Role | Who | Duration |
|------|-----|----------|
| **Agile Trainer** | Hired from outside | Short tenure (weeks). Inculcates initial values. |
| **Agile Coach** | Someone from within the team | Ongoing. Acts as the team's conscience. |

### What a Coach Does

- Makes sure the team sticks to the Agile way
- Role can rotate among team members — as long as it's taken seriously
- Not a manager. Not responsible for planning or budget.
- Customers and managers don't need to know who the coach is — it's internal.

### Scrum Master Trap

In Scrum, the coach is called a Scrum Master. Many project managers took the certification — so the role is often conflated with project manager. The certificate proves the fee was paid, not that transformation occurred. If formal training is given, **the entire team should receive it**, not just one person.

---

## An Alternative View (Damon Poole)

> Coaching is not prescribing a solution — it's discovering blind spots and bringing underlying beliefs that stand in the way to the surface.

- Coaching = asking questions
- Training must account for the learner's unique circumstances
- The learner needs to see "what's in it for me"
- Agile transformation should be conducted in an **Agile way** — not as a top-down project

---

## Agile in the Large

Agile was intended for **small teams** (4–12 developers). But it was soon tried at scale:

| Approach | What It Is |
|----------|-----------|
| **Scrum of Scrums** | Representatives from each Scrum team coordinate |
| **SAFe** (Scaled Agile Framework) | Heavy framework for enterprise |
| **LeSS** (Large Scale Scrum) | Lighter framework for multiple teams |

### Uncle Bob's Take

> The problem of managing big teams is as old as civilization and has been solved rather well. (Pyramids were built.) The problem of organizing small software teams is rather new. Software requires a special set of disciplines.

Big software teams are just small teams organized together. The former is standard management — solved. The latter is Agile.

---

## Agile Tools (Tim Ottinger & Jeff Langr)

### The Carpenter's Lesson

Carpenters first master hand tools (hammer, saw) before power tools (nail gun, CAD). They never abandon hand tools. They pick the right tool for each job: **simple task, simple tool.**

### Tool Mastery

> Through mastery, the tool becomes **transparent.** You focus on the problem, not the tool. Without mastery, tools become an impediment.

### Great Tools...

| Quality | Meaning |
|---------|---------|
| Help people accomplish objectives | Don't get in the way |
| Learnable "well enough" quickly | 80/20 rule applies |
| Become transparent | Disappear in use |
| Allow adaptation and exaptation | Git's cheap branching enabled `test && commit || revert` |
| Affordable | Cost shouldn't be a barrier |

### ALM (Agile Lifecycle Management) Tools — The Warning

Complicated ALM tools require constant attention and upfront training. They usually can only be changed in ways vendors intended. They're expensive and never become transparent.

> ALM tools offer powerful performance charts and statistics — which can be used as a **weapon against programmers** to shame them into working harder. They should not replace personal, informal interactions.

**When in doubt, start with a simple tool.** Sticky notes and a whiteboard for co-located teams. Switch to powerful tools only if needed — not because the vendor's demo was convincing.

---

## Sources

- Martin, Robert C. *Clean Agile*, Chapter 6.
