---
title: "The AI Buzzword Map (Q4 2026): Every 'Buff Word', Sorted Honestly"
date: 2026-09-21
author: LLMOps 🦙
tags: [ai, agents, llm, buzzwords, terminology, reference]
status: living
---

# The AI Buzzword Map (Q4 2026)

> **Companion to:** [[agentic-ai-frameworks-and-terminology]] (Part 8 covered the "-X engineering" family - this note maps *everything else*).
> **Question this answers:** "What other buff words exist around AI / agentic / LLM - and which ones are real?"
> **Method:** Every term web-verified 2026-09-21. Status labels below are my honest calibration, not vendor copy.

---

## The Meta-Pattern: Jargon Arrives in Waves

Before the list - the single most useful observation: **AI terminology doesn't appear one word at a time. It emerges in recognizable families/waves.** Once you see the pattern, you can predict and evaluate new words on sight.

| Wave                  | Family           | Examples                                                                           | Era       |
| --------------------- | ---------------- | ---------------------------------------------------------------------------------- | --------- |
| **Engineering stack** | "-X engineering" | prompt -> context -> harness -> loop -> graph engineering                          | 2023-2026 |
| **Agentic wave**      | "agent-*"        | agents, subagents, agent skills, ambient agents, agentic RAG, agentic commerce, AX | 2024-2026 |
| **Slop family**       | "slop*"          | AI slop, slopaganda, slopsquatting                                                 | 2024-2026 |
| **Washing family**    | "-washing"       | AI washing, agent washing                                                          | 2024-2026 |
| **Maxxing family**    | "-maxxing"       | tokenmaxxing                                                                       | 2025-2026 |
| **Frontier/econ**     | "AI + noun"      | AI capex, neoclouds, inference economics, physical AI                              | 2025-2026 |

> **Why this matters:** when a new word appears, ask "which family is it in?" A new "-washing" term is a criticism of marketing. A new "-engineering" term claims a discipline. A new "agent-*" term claims a capability. The family tells you the intent before the definition.

---

## Status Legend (my honest labels)

| Label | Meaning | How to treat it |
|---|---|---|
| ✅ **Standard** | Established, real, safe in engineering contexts | Use freely |
| 🟢 **Emerging but real** | Genuine concept, still settling | Use with care; verify currency |
| 🟡 **Marketing** | Mostly hype; the underlying thing may be real but the word oversells | Translate before trusting |
| 🔴 **Culture / criticism** | Not an engineering term - but literacy matters | Understand, don't deploy in design docs |

---

## Category 1: Agentic Wave (the "agent-*" family)

| Term | What it means | Status | Notes |
|---|---|---|---|
| **Agentic AI** | Systems that decide and act in loops, not just respond | ✅ Standard (but 🔴 cooling as hype) | Hype trackers now list "agentic" as *overused*. The concept is real; the word is tired. |
| **Subagents** | Delegated worker agents spawned by a parent agent; constructed from skill packages | 🟢 Real | "The new unit of coding automation." Cursor/Claude Code ship them; arXiv papers analyze them. |
| **Agent Skills** | Organized folders of instructions/scripts/resources an agent loads dynamically when relevant | 🟢 Real | Coined by Anthropic (Oct 2025). Solves context bloat - load only when needed. You use the same pattern: Hermes skills. |
| **Computer use / Browser use** | Agent directly operating a computer (GUI, browser) | 🟢 Real | Distinct from API tool use; measured by OSWorld/WebArena. |
| **Ambient agents** | Event-triggered, background agents that run proactively - but *not* fully autonomous | 🟢 Emerging | Microsoft definition: triggered by events, run in background, human stays in control. |
| **Agentic RAG** | Multi-turn retrieval: the agent iteratively refines queries based on intermediate results | 🟢 Real | "Vanilla RAG" (single-shot retrieval) is now the legacy baseline. |
| **Deep research** | Multi-step research agent pattern (advanced RAG at its core) | 🟢 Real | Productized by OpenAI/Google/Perplexity; the pattern behind "research agents." |
| **Agent Experience (AX)** | Designing products/APIs for agents as *users* (not humans) | 🟢 Emerging | Coined by Matt Biilmann (Netlify CEO), early 2025. Triad: AX / UX / DX. |
| **Agent teams / swarms** | Many agents cooperating as a unit | 🟡 Mixed | Real for some workloads; heavily over-sold. Usually one agent + tools wins. |
| **"Year of the agent"** | Marketing phrase for the agent era | 🟡 Marketing | Already cooling in hype trackers. Ignore. |
| **Human-in-the-loop (HITL)** | Human approval gates inside agent workflows | ✅ Standard | Non-negotiable for high-risk actions. |

---

## Category 2: Model & Training Vocabulary

