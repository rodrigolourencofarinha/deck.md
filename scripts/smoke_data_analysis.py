#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise SystemExit(detail or f"command failed: {' '.join(command)}")
    return json.loads(result.stdout)


def main() -> int:
    deck = REPO_ROOT / "examples" / "data-driven.deck.md"
    payload = run([sys.executable, "skill/scripts/validate_deck_data.py", str(deck), "--json"])
    if not payload.get("ok"):
        raise SystemExit(json.dumps(payload, indent=2))

    checked = payload.get("checked_artifacts") or []
    if len(checked) < 4:
        raise SystemExit(f"expected analysis artifacts and chart data to be checked, got {len(checked)}")

    print(json.dumps({"data_analysis_smoke": "ok", "checked_artifacts": len(checked)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
