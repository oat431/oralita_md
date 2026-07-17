"""
Bulk-tag all .md files in a vault with YAML frontmatter tags based on path patterns.
Usage: python tag-vault.py <vault_root>
"""
import os, re, yaml, sys

# === CONFIGURE TAG RULES ===
# (path_fragment, [tags...]) — order matters, more specific first
TAG_RULES = [
    # Vault-level
    ("fitness", ["fitness"]),
    ("programming-note", ["programming"]),
    ("software-engineering-note", ["software-engineering"]),
    ("English Skill", ["english", "teaching"]),
    ("math-for-software-engineering-note", ["math"]),
    ("project-checklist", ["checklist"]),
    # Sub-categories — add your own...
    ("programming-note/API", ["api", "protocols"]),
    ("programming-note/Database", ["database", "sql", "nosql"]),
    ("programming-note/Microservice", ["microservices", "architecture"]),
    ("programming-note/Algorithm", ["algorithms", "data-structures"]),
    ("programming-note/QA", ["testing", "qa"]),
    ("programming-note/Cybersecurity", ["security", "cybersecurity"]),
    ("programming-note/Computer Networks", ["networking", "protocols"]),
    ("programming-note/Operating Systems", ["os", "linux"]),
    ("Clean Code", ["clean-code"]),
    ("Clean Architecture", ["clean-architecture"]),
    ("Design Pattern", ["design-patterns", "oop"]),
    ("Human Computer Interaction", ["hci", "ux", "ui"]),
    ("clean-agile", ["book-summary", "agile", "uncle-bob"]),
    ("clean-craftsmanship", ["book-summary", "craftsmanship", "uncle-bob"]),
    ("the-pragmatic-programmer", ["book-summary", "pragmatic-programmer"]),
    ("clean-coder", ["book-summary", "professionalism", "uncle-bob"]),
    ("Professionalism", ["professionalism"]),
    ("Software Design", ["software-design"]),
    ("Body of Knowledge", ["swebok"]),
]

# === FALSE-MATCH CLEANUP RULES ===
# (path_contains, tags_to_remove)
CLEANUP_RULES = [
    # Software engineering files shouldn't have grammar/english tags
    (lambda p: "software-engineering-note" in p and "English" not in p, 
     {"grammar", "english", "teaching", "thai-speakers", "common-mistakes"}),
    # Programming-note non-algorithm files shouldn't have discrete-math/graphs
    (lambda p: "programming-note" in p and "Algorithm" not in p,
     {"discrete-math", "graphs"}),
    # Clean-coder shouldn't have clean-code tag
    (lambda p: "clean-coder" in p, {"clean-code"}),
    # Architecture/design-pattern files shouldn't have grammar tag
    (lambda p: "architecture" in p.lower() or "design-pattern" in p.lower(), {"grammar"}),
]


def get_tags(filepath, rules=TAG_RULES):
    tags = set()
    normalized = filepath.replace("\\", "/")
    for fragment, rule_tags in rules:
        if fragment in normalized:
            tags.update(rule_tags)
    fn = os.path.basename(filepath).lower()
    if "overview" in fn or " content" in fn:
        tags.add("overview")
    if "introduction" in fn:
        tags.add("introduction")
    return sorted(tags)


def process_file(filepath, dry_run=False):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    tags = get_tags(filepath)
    if not tags:
        return False
    
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    
    if fm_match:
        fm_text = fm_match.group(1)
        rest = content[fm_match.end():]
        try:
            fm = yaml.safe_load(fm_text) or {}
        except:
            fm = {}
        existing = fm.get("tags", [])
        if isinstance(existing, str):
            existing = [existing]
        merged = sorted(set(existing) | set(tags))
        if merged == existing:
            return False
        fm["tags"] = merged
        new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
        new_content = f"---\n{new_fm}\n---{rest}"
    else:
        fm = {"tags": tags}
        new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
        new_content = f"---\n{new_fm}\n---\n\n{content}"
    
    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
    return True


def cleanup_false_matches(base_dir):
    """Remove tags that leaked into wrong vaults via name overlap."""
    fixed = 0
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if not fm_match:
                continue
            try:
                fm = yaml.safe_load(fm_match.group(1)) or {}
            except:
                continue
            tags = set(fm.get("tags", []))
            if isinstance(tags, str):
                tags = {tags}
            original = tags.copy()
            rel = fp.replace(base_dir, "").lstrip("\\/").replace("\\", "/")
            for check_fn, remove_tags in CLEANUP_RULES:
                if check_fn(rel):
                    tags -= remove_tags
            if tags != original:
                fm["tags"] = sorted(tags)
                rest = content[fm_match.end():]
                new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(f"---\n{new_fm}\n---{rest}")
                fixed += 1
                print(f"  Cleaned: {rel}")
    return fixed


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else r"F:\projects\orlita_md"
    print(f"Tagging vaults under: {base}")
    
    tagged = skipped = 0
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            if process_file(fp):
                rel = fp.replace(base, "").lstrip("\\/")
                print(f"  Tagged: {rel} → {get_tags(fp)}")
                tagged += 1
            else:
                skipped += 1
    
    print(f"\nTagged: {tagged}, Skipped: {skipped}")
    
    cleaned = cleanup_false_matches(base)
    print(f"False matches cleaned: {cleaned}")
