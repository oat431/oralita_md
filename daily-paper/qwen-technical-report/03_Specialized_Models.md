---
title: "Qwen Technical Report: Specialized Models (Code-Qwen, Math-Qwen)"
tags: [paper, llm, qwen, code, math]
created: 2026-09-20
source: "Qwen Team, Alibaba Group; arXiv:2309.16609v1 [cs.CL], 28 Sep 2023; PDF: F:/papers/Qwen Technical Report.pdf; covers Sections 4–5 (pp. 16–20)"
---

# Qwen Technical Report: 03 Specialized Models

> *Source: "QWEN Technical Report", Qwen Team, Alibaba Group, arXiv:2309.16609v1 [cs.CL], 28 Sep 2023. This note covers Section 4 "CODE-QWEN" and Section 5 "MATH-QWEN" (pp. 16–20). Page numbers are PDF pages.*

## Key Idea

On top of the general base, Qwen ships two specialist lines: Code-Qwen (7B and 14B, with chat versions) and Math-Qwen-Chat (7B and 14B). The design philosophy is uniform and stated up front: keep the generalist core, then continue training on domain data, because a pure code specialist loses assistant versatility (p. 16). Headline results: Code-Qwen-Chat-14B reaches 66.4% pass@1 on HumanEval (up from 43.9% for the generalist chat model of the same size) and averages 51.9% across six languages on HumanEvalPack; Math-Qwen-Chat-14B reaches 69.8% on GSM8K and beats GPT-3.5 on arithmetic and Chinese math benchmarks. Both lines still trail GPT-4, which the report states plainly (pp. 16–20).

## Code-Qwen: continued pretraining, not lobotomy (pp. 16–18)

- **Continued pretraining** on about 90 billion tokens of code, starting from the text+code generalist base rather than from scratch on code data; context length extended up to 8192 to support tool use and code interpretation scenarios.
- **Training**: learning rate 6.0 × 10−5 (14B) and 3.0 × 10−5 (7B), 3% warmup, no decay; then a multi-stage SFT chosen after empirical comparison, with learning rates 2.0 × 10−6 (14B) and 1.0 × 10−5 (7B), cosine warmup at 3% and then constant (pp. 16–17).

Results, pass@1 on HumanEval / MBPP (Table 10, p. 18):

| Model | HumanEval | MBPP |
|---|---|---|
| CODE-QWEN-7B (continued pretrain) | 40.2 | 41.8 |
| CODE-QWEN-CHAT-7B | 43.3 | 44.2 |
| CODE-QWEN-14B (continued pretrain) | 45.1 | 51.4 |
| CODE-QWEN-CHAT-14B | 66.4 | 52.4 |
| QWEN-CHAT-14B (generalist reference) | 43.9 | 46.4 |
| WizardCoder-Python-34B (reference) | 73.2 | 61.2 |
| GPT-3.5 / GPT-4 (reference) | 73.2 / 86.6 | - |

Multilingual code (Table 11, p. 19): HumanEvalPack zero-shot pass@1 average across Python, JavaScript, Java, Go, C++, and Rust is 51.9 for Code-Qwen-Chat-14B (Python 66.4, JavaScript 58.5, Java 56.1, Go 47.6, C++ 54.2, Rust 28.7), versus 78.3 average for GPT-4, 40.5 for WizardCoder, and 35.5 for OctoCoder.

The report's claims: Code-Qwen significantly outperforms same-size baselines such as OctoGeeX, InstructCodeT5+, and CodeGeeX2, and even rivals larger models like StarCoder; it also notes that these tables are not enough to judge true strengths and weaknesses (p. 17).

## Math-Qwen: instruction tuning with a masking trick (pp. 17–20)

- **Recipe**: math SFT directly on an augmented math instruction dataset (no math-specific pretraining phase), producing the chat model; sequence length 1024 for faster training.
- **Masking**: the system and user turns are excluded from the loss ("we mask the inputs of the system and user to avoid loss computation on them"), because predicting examination questions and possibly random numbers is meaningless; the report found masking accelerates convergence in preliminary experiments (p. 20).
- **Optimization**: AdamW with the same hyperparameters as the main SFT run, peak learning rate 2 × 10−5, and 50,000 training steps (p. 20).

Results (Table 12, pp. 19–20):

| Model | GSM8K | MATH | Math401 | Math23K |
|---|---|---|---|---|
| MATH-QWEN-CHAT-7B | 62.5 | 17.2 | 80.8 | 75.4 |
| MATH-QWEN-CHAT-14B | 69.8 | 24.2 | 85.0 | 78.4 |
| GPT-3.5 (reference) | 80.8 | 34.1 | 75.1 | 60.0 |
| GPT-4 (reference) | 92.0 | 42.5 | 83.5 | 74.0 |
| WizardMath-70B (reference) | 81.6 | 22.7 | - | - |
| Minerva-8B / 62B (reference) | 16.2 / 52.4 | 14.1 / 27.6 | - | - |

The report's reading: the 7B beats Minerva-8B on MATH (17.2 versus 14.1); the 14B is "chasing" Minerva-62B and GPT-3.5 on GSM8K and MATH while outperforming GPT-3.5 on arithmetic (Math401 85.0 versus 75.1) and Chinese math (Math23K 78.4 versus 60.0) (p. 20).

## Memorable Quotes

> "We believe that relying solely on code data for pretraining can result in a significant loss of the ability to function as a versatile assistant." (p. 16)

> "these models fall behind the state-of-the-art methods, such as GPT-4, in general. Nonetheless, with the continued scaling of both model size and data size, we believe that this gap can be narrowed in the near future." (p. 17)

## Related

- [[01_Pretraining]]: the base models these lines continue from
- [[02_Alignment_and_Agents]]: alignment techniques reused for the specialists
- [[04_Evaluation]]: full evaluation material
- [[00_Overview]]: the set map

---

*Summary written 2026-09-20 from arXiv:2309.16609v1, the version matching the source PDF. Page numbers are PDF pages; quotes are verbatim and page-cited; everything else is own-words paraphrase.*
