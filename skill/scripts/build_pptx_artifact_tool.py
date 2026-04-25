#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = Path(__file__).resolve().parents[1]
RUNTIME_NODE = (
    Path.home()
    / ".cache"
    / "codex-runtimes"
    / "codex-primary-runtime"
    / "dependencies"
    / "node"
    / "bin"
    / "node"
)
PRESENTATIONS_PLUGIN_ROOT = (
    Path.home()
    / ".codex"
    / "plugins"
    / "cache"
    / "openai-primary-runtime"
    / "presentations"
)

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SLIDE_HEADING_RE = re.compile(
    r'^### Slide\s+(.+?)\s+(?:\u2014|-)\s+"(.+?)"\s*$',
    re.MULTILINE,
)
FENCED_YAML_RE = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def die(message: str) -> None:
    raise SystemExit(message)


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise SystemExit(detail or f"Command failed: {' '.join(command)}")
    return result


def presentations_skill_dir() -> Path:
    candidates = sorted(PRESENTATIONS_PLUGIN_ROOT.glob("*/skills/presentations"), reverse=True)
    for candidate in candidates:
        if (candidate / "scripts" / "create_presentation_workspace.js").exists():
            return candidate
    die(
        "Could not find the Presentations plugin runtime. "
        "Install or refresh the Codex Presentations plugin."
    )


def load_yaml_mapping(text: str, path: Path, context: str) -> dict:
    try:
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError as exc:
        die(f"invalid YAML in {context}: {path}: {exc}")
    if not isinstance(data, dict):
        die(f"{context} must be a mapping: {path}")
    return data


def split_markdown_frontmatter(text: str, path: Path) -> tuple[dict, str] | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    frontmatter = load_yaml_mapping(match.group(1), path, "frontmatter")
    return frontmatter, text[match.end() :]


