---
title: "GLM: General Language Model Pretraining with Autoregressive Blank Infilling"
tags: [paper, pretraining, language-model, architecture, nlp]
created: 2026-09-23
revised: 2026-09-23
source: "Du, Qian, Liu, Ding, Qiu, Yang, Tang (Tsinghua, BAAI, MIT CSAIL); GLM: General Language Model Pretraining with Autoregressive Blank Infilling; ACL 2022 (Long Papers), Dublin, pp. 320-335; arXiv:2103.10360v2 [cs.CL], 16 pp.; PDF: F:/papers/GLM General Language Model.pdf"
---

# GLM: General Language Model Pretraining with Autoregressive Blank Infilling

> *Paper: Zhengxiao Du, Yujie Qian, Xiao Liu, Ming Ding, Jiezhong Qiu, Zhilin Yang, Jie Tang (Tsinghua University, BAAI, MIT CSAIL, Shanghai Qi Zhi Institute). "GLM: General Language Model Pretraining with Autoregressive Blank Infilling." ACL 2022 (60th Annual Meeting, Dublin), Long Papers, pp. 320-335; the PDF here is arXiv:2103.10360v2 [cs.CL], 17 Mar 2022. Page numbers in the appendix are the arXiv version's printed pages 1-16, identical to the PDF pages (the ACL pagination was confirmed externally via the ACL Anthology). Code: `https://github.com/THUDM/GLM`.*

## What This Paper Is, In Plain Words

Back in 2021, the language-model world was split into three camps, and each camp had a specialist who could not do the other camps' jobs.

Picture three kinds of language experts. The first is a brilliant editor: that is the BERT-style "autoencoder." The editor reads a whole sentence at once, forwards and backwards, so they know exactly what each word means in context. But ask the editor to write an essay and they freeze; they were only ever trained to restore deleted words, one slot at a time, and they treat every deleted word as if it were independent of the others. The second expert is a natural storyteller: the GPT-style "autoregressive" model. The storyteller writes fluently, one word at a time, but can only ever look backwards over their shoulder. With no way to see what is coming, they are weaker at the careful whole-sentence reading where the editor shines. The third is a translation booth with two rooms: the T5-style "encoder-decoder," a reader and a writer joined by a pipe. It handles "read this, produce that" jobs like summarization nicely, but the two-room setup is expensive, needing many more parameters to match the lone editor on reading tasks.

The authors' diagnosis is blunt: no single one of these frameworks performs competitively across all the tasks people care about. Earlier attempts to combine them (UniLM and friends) mostly stacked the two training objectives side by side, and because the objectives differ by nature, a simple unification cannot fully inherit the advantages of both.

GLM's answer is disarmingly simple: make everyone play the same game, a fill-in-the-blanks exercise that secretly teaches writing.

## The Core Idea: Fill-in-the-Blanks That Teaches Writing

Here is the game. Take a passage of text and blank out a few random chunks. Every chunk, no matter how long, is replaced by a single blank marker, like one underline instead of one per missing word. The blanks are collected onto an answer sheet in shuffled, random order. The model's job is to fill in each blank, word by word, like the storyteller, while being allowed to look at the whole passage and at the answers it has already written, but never at the answers still to come.

That one exercise fuses the three camps. Blank-filling is the editor's training. Writing each answer word by word is the storyteller's skill. And because an answer can be a whole chunk, even a whole sentence or half a document, rather than a single word, the model learns genuine open-ended generation on the way. The shuffling matters too: if answers always came left to right, the model could lean on lazy habits, and the paper's own ablations show the shuffle is one of the most load-bearing parts of the design.

## One Model, Two Ways of Seeing

How can a single network do both the whole-passage reading and the word-by-word writing? The trick is a rule about who is allowed to see whom. The input is split into two parts. Part A is the passage with its blanks, and inside Part A every word can see every other word in both directions: editor mode. Part B is the answer sheet, and inside Part B each answer can see all of Part A plus the answers already written, but never the ones that come later: storyteller mode. One model, two ways of seeing, selected purely by the visibility rules. The model is never told which mode to use; the setup makes it grow an encoder for Part A and a decoder for Part B all by itself.

## Hiding the Length of the Blank

One more piece of design makes open-ended writing possible: the model is deliberately kept in the dark about how much text is missing. A ten-word chunk and a one-word chunk both become the same single blank marker, and the position numbers restart inside each answer instead of remembering where the answer sat in the original passage. Why care? Because at generation time you do not know how long the output should be. Rival approaches leak the answer length (XLNet keeps original positions, SpanBERT uses one mask per missing token), and that quietly constrains what the model can do downstream. GLM's encoding hides the blank's length, so the model keeps writing until it decides to stop.

