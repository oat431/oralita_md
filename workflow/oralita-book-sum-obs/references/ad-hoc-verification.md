# Ad-Hoc Verification Pattern (Windows)

After creating many files in a vault, verify completeness with a temp Python script. This catches missing files, undersized stubs, missing Sources sections, broken Mermaid blocks, and orphaned stubs.

## When to Use

- After filling a vault (creating 10+ files in one session)
- When the system flags "No canonical test/lint/build command"
- After moving/renaming files between folders
- After removing ASCII art and replacing with Mermaid

## Script Template

```python
import os, tempfile

verify = r"""
import os, sys, re

base = r"F:\projects\orlita_md\path\to\vault"
expected = {"Folder1": 3, "Folder2": 5, "Folder3": 2}
errors = []; present = with_sources = with_mermaid = 0

# Check overview exists
ov = os.path.join(base, "Overview.md")
if not os.path.exists(ov): errors.append("Overview missing")

for folder, cnt in expected.items():
    path = os.path.join(base, folder)
    files = [f for f in os.listdir(path) if f.endswith(".md")]
    if len(files) != cnt: errors.append(f"{folder}: {len(files)} files, expected {cnt}")
    for fn in files:
        fp = os.path.join(path, fn)
        if os.path.getsize(fp) < 1000: errors.append(f"TOO SMALL: {fn}")
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        if "## Sources" in c: with_sources += 1
        if "```mermaid" in c: with_mermaid += 1
        # Check no broken mermaid
        blocks = re.findall(r'```mermaid\n(.*?)```', c, re.DOTALL)
        for block in blocks:
            if not re.search(r'(classDiagram|graph |sequenceDiagram|stateDiagram)', block):
                errors.append(f"BROKEN MERMAID: {fn}")
        present += 1

# Check Content.md references updated
cp = r"F:\projects\orlita_md\path\to\Content.md"
with open(cp) as f:
    if "Expected New Reference" not in f.read(): errors.append("Content.md not updated")

# Check old stub removed
old = r"F:\projects\orlita_md\path\to\old-stub.md"
if os.path.exists(old): errors.append("Old stub not removed")

total = sum(expected.values())
print(f"Files: {present}/{total}  Sources: {with_sources}/{present}  Mermaid: {with_mermaid}")
if errors:
    for e in errors: print(f"FAIL: {e}")
    sys.exit(1)
print("PASS")
"""

tmp = os.path.join(tempfile.gettempdir(), "hermes-verify-name.py")
with open(tmp, "w") as f: f.write(verify)
rc = os.system(f'python "{tmp}"')
os.remove(tmp)
print(f"Exit {rc}")
```

## Running on Windows

Use the full Python path to avoid venv conflicts:
```
"C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe" -c "..."
```

Or write to temp file and execute:
```bash
"/c/Users/Admin/AppData/Local/Programs/Python/Python312/python.exe" /tmp/hermes-verify-foo.py
```

## What to Check

| Check | Why |
|-------|-----|
| File count per folder vs expected | Catch missing writes |
| Minimum file size (>1000 bytes) | Catch empty stubs |
| `## Sources` section present | Consistency gate |
| ` ```mermaid ` blocks valid | Catch broken diagrams |
| Content.md / Overview updated | Catch stale references |
| Old stub files removed | Catch orphaned files |

## When NOT to Use

- Less than 5 files created — spot-check manually
- Single-file edits — not worth the script overhead
