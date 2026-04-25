# PPTX production

Use this note when the user wants an editable `.pptx` deck.

## Core build path

1. choose either the component-native artifact-tool path, the legacy coded python-pptx path, or the explicit template-driven path
2. work from the approved deck.md
3. for fresh editable slides, default to the component-native artifact-tool path
4. for artifact-tool slides, run `python3 skill/scripts/build_pptx_artifact_tool.py OUTPUT_PPTX DECK_MD`
5. for legacy coded slides, run `python skill/scripts/build_pptx.py OUTPUT_PPTX DECK_MD [TEMPLATE_PPTX]`
6. for explicit template-driven slides, read `skill/references/template-catalog.md`, suggest the best template, then copy the selected one-slide template into the deck workspace and populate it with editable text, shapes, charts, icons, or tables
7. render the populated slide or deck to PNG
8. inspect the rendered PNG and adjust the PPTX until the slide reads cleanly
9. deliver only after the visual review loop passes
10. save the production round as an instance with raw renders, composed/edited renders, reviewed renders, method notes, manifest, and outputs

deck.md is the planning artifact. Do not invent a second planning schema.

Use the artifact-tool path as the default for new `ppt-shapes` decks. Use `assets/RLF_PPT_Template_v1.pptx` as the default base for legacy `python-pptx` coded slides unless the user asks for another base.

## Component-native artifact-tool loop

Use this path for fresh editable PowerPoint output.

Workflow:
1. Confirm the approved deck.md uses `mode: ppt-shapes` or `production_defaults.default_slide_mode: ppt-shapes`.
2. Prefer `production_defaults.ppt_shapes_engine: artifact-tool`; absence of the field also means artifact-tool for new builds.
3. Run `python3 skill/scripts/build_pptx_artifact_tool.py OUTPUT_PPTX DECK_MD`.
4. The builder creates an artifact-tool workspace under the active instance's `method/artifact-tool-workspace/`.
5. The builder maps deck.md slides into editable native components: title stacks, proof lists, process rows, matrices, section dividers, quotes, and chart layouts.
6. The builder exports a final PPTX, full-size slide PNG previews, layout exports, a build report, and a headless package quality report.
7. Inspect the PNG previews in `scratch/previews/` and repair the deck.md or component renderer if the slide does not prove the action title cleanly.

Rules:
- start from the slide job and evidence, not from a pre-existing template
- use native editable text, shapes, charts, and layout primitives
- use native charts when the relationship is chartable
- for tabular slides, add a table component, use the template-driven path, or make a targeted renderer extension before treating the slide as covered
- keep templates as optional structural references only
- do not use designer-mode assets, generated full-slide images, or PDF-only assembly on this path
- do not treat a successful PPTX export as sufficient; the rendered PNGs and package quality report must pass

For template-driven slides, the model must suggest a template before production.
The suggestion should include:
- template file
- slide job it supports
- why it fits the message
- any adaptation needed, such as fewer cards, renamed lanes, or a simplified diagram

Keep the template suggestion inside the deck.md so the user can approve the choice with the rest of the slide logic.
Create a new slide/deck from the selected template; do not overwrite the template itself.

## Template-driven `ppt-shapes` loop

Use this path when the user wants editable PowerPoint output that benefits from the template catalog.

Workflow:
1. Identify the slide job: cover, agenda, process, matrix, funnel, journey, dashboard, hierarchy, text blocks, or image cards.
2. Read `references/template-catalog.md` and pick one primary template plus, when useful, one fallback.
3. Add the selected template file and rationale to the deck.md.
4. After approval, duplicate the template into the deck workspace or output build path.
5. Replace placeholder text with the slide's actual message; do not carry over lorem ipsum or generic labels.
6. Preserve the useful structure, but change counts, labels, colors, icons, and object sizes when the content requires it.
7. Render the slide to PNG for review.
8. Inspect the PNG visually.
9. Fix the PPTX and re-render until the slide passes.

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

## Legacy coded render layer

When using the legacy python-pptx coded render layer:
1. start from `assets/RLF_PPT_Template_v1.pptx` unless the user asks for another base
2. run `python skill/scripts/build_pptx.py OUTPUT_PPTX DECK_MD [TEMPLATE_PPTX]`
3. let the script map supported `ppt-shapes` slides into the coded render layer
4. inspect the rendered output
5. make targeted follow-up edits only after visual review

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

## Current legacy coded archetypes

The legacy `python-pptx` render layer supports:
- takeaway
- agenda
- process
- matrix
- bar-column
- section-divider
- quote

Current mapping intent:
- `layout: takeaway + support` → `takeaway`
- `layout: agenda` → `agenda`
- `layout: horizontal process` or `process` → `process`
- `layout: matrix` → `matrix`
- `layout: bar-column` → `bar-column`
- `layout: section-divider` → `section-divider`
- `layout: quote` → `quote`

## Structural inspiration

Use these only as structural references, not as shipping template mixes:
- `assets/think-cell-selected/Text Box.potx`
- `assets/think-cell-selected/Process, Flow Chart, Phase.potx`
- `assets/think-cell-selected/Matrix, SWOT Analysis.potx`
- `assets/think-cell-selected/Agenda, Schedule, Timetable.potx`
- `assets/think-cell-selected/Dashboard, Statistic.potx`
- `assets/think-cell-selected/Bar, Column.potx`

Recreate the useful pattern inside the RLF template.
Prefer a small number of repeatable archetypes over one-off custom designs.

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
