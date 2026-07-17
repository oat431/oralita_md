# Checklist Management Patterns

## Pitfall: Duplicate Numbering

Real examples from session where checklist had duplicate entries:

1. **#90 appeared twice** — Variance Analysis Reports (PMBOK) and Gantt Chart / Schedule (SWEBOK) both numbered 90
2. **#91-93 in two sections** — Section 7 (PM Closing) had ☐ entries, Section 8 (Procurement) had ✅ duplicates
3. **#63 Basis of Estimates** — Appeared in two different locations
4. **#354-357 merged across sections** — Section 22 documents accidentally added to Section 21 AND still existed as ☐ in Section 22

### Prevention

Before adding items to checklist:
1. Read the checklist section you're modifying
2. Search for the document name across the entire file
3. Verify no duplicate numbers exist
4. Verify no duplicate document names exist

### Detection After Batch Update

```python
# Check for duplicate item numbers
from hermes_tools import read_file
result = read_file("path/to/TEMPLATE-CHECKLIST.md")
content = result["content"]
import re
numbers = re.findall(r'\| (\d+) \|', content)
duplicates = [n for n in numbers if numbers.count(n) > 1]
if duplicates:
    print(f"Duplicate numbers found: {set(duplicates)}")
```

### Fix Pattern

When duplicates found:
1. Identify which entry is correct (usually the one in the right section)
2. Remove the duplicate entry
3. Verify the remaining entry has correct status (☐ or ✅)

## Pitfall: Missing Mark-Offs

User caught: "why do you skip basis of estimates?" — document was created but checklist not updated.

### Prevention

After creating each batch:
1. List all documents created in the batch
2. Verify each has a corresponding ☐ → ✅ update in checklist
3. Use `execute_code` with `patch()` for batch updates

## Pitfall: Section Header Merging

Real example: Section 22 header (`## 22. Domain-Specific`) disappeared after patch, and its items were merged into Section 21.

### Detection

After every batch update:
```bash
grep -n '## [0-9]' TEMPLATE-CHECKLIST.md
```

Verify each section has exactly one header and items are in the correct section.

### Fix

1. Remove items from wrong section
2. Restore missing section header
3. Verify item numbers match section assignments

## Batch Update Pattern

```python
from hermes_tools import patch

# Update multiple items at once
old = """| 77 | Doc A | 🔴 | PMBOK | ☐ |
| 78 | Doc B | 🔴 | PMBOK | ☐ |
| 79 | Doc C | 🔴 | PMBOK | ☐ |"""

new = """| 77 | Doc A | 🔴 | PMBOK | ✅ |
| 78 | Doc B | 🔴 | PMBOK | ✅ |
| 79 | Doc C | 🔴 | PMBOK | ✅ |"""

result = patch("path/to/TEMPLATE-CHECKLIST.md", old, new)
print(result.get("success", False))
```

## Section Completion Verification

After completing a section, verify:
1. All items in section are ✅
2. No duplicate items exist
3. Item numbers are sequential
4. Section header matches content

## Skipping Sections

When user skips sections and returns later:
1. Documents without templates get `—` (em dash) in Template column in profile checklists
2. When templates are created, update `—` to actual folder reference
3. Verify section headers are intact after updates
