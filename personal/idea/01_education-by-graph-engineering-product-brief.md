---
document_type: Product Brief
schema_version: 2
canonical_name: Product Brief
doc_form: light
applicability: universal
min_project_tier: 1  # POC — confirm at grill session
minimum_form: "This one page — fill what you know, leave [?] where you don't"
standards_profile: "ISO/IEC 29110 VSE"  # T1-T4 default; revisit if tier changes at grill
version: "1.0"
status: Draft — idea seed, pending PO grill session
author: "Panomete (idea owner)"
created: "2026-11-16"
last_updated: "2026-11-16"
project_name: "Education by Graph Engineering"
classification: "Internal"
tags: [product-brief, intake, idea-seed, education, math, ai-personas, spec-driven, entry-point]
---

# Product Brief — Education by Graph Engineering

> **What this is:** the human's one-page seed for a new project. Write it rough — half-answers and `[?]` marks are fine. You fill this; the PO grills you on it; together you grow it into the real spec chain (Business Objectives → Stakeholder Needs → User Stories → Acceptance Criteria → …).
>
> **Rule:** this document stays *short*. If a section grows beyond a few lines, it belongs in a downstream template — the PO will move it during the grill session.

> **Filled by:** PO on behalf of Panomete, 2026-11-16, from a verbal idea seed ("initial idea"). Items marked `[?]` were **not** in the original idea — they are grill-session targets, not facts.

---

## 1. The Idea (one line)

> What do you want to build? One sentence, no jargon.

An AI-powered math homework companion with three big personalities — **Math Expert** (checks the homework), **Math Guidance** (creates personal challenge problems), and **Math Teacher** (evaluates whether the homework is good) — that never hands the student a solution, because its purpose is to make the student learn.

## 2. Why — The Problem / Motivation

> Why does this need to exist? Whose pain is it (yours? users'? a client's?)? What happens today without it?

- Problem: when students are stuck on math homework, today's tools either give nothing or instantly reveal the full solution (answer keys, solver apps, chatbots) — which shortcuts learning. Checking homework is also slow for teachers/parents, and good *personalized* practice is scarce.
- Today's workaround: answer keys, solver apps (Photomath, Wolfram, GPT-style chat), tutors, parents, or staying stuck.
- Why now: [?] — trigger not stated in the original idea.

## 3. Who — Users

> Who actually uses it? Be specific; "everyone" is a red flag the PO will grill.

