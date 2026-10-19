---
title: "Harness Maxxing (Q4 2026): Getting Everything Out of a Model You Already Have"
date: 2026-10-19
author: LLMOps 🦙
tags: [ai, agents, harness, harness-maxxing, evals, optimization, cost, reference, ai-series]
status: living
---

# Harness Maxxing (Q4 2026): Getting Everything Out of a Model You Already Have

> **Your question:** If the harness matters more than the model, what does it look like to actually *max out* a harness - and where does that turn into fooling yourself?
> **Short answer:** Harness maxxing is extracting capability from a **fixed** model by engineering the wrapper around it: fewer and sharper tools, verification before the agent is allowed to stop, strict context hygiene, and caps it cannot argue past. It is the highest-ROI engineering work in AI in 2026 - and it is already a named trap, because a harness tuned against a benchmark is **scar tissue shaped for one model** and does not transfer to the next one.
> **Verification:** Web-checked 2026-10-19. The term itself is about three months old and the benchmark numbers below are volatile - re-verify before quoting any of them.
> **Companion:** [[14_agent-harness-anatomy-2026]] (the 19 components and which seven are irreducible), [[04_ai-tools-landscape-2026]] (the layer map), [[02_ai-buzzword-map-2026]] (the `-maxxing` family).

---

## 1. The word, and the family it joined

**Harness maxxing** entered the vocabulary in August 2026, in a paid essay titled "the Rise of Harness-Maxxing" about small open models beating frontier ones on benchmarks. Within three weeks it had a rebuttal with the term in the title: "The Harness-Maxxing Trap". That speed is the story. A practice this effective gets a name, then a backlash, in the same quarter.

It belongs to the `-maxxing` family, and the family members are not the same thing:

| Term | What it means | Status |
|---|---|---|
| **Tokenmaxxing** | Burning tokens on purpose, by orgs or individuals, to look AI-native | 🟢 Real criticism (the anti-pattern) |
| **Context-maxxing** | Deliberately maximizing the *useful* context a model gets, instead of maximizing its length | 🟢 Emerging (Brookings use, 2026) |
| **Harness maxxing** | Tuning the wrapper around a fixed model to raise task success | 🟢 Emerging, already contested |

Three definitions circulate, and you should know which one someone means:

1. **The engineering definition (use this one).** Systematically removing the harness's inefficiencies so a given model reaches its real ceiling: fewer tools, verification gates, context discipline, caps.
2. **The benchmark definition (this is the trap).** Iterating the wrapper against one benchmark until the number looks frontier-class, then reporting the number.
3. **The insult.** "That result is just harness maxxing" - i.e. the score belongs to the scaffolding, not the model.

They share a mechanism and differ in intent. The mechanism is real, which is exactly why the trap works.

---

## 2. Inner harness and outer harness: what you can actually max

You cannot max a harness you cannot modify. So split it first.

| Layer | Who builds it | What is in it | Can you change it? |
|---|---|---|---|
| **Inner harness** | The vendor (Anthropic, OpenAI, Anomaly, ...) | The loop, built-in tools, context management, permission system, orchestration | Only by choosing a different product |
| **Outer harness** | You | Project instructions, skills, hooks, MCP servers, tests, linters, permission rules, eval sets | Yes - this is your maxxing surface |

The outer harness has three kinds of control, and the distinction is the most useful idea in the whole discourse:

- **Guides** shape behaviour *before* the agent acts: instructions, `AGENTS.md`, skills, examples, tool descriptions.
- **Sensors** report *after* it acts: tests, linters, typecheck, schema checks, reviewer agents.
- **Caps** are boundaries the model **cannot talk its way past**: permission rules, sandboxes, infrastructure limits.

> **The asymmetry that matters:** guides advise, sensors report, **only caps stop anything**. A guide that says "never delete files" is a suggestion. A `PreToolUse` hook that rejects the call is a cap. Most "maxxed" harnesses are 90% guides and 0% caps - which is why they feel reliable in a demo and fail in an incident.

When people say "the harness matters more than the model", they usually mean the **inner** harness, and they are usually comparing vendor products. Your leverage is almost entirely in the **outer** one.

---

## 3. Why maxxing works at all

