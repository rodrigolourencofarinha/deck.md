#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise SystemExit(detail or f"command failed: {' '.join(command)}")


def make_ppt_shapes_copy(source: Path, output: Path) -> None:
    text = source.read_text(encoding="utf-8")
    text = text.replace("status: draft", "status: approved", 1)
    text = text.replace("default_slide_mode: designer-mode", "default_slide_mode: ppt-shapes", 1)
    output.write_text(text, encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke-test both editable deck builders.")
    parser.add_argument(
        "--deck",
        default="deck.minimal.md",
        help="Source deck.md file. A temporary ppt-shapes copy is created for the smoke test.",
    )
    parser.add_argument(
        "--skip-artifact-tool",
        action="store_true",
        help="Only run the legacy python-pptx builder.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    source = (REPO_ROOT / args.deck).resolve()
    if not source.exists():
        raise SystemExit(f"deck file does not exist: {source}")

    with tempfile.TemporaryDirectory(prefix="deck-md-smoke-") as tmp:
        tmp_dir = Path(tmp)
        smoke_deck = tmp_dir / "deck.minimal.ppt-shapes.md"
        make_ppt_shapes_copy(source, smoke_deck)

        legacy_output = tmp_dir / "legacy-smoke.pptx"
        run([sys.executable, "skill/scripts/build_pptx.py", str(legacy_output), str(smoke_deck)])
        if not legacy_output.exists() or legacy_output.stat().st_size == 0:
            raise SystemExit(f"legacy builder did not create output: {legacy_output}")

        artifact_output = None
        if not args.skip_artifact_tool:
            artifact_output = tmp_dir / "artifact-tool-smoke.pptx"
            run(
                [
                    sys.executable,
                    "skill/scripts/build_pptx_artifact_tool.py",
                    str(artifact_output),
                    str(smoke_deck),
                    "--allow-draft",
                    "--skip-quality-check",
                ]
            )
            if not artifact_output.exists() or artifact_output.stat().st_size == 0:
                raise SystemExit(f"artifact-tool builder did not create output: {artifact_output}")

        print("legacy_builder=ok")
        if artifact_output:
            print("artifact_tool_builder=ok")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