| User | What they need from it |
|---|---|
| Student (primary; grade 1–12, possibly university) | Know whether their work is right/wrong *without* being given the answer; get nudged toward understanding |
| Student wanting more challenge | Personalized harder/practice problems matched to their level and mistakes (Math Guidance) |
| [? teacher / tutor / parent] | Quality evaluation of a homework/assignment (Math Teacher persona's actual customer — role to confirm) |

> ⚠️ The audience span "grade 1 → university" and the customer vs. user split are both `[?]` — the PO will grill this first.

## 4. Core Features (rough list)

> What must it do? Bullet points, no priority yet — the PO helps you cut and order these.

- **Homework checking** (Math Expert): verify a student's attempt, point at *where* the reasoning breaks, do not reveal the solution
- **Personalized challenge generation** (Math Guidance): create extra problems tailored to the student's level and observed mistakes
- **Homework quality evaluation** (Math Teacher): assess whether a homework is "good or not" — object of evaluation is `[?]` (the *assignment's* quality? or the *student's work's* quality?)
- **Three distinct personas**: the user interacts with three big, separate personalities — not one generic assistant
- **Solution-free guardrail (hard non-goal)**: the whole app never throws solutions at the student; every response teaches instead
- **Wide knowledge scope**: math from grade 1 to grade 12, even university ("any knowledge scope" — `[?]`: math-first or literally any subject?)

**Explicitly NOT wanted (if known):** giving full solutions to students — this is the product's defining constraint, not a nice-to-have.

## 5. Simple Data

> What information does it hold? A rough list is enough — field names, not types.

```
student: name, grade-level, [? curriculum]
homework-problem: statement, topic, difficulty, source
solution-attempt: steps, final-answer, [? input format: photo / handwriting / typed]
check-result: verdict-per-step, misconception-tag, hint-level-issued
knowledge-node: concept, grade-band, prerequisites   ← graph edge ("graph engineering" [?])
challenge-problem: generated-statement, target-concept, difficulty
homework-set: problems, assigned-by, quality-evaluation [?]
```

## 6. Simple Response / Shape

> If it's an API or has screens: what does "it worked" look like? A rough JSON sketch or a described screen is fine.

```json
{
  "verdict": "partially-correct",
  "step_feedback": [
    { "step": 2, "status": "error", "hint": "Check what happens to both sides when you divide..." }
  ],
  "solution_revealed": false
}
```

Key shape property: every response carries feedback or hints, never `solution`. (Chat-style persona screens are `[?]`.)

## 7. Picked Tech (and why)

> What stack are you leaning to? Honesty about constraints matters more than openness — the PO only challenges choices that fight your existing infra or the problem.

| Concern | Pick | Why |
|---|---|---|
| Language / framework | [?] — leaning Go + Fiber v3 | default stack preference; not decided for this project |
| Storage | [?] — PostgreSQL; knowledge-graph core may argue a graph model on top | `[?]` |
| Frontend | [?] — leaning Next.js | `[?]` |
| Deployment | [?] — homelab Docker + Cloudflare Tunnel | existing infra |
| External services | [?] — LLM provider(s) powering the three personas | persona behavior is presumably LLM-backed `[?]` |

> Note: "graph engineering" in the name implies a knowledge-graph core (concept/prerequisite graph) — whether that's a data-model choice, a reasoning method, or the process itself is `[?]`.

## 8. Constraints & Context

> Budget: [free / $X] · Time: [days / weeks / no deadline] · Must reuse: [existing infra, accounts, domains] · Privacy notes: [personal data involved?]

Budget: `[?]` · Time: `[?]` · Must reuse: `[?]` (homelab infra likely) · Privacy notes: **student data, potentially minors** — privacy and compliance are real product constraints; market/curriculum `[?]`.

## 9. What Does Success Look Like?

> One or two observable outcomes. Not metrics theater — what changes in your life/business when this works?

- A student who was stuck finishes the homework having *learned* the missing concept — and never saw the solution
- Generated challenge problems land at "hard but doable" — the student feels personally guided, not generic-practiced

Draft outcomes — to become measurable objectives (baseline/target/timeframe) in [[Business-Objectives]].

## 10. Open Questions / Unknowns

> Everything you're unsure about. The PO's grill session starts here.

- [?] **"Graph engineering" — what does it mean concretely?** Knowledge graph of concepts/prerequisites? Graph-based reasoning/traceability of errors? Or the engineering *methodology* behind the app?
- [?] **Who is the customer** — student, parent, teacher, school? Who pays, who uses?
- [?] **Math Teacher's evaluation object** — the *assignment's* quality (is this homework good?) or the *student's work* quality (is this homework done well?)
- [?] **Input format** — typed answers, photos of handwriting, LaTeX? Math notation input is make-or-break for young grades
- [?] **"Never give solutions"** — absolute, or graduated hints with a teacher-side reveal policy?
- [?] **First scope** — grade 1–12 + university is enormous; which grade band and topic first?
- [?] **Curriculum/locale** — Thai curriculum, US Common Core, or generic?
- [?] **Why now** — what triggered this idea?

## 11. My Tier Guess (optional)

> 🧪 POC · 🔧 Prototype · 🏠 Internal · 🟢 Small-Prod · 🔵 Medium-Prod · 🟣 Prod-Grade · 🔴 Mission-Critical
> The PO confirms this with the decision flow in `release.md` §"Which Tier Am I?" — it determines how much documentation the project needs.

Guess: 🧪 POC (PO suggestion — confirms at grill session)

---

## What Happens Next (PO workflow — do not fill)

| Step | Output | Template |
|---|---|---|
| 1. Grill session on this brief | Confirmed problem, users, scope, tier | — |
| 2. Business direction | Objectives + success measures | [[Business-Objectives]] |
| 3. Needs & stakeholders | Who needs what, evidence | [[Stakeholder-Needs-Document]] / [[Stakeholder-Analysis]] |
| 4. Requirements | Stories + acceptance criteria | [[User-Stories]], [[Acceptance-Criteria]] |
| 5. Tailored doc set | Tier checklist cut to real scope | [[Tailoring-Justification]] + `23_Project_Size/Tier-N` |
| 6. Design/QA/Dev handoffs | Per persona, via meeting minutes | Meeting-minute pattern (PO skill: `templates/designer-handoff-meeting-minute.md`) |

> This brief is **kept, not discarded** — it is the provenance record of the original human intent. Later documents link back to it.

## Related Documents

| Document | Relationship |
|---|---|
| [[Business-Objectives]] | First formal output grown from this brief |
| [[Business-Case]] | Heavy alternative when investment approval is needed |
| [[Tailoring-Justification]] | Records which tier checklist items are skipped and why |

---

> **Template Standard:** intake seed for spec-driven development; aligns with BABOK elicitation (confirmed vs unconfirmed results) and ISO/IEC 29110 VSE agreement process
> **Usage:** fill sections 1–10 roughly, hand to the PO, say "grill me". Keep it under two pages.
> **Source template:** `document_template/01_Business_Analysis_and_strategy/Product-Brief.md` (template repo untouched — this is the filled instance)
