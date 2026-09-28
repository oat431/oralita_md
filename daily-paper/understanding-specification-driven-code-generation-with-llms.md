---
title: "Understanding Specification-Driven Code Generation with LLMs: An Empirical Study Design"
tags: [paper, spec-driven, llm, code-generation, empirical-se]
created: 2026-09-20
revised: 2026-09-23
source: "Rosa, Moreno-Lumbreras, Robles, González-Barahona; arXiv:2601.03878v1 [cs.SE], 7 Jan 2026; PDF: F:/papers/Understanding Specification-Driven Code Generation with LLMs An Empirical Study Design.pdf"
---

# Understanding Specification-Driven Code Generation with LLMs: An Empirical Study Design

> *Paper: Rosa, Moreno-Lumbreras, Robles, González-Barahona (Universidad Rey Juan Carlos, Spain). "Understanding Specification-Driven Code Generation with LLMs: An Empirical Study Design." Stage 1 Registered Report; protocol peer reviewed and accepted at SANER 2026 with a Continuity Acceptance score for Stage 2. arXiv:2601.03878v1 [cs.SE], 7 Jan 2026. 7 pp. Page numbers are PDF pages (they match printed pages in this source). The plain-language explanation is below; the dense detail (design, metrics, verbatim quotes) lives in the appendix after the separator.*

## What Is This Paper, In Plain Words

Start with the strangest thing about it: this paper has no results, and that is the entire point.

It is a Stage 1 Registered Report, which flips the normal publishing order. In ordinary science, researchers run an experiment, look at the data, and then decide which story to tell. That quietly invites result-fishing: run twenty analyses, report the one that looks good, bury the rest. A registered report removes the temptation. The authors write the complete study plan first, the questions, the tool, the participants, the measurements, the analysis; the plan is peer reviewed; and the venue accepts it BEFORE any data is collected. The venue then commits to publishing the results whatever they turn out to be, as long as the study runs as promised. This paper is such an accepted plan: SANER 2026 reviewed the protocol and gave it a Continuity Acceptance score for Stage 2, the stage where the experiment actually happens. So as you read, treat every *we will measure* as a promise, not a finding. The value here is the blueprint.

Now the blueprint itself. The team built CURRANTE, a VS Code extension that walks a developer through a three-stage, test-first workflow. Stage 1: write a structured plain-language description of the problem in TOML format. Stage 2: have an LLM generate a test suite from that description, then refine it, asking for explanations of individual tests, deleting bad ones, regenerating single tests or the whole suite. Stage 3: have the LLM write the actual function and run it against those tests. The twist that makes this a genuine experiment in specification-driven development: the human never writes code. You own the specification and the tests; the machine owns the implementation. If the code comes out wrong, your only lever is to make the tests say more precisely what you meant.

The planned experiment puts real developers (juniors, seniors, CS students, industry professionals) in front of this tool and gives each of them one medium-difficulty problem from LiveCodeBench, a competitive-programming benchmark. They get roughly 30–45 minutes, no web search, no outside tools, and the extension logs everything: every test edit, every regeneration, every pass and fail, every token spent. Two research questions sit on top of that telemetry. RQ1 asks whether the tool can actually generate correct code from the specification the user provides. RQ2 asks how well users can express their intent through a test suite. The first question is about the machine; the second is about you.

One more piece of placement. This paper is the empirical companion to [[spec-driven-development-from-code-to-contract]]. That guide walks through spec-driven development's levels, tools, and case studies, and argues that writing specifications and tests before code makes LLM code generation better. This paper takes one central claim from that argument, that test-first specifications improve LLM code generation, and turns it into a measurable, peer-reviewed experiment. If the guide is the *why*, this protocol is the start of the *how do we know*. When the Stage 2 results land, they will either support the guide with real evidence or complicate it, and either outcome will be publishable, because the plan was locked in first.

## Why You Should Care

- **You are learning to read evidence, not just results.** Most papers you read show you a finished story; this one shows you the machinery behind the story: what will be measured, how, and what could distort it. That transparency is also a general tool. Whenever you suspect publication bias in any field, registered reports are the format to look for, and this seven-page paper is a compact specimen of how they work.
- **The design is stealable.** If you ever need to evaluate an LLM coding workflow (your team's, a vendor's, your own side project), this protocol hands you a ready-made measurement kit: correctness (PassAll, PassRate), test-suite strength (TestCoverage, TestDiversity), efficiency (TimeToPass, IterationsToPass), and process counters (TestEdits, SuiteRegenerations, AdviceTriggers). The threats-to-validity section doubles as a working checklist for any human-LLM study.
- **Process metrics are treated as first-class.** The interesting question is not just whether the code passes, but what the human contributed to get there. Counting test edits, regenerations, and advice triggers alongside outcomes is a design choice worth copying.
- **RQ2 is your daily bottleneck.** If you already work test-first with LLMs, you know the frustration of a suite that passes yet misses your intent. Whether users can encode intent in tests is exactly the question this study is instrumented to answer, and the telemetry schema shows what an honest attempt to measure it looks like.