| Term | What it means | Status | Notes |
|---|---|---|---|
| **Reasoning models** | Models trained to "think before answering" - long internal chain-of-thought first | ✅ Standard | Also called "thinking models." Spend tokens on deliberation. |
| **Test-time compute** | Spending more compute at inference to get better answers | ✅ Real (🟡 cooling as hype) | Legit research direction; the *word* got over-hyped, the technique didn't. |
| **Context rot** | Measurable performance degradation as context grows - gradual, continuous, not a cliff | 🟢 Real & important | Distinct from **lost-in-the-middle** (a *position* failure; context rot is a *length* failure). Both bite long-context agents. |
| **Lost in the middle** | Models attend poorly to information in the middle of long contexts | ✅ Classic | The position-failure half of long-context problems. |
| **Long context degradation** | The formal name for context rot | ✅ Academic | Use when you want the paper-searchable term. |
| **MoE (Mixture of Experts)** | Architecture: route each token to a subset of "expert" subnetworks | ✅ Standard | Why big models can be cheap to serve. |
| **Post-training** | Everything after pretraining: SFT, RLHF, DPO, GRPO | ✅ Standard | The umbrella term for alignment work. |
| **RLHF / DPO / GRPO** | Alignment methods (human feedback / preference optimization / group-relative) | ✅ Standard | RLHF = classic; DPO = simpler; GRPO = the 2025-26 training favorite. |
| **Distillation** | Training a small model to mimic a big one | ✅ Standard | The economics behind cheap capable small models. |
| **Synthetic data** | Training data generated by models | ✅ Standard | Now a mainstay; watch for **model collapse**. |
| **Model collapse** | Degradation from training on too much self-generated data | 🟢 Real risk term | The failure mode of synthetic-data loops. |
| **World models** | Models that learn a simulation of an environment | 🟢 Emerging | Genie-style research; adjacent to robotics. |
| **Physical AI** | AI in robots/machines acting in the physical world | 🟢 Emerging | Hype tracker lists it as a *riser*. "Sounds like a buzzword, but..." |
| **Omni-modal / multimodal** | Models handling text+image+audio+video natively | ✅ Standard | "Omni" is the newer, fancier prefix. |

---

## Category 3: Security Vocabulary

| Term | What it means | Status | Notes |
|---|---|---|---|
| **Lethal trifecta** | The three capabilities that make an agent trivially exploitable: **private data + untrusted content + external communication** | 🟢 Real & essential | Coined by Simon Willison (June 2025) - the same person who coined "prompt injection." If your agent has all three, assume it's exploitable. |
| **Prompt injection** | Hostile input manipulates the model | ✅ Standard (unsolved) | Covered in [[applied-ai-concepts-q4-2026]]. |
| **Slopsquatting** | Registering packages under names AI hallucinated, so agentic installs fetch malware | 🟢 Real & rising | Open models hallucinate package names **21.7%** of the time vs 5.2% commercial (2026 data). Agentic systems *removed the human checkpoint* - the attack got worse. |
| **Jailbreak** | Bypassing a model's safety training | ✅ Standard | Consumer-facing concern; red-team target. |
| **Red teaming** | Adversarially probing AI systems for failures | ✅ Standard | Baseline practice before launch. |
| **Guardrails** | Input/output filtering + fallback layers | ✅ Standard | Covered in the vault. |
| **Zero trust (for AI)** | Applying zero-trust principles to agent access | 🟢 Emerging | Zscaler et al. framing lethal trifecta as "what zero trust was built to stop." |

---

## Category 4: Culture & Criticism (the slop / washing / maxxing families)

These aren't engineering terms - but you need the vocabulary to read the discourse without being fooled.

| Term | What it means | Status | Notes |
|---|---|---|---|
| **AI slop** | Low-effort, high-volume AI-generated content | ✅ Established (culture) | Wikipedia + Britannica entries. The defining content-criticism word of the era. |
| **Slopaganda** | AI slop + propaganda | 🟢 Emerging | Portmanteau; "a lexically perfect summary of the world in 2026." |
| **Tokenmaxxing** | Maximizing token consumption (by orgs or individuals) - wasting costly AI resources to look AI-native | 🟢 Real criticism | Forbes: "foolishly inspiring employees to waste costly AI resources." The anti-pattern twin of cost engineering. |
| **AI washing** | Rebranding ordinary products as "AI" without substance | ✅ Real | The SEC has pursued AI-washing fraud. |
| **Agent washing** | Same, but for "agents" - rebranded chatbots/scripts sold as agents | 🟢 Real (Gartner term) | "95% of AI agents aren't real" (industry reports). Use as a diligence checklist when buying. |
| **Vibe coding** | Writing code by describing intent and accepting AI output largely unread | ✅ Established (Karpathy) | Legit for prototypes; the pushback: real AI-assisted dev is "a deeply intellectual exercise." |
| **Enshittification** | Platforms degrading to extract value | 🔴 Culture (older) | Cory Doctorow's term - now applied to AI platforms too. |
| **AGI-pilled / doomer / e/acc** | Belief-camp labels (expecting AGI soon / fearing it / accelerating it) | 🔴 Culture | Know them to navigate discourse; they're identity labels, not engineering terms. |

---

## Category 5: Business & Economics Vocabulary

