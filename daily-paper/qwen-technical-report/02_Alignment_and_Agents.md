---
title: "Qwen Technical Report: Alignment and Agents (SFT, RLHF, Tool Use)"
tags: [paper, llm, qwen, alignment, rlhf, agents]
created: 2026-09-20
source: "Qwen Team, Alibaba Group; arXiv:2309.16609v1 [cs.CL], 28 Sep 2023; PDF: F:/papers/Qwen Technical Report.pdf; covers Section 3 (pp. 9–16)"
---

# Qwen Technical Report: 02 Alignment and Agents

> *Source: "QWEN Technical Report", Qwen Team, Alibaba Group, arXiv:2309.16609v1 [cs.CL], 28 Sep 2023. This note covers Section 3 "Alignment" (pp. 9–16). Page numbers are PDF pages. The human-evaluation case gallery referenced here is digested in [[04_Evaluation]].*

## Key Idea

Alignment is where Qwen becomes an assistant. The recipe runs in three movements: supervised finetuning on curated conversations in ChatML format, RLHF with a preference-pretrained reward model and PPO, and a deliberate push into agent territory (tool calls, a Python code interpreter, Hugging Face agents). The claims are competitive: the chat models beat every compared open-source model except ChatGPT and LLaMA2-Chat-70B on classic benchmarks, human annotators ranked the RLHF model above both SFT versions and below GPT-4 overall, and the agentic test numbers come impressively close to GPT-4 at a fraction of the size (pp. 9–16).

## SFT: conversations, not templates (pp. 9–10)

The data is annotated multi-style conversation, deliberately human-style rather than prompt-template Q&A, because template formats can limit generalization; safety conversations (violence, bias, pornography) were annotated as well. The format is ChatML (`<|im_start|>` / `<|im_end|>` special tokens that never appear in pretraining, so role markers cannot be confused with ordinary text; rationale in Appendix A.1.1, p. 36).

Training: next-token prediction with the loss masked on system and user turns; sequence length 2048; batch size 128; 4000 steps with roughly 1430 warmup steps to a peak learning rate of 2 × 10−6; weight decay 0.1; dropout 0.1; gradient clipping 1.0 (p. 10).

## RLHF: preference data in, preferences out (pp. 10–11)

The reward model follows a two-step recipe: preference model pretraining (PMP) on comparison pairs, then finetuning on higher-quality annotated comparisons. Data construction: a prompt classification system with 6600 detailed tags and a balanced sampling algorithm that weighs diversity and complexity; responses sampled from Qwen models of different sizes and strategies; annotators follow a standard guideline to form comparison pairs. The reward model itself is a same-size Qwen with a pooling layer that extracts a sentence-level reward at a special end token. Training: constant learning rate 3 × 10−6, batch 64, sequence length 2048, one epoch (pp. 10–11).

Table 4 (p. 11) reports pairwise accuracy: PMP generalizes well to out-of-distribution preference sets (for example, 76.52 on Anthropic Helpful-base), while the finetuned reward model improves on Qwen's own datasets (74.78 versus 62.68 on Qwen Helpful-base).

The RL step is standard PPO with four models (policy, value, reference, reward) plus practical details worth copying: the value model trains alone for 50 steps before PPO for stability; two responses are sampled per query; KL coefficient 0.04; rewards normalized by a running mean; policy learning rate 1 × 10−6 and value learning rate 5 × 10−6; value-loss clipping at 0.15; top-p 0.9 for inference. A "pretrained gradient" term mitigates the alignment tax (degradation of pretrained abilities on non-code/math benchmarks), and the report notes the coefficient must be tuned: too large blocks alignment, too small barely helps (p. 11).

## Benchmarks: where the chat models land (pp. 11–12)

Table 5 (p. 12), reported as 0-shot / few-shot:

| Model | MMLU | C-Eval | GSM8K | HumanEval (0-shot) | BBH |
|---|---|---|---|---|---|
| QWEN-CHAT-1.8B | 42.4 / 43.9 | 50.7 / 50.3 | 27.8 / 19.5 | 14.6 | 27.1 / 25.0 |
| QWEN-CHAT-7B | 55.8 / 57.0 | 59.7 / 59.3 | 50.3 / 54.1 | 37.2 | 39.6 / 46.7 |
| QWEN-CHAT-14B | 64.6 / 66.5 | 69.8 / 71.7 | 60.1 / 59.3 | 43.9 | 46.9 / 58.7 |

Only ChatGPT and LLaMA2-Chat-70B sit ahead across the compared models; HumanEval is where Qwen stands out most against open-source peers (43.9 for the 14B, p. 12).

## Human evaluation: 300 Chinese instructions, ranked by people (pp. 12–13)

Setup: 300 Chinese instructions covering knowledge, language understanding, creative writing, coding, and mathematics; three annotators rank each model's response by helpfulness, informativeness, and validity; compared models: Qwen-7B-Chat (SFT), Qwen-14B-Chat (SFT), Qwen-14B-Chat (RLHF), and GPT-4, against GPT-3.5 as the reference bar.

Results: the RLHF model clearly outperforms the SFT models, which the report reads as evidence that RLHF yields more human-preferred responses, while the series overall stays behind GPT-4. The authors add a caveat: it remains difficult to capture the true gap against proprietary models (pp. 12–13). The per-case gallery with Elo ratings, including cases Qwen wins and loses, is digested in [[04_Evaluation]].

## Agents: tools, interpreter, Hugging Face (pp. 13–16)

The training trick is self-instruct: use Qwen's own in-context learning to generate ReAct-format samples, filter them with rules plus human annotators, iterate, and mix roughly 2000 high-quality samples into the general SFT data instead of adding a separate training stage, so general capabilities are preserved (p. 15).

Three evaluation areas:

1. **Tool selection via ReAct** (Table 6, p. 13): QWEN-CHAT-14B scores 98 on tool selection (GPT-4: 95) and 93 on tool input plausibility (GPT-4: 90), with a 2.4% false-positive rate versus GPT-3.5's 75%, explained partly by the benchmark's Chinese focus (GPT-3.5 attempted tool calls even when no tool fit). The report's own caveat: the benchmark may be relatively easy (p. 15).
2. **Code interpreter** (Tables 7–8, p. 14), three task families (math problem solving, data visualization, general tasks): code executability for QWEN-CHAT-14B is 81.7% overall (math 89.2%, visualization 84.1%, general 65.5%) versus GPT-4's 86.8% and GPT-3.5's 72.9%; final-answer correctness is 56.4% (math 58.4%, hard visualization 53.6%) versus GPT-3.5's 44.2% and GPT-4's 63.8%. Visualization correctness is judged by QWEN-VL, the multimodal sibling. CodeLlama hallucinated non-existent CSV columns on visualization, and the report notes that code-specialist models do not automatically beat generalists on multi-skill agentic tasks (pp. 14–16).
3. **Hugging Face Agent benchmark** (Table 9, p. 15): in chat mode, QWEN-CHAT-14B scores 97.9 tool selection / 97.9 tool used / 95.5 code correctness, essentially matching GPT-4 (97.9 / 97.9 / 98.5); the 7B sits at 94.7 / 94.7 / 85.1.

## Memorable Quotes

> "we find that QWEN-CHAT models trained with RLHF are highly competitive, still falling behind GPT-4 on our benchmark" (p. 4)

> "RLHF can encourage the model to generate responses that are more preferred by humans" (p. 12)

> "specialist models that are optimized for code synthesis do not necessarily outperform generalist models" (p. 16)

## Related

- [[01_Pretraining]]: the base models this alignment starts from
- [[04_Evaluation]]: human-eval gallery and benchmark deep-dive
- [[03_Specialized_Models]]: the code and math specialists
- [[00_Overview]]: the set map

---

*Summary written 2026-09-20 from arXiv:2309.16609v1, the version matching the source PDF. Page numbers are PDF pages; quotes are verbatim and page-cited; everything else is own-words paraphrase.*
