# deck.md

Currently in alpha.

`deck.md` is a Markdown format for writing presentation briefs that AI agents turn into slide decks. The human owns the logic: narrative structure, action titles, data, sources, and approval. The agent owns composition, visual treatment, slide production, and render review.

This repo also ships `deck-architect`, a public skill for OpenAI/Codex-style agents that can load a local skill folder with `SKILL.md`, `references/`, and `scripts/`.

## How It Works

1. The human sends a briefing, source material, existing slides, assets, or a partial `deck.md`.
2. If the request includes data, SQL, CSV/Excel, metrics, or asks for analysis/rationale, the agent first creates traceable analysis artifacts: source data, SQL/query notes, derived CSVs, interpretation notes, and a manifest.
3. The agent drafts a complete `deck.md` with `status: draft`, clear consulting takeaways, and data/chart references when relevant.
4. The human approves the brief or asks for changes.
5. Only after approval does the agent produce slides.
6. The agent renders the output, inspects it against the approved brief, and repairs anything that fails.

Post-render changes create a new review version, such as `review-01`, and regenerate only changed slides.

Default production is `designer-mode`. Use `ppt-shapes` when a slide needs precise editability, data-accurate charts, tables, or native PowerPoint structure. Pure `designer-mode` decks produce final PDFs, not PPTX wrappers, with OCR/searchable text added when tooling is available.

For data-driven decks, the skill is intentionally consulting-first: it should reduce the analysis to a storyline, not turn every table into a chart. Every slide needs one clear takeaway; charts are proof for that takeaway.

## Requirements

Minimum requirements:
- An OpenAI/Codex-style agent, or another agent that can read and follow the local `skill/SKILL.md` instructions plus files in `skill/references/`.
- Python 3.10+ for packaging, validation, and helper scripts.
- `PyYAML` available to Python for parsing `deck.md` frontmatter and slide YAML blocks.

For editable PowerPoint output with `ppt-shapes`:
- The OpenAI/Codex Presentations runtime must be installed and available locally.
- The runtime must include `@oai/artifact-tool` and the Presentations helper scripts used to create the isolated presentation workspace.
- Run `python3 scripts/smoke_builders.py` after installation to confirm PPTX export, PNG previews, layout JSON, and the quality report work on the machine.

For `designer-mode` image output:
- Access to `gpt-image-2` through Codex OAuth/Codex image tooling is the default path.
- Direct OpenAI API-key image generation is only a fallback after the Codex-authenticated path fails and the human approves the fallback.
- OCR/searchable PDF output depends on local PDF/OCR tooling being available.

Asset requirements:
- The public skill includes no bundled logos, templates, icon packs, fonts, decks, or visual references.
- Any logo, template, old deck, screenshot, brand guide, icon pack, font, or reference image must be supplied externally and declared in `designer_assets` before approval.

## Working With Different Agents

This skill is written for OpenAI/Codex-style local agents, but the format is portable. Other agents can use it if they can read the same files and provide equivalent model/tool capabilities.

For a Codex/OpenAI local-skill agent:
- Install the packaged skill into the agent's skill folder.
- Let the agent load `SKILL.md`; it will route itself to the needed `references/` files.
- Use Codex OAuth image tooling for `designer-mode` when available.
- Use the bundled Presentations runtime for editable `ppt-shapes` PPTX output.

For Claude or Claude Code:
- Install the skill as a Claude skill, for example under `~/.claude/skills/deck-architect/` for personal use or `.claude/skills/deck-architect/` inside a project.
- Claude Code can read the repo, edit files, run commands, and invoke skills, so it can draft `deck.md`, validate it, run packaging scripts, and run smoke tests.
- Claude can read and analyze images, so it can inspect supplied logos, screenshots, slide previews, and rendered PNGs when the Claude surface has image input enabled.
- Claude does not produce image files by itself. For `designer-mode`, pair Claude with an external image generator: OpenAI Images with `OPENAI_API_KEY`, Codex image tooling, or another model that can generate full-slide 16:9 PNGs with accurate text.
- If using OpenAI Images with Claude, set `OPENAI_API_KEY` in the shell environment that Claude Code can access, then ask Claude to use `skill/references/designer-mode-direct-api-pattern.md` as the fallback API pattern.
- If using another image model, adapt `skill/references/designer-mode-gpt-image-prompt-scaffold.md` to that model's API while preserving exact `required_text`, declared asset inputs, footer rules, and render review.
- For editable `ppt-shapes`, Claude still needs a local PPTX renderer. Use this repo's artifact-tool path only if the OpenAI/Codex Presentations runtime is installed; otherwise replace `skill/scripts/build_pptx_artifact_tool.py` with an equivalent renderer Claude can run.