| Term | What it means | Status | Notes |
|---|---|---|---|
| **AI capex (bubble)** | The trillion-dollar infrastructure buildout - and the debate about whether it pays back | 🟢 Real (trending) | $2T cumulative hyperscaler+neocloud commitments; the #1 hype-riser of 2026. |
| **Neoclouds** | GPU-focused cloud providers (vs hyperscalers) | 🟢 Real | The category serving AI compute demand. |
| **Inference economics** | The unit economics of serving models (tokens, GPUs, margin) | ✅ Real | Where AI products live or die commercially. |
| **Token economics** | Cost/latency per token as a design constraint | ✅ Real | Covered in the vault (cost optimization). |
| **AI ROI** | Whether AI spend returns value | ✅ Real | The question every CFO asks in 2026. |

---

## The Buzzword Test (use on ANY new word)

When you meet a new term, run these three checks before adopting it:

1. **The failure-mode test**: can the person using it explain *what fails* when that thing is done wrong? (No failure mode = marketing.)
2. **The artifact test**: does it produce a measurable artifact (a doc, a metric, a system change)? ("Context engineering" produces context budgets; "agentic" alone produces nothing.)
3. **The design-review test**: would a senior engineer use this word in a design review without embarrassment? (If it only sounds good in a keynote, it fails.)

And the lifecycle to expect: **coin -> hype -> overuse -> cool -> either standardize or die.** Most words in this map are mid-lifecycle. A few ("prompt injection," "RAG," "guardrails") standardized. Many ("agentic," "year of the agent") are cooling. That's normal - judge the concept, not the fashion.

---

## Thai Speaker Traps (buzzword edition)

⚠️ **"Agentic"** != มีตัวแทน = ลักษณะของระบบที่ตัดสินใจและลงมือทำเองในลูป
⚠️ **"Slop"** = ขยะคอนเทนต์ที่ AI สร้าง (ไม่มีคำไทยตรงตัว - ใช้ทับศัพท์ได้)
⚠️ **"Vibe coding"** != การเขียนโค้ดแบบมีสไตล์ = การให้ AI เขียนโค้ดตามคำอธิบายโดยไม่ตรวจละเอียด
⚠️ **"Washing"** (AI washing / agent washing) != การล้าง = การแปะป้าย AI โดยไม่มีของจริง
⚠️ **"Tokenmaxxing"** != การสะสมโทเคน = การใช้โทเคนให้เปลืองเพื่อให้ดูเป็น AI-first

---

## Quick Index (A-Z for lookup)

- Agent Skills 🟢, Agent washing 🟢, Agentic AI ✅/🔴, Agentic commerce 🟢, Agentic RAG 🟢, Agent Experience (AX) 🟢, AI capex 🟢, AI slop ✅, AI washing ✅, Ambient agents 🟢
- Computer use 🟢, Context rot 🟢, Deep research 🟢, Distillation ✅, Enshittification 🔴
- HITL ✅, Inference economics ✅, Jailbreak ✅, Lethal trifecta 🟢, Long context degradation ✅, Lost in the middle ✅
- Model collapse 🟢, MoE ✅, Neoclouds 🟢, Omni-modal ✅, Physical AI 🟢, Post-training ✅, Prompt injection ✅
- Reasoning models ✅, Red teaming ✅, RLHF/DPO/GRPO ✅, Slopaganda 🟢, Slopsquatting 🟢, Subagents 🟢, Synthetic data ✅
- Test-time compute ✅/🟡, Token economics ✅, Tokenmaxxing 🟢, Vibe coding ✅, World models 🟢, Zero trust for AI 🟢

---

## Related Notes

- [[agentic-ai-frameworks-and-terminology]] - frameworks, protocols, harnesses, and the "-X engineering" stack
- [[applied-ai-concepts-q4-2026]] - the 7 concepts that matter in production
- ai-knowledge vault: `04_Applied_AI_Engineering/` - where the real terms become practice

## Sources (verified 2026-09-21)

- Fred Pelard - AI Hype tracker (risers/coolers: AI capex, Evals, AI slop, Physical AI, Lethal trifecta / Agentic AI, Test-time compute)
- alignify.co - AI Terminology Batch Emergence (jargon waves analysis)
- Simon Willison - The lethal trifecta (June 2025); Zscaler, Unihackers - lethal trifecta analyses
- Anthropic Engineering - Agent Skills (Oct 2025); arXiv 2609.09233 - Subagents vs Agent Skills
- zdnet - ambient agents definition (Microsoft); traversaal - ambient agents product design
- ipullrank / Milvus / arXiv 2605.27123 - agentic RAG; Yahoo Finance / chatbotx - agentic commerce 2026
- tmls.nyc / lyzr / Salesforce / morphllm - context rot; understandingai - context rot origin
- CSA Labs / TechTarget / particula - slopsquatting; Wikipedia/Britannica - AI slop; TheJournal.ie - slopaganda
- Forbes - tokenmaxxing criticism; LinkedIn / fin.ai - agent washing; Gartner - agent washing
- pixelmojo / Tarik Davis / LinkedIn - Agent Experience (AX), Matt Biilmann coinage
- Medium - neocloud economy; Exponential View - State of the AI Economy 2026 ($2T capex)

---

*Authored by LLMOps 🦙, 2026-09-21. All terms web-verified on date shown. Buzzwords churn weekly - re-check before citing in an ADR; judge the concept, not the fashion.*
