---
title: "Qwen Technical Report: Evaluation (Benchmarks, Human Eval, Case Studies)"
tags: [paper, llm, qwen, evaluation, benchmarks]
created: 2026-09-20
source: "Qwen Team, Alibaba Group; arXiv:2309.16609v1 [cs.CL], 28 Sep 2023; PDF: F:/papers/Qwen Technical Report.pdf; covers Appendix A.2–A.3 (pp. 36–59) plus evaluation framing (pp. 11–13, 17)"
---

# Qwen Technical Report: 04 Evaluation

> *Source: "QWEN Technical Report", Qwen Team, Alibaba Group, arXiv:2309.16609v1 [cs.CL], 28 Sep 2023. This note is the tests file: the appendix benchmark deep-dive (A.2.1, pp. 36–40), the human-evaluation case gallery (A.2.2, pp. 40–58), and the code-interpreter analysis (A.3, pp. 58–59), with evaluation framing from the main text (pp. 11–13, 17). Headline numbers for each model family live in [[01_Pretraining]], [[02_Alignment_and_Agents]], and [[03_Specialized_Models]]. Page numbers are PDF pages.*

## Key Idea

This file answers "how do we know it works" with three layers of evidence: automatic benchmarks run against the OpenCompass category set and reported in full in the appendix; a human evaluation on 300 Chinese instructions where annotators ranked outputs and individual cases carry Elo ratings; and a qualitative agent test showing a two-step planning win. The most valuable part is the honesty: the report says outright that traditional benchmarks under-measure aligned chat models and that more rigorous tests are needed (pp. 12, 17).

## How the tests were run (p. 36)

- The automatic evaluation follows OpenCompass categories: examination, language, knowledge and understanding, and reasoning. Protocols per benchmark: 5-shot for MMLU, C-Eval, and CMMLU; zero-shot for AGIEval, Gaokao-Bench, and ARC; 8-shot for CommonsenseQA; and so on.
- For baselines, the report takes the better result between the models' own reported scores and the leaderboard values (p. 36).
- Fairness note from the authors: Chinese benchmarks heavily penalize models not optimized for Chinese (LLaMA, MPT, Falcon score low on CMMLU, AGIEval, Gaokao-Bench), which explains part of the gaps (p. 38).

## Base-model deep results, appendix tables 13–17

All values are the QWEN base models (1.8B / 7B / 14B):

| Category | Benchmark | 1.8B | 7B | 14B |
|---|---|---|---|---|
| Examination | MMLU (5-shot) | 44.6 | 58.2 | 66.3 |
| Examination | C-Eval (5-shot, average) | 54.7 | 63.5 | 72.1 |
| Examination | C-Eval (hard subset) | 41.8 | 46.4 | 53.7 |
| Examination | CMMLU (5-shot) | 49.3 | 62.2 | 71.0 |
| Examination | AGIEval (zero-shot) | 36.9 | 45.8 | 52.3 |
| Examination | Gaokao-Bench (zero-shot) | 44.9 | 52.5 | 61.9 |
| Examination | ARC-e / ARC-c | 71.6 / 53.2 | 84.0 / 75.3 | 90.3 / 84.4 |
| Knowledge | BoolQ | 68.0 | 76.4 | 86.2 |
| Knowledge | CommonsenseQA | 60.1 | 66.8 | 70.3 |
| Knowledge | NaturalQuestions | 3.2 | 17.4 | 23.9 |
| Knowledge | LAMBADA | 58.4 | 67.9 | 71.1 |
| Reasoning | HellaSwag | 56.7 | 75.1 | 80.2 |
| Reasoning | PIQA | 73.3 | 77.9 | 79.9 |
| Reasoning | SIQA | 56.1 | 69.9 | 77.9 |
| Reasoning | OCNLI | 39.0 | 47.4 | 57.9 |

Reading the full picture:

