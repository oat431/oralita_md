---
title: "AI Tools Landscape (Q4 2026): Routers, Harnesses, and Assistant Platforms"
date: 2026-09-22
author: LLMOps 🦙
tags: [ai, tools, routers, harnesses, agents, reference]
status: living
---

# AI Tools Landscape (Q4 2026): Routers, Harnesses, and Assistant Platforms

> **Your question:** You know Codex, Claude Code, Antigravity - then you landed on OpenRouter, 9Router, Hermes Agent, OpenClaw. Some are "harnesses", but what are the others? And what else exists that you have not seen yet?
> **Short answer:** Most of the confusion is a **layer problem**. Models are engines. **Routers** (OpenRouter, 9Router) are plumbing that moves requests to engines. **Harnesses** (Claude Code, Codex, Antigravity) are the agent loops you work inside. **Assistant platforms** (Hermes Agent, OpenClaw) are persistent personal agents that can drive harnesses. Once you know the layer, every new tool instantly has a place.
> **Verification:** All facts web-checked 2026-09-22. This layer churns fast - re-verify names, prices, and versions before citing in an ADR.

---

## 1. Your list, classified 🧭

| Tool | Layer | One-liner |
|---|---|---|
| Codex | Harness | OpenAI coding agent: local CLI + cloud agent in ChatGPT |
| Claude Code | Harness | Anthropic terminal coding agent (see [[claude-code-setup]]) |
| Antigravity | Harness platform | Google agentic dev platform: IDE + CLI + SDK + command center |
| OpenRouter | Router (cloud) | One API key, 500+ models, pay per token |
| 9Router | Router (local) | Between your coding tools and 60+ providers, 3-tier fallback |
| Hermes Agent | Assistant platform | The tool we are using right now: memory, skills, cron, channels |
| OpenClaw | Assistant platform | Open-source personal assistant on your machine, messaging-first |

**Short answer for the routers:** OpenRouter and 9Router are **not harnesses**. They never run an agent loop and they never "think". A harness decides *what* to send; a router decides *where* it goes - with which key, which fallback, and which budget.

## 2. The one-picture map 🗺️

| Layer | Job | Examples | Analogy |
|---|---|---|---|
| Model | Generate tokens | GPT, Claude, Gemini, Qwen, DeepSeek, GLM | Engine |
| Router / gateway | Move requests to models and providers | OpenRouter, 9Router, LiteLLM, Portkey, ClawRouter | Fuel line + adapter |
| Harness | Run the agent loop: tools, context, permissions | Claude Code, Codex, Antigravity, Cursor, Cline | The car |
| Assistant platform | Persistent agent: memory, skills, schedules, channels | Hermes Agent, OpenClaw | Garage + butler |

**The layer test (3 questions):**

1. Does it generate tokens itself? -> **Model**
2. Does it run a loop where the model decides what to do next? -> **Harness** (or **assistant platform**, if it also has memory, schedules, and channels)
3. Does it only move requests between tools and models? -> **Router / gateway**

The layers are independent. You can swap any one without touching the others. That is the whole point.

## 3. Routers and gateways: the plumbing layer 🔌

### Why routers exist (the five jobs)

1. **One credential, many models** - stop juggling six API keys and six billing dashboards
2. **Failover** - provider down, or quota hit? Route to another one
3. **Cost control** - budgets, quotas, live usage; send cheap jobs to cheap models
4. **Format translation** - OpenAI, Anthropic, and Gemini APIs speak different dialects; a router normalizes them
5. **Observability** - one place to see spend and usage

### Two families

**Cloud routers (hosted service, pay per token):**

- **OpenRouter** - the mainstream one. 500+ models, 80+ providers, 400T+ tokens per month, 10M+ users (per openrouter.ai, Sep 2026). One API key, no subscription, automatic fallback between providers serving the same model. **Presets** = config-as-code for calls: a named, versioned set of model + system prompt + routing + sampling. This is the router for apps and scripts.
- **Vercel AI Gateway / Cloudflare AI Gateway** - managed gateways with edge caching and analytics. Fast onboarding, nothing to operate, but traffic goes through the vendor network.
- **Portkey** - gateway with guardrails and observability, production-focused.

**Local / self-hosted routers (run on your machine or server):**

- **9Router** - a smart gateway between your *tools* (Claude Code, Codex, Cursor, Cline, Copilot, OpenClaw, Hermes, Antigravity...) and 60+ providers. Runs locally as an OpenAI-compatible endpoint at `localhost:20128`.
  - **3-tier fallback:** subscription quotas first (Claude Code, Codex, Gemini, Copilot) -> cheap tier (GLM, MiniMax, Kimi) -> free tier (iFlow, Qwen, Kiro, OpenCode). "Never stop coding when limits hit."
  - **Extras:** format translator, multi-account round-robin, live quota tracking, RTK + Caveman token savers (claim 20-65%), and an MITM bridge that intercepts Antigravity / Copilot / Kiro IDE traffic. The MITM part is powerful but gray - mind each tool's policy.
  - **Install:** `npm install -g 9router` (npm = Node package manager; `-g` installs it globally so the `9router` command works anywhere), then run `9router` and a dashboard opens.
  - **Honest label:** community project (github.com/decolua/9router). Practical, not enterprise.