---

# Appendix: The Dense Details

## The Registered-Report Framing

> "This paper is a Stage 1 Registered Report. The study protocol and analysis plan were peer reviewed and accepted at SANER 2026 with a Continuity Acceptance (CA) score for Stage 2." (p. 1)

Stage 1 means the protocol and analysis plan were peer reviewed and accepted before data collection; Stage 2 is the execution and results phase, covered by the Continuity Acceptance score. Every *we will* in the paper is a commitment, not a finding. The introduction motivates the study by noting that prior work validated TDD workflows with LLMs while "leaving the human factor underexplored" (p. 1), which presents:

> "a gap in understanding the user's role in guiding the LLM through structured requirements specification and test case definition" (p. 1)

> "The results will provide empirical insights into the design of next-generation development environments that align human reasoning with model-driven code generation." (p. 1)

## The CURRANTE Tool

CURRANTE is a VS Code extension implementing a TDD-style workflow where the test suite becomes the specification. The GUI has three areas (pp. 1–2):

1. **Problem description (area 1)**: a structured natural language specification in TOML format, capturing the user's intent, the function signature, and constraints. It seeds the process and guides the LLM.
2. **Test cases (area 2)**: an LLM generates an initial test suite from the TOML spec; the user refines it by requesting explanations for individual tests, deleting irrelevant ones, or regenerating single tests or the whole suite. The suite is the formal specification that drives code generation.
3. **Code generation (area 3)**: the LLM produces the function from the refined tests; the suite executes; per-test results and the aggregate pass rate are displayed. The user can regenerate after further test refinement.

```mermaid
flowchart LR
  S["1. Specification<br/>TOML problem description"] --> T["2. Tests<br/>generate and refine suite"]
  T --> F["3. Function<br/>LLM generates code"]
  F --> V{"All tests pass?"}
  V -->|"no"| T
  V -->|"yes"| D["Done"]
```

One design choice is the whole hypothesis in miniature: the final code is generated entirely by the LLM, and the human never writes code directly. The human's leverage is the specification and the tests.

## Research Questions

> **RQ1:** "To what extent is CURRANTE able to generate code based on the specification provided by the user?" (p. 2)

> **RQ2:** "To what extent does CURRANTE allow the user to express their intent through a test suite specification?" (p. 2)

RQ1 is about the tool's capability (does the pipeline produce correct code from a given specification); RQ2 is about the human's expressiveness (can users encode intent in tests effectively). Together they cover the two halves of the human-in-the-loop claim: the machine must be capable, and the human must be able to steer it.

## The Experiment Design

**Participants (p. 3).** A diverse pool of junior and senior developers, CS students, and industry professionals. Sessions are individual, on a single-monitor workstation with a fixed VS Code version, fixed LLM endpoint, prompts, and parameters. After a brief tutorial and one warm-up example, participants work only inside the IDE, with no external tools or web search. Participation is voluntary under informed consent; data are pseudonymized.

**Tasks (pp. 3–4).** Problems come from LiveCodeBench (release_v5, 880 problems as of January 2025): three easy warm-up problems plus three medium-difficulty evaluation candidates, selected for difficulty, type diversity, length, and contamination avoidance. The experiment runs only on the evaluation problems; each participant solves one, assigned randomly with balanced assignment, and TaskId is used as a blocking factor.

**Variables (pp. 4–5, Table I).** Three groups:

| Group | Variables |
|---|---|
| Independent | TaskId (the problem instance) |
| Dependent, correctness | PassAll (binary), PassRate (fraction) |
| Dependent, suite strength | TestCoverage, TestDiversity (for example Jaccard similarity) |
| Dependent, efficiency | TimeToPass (seconds), IterationsToPass (count) |
| Dependent, process | TestEdits, SuiteRegenerations, AdviceTriggers |
| Confounding | ProgrammingExperienceYears, PythonFamiliarity, PriorTDDExperience, PriorLLMCodeGenUse |

**Metrics (p. 5).** All metrics derive from time-stamped logs and test executions: times run from the first produced test suite; rapid duplicate clicks are filtered; participants who never reach all-pass get TimeToPass set to the full budget. Analysis plans descriptive statistics (medians, IQR, proportions) plus Spearman's ρ for exploratory correlations, with outliers flagged and excluded in sensitivity checks.

## Procedure and Execution Plan

