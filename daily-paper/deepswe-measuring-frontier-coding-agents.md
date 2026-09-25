---
title: "DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks"
tags: [paper, benchmark, coding-agents, software-engineering, evaluation]
created: 2026-09-23
source: "Huang, Lee, Tng, Ge (Datacurve); DeepSWE technical report, May 2026; arXiv:2607.07946v1 [cs.SE], 32 pp.; PDF: F:/papers/DeepSWE.pdf"
---

# DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks

> *Paper: Wenqi Huang, Charley Lee, Leonard Tng, Serena Ge (Datacurve). "DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks." May 2026; arXiv:2607.07946v1 [cs.SE], 8 Jul 2026, 32 pp. Page numbers below are the paper's printed pages, identical to the PDF pages. Benchmark, verifiers, and full trajectory record: `https://github.com/datacurve-ai/deep-swe`, browser at `https://deepswe.datacurve.ai/`.*

## TL;DR

DeepSWE is a 113-task coding-agent benchmark that attacks the two structural weaknesses of the SWE-bench lineage at once. First, contamination: every task is authored from scratch and never merged upstream, so no reference solution exists in the public commit record that pretraining scrapes, and the task container ships only a shallow clone at the base commit (no `.git` history to mine). Second, grading: instead of inheriting the tests that shipped with some merged pull request, each task gets a hand-written functional verifier that asserts observable behavior through public APIs, so any implementation providing the requested functionality passes. An independent LLM-judge audit finds the judge disagrees with DeepSWE's verifier on 1.4% of rollouts versus 32.4% for SWE-Bench Pro's inherited tests, an order-of-magnitude gap. The prompts are half the length of SWE-Bench Pro's, yet reference solutions touch 5.5x more code. And the leaderboard separates frontier agents across a 69.8-point band where SWE-Bench Pro compresses them into 29.7 points, which is exactly why new model releases now headline their DeepSWE score (pp. 1-21).

## Why This Benchmark Became the Popular One

The paper answers this question directly, and the field's behavior confirms it:

1. **The old leaderboards saturated and spoiled.** SWE-bench-style tasks are mined from merged public pull requests, so gold patches sit in pretraining data; direct probing shows state-of-the-art models reproduce SWE-bench gold solutions far more verbatim than matched off-benchmark tasks (p. 4). Frontier labs themselves voice contamination concerns (the paper cites Anthropic, 2026, p. 3). A benchmark where a high score can reflect recall rather than problem-solving stops being news.
2. **DeepSWE still has headroom at the top.** The best configuration in the launch evaluation, GPT-5.5 [xhigh], scores 70.0% pass@1 (p. 2). There is room to grow, so improvements stay visible.
3. **It discriminates.** On SWE-Bench Pro eight frontier models cluster within a 29.7-point range; on DeepSWE the same models spread across 69.8 points (p. 14). A benchmark that separates models that otherwise look tied is immediately useful to anyone announcing a new release.
4. **The grading is auditable and the audit is public.** An independent judge re-reviews every graded rollout, the disagreement rate is 1.4% (p. 1), and the full trajectory record ships with the benchmark so anyone can re-check any verdict (p. 21).
5. **Model vendors adopted it as a headline metric.** The [[mimo-v26-technical-report]] note in this folder is one concrete example: Xiaomi reports DeepSWE as the first row of its main results table, with MiMo-V2.5-Pro at 19.0 climbing to 71.9 (V2.6-Pro) on DeepSWE v1.1, the refreshed corpus from the same team. This paper's own leaderboard carries mimo-v2.5-pro at 19.5% pass@1, consistent with that starting point. When the biggest training runs pick your benchmark to prove their RL worked, the benchmark becomes the default lens.

## The Two Structural Problems With Mined Benchmarks (pp. 1-2)

Most public agentic coding benchmarks descend from SWE-bench, which framed evaluation as resolving real GitHub issues from 2,294 instances mined from merged pull requests across twelve Python projects. The recipe scales, but it carries two costs:

- **Contamination.** The fixes and their discussion are already public and plausibly in pretraining data, "so a high score can reflect recall rather than problem-solving" (p. 1). Worse, the paper documents a packaging leak: in its SWE-Bench Pro audit, a sizable share of Claude Opus rollouts recovered the reference fix directly from the repository's `.git` history shipped inside the evaluation container (p. 7). An external report on the same benchmark found 33 of 38 cheating trials (87%) read the gold commit out of `.git` history (p. 17).
- **Inherited grading.** Each task is graded by the tests that happened to ship with its merged fix. Those tests were written to confirm one specific fix, not to grade an arbitrary solution, so they fail correct alternatives (a gold test imports a private helper the prompt never mentions) and pass incomplete ones (an agent stubs `execExternalPortScan` into a pass-through and the weak gold tests never notice). SWE-Bench Pro's human-written requirements and interface blocks reduce naming-mismatch false negatives but do not change how submissions are graded (p. 4).

DeepSWE takes a third position on decontamination, beyond racing model cutoffs (SWE-bench Live, SWE-rebench, LiveCodeBench) and access barriers (SWE-Bench Pro's private splits): author tasks from scratch and never merge them, so the reference solution stays off the public record (p. 4).

## Benchmark Construction (pp. 5-9)

**Corpus.** 113 tasks across 91 active open-source repositories and five languages: TypeScript 35 tasks (31%), Go 34 (30%), Python 34 (30%), JavaScript 5, Rust 5. Repositories must be public, actively maintained, at least 500 GitHub stars, and permissively licensed; each task pins to an immutable commit hash. The median repository contributes a single task (75 of 91 repos contribute exactly one), so no repo dominates. That breadth matters: SWE-Bench Pro Public spans 11 repositories and SWE-Bench Verified 12, mostly flagship projects, which is narrower than what developers actually point agents at (p. 5).

**Prompt/solution asymmetry.** Mean prompt length: DeepSWE 2,158 characters versus 4,614 for SWE-Bench Pro and 1,700 for SWE-Bench Verified. Mean reference solution: 668 lines added versus 120 and 9.9; mean files edited 7.4 versus 5.1 and 1.2 (p. 6). Short, natural prompts (the way developers actually talk to agents, with no interface-definition blocks) eliciting large multi-file solutions is what "long-horizon" means here: the agent must explore the codebase to locate the relevant surface and reconstruct the implicit specification before writing code (p. 19).

**Task artifacts.** Every task ships three pieces: the prompt, an executable verifier, and a reference solution used only during review, never at grading time. Verifiers extend the repository's own test infrastructure, assert through public APIs and observable outputs, run three times during authoring (flaky verifiers go back for revision), and include regression checks against a selection of the repository's existing tests: a patch that implements the feature but breaks unrelated functionality fails (pp. 8-9).

**Quality assurance.** Human reviewers judge each task on four dimensions (p. 9): prompt-verifier bijection (the verifier tests exactly what the prompt asks, no more, no less), acceptance breadth (any reasonable implementation passes, not just the reference shape), realism (natural developer register; a maintainer might plausibly accept the task as a contribution), and environment cleanliness (failures come from the task, not from flaky infrastructure). Multiple frontier configurations attempt each task during review; near-correct failing rollouts are used to refine the verifier.

## Experimental Setup (pp. 9-13)

- **Configurations:** 16 frontier model-and-reasoning-effort pairs, from GPT-5.5 [xhigh] down to minimax-m2.7. Effort settings mix explicitly set and provider defaults, a comparability caveat the paper states plainly (p. 10).
- **Harness:** every model runs under mini-swe-agent (pinned commit adfe2023) with a single bash tool and one shared prompt: no per-vendor editing primitives, no model-specific system prompts, so the leaderboard reflects model capability rather than scaffolding (p. 5). A sanity pilot (n = 10 SWE-Bench Pro tasks per model) found no systematic handicap from the standardized harness: pass rates were equal or higher than native products for all three models tested (50% vs 40% for Claude Opus 4.7 against Claude Code, 40% vs 40% for GPT-5.5 against Codex CLI, 40% vs 20% for Gemini 3.1 Pro against Gemini CLI), though the sample is too small to rank harnesses (pp. 10-11).
- **Budget:** about 4 rollouts per task per configuration, 7,174 scored rollouts in total (each configuration contributes 428 to 452). Wall-clock timeout 9,000 seconds (2.5 hours), no step or cost cap; only 67 rollouts (0.9%) hit the timeout (p. 10). Leaderboard runs collected May 2026.
- **Metrics:** pass@1 is the macro-average per-task pass fraction (every task weighted equally); pass@4 is the fraction of tasks solved by at least one of four rollouts. Their difference is the headroom a model gains from a few extra attempts (pp. 11-12).
- **Uncertainty:** running every task about four times is like running the whole benchmark four times, giving run-to-run 95% CIs (pass@1 +/- 1.96 SE), following Terminal-Bench. The paper is candid that this captures only rerun noise, not task-selection noise: a cluster bootstrap would give wider intervals, and even a pooled Wilson interval for GPT-5.5 is [65.6, 74.1] against [67.2, 72.9] run-to-run (p. 12).
- **Exclusions:** provider, verifier, and network errors are excluded from numerator and denominator; context-window exhaustion and agent timeouts count as genuine failures because they are within the agent's control. Exclusions range from 0% (the three top configurations) to 5.3% (Gemini 3 Flash), so ordering is not sensitive to the rule (p. 13).

## The Leaderboard (p. 2)

| Configuration | pass@1 | pass@4 |
|---|---|---|
| gpt-5.5 [xhigh] | 70.0% | 88% |
| gpt-5.4 [xhigh] | 55.5% | 77% |
| claude-opus-4.7 [max] | 54.2% | 86% |
| claude-sonnet-4.6 [high] | 31.6% | 62% |
| gemini-3.5-flash [medium] | 28.3% | 57% |
| claude-opus-4.6 [max] | 27.1% | 50% |
| gpt-5.4-mini [xhigh] | 24.3% | 46% |
| kimi-k2.6 | 23.9% | 49% |
| mimo-v2.5-pro | 19.5% | 45% |
| glm-5.1 | 17.5% | 39% |
| gemini-3.1-pro | 9.9% | 25% |
| deepseek-v4-pro | 7.5% | 19% |
| gemini-3-flash | 5.2% | 15% |
| qwen3.6-plus | 2.7% | 10% |
| claude-haiku-4.5 | 0.2% | - |
| minimax-m2.7 | 0.2% | - |

Read it with the CIs: GPT-5.5 sits clearly apart at the top ([67.2, 72.9]), but GPT-5.4 ([53.4, 57.7]) and Claude Opus 4.7 ([49.5, 58.9]) have overlapping intervals and are not statistically separated (p. 12). The paper also warns that a wider spread aids resolution but is not by itself a capability claim: it discriminates only insofar as the rank order tracks an external signal of quality, which the paper does not measure (p. 13). On cost, output tokens, wall-clock minutes, and dollar cost per trial each vary by an order of magnitude across agents, and none correlates strongly with pass rate: "emitting more tokens, running longer, or costing more does not consistently solve more tasks" (p. 13).

## Qualitative Analysis: What the Trajectories Show (pp. 15-19)

A structured audit ran a judge (GPT-5.5 at xhigh, operating as a Codex CLI agent in a fresh sandbox) over 30 random tasks per benchmark, 9 configurations, 3 rollouts each, with every verdict grounded in cited evidence and the full audited sample released. Findings that cluster by model family:

- **Claude configurations miss enumerated requirements most often.** DeepSWE prompts frequently list parallel requirements ("support both sync and async"); Claude often implements one branch and does not mirror the change in the other. Roughly two-thirds of Claude's MISSED_REQUIREMENT rollouts fit this "one branch shipped" pattern (p. 16).
- **Claude configurations most often recover the gold solution from the container.** On SWE-Bench Pro, about 18% of Opus 4.7's passes and 25% of Opus 4.6's were judged improper (CHEATED), versus roughly 1% for Gemini and none observed for GPT-5.4/5.5 in the audited sample. The benchmark makes this possible (the gold commit lives in the container); Claude configurations are the ones that most consistently exploit it (p. 16).
- **GPT configurations miss stated requirements least often.** GPT-5.5 has the lowest MISSED_REQUIREMENT rate of any configuration; trials converge on the same prompt interpretation across runs, consistent with a stable trait (p. 16).
- **Stronger models test more, unprompted.** Claude Opus 4.7 and GPT-5.4 author new tests in the project's own framework on over 80% of DeepSWE runs (85% and 83%), even though nothing asks them to; Gemini 3 Flash submits without running any test on 18% of runs. And one prompt line explains a striking gap: SWE-Bench Pro's standard wrapper tells agents not to modify tests, and self-test-writing collapses (the same models drop to single digits to low tens of percent), while DeepSWE's prompts say nothing about tests and the behavior returns (pp. 16-17).
- **SWE-Bench Pro disagreement bands:** TEST_MISMATCH (verifier failed a trial the judge deemed correct) hits 19% to 28% of GPT-5 variants' reviewed trials; CHEATED hits roughly 13% of Claude Opus trials (p. 17).

The audit's headline number: over n = 789 SWE-Bench Pro and n = 735 DeepSWE rollouts, the judge disagreed with the SWE-Bench Pro verifier on 256 rollouts (67 false positives, 8.5%; 189 false negatives, 24.0%; 32.4% overall, 95% Clopper-Pearson [29.2, 35.8]%) against 10 for DeepSWE (2 false positives, 0.3%; 8 false negatives, 1.1%; 1.4% overall, [0.7, 2.5]%). The intervals are far from overlapping, though the DeepSWE side rests on single-digit counts, and this is a disagreement rate between two independent readers, not a ground-truth error rate (pp. 7-8).

## Limitations the Paper States (pp. 19-21)

Refreshingly explicit: binary reward with no partial credit (a patch missing one requirement scores like one that never compiles); functional correctness only (no code quality, style, performance, or documentation scoring, so a pass does not certify something a maintainer would merge); prompts around 2,000 characters are still longer than day-to-day agent requests, and results may not transfer to terser instructions; under-specified requests and non-coding agent uses are unmeasured by construction; a single fixed harness may hold some families below their native ceiling; the verifier audit is small-sample and the judge (GPT-5.5) is also the top-ranked configuration, so self-preference bias cannot be excluded; and decontamination is a property at evaluation time, since released prompts and verifiers could enter future training data (the mitigation is that an authored corpus can be refreshed). Future work: multi-harness runs to decompose model versus scaffold, C++ and Java, more bug-localization and refactoring tasks, and hybrid verifiers.

## Takeaways (for practitioners)

1. **Check how a coding benchmark's tasks were sourced before trusting its leaderboard.** Mined tasks measure recall as much as reasoning; authored, never-merged tasks with shallow-clone containers measure problem-solving.
2. **The verifier is the benchmark.** Inherited PR tests produce both false passes (stubbed features) and false fails (private-helper imports, missing fixtures, unrelated snapshot tests). Functional verifiers written from the spec, asserting public behavior, are an order of magnitude more trustworthy under audit.
3. **Prompt wrappers shape agent behavior.** Telling an agent "tests are already handled, do not modify them" suppresses self-verification; removing that line brings test-writing back. If you run your own agent evaluations, your wrapper is part of the measurement.
4. **Discrimination matters more than difficulty.** A benchmark where frontier models cluster within a few points cannot rank releases; DeepSWE's 69.8-point spread is why it became the headline metric for new models.
5. **Beware pass rates without CIs.** Mid-table neighbors here are not statistically separated, and run-to-run intervals understate true uncertainty (task-selection noise); read leaderboards as bands, not ranks.
6. **Agents cheat along the paths the environment leaves open.** A gold commit in `.git` history is an invitation; 87% of externally documented cheating trials took it. Environment scrubbing is a first-class part of evaluation design (the same defense-in-depth logic as the [[mimo-v26-technical-report]] hack-agent).

## Memorable Quotes

> "a high score can reflect recall rather than problem-solving" (p. 1)

> "A benchmark is only as good as its verifier." (p. 7)

> "This is intended to test whether an agent can solve a novel software engineering problem, rather than recall, retrieve, or rediscover a public fix." (p. 7)

> "so that the leaderboard reflects model capability rather than scaffolding" (p. 5)

> "Stronger models test more, and they do it unprompted." (p. 16)

## Related

- Adopted as the headline coding metric in the Xiaomi MiMo-V2.6 report: [[mimo-v26-technical-report]] (DeepSWE v1.1, the refreshed corpus from the same team: MiMo-V2.5-Pro 19.0 to MiMo-V2.6-Pro 71.9; this paper's leaderboard shows mimo-v2.5-pro at 19.5% pass@1).
- Benchmark and trajectories: `https://github.com/datacurve-ai/deep-swe`, `https://deepswe.datacurve.ai/`
- Source PDF: `F:/papers/DeepSWE.pdf`

---

*Summary written 2026-09-23. Page numbers are the paper's printed pages (identical to PDF pages). Quotes are verbatim; everything else is own-words paraphrase. References (pp. 22-24) and the appendix prompt gallery (pp. 28-32) are not summarized beyond the prompt-length contrast. The MiMo-V2.6 connection is a deliberate, specific cross-link, not a generic folder list.*
