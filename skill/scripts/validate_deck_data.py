#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_pptx_artifact_tool import (  # noqa: E402
    ensure_list,
    is_remote_ref,
    load_structured_file,
    read_chart_data,
    resolve_local_ref,
)


def csv_summary(path: Path, required_columns: list[str] | None = None) -> dict:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    if not fieldnames:
        raise ValueError("CSV has no header")
    if not rows:
        raise ValueError("CSV has no data rows")

    missing = [column for column in (required_columns or []) if column not in fieldnames]
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

    return {"path": str(path), "columns": fieldnames, "rows": len(rows)}


def local_path(spec_path: Path, value: str) -> Path:
    if is_remote_ref(value):
        raise ValueError("remote refs are not valid analysis artifacts; save a local CSV or query file")
    return resolve_local_ref(spec_path, value)


def validate_existing_file(
    spec_path: Path,
    value: str,
    label: str,
    errors: list[str],
    summaries: list[dict],
    *,
    csv_required_columns: list[str] | None = None,
) -> None:
    try:
        path = local_path(spec_path, value)
    except ValueError as exc:
        errors.append(f"{label}: {value}: {exc}")
        return

    if not path.exists():
        errors.append(f"{label} does not exist: {value}")
        return
    if path.is_file() and path.stat().st_size == 0:
        errors.append(f"{label} is empty: {value}")
        return

    if path.suffix.lower() == ".csv":
        try:
            summaries.append(csv_summary(path, csv_required_columns))
        except ValueError as exc:
            errors.append(f"{label} is invalid: {value}: {exc}")
    else:
        summaries.append({"path": str(path), "bytes": path.stat().st_size})


def slide_ids(spec: dict) -> set[str]:
    return {str(slide.get("id")) for slide in ensure_list(spec.get("slides")) if isinstance(slide, dict)}


def validate_analysis_artifacts(spec_path: Path, spec: dict, errors: list[str], summaries: list[dict]) -> None:
    artifacts = spec.get("analysis_artifacts") or {}
    if not artifacts:
        return
    if not isinstance(artifacts, dict):
        errors.append("analysis_artifacts must be a mapping")
        return

    manifest = str(artifacts.get("manifest") or "").strip()
    if manifest:
        validate_existing_file(spec_path, manifest, "analysis_artifacts.manifest", errors, summaries)

    notes = str(artifacts.get("notes") or "").strip()
    if notes:
        validate_existing_file(spec_path, notes, "analysis_artifacts.notes", errors, summaries)

    ids = slide_ids(spec)
    for item in ensure_list(artifacts.get("queries")):
        if isinstance(item, str):
            query_path = item
            query_id = item
        elif isinstance(item, dict):
            query_path = str(item.get("path") or "").strip()
            query_id = str(item.get("id") or query_path).strip()
        else:
            errors.append("analysis_artifacts.queries entries must be strings or mappings")
            continue
        if not query_path:
            errors.append(f"analysis_artifacts.queries entry has no path: {query_id}")
            continue
        validate_existing_file(spec_path, query_path, f"analysis_artifacts.queries.{query_id}", errors, summaries)

    for item in ensure_list(artifacts.get("tables")):
        if not isinstance(item, dict):
            errors.append("analysis_artifacts.tables entries must be mappings")
            continue
        table_id = str(item.get("id") or item.get("path") or "").strip()
        table_path = str(item.get("path") or "").strip()
        if not table_path:
            errors.append(f"analysis_artifacts.tables entry has no path: {table_id or '<unknown>'}")
            continue
        required_columns = [str(value) for value in ensure_list(item.get("required_columns"))]
        validate_existing_file(
            spec_path,
            table_path,
            f"analysis_artifacts.tables.{table_id or table_path}",
            errors,
            summaries,
            csv_required_columns=required_columns,
        )
        for slide_id in ensure_list(item.get("used_by_slides")):
            if str(slide_id) not in ids:
                errors.append(
                    f"analysis_artifacts.tables.{table_id or table_path} references unknown slide id: {slide_id}"
                )


def chart_specs(spec: dict) -> list[tuple[dict, dict]]:
    pairs: list[tuple[dict, dict]] = []
    for slide in ensure_list(spec.get("slides")):
        if not isinstance(slide, dict):
            continue
        content = slide.get("content") if isinstance(slide.get("content"), dict) else {}
        chart = slide.get("chart") or content.get("chart")
        if isinstance(chart, dict):
            pairs.append((slide, chart))
    return pairs


def validate_chart_data(
    spec_path: Path,
    spec: dict,
    errors: list[str],
    warnings: list[str],
    summaries: list[dict],
) -> None:
    charts = chart_specs(spec)
    for slide, chart in charts:
        slide_id = slide.get("id")
        data_ref = chart.get("data_ref") or chart.get("data")
        if not data_ref:
            warnings.append(f"slide {slide_id} has a chart without data_ref")
            continue
        try:
            data = read_chart_data(spec_path, chart, allow_missing_data=False)
        except SystemExit as exc:
            errors.append(f"slide {slide_id} chart data is invalid: {exc}")
            continue
        if data:
            summaries.append(
                {
                    "path": data.get("source"),
                    "categories": len(data.get("categories") or []),
                    "series": [series.get("name") for series in data.get("series") or []],
                }
            )
        if not str(chart.get("emphasis") or "").strip():
            warnings.append(f"slide {slide_id} chart should include emphasis that echoes the takeaway")

    slide_count = len([slide for slide in ensure_list(spec.get("slides")) if isinstance(slide, dict)])
    if slide_count >= 4 and len(charts) > max(2, slide_count // 2):
        warnings.append(
            "more than half the deck has chart blocks; confirm this is a storyline, not an analysis dump"
        )


def validate(path: Path) -> dict:
    spec = load_structured_file(path)
    errors: list[str] = []
    warnings: list[str] = []
    summaries: list[dict] = []

    validate_analysis_artifacts(path, spec, errors, summaries)
    validate_chart_data(path, spec, errors, warnings, summaries)

    return {
        "deck": str(path),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "checked_artifacts": summaries,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate data artifacts referenced by a deck.md.")
    parser.add_argument("deck_md", help="Path to deck.md or structured deck spec.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args(argv)

    payload = validate(Path(args.deck_md).expanduser().resolve())
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
