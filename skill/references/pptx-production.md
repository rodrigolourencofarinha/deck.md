# PPTX production

Use this note when the user wants an editable `.pptx` deck.

## Core build path

1. choose the component-native artifact-tool path
2. work from the approved deck.md
3. for fresh editable slides, start from slide job, action title, evidence, and native components
4. run `python3 scripts/build_pptx_artifact_tool.py OUTPUT_PPTX DECK_MD`
5. render the populated slide or deck to PNG
6. inspect the rendered PNG and adjust the deck.md or renderer until the slide reads cleanly
7. deliver only after the visual review loop passes
8. save the production round as an instance with raw renders, composed/edited renders, reviewed renders, method notes, manifest, and outputs

deck.md is the planning artifact. Do not invent a second planning schema.

The public skill ships no bundled templates, icons, logos, fonts, or brand materials. Use only external assets declared in the approved `designer_assets` block.

## Component-native artifact-tool loop

Use this path for fresh editable PowerPoint output.

Workflow:
1. Confirm the approved deck.md uses `mode: ppt-shapes` or `production_defaults.default_slide_mode: ppt-shapes`.
2. Run `python3 scripts/build_pptx_artifact_tool.py OUTPUT_PPTX DECK_MD`.
3. The builder creates an artifact-tool workspace under the active instance's `method/artifact-tool-workspace/`.
4. The workspace has `src/`, `scratch/`, and `output/` folders.
5. The builder maps deck.md slides into editable native primitives: `text`, `grid`, `row`, `column`, `shape`, `chart`, `table` where supported, `image`, and `rule`.
6. Declared local assets are copied into `scratch/assets/` and recorded in `scratch/external-assets.json`; undeclared assets are ignored.
7. The builder exports a final PPTX, full-size slide PNG previews, layout exports, a build report, and a headless package quality report.
8. Inspect the PNG previews in `scratch/previews/` and repair the deck.md or component renderer if the slide does not prove the action title cleanly.

Rules:
- start from the slide job and evidence, not from a pre-existing template
- use native editable text, shapes, charts, and layout primitives
- use native charts when the relationship is chartable
- for tabular slides, add or extend a native table component before treating the slide as covered
- keep externally supplied templates as optional structural references only
- do not use designer-mode assets, generated full-slide images, or PDF-only assembly on this path
- do not treat a successful PPTX export as sufficient; the rendered PNGs and package quality report must pass

For externally supplied template references, the model must describe the intended use before production:
- declared asset id
- slide job it supports
- why it fits the message
- what to borrow, such as margins, density, typography, or object rhythm
- what not to copy, such as placeholder text, outdated labels, or irrelevant objects

Visual QA checklist:
- no clipped or missing text
- standard footer appears on every slide unless disabled: `CR` lower-left and simple page number lower-right, never `1/3`
- no awkward line breaks in titles, labels, or cards
- no text boxes overflowing their shapes
- no labels colliding with arrows, icons, chart marks, or other labels
- font size is large enough to read in presentation mode
- title hierarchy is clear and the action title remains dominant
- body has one primary reading path, not a scattered collage
- spacing and alignment look intentional
- source/footer text, if present, stays separate from the slide body
- template structure still fits the content after adaptation

Fix order:
1. shorten text and make labels more precise
2. reduce the number of blocks/cards/labels
3. resize or move objects to restore whitespace
4. adjust font size only within readable limits
5. split the slide if the message is too dense
6. switch to a better template if the structure is fighting the content

The PPTX file existing is not enough.
The rendered PNG must look correct.

## Output hygiene

When saving deck artifacts, prefer:
- `decks/<deck-slug>/instances/<###-round>/images/raw/` for direct PowerPoint or render outputs before edits
- `decks/<deck-slug>/instances/<###-round>/images/composed/` for edited or composited slide images
- `decks/<deck-slug>/instances/<###-round>/images/reviewed/` for accepted render PNGs
- `decks/<deck-slug>/instances/<###-round>/method/` for template choices, render notes, manipulation logs, and review notes
- `decks/<deck-slug>/instances/<###-round>/outputs/` for the PPTX/PDF assembled from that instance
- `decks/<deck-slug>/outputs/final/` for final human-facing PPTX/PDF
- `decks/<deck-slug>/outputs/review/` for review contact sheets or PDFs
- `decks/<deck-slug>/assets/source/` for source material
- `decks/<deck-slug>/assets/prepared/` for prepared reference assets

Avoid leaving behind:
- duplicate export trees with unclear status
- `prepared-*` resized variants as if they were source assets
- ad hoc output folders that encode versioning only in folder names

## Current artifact-tool archetypes

The component-native artifact-tool renderer currently supports:
- takeaway
- agenda
- process
- matrix
- chart
- section-divider
- quote

This path is intended to grow by adding reusable native components, not by adding more required template files.

## Layout rules

- do not add closing bars by default
- treat `closing` as optional emphasis, not a required field
- use `closing` mainly for synthesis, recommendation, quote, or section-closing slides
- if the title already states the takeaway clearly, prefer omitting `closing`
- avoid repeated bottom closing bars on adjacent slides
- keep process cards and agenda sections concise enough to scan quickly
- if card text becomes paragraph-like, shorten it or split the slide
- keep subtitles only when they add framing beyond the title
- keep footer and source elements visually separate from any closing bar
- keep the standard `CR` mark and page number small, muted, and consistent across slides

## Render standard

Prefer this review order:
1. Microsoft PowerPoint render/export
2. PowerPoint-rendered PNG slide exports for visual review
3. PowerPoint-exported PDF as a backup artifact

Treat PowerPoint-rendered output as the source of truth for layout fidelity whenever PowerPoint is available.

If PowerPoint export is unavailable, use another renderer only as a fallback and mark it clearly as non-canonical.

## Review rule

When layout quality matters, trust the rendered PNG slides over the raw slide structure.
The deck is not done just because the PPTX file exists.

If a visual asset was meant to be a native 16:9 slide image, do not repair it by cropping just to make the PPTX look filled.
Regenerate the asset or improve the prompt instead.
