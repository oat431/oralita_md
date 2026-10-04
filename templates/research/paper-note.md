---
title: Paper Note Template
tags: [research, template, paper-note, academic-reading]
created: 2026-10-04
---

# Paper Note Template

> These are your notes on a paper, not a summary of it. Hermes writes an AI summary of each paper to `daily-paper/<slug>.md`: that's what the paper *says*. This note records what *you* think after reading it. Copy the block into `daily-paper/reading-notes/` for every paper that gets past Pass 1. Papers that stop at Pass 1 get one line in the reading log instead. The method behind every field is in [[how-to-read-a-research-paper]].

## Rules That Keep Paper Notes Useful

1. **Pass 1 only: one log line, not a note.** A full note is for papers you read at Pass 2 or deeper. Keep the log in `daily-paper/reading-notes/00-reading-log.md`.
2. **Read the paper before the AI summary.** Do your passes and fill in this note first. Then open the Hermes summary and compare; where they disagree, the PDF decides. The summary's quotes and numbers are machine-checked, but its narrative and cross-links are not.
3. **Write your summary in your own words.** If you can't write three sentences without looking, go back to Pass 2.
4. **Every claim gets a location.** Section, figure, or table. The same rule applies to AI summaries.
5. **Critique = what the authors didn't list.** Mark which threats the authors listed and which you found yourself.
6. **Filename:** `daily-paper/reading-notes/<summary-slug>-reading.md`, e.g. `understanding-specification-driven-code-generation-with-llms-reading.md`. The `-reading` suffix keeps `[[wikilinks]]` to the summary unambiguous.
7. **Record the version you read** (arXiv v1, v2, or the published version) and the PDF path.

## Template

```markdown
---
title: "<Paper title>"
summary: "[[<summary-slug>]]"
tags: [paper, <topic>]
created: YYYY-MM-DD
authors: "<First author> et al."
year: YYYY
venue: "<conference / journal, or arXiv / tech report>"
peer_reviewed: yes | no | stage-1-rr
link: "<arXiv or DOI URL>"
version: "<arXiv v1 / v2 / published>"
paper_type: empirical | method | tech-report | benchmark | system | classic | position | experience | out-of-field
pass: 1 | 2 | 3
pdf: 'F:\papers\<file>.pdf'
---

# <Paper title>

## Five Cs (after Pass 1)

| C | One line |
|---|---|
| Category |  |
| Context |  |
| Correctness |  |
| Contributions |  |
| Clarity |  |

**Verdict:** stop here | Pass 2 | Pass 3, because <reason>

## Summary in my own words

<Three sentences, no copy-paste: the problem, what they did, what they found.>

## Claims -> evidence

| Claim | Evidence (section / figure / table) | Convinced? |
|---|---|---|
|  |  | ✅ / ⚠️ / ❌ |

## Core extract (depends on paper type)

<Empirical: RQs, design, participants/data, variables, metrics, statistics.
Method: the idea, baselines, ablations, failure cases.
Tech report: architecture, data, training recipe, eval setup (self-reported?).
Benchmark: task construction, grading, contamination defense, human baseline.>

## My critique (Pass 3)

| Validity | Threat | Listed by authors? |
|---|---|---|
| Conclusion |  | yes / no |
| Internal |  | yes / no |
| Construct |  | yes / no |
| External |  | yes / no |

## Questions and unknown terms

-

## Follow-up references

- [ ] <ref [n]: why it's worth reading>

## Connections

- [[<related-note>]]: <how it connects>

## Takeaway

<The one concept, method, tool, or reading-list item I'm keeping.>
```

## Reading Log Line (Pass 1 only)

```markdown
| Date | Paper | Type | Five Cs (one line each, separated by /) | Verdict |
|---|---|---|---|---|
| YYYY-MM-DD | <title> (<venue>, <year>) | <type> | <category / context / correctness / contributions / clarity> | stop / Pass 2 later |
```

## Example (filled, abbreviated)

```markdown
---
title: "Understanding Specification-Driven Code Generation with LLMs: An Empirical Study Design"
summary: "[[understanding-specification-driven-code-generation-with-llms]]"
tags: [paper, llm, tdd, empirical-se]
created: 2026-09-20
authors: "Rosa et al."
year: 2026
venue: "SANER 2026 (Registered Report track)"
peer_reviewed: stage-1-rr
link: "https://arxiv.org/abs/2601.03878"
version: "arXiv v1"
paper_type: empirical
pass: 3
pdf: 'F:\papers\Understanding Specification-Driven Code Generation with LLMs An Empirical Study Design.pdf'
---

# Understanding Specification-Driven Code Generation with LLMs: An Empirical Study Design

## Five Cs (after Pass 1)

| C | One line |
|---|---|
| Category | Stage 1 registered report: a study protocol plus a tool description, no results |
| Context | TDD-for-LLM work (TGen, TICODER, LLM4TDD) and human-AI interaction research |
| Correctness | Plausible on Pass 1; Pass 3 finds construct and internal validity gaps |
| Contributions | CURRANTE (a VS Code extension), a study protocol, a telemetry schema |
| Clarity | Readable, with several typos |

**Verdict:** Pass 3, because it's the running example for my reading method.

## Summary in my own words

LLM coding tools rarely make developers pin down requirements before code gets generated. The authors built CURRANTE, a VS Code extension where the developer writes a TOML spec, curates LLM-generated tests, and lets the LLM write the function. They plan a study of how people use it on LiveCodeBench problems. There are no results yet: this is the plan.

## Claims -> evidence

| Claim | Evidence (section / figure / table) | Convinced? |
|---|---|---|
| CURRANTE generates correct code (RQ1) | Planned PassAll / PassRate (Table I, Sec. V-C) | ❌ scored against the participant's own suite, not reference tests |
| Users can express intent through tests (RQ2) | Planned TestEdits, TestCoverage, TestDiversity (Table I) | ⚠️ measures suite properties, not intent |

## My critique (Pass 3)

| Validity | Threat | Listed by authors? |
|---|---|---|
| Conclusion | Analysis "chosen as warranted by the collected data"; no hypotheses or target N | no |
| Internal | No comparison condition, yet causal framing ("influences", "real impact") | no |
| Construct | "Correct" = passes the user's own tests; contamination tension (release_v5 vs newest model) | no |
| External | One IDE, one dataset, one model; medium-difficulty problems only | yes |

## Takeaway

Method: the variable taxonomy (independent / dependent / confounding) and the fine-grained interaction logging are worth reusing. Wait for Stage 2 before citing any finding.
```
