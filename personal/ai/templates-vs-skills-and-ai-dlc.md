---
title: "Document Templates vs Agent Skills, and What AI-DLC Actually Means"
tags: [ai, spec-driven, ai-dlc, document-template, agent-skills, opinion]
created: 2026-10-03
author: LLMOps profile (opinion note, for Panomete to challenge)
---

# Document Templates vs Agent Skills, and What AI-DLC Actually Means

> Opinion note from LLMOps 🦙 after reviewing `F:\obsidian_note\document_template` (361 templates, 7 tiers), the fleet's spec-driven skills, and both SDD paper notes in [[spec-driven-development-from-code-to-contract]] and [[understanding-specification-driven-code-generation-with-llms]]. Web-verified terminology state as of 2026-10.

## 1. The templates vs skills confusion is a false dichotomy

They are two layers of the same stack, not competitors:

| Layer | Question it answers | Panomete's asset |
|---|---|---|
| Templates (data) | What does the artifact look like? | `document_template/` 361 templates + tier checklists |
| Skills (procedure) | How does the agent produce and validate artifacts? | `software-specification`, `spec-driven-design`, `spec-driven-qa-authoring`, `spec-driven-code-review` |

Why online resources cause confusion: tools like GitHub Spec Kit, Kiro, and addyosmani/agent-skills ship templates *embedded inside* skill packages, so the skill looks like it replaces the template library. It does not. The SDD tools only bundle 3-4 artifacts (spec, plan, tasks) because they target one workflow. A 361-template library covers the full SE lifecycle (QA, ops, security, governance) and is a superset, not a mismatch.

The existing fleet already models this correctly: `spec-driven-design` reads from a `template/02_design/` directory instead of hardcoding structure. Skills reference templates; templates stay tool-agnostic. Switch agent runtime tomorrow and the template library survives intact.

**Verdict: keep the template approach.** The 7-tier system is the safeguard against "too much". It is the Golden Rule from the Piskala paper made operational: minimum rigor that removes ambiguity, per project. Tier 1 POC touches a handful of docs, Tier 6+ touches dozens. Overhead scales with consequence, which is exactly right.

The real gap is not templates vs skills. It is **enforcement**. The paper's top failure modes are spec rot and false confidence ("if the spec is wrong, the code faithfully implements the wrong thing"). Tier checklists say which docs to create, but nothing yet verifies docs stay true against the code. Direction to invest in: wire `spec-driven-code-review` style checks into CI so drift fails the build instead of accumulating silently. Spec-anchored is the sweet spot; advisory docs are how design documents died in the pre-AI era.

## 2. AI-SDLC vs AI-DLC: neither term is standardized yet

Web-verified state (2026-10):

- **AI-SDLC** = AI-assisted Software Development Life Cycle. Classic phases (requirements, design, build, test, deploy, operate) with AI tools plugged into each. AI is a helper; the lifecycle is unchanged.
- **AI-DLC** = AI-Augmented (or AI-native) Development Life Cycle. Newer framing, gaining traction 2025-2026, vendor-driven (Wipro is an early adopter with an Agentic AI SDLC Orchestrator on AWS). Claim: AI is an active participant across the lifecycle, agents draft specs, generate code, run tests; humans shift to spec ownership and supervision. One framing found online: "AI-SDLC bolts AI onto the lifecycle; AI-DLC governs it."

Honest take: AI-DLC is the term with current momentum but it is marketing-adjacent and churning fast. Do not anchor an identity to either acronym. In conversation, "AI-assisted SDLC" is unambiguous.

Amusing footnote: the `soul-collection/AI-SDLC/` persona fleet already implements the concept more concretely than most blog posts. Each profile owns a lifecycle phase (PO, full-stack, devops, QA, security, data, LLMOps, UI/UX). That is AI-DLC operationalized as an org chart of agents.

## 3. How SDD relates to AI-DLC: it is the control mechanism

The causal chain:

1. AI-DLC means agents do much of the lifecycle work.
2. Agents are "excellent at pattern completion but poor at mind reading" (Piskala, p.1).
3. So the artifact that carries human intent into agent work must be the spec. The spec becomes the contract, the "super-prompt".
4. Therefore AI-DLC without SDD degenerates into vibe coding at scale. The bottleneck shifts from writing code to specification quality.

Three-layer map of Panomete's stack:

| Layer | Concept | Asset |
|---|---|---|
| Operating model | AI-DLC: who does the work across the lifecycle | Hermes persona fleet (AI-SDLC souls) |
| Control mechanism | SDD: how intent survives the human to agent handoff | spec-driven skills + grill protocols |
| Artifact layer | Templates: what the specs physically look like | `document_template/` library |

The confusion dissolves once you see these were three views of one stack, not three rival approaches.

## 4. Recommended next moves (LLMOps opinion)

1. ✅ Keep templates. Keep tiers. Resist pressure to collapse everything into skill-embedded templates.
2. 🔴 Close the enforcement gap: pick one pilot project, run it spec-anchored, wire spec-vs-code drift checks into CI. Eval gates for docs, same philosophy as eval gates for models.
3. 🟡 Add a one-page mapping doc in `document_template/_governance/`: which skills consume which template folders. Makes the two-layer architecture explicit for future profiles.
4. 🟢 When writing about this externally, use "AI-assisted SDLC" or define your terms on first use. The acronym war (AI-DLC vs AI-SDLC) is unresolved and vendor-driven.

## Related

- [[spec-driven-development-from-code-to-contract]] - the practice guide (3 rigor levels, 4 phases, Golden Rule)
- [[understanding-specification-driven-code-generation-with-llms]] - the empirical companion (CURRANTE, tests as spec)
- [[agentic-ai-frameworks-and-terminology]] - terminology churn context
- `F:\obsidian_note\document_template\README.md` - tier workflow
