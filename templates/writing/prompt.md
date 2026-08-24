---
date: 2026-08-24
tags: [writing, template, prompt]
---

# Prompt Templates

> Fill-in masters for AI prompts. Copy ONE block, fill the brackets, run. Frameworks & techniques explained: [[05-Prompt-Writing-Guide]].
>
> **Language-neutral by design:** the structure steers any model in any language — but write the prompt in the language the model is strongest at for the task, and demand output in your audience's language.

## RTF — everyday prompts (daily driver)

```markdown
Role: <only if it helps — "senior backend engineer reviewing a PR">
Task: <ONE imperative verb + the deliverable — "summarize", "rewrite", "compare">
Format: <bullet list / JSON / 300 words / markdown table / checklist>
```

**Filled example**

```markdown
Role: senior DevOps engineer
Task: rewrite my homelab runbook section so a beginner can follow it
Format: numbered steps, each command explained in one line, pitfalls as a checklist
```

## CO-STAR — high-stakes, multi-constraint

```markdown
Context: <what the model must know to not guess — background, situation, constraints>
Objective: <the ONE outcome>
Style: <reference or style description>
Tone: <register — direct / friendly / formal>
Audience: <who consumes the output>
Response format: <shape of the answer — structure, length, schema>
```

**Filled example**

```markdown
Context: This is a personal finance plan for a 25-year-old in Thailand,
32K THB/month income, ~20K fixed expenses, emergency fund is the priority.
Objective: produce a monthly savings allocation plan.
Style: concise, practical, no theory.
Tone: direct, no fluff, no hype.
Audience: the user, who executes the plan hands-on.
Response format: markdown table with amounts + reasoning per bucket,
ending with a 3-item "first moves" checklist.
```

## CRISPE — creative work with variations

```markdown
Act as <CAPACITY/ROLE> with expertise in <INSIGHT — domain knowledge to draw on>.
Your task: <STATEMENT — the assignment, with the creative brief>.
Match my style: <PERSONALITY — tone, voice, constraints>.
Then: <EXPERIMENT — give N variations / ask before proceeding / rank options>.
```

**Filled example**

```markdown
Act as a copywriter with expertise in Thai-English bilingual marketing.
Your task: write 3 opening lines for a birthday wish to a close friend —
specific, grounded, no clichés.
Match my style: warm, casual, one Thai-English mix allowed.
Then: rank the 3 by emotional impact and explain each pick in one line.
```

## Structured output — machine-readable (JSON)

```markdown
Task: <the extraction / conversion job>
Input: <the content to process>
Return JSON exactly in this shape:
{
  "title": "string",
  "summary": "string",
  "tags": ["string"],
  "rating": number
}
Rules: only valid JSON, no markdown fences, no commentary outside the JSON.
```

## Quick Check (before hitting run)

- [ ] One imperative verb, one job — split if two verbs
- [ ] Format specified — the model should never choose its own
- [ ] Context present — what does it need to know to not guess?
- [ ] Audience + tone stated when the output is human-facing
- [ ] Negative constraints phrased as positives ("plain text, no decorations")
- [ ] If output disappoints: fix one thing, rerun — don't rewrite from scratch

## Related

- Framework theory & failure modes: [[05-Prompt-Writing-Guide]]
- Prompts that produce writing borrow the craft targets: [[01-Review-Writing-Guide]] [[02-Storytelling-Guide]] [[03-Media-Script-Guide]] [[04-Wishing-Note-Guide]]
- Agent profiles are long-form prompts — audit yours against the checklist above