- **LiteLLM** - the open-source standard proxy. 100+ LLMs behind one OpenAI-compatible API, with virtual keys, budgets, and fallbacks. Self-host when you want full control.
- **ClawRouter** - OpenClaw's bundled router: self-hosted, OpenAI-compatible, with pay-per-call billing on the hosted option. Enabled by default in OpenClaw (`openclaw plugins enable clawrouter`).

### Quick comparison

| | OpenRouter | 9Router | LiteLLM |
|---|---|---|---|
| Shape | Cloud service | Local process | Self-hosted server |
| Built for | Apps and scripts | Coding tools + your subscriptions | Teams and production apps |
| Credentials | OpenRouter account with credits (pay per token) | Your own provider keys and subscriptions | Your own keys |
| Killer feature | 500+ models, one key, fallbacks | 3-tier subscription fallback, token savers | Budgets, virtual keys, full control |

### Where it fits (LLMOps read) 🎯

Routers are **inference operations** infrastructure: exactly the "model routing" capability from [[applied-ai-concepts-q4-2026]]. Treat routing policy (which model for which job, fallback order, cost caps) as a designed artifact, not a default.

## 4. Harnesses: the coding agents 🚗

| Tool | Maker | Surface | Notes |
|---|---|---|---|
| Claude Code | Anthropic | Terminal CLI | The reference harness; setup notes in [[claude-code-setup]] |
| Codex | OpenAI | Local CLI + cloud | Open-source CLI; cloud agent inside ChatGPT, built for multi-agent workflows |
| Antigravity | Google | IDE + CLI + SDK | Agentic dev platform: 2.0 command center (parallel local agents, Projects, scheduled messages), terminal-first CLI with background subagents, SDK to build custom agents on their harness |
| Gemini CLI | Google | Terminal | Lightweight terminal agent |
| Cursor | Cursor | IDE | AI-native code editor |
| Cline, Roo Code, Kilo Code, Continue | community | VS Code extensions | Bring-your-own-key agents inside VS Code |
| OpenCode | community | Terminal | Open-source terminal agent with a free usage tier |
| Factory Droid | Factory | Terminal + enterprise | Agent for enterprise workflows |
| Kiro | AWS | IDE | Agentic IDE |
| GitHub Copilot | GitHub | IDE and beyond | The incumbent assistant, now agentic |

Key insight from [[agentic-ai-frameworks-and-terminology]]: **the harness matters more than the model.** Same model in different harnesses = very different results. "Which coding tool?" is a better question than "which model?".

## 5. Assistant platforms: the persistent agents 🏠

These are not just coding tools. They are always-on personal agents.

- **Hermes Agent** (Nous Research) - the tool we are talking in right now. Open-source agent runtime: memory across sessions, reusable skills, cron jobs, subagents, terminal + dashboard + messaging channels. Bring your own model (any provider, e.g. OpenRouter or DashScope). Supports profiles for different jobs.
- **OpenClaw** (formerly Clawdbot, then Moltbot) - open-source personal AI assistant that runs on your machine and works from WhatsApp, Telegram, or any chat app. Channels, agents, skills (ClawHub), gateway and ops. Bundles ClawRouter for model routing.

**What makes a platform different from a harness:**

- **Persistent memory** - it remembers across sessions, not just within one task
- **Skills** - reusable procedures that load on demand
- **Schedules** - cron jobs that run without you
- **Channels** - reachable from chat apps, not just a terminal
- **It can drive harnesses** - spawn Claude Code or Codex as workers / subagents

## 6. How the layers compose (real setups) 🧩

1. **You, now:** Hermes Agent -> provider (OpenRouter / QwenCloud DashScope) -> models. Coding delegated to Claude Code; memory and orchestration live in Hermes.
2. **Limit-maxxer:** Claude Code + Codex -> 9Router (`localhost:20128`) -> subscription tier -> cheap tier -> free tier.
3. **Chat-first assistant:** WhatsApp / Telegram -> OpenClaw -> ClawRouter -> models. Drives Claude Code for coding tasks.
4. **App builder:** your app -> OpenRouter (one key, 500+ models) or self-hosted LiteLLM (budgets, virtual keys).
5. **Enterprise:** app -> Portkey / Cloudflare / Vercel gateway -> providers, with guardrails, caching, and audit.

