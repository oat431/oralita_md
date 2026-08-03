# Safe Post-Batch Verification Gates

Use this after delegated agents or scripts create or update Markdown notes. The goal is to prove scope, structure, and link integrity without turning heuristics into destructive rewrites.

## 1. Scope and recovery

- Keep a manifest with one owner and one canonical output path per note.
- Capture the pre-run file inventory (and hashes when overwrites are possible).
- Reject output-path collisions unless the user explicitly authorized an update.
- Prefer staging outputs outside the vault; promote only validated files.
- Compare the post-run changed-file set with the manifest before declaring success.

## 2. Structural checks

For every planned output, verify:

- exact path and UTF-8 readability;
- substantive content rather than only a byte/character threshold;
- source attribution and known-or-explicitly-unknown page/section metadata;
- frontmatter delimiters and required fields when frontmatter is used;
- balanced fenced code blocks and readable headings/tables;
- no unresolved template placeholders.

A read-only verifier is a safety net. A passing result does not prove semantic fidelity, source accuracy, or Mermaid validity unless it explicitly checks those properties.

## 3. Wikilink resolution

Treat links as targets, not a presence quota. A self-contained note may legitimately have no Related section.

The resolver must normalize:

- aliases (`[[Target|display text]]`);
- heading/block suffixes (`#Heading`, `^block-id`);
- nested paths and path separators;
- optional `.md` suffixes;
- case-insensitive Windows matching while reporting ambiguous duplicate basenames.

Do not count an anchor as fully valid unless the target heading/block is checked, or explicitly report anchor validation as out of scope. Do not invent sibling links to make a file pass.

## 4. Language review

Script counts are triage signals only. Proper names, formulas, URLs, code, and short quotations may contain non-Latin characters. Review prose density against the requested language. Rewrite only a substantially mislocalized note, preserve source material and attribution, then rerun all gates.

## 5. Repair discipline

Use an explicit correction map and targeted `patch` operations where possible. Read the affected note before editing. After each repair pass, rerun the resolver and structural checks, and report every changed path. Never let a retry overwrite a good note merely because a child agent reported failure.

## 6. Completion evidence

Report planned/written/failed/needs-review counts, the verifier result, changed paths, unresolved links or limitations, and representative source comparisons. A child completion message alone is not evidence that the expected file exists or is correct.
