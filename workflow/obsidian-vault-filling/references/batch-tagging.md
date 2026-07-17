# Batch Tagging — YAML Frontmatter Tags for Obsidian

Add `tags: [tag1, tag2]` YAML frontmatter to all notes in a vault. Tags enable Obsidian's graph view and tag pane filtering.

## Tag Rule Design

Define rules as `(path_fragment, [tags])` pairs. Match in order — more specific rules first, broader rules later. Fragments are substring-matched against the file path.

```python
tag_rules = [
    ("fitness", ["fitness"]),
    ("programming-note/API", ["api", "protocols"]),
    ("programming-note/Database", ["database", "sql", "nosql"]),
    ("Professionalism/clean-agile", ["book-summary", "agile", "uncle-bob"]),
    # ... more rules
]
```

## The Script

```python
def get_tags(filepath):
    tags = set()
    for fragment, rule_tags in tag_rules:
        if fragment in filepath:
            tags.update(rule_tags)
    # Auto-add overview tag
    fn = os.path.basename(filepath).lower()
    if "overview" in fn or "content" in fn:
        tags.add("overview")
    return sorted(tags)

def process_file(filepath):
    content = open(filepath).read()
    tags = get_tags(filepath)
    
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        # Parse existing frontmatter, merge tags
        fm = yaml.safe_load(fm_match.group(1)) or {}
        existing = fm.get("tags", [])
        merged = sorted(set(existing) | set(tags))
        if merged == existing:
            return  # No change
        fm["tags"] = merged
        # Rebuild
    else:
        fm = {"tags": tags}
        # Prepend frontmatter
    # Write back
```

## False Match Cleanup

Substring matching causes false positives: "Foundation" in a software folder matches English grammar rules. After initial tagging, run a cleanup pass that removes wrong tags based on vault context:

```python
# Fix: SE files shouldn't have grammar/english tags
if "software-engineering" in rel and "English" not in rel:
    tags.discard("grammar")
    tags.discard("teaching")
```

## Key Dependencies

- `pyyaml` for YAML frontmatter parsing/writing
- `re` for regex matching of existing frontmatter blocks
