---
date: 2026-08-24
tags: [writing, prompt, ai, template]
---

# Prompt Writing Guide (AI)

> The most *executed* form of writing there is: the reader is a language model, and the text is acted on the moment it's read. A prompt is code for a probabilistic machine — precision beats elegance. Up to parent map [[00-Writing-Types]].

## What Makes Prompt Writing Different

| Human reader | Model reader |
|--------------|--------------|
| Fills gaps with inference, patience, context | Fills gaps by guessing — no patience, no world sense beyond training |
| Punishes ambiguity through confusion | Punishes ambiguity through *wrong output* |
| Reads once, remembers tone | Every word shifts probability — small rewrites change results |
| You can't test a letter before sending | **Prompts are instantly testable** — the response is your feedback loop |

The last row is the superpower: prompt writing is the only genre where you get a draft *and* a test run in the same minute. Write → run → read the output as evidence → fix. That loop is the whole craft.

## The Three Jobs of a Prompt

Every prompt answers three questions — missing one, and the model improvises it:

1. **WHO** — role/persona, when it matters ("You are a senior backend engineer reviewing a PR"). Skip when unnecessary — a persona is a tool, not a costume.
2. **WHAT** — the task, in one imperative verb ("Summarize", "Rewrite", "Compare", "Find"). Vague verbs ("help me with...") produce vague output.
3. **HOW** — the constraints: output format, length, audience, tone, structure, what to avoid.

## Frameworks (memory aids for the Three Jobs)

### RTF — minimal, daily-driver
**Role → Task → Format**

```
You are <ROLE>.
<TAKS — imperative verb, one job>
Respond in <FORMAT>: bullet list / JSON / 300 words / markdown table
```

Best for: 80% of everyday prompts. When you don't need it, skip it — short prompts work.

### CO-STAR — richer, important tasks (GovTech Singapore, popularized 2024)
**Context → Objective → Style → Tone → Audience → Response format**

| Letter | Element | Example |
|--------|---------|---------|
| C | Context — what the model must know | "This is a homelab runbook for a 25-year-old SE, beginner-friendly" |
| O | Objective — the ONE outcome | "Produce a 3-step fix for the sync conflict" |
| S | Style — writing style reference | "Concise, numbered steps, explain each command" |
| T | Tone — emotional register | "Direct, no fluff, no enthusiasm inflation" |
| A | Audience — who reads the output | "The user will execute these steps hands-on" |
| R | Response format — shape of output | "Markdown with a checklist at the end" |

Best for: high-stakes, multi-constraint prompts — exactly what you'd hand a specialist profile.

### CRISPE — creative / iterative work
**Capacity & Role → Insight → Statement → Personality → Experiment**

```
Act as <CAPACITY/ROLE> with expertise in <INSIGHT>.
Your task: <STATEMENT — the assignment>.
Match my style: <PERSONALITY — tone/voice constraints>.
Then: <EXPERIMENT — request 2-3 variations / ask me before proceeding>.
```

Best for: writing, naming, design exploration — anything where you want drafts + options, not one answer.

## Techniques (moves, not frameworks)

- **Few-shot beats description** — one concrete example ("Here's a sample: ...") outperforms three paragraphs explaining what you want. Show, don't tell — same law as storytelling, different mechanism.
- **Chain-of-thought for reasoning** — "Think step by step, then answer" measurably improves multi-step tasks (math, logic, planning). For writing tasks it can add stilted filler — use selectively.
- **Structured output** — if you need machine-readable results, demand the schema: "Return JSON: {title, summary, tags[]}".
- **Negative constraints phrased positively** — "Do NOT use emojis" works, but "Use plain text, no decorations" steers better.
- **One job per prompt** — a prompt doing two tasks makes the model split attention. Split it.
- **Iterate, don't re-prompt from scratch** — fix the failing part: "Keep everything, but change X to Y."

## Common Failure Modes

