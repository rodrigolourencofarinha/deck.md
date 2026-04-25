#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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


def require_path(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"{label} does not exist: {path}")
    if path.is_file() and path.stat().st_size == 0:
        raise SystemExit(f"{label} is empty: {path}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke-test the artifact-tool editable PPTX builder.")
    parser.add_argument(
        "--deck",
        default="deck.minimal.md",
        help="Source deck.md file. A temporary ppt-shapes copy is created for the smoke test.",
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

        artifact_output = tmp_dir / "artifact-tool-smoke.pptx"
        workspace = tmp_dir / "artifact-tool-workspace"
        run(
            [
                sys.executable,
                "skill/scripts/build_pptx_artifact_tool.py",
                str(artifact_output),
                str(smoke_deck),
                "--workspace",
                str(workspace),
                "--allow-draft",
            ]
        )
        require_path(artifact_output, "artifact-tool output PPTX")
        previews = sorted((workspace / "scratch" / "previews").glob("*.png"))
        layouts = sorted((workspace / "scratch" / "layouts").glob("*.layout.json"))
        if not previews:
            raise SystemExit("artifact-tool builder did not create PNG previews")
        if not layouts:
            raise SystemExit("artifact-tool builder did not create layout JSON")
        require_path(workspace / "scratch" / "quality-report.json", "quality report")
        print(json.dumps({
            "artifact_tool_builder": "ok",
            "output_pptx": str(artifact_output),
            "previews": len(previews),
            "layouts": len(layouts),
            "quality_report": str(workspace / "scratch" / "quality-report.json"),
        }, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
