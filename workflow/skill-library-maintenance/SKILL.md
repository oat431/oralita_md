---
name: skill-library-maintenance
description: "Use when reviewing or improving a Hermes skill library."
version: 1.1.0
author: Panomete + Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [skills, curation, skill-library, workflows, maintenance, review]
    related_skills: [hermes-agent-skill-authoring]
---

# Hermes Skill Library Maintenance

## Overview

Maintain a reusable skill library as a set of **class-level workflows**, not a diary of one-session fixes. A good update captures a durable behavior change: a user preference, a corrected workflow, a non-trivial technique, or a discovered failure mode that will recur in the same class of work.

Keep the main `SKILL.md` operational and compact. Put session-specific evidence, provider quirks, transcripts, reproductions, and extended examples in `references/`. Put deterministic reusable actions in `scripts/`, and copyable boilerplate in `templates/`.

This skill governs the curation decision and the quality bar. It does not replace domain skills such as Obsidian, PDF extraction, GitHub, or Hermes configuration.

## When to Use

Use this skill after:

- the user explicitly asks you to review, improve, or update skills;
- the user corrects style, tone, format, verbosity, legibility, or workflow;
- a complex task reveals a reusable technique, workaround, debugging path, or verification pattern;
- a loaded skill is stale, contradictory, overly narrow, or missing a critical step;
- a skill has accumulated historical run logs, duplicate rules, guessed paths, unsupported tool arguments, or unverifiable completion claims;
- a session creates a deterministic verifier, fixture generator, migration helper, or other reusable support artifact.

Do not create a skill for a one-off task narrative, a transient setup failure, an unconfigured credential, a missing binary, or a negative claim that a tool/feature does not work. Capture the fix or retry pattern under an appropriate existing class skill instead.

## Core Rule: Prefer the Earliest Valid Update

Use this decision ladder. Stop at the first option that fits:

1. **Patch a currently loaded curator-managed skill** that governs the learning.
2. **Patch an existing class-level umbrella** discovered with `skills_list` and `skill_view`.
3. **Add a support file** under an existing writable umbrella and add a one-line pointer from its `SKILL.md`.
4. **Create a new class-level umbrella** only when no writable skill covers the class.

A skill being loaded, relevant, or located under a user-local directory does **not** prove it is writable. Being in play is not ownership.

## Ownership and Safety Gate

Before editing or adding anything:

- Do not edit bundled skills shipped with Hermes.
- Do not edit hub-installed skills, skills in externally owned directories, pinned skills, or user-owned/manual skills.
- Do not edit another Hermes profile's skills unless the user explicitly directs that cross-profile change.
- If the only relevant skill is protected, say `Nothing to save.` only when no writable umbrella or valid support-file/new-umbrella option remains. Otherwise create or update a writable class-level alternative without copying a protected skill verbatim.
- If a protected skill is outdated, report the issue and recommend `hermes curator adopt <name>`; never bypass the guard with a direct filesystem write.
- Never expose secrets, tokens, private paths beyond what the user needs, or raw session material that is not useful for future work.

**Completion criterion:** the target skill's ownership is understood, the intended profile is confirmed, and the chosen action is allowed before any write occurs.

## What Belongs in a Skill

Capture a lesson when it changes future behavior for a recurring class of task.

### Strong signals

- **User correction:** “don’t do that,” “use this format,” “stop explaining,” “remember this,” or a repeated preference.
- **Workflow correction:** a step was missing, in the wrong order, or needed a gate before proceeding.
- **Durable technique:** a reliable extraction, delegation, verification, migration, or repair method.
- **Tool truth:** a current interface constraint or supported invocation discovered from authoritative tool/schema output.
- **Quality failure:** a recurring hallucination, path assumption, language drift, link error, or silent dropped output.

### Do not capture

- A single market lookup, PR review, book, issue, or other one-off narrative.
- “Tool X failed” without the durable setup fix or recovery pattern.
- Current machine state, temporary paths, current model/provider, or transient availability.
- An instruction that merely restates generic good intentions (“be careful,” “be thorough”). Convert it into a checkable gate instead.

**Test:** if the lesson would still help on a different book, repository, vault, provider, or date, it is probably skill material. If it only explains what happened today, put it in a reference or do not save it.

## Review Workflow

### 1. Reconstruct the learning

Read the current conversation and identify:

- what changed in behavior or understanding;
- whether the change is user preference, workflow, technique, tool usage, or quality control;
- the recurring task class it belongs to;
- what must happen differently next time;
- what evidence supports the change.

Do not promote a model's speculation to a rule. A delegated reviewer is useful for finding candidates, but its summary is not proof of a write or external side effect.

### 2. Find the right class skill

Use `skills_list` to locate candidate umbrellas. Load the most relevant candidates with `skill_view`, including linked files when needed. Look for overlap by trigger, not only by name:

- same user goal;
- same artifact type;
- same workflow stage;
- same verification or recovery pattern.

If two skills overlap, prefer the broader existing umbrella and note the overlap in the final response. Do not create a narrow sibling merely because the current session has a memorable name or error string.

### 3. Inspect before editing

Read the candidate's:

- frontmatter and trigger description;
- Overview and When to Use sections;
- ordered workflow and completion criteria;
- Common Pitfalls and Verification Checklist;
- linked references, templates, and scripts;
- current file size and signs of sediment.

For a large skill, inspect structure and representative sections before deciding whether a targeted patch or full rewrite is warranted.

### 4. Choose the smallest durable change

Use:

- **Patch** for one correction, trigger, pitfall, or verification gate.
- **Support reference** for session-specific detail, transcripts, authoritative excerpts, extended examples, or provider quirks.
- **Script** for deterministic checks or transformations that should be run rather than retyped.
- **Template** for a reusable starter artifact.
- **Full rewrite** only when the main skill has structural sprawl, contradictory rules, duplicate numbering, stale commands, or too much historical sediment.

When rewriting, preserve useful linked references unless they are demonstrably stale. Do not silently delete valuable domain knowledge; move it behind a reference pointer instead.

### 5. Write for predictable behavior

Every durable rule should answer at least one of these:

- **Trigger:** when should the skill load?
- **Action:** what should the agent do?
- **Gate:** how does it know the step is complete?
- **Recovery:** what should it do when the step fails?
- **Boundary:** when should it not apply?

Prefer strong leading words such as **Resolve**, **Inspect**, **Manifest**, **Patch**, **Verify**, **Reconcile**, and **Report**. Co-locate the rule with the workflow step it governs. Remove superseded wording instead of stacking another warning below it.

### 6. Separate always-needed rules from detail

Keep in `SKILL.md`:

- trigger and counter-trigger;
- the core workflow;
- safety/ownership boundaries;
- current tool-invocation constraints that materially change behavior;
- completion criteria;
- verification checklist;
- pointers to support files.

Move to `references/`:

- one-session evidence and error transcripts;
- historical case studies;
- long source excerpts or API notes;
- domain-specific templates and examples;
- compatibility/provider quirks that apply only to a branch.

Move to `scripts/`:

- manifest validators;
- link/frontmatter scanners;
- deterministic fixture generators;
- repeatable migration or normalization actions.

**Completion criterion:** the main skill tells the agent what to do without requiring a historical transcript, while branch-specific detail is discoverable through a one-line reference pointer.

## Updating User Preferences

When the user corrects style, format, or workflow, embed the preference in the governing skill's body—not only in memory.

Write the preference as a task rule, for example:

- `Use numbered Markdown files and hyphenated wikilinks when creating notes in this vault.`
- `Present a gap-analysis table before expensive summarization when existing coverage may overlap.`
- `Use concise direct answers unless the task requires a detailed explanation.`
- `Verify the written artifact instead of trusting an agent completion report.`

Avoid turning a context-specific choice into a universal rule. Scope it to the relevant task class or vault convention.

## Support-File Pattern

When adding a reference, use a descriptive class-oriented filename, not a session ID or error string:

```text
references/
  review-criteria.md
  provider-quirks.md
  migration-reproduction.md
scripts/
  verify_skill_artifact.py
templates/
  skill-manifest.json
```

The parent `SKILL.md` must contain a one-line pointer explaining when to load each new support file. A support file without a pointer is effectively hidden and should not be created.

A good reference starts with:

```markdown
# <Topic>

Use when <specific branch or recurring situation>.

## Evidence / Context

<short, durable explanation>

## Procedure or Example

<reproducible detail>

## Verification

<observable result>
```

Do not mirror an entire upstream manual. Extract only the detail that changes execution quality.

## Review Patterns for Large Skills

For the detailed review rubric and durable findings from the book-to-Obsidian review, load `references/large-skill-review.md` and `references/book-to-obsidian-review.md`.

