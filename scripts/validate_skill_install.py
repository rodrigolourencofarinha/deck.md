#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/SPEC.md",
    "references/deck.md",
    "references/deck.minimal.md",
    "references/deck.full.md",
    "references/standards/deck-validation.md",
    "references/standards/slide-archetypes.md",
    "references/standards/narrative-templates.md",
    "references/standards/image-prompts.md",
    "references/standards/artifact-structure.md",
    "references/examples/scr.deck.md",
    "references/examples/pyramid.deck.md",
    "references/examples/problem-solution.deck.md",
    "references/examples/update.deck.md",
    "references/deck-workflow.md",
    "references/consulting-slide-standards.md",
    "references/single-slide-workflow.md",
    "references/pptx-production.md",
    "references/designer-mode-workflow.md",
    "references/designer-mode-gpt-image-prompt-scaffold.md",
    "references/designer-mode-direct-api-pattern.md",
    "scripts/build_pptx_artifact_tool.py",
]

SKILL_BAD_PATTERNS = [
    (re.compile(r"skill/references/"), "Use references/ paths inside the installable skill, not skill/references/."),
    (re.compile(r"skill/scripts/"), "Use scripts/ paths inside the installable skill, not skill/scripts/."),
    (re.compile(r"(?<!references/)SPEC\.md"), "Use references/SPEC.md inside SKILL.md."),
    (re.compile(r"(?<!references/)standards/"), "Use references/standards/ paths inside SKILL.md."),
]

PUBLIC_BAD_PATTERNS = [
    (re.compile(r"\bRLF\b|RLF_"), "Personal RLF assets must not be referenced in the public skill."),
    (re.compile(r"\bRRF\b|RRF_"), "Personal RRF assets must not be referenced in the public skill."),
    (re.compile(r"\bTabler\b|\btabler\b"), "Bundled Tabler/icon-pack references must not appear in the public skill."),
    (re.compile(r"template-catalog"), "Bundled template catalog references must not appear in the public skill."),
    (re.compile(r"assets/templates"), "Bundled template assets must not appear in the public skill."),
    (re.compile(r"visual-templates"), "Bundled visual-template assets must not appear in the public skill."),
    (re.compile(r"split_template_deck"), "Template-splitting helper must not ship in the public skill."),
    (re.compile(r"tabler_icons"), "Bundled icon helper must not ship in the public skill."),
    (re.compile(r"python-pptx|build_pptx\.py"), "Legacy python-pptx path must not ship in the public skill."),
    (re.compile(r"/Users/|/Volumes/|Dropbox/Resources"), "Personal filesystem paths must not appear in the public skill."),
]

TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".mjs", ".js"}


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def iter_text_files(skill_dir: Path):
    for path in skill_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def validate(skill_dir: Path) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_dir.exists():
        return {"errors": [f"skill directory does not exist: {skill_dir}"], "warnings": []}
    if not skill_dir.is_dir():
        return {"errors": [f"skill path is not a directory: {skill_dir}"], "warnings": []}

    for rel in REQUIRED_FILES:
        path = skill_dir / rel
        if not path.exists():
            errors.append(f"missing required path: {rel}")
        elif path.is_file() and path.stat().st_size == 0:
            errors.append(f"required file is empty: {rel}")

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8")
        meta = frontmatter(text)
        if not meta.get("name"):
            errors.append("SKILL.md frontmatter is missing name")
        if not meta.get("description"):
            errors.append("SKILL.md frontmatter is missing description")
        for pattern, message in SKILL_BAD_PATTERNS:
            if pattern.search(text):
                errors.append(message)

    assets_dir = skill_dir / "assets"
    if assets_dir.exists():
        errors.append("public skill package must not contain an assets/ directory; declare external assets in deck.md")

    for path in iter_text_files(skill_dir):
        rel = path.relative_to(skill_dir).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern, message in PUBLIC_BAD_PATTERNS:
            if pattern.search(text):
                errors.append(f"{message} Offending file: {rel}")
                break

    return {"errors": errors, "warnings": warnings}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate a deck-architect skill tree.")
    parser.add_argument("skill_dir", nargs="?", default="skill", help="Skill directory to validate.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args(argv)

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    result = validate(skill_dir)
    ok = not result["errors"]

    payload = {
        "skill_dir": str(skill_dir),
        "ok": ok,
        "errors": result["errors"],
        "warnings": result["warnings"],
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload, indent=2))

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