1. **Vague verbs** — "help me with my review" vs "rewrite my review: add one weakness paragraph, keep my voice"
2. **No output format** — the model picks its own, you get a wall of text
3. **Missing context** — the model guesses your audience, level, or constraints
4. **Constraint soup** — 8 demands at once; models satisfy the loudest, not all
5. **No testing** — treating the prompt as a spell instead of a first draft
6. **Persona abuse** — "you are a world-class expert" on every prompt dilutes actual instruction

## Fill-in Template

```markdown
# Prompt: <what it produces>

**Role:** <only if it helps>
**Task:** <one imperative verb + the deliverable>
**Context:** <what the model must know to not guess>
**Style/Tone:** <reference + register>
**Audience:** <who consumes the output>
**Format:** <structure, length, schema if needed>
**Constraints:** <don'ts, phrased as do's>
**Example (optional):** <one sample of desired output>
```

## Meta-Note: This Guide Writes Itself

Your own agent profiles (`soul-collection/*.md`) are prompts. The best way to practice prompt writing is to audit your SOUL files against the checklist above — role stated, task scope, format, constraints, iteration history. Every guide in this vault was produced through this exact craft.

## Miscellaneous — the rest of the prompt frameworks

RTF, CO-STAR, and CRISPE above cover the everyday/high-stakes/creative cases. These six are the other widely-used ones — same underlying job (WHO/WHAT/HOW), different emphasis. None is required reading; reach for one when its "best for" matches the task in front of you.

| Framework | Components | Best for | What it adds over RTF |
|-----------|-----------|----------|------------------------|
| **RACE** | Role → Action → Context → Expect | Quick structured prompts, daily default when RTF feels too thin | An explicit "what does good look like" (Expect) field |
| **APE** | Action → Purpose → Expectation | Fastest possible structure — brainstorming, one-off asks | The **Purpose** field — forces a "why," which prevents aimless output |
| **RISEN** | Role → Instructions → Steps → End Goal → Narrowing | Multi-step technical tasks (audits, migrations, code review) | An explicit **Steps** field — stops the model from skipping or reordering a process |
| **RICE** | Role → Instructions → Context → Examples | Anything where output must match a specific style | Built-in **Examples** slot — few-shot beats description (see Techniques above) |
| **CREATE** | Character → Request → Examples → Adjustments → Type → Extras | Detailed creative/brand work, docs that must match a style guide | Examples *and* a dedicated Adjustments pass for edge cases |
| **STOKE** | Situation → Task → Objective → Knowledge → Examples | Domain-expert / analytical tasks where the model needs specialized facts it wasn't trained deeply on | A **Knowledge** field — where you inject the domain context CO-STAR has no slot for |

**Picking one, fast:**
```
Need tone/audience control, nothing fancy?      → CO-STAR (above)
Need a defined process, in order?               → RISEN
Need the model to match a reference style?      → RICE or CREATE
Need domain expertise the model won't have?     → STOKE
Just need speed?                                → APE or RACE
Not sure?                                       → RTF (above) — upgrade only if output isn't specific enough
```

Frameworks compose — borrowing one component into another (e.g. RACE + an explicit Steps list, or CO-STAR + an Examples section) is normal and often better than switching frameworks wholesale. The frameworks are a checklist for "did I give the model everything it needs," not a contract you're locked into.

## Related

- Map: [[00-Writing-Types]]
- Prompts that write human-facing text borrow everything here: [[01-Review-Writing-Guide]], [[02-Storytelling-Guide]], [[03-Media-Script-Guide]], [[04-Wishing-Note-Guide]]

*Written 2026-08-24 from established prompt-engineering knowledge. Note: live search (SearXNG instance up, engines returned empty; fallback backend also empty) was unavailable at write time — frameworks listed are stable, widely documented constructs (RTF, CO-STAR, CRISPE), not invented or recalled from a single source.*

*Miscellaneous section added 2026-08-24 — SearXNG confirmed working after the DNS fix (see [[2026-08-24-searxng-dns-outage-fix]] in home-lab), cross-checked live against gptprompts.ai's prompt-frameworks guide and promplify.ai's framework comparison.*
