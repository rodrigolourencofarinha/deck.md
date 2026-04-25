# deck.md

Currently in alpha.

`deck.md` is a Markdown format for writing presentation briefs that AI agents turn into slide decks. The human owns the logic: narrative structure, action titles, data, sources, and approval. The agent owns composition, visual treatment, slide production, and render review.

## How It Works

1. The human sends a briefing, source material, existing slides, assets, or a partial `deck.md`.
2. The agent drafts a complete `deck.md` with `status: draft`.
3. The human approves the brief or asks for changes.
4. Only after approval does the agent produce slides.
5. The agent renders the output, inspects it against the approved brief, and repairs anything that fails.

Post-render changes create a new review version, such as `review-01`, and regenerate only changed slides.

Default production is `designer-mode`. Use `ppt-shapes` when a slide needs precise editability, data-accurate charts, tables, or native PowerPoint structure. Pure `designer-mode` decks produce final PDFs, not PPTX wrappers, with OCR/searchable text added when tooling is available.

## Quick Start

Use [`deck.md`](./deck.md) or [`deck.minimal.md`](./deck.minimal.md) as the first file to copy. They contain the minimum useful surface:

- frontmatter with `status: draft`
- one narrative block
- a few slide headings with action titles
- the default footer and `designer-mode` production default

Use [`deck.full.md`](./deck.full.md) when you need designer assets, design tokens, revision briefs, advanced image controls, or richer production notes.

## Key Rules

- Every slide title must be an action title: a full sentence with a verb, sentence case, no trailing period.
- Body content must prove the title.
- Reading only the slide titles should reproduce the deck argument.
- Every visual-model input must be declared in `designer_assets` before approval.
- Every generated slide should carry the small `CR` mark and simple page number unless disabled in the approved brief.
- Every production round should use a new instance folder; do not overwrite raw images, method metadata, or reviewed slides.

## Files

| File | Purpose |
|---|---|
| [`deck.md`](./deck.md) | Quick-start starter brief |
| [`deck.minimal.md`](./deck.minimal.md) | Same minimal starter, kept explicit for packaging |
| [`deck.full.md`](./deck.full.md) | Rich starter with assets, revision brief, design tokens, and advanced controls |
| [`SPEC.md`](./SPEC.md) | Authoritative format specification |
| [`standards/`](./standards/) | Archetypes, validation, prompts, narrative templates, and artifact structure |
| [`examples/`](./examples/) | Worked SCR, pyramid, problem-solution, and update examples |
| [`skill/`](./skill/) | Installable `deck-architect` skill source |
| [`scripts/`](./scripts/) | Packaging and validation scripts |

## Skill Installation

The repo skill is self-contained under `skill/`: it uses `references/` and `scripts/` paths exactly as installed skills do. To install or refresh the Codex skill:

```bash
python3 scripts/package_skill.py --target ~/.codex/skills/deck-architect --force
```

To install or refresh the OpenClaw copy:

```bash
python3 scripts/package_skill.py --target ~/.openclaw/skills/deck-architect --force
```

The packager copies `skill/`, overlays the current root spec/templates/standards/examples into `skill/references/`, validates the result, and preserves an existing target `assets/` folder by default when this repo does not include large optional assets.

For a first install with a separate asset bundle, add `--with-assets /path/to/assets`.

Validate a skill tree without installing:

```bash
python3 scripts/validate_skill_install.py skill
```

Optional large assets live under `assets/` in installed skill copies when available. The skill can still plan decks and run basic editable rendering without them; template, icon, and visual-template workflows require those optional assets.

## Build Smoke Tests

From the repo root:

```bash
python3 scripts/smoke_builders.py
```

The smoke script reads `deck.minimal.md`, creates a temporary `ppt-shapes` copy, and runs both editable PPTX builders.

## License

[MIT](./LICENSE)
