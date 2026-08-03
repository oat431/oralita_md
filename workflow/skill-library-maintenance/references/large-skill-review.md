# Large Skill Review Criteria

Use when a skill has grown beyond a compact workflow through repeated sessions, especially when it contains historical run notes, multiple branches, or agent delegation.

## Durable Findings from the Book-to-Obsidian Review

The reviewed skill had accumulated useful experience, but its main file mixed universal rules with session history and branch-specific details. The high-value repairs were:

- replace repeated and out-of-order numbered lists with one canonical workflow;
- separate current workflow rules from historical `proven on` narratives;
- remove stale absolute paths and old workspace assumptions;
- replace unsupported delegation arguments with the current tool contract;
- keep the actual concurrency limit only when verified against the runtime;
- require a manifest before parallel writing so missing or misplaced outputs are detectable;
- verify files directly instead of trusting delegated-agent completion reports;
- treat language scans as triage rather than blindly rewriting names, formulas, URLs, or quotations;
- verify planned-but-not-yet-written wikilinks without confusing them with unexpected links;
- move deterministic checks into a reusable script and exercise both pass and fail fixtures;
- keep source-derived claims separate from supplemental synthesis and never invent page ranges.

## Review Questions

1. What is the smallest class-level trigger for this skill?
2. Which rules must be present on every run?
3. Which details apply only to one source, vault, provider, or historical incident?
4. What output can be verified by path, content, checksum, or command result?
5. What does failure recovery look like, and can the run resume without starting over?
6. Which references are still real and which are stale or missing?
7. Can a new agent follow the workflow without reading old session transcripts?

## Verification Record

The new reusable verifier pattern should be tested with:

- a fixture that passes frontmatter/source/fence/link checks;
- a fixture with a deliberately broken wikilink that must fail under strict mode;
- a fixture containing a planned output that is not yet written, to ensure planned links are handled intentionally;
- a reload of the parent skill confirming this reference is discoverable.
