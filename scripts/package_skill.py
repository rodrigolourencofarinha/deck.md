#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILL = REPO_ROOT / "skill"
VALIDATOR = REPO_ROOT / "scripts" / "validate_skill_install.py"


def ignore_names(_directory: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name == ".DS_Store" or name == "__pycache__" or name.endswith(".pyc"):
            ignored.add(name)
    return ignored


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise SystemExit(f"missing source file: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        raise SystemExit(f"missing source directory: {src}")
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=ignore_names)


def overlay_current_references(stage: Path) -> None:
    refs = stage / "references"
    copy_file(REPO_ROOT / "SPEC.md", refs / "SPEC.md")
    copy_file(REPO_ROOT / "deck.md", refs / "deck.md")
    copy_file(REPO_ROOT / "deck.minimal.md", refs / "deck.minimal.md")
    copy_file(REPO_ROOT / "deck.full.md", refs / "deck.full.md")
    copy_tree(REPO_ROOT / "standards", refs / "standards")
    copy_tree(REPO_ROOT / "examples", refs / "examples")


def validate_stage(stage: Path) -> None:
    command = [sys.executable, str(VALIDATOR), str(stage)]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        detail = (result.stdout or result.stderr).strip()
        raise SystemExit(detail or "skill validation failed")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package/install the deck-architect skill.")
    parser.add_argument(
        "--target",
        default="~/.codex/skills/deck-architect",
        help="Install target directory. Defaults to ~/.codex/skills/deck-architect.",
    )
    parser.add_argument("--force", action="store_true", help="Replace the target if it already exists.")
    parser.add_argument(
        "--stage-only",
        help="Write the packaged skill to this directory instead of installing to --target.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    target = Path(args.target).expanduser().resolve()
    final_target = Path(args.stage_only).expanduser().resolve() if args.stage_only else target

    with tempfile.TemporaryDirectory(prefix="deck-architect-skill-") as tmp:
        stage = Path(tmp) / "deck-architect"
        shutil.copytree(SOURCE_SKILL, stage, ignore=ignore_names)
        overlay_current_references(stage)

        validate_stage(stage)
        if final_target.exists():
            if not args.force:
                raise SystemExit(f"target exists; rerun with --force to replace: {final_target}")
            shutil.rmtree(final_target)
        final_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(stage, final_target, ignore=ignore_names)

    print(final_target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
