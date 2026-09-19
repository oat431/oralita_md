---
title: "AI Engineering Vault — Curated Reading List"
date: 2026-09-19
author: LLMOps 🦙
tags: [ai, vault, reading-list, sources, evergreen]
status: draft
---

# AI Engineering Vault — Curated Reading List

> **Purpose:** The canonical sources to build `ai-knowledge/` from. Tiered by priority and mapped to the vault pillars in `[[AI-Engineering-Knowledge-Vault-Proposal]]`.
>
> **Principle:** Core principles churn slowly (textbooks). Frameworks/models/tooling churn fast (web-verify before citing). This list separates them.
> **Verification:** Sources web-checked 2026-09-19. Re-verify editions/versions before buying or citing.

---

## Tier 0 — The Anchor Books (start here, all pillars)

These are the **canonical 2026 texts** — cited across every "best AI engineering books" list and already in your career-path overview as source frameworks.

| Book | Author | Why it's Tier 0 | Vault pillars it seeds |
|---|---|---|---|
| **AI Engineering: Building Applications with Foundation Models** | Chip Huyen (O'Reilly, 2025) | The single best applied-AI-engineering book. Covers RAG, eval, guardrails, inference ops, cost. Your career-path 18 overview already cites it. | `04_Applied_AI_Engineering` (all), `05_AI_Ops`, `06_Governance` |
| **Hands-On Large Language Models** | Jay Alammar & Maarten Grootendorst (O'Reilly) | Best book for *understanding* what you're calling via API — transformers, embeddings, tokenization, capabilities. Bridges fundamentals → applied. | `03_Foundation_Models_and_LLMs`, `04_Applied` |
| **Designing Machine Learning Systems** | Chip Huyen (O'Reilly) | The ML systems engineering classic — data pipelines, serving, monitoring, MLOps. Best for `05_AI_Ops`. | `05_AI_Operations_and_MLOps` |
| **Build a Large Language Model (From Scratch)** | Sebastian Raschka | If you want to *understand* the transformer by building one. Deeper than you need for applied work — use selectively for `03`. | `03_Foundation_Models_and_LLMs` (deep) |
| **LLM Engineer's Handbook** | Paul Iusztin & Maxime Labonne | End-to-end LLM system build — from data to serving. Practical companion to Chip Huyen. | `04_Applied`, `05_AI_Ops` |
| **Prompt Engineering for Generative AI** | James Phoenix & Mike Taylor (O'Reilly) | Best focused book on context/prompt engineering. Maps directly to pillar `04/02`. | `04_Applied/02_Context_and_Prompt_Engineering` |

> **Minimum viable reading set:** Chip Huyen's *AI Engineering* + Jay Alammar's *Hands-On LLMs*. These two alone seed 70% of the applied vault.

---

## Tier 1 — Foundations & Core ML (the slow-churn layer)

| Source | Author | Pillar | Notes |
|---|---|---|---|
| **Mathematics for Machine Learning** | Deisenroth, Faisal, Ong (Cambridge, free) | `01_Foundations` | The canonical bridge book. Linear algebra + probability + optimization + how they meet ML. Free at mml-book.github.io. |
| **Understanding Deep Learning** | Simon Prince (MIT Press, 2024) | `02_Core_ML` | Most current deep-learning textbook. Covers CNNs, RNNs, transformers, diffusion, RL. Reddit's consensus pick for "best modern DL book." |
| **Deep Learning** | Goodfellow, Bengio, Courville (MIT Press) | `02_Core_ML` | The classic "DL Bible." Slightly older but theory still canonical. Use as reference, not primary. |
| **Pattern Recognition and Machine Learning (PRML)** | Christopher Bishop | `02_Core_ML` | The classical ML theory reference. Dense; use selectively when you hit a theory wall. |
| **An Introduction to Statistical Learning (ISLR)** | James, Witten, Hastie, Tibshirani | `02_Core_ML` | Best classical-ML primer (regression, trees, etc.). Free PDF. Pairs with "The Elements of Statistical Learning" for deeper theory. |

> **Foundations strategy:** Don't front-load all of math. Start with ISLR (classical ML) + the MML book's chapters on linear algebra + probability *as you hit walls in applied work*. Front-loading 4 semesters of math you forget without application is the anti-pattern.

---

## Tier 2 — Foundation Models & LLMs (medium-churn bridge layer)

| Source | Type | Pillar | Notes |
|---|---|---|---|
| **The Illustrated Transformer** | Jay Alammar (blog) | `03` | The canonical explainer. Read before any textbook chapter on attention. |
| **LLM Course** | Maxime Labonne (free, GitHub) | `03`, `04` | Practical, current. Models, fine-tuning, evaluation. Pair with his LLM Engineer's Handbook. |
| **Hugging Face NLP Course** | Hugging Face (free) | `03` | Best free intro to tokenization, embeddings, fine-tuning with HF libraries. |
| **OpenAI / Anthropic / Google model docs** | Official | `03`, `04` | Primary source for capabilities, limits, API contracts. Re-verify per model release. |
| **Sebastian Raschka's magazine** | Substack | `03`, `06` | Best independent deep-dive on fine-tuning, LoRA, and "what actually works." |
| **arXiv (cs.CL, cs.LG, cs.AI)** | Papers | `03` | For specific deep dives. Use Semantic Scholar / ar5iv for reading. |

> **Bridge-layer rule:** This layer churns every 6–12 months. Re-verify model names, context lengths, and capabilities before citing in any ADR.

---

## Tier 3 — Applied AI Engineering (fast-churn — web-verify before citing)

| Source | Type | Pillar | Notes |
|---|---|---|---|
| **OWASP Top 10 for LLM Applications (2025)** | Framework | `04/04` | **The** security baseline. Already cited in your career-path 18 overview. |
| **Anthropic: Building Effective Agents** (engineering blog) | Blog | `04/01`, `04/07` | Pragmatic, opinionated. Best short read on "when to build an agent and when not to." |
| **Karpathy on Context Engineering** (X/posts) | Social | `04/02` | Kicked off the "context engineering" paradigm shift in 2026. |
| **promptfoo / DeepEval / Inspect / LangSmith / Braintrust docs** | Docs | `04/03` | Eval frameworks — pick by your stack, re-verify current state before recommending. |
| **Chip Huyen's blog (chiphuyen.com)** | Blog | `04`, `05` | Regular current-practice posts. |
| **Eugene Yan's blog (eugeneyan.com)** | Blog | `04`, `05` | Production ML patterns, evaluation, deployment. High signal. |
| **Hamel Husain's blog** | Blog | `04/03` | Best writing on LLM evaluation practice — "build evals that actually work." |
| **NIST AI RMF + ISO 42001** | Standards | `06` | Governance frameworks. NIST = voluntary US guide; ISO 42001 = market-driven cert. See separate governance tier below. |

> **Fast-churn rule:** Anything in `04_Applied_AI_Engineering/` must be web-searched before you cite it in an ADR or recommend it to a stakeholder. "It works on my examples" is the most expensive sentence in AI engineering.

---

## Tier 4 — AI Operations & MLOps

| Source | Author/Type | Pillar | Notes |
|---|---|---|---|
| **Designing Machine Learning Systems** | Chip Huyen | `05` | Already in Tier 0. The MLOps infrastructure reference. |
| **LLM Engineer's Handbook** | Iusztin & Labonne | `05` | Already in Tier 0. End-to-end LLM system build. |
| **vLLM / SGLang / TensorRT-LLM docs** | Official | `05/02` | Serving infrastructure. Churns fast — verify before citing. |
| **Weights & Biases / MLflow / DVC docs** | Official | `05/03` | Experiment tracking + model registry. |
| **Hugging Face Hub** | Platform | `05` | Model discovery, datasets, spaces. |
| **Google SRE Book + Site Reliability Engineering** | Google | `05/04` | Reliability grounding — applies to AI serving. |

---

## Tier 5 — Governance & Responsible AI

| Source | Type | Pillar | Notes |
|---|---|---|---|
| **NIST AI Risk Management Framework (AI RMF)** | US gov framework | `06/01` | Voluntary, no penalty. The governance operating model baseline. |
| **ISO/IEC 42001:2023** | Standard | `06/01` | AI management system standard. Market-driven certification. |
| **EU AI Act** | Regulation | `06/04` | First major AI regulation. Risk-tiered (unacceptable/high/limited/minimal). If shipping to EU, mandatory. |
| **OWASP LLM Top 10 (2025)** | OWASP | `04/04` + `06` | Already Tier 3. The security-governance bridge. |
| **Model Cards for Model Reporting** | Mitchell et al. (paper) | `06/03` | The original model card format. Your career-path 18/06/03 note is built on this. |
| **Co-Intelligence** | Ethan Mollick | `06` (context) | Best non-technical "what AI means for work" book. Good for stakeholder communication (capability 8). |
| **AI Engineering (Governance chapters)** | Chip Huyen | `06` | Already Tier 0. Covers responsible AI, compliance, ROI. |

---

## Tier 6 — Specialized Domains (build on demand)

Only build these when a real project demands it — don't front-load.

| Domain | Best starter source | Pillar |
|---|---|---|
| **NLP deep dive** | Speech and Language Processing (Jurafsky & Martin, free online) | `07/01` |
| **Computer Vision** | Deep Learning for Computer Vision (PyImageSearch / Adrian Rosebrock) | `07/02` |
| **Speech/Audio** | AudioCraft / MusicGen docs + ESPnet docs | `07/03` |
| **Multimodal** | LLaVA paper + CLIP paper + model-specific docs | `07/04` |
| **AI for Code/SE** | GitHub Copilot research + coding agent literature (Claude Code, Cursor) | `07/05` |

---

## Tier 7 — Practitioner Notes (your own — no external source)

This pillar is your own working knowledge. Sources are *your* projects:

- `08/01_ADRs/` — every consequential AI decision (pattern, model, provider) gets a decision record
- `08/02_Eval_Suites/` — actual eval designs with golden sets + results
- `08/03_Postmortems/` — production model failures, abuse incidents, cost overruns
- `08/04_Tooling_Reviews/` — current-state reviews of frameworks, re-verified before citing

> **Rule:** A practitioner note is only trustworthy if it has a real system behind it. Don't write "how to build a RAG system" as a practitioner note until you've *built and shipped one*. Use the other tiers for theory; use Tier 7 for war stories.

---

## Reading Order (recommended path through the tiers)

**If you're an applied engineer (you are):**

```
Tier 0: AI Engineering (Huyen) → Hands-On LLMs (Alammar)
   ↓  [you now have enough to build]
Tier 3: OWASP LLM Top 10 → Anthropic Building Effective Agents → Hamel Husain evals
   ↓  [you now ship safely]
Tier 0: Designing ML Systems (Huyen) → LLM Engineer's Handbook
   ↓  [you now operate it]
Tier 2: Illustrated Transformer → HF NLP Course → Maxime Labonne course
   ↓  [you now understand the bridge layer]
Tier 1: ISLR → MML book (selective) → Understanding Deep Learning (selective)
   ↓  [you now have the foundations, built on demand]
Tier 5: NIST AI RMF → EU AI Act → model cards
   ↓  [you now govern]
Tier 7: your own ADRs, eval suites, postmortems
   ↓  [ongoing]
```

**If you want the foundations first (alternative path):**

```
Tier 1: ISLR → Understanding Deep Learning → MML book (selective)
   ↓
Tier 2: Illustrated Transformer → HF NLP Course
   ↓
Tier 0: AI Engineering (Huyen) → Hands-On LLMs (Alammar)
   ↓
[continue as above]
```

> I recommend the applied-first path. You're an applied engineer with a working stack — foundations built on demand stick better than front-loaded theory. Same principle as "build the eval suite, the code is secondary."

---

## Source Verification Log

| Source | Verified | Status |
|---|---|---|
| Chip Huyen — AI Engineering | 2026-09-19 | Current (O'Reilly 2025), consensus #1 pick |
| Jay Alammar — Hands-On LLMs | 2026-09-19 | Current O'Reilly title |
| Sebastian Raschka — Build a LLM (From Scratch) | 2026-09-19 | Current |
| Maxime Labonne — LLM Course | 2026-09-19 | Active, free, GitHub-hosted |
| Mathematics for Machine Learning (mml-book) | 2026-09-19 | Free, stable, canonical |
| Understanding Deep Learning (Prince) | 2026-09-19 | Current MIT Press title, Reddit consensus |
| OWASP Top 10 for LLM Applications | 2026-09-19 | 2025 edition current |
| NIST AI RMF | 2026-09-19 | Active, voluntary framework |
| ISO/IEC 42001 | 2026-09-19 | 2023 standard, current |
| EU AI Act | 2026-09-19 | In force; phased application |

> **Re-verify cadence:** Tier 0 books = yearly (new editions). Tier 3 sources = per-citation. Tier 5 frameworks = on amendment.

---

## What I Deliberately Excluded (and why)

- **"AI for Everyone" type mass-market books** — not engineering depth. Skip unless you need talking points for non-technical stakeholders.
- **Online course certificates (Coursera, etc.)** — the books + practice cover the same ground; certificates are for résumés, not knowledge.
- **Specific model names (GPT-x, Claude x, Gemini x)** as sources — they're products, not knowledge. Model capabilities go in `03/04_Capabilities_and_Limits` and are re-verified per release.
- **"100 prompts that will change your life" content** — prompt-engineering-as-hacks. The vault is about *engineering*, not prompt collections.
- **Most "AI thought leaders" on social media** — high noise. Karpathy and a small handful are worth following; the rest is derivative.

---

*Curated by LLMOps 🦙 — 2026-09-19. Sources web-verified on date shown. This list is a living document — add sources as you read, re-verify before citing in production work.*