## Turning Every Task Into a Cloze Question

To make this blank-filler do ordinary jobs like sentiment classification, the authors borrow an idea called PET: rewrite every task as a fill-in-the-blanks question in plain language. Sentiment becomes "This review was glowing. It's really ____," where the word "good" stands for positive and "bad" stands for negative; the model fills the blank and the probability of those label words is the prediction. Because GLM writes answers word by word, it handles multi-word answers naturally, something BERT-style cloze cannot do without enumerating lengths. The same interface covers classification, summarization, and free generation.

## Did It Work?

Yes, convincingly. At the same size and on the same training data, GLM beat BERT on the SuperGLUE understanding suite by roughly five points, matched or beat the translation-booth models on summarization and question generation, and in a slightly larger multi-task form did all three job families from a single checkpoint, competing with the best specialist in each family. The lesson the paper leaves behind: a better-chosen training game can beat brute-force scaling. The gains come from how the blanks are made, shuffled, and filled, not from more parameters.

## Why It Still Matters

This is the founding paper of the GLM family from Zhipu AI and Tsinghua, the lineage behind ChatGLM, GLM-4, and today's GLM-5 series, so it explains the name on every Z.ai model card. And its central claim, that one well-designed objective can unify understanding and generation, has since become the field's default assumption.

---

# Appendix: The Dense Details

## Why This Paper Matters

