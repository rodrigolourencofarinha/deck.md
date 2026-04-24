#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets" / "tabler-icons"
VARIANTS = ("outline", "filled")
SUGGESTIONS = {
    "process": {
        "aliases": ["flow", "workflow", "sequence"],
        "description": "Process flows, operating models, and step-by-step transitions",
        "icons": ["route", "route-2", "hierarchy-2", "arrow-ramp-right", "arrows-right"],
    },
    "roadmap": {
        "aliases": ["timeline", "milestones", "plan", "phases"],
        "description": "Roadmaps, phased plans, milestones, and direction-of-travel slides",
        "icons": ["map-route", "flag", "calendar-week", "calendar-time", "target-arrow"],
    },
    "analytics": {
        "aliases": ["analysis", "data", "dashboard", "charts"],
        "description": "Data, evidence, dashboards, and analytical proof slides",
        "icons": ["chart-bar", "chart-line", "chart-pie-2", "chart-donut", "report-analytics"],
    },
    "growth": {
        "aliases": ["trend", "momentum", "scale"],
        "description": "Growth, momentum, performance change, and upside stories",
        "icons": ["trending-up", "trending-up-2", "growth", "rocket", "target-arrow"],
    },
    "people": {
        "aliases": ["team", "org", "stakeholders", "users"],
        "description": "Teams, stakeholders, audiences, org structures, and customer groups",
        "icons": ["users", "users-group", "users-plus", "message-user", "hierarchy-2"],
    },
    "product": {
        "aliases": ["platform", "system", "tech", "app"],
        "description": "Products, platforms, systems, stacks, and digital-service slides",
        "icons": ["devices", "devices-2", "stack", "stack-2", "app-window"],
    },
    "communication": {
        "aliases": ["messages", "feedback", "conversation", "comms"],
        "description": "Communication, collaboration, feedback, and change-management slides",
        "icons": ["message", "messages", "message-dots", "message-user", "speakerphone"],
    },
    "security-risk": {
        "aliases": ["risk", "security", "compliance", "control"],
        "description": "Risk, security, controls, compliance, and issue framing",
        "icons": ["shield", "shield-check", "shield-lock", "alert-triangle", "alert-circle"],
    },
    "finance": {
        "aliases": ["money", "revenue", "budget", "pricing"],
        "description": "Financial performance, revenue, cost, savings, and value slides",
        "icons": ["coin", "coins", "wallet", "report-money", "pig-money"],
    },
    "timing": {
        "aliases": ["calendar", "schedule", "deadline", "time"],
        "description": "Timing, cadence, schedules, deadlines, and planning horizons",
        "icons": ["calendar", "calendar-week", "calendar-time", "clock", "alarm"],
    },
    "global": {
        "aliases": ["geography", "market", "footprint", "location"],
        "description": "Geography, footprint, site network, and multi-market slides",
        "icons": ["globe", "building", "buildings", "map-route", "flag"],
    },
    "quality": {
        "aliases": ["check", "validation", "completion", "priority"],
        "description": "Validation, completion, status, and quality-assurance slides",
        "icons": ["check", "checklist", "list-check", "flag-check", "target-arrow"],
    },
}


