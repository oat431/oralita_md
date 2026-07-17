# Overview-Driven Vault Filling (Non-PDF Sources)

Use this when the user has an existing Overview/MOC file with `[[wikilinks]]` and wants to fill missing topic notes from web sources or body-of-knowledge documents — no PDF extraction needed.

## When to Use

- User has an Overview/MOC already written with `[[wikilinks]]`
- Most topic notes are stubs or don't exist yet
- Source material is online (GeeksForGeeks, Wikipedia, etc.) or a body-of-knowledge markdown
- No PDF to extract from
- User says "fill in the missing notes" or "complete my vault"

## Pipeline (3 Phases)

### Phase 1: Gap Analysis

1. Read the source/body-of-knowledge file (and web sources if provided)
2. Read the Overview/MOC — extract all `[[wikilinks]]`
3. List all existing `.md` files in the vault
4. Cross-reference: which topics from the Overview have no note file?
5. Present the gap analysis as a table before doing any work

### Phase 2: Source Gathering

For each missing topic:
- If user provided a specific URL (e.g., GeeksForGeeks): fetch it via `browser_navigate` or `terminal` curl
- If source is a body-of-knowledge `.md`: use the topic descriptions as the authoritative outline
- Supplement with general knowledge for practical SE applications

**Important:** GeeksForGeeks and similar sites are SPAs — the useful content is embedded in `__NEXT_DATA__` or Redux store JSON within the HTML. The main portal page may only link to sub-pages. For specific topics, navigate to the sub-page or synthesize from multiple sources.

### Phase 3: Direct Summarization

Write notes directly (don't spawn sub-agents for this scale — it's faster to do inline). Each note follows the vault's existing style:

**Style conventions observed in Panomete's math vault:**
```markdown
# Topic N: Topic Name

Brief intro paragraph (2-3 sentences).

## Subtopic 1

Concepts with tables, formulas in LaTeX ($...$ and $$...$$).

| Column | Column | Column |
|--------|--------|--------|
| ... | ... | ... |

**In code:** Practical connection to software engineering.

## Subtopic 2

...

## Why This Matters in SE

| Concept | SE Application |
|---------|---------------|
| ... | ... |

## Sources

- [1*] Author, *Book Title*, Edition, Publisher, Year.
- SWEBOK v4.0 — Chapter X: Chapter Name
```

**Key conventions:**
- LaTeX math uses `$inline$` and `$$block$$` (not `\( \)` or `\[ \]`)
- Tables for comparisons, properties, and SE applications
- Code examples in ``` fences with language tag
- Always include "Why This Matters in SE" section — this is the bridge from theory to practice
- Source citations at bottom
- Filename matches the `[[wikilink]]` name exactly

### Programming/Engineering Note Format

When the vault covers software engineering topics (not math or languages), the format shifts from the math/language template above:

- **Mermaid diagrams** — `classDiagram`, `sequenceDiagram`, `graph TD`, `stateDiagram-v2`, `graph LR`. Every architecture and workflow benefits from a diagram.
- **Code blocks** — Java/Python/JS examples with `// ❌ Broken` and `// ✅ Fixed` comments inline. Show attack + defense pairs for security. Show naive → optimal progression for algorithms.
- **Tool comparison tables** — "Kafka vs RabbitMQ", "Cypress vs Playwright vs Selenium", "Istio vs Linkerd". Help the user decide.
- **Configuration YAML** — Spring Boot `application.yml`, Dockerfile, Kubernetes manifests, CI pipeline configs. Real code, not pseudocode.
- **Cross-vault links** — if a topic overlaps with Clean Architecture or Clean Code vaults, add `> Deep dive: [[Topic Name]]` callout boxes. Don't duplicate content — route to the authoritative source.
- **Decision guides** — "When to use REST vs GraphQL vs gRPC", protocol selection matrices.
- **Sources** — OWASP, CLRS, official project docs (kubernetes.io, grpc.io, spring.io), not just textbooks.

### Stub Cleanup (Post-Fill)

After all topic notes are written:
1. **Remove original stub** — if the original was a bullet-point outline and all topics are now filled in the new folder, delete the old stub file (e.g., `Api Note.md`)
2. **Update parent Content.md** — any index file that linked to the old stub should now link to the new Overview (e.g., `[[API Overview]]` instead of `[[Api Note]]`)
3. **Overview lives in folder** — `API Overview.md` goes inside `API/`, not as a loose file at vault root. The Overview is the index for its folder.

### Category-Folder Preference (Pitfall Avoided)

The user pushed back on flat files — they want **category folders with numbered prefixes**: `01 Foundation/`, `02 Tenses & Time/`. Files go inside category folders, not at root. Exception: the Overview stays at the top of its topic folder. Don't create folder-per-topic wrappers — the filename is self-explanatory (`API Gateway.md` not `API Gateway/API Gateway.md`).

### Post-Fill

- Update the Overview to add `[[wikilinks]]` for any topics that were plain headings
- Verify all files exist with `mcp_filesystem_directory_tree`

## Token Profile

| Vault Size | Topics | Typical Tokens | Approach |
|-----------|--------|---------------|----------|
| Small (10-15 topics) | ~12 | ~30K output | Direct inline summarization |
| Medium (15-30 topics) | ~25 | ~60K output | Consider sub-agents for speed |
| Large (30+ topics) | ~50 | ~120K output | Batch sub-agents (use main PDF pipeline) |

## Proven On

- Math for SE Note (12 topics, ~30K tokens output, ~5 min) — source: SWEBOK v4 + GeeksForGeeks + general knowledge
- English Skill (27 topics across 8 categories) — source: general knowledge + Thai-specific error patterns
- HCI / UI / UX (29 topics, 4 categories) — source: Laws of UX + Refactoring UI
- Design Patterns — Mermaid class diagrams added to all 22 pattern files + OOP intro (ASCII art replaced)
- Microservices (19 topics, 7 categories) — source: Building Microservices (Newman) + general knowledge
- API Design (12 topics, 4 categories) — source: general knowledge + official docs
- QA & Testing (12 topics, 4 categories) — source: ISTQB + Clean Code cross-references
- Algorithms & Data Structures (14 topics, 3 categories) — source: CLRS + LeetCode patterns
- Cybersecurity (13 topics, 4 categories) — source: OWASP + roadmap.sh
- Clean Agile (18 topics, 7 chapters) — source: 27-page PDF summary, then upgraded to full 235-page book (Chapter 8 Conclusion + Afterword added)
- Clean Craftsmanship (15 topics, 14 chapters, 3 parts) — source: full 519-page PDF, direct extraction + summarization

## Differences from Main PDF Pipeline

| Aspect | PDF Pipeline | Overview-Driven Fill |
|--------|-------------|---------------------|
| Source | PDF book file | Online resources + body-of-knowledge .md |
| Structure discovery | Extract TOC from PDF | Overview/MOC already has structure |
| Gap detection | All chapters need writing | Compare Overview wikilinks vs existing files |
| Summarization | Sub-agents (batch of 3) | Direct agent (inline) for small vaults |
| Source citation | Printed page ranges | URL + body-of-knowledge reference |
| Best for | Full book summarization | Completing partially-built vaults |
