#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
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
    "references/template-catalog.md",
    "references/designer-mode-workflow.md",
    "references/designer-mode-gpt-image-prompt-scaffold.md",
    "references/designer-mode-direct-api-pattern.md",
    "references/tabler-icon-selection.md",
    "scripts/build_pptx.py",
    "scripts/build_pptx_artifact_tool.py",
    "scripts/split_template_deck.py",
    "scripts/tabler_icons.py",
]

OPTIONAL_ASSET_PATHS = [
    "assets/RLF_PPT_Template_v1.pptx",
    "assets/templates",
    "assets/templates_full.pptx",
    "assets/visual-templates/default-slide.png",
    "assets/visual-templates/title-page.png",
    "assets/tabler-icons/aliases.json",
]

SKILL_BAD_PATTERNS = [
    (re.compile(r"skill/references/"), "Use references/ paths inside the installable skill, not skill/references/."),
    (re.compile(r"skill/scripts/"), "Use scripts/ paths inside the installable skill, not skill/scripts/."),
    (re.compile(r"(?<!references/)SPEC\.md"), "Use references/SPEC.md inside SKILL.md."),
    (re.compile(r"(?<!references/)standards/"), "Use references/standards/ paths inside SKILL.md."),
]


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


def validate(skill_dir: Path, *, strict_assets: bool = False) -> dict[str, list[str]]:
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

    missing_assets = [rel for rel in OPTIONAL_ASSET_PATHS if not (skill_dir / rel).exists()]
    if missing_assets:
        target = errors if strict_assets else warnings
        for rel in missing_assets:
            target.append(f"optional asset path missing: {rel}")

    return {"errors": errors, "warnings": warnings}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate a deck-architect skill tree.")
    parser.add_argument("skill_dir", nargs="?", default="skill", help="Skill directory to validate.")
    parser.add_argument("--strict-assets", action="store_true", help="Treat optional assets as required.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args(argv)

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    result = validate(skill_dir, strict_assets=args.strict_assets)
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
