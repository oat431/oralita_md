---
date: 2026-08-24
tags: [audit, prompt, ai]
piece: "[[00_example]]"
auditor: journey-writer
---

# Audit — `prompt/00_example` (home-lab backup/DNS/security prompt)

> Audited 2026-08-24 against [[05-Prompt-Writing-Guide]]. Contract: problems first · cited evidence · `[objective]` vs `[taste]`.

## Summary Judgment

A real, reasonable need — home-lab backups, DNS, and security are genuinely related hygiene tasks — wrapped in a prompt that skips all three of the guide's jobs (WHO/WHAT/HOW) at once. This isn't a bad idea badly worded; it's three separate prompts bundled into one, wearing a generic persona, with no format demanded. The model will guess your setup, split attention across three asks, and hand back a wall of text matching none of them well.

## The Three Jobs Compliance

| Job | Status | Note |
|-----|--------|------|
| WHO | ⚠️ | "You are an expert" — expert in *what*? Persona abuse (failure mode #6): a title with no domain steers nothing |
| WHAT | ❌ | Three tasks bundled — set up backups, check DNS, review security — no single imperative verb |
| HOW | ❌ | "detailed and professional" describes a *tone*, not a format — no structure, length, or schema requested |

## Problems (cited)

1. **[objective] Persona abuse.** "You are an expert" is the guide's own named failure mode #6 verbatim — "'you are a world-class expert' on every prompt dilutes actual instruction." Compare the guide's own good example: "You are a senior DevOps engineer" — domain-specific, actionable. This prompt's persona is neither.
2. **[objective] Three jobs in one prompt.** Backups, DNS review, and security review are each their own task with their own evidence needs. The guide: "One job per prompt — a prompt doing two tasks makes the model split attention. Split it." This bundles three; expect shallow coverage on all of them, not thorough coverage on any.
3. **[objective] Vague verb.** "Help me with my home lab" is the guide's exact banned phrase, unchanged, for failure mode #1 ("'help me with my review' vs 'rewrite my review: add one weakness paragraph...'"). No task-specific imperative verb anywhere in the prompt.
4. **[objective] Missing context.** No container list, no current DNS provider/software, no existing backup state. Failure mode #3, and avoidable for free — `home-lab/` already holds this setup info; none of it made it into the prompt, so the model must invent your infrastructure before it can advise on it.
5. **[objective] No output format.** "Make it detailed and professional" is tone, not shape. Failure mode #2 — expect the model to pick its own structure, which usually means an undifferentiated wall of text across three unrelated topics.

## What Works

- **The underlying ask is sound and scoped to something real** — this isn't a vague "help me" with no actual task behind it; backups/DNS/security genuinely belong on one homelab-hygiene checklist, they just don't belong in one *prompt*.

## Fix Priority (next draft)

1. Split into three prompts (or three clearly separated, individually-formatted sections)
2. Replace "You are an expert" with a domain-specific persona: "You are a homelab sysadmin familiar with Docker and DNS" — or drop the persona line entirely
3. Paste actual context: container list, DNS provider, current backup state (or point at the relevant `home-lab/` note directly)
4. Replace "detailed and professional" with a real format: e.g. "numbered steps, each with the command and a one-line reason"
5. Given this feeds real infrastructure decisions, this is exactly the guide's "high-stakes, multi-constraint" case — upgrade to CO-STAR instead of writing it free-form: state one Objective per prompt, Audience ("me, executing by hand"), and an explicit Response format

## Auditor's Meta-Note

Seed example for this practice loop — written to demonstrate the audit, not pulled from a prompt actually sent. Replace with a real one whenever there's one worth auditing; the folder and format are ready either way.
