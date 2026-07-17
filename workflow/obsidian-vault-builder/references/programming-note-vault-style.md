# Programming Note Vault — Style Conventions

Vault path: `F:\projects\orlita_md\programming-note`

## Vault Structure (as of 2026-07-11)

```
programming-note/
├── Programming Note Content.md      ← root index (table of all sections)
├── Fundamental/                      ← flat folder, 15 files (01-09 + 10-14 standalone)
├── Algorithm/                        ← multi-file section with sub-folders, 17 files
│   ├── 01 Data Structures/           (Arrays, Stacks, Hash Tables, Trees, Graphs, Heaps, Deque)
│   ├── 02 Algorithms/                (Searching, Sorting, Recursion, DP, Greedy, String Algo, Math Algo)
│   └── 03 Problem Solving/           (Patterns & Strategies — Big-O, 10 patterns)
├── API/                              ← multi-file section, 12 files
│   ├── 01 API Design/                (REST, OpenAPI — REST patched with Error Format, CORS, Idempotency)
│   ├── 02 API Protocols/             (GraphQL, gRPC, WebSocket, WebHook, SOAP/MQTT/AMQP)
│   ├── 03 API Security/              (Authentication, Authorization & Rate Limiting)
│   └── 04 API Operations/            (CI/CD, Monitoring)
├── Computer Networks/                10 files (OSI, IP, DNS, HTTP, TCP/UDP, Load Balancing, Security, Tools)
├── Cybersecurity/                    13 files (Crypto, OWASP, Auth, Secure Coding, Dependencies, Secrets, etc.)
├── Database/                         10 files (SQL, Normalization, Indexing, Transactions, NoSQL, Migration/Scaling)
├── Microservice/                     19 files (Decomposition, Gateway, EDA, Messaging, Saga, CQRS, Resilience, Observability, Deployment)
├── Operating Systems/                10 files (Processes, CPU, Syscalls, Memory, File Systems, I/O, IPC, Sync, Practice)
├── QA/                               13 files (Planning, Mindset, V&V, Functional, Non-Functional, TDD, Automation, Metrics)
├── Design Patterns/                  4 files (Overview, Creational, Structural, Behavioral) — quick-reference with cross-vault links
├── Version Control/                  4 files (Overview, Git Fundamentals, Workflows, Advanced)
└── Clean Code/                       4 files (Overview, Naming & Functions, Code Smells & Refactoring, Comments) — with cross-vault links
```

Total: 131 files across 12 sections. Each section has an `{Section} Overview.md` at section root.

## File Naming

- Overview: `{Section} Overview.md` (e.g., `Fundamental Overview.md`)
- Numbered notes: `{NN} {Topic}.md` (e.g., `01 Core Concepts.md`)
- Numbers are GLOBAL within a section, not per sub-folder
- Sub-folders use `{NN} {Category}` prefix (e.g., `01 Data Structures/`)

## YAML Frontmatter

```yaml
---
tags:
- programming
- fundamental
- concepts
---
```

Always list format (not inline). Always include `programming` as a tag.

## Content Style

| Element | Convention |
|---------|-----------|
| **Primary language** | Java |
| **Secondary languages** | Python, TypeScript, Rust, Go (as applicable) |
| **Code blocks** | `java` tag primary, inline comments with `//` |
| **Tables** | For comparisons, complexity, decision matrices |
| **Emoji** | ❌/✅ for bad/good code, 🔴🟡🟢 for priority |
| **Section dividers** | `---` between every major section |
| **Intro** | 2-3 sentences max, punchy |
| **Sources** | At bottom: book title + chapter, URL, RFC number |
| **Wikilinks** | `[[Topic Name]]` inline, `> [[Topic Name]] — description` in overviews |
| **Cross-vault** | Link to `software-engineering-note` when deep coverage exists there |

## Content Decision Rules

| Scenario | Decision |
|----------|----------|
| Paradigm/concept (OOP, FP) | Single file in Fundamental/ |
| Broad domain (Algorithms, Database) | Multi-file section with sub-folders |
| 3 small additions to one topic | Patch existing file, don't create standalone |
| Topic has book-level coverage in `software-engineering-note` | Create fundamentals-level note + cross-vault link |
| Topic has ZERO coverage anywhere | Full treatment |
| Quick-reference for existing book summary | Lightweight lookup file (Design Patterns style) |
| Engineering craft skill (Git, Clean Code) | New section — different purpose from knowledge domains |

## Section-by-Section Review Pattern

When user says "review section X":
1. Read ALL files in the section (use `mcp_filesystem_read_multiple_files`)
2. Assess each file individually
3. Give three-tier report: ✅ solid / ⚠️ missing / ❌ not needed
4. Recommend: new file, patch, or no action
5. Wait for confirmation before writing

## Sibling Vault

`F:\projects\orlita_md\software-engineering-note` contains:
- Clean Architecture (Programming Paradigms, SOLID, OOP)
- Clean Code (Class Design, Function Design, Error Handling)
- Design Pattern (all 23 GoF patterns — 01-Foundations, 02-Creational, 03-Structural, 04-Behavioral)
- Book summaries: Clean Coder, Pragmatic Programmer, Clean Agile, Clean Craftsmanship
- Body of Knowledge: SWEBOK, PMBOK, SEBoK, BABOK, CyBOK, DMBoK

Always check this vault before creating content that might duplicate book summaries.

## Cross-Vault Linking Pattern

Wikilinks don't resolve across separate Obsidian vaults. Use file paths instead:

```markdown
## Book Deep Dive

For full implementations with UML diagrams, participants, and trade-offs:
- `software-engineering-note/Software Design/Design Pattern/02-Creational/builder.md`
- `software-engineering-note/Software Design/Design Pattern/02-Creational/singleton.md`
```

In overview files, use a mapping table:
```markdown
## Deep Dives in software-engineering-note

| Topic | Book Summary |
|-------|-------------|
| Naming rules | `Naming Conventions.md` — full chapter with examples |
| Function design | `Function Design.md` — one thing, small, arguments |
```

Add these sections BEFORE `## Sources`. Clarify the relationship: quick-reference vs book-level deep dive.
