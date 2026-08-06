# Direct Vault Creation from Domain Knowledge

## When to Use

When the user wants a knowledge base for a topic that:
- Has no single canonical PDF (e.g., Software Methodology, UX/UI Design)
- Needs to be synthesized from multiple existing sources (PDFs + domain knowledge)
- Is a methodology, process, or design discipline not covered by existing BOKs

## Workflow

1. **Check existing books** — `ls -la /f/books/` to see what PDFs are available
2. **Identify knowledge sources** — Which existing PDFs cover parts of the topic? What domain knowledge is needed?
3. **Create folder** — `mcp_filesystem_create_directory` with descriptive name
4. **Create files** — Write directly using `write_file` with:
   - YAML frontmatter: `tags: [topic, category, methodology]`
   - Source citations (book references, industry standards)
   - Comparison tables (methodology vs methodology)
   - Mermaid diagrams (process flows, relationships)
   - Anti-patterns sections
   - Decision guides
5. **Create overview** — Master index with file list, relationship diagram, reading paths
6. **Cross-link** — Link to Essential Documents, BOK vaults, and other methodology folders
7. **Update Essential Documents** — Add link to new vault in "Which Checklist Do I Need?" section

## Template Structure

```yaml
---
tags: [topic, category, methodology]
---

# Title

> *Source: Book/Standard by Author/Organization*

## Purpose

Brief description of what this covers and why it matters.

## Key Concepts

### Concept 1
Description, examples, when to use.

### Concept 2
Description, examples, when to use.

## Comparison Table

| Aspect | Option A | Option B | Option C |
|---|---|---|---|
| Criteria 1 | Value | Value | Value |

## Anti-Patterns

| Anti-Pattern | What It Looks Like | Fix |
|---|---|---|
| Pattern 1 | Description | Solution |

## Related

- [[Other File]] — Description
```

## Proven Examples

- **Software Methodology** — 5 files synthesized from `clean-agile.pdf` + Lean/Kanban domain knowledge. Covers Agile, Lean, Kanban, Waterfall/V-Model, comparison overview.
- **UX/UI Design** — 6 files synthesized from industry standards (Nielsen Norman Group, IDEO, Material Design). Covers User Research, UX Design, UI Design, Usability/A/B Testing, Essential Documents.

## Cross-Vault Linking Pattern

When creating a new vault, establish bidirectional links:

1. **New vault → Essential Documents** — Link to document checklists
2. **New vault → BOK vaults** — Link to relevant BOK chapters
3. **Essential Documents → New vault** — Add to "Which Checklist Do I Need?"
4. **BOK overview → New vault** — If relevant, add to relationship diagram

This creates a web of interconnected knowledge rather than isolated silos.

## Pitfalls

1. **Don't wait for perfect sources** — Domain knowledge + existing PDFs is enough. The user can modify files later when they get more books.

2. **Always create an overview** — Even for small vaults (4-6 files), an overview with a Mermaid diagram and reading paths is essential for navigation.

3. **Update Essential Documents** — The user will remind you if you forget. Do it proactively.

4. **Use Mermaid for diagrams** — The user prefers Mermaid over ASCII for all relationship and process diagrams.

5. **Include anti-patterns** — Every methodology file should have an anti-patterns table. Users find these more actionable than best practices alone.
