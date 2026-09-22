---
title: "Qwen Technical Report: Pretraining (Data, Tokenization, Architecture)"
tags: [paper, llm, qwen, pretraining, tokenization]
created: 2026-09-20
source: "Qwen Team, Alibaba Group; arXiv:2309.16609v1 [cs.CL], 28 Sep 2023; PDF: F:/papers/Qwen Technical Report.pdf; covers Introduction (pp. 3–4) and Section 2 (pp. 4–8)"
---

# Qwen Technical Report: 01 Pretraining

> *Source: "QWEN Technical Report", Qwen Team, Alibaba Group, arXiv:2309.16609v1 [cs.CL], 28 Sep 2023. This note covers the Introduction (pp. 3–4) and Section 2 "Pretraining" (pp. 4–8). Page numbers are PDF pages (they match printed pages in this source). Headline benchmark numbers live here; the full evaluation deep-dive is in [[04_Evaluation]].*

## Key Idea

Before Qwen could chat, it had to read. The pretraining section describes how the team assembled up to 3 trillion tokens of mostly Chinese and English text plus code, chose an approximately 152K-token vocabulary, and trained three base models (1.8B, 7B, 14B) on a LLaMA-style architecture with a few deliberate deviations. Two choices stand out for anyone training models today: a multilingual data pipeline with aggressive deduplication and quality filtering, and a training-free method that stretches the usable context window at inference time. The payoff claim: the 14B base model outperforms the previous 13B state of the art on all seven reported benchmarks (pp. 4–9).

## Data: built for diversity, filtered for quality (pp. 4–6)

Sources: public web documents, encyclopedia, books, code, "and a significant portion of the data being in English and Chinese" (p. 5). The preprocessing pipeline runs in three motions:

- **Deduplication**: exact-match after normalization, plus fuzzy deduplication with MinHash and LSH.
- **Filtering**: rule-based plus model-based scoring (language models, text-quality scoring models, and offensive content detection), with manual sampling to review sources.
- **Up-sampling**: quality sources get re-weighted so the final mix is diverse and high-quality.

Instruction data was also incorporated into pretraining; to protect evaluation integrity, any instruction sample with a 13-gram overlap with a test set was removed, following the GPT-3 approach (p. 6). Final dataset: up to 3 trillion tokens (p. 6).

## Tokenization: 152K vocabulary, multilingual by design (p. 6)

BPE following the GPT-3.5/4 approach, starting from the open-source tiktoken `cl100k base` vocabulary, then augmented with common Chinese characters and words plus other languages; numbers are split into single digits. Final vocabulary size: approximately 152K. A compression study (Figure 3, p. 6) shows the Qwen tokenizer packing more text per token than XLM-R, LLaMA, Baichuan, and InternLM across most languages (Chinese, English, code, and many others), which reduces serving cost. Preliminary experiments found the larger vocabulary did not hurt downstream performance.

## Architecture: LLaMA-style with deliberate changes (pp. 6–7)

The base is a modified Transformer following the LLaMA recipe, with five documented changes:

- **Untied embedding** (input embedding and output projection separated) for better performance, accepting the memory cost.
- **RoPE positional embeddings** with the inverse-frequency matrix kept in FP32 precision for accuracy.
- **Bias removed** in most layers, but kept in the QKV attention layer to help extrapolation.
- **Pre-Norm + RMSNorm** for stability with equivalent performance and better efficiency.
- **SwiGLU activation**, with the FFN dimension reduced to 8/3 of hidden size.

Table 1 (p. 7) gives the three configurations:

| Params | Hidden | Heads | Layers | LR | Batch (tokens) | Training tokens |
|---|---|---|---|---|---|---|
| 1.8B | 2048 | 16 | 24 | 3.0 × 10−4 | 4M | 2.2T |
| 7B | 4096 | 32 | 32 | 3.0 × 10−4 | 4M | 2.4T |
| 14B | 5120 | 40 | 40 | 3.0 × 10−4 | 4M | 3.0T |

## Training (p. 7)

Standard autoregressive next-token prediction; context length 2048; shuffled and merged documents truncated into batches; Flash Attention; AdamW with β1 = 0.9, β2 = 0.95, ε = 10−8; cosine learning-rate schedule decaying to 10% of peak; BF16 mixed precision for stability.

## Context Length Extension: extend at inference, not in training (pp. 7–9)

Instead of retraining for longer inputs, Qwen applies a training-free stack at inference time:

- **NTK-aware interpolation**: rescales the RoPE frequency base, preserving high-frequency information.
- **Dynamic NTK**: changes the scale by chunks to avoid severe degradation.
- **LogN-Scaling**: rescales attention scores by the context/training length ratio so attention entropy stays stable.
- **Layer-wise window attention**: shorter attention windows in lower layers, longer in higher layers, because lower layers proved more sensitive to context extension.

Table 3 (p. 9), perplexity on arXiv text for QWEN-7B: the baseline degrades from 3.78 at 2,048 tokens to 2,645.09 at 16,384; with the full stack it holds at 4.32. QWEN-14B with the full stack: 3.42 at 16,384. The report's conclusion: the combination maintains performance beyond 8,192 tokens (p. 9).

## Results: three sizes, seven benchmarks (pp. 8–9)

Table 2 (p. 8): MMLU (5-shot), C-Eval (5-shot), GSM8K (8-shot), MATH (4-shot), HumanEval (0-shot), MBPP (3-shot), BBH (3-shot).

| Model | MMLU | C-Eval | GSM8K | MATH | HumanEval | MBPP | BBH |
|---|---|---|---|---|---|---|---|
| QWEN-1.8B | 44.6 | 54.7 | 21.2 | 5.6 | 17.1 | 14.8 | 28.2 |
| QWEN-7B | 58.2 | 63.5 | 51.7 | 11.6 | 29.9 | 31.6 | 45.0 |
| QWEN-14B | 66.3 | 72.1 | 61.3 | 24.8 | 32.3 | 40.8 | 53.4 |
| LLaMA2-13B (reference) | 55.0 | 41.4 | 29.6 | 5.0 | 18.9 | 30.3 | 45.6 |
| LLaMA2-70B (reference) | 69.8 | 50.1 | 63.3 | 13.5 | 29.9 | 45.0 | 64.9 |

Reading the table:

- QWEN-14B outperforms the previous 13B state of the art on all datasets (caption, p. 8), and also beats LLaMA2-70B on three of them: C-Eval, MATH, and HumanEval.
- QWEN-7B surpasses LLaMA2-13B and reaches comparable results with Baichuan2-13B (p. 9).
- QWEN-1.8B stays competitive for its size and, in the report's words, "even outperforms larger models in some instances" (p. 9).
- Figure 2 (p. 5) plots QWEN-14B against GPT-4 and GPT-3.5 across 12 datasets: ahead of the previous 13B SOTA, still behind the proprietary models.

## Memorable Quotes

> "we have implemented simple training-free techniques that are solely applied during inference to extend the context length of the model" (p. 7)

> "Finally, we have built a dataset of up to 3 trillion tokens." (p. 6)

## Related

- [[00_Overview]]: the set map and reading paths
- [[02_Alignment_and_Agents]]: how these base models became chat models
- [[03_Specialized_Models]]: Code-Qwen and Math-Qwen build on this base
- [[04_Evaluation]]: full benchmark tables and the appendix deep-dive

---

*Summary written 2026-09-20 from arXiv:2309.16609v1, the version matching the source PDF. Page numbers are PDF pages; quotes are verbatim and page-cited; everything else is own-words paraphrase.*