For an OpenAI API-key agent:
- Set `OPENAI_API_KEY` in that agent's environment.
- Use an OpenAI image model capable of generating or editing full-slide 16:9 PNGs for `designer-mode`.
- Map `image_generation.model`, `size`, `quality`, and `output_format` from `deck.md` into the agent's image-generation call.
- Save prompts, model settings, input assets, and outputs under the standard `method/` and `images/` folders.
- Keep `ppt-shapes` on the artifact-tool path only if the agent also has the Presentations runtime; otherwise use `designer-mode` or provide a different editable-PPTX renderer.

For a non-OpenAI model or agent:
- Use a model that can reliably create presentation-slide images with exact text, supplied reference images, and 16:9 output.
- Adapt `skill/references/designer-mode-gpt-image-prompt-scaffold.md` to that model's prompt and image-input API.
- Preserve the same contract: no undeclared assets, exact `required_text`, standard footer, rendered review before delivery, and a new review `deck.md` for post-render changes.
- If the model cannot render accurate text, use it only for visuals and place text with an editable renderer outside the model.
- If the agent cannot use `@oai/artifact-tool`, `ppt-shapes` is not available unless you replace `skill/scripts/build_pptx_artifact_tool.py` with an equivalent PPTX-native renderer.

For any agent:
- Start with a complete `deck.md` and keep `status: draft` until the human approves production.
- For data-driven requests, create the analysis artifacts before drafting the final `deck.md`: `data/source/`, `data/analysis/`, `data/charts/`, `analysis/queries/`, `analysis/notes.md`, and `analysis/manifest.yaml`.
- Do not generate slides from chat history alone; `deck.md` is the production contract.
- Declare every external asset in `designer_assets` before production.
- Keep charts selective: use the minimum evidence that proves the action title.
- Run the validation and smoke commands before trusting a new install.

## Quick Start

Use [`deck.md`](./deck.md) or [`deck.minimal.md`](./deck.minimal.md) as the first file to copy. They contain the minimum useful surface:

- frontmatter with `status: draft`
- one narrative block
- a few slide headings with action titles
- the default footer and `designer-mode` production default

Use [`deck.full.md`](./deck.full.md) when you need designer assets, design tokens, revision briefs, advanced image controls, or richer production notes.

For data-backed decks, follow [`standards/data-analysis-workflow.md`](./standards/data-analysis-workflow.md) before approving `deck.md`. The deck should link to a manifest, notes, queries, and chart-ready CSVs through `analysis_artifacts`.

## Key Rules

- Every slide title must be an action title: a full sentence with a verb, sentence case, no trailing period.
- Body content must prove the title.
- Reading only the slide titles should reproduce the deck argument.
- Data analysis must become a clear argument, not a pile of charts.
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
| [`examples/`](./examples/) | Worked SCR, pyramid, problem-solution, update, and data-driven examples |
| [`skill/`](./skill/) | Installable `deck-architect` skill source |
| [`scripts/`](./scripts/) | Packaging and validation scripts |

## Skill Installation

The repo skill is self-contained under `skill/`: it uses `references/` and `scripts/` paths exactly as installed skills do. To install or refresh the skill for a local OpenAI/Codex agent:

```bash
python3 scripts/package_skill.py --target ~/.codex/skills/deck-architect --force
```

Optional: to install or refresh an OpenClaw copy that follows the same skill-folder layout:

```bash
python3 scripts/package_skill.py --target ~/.openclaw/skills/deck-architect --force
```

The packager copies `skill/`, overlays the current root spec/templates/standards/examples into `skill/references/`, validates the result, and writes a clean asset-neutral skill tree.
The public skill package intentionally contains no bundled visual assets. Logos, templates, old decks, screenshots, icon packs, brand guides, fonts, and reference images are supplied at deck-production time through external paths or URLs declared in `designer_assets`.

Validate a skill tree without installing:

```bash
python3 scripts/validate_skill_install.py skill
```

Validate data artifacts referenced by a draft or approved deck:

```bash
python3 skill/scripts/validate_deck_data.py deck.md
```

Do not install private asset folders into the skill. Keep source assets next to the deck project, then declare them in the approved `deck.md`.

## Build Smoke Tests

From the repo root:

```bash
python3 scripts/smoke_builders.py
```

The smoke script reads `deck.minimal.md`, creates a temporary `ppt-shapes` copy, and runs the artifact-tool editable PPTX builder. It verifies the PPTX, PNG previews, layout JSON, and quality report.

External asset handling can be smoke-tested with:

```bash
python3 scripts/smoke_external_assets.py
```

Data-to-deck validation can be smoke-tested with:

```bash
python3 scripts/smoke_data_analysis.py
```

## License

[MIT](./LICENSE)