- **Procedure (pp. 4–5).** The design follows the ACM SIGSOFT Empirical Standards for quantitative human-participant studies: tutorial, one warm-up task, then a between-subjects main task. The in-experiment workflow: open the TOML spec, produce the initial test suite, refine it (Explain / Regenerate / Delete, optional full-suite regeneration), generate the function and execute tests, then iterate, either refining tests or regenerating the function guided by auto-generated advice from failures. The task ends when all tests pass or the fixed time budget elapses.
- **Execution plan (pp. 5–6).** Three phases: *Preparation* (freeze the environment: VS Code version, CURRANTE build, prompt templates, LLM parameters; filter the dataset; select three easy training and three medium evaluation tasks; run a pilot with 2–3 participants; finalize consent forms and questionnaires), *Execution* (consent, pre-study questionnaire, training task, evaluation task under a budget of approximately 30–45 minutes, post-study questionnaire on usability and workload, short Likert items and free text), and *Analysis* (descriptive summaries first, then non-parametric comparisons, basic regressions, or survival-style summaries with right-censoring as the data warrants; de-identified logs, scripts, and artifacts archived for replication).
- **The LLM.** A recent, capable open-weight model, selected at execution time; the paper names Qwen3-Coder as a possible option, and prompts are deliberately kept simple with no advanced prompting techniques (p. 4).

## Threats to Validity

The authors separate internal from external threats and, in the registered-report spirit, commit to documenting new ones in the final protocol (p. 6).

**Internal.** Subject heterogeneity is handled by collecting demographics and using them as covariates, with constant instructions and time budget. Task sampling uses one medium task from three candidates with TaskId as a blocking factor. A warm-up and a single evaluation task per participant limit learning and fatigue. Instrumentation risk is mitigated by pilot-validating the logger, hashing artifacts, and fixing the timing boundaries. LLM non-determinism is addressed by fixing prompt templates and key parameters; the authors acknowledge exact reproducibility cannot be guaranteed in human–LLM studies and rely on multiple sessions to average out variation. Researcher effects are controlled with scripted briefings.

**External.** The sample may not represent all developers; the setup is one specific IDE, language, and model (single-monitor VS Code, Python/unittest, fixed LLM); only medium-difficulty benchmark tasks are used; disallowing web search raises internal control but lowers ecological validity; and the modest sample size means descriptive summaries take priority over inference.

## Contributions and Implications

Three contributions (p. 6): a reproducible task protocol on LiveCodeBench, a fine-grained telemetry schema capturing time-stamped actions and process metrics, and a transparent study plan for human-in-the-loop TDD. All materials will be open-sourced. For research, this enables principled comparisons of LLM workflows and test-curation strategies; for practice, the results will inform IDE design for spec-by-tests development; for education, CURRANTE offers scaffolded TDD with tighter feedback cycles.

## Practitioner Takeaways (synthesis)

1. **The spec is executable by design.** The TOML file is the seed, but the test suite is the real specification; the workflow turns the spec into something the machine can verify, not just read.
2. **Read it as a protocol.** Every *we will* is a hypothesis. The Stage 2 results are the thing to watch for; the design tells you exactly what will be measured when they land.
3. **Steal the instrument.** The telemetry schema, metric definitions, and validity checklist form a reusable blueprint for evaluating any LLM coding workflow.
4. **Process metrics are first-class.** TestEdits, regenerations, and advice triggers are measured alongside outcomes, because the research question is about the human's contribution, not just the final pass rate.
5. **The mitigations are a checklist.** Fixing model parameters, piloting the logger, hashing artifacts, and reporting demographics is a solid pattern for any human-LLM study.

## Memorable Quotes

> "This paper is a Stage 1 Registered Report. The study protocol and analysis plan were peer reviewed and accepted at SANER 2026 with a Continuity Acceptance (CA) score for Stage 2." (p. 1)

> "a gap in understanding the user's role in guiding the LLM through structured requirements specification and test case definition" (p. 1)

> "The results will provide empirical insights into the design of next-generation development environments that align human reasoning with model-driven code generation." (p. 1)

> "Broadly, our methodology offers a reusable blueprint for evaluating emerging LLM coding tools with a focus on human–AI interaction and realistic constraints." (p. 6)

## Related

- Companion paper: [[spec-driven-development-from-code-to-contract]], the practitioner guide this study empirically tests.
- Source PDF: `F:/papers/Understanding Specification-Driven Code Generation with LLMs An Empirical Study Design.pdf`
- arXiv: https://arxiv.org/abs/2601.03878

---

*Summary originally written 2026-09-20 from arXiv:2601.03878v1, the version matching the source PDF; restructured 2026-09-23 into plain-language body plus dense appendix. Page numbers are PDF pages; quotes are verbatim and page-cited; everything else is own-words paraphrase. This is a study protocol: no results exist yet at the time of writing.*