One sentence: **model intelligence is spiky, and the harness sands down the spikes for the tasks you care about.**

Concretely, three things are true at once:

1. **A model cannot act.** It cannot open a file, run a test, remember yesterday, or ask permission. Every one of those is harness work.
2. **Benchmarks measure a triple.** The honest sentence is never "model X scores 82". It is "**model X, in harness Y, at effort level Z**, scores 82". The official leaderboards record all three; marketing collapses them into one.
3. **Small harness differences are worth more than small model differences.** The public numbers, all same-model comparisons, are in the next section.

The corollary is the uncomfortable part: if the triple is what gets measured, then **you can raise the number without improving the model, and you can raise the model's number on your workload without ever touching the model.** Both are legitimate. Only the first one is dishonest.

---

## 4. The evidence: same model, different wrapper

| Comparison | Result | Source |
|---|---|---|
| Qwen3.6-27B, bash-only agent vs one extra edit tool | 28% -> **50.7%** on SWE-bench Pro (published figure 53.5%) | Qwen issue tracker, via AI Realist |
| GPT-5.5, Codex vs Terminus 2, same effort level | **83.1% vs 78.0%** on Terminal-Bench 2.1 | official leaderboard |
| Opus 4.7, Claude Code vs Terminus 2, same effort | **68.9% vs 66.1%** | official leaderboard |
| Kimi K3, vendor harness vs third-party harness | 88.3% -> **85.0%** (3.3 points lost) | Artificial Analysis, via AI Realist |
| LangChain coding agent, harness work only | **52.8% -> 66.5%** on Terminal-Bench 2.0, outside top 30 -> top 5 | LangChain |
| Same model, 8 harnesses, 25 tasks | 68% -> **88%** success | Composio bench, via Marmelab |
| Princeton CORE-Bench, same model, different scaffold | **42% vs 78%** | via MongoDB |
| Vercel, 80% of tools removed | 80% -> **100%**, tokens more than halved, 724s -> 141s | Vercel (second-hand magnitude) |
| Qwen3.6-27B inside Claude Code CLI | 90.0 on SWE-bench Verified vs Sonnet 4.6's published 79.6 | independent researcher, via AI Realist |

Read that last row carefully, because it is the trap in one line: a 27B open-weight model, run inside *someone else's* harness, reporting a number above a frontier model's vendor-published score. That does not mean the 27B model is better. It means the comparison is **not a model comparison at all**.

**The four fixes LangChain actually shipped** are worth memorising, because they are the boring kind that work: a middleware hook that intercepts the agent **before it exits** and forces a verification pass, a startup step that **maps the directory** so the agent stops burning turns on discovery, a **loop detector**, and a tighter prompt. Their most common failure was the agent writing code, re-reading it, deciding it looked fine, and stopping **without running a single test**. The fix lived entirely in the wrapper.

---

## 5. The maxxing ladder: twelve moves, ordered by return per hour

Step 0 is not a move, it is the precondition.

| # | Move | The change | Why it works | How you verify it |
|---|---|---|---|---|
| 0 | **Build the eval set** | 20 to 50 real tasks from your own traces, pass/fail | Without it, every move below is a coin flip | Baseline run passes/fails reproducibly |
| 1 | **Cut the tool set** | Delete tools until <=10; rewrite the survivors' descriptions | Tool count is a performance setting, not a feature list | Same tasks, fewer tokens, no success loss |
| 2 | **Add the one missing primitive** | Usually a real file-edit tool (`str_replace` / `apply_patch`) | One missing primitive can nearly halve a score | Watch for edit-shaped failures in traces |
| 3 | **Gate the exit** | Verification runs *before* the agent may stop | Agents declare victory after re-reading their own code | Ask for a deliberately broken change; it must not say "done" |
| 4 | **Map the environment** | Directory map, command list, `AGENTS.md` as an index | Stops the agent spending turns on discovery | Count exploration steps per task, before and after |
| 5 | **Clip and compact** | Cap tool output at ingest; summarise old turns into a state file | Context rot is a length failure, not a position one | Watch success rate vs step number in traces |
| 6 | **Cap the irreversible** | Deny-list + hook for delete/push/spend/send | A rule ending in a prompt is not a rule (93% approval rate) | Try a destructive command; it must be blocked, not asked |
| 7 | **Externalize the plan** | Write the plan to `plan.md` / `TODO.json`, not to context | Makes context disposable and resumable | Kill the session; the next one continues from the file |
| 8 | **Reset, don't just compact** | Fresh window + handoff artifact for long runs | Kills "context anxiety" (premature wrap-up) | Long task: quality at step 60 vs step 10 |
| 9 | **Subagent, only for overflow** | Read-only child, depth cap 2, summary returned | Context isolation, not a management diagram | Child count and token spend per task |
| 10 | **Separate the evaluator** | Rubric written as gradable criteria, different model, no shared context | Self-grading is reliably lenient | Evaluator catches failures the generator missed |
| 11 | **Fix the economics** | Prefix caching, model routing, effort level per task class | Cached input is roughly a tenth of the price | Cost and p95 per task, per model |
| 12 | **Automate the ratchet** | Every failure becomes a rule, hook, or eval case - permanently | The harness only improves if failures are captured | Count of cases/rules added per week |

