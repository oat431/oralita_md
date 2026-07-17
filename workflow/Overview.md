# Workflow Overview

> *Agent-created Hermes skills — copy to `~/.hermes/skills/` on any new machine to restore full capability.*

---

## Skills Map

### 📚 PDF & Book Summarization

| Skill | Use when |
|-------|---------|
| **oralita-book-sum-obs** | Summarizing a PDF book (200-1000pp) into Obsidian vault as cross-linked `.md` files. 5-phase pipeline: TOC → topic mapping → chapter extraction → parallel sub-agents → overview + polish. Proven on Clean Code, Clean Coder. |
| **bok-essential-documents** | Extracting only the essential/reference documents from a body-of-knowledge PDF — skips narrative, keeps rules, checklists, and catalogs. |

### 🏗️ Obsidian Vault Management

| Skill | Use when |
|-------|---------|
| **obsidian-vault-builder** | Building out an incomplete Obsidian vault from skeleton overview files. Creates missing topic notes in bulk. |
| **obsidian-vault-filling** | Filling in missing notes identified by gap analysis. Reads Overview/MOC, finds missing `[[wikilinks]]`, fills them. |
| **obsidian-vault-maintenance** | Detecting and fixing broken wikilinks, adding YAML frontmatter, normalizing tags. |
| **vault-completion** | General vault completion — filling missing Obsidian vault notes from overview/MOC files and web research. |

### 📄 Project Documentation

| Skill | Use when |
|-------|---------|
| **project-launch-checklist** | Building two-tier production launch checklists — generic (framework-agnostic) + framework-specific companions. |
| **project-document-templates** | Generating project document templates (PRD, tech spec, architecture decision records). |
| **md-project-document-templates** | Markdown-native project document templates — lighter, faster than the full template system. |
| **document-template-authoring** | Authoring new document templates — defining sections, prompts, and output formats. |

### 🎬 Presentations

| Skill | Use when |
|-------|---------|
| **pptx-deck-series** | Creating a series of `.pptx` decks from vault content — consistent theming across multiple presentations. |
| **presentation-from-vault** | Extracting Obsidian vault content into a structured presentation outline, ready for deck assembly. |

### 💻 Development

| Skill | Use when |
|-------|---------|
| **go-fiber-api** | Building Go REST APIs with Fiber v3 + sqlx. Clean architecture, PostgreSQL, spec-driven. |
| **software-specification** | Writing detailed software specifications from user requirements — features, architecture, data models. |

### ⚙️ Hermes Configuration

| Skill | Use when |
|-------|---------|
| **hermes-profile-setup** | Creating and configuring Hermes profiles for separate use cases. Profiles = isolated memory, skills, SOUL, tools per persona. |

---

## Common Workflows

### Workflow A: Summarize a Book → Obsidian Vault

```
1. Place PDF in accessible location (e.g., F:\books\)
2. Load skill: /skill oralita-book-sum-obs
3. Run: "Summarize F:\books\my-book.pdf into F:\projects\orlita_md\My Vault\"
4. Pipeline auto-runs: TOC → topic map → extract → sub-agents → overview
5. Result: cross-linked .md vault with checklist, wikilinks, code examples
```

### Workflow B: Build Out an Incomplete Vault

```
1. Create Overview.md with [[wikilinks]] to all desired topics
2. Load skill: /skill obsidian-vault-builder
3. Run: "Fill missing notes from Overview.md in F:\projects\orlita_md\My Vault\"
4. Agent fills in blanks, creates consistent .md files
```

### Workflow C: Create a Project Launch Checklist

```
1. Load skill: /skill project-launch-checklist
2. Run: "Create a launch checklist for <project type>"
3. Produces: generic checklist (~45 items) + framework-specific companion
```

### Workflow D: Spec → Code (Go/Fiber API)

```
1. Write spec doc in Obsidian vault
2. Load skill: /skill go-fiber-api
3. Run: "Build API from spec at F:\projects\orlita_md\...\spec.md"
4. Produces: structured Go project with Fiber v3, sqlx, clean architecture
```

---

## Restoring on a New Machine

```bash
# Copy all skills into Hermes
cp -r F:/obsidian_note/oralita_md/workflow/* ~/AppData/Local/hermes/skills/

# Verify
hermes skills list | grep local

# Load any skill
hermes -s <skill-name>
```

---

## Skill Lifecycle

```
[Create] → [Prove on real task] → [Save as skill] → [Use across sessions]
                                                        ↓
                                              [Backup to Obsidian vault]
                                                        ↓
                                              [Restore on new machine]
```

---

*Last updated: 2026-07-18*