- **It unified the three pretraining families with one objective.** Instead of multi-task bolt-ons (UniLM's mask switching), autoregressive blank infilling is a single loss whose behavior changes just by varying the number and lengths of masked spans (p. 2).
- **It made NLU a generation task.** Following PET, classification becomes cloze-question answering, and unlike BERT, GLM handles multi-token answers naturally through autoregression (p. 2).
- **The 2D positional encoding trick still echoes today.** Hiding span length from the model (one [MASK] regardless of how much text is missing) is what makes generation with unknown output length possible (pp. 3-4).
- **It is the origin of a major open model family:** the GLM name in Zhipu's ChatGLM/GLM-4/GLM models traces directly to this framework.

## The Problem: Three Families, None General (pp. 1-2)

Each pretraining family of the era had a structural weakness:

| Family | Example | Strength | Weakness |
|---|---|---|---|
| Autoregressive | GPT | Long-text generation, few-shot ability at scale | Unidirectional attention cannot fully capture dependencies between context words for NLU |
| Autoencoding | BERT | Bidirectional contextualized representations for NLU | Cannot be directly applied to text generation; MLM assumes masked tokens are independent |
| Encoder-decoder | T5, BART | Conditional generation (summarization, seq2seq) | Needs more parameters to match autoencoders on NLU (T5-Large 770M vs BERT-Large 340M) |

Prior unification attempts (UniLM, UniLMv2) combined objectives via multi-task learning under masked language modeling, but "since the autoencoding and autoregressive objectives differ by nature, a simple unification cannot fully inherit the advantages of both frameworks" (p. 2).

## The GLM Objective: Autoregressive Blank Infilling (pp. 2-3)

Given input text x, sample multiple spans, replace each span with a single [MASK] token to form the corrupted text (Part A), and put the masked spans, shuffled into random order, into Part B. The model learns to reconstruct the spans autoregressively: when predicting a span, it sees the corrupted text and the previously predicted spans. The objective maximizes the log-probability of each span given the corrupted text and earlier spans in the permutation, averaged over random permutations (Eq. 1), with each span generated left-to-right internally (Eq. 2).

The attention mask is the heart of the design (Figure 2d):

- **Part A tokens** attend to each other (bidirectional) but never to Part B.
- **Part B tokens** attend to Part A and their antecedents in Part B, never to subsequent tokens.

So the model "automatically learns a bidirectional encoder (for Part A) and a unidirectional decoder (for Part B) in a unified model" (p. 3). Spans are wrapped in [START] and [END] special tokens. Span lengths are drawn from a Poisson distribution with λ = 3, resampled until at least 15% of tokens are masked; the paper notes "the 15% ratio is critical for good performance on downstream NLU tasks" (p. 3).

### 2D Positional Encoding (pp. 3-4)

Each token gets two positional ids: the position of its [MASK] (or original position) in the corrupted text, and the intra-span position (0 for Part A tokens, 1 to span length for Part B). Both are learned embeddings added to the token embeddings. The consequence: the model cannot perceive the length of a masked span while reconstructing it, unlike XLNet (which keeps original positions and must know or enumerate answer lengths) and SpanBERT (which uses one [MASK] per token, fixing the length). That design fits downstream generation, where output length is unknown beforehand (p. 4).

### Multi-Task Pretraining for Generation (p. 3)

To handle generation as well as NLU, a second objective is mixed in by changing only the span configuration:

- **Document-level (GLM-Doc):** one span covering a uniform 50%-100% of the document, aiming at long text generation.
- **Sentence-level (GLM-Sent):** masked spans restricted to full sentences covering 15% of tokens, aiming at seq2seq tasks whose outputs are complete sentences.

### Architecture Details (p. 3)

A single Transformer with three modifications: post-layer-norm rearrangement (residual connection before normalization, following Megatron-LM's guidance for numerical stability at scale), a single linear output layer, and GeLU activations replacing ReLU.

## Finetuning: NLU as Cloze Questions (p. 4)

Following PET, each NLU example (x, y) becomes a cloze question c(x) written in natural language with one [MASK], and labels map to verbalizer words v(y). Sentiment classification becomes "{SENTENCE}. It's really [MASK]" with "positive"/"negative" mapped to "good"/"bad"; the label probability is the softmax over verbalizer predictions (Eq. 3), trained with cross-entropy. Unlike BERT-based PET, GLM handles multi-token answers natively via autoregressive blank filling (p. 2). For generation tasks, the context is Part A with a mask appended, and Part B is generated autoregressively, directly or after finetuning.

## How GLM Differs From Its Neighbors (pp. 4-5)

- **vs BERT:** MLM's independence assumption misses interdependencies among masked tokens, and BERT cannot fill multi-token blanks without enumerating lengths (p. 4).
- **vs XLNet:** both are autoregressive, but XLNet's original-position encoding leaks answer length, and its two-stream self-attention doubles pretraining time (p. 4).
- **vs T5:** T5 shares the blank-infilling idea but is an encoder-decoder with independent positional encodings, multiple sentinel tokens (wasted capacity downstream, since only one sentinel is used), and a fixed left-to-right span order. GLM is a single encoder that shuffles spans and uses one [MASK] (pp. 4-5, and the ablation on p. 8).
- **vs UniLM/UniLMv2:** UniLM switches attention masks but always replaces spans with [MASK] tokens, limiting dependency modeling; GLM unifies NLU and generation under autoregressive pretraining instead (pp. 4-5).

## Experiments (pp. 5-8)

**Setup (p. 5).** GLM-Base (110M) and GLM-Large (340M) mirror BERT's architectures and train on BooksCorpus + English Wikipedia with BERT's 30k wordpiece tokenizer. Multi-task variants GLM-Doc and GLM-Sent are Large-sized; GLM-410M (30 layers, hidden 1024, 16 heads) and GLM-515M (30 layers, hidden 1152, 18 heads) scale up with document-level multi-task pretraining. GLM-RoBERTa matches RoBERTa's data recipe (158GB of uncompressed text, close to RoBERTa's 160GB) but trains for only 250,000 steps, half of RoBERTa and BART, due to resource limits. Training runs on 64 V100 GPUs, batch size 1024, about 2.5 days for GLM-Large (p. 11, Appendix A).

**SuperGLUE (Table 1, p. 6).** GLM-Base averages 70.7 versus BERT-Base 66.1 (+4.6%); GLM-Large 77.0 versus BERT-Large 72.0 (+5.0%). The only task where BERT wins is WiC (word sense disambiguation). Scaled multi-task models keep improving: GLM-410M 78.0, GLM-515M 78.8. Against larger-corpus baselines, GLM-RoBERTa averages 82.9, beating T5-Large (81.2) at roughly half the parameters and edging RoBERTa-Large (81.5). Among multi-task variants, GLM-Sent beats GLM-Doc by 1.1% on average (p. 6).

**Seq2seq (Tables 2-4, pp. 6-7).** On Gigaword summarization GLM-Large reaches 38.6 RG-1 versus UniLM-Large 38.5 and MASS 37.7; on SQuAD question generation GLM-410M tops the table (22.9 BLEU-4). On CNN/DailyMail and XSum, GLM-RoBERTa matches BART-Large and outperforms T5-Large and UniLMv2 (XSum RG-1 45.5 vs BART 45.1, T5-Large 40.9). The pattern: GLM-Sent helps conditional generation, GLM-Doc slightly hurts it, because the document-level objective teaches extending context rather than extracting from it (p. 6).

**Text infilling (Table 5, p. 7).** On Yahoo Answers, GLM-Large beats BERT and the purpose-built Blank Language Model at every mask ratio (10%-50%), by 1.3 to 3.9 BLEU: state of the art on the task the objective was designed for (p. 7).

**Zero-shot language modeling (Figure 4, p. 7).** Without a generative objective, GLM-Large cannot do language modeling at all (perplexity over 100). GLM-Doc at equal parameters trails GPT-Large (expected, since it also optimizes blank infilling), but GLM-410M (1.25x) roughly matches GPT-Large and GLM-515M (1.5x) surpasses it; encoding the context bidirectionally improves language modeling further, an advantage unidirectional GPT cannot use. Removing 2D positional encoding lowers LAMBADA accuracy and raises perplexity (p. 7).

**Ablations (Table 6, p. 8).** Four findings: (1) a reproduced BERT-Large under the authors' own implementation scores 71.2, still far below GLM-Large's 77.0, confirming the objective, not the implementation, carries the gain; (2) cloze-style finetuning is critical for GLM: finetuning as a plain sequence classifier drops it from 77.0 to 70.0, a 7-point swing, while autoregressive pretraining lets GLM beat cloze-finetuned BERT especially on multi-token-answer tasks (ReCoRD, WSC); (3) removing span shuffling (always left-to-right) collapses the average to 68.5, with RTE falling from 74.0 to 54.5; (4) replacing the single [MASK] with T5-style sentinel tokens costs a point (76.0), because capacity is wasted learning tokens that single-blank downstream tasks never use. The paper notes T5 is approximately GLM minus span shuffling plus sentinel tokens (p. 8).

**Other benchmarks (Appendix C, p. 15).** On GLUE, GLM-Large averages 85.1 versus BERT-Large 84.4; on SQuAD v1.1/v2.0 dev, GLM-Large reaches 85.4/91.6 EM/F1 versus BERT-Large 84.1/90.9 and 80.3/83.3: consistent wins, smaller margins than SuperGLUE.

## Takeaways (for practitioners)

1. **Objective design can beat architecture scaling.** GLM's gains over BERT come from how spans are masked, ordered, and reconstructed, not from more parameters; T5 needed 770M to do what GLM-Large did at 340M.
2. **One loss, three task families:** vary the span configuration (short Poisson spans for NLU, full sentences for seq2seq, half-to-full documents for generation) and the same model covers all three.
3. **Hide answer length from the model.** The single-[MASK] plus 2D-position design is what enables open-ended generation; any scheme that leaks span length (XLNet positions, SpanBERT multi-masks) constrains downstream use.
4. **Span shuffling is load-bearing:** the ablation shows a 8.5-point average SuperGLUE drop without it, the largest single ablation effect in the paper.
5. **Finetuning format matters as much as pretraining:** cloze-style (PET) finetuning is worth 7 SuperGLUE points for GLM, while the same trick barely helps BERT. Match the finetuning interface to the pretraining objective.
6. **Multi-task pretraining trades a little NLU for generation breadth:** GLM-Doc/Sent score slightly below pure GLM-Large on SuperGLUE but unlock summarization, question generation, and language modeling in one checkpoint; scaling to 1.25x parameters recovers and exceeds the pure-NLU model.

## Memorable Quotes

> "None of these pretraining frameworks is flexible enough to perform competitively across all NLP tasks." (p. 2)

> "our model automatically learns a bidirectional encoder (for Part A) and a unidirectional decoder (for Part B) in a unified model" (p. 3)

> "Our encoding method ensures that the model is not aware of the length of the masked span when reconstructing them." (pp. 3-4)

> "we conclude that GLM effectively shares model parameters across natural language understanding and generation tasks, achieving better performance than a standalone BERT, encoder-decoder, or GPT model." (p. 8)

## Related

- Source PDF: `F:/papers/GLM General Language Model.pdf`
- Code and pretrained models: `https://github.com/THUDM/GLM`
- ACL Anthology record (external): aclanthology.org/2022.acl-long.26, DOI 10.18653/v1/2022.acl-long.26

---

*Summary written 2026-09-23; restructured into plain-language body + dense appendix on the same date. Page numbers are the arXiv v2 printed pages 1-16 (identical to PDF pages); the ACL 2022 venue and pp. 320-335 come from the ACL Anthology (external, labeled where used). Quotes are verbatim; everything else is own-words paraphrase. References (pp. 9-11), hyperparameter tables (Appendix A), cloze-question templates (Appendix B.1), and generation samples (Appendix D) are not summarized. The Zhipu/GLM-5 family context line is external background, not from the paper.*