**Order matters.** A team that starts at #11 (routing and caching) is optimising the cost of a system that does not work yet. A team that starts at #1 without #0 cannot tell whether deleting tools helped or hurt.

### 5.1 The three moves that pay most, in detail

**Cut the tools (move 1).** The instinct when an agent fails is to add a tool. The evidence says the opposite: fewer, better-described tools win on success, cost, *and* latency simultaneously - the only intervention in this whole area that moves all three the same direction. Microsoft's Azure operations agent crossed 100 tools in two weeks and had to collapse them into two broad ones. Before adding a tool, ask what failure it addresses; if you cannot name one, do not add it.

**Gate the exit (move 3).** This is the single highest-value hook in a coding harness. The pattern: intercept the stop, run the project's verify command, and if it fails, refuse the stop and feed the output back as an observation. It converts "the agent thinks it is done" into "the agent has to make the check pass". LangChain's version of exactly this hook is where their 13.7-point gain largely came from.

**Cap the irreversible (move 6).** Three verbs deserve caps, everywhere, always: **delete** outside the workspace, **push** to a protected branch or remote, and **spend** (money, quota, external messages). A 113-participant study found that people who wrote permission rules in advance blocked 20.1 percentage points *fewer* bad actions than people who approved each action as it came - because they set rules to "ask", then approved anyway (93% of prompts get approved). Rules that resolve to a prompt are decoration. Encode the cap in the runtime.

### 5.2 The economics table (maxxing without tokenmaxxing)

| Lever | What it buys | How | Caveat |
|---|---|---|---|
| **Prefix caching** | Cached input at roughly 10% of normal price; large latency cuts | Stable prefix first (system, tools, project docs), variable content last; cache TTL aware | Cache invalidation on prompt edits; provider-specific pricing |
| **Model routing** | 2x to 10x cost cut on grunt work | Cheap model for retrieval, summarisation, classification; expensive model for planning | One more hop and failure mode; misroutes silently |
| **Effort level** | Cost and latency down on easy tasks | Set reasoning effort per task class, not globally | Leaderboards record effort; your logs should too |
| **Output clipping** | The cheapest saving that exists | 16 KB shell cap, 250 lines for grep, 10 MB file-read cap | Clip too hard and the agent loses the evidence it needed |
| **Prompt caching + compaction** | Avoids re-sending a 100k-token prefix every turn | Compact late enough to keep detail, early enough to avoid rot | Over-aggressive compaction loses the one detail that mattered |

> This is where maxxing and tokenmaxxing split. **Tokenmaxxing spends tokens to look busy. Maxxing spends fewer tokens to get more done.** If a change raises cost and does not move success, it is not maxxing - it is a subscription to a feeling.

---

## 6. The trap: three dangers

This is the part that makes the note useful rather than a cheerleader piece. The critique is not "harness engineering is bad" - it is that harness maxxing is easy to confuse with deployment.

### 6.1 Danger one: the score belongs to the pair

When a vendor reports a benchmark result, the honest sentence is the triple: **model, harness, effort level**. Most marketing reports one third of it and lets you assume the rest. Moonshot's Kimi K3 was evaluated in Moonshot's own harness while the comparison columns used the best score across harnesses; re-run in a third-party harness it lost 3.3 points. Same model, same benchmark, different wrapper.