- **Chinese examinations are the strong suit.** On C-Eval, QWEN-14B's 72.1 average sits above GPT-4's 68.7 and GPT-3.5's 54.4 in the same table, though its hard-subset score (53.7) stays just below GPT-4's 54.9; the MMLU total (66.3) is just under LLaMA2-70B's 68.9 while its subject breakdown is strong (STEM 59.4, social sciences 76.2, humanities 60.9).
- **Knowledge is mixed.** Strong BoolQ and CommonsenseQA; NaturalQuestions is a visible weak spot (23.9 versus LLaMA2-70B's 34.2).
- **Reasoning splits by task.** SIQA (77.9) and OCNLI (57.9) lead the big open models by wide margins, while HellaSwag (80.2) and PIQA (79.9) trail LLaMA2-70B (85.3 and 82.8).

## Human evaluation: the case gallery with Elo ratings (A.2.2, pp. 40–58)

Structure: the dataset mixes manually written instructions with ones revised from public sources (CLiB, C-Eval, FacTool, LeetCode). Every case shows each model's response plus an Elo rating, in Chinese with English translations. Eight representative cases across five categories, including wins and losses:

| Case | Category | Qwen best (Elo) | GPT-4 (Elo) | Reading |
|---|---|---|---|---|
| Peking University predecessor | Knowledge | 14B-RLHF 1090 | 955 | RLHF answer, the most detailed, rated top; GPT-3.5 lowest at 910 |
| Tallest wooden tower | Knowledge | 14B-RLHF 1060 | 1040 | Qwen edges out; GPT-3.5 rated 864 for answering with a different pagoda |
| Pinyin for a tongue twister | Language | 14B-RLHF 1068 | 1040 | Qwen 14B variants ahead of GPT-4 (1040) and GPT-3.5 (946) |
| Supermarket fruit joke | Creative writing | 14B-RLHF 986 | 1144 | Clear GPT-4 win; Qwen's 7B-SFT lowest at 849 |
| Square of five rectangles | Math | 14B-RLHF 1139 | 1010 | Only the RLHF model solves it (100 centimeters); GPT-4's walkthrough lands on 60 |
| Class in six rows | Math | 14B-RLHF 1139 | 1010 | Qwen-14B variants and GPT-4 reach 42; GPT-3.5 gets 11 |
| Regex for 139-prefixed numbers | Code | 14B-RLHF 1090 | 1134 | GPT-4 rated top; both Qwen SFT variants sit at 941 |
| Binary tree max-depth debugging | Code | 14B-RLHF 992 | 1095 | GPT models pinpoint the actual bug; 7B-SFT wrongly says the code is correct (876) |

Pattern: Qwen is strong on Chinese knowledge, language, and several math cases; GPT-4 stays ahead on creative writing and precise debugging, and small models err visibly. Note that Elo captures overall response quality as judged by annotators, not just correctness (for example, the terse correct GPT-4 answer to the Peking University question rated below the longer RLHF answer).

## Code interpreter case study (A.3, pp. 58–59)

The closing figure compares QWEN-CHAT with CodeLlama on a plotting task over a CSV file: Qwen plans in two steps, first inspecting which columns exist, then writing the plotting code; CodeLlama attempts the plot using non-existent columns and produces hallucinated output, and is only reliable when the columns are given in the query. It is a small but concrete picture of planning plus tool use working together.

## Where the report admits limits

- Traditional benchmarks under-measure aligned chat models; the report explicitly says it has reservations and calls for new evaluation methods tailored to them (p. 12).
- The evaluation of the code specialists is judged insufficient for capturing true strengths and weaknesses (p. 17).
- The human evaluation samples only 300 Chinese instructions, and the authors state it remains difficult to capture the gap versus proprietary models (pp. 12–13).

## Memorable Quotes

> "we have reservations about the ability of traditional benchmark evaluation to accurately measure the performance and potential of chat models trained with alignment techniques in today's landscape" (p. 12)

> "it is necessary to develop more rigorous tests to enable us to accurately assess our relative performance in comparison to GPT-4" (p. 17)

## Related

- [[01_Pretraining]] / [[02_Alignment_and_Agents]] / [[03_Specialized_Models]]: headline numbers for each family
- [[00_Overview]]: the set map and reading paths

---

*Summary written 2026-09-20 from arXiv:2309.16609v1, the version matching the source PDF. Page numbers are PDF pages; quotes are verbatim and page-cited; everything else is own-words paraphrase.*
