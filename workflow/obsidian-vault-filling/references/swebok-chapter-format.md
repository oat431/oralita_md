# SWEBOK Chapter Format

When filling the `swe-knowledge` Obsidian vault (`F:\obsidian_note\swe-knowledge\body-of-knowledge\SWEBOK\`), all SWEBOK chapters follow this exact structure.

## File Naming

- Pattern: `{NN}_{Title_With_Underscores}.md`
- NN is zero-padded two digits (00–19+)
- 00 = Introduction, 01–15 = SWEBOK v4 Software Engineering KAs, 16–18 = Foundations, 19+ = supplementary chapters

## YAML Frontmatter

```yaml
---
tags:
- software-engineering
- swebok
---
```

Add topic-specific tags when relevant (e.g., `future-trends`, `emerging-technology`).

## Chapter Structure

Every chapter follows this exact section order:

### 1. Purpose Blockquote
```markdown
> **Purpose:** [One-paragraph description of what this KA covers and why it matters.]
```

### 2. Knowledge Areas
Top-level `## Knowledge Areas` heading, then `### N. Topic Name` sub-headings. Each sub-topic uses bold-term definitions:
```markdown
### 1. Topic Name
- **Sub-topic A:** Definition and explanation in one paragraph.
- **Sub-topic B:** Definition and explanation.
```

### 3. Essential Concepts
`## Essential Concepts` — a bullet list of the 10–15 most important ideas, each with a bold term and one-sentence explanation:
```markdown
- **Concept Name:** One-sentence definition or explanation.
```

### 4. Tools & Techniques Mentioned
`## Tools & Techniques Mentioned` — categorized bullet list of concrete tools, standards, frameworks:
```markdown
- **Category Name:** Tool1, Tool2, Tool3 — brief context
```

### 5. Related SWEBOK Chapters
`## Related SWEBOK Chapters` — wikilinks to other chapters with brief context:
```markdown
- [[01_Software_Requirements]]: What connects this KA to Requirements
- [[03_Software_Design]]: What connects this KA to Design
```

## Source Material

- Primary source: `F:\books\Body_Of_Knowledge\swebok-v4.pdf`
- Overview file: `F:\obsidian_note\swe-knowledge\body-of-knowledge\SWEBOK\SWEBOK v4 - Overview.md`
- Read existing chapters (especially 13_Software_Security, 14_Software_Engineering_Professional_Practice) for tone and depth reference
- The companion software-engineering-note vault at `F:\obsidian_note\swe-knowledge\software-engineering-note\` mirrors the same chapter structure with per-topic subdirectories

## Pitfalls

- Do NOT use `\r\n` line endings — use `\n` only (the existing files are mixed; new files should be clean LF)
- Wikilinks use `[[FileName]]` not `[[path/FileName]]` within the SWEBOK directory
- Each Knowledge Area sub-topic should be 2–4 sentences, not a wall of text — use bold terms to aid scanning
- The Purpose blockquote is required; omitting it breaks the pattern
- Do not add a "Sources" section — the chapter's reference matrix in the actual SWEBOK PDF handles that; the vault notes are distilled knowledge, not citations