The procurement consequence: **buying a model on published scores means buying a harness you do not have, tuned to a benchmark you do not run.** When you wire that model into your own harness, none of the tuning transfers. The Qwen developer who measured 28% with a bash-only agent was not doing anything wrong - he was doing what every enterprise does: running the model in a different environment.

### 6.2 Danger two: a maxed harness is scar tissue for one model

Every component in a tuned harness encodes an assumption about a *specific model's specific failure*:

- the pre-exit verification hook exists because **this** model skips tests
- the directory map exists because **this** model wastes turns exploring
- the loop detector exists because **this** model gets stuck in **that** way

OpenAI's harness team says it plainly: their best harness components are **designed to be deleted**, because each is a workaround for a limitation the next model may not have. With model cycles measured in months, a harness maxed against a March model can become a liability by September - and worse, the tuning becomes the reason you cannot switch.

**The practical test:** keep a "clean config" baseline (no project rules, no extra tools) and re-run it after every model upgrade. If clean-config performance catches up to the maxxed config, your rules are now scar tissue. Delete them and celebrate.

### 6.3 Danger three: the harness sits inside the blast radius

A harness lives inside the agent's process. Its guides are prompts, its sensors are tests, its caps are permission checks **enforced by the runtime the agent is running in**. That is the right place for making one agent do one task well. It is the wrong place for the failures that actually kill production systems.

Gartner's reading of the failure data: more than 40% of agentic AI projects will be canceled by the end of 2027, and separately that 40% of enterprises will demote or decommission autonomous agents by 2027 because of governance gaps discovered after incidents. The cited causes are unclear business value, weak governance, integration with systems the agent does not own, identity and audit, and "who is accountable when the agent is wrong". **Not one of those is fixed by a better harness.**

> A harness can enforce that the agent tested its work. It cannot enforce that the work was the right work. That is a specification problem and an ownership problem, and no amount of wrapper engineering touches either.

---

## 7. The rules of responsible maxxing

1. **Max against your own tasks, never a public benchmark.** A benchmark-optimised harness is a benchmark-shaped harness. Public numbers are a shopping signal; your eval set is the engineering one.
2. **Record the triple.** Every result you keep must carry model, harness version, and effort level. Results without the triple are anecdotes.
3. **One change at a time when you are tuning.** Batch changes only for a first exploratory pass, and say so when you do - a batched run gives you one number, not four explanations.
4. **Every component needs a deletion condition.** Write it when you add the component: "delete this when check passes without it". Otherwise you are accumulating scar tissue on purpose.
5. **Measure cost and latency next to success.** A harness that gains 3 points for double the tokens is a different product, not a better one.
6. **Caps go in the runtime, not the prompt.** Guides and sensors are for quality. Caps are for damage.
7. **Maxxing never substitutes for a spec.** If you cannot say what success looks like in a sentence a human can check, no wrapper will rescue the task.


## 8. The maxxing scorecard

Score each row 0 (absent), 1 (partial), 2 (solid). Twenty-four points total.

| # | Check | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | Eval set from your own traces, runnable on demand | none | <20 cases | 20+ with pass checks |
| 2 | Baseline recorded with model + harness + effort | none | partial | stamped per run |
| 3 | Tool count <=10, each tied to a named failure | sprawl | some | disciplined |
| 4 | A real edit primitive exists | no | partial | yes |
| 5 | Verification runs automatically before "done" | no | manual | gated |
| 6 | Environment mapped at startup | no | partial | indexed |
| 7 | Tool output clipped, compaction configured | no | some | tuned |
| 8 | Irreversible actions capped, not prompted | prompts | some caps | enforced |
| 9 | Plan and progress externalized to files | no | sometimes | always |
| 10 | Reset + handoff artifact for long runs | no | compaction only | reset + artifact |
| 11 | Evaluator separate from generator, rubric written | no | same context | separate model |
| 12 | Cost per task measured, prefix caching in place | no | measured | optimised |

