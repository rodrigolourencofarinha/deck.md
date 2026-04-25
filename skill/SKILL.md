---
name: deck-architect
description: "Plan, critique, redesign, and produce slide decks from deck.md briefs. Use for consulting-style decks, executive reports, MBA/class decks, workshops, talk decks, designer-mode PDF output with gpt-image-2, editable ppt-shapes PPTX output with artifact-tool, and visual redesigns from user-supplied decks, templates, screenshots, logos, brand guides, icon packs, or reference assets."
---

# Deck Architect

Use this skill to turn messy material into a reviewable `deck.md`, get the human to approve it, and then produce slides from that approved brief.

## Core Contract

`deck.md` is the planning artifact and source of truth. Do not invent a parallel schema.

Hard rules:
- Draft or normalize a complete `deck.md` first.
- Keep `status: draft` until the human approves production.
- Do not build slides, generate images, assemble PDFs, or export PPTX files before approval.
- Default `production_defaults.default_slide_mode` to `designer-mode` unless the user asks for `ppt-shapes` or mixed/editable output.
- Declare every model input in `designer_assets` before approval; do not send or use undeclared files.
- Treat all logos, templates, old decks, screenshots, brand guides, icon packs, fonts, and reference images as external assets supplied by the user or declared by URL/path. This public skill has no bundled visual asset library.
- If the request includes data, CSV/Excel, SQL, metrics, benchmarks, or asks for analysis/rationale, complete the data-analysis workflow before drafting `deck.md`.
- Make the takeaway unmistakable on every slide. Use charts as proof, not decoration or a catalog of analysis cuts.
- For pure `designer-mode`, deliver PDF output only; add OCR/searchable text when available and report if OCR was not applied.
- Use the standard footer unless the approved brief disables it: small `CR` lower-left and simple page numbers (`1`, `2`, `3`) lower-right.
- Render and inspect the produced artifact before delivery; repair and rerender failed slides.
- For post-render changes, create a review `deck.md` version and regenerate only changed slides.
- Save meaningful specs and production rounds under the standard instance structure.

## Fast Workflow

1. Classify the request: outline, content plan, data-to-deck, critique, designer-mode PDF, editable PPTX, or mixed deck.
2. If data or SQL is involved, preserve inputs, create analysis/chart CSVs, write notes and a manifest, then reference them in `deck.md`.
3. Draft or update `deck.md` with the narrative, action titles, slide types, production defaults, declared assets, and analysis artifacts when relevant.
4. Send the full draft `deck.md` to the human for approval.
5. After approval, validate the brief, prepare declared assets, validate data refs, and produce only in the approved mode.
6. Render, inspect, repair, and save the output in a production instance.
7. For review changes, fork from the previous approved brief, add `## Revision Brief`, and reuse unchanged slides.

If the build is simple, keep the workflow simple. Do not create extra planning files unless they materially help review or production.

## Reference Router

Read only the files needed for the task:

- `references/SPEC.md` - authoritative `deck.md` schema, defaults, precedence, and output rules.
- `references/deck.md` - quick-start starter brief.
- `references/deck.full.md` - rich starter with assets, revision brief, design tokens, and advanced designer-mode controls.
- `references/standards/deck-validation.md` - hard validation rules and self-check checklist.
- `references/standards/data-analysis-workflow.md` - SQL/CSV/spreadsheet analysis preflight, artifact layout, manifest schema, and chart economy rules.
- `references/standards/slide-archetypes.md` - valid slide `type` values and preferred production modes.
- `references/standards/narrative-templates.md` - SCR, pyramid, problem-solution, and update templates.
- `references/standards/artifact-structure.md` - specs, assets, instances, image folders, method files, manifests, and outputs.
- `references/standards/image-prompts.md` - designer-mode prompt rules and image-generation defaults.
- `references/deck-workflow.md` - deck-level storyline and consulting narrative rules.
- `references/consulting-slide-standards.md` - action-title, proof, source, and pre-flight standards.
- `references/single-slide-workflow.md` - one-slide build or critique sequence.
- `references/designer-mode-workflow.md` - designer-mode production and review loop.
- `references/designer-mode-gpt-image-prompt-scaffold.md` - convert an approved slide block into a `gpt-image-2` prompt.
- `references/designer-mode-direct-api-pattern.md` - direct OpenAI Image API fallback, only after Codex path failure and human approval.
- `references/pptx-production.md` - editable PPTX production with artifact-tool.

## Production Modes

Use `designer-mode` for premium visual slides and image-backed explanatory pages. Generate slide by slide with `gpt-image-2` through Codex OAuth/Codex image tooling first. Use direct API-key generation only after that path fails and the human approves the fallback.

Use `ppt-shapes` for editable analytical slides, precise charts, tables, process flows, matrices, and decks where the user needs a PowerPoint-native file. Prefer:

```bash
python scripts/build_pptx_artifact_tool.py OUTPUT.pptx APPROVED_DECK.md
```

This is the public editable-PPTX path. It creates an isolated artifact-tool workspace with `src/`, `scratch/`, and `output/`; uses editable presentation primitives; exports PPTX, PNG previews, layout JSON, and a quality report; and prepares only assets declared in the approved brief.

Use `mixed` only when specific slides need different modes. Set `mode:` explicitly per slide.

## External Asset Contract

The installable skill is intentionally asset-neutral. Do not assume any bundled templates, logo sets, icon packs, deck examples, fonts, or brand materials exist inside the skill.

When the user provides assets, add them to `designer_assets` before approval. Supported generic types include `logo`, `ppt-template`, `existing-deck`, `slide-preview`, `brand-guide`, `reference-image`, `screenshot`, `icon-pack`, `font`, and `other`.

For `designer-mode`, prepare declared non-image assets into model-readable inputs and record them in `method/model-inputs.yaml`.

For `ppt-shapes`, pass declared local assets through the artifact-tool workspace under `scratch/assets/` and record them in `scratch/external-assets.json`. Use them only when referenced by `scope: deck` or slide-level `asset_refs`.

If an approved deck marks an asset as `required: true` and it cannot be found or prepared, stop and report the missing asset. Optional missing assets should not block storyline planning or validation.

## Validation Before Delivery

Before delivering, check:
- the current `deck.md` is approved
- data-driven decks have `analysis_artifacts`, local chart CSVs, notes/manifest, and clear caveats
- narrative template and slide types are valid
- slide titles are action titles and the title sequence tells the argument
- each slide has one consulting takeaway and any chart directly proves it
- quantitative claims have sources
- all `asset_refs` resolve to declared `designer_assets`
- prepared model inputs are recorded in `method/model-inputs.yaml` when designer assets are used
- output has been rendered and inspected for text accuracy, overlap, clipping, logo placement, safe margins, and footer
- production artifacts are stored in the instance structure
- review changes use a new review spec and regenerate only changed slides

Full validation lives in `references/standards/deck-validation.md`.
