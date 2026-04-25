#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

PNG_1X1 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAFgwJ/"
    "l6d8JwAAAABJRU5ErkJggg=="
)


def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise SystemExit(detail or f"command failed: {' '.join(command)}")


def write_case_deck(path: Path, asset_id: str, asset_type: str, asset_path: Path) -> None:
    path.write_text(
        f"""---
schema_version: deck-md/v2-alpha
status: approved

deck:
  title: "External asset smoke"
  objective: "Confirm declared external assets are prepared"
  audience: "Maintainers"
  language: en

narrative_template: scr

production_defaults:
  default_slide_mode: ppt-shapes
  aspect_ratio: "16:9"
  footer:
    page_numbers: true
    cr_mark: true

designer_assets:
  - id: {asset_id}
    type: {asset_type}
    path: "{asset_path.as_posix()}"
    usage: "Smoke-test declared external asset handling"
    scope: deck
    placement: top-right
    required: true

design_tokens:
  palette:
    primary: "#111111"
    secondary: "#5B5B5B"
    accent: "#2F6BFF"
    accent_soft: "#DCE7FF"
    background: "#FFFFFF"
    line: "#B8C7E6"
---

# External asset smoke

## Narrative

```yaml
situation: "Public skill installs without bundled assets."
complication: "Production still needs user-supplied visual inputs sometimes."
resolution: "Declared external assets are prepared inside the workspace."
```

## Slides

### Slide 1 — "Declared external assets are prepared without bundled skill files"

```yaml
id: 1
type: executive_summary
mode: ppt-shapes
asset_refs: [{asset_id}]
```

**Body**
- Asset id `{asset_id}` is declared before production
- The builder records the prepared asset in the workspace
""",
        encoding="utf-8",
    )


def assert_asset_record(workspace: Path, asset_id: str) -> None:
    asset_log = workspace / "scratch" / "external-assets.json"
    report_path = workspace / "scratch" / "build-report.json"
    if not asset_log.exists():
        raise SystemExit(f"external asset log missing: {asset_log}")
    if not report_path.exists():
        raise SystemExit(f"build report missing: {report_path}")

    assets = json.loads(asset_log.read_text(encoding="utf-8"))
    reports = json.loads(report_path.read_text(encoding="utf-8"))
    asset = next((item for item in assets if item.get("id") == asset_id), None)
    report_asset = next((item for item in reports.get("prepared_assets", []) if item.get("id") == asset_id), None)
    if not asset or not asset.get("exists") or not asset.get("prepared_path"):
        raise SystemExit(f"asset was not prepared correctly: {asset_id}")
    if not report_asset or not report_asset.get("prepared_path"):
        raise SystemExit(f"asset missing from build report: {asset_id}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="deck-md-assets-") as tmp:
        tmp_dir = Path(tmp)
        logo = tmp_dir / "logo.png"
        logo.write_bytes(base64.b64decode(PNG_1X1))

        template = tmp_dir / "template.pptx"
        template.write_bytes(b"PK\x03\x04external-template-smoke")

        icon_pack = tmp_dir / "icons"
        icon_pack.mkdir()
        (icon_pack / "check.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"></svg>\n',
            encoding="utf-8",
        )

        cases = [
            ("brand_logo", "logo", logo),
            ("board_template", "ppt-template", template),
            ("line_icons", "icon-pack", icon_pack),
        ]

        for asset_id, asset_type, asset_path in cases:
            deck = tmp_dir / f"{asset_id}.deck.md"
            output = tmp_dir / f"{asset_id}.pptx"
            workspace = tmp_dir / f"{asset_id}-workspace"
            write_case_deck(deck, asset_id, asset_type, asset_path)
            run(
                [
                    sys.executable,
                    "skill/scripts/build_pptx_artifact_tool.py",
                    str(output),
                    str(deck),
                    "--workspace",
                    str(workspace),
                    "--skip-quality-check",
                ]
            )
            if not output.exists() or output.stat().st_size == 0:
                raise SystemExit(f"output PPTX missing for {asset_id}")
            assert_asset_record(workspace, asset_id)

    print(json.dumps({"external_asset_smoke": "ok", "cases": [case[0] for case in cases]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