| Score | Verdict |
|---|---|
| 0 to 6 | Toy. It demos; it does not deploy. |
| 7 to 12 | Working harness. Most of the value is still on the table. |
| 13 to 18 | Production-shaped. Now the gains get expensive. |
| 19 to 24 | Frontier-shaped. Your remaining wins are model-specific - watch for scar tissue. |

---

## 9. A 90-minute maxxing session

For a harness you already run (Claude Code, Codex, OpenCode, Hermes). This is a first pass, not a tuning campaign.

1. **0-15 min - build cases.** Open your last 10 sessions. For each, write one JSONL line: task, the check that defines success, and pass/fail. You now have an eval set. It is crude and it is better than every benchmark you do not run.
2. **15-25 min - baseline.** Run all 10 with your current config. Record model, harness version, effort level, tokens, wall-clock.
3. **25-40 min - cut tools.** List every tool and the failure it addresses. Delete the ones you cannot justify. Re-run. If success holds, keep the deletion.
4. **40-55 min - gate the exit.** Wire the project's verify command into the stop path. Test it by asking for a change that breaks the build - it must not report "done".
5. **55-65 min - context hygiene.** Clip shell output at 16 KB, set a compaction threshold, move the plan into a file. Re-run.
6. **65-75 min - cap the irreversible.** Deny-list delete/push/spend, add the hook. Test with one destructive command; it must be blocked, not asked about.
7. **75-90 min - measure and write it down.** Re-run the 10 cases. Record the delta with the triple. Keep what helped, revert what did not, and log one line per change in the harness's own changelog.

You will usually end this session with a net gain and **no idea which change caused it**, because you batched. That is fine for a first pass. The next session is four separate afternoons of one change each - that is the ablation, and it is the only way to know what to keep.

---

## 10. Applied to your stack 🎯

Your setup is Hermes Agent (platform: memory, skills, scheduler, subagents) plus Claude Code (the coding harness). Five concrete maxxing moves, in order:

1. **A `Stop` hook in Claude Code that runs `make test` or `bun test`.** Refuse the stop on non-zero exit and feed the output back. This is move 3, and it is the highest-value change available to you for the least effort.
2. **A `PreToolUse` cap for three verbs.** `rm -rf` outside the workspace, force-push, and anything touching `.env`. You already deny `.env` reads in settings - extend the same mechanism from "read" to "irreversible write".
3. **`AGENTS.md` as an index, symlinked to `CLAUDE.md`.** One human-written file, under 100 lines, pointing at `docs/` and rule files. Every harness you run reads the same source. Add a line only after an incident; delete a line when a model stops needing it.
4. **Twenty cases from your own repos.** Your job-hunting loop note already describes a bounded loop with a verifier - that is the shape. The cases come from real sessions: "fix the failing test", "add the endpoint", "refactor without breaking `make lint`".
5. **Cost per task, then routing.** Log tokens per session. Put `qwen3.8-flash` on grunt work and reserve `qwen3.8-max` / `deepseek-v4-pro` for planning and stuck runs. Turn on prefix caching by keeping the system prompt and project docs stable and putting variable content last. And prune memory before adding to it: a memory store at its budget is the clearest maxxing signal there is - stale entries cost context on every single turn.

---

## 11. Skeptic's corner ⚠️

- **The term is three months old and already has a rebuttal with its name in the title.** That is not a reason to ignore it; it is a reason to read both sides before quoting either. The practice predates the word by at least a year - people have been "fixing the wrapper" since the first agent loop.
- **The deltas do not transfer.** 83.1 vs 78.0 is a harness comparison. 3.3 points lost when re-run in a different harness is the same lesson from the other side. Your workload will produce a third number.
- **Effort level is a hidden dial.** Raising reasoning effort raises scores and token spend. That is maxxing on the benchmark and tokenmaxxing in the bill. Stamp the effort level in your logs or you will not know which one you did.
- **Automated harness search makes Goodhart cheap.** Research systems now search over harness code itself - LangChain's managed variant detects failures in production traces, drafts a fix, and adds an evaluator to prevent regression. Point that at a benchmark and you will get a benchmark-shaped harness at machine speed. Point it at your own eval set, and it is the ratchet with a motor.
- **Most of the gains are boring.** Directory maps, loop detectors, output clipping, a verify hook. Nobody writes a conference talk about those, which is why teams keep skipping them for agent architectures.
- **A maxxed harness can hide a specification failure.** If the task was wrong, a harness that reliably does the wrong thing faster is worse than one that fails loudly. Ask what "done" means before you make the agent better at reaching it.

