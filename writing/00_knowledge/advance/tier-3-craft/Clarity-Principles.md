---
title: Clarity Principles
tags: [writing, craft, clarity]
---

# Clarity Principles

> **Question it answers:** how do I reduce the reader's unnecessary cognitive effort?

Clear writing is writing that doesn't make the reader work harder than the subject demands. The principle is not "use small words" — it's "remove every obstacle that isn't load-bearing."

## Prefer

- Concrete nouns
- Precise verbs
- Defined technical terms
- Short sentences for critical instructions
- Explicit logical relationships
- Consistent terminology
- Examples after abstract explanations
- Headings that describe section content

## Avoid

- Unnecessary jargon
- Ambiguous pronouns
- Hidden assumptions
- Excessive nominalization
- Repeated qualifications
- Long introductory phrases
- Decorative complexity
- Unexplained abbreviations
- Multiple terms for the same concept

## The Core Enemy: Nominalization

Nominalization turns a verb into a noun and buries the action:

```mermaid
flowchart LR
    BAD["The implementation of the configuration modification was performed by the administrator"] --> GOOD["The administrator changed the configuration"]
```

The second version is shorter, clearer, and more direct. Nominalization is the single most common cause of dense, hard-to-read prose — hunt it down.

## Key Principles

### One Term, One Meaning

Call the same concept by the same name throughout. Two terms for one thing create false distinctions; one term for two things hides real ones.

### Concrete Before Abstract

State the specific, then the general. An abstract statement followed by a concrete example lands; a concrete example buried under abstraction is lost.

### Say What You Mean Directly

Ambiguous pronouns, hidden assumptions, and long introductions all force the reader to reconstruct your meaning. Make the relationship explicit.

## Common Pitfalls

- **Nominalization everywhere:** actions buried in nouns
- **Jargon without definition:** technical terms the reader can't decode
- **Multiple terms for one concept:** false distinctions that confuse
- **Decorative complexity:** writing that sounds impressive but obscures

## Quality Criterion

> The reader understands the meaning on first pass, without reconstructing it — every term defined, every action visible, every obstacle removed.

## Template

> Copy this skeleton into a new note; name live files `YYYYMM-DD-<slug>.md`.

```markdown
---
date: YYYY-MM-DD
tags: [writing, clarity]
---

# <Piece> — Clarity pass

## Nominalization hunt
| Before (nominalized) | After (direct verb) |
|---|---|

## Term consistency
- <concept> = <the ONE term used throughout>

## Assumptions made visible
- <any hidden premise to state explicitly>

## Read-aloud check
<read it aloud — where does the reader stumble?>
```

## Related

- [[Tone-Voice-Style]]: clarity is style's primary duty
- [[Evidence-Source-Use]]: distinguishing fact from assumption
- [[00-Writing-Types-Reference]]: the multidimensional model
- [[writing/00_knowledge/advance/tier-3-craft/00_overview|Tier 3 overview]]

## Sources

- Readability Formulas, "The Hidden Pitfalls of Nominalizations" (https://readabilityformulas.com/the-hidden-pitfalls-of-nominalizations/)
- Word Frequency Analyzer, "Plain Language for Technical Teams" (https://word-frequency-analyzer.com/blog/plain-language-for-technical-teams-before-after)