When a skill has grown through many sessions, look specifically for:

- duplicate or out-of-order list numbering;
- repeated “proven on” run histories in the main body;
- stale absolute paths and old workspace names;
- references to tools or arguments not present in the current tool schema;
- hard-coded concurrency limits that should be runtime-checked;
- completion claims based only on sub-agent reports;
- rules repeated in both the checklist and pitfalls with different wording;
- one workflow trying to serve unrelated branches without routing;
- language heuristics that mistake names, formulas, URLs, or quotations for prose drift;
- link checks that ignore aliases, headings, folders, or planned-but-not-yet-written files;
- scripts that overwrite files non-atomically or lack a fixture test.

The preferred repair is to establish one canonical workflow, route branch-specific behavior to references, and make verification observable.

### Verification

After any update:

1. Reload the changed skill with `skill_view` and confirm the intended content is present.
2. When the update changes a skill's core workflow, also reload the governed skill itself and inspect the exact changed section. Do not rely on the curator skill's view or an earlier cached snapshot.
3. If the governed skill includes a verifier or helper script, treat that script as part of the change: re-read it completely after edits, run a passing fixture and an intentional failure fixture, and confirm the reported failure is the expected one.
4. Validate frontmatter starts at byte 0, parses as a mapping, has a focused description, and stays within the platform size limit.
5. Confirm the description's trigger is self-contained near its beginning; the skill index truncates long descriptions.
6. Confirm every new support file exists and is pointed to from the parent `SKILL.md`.
7. Check that no protected skill was modified and no unrelated profile was touched.
8. Check for duplicated or contradictory rules introduced by the patch.
9. Report the actual changed skill/support files, verification results, and any overlap with existing skills.

Do not claim “fully verified” when only frontmatter was checked. Say exactly which checks ran and what they returned.

## Common Pitfalls

1. **Loaded means writable.** It does not. Perform ownership triage before editing.
2. **One session, one skill.** Avoid narrow names based on today's book, PR, provider, error string, or codename. Extend an umbrella or add a reference.
3. **Skill sediment.** Historical run lists, repeated lessons, and stale paths make a skill less reliable. Prune or move them instead of appending more.
4. **Reference without a pointer.** Add a one-line load instruction in the parent skill or the reference will be missed.
5. **Generic advice.** Replace “be careful” with a gate such as “verify every expected output path and read one representative artifact.”
6. **Tool-schema drift.** Never copy old arguments or tool names without checking the current interface. If a constraint is configurable, describe how to discover it rather than hard-coding it forever.
7. **Report-based completion.** Agent summaries are evidence of intent, not proof of a file write. Stat/read the artifact yourself.
8. **Blind full rewrites.** Read first, preserve useful references, and patch when the change is local. Full rewrites require a structural reason.
9. **Over-aggressive language checks.** Treat Unicode scans as triage; inspect prose before rewriting names, formulas, URLs, or quotations.
10. **Unverified scripts.** A script is part of the skill's behavior. Test it on a fixture, including at least one failure path when feasible.
11. **Cross-profile edits.** Do not modify another profile's skill, plugin, cron, or memory without explicit direction.
12. **Overlap blindness.** If a new class skill overlaps a protected or existing skill, mention the overlap so the curator can consolidate later.

## Verification Checklist

### Triage

- [ ] A durable learning signal was identified
- [ ] Transient environment state and one-off narrative were excluded
- [ ] The recurring class of work is clear
- [ ] Candidate umbrellas were searched and loaded

### Ownership

- [ ] Target is curator-managed and writable, or a valid new umbrella is justified
- [ ] No bundled, hub-installed, pinned, external, user-owned, or cross-profile skill was edited
- [ ] Protected-skill issues were reported with the adopt recommendation when relevant

### Design

- [ ] Earliest valid update path was chosen
- [ ] Main SKILL.md contains only always-needed behavior
- [ ] Session-specific detail is in a referenced support file
- [ ] No narrow one-session skill was created
- [ ] New rules have triggers, actions, gates, or recovery behavior

### Verification

- [ ] Changed skill reloaded successfully
- [ ] Frontmatter and size validated
- [ ] New support files exist and are linked
- [ ] New scripts were exercised with real output
- [ ] Duplicate/contradictory rules were checked
- [ ] Final report states actual results and overlap notes