## 7. Honest status labels 📊

| Tool | Label | Why |
|---|---|---|
| OpenRouter | ✅ Standard | Mainstream; 400T+ tokens/month, 10M+ users |
| LiteLLM | ✅ Standard | Default open-source proxy for teams |
| Claude Code, Codex | ✅ Standard | The reference coding harnesses |
| Cursor, Copilot | ✅ Standard | Established IDE agents |
| Antigravity | 🟢 Emerging, moving fast | 2.0 + CLI + SDK in 2026; Google pushing hard |
| OpenClaw | 🟢 Emerging, fast-growing | Renamed twice in months; big community |
| Hermes Agent | 🟢 Emerging | Self-hosted, bring-your-own-model; smaller but serious |
| 9Router | 🟡 Niche, gray edges | Community project; MITM intercept features need policy care |
| ClawRouter | 🟡 Niche, new | Bundled with OpenClaw; crypto billing on the hosted option |

## 8. Skeptic's corner ⚠️ (read before adopting)

- **Routers add a hop.** One more thing between you and the model: one more place for latency, one more place your data passes through, one more config to maintain. Use one when the fallback, billing, or translation value is real.
- **Routers do not improve quality.** They cannot make a bad model good. They move bytes.
- **Third-party routers see your prompts.** OpenRouter and friends are trusted by millions, but read their data policies. For sensitive work: self-host (LiteLLM, local 9Router) or go direct to the provider.
- **MITM interception is a gray zone.** Using IDE subscriptions through interception may violate vendor terms. "Works technically" is not "allowed".
- **Names churn.** Clawdbot -> Moltbot -> OpenClaw in months; 9Router is not OpenRouter. Verify the actual project before installing anything.

## 9. Thai Speaker Traps (tooling edition)

⚠️ **"Router"** != เราเตอร์บ้าน (home WiFi router) = ตัวกลางที่ส่ง request ไปยังโมเดลและผู้ให้บริการหลายเจ้า พร้อมจัดการ fallback และค่าใช้จ่าย
⚠️ **"Harness"** != สายรัด (literal strap) = โครงที่ห่อโมเดลให้เป็นเอเจนต์ (tools + loop + context) ตัวที่เรานั่งทำงานด้วย
⚠️ **"Gateway"** != ประตูบ้าน = ชั้น proxy ระหว่างแอปกับ API โมเดล (จัดการ key, budget, cache, guardrail)
⚠️ **"Provider"** != ผู้ให้บริการอินเทอร์เน็ต (ISP) = เจ้าของ API ของโมเดล เช่น OpenAI, Anthropic, Google
⚠️ **"OpenRouter" vs "9Router"** = คนละเจ้า: OpenRouter คือบริการบนคลาวด์ ส่วน 9Router คือโปรเซสที่รันบนเครื่องเรา อย่าสับสนเพราะชื่อคล้ายกัน

## 10. What I would do with this 🎯

- You already run all four layers: Hermes (platform) + OpenRouter / QwenCloud (routers and providers) + Claude Code (harness) + models. That is a complete stack.
- If Claude Code quota pain becomes real, 9Router is the pragmatic fix: stretch the subscription, fall back to cheap and free tiers. Respect the terms of service on the MITM features.
- Watch Antigravity: the SDK lets you build custom agents on Google's harness, and run evaluations on top of it. Relevant to the eval-suite work in [[applied-ai-concepts-q4-2026]].
- Before adopting any new tool, ask: (1) which layer is it? (2) what does it cost? (3) what happens when a provider dies? (4) does it lock in my config?

## Related notes

- [[agentic-ai-frameworks-and-terminology]] - frameworks, protocols, memory, observability
- [[ai-buzzword-map-2026]] - the vocabulary around all of this
- [[claude-code-setup]] - your Claude Code setup guide
- [[applied-ai-concepts-q4-2026]] - model routing as an applied practice
- [[ai-data-leakage-and-privacy-2026]] - the security side: what leaks, why, and how to prevent it

## Sources (web-verified 2026-09-22)

- OpenRouter: openrouter.ai (homepage, model routing blog, presets guide)
- 9Router: 9router.com and github.com/decolua/9router
- OpenClaw: openclaw.ai, docs.openclaw.ai (ClawRouter provider page), Wikipedia
- Antigravity: antigravity.google (products: 2.0, CLI, SDK, IDE)
- Codex: openai.com/codex and github.com/openai/codex
- Hermes Agent: hermes-agent.ai and hermes-agent.nousresearch.com docs
- Gateway landscape: Vercel (7 Best AI Gateways 2026), api7.ai gateway comparison

---

*Authored by LLMOps 🦙, 2026-09-22. This layer churns fast - re-verify names, prices, and versions before citing in any ADR.*