def normalize(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def load_aliases() -> dict[str, dict[str, str]]:
    path = ASSETS_DIR / "aliases.json"
    if not path.exists():
        return {variant: {} for variant in VARIANTS}
    data = json.loads(path.read_text())
    return {variant: data.get(variant, {}) for variant in VARIANTS}


def iter_icons(variant: str | None = None):
    variants = (variant,) if variant else VARIANTS
    aliases = load_aliases()
    for current_variant in variants:
        icon_dir = ASSETS_DIR / current_variant
        if not icon_dir.exists():
            continue
        current_aliases = aliases.get(current_variant, {})
        reverse_aliases: dict[str, list[str]] = {}
        for alias, canonical in current_aliases.items():
            reverse_aliases.setdefault(canonical, []).append(alias)
        for path in sorted(icon_dir.glob("*.svg")):
            canonical = path.stem
            yield {
                "variant": current_variant,
                "name": canonical,
                "path": path,
                "aliases": sorted(reverse_aliases.get(canonical, [])),
            }


def score_icon(name: str, aliases: list[str], terms: list[str], preferred_variant: str | None, variant: str):
    exact_name = name == " ".join(terms).replace(" ", "-")
    starts = all(name.startswith(term) for term in terms)
    alias_exact = any(alias == " ".join(terms).replace(" ", "-") for alias in aliases)
    variant_penalty = 0 if preferred_variant is None or variant == preferred_variant else 1
    alias_penalty = 0 if not aliases else 1
    return (
        variant_penalty,
        0 if exact_name else 1,
        0 if alias_exact else 1,
        0 if starts else 1,
        alias_penalty,
        len(name),
        name,
    )


def search_icons(query: str, variant: str | None, limit: int):
    terms = [normalize(part) for part in query.replace(",", " ").split() if part.strip()]
    if not terms:
        raise SystemExit("Search query cannot be empty")

    matches = []
    for icon in iter_icons(variant=variant):
        haystacks = [icon["name"], *icon["aliases"]]
        if all(any(term in haystack for haystack in haystacks) for term in terms):
            matches.append(icon)

    matches.sort(key=lambda icon: score_icon(icon["name"], icon["aliases"], terms, variant, icon["variant"]))
    return matches[:limit]


def resolve_icon(name: str, variant: str | None):
    canonical = normalize(name)
    aliases = load_aliases()
    variants = (variant,) if variant else VARIANTS
    for current_variant in variants:
        current_aliases = aliases.get(current_variant, {})
        resolved = current_aliases.get(canonical, canonical)
        candidate = ASSETS_DIR / current_variant / f"{resolved}.svg"
        if candidate.exists():
            return current_variant, resolved, candidate
    raise FileNotFoundError(f"Icon not found: {name}")


def resolve_topic(raw_topic: str):
    topic = normalize(raw_topic)
    if topic in SUGGESTIONS:
        return topic
    for canonical, data in SUGGESTIONS.items():
        if topic in [normalize(alias) for alias in data["aliases"]]:
            return canonical
    raise FileNotFoundError(f"Unknown topic: {raw_topic}")


def build_suggestions(topic: str):
    canonical_topic = resolve_topic(topic)
    data = SUGGESTIONS[canonical_topic]
    payload = []
    for icon_name in data["icons"]:
        variant, resolved, path = resolve_icon(icon_name, "outline")
        payload.append(
            {
                "topic": canonical_topic,
                "description": data["description"],
                "aliases": data["aliases"],
                "variant": variant,
                "name": resolved,
                "path": str(path),
            }
        )
    return canonical_topic, data, payload


def cmd_topics(args: argparse.Namespace) -> int:
    if args.json:
        print(json.dumps(SUGGESTIONS, indent=2))
        return 0
    for topic, data in SUGGESTIONS.items():
        aliases = f" aliases={','.join(data['aliases'])}" if data["aliases"] else ""
        print(f"{topic:<14} {data['description']}{aliases}")
    return 0


def cmd_suggest(args: argparse.Namespace) -> int:
    canonical_topic, data, payload = build_suggestions(args.topic)
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print(f"{canonical_topic}: {data['description']}")
    if data["aliases"]:
        print(f"aliases: {', '.join(data['aliases'])}")
    for icon in payload:
        print(f"{icon['variant']:7} {icon['name']:<32} {icon['path']}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    matches = search_icons(args.query, args.variant, args.limit)
    if args.json:
        payload = [
            {
                "variant": icon["variant"],
                "name": icon["name"],
                "path": str(icon["path"]),
                "aliases": icon["aliases"],
            }
            for icon in matches
        ]
        print(json.dumps(payload, indent=2))
        return 0

    for icon in matches:
        alias_suffix = f" aliases={','.join(icon['aliases'])}" if icon["aliases"] else ""
        print(f"{icon['variant']:7} {icon['name']:<32} {icon['path']}{alias_suffix}")
    return 0


def cmd_export_png(args: argparse.Namespace) -> int:
    _, resolved, svg_path = resolve_icon(args.icon, args.variant)
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "sips",
        "-Z",
        str(args.size),
        "-s",
        "format",
        "png",
        str(svg_path),
        "--out",
        str(output),
    ]
    subprocess.run(command, check=True)
    print(output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search and export bundled Tabler icons")
    subparsers = parser.add_subparsers(dest="command", required=True)

    topics_parser = subparsers.add_parser("topics", help="List curated presentation icon topics")
    topics_parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    topics_parser.set_defaults(func=cmd_topics)

    suggest_parser = subparsers.add_parser("suggest", help="Show a curated shortlist for one presentation topic")
    suggest_parser.add_argument("topic", help="Topic such as process, roadmap, analytics, people, or risk")
    suggest_parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    suggest_parser.set_defaults(func=cmd_suggest)

    search_parser = subparsers.add_parser("search", help="Search bundled icons by keyword")
    search_parser.add_argument("query", help="Keyword query, e.g. 'chart arrow'")
    search_parser.add_argument("--variant", choices=VARIANTS, help="Restrict search to one icon style")
    search_parser.add_argument("--limit", type=int, default=20, help="Maximum matches to print")
    search_parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    search_parser.set_defaults(func=cmd_search)

    export_parser = subparsers.add_parser("export-png", help="Export one icon to a PNG for deck insertion")
    export_parser.add_argument("icon", help="Canonical icon name or known alias")
    export_parser.add_argument("output", help="Output PNG path")
    export_parser.add_argument("--variant", choices=VARIANTS, help="Prefer one icon style")
    export_parser.add_argument("--size", type=int, default=512, help="Output size in pixels (max width/height)")
    export_parser.set_defaults(func=cmd_export_png)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Command failed with exit code {exc.returncode}: {' '.join(exc.cmd)}", file=sys.stderr)
        raise SystemExit(exc.returncode)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