---

## Related notes

- [[14_agent-harness-anatomy-2026]] - the 19 components, the seven that are irreducible, and the market comparison
- [[03_agentic-ai-frameworks-and-terminology]] - harness engineering, loop engineering, and the `-X engineering` stack
- [[04_ai-tools-landscape-2026]] - model vs router vs harness vs platform
- [[07_job-hunting-as-loop-engineering]] - a bounded loop with a verifier and designed exits (the same pattern, non-coding)
- [[01_applied-ai-concepts-q4-2026]] - context engineering, trajectory eval, bounded agents
- [[02_ai-buzzword-map-2026]] - the `-maxxing` family and how to judge a new word
- [[06_templates-vs-skills-and-ai-dlc]] - skills and hooks as process, not prompt text
- ai-knowledge vault: `04_Applied_AI_Engineering/03_Evaluation_and_Observability/`

## Sources (web-verified 2026-10-19)

- Maria Sukhareva, "How a Small Open Model Beat a Frontier LLM: the Rise of Harness-Maxxing", AI Realist (2026-08-04) - https://msukhareva.substack.com/p/how-a-small-open-model-beat-a-frontier
- Pascal Biese, "The Harness-Maxxing Trap", LLM Watch (2026-08-25) - https://www.llmwatch.com/p/the-harness-maxxing-trap
- Qwen issue #179 (bash-only vs `str_replace`, 28% -> 50.7% on SWE-bench Pro) - https://github.com/QwenLM/Qwen3.6/issues/179
- Terminal-Bench 2.1 leaderboard (model + harness + effort triples) - https://www.tbench.ai/leaderboard/terminal-bench/2.1
- LangChain, "Improving deep agents with harness engineering" (52.8% -> 66.5%) - https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering
- OpenAI, "Harness engineering" (1,500 merged PRs, ~100-line AGENTS.md, components designed to be deleted) - https://openai.com/index/harness-engineering/
- Anthropic Engineering, "Effective harnesses for long-running agents" - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic Engineering, "Harness design for long-running application development" (context resets, planner/generator/evaluator) - https://www.anthropic.com/engineering/harness-design-long-running-apps
- Birgitta Böckeler, "Harness engineering" (inner/outer harness, guides and sensors) - https://martinfowler.com/articles/harness-engineering.html
- Microsoft Agent Framework docs, agent harness - https://learn.microsoft.com/en-us/agent-framework/agents/harness
- Microsoft Tech Community, Azure SRE agent context-engineering lessons (100 tools -> 2; four-handoff limit)
- Marmelab, "The State Of AI Harness Engineering 2026" (2026-09-24) - https://marmelab.com/blog/2026/09/24/the-state-of-ai-harness-engineering-2026.html
- Winder.AI, harness comparison (2026-08-20) - https://winder.ai/ai-agent-harness-comparison/
- Stanford IRIS lab, Meta-Harness (search over harness code) - https://github.com/stanford-iris-lab/meta-harness
- Claude Code hooks reference (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Stop`) - https://code.claude.com/docs/en/hooks
- AGENTS.md as a cross-harness standard (Codex, Claude Code, Cursor, OpenCode, Copilot) - https://aq.dev/glossary/agents-md/
- Sandbox providers compared: E2B, Modal Sandboxes, Daytona, Cloudflare Sandbox SDK - https://blog.logrocket.com/comparing-ai-agent-sandbox-platforms-e2b-modal-daytona-and-more/
- Prompt caching cost math across providers (2026) - https://www.developersdigest.tech/blog/prompt-caching-across-ai-providers-2026
- Permission-supervision study, 113 participants (arXiv 2608.27443); 93% prompt-approval rate, Anthropic Claude Code sandboxing post
- Gartner agentic-project forecasts, as reported by Forbes (2026-07-07) and EnterpriseDNA (2026)

---

*Authored by LLMOps 🦙, 2026-10-19. The evidence base is three months old and contested; the discipline is older and sound. Re-verify the numbers, keep the order of operations.*