def parse_sources(markdown: str) -> str | None:
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        match = re.match(r"^\*\*sources?:\*\*\s*(.*)$", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.match(r"^sources?:\s*(.*)$", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def parse_markdown_items(markdown: str) -> list[dict[str, str]]:
    body = FENCED_YAML_RE.sub("", markdown)
    body = HTML_COMMENT_RE.sub("", body)

    items: list[dict[str, str]] = []
    paragraphs: list[str] = []
    in_speaker_notes = False
    in_body_label = False

    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line or line == "---":
            continue
        lower = line.lower()
        if lower in {"**body**", "body"}:
            in_body_label = True
            continue
        if lower.startswith("**sources:**") or lower.startswith("sources:"):
            in_speaker_notes = False
            continue
        if lower.startswith("**speaker notes:**") or lower.startswith("speaker notes:"):
            in_speaker_notes = True
            continue
        if in_speaker_notes or line.startswith("#") or line.startswith("<"):
            continue
        if line.startswith("**") and line.endswith("**") and not in_body_label:
            continue

        bullet = re.match(r"^(?:[-*]|\d+[.)])\s+(.+)$", line)
        text = bullet.group(1).strip() if bullet else line
        text = re.sub(r"\s+", " ", text)

        labeled = re.match(r"^\*\*(.+?)[.:]?\*\*\s*[-:]\s*(.+)$", text)
        sentence_label = re.match(r"^\*\*(.+?)[.:]?\*\*\s*(.+)$", text)
        if labeled:
            items.append({"lead": labeled.group(1).strip(), "body": labeled.group(2).strip()})
        elif sentence_label:
            items.append({"lead": sentence_label.group(1).strip(), "body": sentence_label.group(2).strip()})
        elif bullet:
            items.append({"lead": text, "body": ""})
        else:
            paragraphs.append(text)

    if not items and paragraphs:
        joined = " ".join(paragraphs).strip()
        if joined:
            items.append({"lead": joined, "body": ""})
    return items


def parse_deck_markdown(path: Path, text: str) -> dict | None:
    split = split_markdown_frontmatter(text, path)
    if not split:
        return None

    frontmatter, body = split
    if "## Slides" not in body or "deck" not in frontmatter:
        return None

    slides_section = body.split("## Slides", 1)[1]
    headings = list(SLIDE_HEADING_RE.finditer(slides_section))
    if not headings:
        die(f"No deck.md slide headings found in {path}")

    slides: list[dict] = []
    for index, heading in enumerate(headings):
        segment_end = headings[index + 1].start() if index + 1 < len(headings) else len(slides_section)
        segment = slides_section[heading.end() : segment_end]

        metadata: dict = {}
        for block_index, block in enumerate(FENCED_YAML_RE.findall(segment)):
            block_data = load_yaml_mapping(block, path, f"slide {index + 1} YAML block")
            if block_index == 0 and {"id", "type", "layout", "mode", "image_decision"} & set(block_data):
                metadata.update(block_data)
            else:
                for key in ("chart", "table", "creative_direction", "required_text"):
                    if key in block_data:
                        metadata[key] = block_data[key]

        slide_type = str(metadata.get("type") or "").strip()
        body_items = parse_markdown_items(segment)
        content: dict = {"body": body_items}
        if slide_type == "roadmap":
            content["phases"] = body_items
        if slide_type == "framework" and body_items:
            content["quadrants"] = body_items[:4]
        if metadata.get("chart"):
            content["chart"] = metadata["chart"]
        if metadata.get("table"):
            content["table"] = metadata["table"]

        slide = {
            "id": metadata.get("id") or heading.group(1).strip(),
            "title": heading.group(2).strip(),
            "type": slide_type,
            "layout": metadata.get("layout"),
            "mode": metadata.get("mode"),
            "slide_mode": metadata.get("mode"),
            "template": metadata.get("template"),
            "image_decision": metadata.get("image_decision"),
            "asset_refs": ensure_list(metadata.get("asset_refs")),
            "content": content,
            "sources": parse_sources(segment),
        }
        if metadata.get("chart"):
            slide["chart"] = metadata["chart"]
        if metadata.get("table"):
            slide["table"] = metadata["table"]
        slides.append(slide)

    return {
        "schema_version": frontmatter.get("schema_version"),
        "status": frontmatter.get("status"),
        "deck": frontmatter.get("deck") or {},
        "narrative_template": frontmatter.get("narrative_template"),
        "production_defaults": frontmatter.get("production_defaults") or {},
        "image_generation": frontmatter.get("image_generation") or {},
        "designer_assets": frontmatter.get("designer_assets") or [],
        "analysis_artifacts": frontmatter.get("analysis_artifacts") or {},
        "design_tokens": frontmatter.get("design_tokens") or {},
        "slides": slides,
    }


def load_structured_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".md":
        deck = parse_deck_markdown(path, text)
        if deck is not None:
            return deck
        return load_yaml_mapping(text, path, "spec root")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return load_yaml_mapping(text, path, "spec root")
    return json.loads(text)


def normalize_mode(deck_mode: str | None, slide: dict) -> str:
    deck_mode = (deck_mode or "").strip().lower()
    slide_mode = str(slide.get("slide_mode") or slide.get("mode") or "").strip().lower()
    if deck_mode == "mixed":
        if slide_mode not in {"ppt-shapes", "designer-mode"}:
            die(f"mixed decks require mode per slide; missing on slide id={slide.get('id')}")
        return slide_mode
    if slide_mode in {"ppt-shapes", "designer-mode"}:
        return slide_mode
    if deck_mode in {"ppt-shapes", "designer-mode"}:
        return deck_mode
    return slide_mode or "ppt-shapes"


def infer_archetype(slide: dict) -> str:
    slide_type = str(slide.get("type") or "").strip().lower().replace("_", "-")
    template = str(slide.get("template") or "").strip().lower()
    layout = str(slide.get("layout") or "").strip().lower()
    content = slide.get("content") or {}
    chart = slide.get("chart") or (content.get("chart") if isinstance(content, dict) else None) or {}
    chart_type = str(chart.get("type") or "").strip().lower() if isinstance(chart, dict) else ""
    for value in (template, layout, slide_type):
        if value in {"takeaway", "takeaway + support"}:
            return "takeaway"
        if value == "agenda":
            return "agenda"
        if value in {"horizontal process", "process"}:
            return "process"
        if value == "matrix":
            return "matrix"
        if value in {"bar-column", "bar column"}:
            return "chart"
        if value in {"section-divider", "section divider"}:
            return "section-divider"
        if value == "quote":
            return "quote"
    if slide_type == "section-divider":
        return "section-divider"
    if slide_type == "roadmap" or "timeline" in layout or "roadmap" in layout:
        return "process"
    if slide_type == "framework" and any(token in layout for token in ("2x2", "matrix", "quadrant")):
        return "matrix"
    if slide_type == "chart" or chart_type:
        return "chart"
    if slide_type in {
        "executive-summary",
        "situation",
        "complication",
        "key-takeaways",
        "analysis",
        "framework",
        "recommendation",
        "risk-mitigation",
        "next-steps",
        "appendix",
    }:
        return "takeaway"
    return "takeaway"


def ensure_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def slugify(value: str, default: str = "asset") -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(value or "")).strip("-").lower()
    return slug or default


def is_remote_ref(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"}


def resolve_local_ref(spec_path: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = spec_path.parent / path
    return path.resolve()


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "required"}
    return bool(value)


def copy_declared_asset(source: Path, destination_root: Path, asset_id: str) -> Path:
    safe_id = slugify(asset_id)
    if source.is_dir():
        destination = destination_root / safe_id
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        return destination

    suffix = source.suffix or ".asset"
    destination = destination_root / f"{safe_id}{suffix}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def download_declared_asset(source: str, destination_root: Path, asset_id: str) -> Path:
    safe_id = slugify(asset_id)
    suffix = Path(urlparse(source).path).suffix or ".asset"
    destination = destination_root / f"{safe_id}{suffix}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(source, headers={"User-Agent": "deck-architect/1.0"})
    with urlopen(request, timeout=30) as response:
        status = getattr(response, "status", 200)
        if status >= 400:
            raise OSError(f"HTTP {status}")
        destination.write_bytes(response.read())
    return destination


def prepare_external_assets(spec_path: Path, spec: dict, workspace: Path) -> list[dict]:
    raw_assets = spec.get("designer_assets") or []
    if raw_assets is None:
        raw_assets = []
    if not isinstance(raw_assets, list):
        die("designer_assets must be a list when present")

    scratch_assets = workspace / "scratch" / "assets"
    scratch_assets.mkdir(parents=True, exist_ok=True)
    prepared: list[dict] = []
    seen: set[str] = set()

    for index, raw in enumerate(raw_assets, start=1):
        if not isinstance(raw, dict):
            die(f"designer_assets item {index} must be a mapping")
        asset_id = str(raw.get("id") or "").strip()
        if not asset_id:
            die(f"designer_assets item {index} is missing id")
        if asset_id in seen:
            die(f"duplicate designer_assets id: {asset_id}")
        seen.add(asset_id)

        source = str(raw.get("path") or raw.get("url") or "").strip()
        required = boolish(raw.get("required", False))
        record = {
            "id": asset_id,
            "type": str(raw.get("type") or "other").strip() or "other",
            "source": source,
            "usage": raw.get("usage"),
            "scope": raw.get("scope") or "deck",
            "placement": raw.get("placement"),
            "required": required,
            "notes": raw.get("notes"),
            "exists": False,
            "remote": False,
            "prepared_path": None,
        }

        if not source:
            if required:
                die(f"required designer asset has no path/url: {asset_id}")
            prepared.append(record)
            continue

        if is_remote_ref(source):
            record["remote"] = True
            try:
                downloaded = download_declared_asset(source, scratch_assets, asset_id)
            except Exception as exc:
                record["download_error"] = str(exc)
                if required:
                    die(f"required designer asset URL could not be downloaded: {asset_id} -> {source}: {exc}")
                prepared.append(record)
                continue
            record["exists"] = True
            record["prepared_path"] = downloaded.relative_to(workspace).as_posix()
            prepared.append(record)
            continue

        local_path = resolve_local_ref(spec_path, source)
        record["source_path"] = str(local_path)
        if not local_path.exists():
            if required:
                die(f"required designer asset not found: {asset_id} -> {local_path}")
            prepared.append(record)
            continue

        copied = copy_declared_asset(local_path, scratch_assets, asset_id)
        record["exists"] = True
        record["is_directory"] = copied.is_dir()
        record["prepared_path"] = copied.relative_to(workspace).as_posix()
        prepared.append(record)

    asset_log = workspace / "scratch" / "external-assets.json"
    asset_log.write_text(json.dumps(prepared, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return prepared


def attach_prepared_assets(rendered: dict, assets: list[dict]) -> None:
    rendered["prepared_assets"] = assets
    ids = {asset["id"] for asset in assets}
    for slide in rendered.get("slides", []):
        refs = ensure_list(slide.get("asset_refs"))
        missing = [ref for ref in refs if ref not in ids]
        if missing:
            die(f"slide id={slide.get('id')} references undeclared designer_assets ids: {', '.join(map(str, missing))}")


def read_chart_data(spec_path: Path, chart_spec: dict, allow_missing_data: bool) -> dict | None:
    data_ref = chart_spec.get("data_ref") or chart_spec.get("data")
    if not data_ref:
        return None

    data_path = Path(str(data_ref)).expanduser()
    if not data_path.is_absolute():
        data_path = spec_path.parent / data_path
    if not data_path.exists():
        if allow_missing_data:
            return {
                "missing": True,
                "message": f"Missing chart data: {data_ref}",
                "source": str(data_ref),
            }
        die(f"Missing chart data for chart slide: {data_path}")

    rows: list[dict[str, str]] = []
    with data_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(row)

    if not rows or not reader.fieldnames:
        die(f"Chart data is empty: {data_path}")

    fields = list(reader.fieldnames)
    numeric_fields: list[str] = []
    for field in fields:
        ok = True
        for row in rows:
            value = str(row.get(field, "")).strip().replace(",", "")
            if value == "":
                continue
            try:
                float(value)
            except ValueError:
                ok = False
                break
        if ok:
            numeric_fields.append(field)

    category_field = next((field for field in fields if field not in numeric_fields), fields[0])
    if not numeric_fields:
        die(f"Could not find numeric series in chart data: {data_path}")

    categories = [str(row.get(category_field, "")).strip() or f"Row {idx + 1}" for idx, row in enumerate(rows)]
    series = []
    for field in numeric_fields:
        values = []
        for row in rows:
            raw = str(row.get(field, "")).strip().replace(",", "")
            values.append(float(raw) if raw else 0)
        series.append({"name": field, "values": values})

    return {
        "categories": categories,
        "series": series,
        "source": str(data_path),
    }


def chart_from_bars(bars: list) -> dict | None:
    categories: list[str] = []
    values: list[float] = []
    for idx, item in enumerate(bars):
        if isinstance(item, dict):
            label = str(item.get("label") or item.get("name") or item.get("lead") or f"Item {idx + 1}")
            value = item.get("value")
        else:
            label = str(item)
            value = None
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            continue
        categories.append(label)
        values.append(numeric)
    if not categories:
        return None
    return {"categories": categories, "series": [{"name": "Value", "values": values}]}


def compile_slide_payload(spec_path: Path, slide: dict, allow_missing_data: bool) -> dict:
    content = slide.get("content") or {}
    archetype = infer_archetype(slide)
    chart_spec = slide.get("chart") or content.get("chart") or {}
    body_items = ensure_list(content.get("body"))

    payload = {
        "id": slide.get("id"),
        "archetype": archetype,
        "title": slide.get("title") or "Untitled slide",
        "subtitle": slide.get("subtitle"),
        "sources": slide.get("sources"),
        "asset_refs": ensure_list(slide.get("asset_refs")),
        "bullets": body_items,
    }

    if archetype == "agenda":
        payload["sections"] = ensure_list(content.get("sections") or content.get("items") or body_items)
    elif archetype == "process":
        payload["phases"] = ensure_list(content.get("steps") or content.get("phases") or body_items)
    elif archetype == "matrix":
        axes = content.get("axes") or {}
        payload["x_axis"] = content.get("x_axis") or axes.get("x")
        payload["y_axis"] = content.get("y_axis") or axes.get("y")
        payload["quadrants"] = ensure_list(content.get("quadrants") or body_items)[:4]
    elif archetype == "quote":
        quote_value = content.get("quote") or slide.get("quote")
        if isinstance(quote_value, list):
            quote_value = " ".join(str(x) for x in quote_value)
        payload["quote"] = quote_value or payload["title"]
        payload["attribution"] = content.get("attribution") or slide.get("attribution")
    elif archetype == "chart":
        chart_data = read_chart_data(spec_path, chart_spec, allow_missing_data) if chart_spec else None
        if not chart_data:
            chart_data = chart_from_bars(ensure_list(content.get("bars")))
        payload["chart"] = {
            "type": str(chart_spec.get("type") or "bar").lower() if isinstance(chart_spec, dict) else "bar",
            "emphasis": chart_spec.get("emphasis") if isinstance(chart_spec, dict) else None,
            "annotation": chart_spec.get("annotation") if isinstance(chart_spec, dict) else None,
            "data": chart_data,
        }

    return payload


def footer_config_from_spec(spec: dict) -> dict:
    production = spec.get("production_defaults") or {}
    footer = spec.get("footer") or production.get("footer") or {}
    if not isinstance(footer, dict):
        footer = {}
    return {
        "enabled": footer.get("enabled", True),
        "page_numbers": footer.get("page_numbers", True),
        "cr_mark": footer.get("cr_mark", True),
        "cr_text": str(footer.get("cr_text") or footer.get("cr") or "CR"),
    }


def rendered_spec(spec_path: Path, spec: dict, allow_missing_data: bool) -> dict:
    production_defaults = spec.get("production_defaults") or {}
    deck_mode = production_defaults.get("default_slide_mode")
    slides = spec.get("Slides") or spec.get("slides") or []
    if not isinstance(slides, list):
        die("Slides must be a list in the deck spec")

    rendered = []
    skipped = 0
    for page_number, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            continue
        mode = normalize_mode(deck_mode, slide)
        if mode != "ppt-shapes":
            skipped += 1
            continue
        payload = compile_slide_payload(spec_path, slide, allow_missing_data)
        payload["page_number"] = page_number
        rendered.append(payload)

    if not rendered:
        die("No ppt-shapes slides found to render from the deck spec")
    return {
        "deck": spec.get("deck") or {},
        "design_tokens": spec.get("design_tokens") or {},
        "production_defaults": production_defaults,
        "footer": footer_config_from_spec(spec),
        "slides": rendered,
        "skipped": skipped,
    }


def default_workspace_for_output(output: Path) -> Path:
    if output.parent.name == "outputs":
        instance_dir = output.parent.parent
    else:
        instance_dir = output.parent
    return instance_dir / "method" / "artifact-tool-workspace"


def write_deck_module(workspace: Path, deck_spec: dict) -> Path:
    module_path = workspace / "src" / "deck.mjs"
    module_path.parent.mkdir(parents=True, exist_ok=True)
    deck_json = json.dumps(deck_spec, ensure_ascii=False, indent=2)
    module_path.write_text(
        f"""import fs from "node:fs";
import path from "node:path";

const {{
  Presentation,
  PresentationFile,
  row,
  column,
  grid,
  panel,
  text,
  image,
  shape,
  chart,
  rule,
  fill,
  hug,
  fixed,
  wrap,
  grow,
  fr,
  auto,
}} = await import("@oai/artifact-tool");

const deck = {deck_json};

const W = 1920;
const H = 1080;
const palette = {{
  primary: "#111111",
  secondary: "#5B5B5B",
  accent: "#2F6BFF",
  accentSoft: "#DCE7FF",
  background: "#FFFFFF",
  line: "#B8C7E6",
  ...(deck.design_tokens?.palette || {{}}),
}};
palette.accentSoft = palette.accent_soft || palette.accentSoft;
const font = {{
  title: "Aptos Display",
  body: "Aptos",
}};

const presentation = Presentation.create({{ slideSize: {{ width: W, height: H }} }});
const previewDir = path.join("scratch", "previews");
const layoutDir = path.join("scratch", "layouts");
fs.mkdirSync(previewDir, {{ recursive: true }});
fs.mkdirSync(layoutDir, {{ recursive: true }});

function t(value, options = {{}}) {{
  return text(String(value || ""), {{
    width: options.width ?? fill,
    height: options.height ?? hug,
    name: options.name,
    columnSpan: options.columnSpan,
    rowSpan: options.rowSpan,
    style: {{
      fontFace: options.fontFace || font.body,
      fontSize: options.fontSize || 26,
      bold: options.bold || false,
      italic: options.italic || false,
      color: options.color || palette.primary,
    }},
  }});
}}

function itemText(item) {{
  if (typeof item === "string") return item;
  const lead = item?.lead || item?.title || item?.label || "";
  const body = item?.body || item?.caption || item?.description || "";
  const cleanBody = String(body || "").replace(/^[\\s:\\u2013\\u2014-]+/, "").trim();
  return cleanBody ? `${{lead}}: ${{cleanBody}}` : lead;
}}

function shortItems(items, max = 5) {{
  return (items || []).map(itemText).filter(Boolean).slice(0, max);
}}

function footer(slide) {{
  if (!deck.footer?.enabled) return t("", {{ fontSize: 1 }});
  const left = deck.footer.cr_mark ? deck.footer.cr_text || "CR" : "";
  const right = deck.footer.page_numbers ? String(slide.page_number || "") : "";
  return row({{ name: "footer", width: fill, height: hug, justify: "between", align: "end" }}, [
    t(left, {{ name: "footer-cr", width: fixed(260), fontSize: 15, color: palette.secondary }}),
    t(right, {{ name: "footer-page", width: fixed(120), fontSize: 15, color: palette.secondary }}),
  ]);
}}

function assetApplies(asset, slide) {{
  if (!asset?.exists || !asset?.prepared_path) return false;
  const refs = slide.asset_refs || [];
  return refs.includes(asset.id) || asset.scope === "deck";
}}

function firstPreparedAsset(slide, types) {{
  const wanted = new Set(types);
  return (deck.prepared_assets || []).find((asset) => wanted.has(asset.type) && assetApplies(asset, slide));
}}

function logoNode(slide) {{
  const asset = firstPreparedAsset(slide, ["logo"]);
  if (!asset) return null;
  return image({{
    name: `asset-${{asset.id}}`,
    path: asset.prepared_path,
    width: fixed(190),
    height: fixed(66),
    fit: "contain",
    alt: asset.id,
  }});
}}

function titleStack(slide, subtitle) {{
  return column({{ name: "title-stack", width: fill, height: hug, gap: 14 }}, [
    t(slide.title, {{
      name: "slide-title",
      width: wrap(1600),
      fontFace: font.title,
      fontSize: slide.title.length > 95 ? 39 : 46,
      bold: true,
      color: palette.primary,
    }}),
    subtitle ? t(subtitle, {{ name: "slide-subtitle", width: wrap(1280), fontSize: 24, color: palette.secondary }}) : null,
  ].filter(Boolean));
}}

function sourceLine(slide) {{
  if (!slide.sources) return null;
  return t(`Source: ${{slide.sources}}`, {{
    name: "source",
    width: fill,
    fontSize: 14,
    color: palette.secondary,
  }});
}}

function bulletList(items, name = "proof-list") {{
  const children = shortItems(items).map((value, idx) =>
    row({{ name: `${{name}}-${{idx + 1}}`, width: fill, height: hug, gap: 18, align: "start" }}, [
      shape({{ name: `${{name}}-mark-${{idx + 1}}`, width: fixed(9), height: fixed(34), fill: palette.accent, line: {{ style: "none" }} }}),
      t(value, {{ name: `${{name}}-text-${{idx + 1}}`, width: fill, fontSize: 27, color: palette.primary }}),
    ])
  );
  if (!children.length) {{
    children.push(t("Add supporting evidence in the approved deck.md.", {{ name: `${{name}}-empty`, width: wrap(980), fontSize: 28, color: palette.secondary }}));
  }}
  return column({{ name, width: fill, height: hug, gap: 24 }}, children);
}}

function root(slide, bodyChildren, options = {{}}) {{
  const slideObj = presentation.slides.add();
  const logo = logoNode(slide);
  slideObj.compose(
    grid(
      {{
        name: "slide-root",
        width: fill,
        height: fill,
        columns: [fr(1)],
        rows: [auto, fr(1), auto],
        rowGap: 34,
        padding: {{ x: 86, y: 64 }},
      }},
      [
        row({{ name: "header", width: fill, height: hug, justify: "between", align: "start", gap: 36 }}, [
          titleStack(slide, options.subtitle),
          logo,
        ].filter(Boolean)),
        column({{ name: "body", width: fill, height: fill, gap: 22 }}, bodyChildren.filter(Boolean)),
        footer(slide),
      ],
    ),
    {{ frame: {{ left: 0, top: 0, width: W, height: H }}, baseUnit: 8 }},
  );
  return slideObj;
}}

function renderTakeaway(slide) {{
  const body = [bulletList(slide.bullets), sourceLine(slide)];
  return root(slide, body, {{ subtitle: slide.subtitle }});
}}

function renderAgenda(slide) {{
  const sections = shortItems(slide.sections || slide.bullets, 6);
  const rows = sections.map((label, idx) =>
    row({{ name: `agenda-item-${{idx + 1}}`, width: fill, height: hug, gap: 28, align: "center" }}, [
      t(String(idx + 1).padStart(2, "0"), {{ name: `agenda-num-${{idx + 1}}`, width: fixed(80), fontSize: 30, bold: true, color: palette.accent }}),
      column({{ name: `agenda-copy-${{idx + 1}}`, width: fill, height: hug, gap: 12 }}, [
        t(label, {{ name: `agenda-label-${{idx + 1}}`, width: fill, fontSize: 30, bold: true, color: palette.primary }}),
        rule({{ name: `agenda-rule-${{idx + 1}}`, width: fill, stroke: palette.line, weight: 1 }}),
      ]),
    ])
  );
  return root(slide, [column({{ name: "agenda-list", width: fill, height: hug, gap: 24 }}, rows), sourceLine(slide)], {{ subtitle: slide.subtitle }});
}}

function renderProcess(slide) {{
  const phases = shortItems(slide.phases || slide.bullets, 5);
  const cards = phases.map((label, idx) =>
    panel(
      {{
        name: `process-step-${{idx + 1}}`,
        width: grow(1),
        height: fill,
        fill: idx === 0 ? palette.accentSoft : "#F8FAFC",
        line: {{ style: "solid", width: 1, fill: palette.line }},
        padding: {{ x: 28, y: 28 }},
        borderRadius: "rounded-md",
      }},
      column({{ width: fill, height: fill, gap: 22 }}, [
        t(String(idx + 1), {{ name: `process-number-${{idx + 1}}`, width: fixed(80), fontSize: 36, bold: true, color: palette.accent }}),
        t(label, {{ name: `process-label-${{idx + 1}}`, width: fill, fontSize: 26, bold: true, color: palette.primary }}),
      ]),
    )
  );
  return root(slide, [row({{ name: "process-row", width: fill, height: fill, gap: 24 }}, cards), sourceLine(slide)], {{ subtitle: slide.subtitle }});
}}

function renderMatrix(slide) {{
  const quadrants = shortItems(slide.quadrants || slide.bullets, 4);
  while (quadrants.length < 4) quadrants.push("");
  const cells = quadrants.map((label, idx) =>
    panel(
      {{
        name: `matrix-cell-${{idx + 1}}`,
        width: fill,
        height: fill,
        fill: idx === 0 ? palette.accentSoft : "#F8FAFC",
        line: {{ style: "solid", width: 1, fill: palette.line }},
        padding: {{ x: 30, y: 28 }},
        borderRadius: "rounded-md",
      }},
      t(label, {{ name: `matrix-label-${{idx + 1}}`, width: fill, fontSize: 25, bold: Boolean(label), color: palette.primary }}),
    )
  );
  return root(slide, [
    grid({{ name: "matrix", width: fill, height: fill, columns: [fr(1), fr(1)], rows: [fr(1), fr(1)], columnGap: 20, rowGap: 20 }}, cells),
    sourceLine(slide),
  ], {{ subtitle: slide.subtitle }});
}}

function chartTypeFor(slide) {{
  const type = String(slide.chart?.type || "bar").toLowerCase();
  if (type.includes("line")) return "line";
  if (type.includes("scatter")) return "scatter";
  if (type.includes("doughnut")) return "doughnut";
  if (type.includes("pie")) return "pie";
  return "bar";
}}

function renderChart(slide) {{
  const data = slide.chart?.data;
  if (!data || data.missing) {{
    return root(slide, [
      t(data?.message || "Chart data was not available at build time.", {{ name: "chart-missing", width: wrap(1120), fontSize: 34, bold: true, color: palette.accent }}),
      bulletList(slide.bullets),
      sourceLine(slide),
    ], {{ subtitle: slide.chart?.emphasis || slide.subtitle }});
  }}
  const chartNode = chart({{
    name: "chart-main",
    chartType: chartTypeFor(slide),
    width: fill,
    height: fill,
    config: {{
      title: slide.chart?.emphasis || "",
      categories: data.categories,
      series: data.series,
    }},
  }});
  const proof = [
    slide.chart?.annotation ? t(slide.chart.annotation, {{ name: "chart-annotation", width: fill, fontSize: 30, bold: true, color: palette.primary }}) : null,
    bulletList(slide.bullets, "chart-proof"),
  ].filter(Boolean);
  return root(slide, [
    grid({{ name: "chart-layout", width: fill, height: fill, columns: [fr(1.35), fr(0.65)], columnGap: 44 }}, [
      chartNode,
      column({{ name: "chart-side", width: fill, height: fill, gap: 28 }}, proof),
    ]),
    sourceLine(slide),
  ], {{ subtitle: slide.subtitle }});
}}

function renderSection(slide) {{
  const slideObj = presentation.slides.add();
  const logo = logoNode(slide);
  slideObj.compose(
    grid({{ name: "section-root", width: fill, height: fill, columns: [fr(1)], rows: [auto, fr(1), auto], padding: {{ x: 92, y: 78 }} }}, [
      row({{ name: "section-header", width: fill, height: hug, justify: "end" }}, [logo].filter(Boolean)),
      column({{ name: "section-title-stack", width: fill, height: fill, justify: "center", gap: 28 }}, [
        rule({{ name: "section-rule", width: fixed(260), stroke: palette.accent, weight: 7 }}),
        t(slide.title, {{ name: "slide-title", width: wrap(1400), fontFace: font.title, fontSize: 64, bold: true, color: palette.primary }}),
      ]),
      footer(slide),
    ]),
    {{ frame: {{ left: 0, top: 0, width: W, height: H }}, baseUnit: 8 }},
  );
  return slideObj;
}}

function renderQuote(slide) {{
  return root(slide, [
    column({{ name: "quote-block", width: fill, height: fill, justify: "center", gap: 28 }}, [
      t(`"${{slide.quote || slide.title}}"`, {{ name: "quote", width: wrap(1320), fontFace: font.title, fontSize: 52, bold: true, color: palette.primary }}),
      slide.attribution ? t(slide.attribution, {{ name: "quote-attribution", width: wrap(900), fontSize: 24, color: palette.secondary }}) : null,
    ].filter(Boolean)),
    sourceLine(slide),
  ], {{ subtitle: slide.subtitle }});
}}

function renderSlide(slide) {{
  if (slide.archetype === "agenda") return renderAgenda(slide);
  if (slide.archetype === "process") return renderProcess(slide);
  if (slide.archetype === "matrix") return renderMatrix(slide);
  if (slide.archetype === "chart") return renderChart(slide);
  if (slide.archetype === "section-divider") return renderSection(slide);
  if (slide.archetype === "quote") return renderQuote(slide);
  return renderTakeaway(slide);
}}

for (const slide of deck.slides) {{
  renderSlide(slide);
}}

for (let index = 0; index < presentation.slides.count; index += 1) {{
  const slide = presentation.slides.getItem(index);
  const png = await slide.export({{ format: "png" }});
  fs.writeFileSync(path.join(previewDir, `slide-${{String(index + 1).padStart(2, "0")}}.png`), Buffer.from(await png.arrayBuffer()));
  const layout = await slide.export({{ format: "layout" }});
  fs.writeFileSync(path.join(layoutDir, `slide-${{String(index + 1).padStart(2, "0")}}.layout.json`), JSON.stringify(layout, null, 2));
}}

const pptxBlob = await PresentationFile.exportPptx(presentation);
await pptxBlob.save("output/output.pptx");
fs.writeFileSync("scratch/build-report.json", JSON.stringify({{
  slide_count: deck.slides.length,
  skipped_non_ppt_shapes: deck.skipped || 0,
  prepared_assets: (deck.prepared_assets || []).map((asset) => ({{
    id: asset.id,
    type: asset.type,
    scope: asset.scope,
    exists: asset.exists,
    remote: asset.remote,
    prepared_path: asset.prepared_path,
  }})),
  previews: previewDir,
  output: "output/output.pptx",
}}, null, 2));
""",
        encoding="utf-8",
    )
    return module_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build editable ppt-shapes slides with @oai/artifact-tool."
    )
    parser.add_argument("output_pptx", help="Final PPTX path to write.")
    parser.add_argument("deck_md", help="Approved deck.md, YAML, or JSON spec.")
    parser.add_argument(
        "--workspace",
        help="Artifact-tool workspace. Defaults to <instance>/method/artifact-tool-workspace.",
    )
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="Allow building a deck.md whose frontmatter status is not approved.",
    )
    parser.add_argument(
        "--allow-missing-data",
        action="store_true",
        help="Render chart placeholders instead of failing on missing chart data files.",
    )
    parser.add_argument(
        "--skip-quality-check",
        action="store_true",
        help="Skip headless PPTX package quality checks.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    output = Path(args.output_pptx).expanduser().resolve()
    spec_path = Path(args.deck_md).expanduser().resolve()
    if not spec_path.exists():
        die(f"Deck spec does not exist: {spec_path}")
    output.parent.mkdir(parents=True, exist_ok=True)

    spec = load_structured_file(spec_path)
    if spec.get("status") != "approved" and not args.allow_draft:
        die(
            "Refusing to build before deck.md approval. "
            "Set status: approved or rerun with --allow-draft for local testing."
        )

    prepared = rendered_spec(spec_path, spec, args.allow_missing_data)
    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else default_workspace_for_output(output)
    plugin_skill = presentations_skill_dir()
    create_workspace = plugin_skill / "scripts" / "create_presentation_workspace.js"
    check_quality = plugin_skill / "scripts" / "check_presentation_quality.js"
    deck_slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", output.stem).strip("-").lower() or "deck"

    if not RUNTIME_NODE.exists():
        die(f"Could not find Codex runtime Node executable: {RUNTIME_NODE}")

    setup = run(
        [
            str(RUNTIME_NODE),
            str(create_workspace),
            "--deck-id",
            deck_slug,
            "--workspace",
            str(workspace),
            "--force",
        ]
    )
    setup_info = json.loads(setup.stdout)

    spec_json_path = workspace / "scratch" / "deck-render-spec.json"
    spec_json_path.parent.mkdir(parents=True, exist_ok=True)

    prepared_assets = prepare_external_assets(spec_path, spec, workspace)
    attach_prepared_assets(prepared, prepared_assets)
    spec_json_path.write_text(json.dumps(prepared, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    module_path = write_deck_module(workspace, prepared)
    run([setup_info["node"], str(module_path)], cwd=workspace)

    workspace_pptx = workspace / "output" / "output.pptx"
    if not workspace_pptx.exists() or workspace_pptx.stat().st_size == 0:
        die(f"Artifact-tool build did not create a PPTX: {workspace_pptx}")

    if not args.skip_quality_check:
        run(
            [
                setup_info["node"],
                str(check_quality),
                "--workspace",
                str(workspace),
                "--pptx",
                str(workspace_pptx),
                "--report",
                str(workspace / "scratch" / "quality-report.json"),
            ]
        )

    shutil.copyfile(workspace_pptx, output)
    print(
        json.dumps(
            {
                "output_pptx": str(output),
                "workspace": str(workspace),
                "source_spec": str(spec_path),
                "rendered_slides": len(prepared["slides"]),
                "skipped_non_ppt_shapes": prepared.get("skipped", 0),
                "previews": str(workspace / "scratch" / "previews"),
                "quality_report": str(workspace / "scratch" / "quality-report.json"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
