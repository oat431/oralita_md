# Batch Tagging with YAML Frontmatter

Add Obsidian YAML frontmatter `tags: [...]` to all `.md` files in a vault based on file path and folder structure. Tags are hierarchical: vault-level, category-level, and special tags (overview, book-summary, introduction).

## Tag Rules

Define rules as `(path_fragment, tags_tuple)` pairs. Rules are applied as substring matches — order matters (more specific earlier wins). Always include vault-level tags first, then sub-categories.

```python
tag_rules = [
    # Vault-level (broadest first — subcategories override)
    ("programming-note", ["programming"]),
    ("software-engineering-note", ["software-engineering"]),
    ("English Skill", ["english", "teaching"]),
    ("math-for-software-engineering-note", ["math"]),
    ("fitness", ["fitness"]),
    
    # Sub-categories within programming-note
    ("programming-note/API", ["api", "protocols"]),
    ("programming-note/Database", ["database", "sql", "nosql"]),
    ("programming-note/Microservice", ["microservices", "architecture"]),
    ("programming-note/Algorithm", ["algorithms", "data-structures"]),
    ("programming-note/Cybersecurity", ["security", "cybersecurity"]),
    ("programming-note/Computer Networks", ["networking", "protocols"]),
    ("programming-note/Operating Systems", ["os", "linux"]),
    
    # Sub-categories within software-engineering-note
    ("Clean Code", ["clean-code"]),
    ("Design Pattern", ["design-patterns", "oop"]),
    ("Human Computer Interaction", ["hci", "ux", "ui"]),
    
    # Book summaries
    ("clean-agile", ["book-summary", "agile", "uncle-bob"]),
    ("clean-craftsmanship", ["book-summary", "craftsmanship", "uncle-bob"]),
    ("the-pragmatic-programmer", ["book-summary", "pragmatic-programmer"]),
    ("clean-coder", ["book-summary", "professionalism", "uncle-bob"]),
]
```

## Processing (Core Function)

```python
import os, re, yaml

def get_tags(filepath):
    """Determine tags for a file based on its path."""
    tags = set()
    for fragment, rule_tags in tag_rules:
        if fragment in filepath.replace("\\", "/"):
            tags.update(rule_tags)
    # Special tags
    fn = os.path.basename(filepath).lower()
    if "overview" in fn or " content" in fn:
        tags.add("overview")
    if "introduction" in fn:
        tags.add("introduction")
    return sorted(tags)

def add_frontmatter(filepath, tags):
    """Add or merge tags into YAML frontmatter. Returns True if changed."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm = yaml.safe_load(fm_match.group(1)) or {}
        existing = fm.get("tags", [])
        if isinstance(existing, str): existing = [existing]
        merged = sorted(set(existing) | set(tags))
        if merged == existing: return False
        fm["tags"] = merged
        rest = content[fm_match.end():]
        new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
        new_content = f"---\n{new_fm}\n---{rest}"
    else:
        fm = {"tags": tags}
        new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
        new_content = f"---\n{new_fm}\n---\n\n{content}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True
```

## Cleanup Pass

After initial tagging, always run a cleanup pass for false matches:

```python
# Software engineering files shouldn't have grammar/english tags
if "software-engineering-note" in rel and "English" not in rel:
    tags.discard("grammar")
    tags.discard("english")
    tags.discard("teaching")
    tags.discard("thai-speakers")
    tags.discard("common-mistakes")

# Non-algorithm programming files shouldn't have discrete-math/graphs
if "programming-note" in rel and "Algorithm" not in rel:
    tags.discard("discrete-math")
    tags.discard("graphs")
```

## Panomete's Tagging Convention

| Vault | Root Tag | Key Sub-tags |
|-------|----------|-------------|
| programming-note | `programming` | `api`, `database`, `microservices`, `algorithms`, `networking`, `os`, `security`, `testing` |
| software-engineering-note | `software-engineering` | `clean-code`, `clean-architecture`, `design-patterns`, `hci`, `professionalism`, `swebok`, `software-design` |
| English Skill | `english`, `teaching` | `grammar`, `tenses`, `verbs`, `writing`, `thai-speakers`, `common-mistakes` |
| Math for SE | `math` | `logic`, `graphs`, `probability`, `discrete-math`, `calculus`, `algebra` |
| Books | `book-summary` | `uncle-bob`, `pragmatic-programmer`, `agile`, `craftsmanship` |
| Special | `overview`, `introduction` | Applied automatically to Overview/Content/Introduction files |
