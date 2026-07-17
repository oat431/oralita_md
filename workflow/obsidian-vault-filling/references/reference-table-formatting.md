# Reference Table Formatting

Use when creating structured reference documents (document inventories, checklist tables, decision matrices, SDLC artifact lists, or any table with a priority/importance/urgency column).

## Priority sorting rule

**Always sort rows by priority — highest importance first.** Do not leave tables in unsorted, creation-order, or alphabetical order when a priority column exists.

The canonical priority order:

1. 🔴 **Must Have** / Critical / Required
2. 🟡 **Nice to Have** / Recommended
3. 🟢 **Optional** / Situational

This lets readers scan what's critical at a glance and stop reading at lower tiers.

## Table structure

Preferred 4-column format for reference tables:

```
| Document | Description | Priority | ISO/IEEE Reference |
|---|---|---|---|
```

- **Document** — bold name with acronym in parens
- **Description** — one-line summary of what it contains
- **Priority** — emoji + label (🔴 Must Have)
- **Reference** — standard identifier if applicable

## When to add a priority column

- When the audience needs to triage (what's essential vs. nice-to-know)
- When items have different applicability based on project size/domain/methodology
- When the table is meant as a checklist or decision aid

## Programmatic sorting

If tables are large (10+ rows), use a Python script to sort instead of hand-editing:

```python
def priority_sort_key(row):
    cols = [c.strip() for c in row.split('|')]
    p = cols[3]  # Priority column
    if '\U0001f534' in p: return (0, cols[1])
    if '\U0001f7e1' in p: return (1, cols[1])
    if '\U0001f7e2' in p: return (2, cols[1])
    return (9, '')
```

Run through markdown tables, detect by header+separator pattern, sort body rows, rewrite.
