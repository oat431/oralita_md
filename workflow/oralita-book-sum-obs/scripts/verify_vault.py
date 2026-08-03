#!/usr/bin/env python3
"""Verify an Oralita book-to-Obsidian run.

The verifier checks manifest/path safety, expected outputs, basic Markdown
structure, source markers, frontmatter when PyYAML is available, and wikilinks.
It does not prove semantic correctness or validate Mermaid syntax.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    yaml = None

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
PLACEHOLDER_RE = re.compile(r"\[(?:INSERT|TODO|TBD|FIXME)[^\]]*\]", re.IGNORECASE)
NON_LATIN_RE = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0400-\u04ff]")


def norm(value: str) -> str:
    return value.replace("\\", "/").strip("/").casefold()


def link_key(value: str) -> str:
    value = value.strip().replace("\\", "/")
    if value.casefold().endswith(".md"):
        value = value[:-3]
    return norm(value)


def canonical_path(path: Path) -> str:
    return norm(path.as_posix())


def same_path(left: str | Path, right: str | Path) -> bool:
    try:
        return os.path.normcase(str(Path(left).expanduser().resolve())) == os.path.normcase(
            str(Path(right).expanduser().resolve())
        )
    except OSError:
        return norm(str(left)) == norm(str(right))


def source_paths(root: Path, planned: Iterable[Path] = ()) -> list[Path]:
    return sorted(set(root.rglob("*.md")) | set(planned), key=lambda p: canonical_path(p))


def iter_manifest_outputs(manifest: dict) -> list[str]:
    outputs = manifest.get("outputs", [])
    if not isinstance(outputs, list):
        return []
    result: list[str] = []
    for item in outputs:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict) and isinstance(item.get("output"), str):
            result.append(item["output"])
    return result


def path_for_output(root: Path, output: str) -> Path:
    candidate = Path(output)
    return (candidate if candidate.is_absolute() else root / candidate).resolve()


def safe_relative(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def heading_key(value: str) -> str:
    value = unquote(value).strip().casefold()
    value = value.replace("\\", " ")
    value = re.sub(r"[`*_~]", "", value)
    value = "".join(ch for ch in unicodedata.normalize("NFKD", value) if not unicodedata.combining(ch))
    return re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().replace(" ", "-")


def heading_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for match in re.finditer(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", text, re.MULTILINE):
        raw = match.group(1).strip()
        keys.add(heading_key(raw))
        keys.add(raw.casefold())
    return keys


def block_ids(text: str) -> set[str]:
    return {match.group(1).casefold() for match in re.finditer(r"\^(\S+)", text)}


class LinkIndex:
    def __init__(self, root: Path, paths: Iterable[Path]):
        self.root = root
        self.by_full: dict[str, Path] = {}
        self.by_name: dict[str, list[Path]] = {}
        for path in sorted(set(paths), key=lambda item: canonical_path(item)):
            if path.suffix.casefold() != ".md":
                continue
            full = link_key(path.relative_to(root).with_suffix("").as_posix())
            name = link_key(path.stem)
            self.by_full[full] = path
            self.by_name.setdefault(name, []).append(path)

    def resolve_file(self, target: str) -> tuple[Path | None, str | None]:
        key = link_key(target)
        if not key:
            return None, "empty link target"
        if "/" in key:
            path = self.by_full.get(key)
            return (path, None) if path else (None, "target does not exist")
        matches = self.by_name.get(key, [])
        if len(matches) == 1:
            return matches[0], None
        if len(matches) > 1:
            names = ", ".join(str(p.relative_to(self.root)) for p in matches)
            return None, f"ambiguous basename; matches: {names}"
        return None, "target does not exist"

    def resolve(self, raw_link: str, current: Path) -> tuple[bool, str | None]:
        expression = raw_link.split("|", 1)[0].strip()
        if not expression:
            return False, "empty link"
        if "://" in expression:
            return True, None

        if "#" in expression:
            target, anchor = expression.split("#", 1)
        else:
            target, anchor = expression, ""

        if target.strip():
            target_path, error = self.resolve_file(target)
            if target_path is None:
                return False, error
        else:
            target_path = current

        if not anchor:
            return True, None
        anchor = unquote(anchor.strip())
        text = target_path.read_text(encoding="utf-8-sig")
        if anchor.startswith("^"):
            block = anchor[1:].casefold()
            return (True, None) if block in block_ids(text) else (False, "block id does not exist")
        key = heading_key(anchor)
        return (True, None) if key in heading_keys(text) or anchor.casefold() in heading_keys(text) else (False, "heading does not exist")


def read_yaml_frontmatter(text: str) -> tuple[bool, str | None]:
    if text.startswith("\ufeff"):
        return False, "UTF-8 BOM before frontmatter"
    if not text.startswith("---\n"):
        return True, None
    match = FRONTMATTER_RE.match(text)
    if not match:
        return False, "frontmatter opening fence has no closing fence"
    if yaml is None:
        return True, "PyYAML unavailable; frontmatter syntax not parsed"
    try:
        value = yaml.safe_load(match.group(1))
    except Exception as exc:  # pragma: no cover - parser-specific
        return False, f"invalid YAML frontmatter: {exc}"
    if value is not None and not isinstance(value, dict):
        return False, "frontmatter is not a YAML mapping"
    return True, None


def load_baseline(manifest: dict, root: Path) -> set[str] | None:
    baseline = manifest.get("baseline_files")
    if not isinstance(baseline, list):
        return None
    result: set[str] = set()
    for item in baseline:
        if isinstance(item, str):
            result.add(norm(item))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Vault folder to verify")
    parser.add_argument("--manifest", required=True, help="Run manifest JSON")
    parser.add_argument("--language", default="en", help="Requested prose language")
    parser.add_argument("--strict-links", action="store_true", help="Treat unresolved wikilinks as errors")
    parser.add_argument("--min-chars", type=int, default=200, help="Minimum non-whitespace characters per planned non-overview note")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    manifest_path = Path(args.manifest).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"FAIL: root does not exist or is not a directory: {root}")
        return 1
    if not manifest_path.is_file():
        print(f"FAIL: manifest does not exist: {manifest_path}")
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive CLI error path
        print(f"FAIL: cannot parse manifest: {exc}")
        return 1
    if not isinstance(manifest, dict):
        print("FAIL: manifest root must be a JSON object")
        return 1

    declared_root = manifest.get("target_root")
    if isinstance(declared_root, str) and declared_root and not same_path(declared_root, root):
        errors.append(f"MANIFEST ROOT MISMATCH: {declared_root} != {root}")

    outputs = iter_manifest_outputs(manifest)
    if not outputs:
        errors.append("manifest has no outputs")

    planned: list[Path] = []
    output_keys: set[str] = set()
    for output in outputs:
        path = path_for_output(root, output)
        key = canonical_path(path)
        if key in output_keys:
            errors.append(f"DUPLICATE OUTPUT: {output}")
        output_keys.add(key)
        if not safe_relative(path, root):
            errors.append(f"OUTPUT OUTSIDE ROOT: {output}")
            continue
        planned.append(path)
        if not path.is_file():
            errors.append(f"MISSING: {path}")

    actual_paths = source_paths(root)
    baseline = load_baseline(manifest, root)
    if baseline is not None:
        actual_keys = {norm(path.relative_to(root).as_posix()) for path in actual_paths}
        planned_rel = {norm(path.relative_to(root).as_posix()) for path in planned}
        unexpected = actual_keys - baseline - planned_rel
        for item in sorted(unexpected):
            errors.append(f"UNEXPECTED NEW FILE: {item}")

    index = LinkIndex(root, actual_paths + planned)
    for path in planned:
        if not path.is_file():
            continue
        label = str(path.relative_to(root))
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            errors.append(f"NOT UTF-8: {label}: {exc}")
            continue

        is_overview = "overview" in path.stem.casefold()
        if not is_overview and len(text.strip()) < args.min_chars:
            errors.append(f"TOO SMALL: {label} ({len(text.strip())} chars)")
        if not ("## Sources" in text or re.search(r"^source:\s*", text, re.MULTILINE) or "> *Source:" in text):
            warnings.append(f"NO SOURCE MARKER: {label}")
        if PLACEHOLDER_RE.search(text):
            warnings.append(f"PLACEHOLDER TEXT: {label}")

        for fence in ("```", "~~~"):
            if len(re.findall(rf"^\s*{re.escape(fence)}", text, re.MULTILINE)) % 2:
                errors.append(f"UNCLOSED CODE FENCE: {label} ({fence})")

        valid_frontmatter, frontmatter_message = read_yaml_frontmatter(text)
        if not valid_frontmatter:
            errors.append(f"FRONTMATTER: {label}: {frontmatter_message}")
        elif frontmatter_message:
            warnings.append(f"FRONTMATTER: {label}: {frontmatter_message}")

        for raw in WIKILINK_RE.findall(text):
            ok, reason = index.resolve(raw, path)
            if not ok:
                message = f"BROKEN WIKILINK: {label}: [[{raw}]] ({reason})"
                (errors if args.strict_links else warnings).append(message)

        if args.language.casefold().startswith("en"):
            unusual = NON_LATIN_RE.findall(text)
            if len(unusual) >= 20:
                warnings.append(f"LANGUAGE REVIEW: {label} contains {len(unusual)} non-Latin-script characters")

    print(f"Root: {root}")
    print(f"Manifest outputs: {len(outputs)}")
    print(f"Existing Markdown files: {len(actual_paths)}")
    print(f"Errors: {len(errors)}  Warnings: {len(warnings)}")
    for item in errors:
        print(f"FAIL: {item}")
    for item in warnings:
        print(f"WARN: {item}")

    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS" if not warnings else "RESULT: PASS WITH WARNINGS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
