---
name: deck-architect
description: "Design and build slide decks including consulting-style decks, executive reports, MBA/class presentations, workshops, and talk decks. Use when the agent needs to create, revise, structure, critique, or translate a slide-based narrative; choose the material type and audience; draft the storyline before production; generate editable decks with python-pptx; decide between clean analytical slides and more elaborate image-driven framework slides; use designer-mode visual template references; or use bundled Tabler icons for process flows, roadmaps, comparison cards, callouts, and other slide-native visual framing."
---

# Deck Architect

## Overview

Use this skill to think clearly before building decks.
Prioritize audience, decision, storyline, evidence, and reading flow before visual polish.

Use this skill for:
- deck structuring and storyline design
- slide critique and redesign
- converting rough ideas into presentation logic
- building editable `.pptx` decks
- producing premium designer-mode slides with GPT Image 2
- using bundled Tabler icons for clean analytical slides

For editable deck output, prefer `assets/RLF_PPT_Template_v1.pptx` as the default base.
For visual QA, prefer Microsoft PowerPoint renders when available.

## Core rule

**`deck.md` is the canonical planning artifact.**

Hard rules:
- use the `deck.md` format defined in `SPEC.md` for all deck planning
- do not invent a parallel planning schema
- do not begin production until the user has approved the current deck.md (set `status: approved`)
- default `production_defaults.default_slide_mode` to `designer-mode` unless the user explicitly asks for another mode
- record any user-provided designer-mode templates, logos, brand guides, screenshots, or visual references in `designer_assets`
- after producing any output, render and inspect it against the approved deck.md, original briefing, and any Revision Brief; repair and rerender until it passes
- when the user requests post-render changes, create a new review deck.md version and regenerate only changed slides
- for pure designer-mode decks, produce final PDF only; do not create a PPTX wrapper
- add OCR/searchable text to designer-mode PDFs when tooling is available, and report clearly if OCR could not be applied
- include the standard small footer on every generated slide unless the approved deck.md disables it: `CR` lower-left and simple page numbers (`1`, `2`, `3`, ...) lower-right, never `1/3` or `1 of 3`
- save meaningful deck.md versions under `decks/<deck-slug>/specs/`

## Assets and tools

### Core assets
- `assets/RLF_PPT_Template_v1.pptx` — default editable deck base
- `assets/templates_full.pptx` — source deck for the editable template library
- `assets/templates/` — one-slide editable PPTX templates extracted from `templates_full.pptx`
- `assets/visual-templates/` — designer-mode PNG references; use `default-slide.png` when the user says "use my default template" and `title-page.png` for designer-mode covers
- `assets/tabler-icons/outline/`
- `assets/tabler-icons/filled/`
- `assets/tabler-icons/aliases.json`

### Icon workflow
Use Tabler as the default icon set for clean analytical slides, process flows, roadmaps, comparison cards, status markers, and callouts.

Useful commands (from repo root):
- `python skill/scripts/tabler_icons.py topics`
- `python skill/scripts/tabler_icons.py suggest roadmap`
- `python skill/scripts/tabler_icons.py search "chart arrow"`
- `python skill/scripts/tabler_icons.py export-png chart-bar tmp/chart-bar.png --size 512`

Rules:
- prefer `outline` by default
- use `filled` only for stronger emphasis or tiny badges
- export PNG before placing icons in PPT; `python-pptx` is not reliable with these SVGs

## Which reference to read

Read only what the task needs.

### Format (always available at repo root)
- `SPEC.md` — authoritative deck.md format specification
- `standards/narrative-templates.md` — SCR, pyramid, problem-solution, update template reference
- `standards/slide-archetypes.md` — valid slide `type` values and preferred modes
- `standards/deck-validation.md` — hard rules the agent self-checks before emitting
- `standards/image-prompts.md` — gpt-image-2 prompt templates and token injection

### Deck logic
- `skill/references/deck-workflow.md` — deck-level workflow, density, archetypes, and consulting-style storyline rules
- `skill/references/consulting-slide-standards.md` — consulting-grade action-title, body-as-proof, source/footer, and pre-flight standards

### Slide building and critique
- `skill/references/single-slide-workflow.md` — build order, chart cleanup, and visual standards for one slide
- `skill/references/consulting-slide-standards.md` — use when the slide needs McKinsey/BCG/Bain-style discipline

### PPT shapes / editable deck output
- `skill/references/pptx-production.md` — coded render layer, template-driven `ppt-shapes` workflow, and render standard
- `skill/references/template-catalog.md` — catalog of one-slide editable PPTX templates by title, category, and best use
- `skill/scripts/build_pptx.py` — renders supported `ppt-shapes` slides from a deck.md
- `skill/scripts/split_template_deck.py` — regenerates `assets/templates/` and `skill/references/template-catalog.md` from `assets/templates_full.pptx`

### Designer mode
- `skill/references/designer-mode-workflow.md` — designer-mode workflow, visual branches, image decisions, and iteration loop
- `skill/references/designer-mode-gpt-image-prompt-scaffold.md` — convert one deck.md slide into a GPT Image 2 prompt
- `skill/references/designer-mode-direct-api-pattern.md` — default direct GPT Image 2 API pattern for native 16:9 full-slide generation

### Rendering and icons
- `skill/references/tabler-icon-selection.md` — shortlist/safe icon choice guidance

## Production branches

Choose one branch before producing slides.

### 1. Clean analytical
Use for most teaching, consulting, and executive slides.

Characteristics:
- white or very light background
- strong typography and whitespace
- restrained frameworks and emphasis
- charts, matrices, agendas, process flows, text-led synthesis
- images only when they materially help
- simple composition with one clear message, not a dashboard collage
- minimal on-slide text; prefer short labels, crisp titles, and a few support points

### 2. Elaborated framework
Use when the slide benefits from a more crafted visual framework.

Characteristics:
- premium consulting style
- stronger central structure or hero visual
- labels/callouts around the visual
- useful for opening concepts, frameworks, strategic synthesis

### 3. Visual redesign
Use when transforming an existing slide without losing its core logic.

Characteristics:
- preserve original message and key content blocks
- redesign composition, not just spacing
- increase occupancy and visual presence
- integrate visuals only when they improve explanation

### 4. Designer mode
Use when the user wants a more art-directed workflow with explicit separation between content design, slide architecture, and generated visual.

Characteristics:
- spec first, image second
- visuals remain subordinate to slide logic
- design language must stay consistent across the deck

## Canonical workflow

### 1. Build the deck.md

The user may arrive with:
1. raw source material
2. a broad deck idea
3. a mostly formatted structure or partial deck.md

In all three cases:
- normalize into a `deck.md` following the format in `SPEC.md`
- set `production_defaults.default_slide_mode: designer-mode` unless the user explicitly asks for `ppt-shapes` or a mixed/editable build
- for cases 1 and 2, generate the deck.md with `status: draft` and populate `## Brief` with what was provided and what was inferred — see `SPEC.md` for the `## Brief` schema
- send the complete draft deck.md to the user before producing any slides
- do not jump into production while structure is still unclear
- make the action-title sequence readable as the deck's argument before producing slide bodies
- choose the right `narrative_template`: `scr`, `pyramid`, `problem-solution`, or `update`

### 2. Use deck.md as the source of truth

The deck.md should carry:
- deck metadata and design tokens (frontmatter)
- footer defaults for the standard `CR` mark and simple numeric page numbers
- designer-mode asset references (`designer_assets`) for templates, logos, brand guides, screenshots, or other visual inputs
- narrative spine (`## Narrative` block)
- revision intent (`## Revision Brief`) when changing a previously approved/rendered deck
- per-slide intent (`## Slides` — action titles, `type`, `layout`, `mode`)
- image decisions and creative direction where relevant
- production notes (`## Notes to the agent`)

Mode nuance:
- `ppt-shapes`: tighter, more structural, easier to route into the coded render layer
- `designer-mode`: clearer art direction, but still anchored in the same spec

### 3. Mandatory approval gate

The human approval loop is required:
1. human sends briefing, source material, or partial deck.md
2. agent drafts a complete deck.md with `status: draft`
3. agent sends that deck.md to the human for validation
4. human approves or requests changes
5. agent revises and resends deck.md until the human approves
6. only then does production begin

Do not:
- build slides
- generate slide visuals
- assemble the deck
- export PPTX/PDF

until `status: approved` is set in the deck.md frontmatter.

When the deck.md is agent-generated (from a broad idea or raw content), the user MUST review `## Brief` and all slide titles before approving. Draft renders do not replace this approval gate.

### 4. Choose production mode

Modes: `ppt-shapes` | `designer-mode` | `mixed`

The `production_defaults.default_slide_mode` in the deck.md frontmatter sets the deck default. Individual slides override with `mode:` in their YAML block. Each archetype in `standards/slide-archetypes.md` declares a `preferred_mode` as a starting point.

If the user has not chosen, use `designer-mode` as the default. Override individual chart, table, and heavily editable analytical slides to `mode: ppt-shapes` when that will produce clearer or more maintainable output.

### 5. Produce in the chosen mode

#### `ppt-shapes`
Use editable PPTX structures.

Rules:
- build through the coded `python-pptx` render layer driven by the deck.md
- when a user asks for template-driven output, read `skill/references/template-catalog.md` first and choose a one-slide template from `assets/templates/` by slide job
- treat template files as editable structural references; adapt the message, title, chart/table content, and visual hierarchy
- suggest the selected template for each `ppt-shapes` slide and give a short reason before building
- after creating a populated PPTX slide, render it to PNG and inspect the image for wrapping, clipped text, tiny fonts, overlaps, alignment, and density before delivery
- if the render has problems, revise the slide and re-render until it reads cleanly
- prefer editable shapes, text, icons, and charts
- use Tabler icons when a small pictogram, connector, or status cue helps
- after rendering, inspect the slide/deck image for match to briefing, overlaps, clipping, logo placement, text readability, and visual hierarchy; fix and rerender until clean

#### `designer-mode`
Use GPT Image 2 as the default production engine for the slide visual output.

Rules:
- do not generate before the deck.md is approved
- generate slide by slide, not all at once
- use only designer assets declared in `designer_assets` or explicitly supplied in the current turn
- when a slide references `asset_refs`, load and prepare those assets before prompt construction
- render non-image assets such as `.pptx` templates into image previews before using them as model references
- if a required logo/template/brand asset cannot be found or prepared, stop and report the missing asset
- assemble pure designer-mode decks as PDF only, plus optional review PNGs; do not generate a PPTX version
- add an OCR/searchable text layer to the final PDF when tooling is available
- add the standard footer to every slide image: `CR` lower-left and the simple slide-order page number lower-right, unless disabled in the approved deck.md; do not include total-count numbering such as `1/3`
- allow creative freedom only after the slide logic is locked
- default to GPT Image 2 end-to-end slide generation for designer mode unless the user explicitly asks for a hybrid workflow
- enforce `aspect_ratio: 16:9` in both the deck.md and the image-generation call
- prefer native 16:9 generation with `size="2560x1440"` as the default full-slide resolution
- use `quality="high"` for final designer-mode slides
- use `quality="medium"` only for layout or mood previews, and `quality="low"` only for fast exploration
- use `output_format="png"` and `n=1` for final slides
- treat the slide as a real presentation slide, not a loose poster or background image
- require a visible slide structure: title zone, key-message zone, and main visual body in a fast left-to-right / Z-reading flow
- put literal slide text in `required_text` — see `SPEC.md` for the required_text schema
- append computed footer text to the designer-mode prompt's allowed text list so page numbers and `CR` do not violate the text lock
- explicitly prohibit extra invented text, watermarks, logos, decorative captions, and unrequested labels
- use `skill/references/designer-mode-gpt-image-prompt-scaffold.md` to convert the deck.md slide block into the image prompt
- after generation, render/inspect the slide or PDF against the approved deck.md and briefing; check logo placement, asset usage, text accuracy, overlaps, clipping, safe areas, and whether the slide still lands the intended message
- if a generated slide fails inspection, regenerate only that slide with the prior image/prompt plus the specific defect to fix

#### `mixed`
Use when some slides should stay editable and others benefit from designer-mode visuals.

Rules:
- use `mode:` explicitly per slide in the deck.md YAML block
- do not invent mode decisions late in the process
- produce PPTX only when the editable `ppt-shapes` portion matters or the user explicitly asks for a mixed editable file; designer-mode slides remain raster content inside any mixed artifact
- render and inspect the whole assembled artifact so editable and raster slides work together visually

### 6. Save history and outputs

Save deck work under a tight standard structure:
- `decks/<deck-slug>/specs/` — versioned deck.md files
- `decks/<deck-slug>/outputs/final/`
- optional: `decks/<deck-slug>/outputs/review/`
- optional: `decks/<deck-slug>/assets/source/`
- optional: `decks/<deck-slug>/assets/generated/`
- optional: `decks/<deck-slug>/work/` only for durable helper scripts

Preferred filenames:
- `decks/<deck-slug>/specs/YYYY-MM-DD-v01-deck.md`
- `decks/<deck-slug>/specs/YYYY-MM-DD-v02-deck.md`
- `decks/<deck-slug>/specs/YYYY-MM-DD-review-01-deck.md`
- `decks/<deck-slug>/specs/YYYY-MM-DD-review-02-deck.md`
- `decks/<deck-slug>/outputs/final/YYYY-MM-DD-v02-deck.pdf` — required final deliverable for designer-mode decks
- `decks/<deck-slug>/outputs/final/YYYY-MM-DD-v02-deck.pptx` — only for `ppt-shapes` or explicitly requested mixed/editable decks
- `decks/<deck-slug>/outputs/review/YYYY-MM-DD-v02-slide-01.png`

Rules:
- save meaningful revisions, not every trivial wording tweak
- use review filenames for post-render human change requests
- keep the latest approved deck.md easy to find
- keep earlier major versions when structure changes materially
- do not scatter duplicate export trees unless there is a clear operational reason
- do not persist scratch crops, temporary resized variants, or throwaway assembly files

### 7. Render review and repair

After producing slides, always render the artifact before delivery.

Inspect:
- slide/page count and order
- match to the approved deck.md and original briefing
- title, required text, labels, and body text accuracy
- logo and designer asset placement, especially overlap and safe margins
- clipping, unreadable text, poor contrast, broken reading path, and visual clutter
- whether each slide still proves its action title

If anything fails:
- if the spec is wrong, patch deck.md first
- if the generated/built output is wrong, regenerate or rebuild only the affected slide
- render and inspect again before delivery

### 8. Post-render human changes

When the human says the rendered deck is basically okay but asks for a change:
- start from the previous approved deck.md and the human's new change request
- create a new review version such as `YYYY-MM-DD-review-01-deck.md`
- add `## Revision Brief` with the previous deck path, review round, change request, changed slides, unchanged slides, and regeneration scope
- patch only the affected slide specs and any deck-level fields required by the change
- pass the old slide spec, old rendered slide image or prompt when available, updated slide spec, and exact human change request to the image model
- ask the model to change only the requested elements and preserve everything else that still matches the approved spec
- regenerate only changed slides, then assemble, render, and inspect the full artifact

### 9. Keep the user informed

Especially in designer mode, use concise progress updates such as:
- "Slide 1 generated. Going to the next."
- "Slide 3 failed logo overlap review; regenerating only that slide."

## Fast operating sequence

1. Classify the request.
2. Draft the storyline.
3. Create the deck.md (or refine the existing one) with `status: draft` and designer-mode as the default production mode.
4. Save the current version under `decks/<deck-slug>/specs/`.
5. Send the deck.md to the user for validation.
6. Revise and resend until the user approves it (`status: approved`).
7. Produce slides in the approved mode; for pure designer-mode, assemble the final OCRed PDF only.
8. Render and inspect the output against the deck.md, briefing, and asset rules.
9. Repair and rerender any failed slides.
10. Save outputs under `decks/<deck-slug>/outputs/`.
11. Review against visual standards.

If the build is simple, keep the workflow simple.
Do not create extra planning files unless they materially help.

## deck.md per-slide schema

Each slide in a deck.md is a `### Slide N — "Action title"` heading followed by a YAML block and markdown body. The full field reference is in `SPEC.md`. Key fields:

```yaml
id: <integer or stable string>
type: <archetype — see standards/slide-archetypes.md>
layout: "<layout hint>"
mode: "<ppt-shapes|designer-mode>"      # overrides deck default
image_decision: "<none|icon-only|cutout|full-generated-visual>"
asset_refs: ["<designer_assets.id>"]      # optional; slide-specific designer-mode assets
```

Optional per-slide fenced blocks:

```yaml
chart:
  type: <chart type>
  emphasis: "<echoes the action title>"
  data_ref: <path>
  annotation: "<key insight>"
```

```yaml
creative_direction:
  mood: "<one or two words>"
  metaphor: "<the visual idea>"
  composition_intent: "<how to compose the slide>"
  prompt_notes:
    - "<specific guidance for gpt-image-2>"
  avoid:
    - "<anti-patterns>"
```

```yaml
required_text:
  title: "<exact title as it should appear in the image>"
  labels:
    - "<label 1>"
    - "<label 2>"
```

Deck-level designer assets live in frontmatter:

```yaml
designer_assets:
  - id: brand_logo
    type: logo
    path: assets/source/logo.png
    usage: "Place exact logo in the top-right corner"
    scope: deck
    placement: top-right
    required: true
  - id: board_template
    type: ppt-template
    path: assets/source/board-template.pptx
    usage: "Use as layout and typography reference; do not copy text"
    scope: deck
    required: false
```

Deck-level footer defaults also live in frontmatter:

```yaml
production_defaults:
  footer:
    page_numbers: true
    page_number_format: "{page}"
    cr_mark: true
    cr_text: "CR"
    placement: bottom-left-cr-bottom-right-page
```

Slide content (body, sources, speaker notes) is markdown, not YAML.
Titles MUST be action titles: full sentence with verb, sentence case, no trailing period, ≤14 words.
See `standards/deck-validation.md` for the full checklist.

## Designer-mode sequence

When the request implies designer mode:

1. **Content design** — define the slide objective and audience takeaway; write the action title and body before choosing imagery
2. **Slide structure proposal** — propose the composition before generating visuals; decide the layout and image role; keep the slide aligned to the deck design system
3. **Asset preparation** — resolve `designer_assets` and slide `asset_refs`; render `.pptx` templates or prior decks to PNG previews; prepare logos and reference images for the model
4. **Spec lock** — make sure the slide block in deck.md is clear enough to produce without guessing; confirm the image role and asset usage
5. **Image generation** — derive the prompt from the approved deck.md slide using `skill/references/designer-mode-gpt-image-prompt-scaffold.md`; include prepared asset references by id and usage; use `gpt-image-2`, `size="2560x1440"`, `quality="high"`, `output_format="png"`, `n=1` for final full-slide generation
6. **PDF assembly** — assemble the generated slides into a final PDF only; add OCR/searchable text when tooling is available; do not create a PPTX wrapper for pure designer-mode output
7. **Render review** — inspect the slide/PDF for briefing match, text accuracy, footer/page numbers, logo placement, overlaps, clipping, safe margins, and reading flow; regenerate affected slides only until it passes

The image is a downstream artifact of the slide concept, not the first step.

## Editable deck production

Use when the user wants a `.pptx` and the deck is `ppt-shapes` or explicitly mixed/editable. Do not use this path for pure designer-mode decks.

Preferred build path:
- use `python skill/scripts/build_pptx.py OUTPUT_PPTX DECK_MD [TEMPLATE_PPTX]`
- pass the approved deck.md directly into the builder
- then extend or edit the `.pptx` with `python-pptx` if needed
- preserve template theme, masters, and layouts whenever possible
- export icon PNGs before placement when icons are needed

## Output modes

### Deck outline
Use when the user needs storyline and deck structure only.

### Slide content plan
Use when the user wants exact per-slide thinking without producing files yet.

### Slide critique
Use when reviewing or improving an existing slide/deck.

### Designer-mode PDF
Use when the approved deck is pure `designer-mode`. Deliver a final PDF, add OCR/searchable text when available, and keep review PNGs only as supporting artifacts.

### Editable deck production
Use when the user wants a `.pptx` and the deck has editable `ppt-shapes` content.

## Reuse rule

When the user wants a reviewable planning artifact, keep one canonical deck.md.
Do not split deck logic across multiple files unless the extra structure is operationally useful.

## Guardrails

- do not let visuals drive the message
- do not force images across the whole deck
- do not use decorative stock imagery where icons or clean structure would work better
- do not treat one deck-level image as enough for a designer-mode deck; decide imagery per slide
- do not wrap pure designer-mode slide images in a PPTX just to create a PowerPoint file
- do not use logos, templates, or reference assets without recording them in `designer_assets`
- do not silently ignore a required designer asset that cannot be loaded or prepared
- do not deliver without rendering and inspecting the output
- do not regenerate the whole deck for a localized post-render change unless the change affects the whole deck
- do not let templates, icons, or photos overpower the message
- do not accept title-only opening slides with too much empty space
- do not compress overcrowded content when the right answer is to split the slide
- do not invent unstable layout names from one deck to the next
- do not build slides that read like dashboards or crowded BI screens unless explicitly asked
- do not cram many equal-weight boxes, metrics, legends, and callouts onto one slide
- do not use long paragraphs, tiny text, or sprawling bullet stacks
- do not confuse completeness with clarity; cut, group, or split content until the message is obvious at a glance
- make every slide defend one main takeaway with a small number of supporting elements

## Production mode guidance

### `ppt-shapes`
Best for:
- analytical slides
- editable structures
- process, matrix, agenda, chart, and text-led pages

### `designer-mode`
Best for:
- premium visual slides
- image-backed explanatory pages
- art-directed slides where one visual materially improves communication

### `mixed`
Best for:
- decks that need both clean editable analytical pages and selected premium visual pages

## Style system rules

Always define or infer:
- aspect ratio
- background behavior
- typography mood
- accent palette
- image behavior
- footer behavior
- framing devices

Consistency rules:
- do not let each slide invent a different art direction
- keep repeated elements structurally similar
- keep prompts aligned to one visual language per section or deck
- align to requested brand styling without turning the deck into an ad mockup
- preserve a stable slide grammar: short top title, optional two-line max, compact supporting key-message line, and a main visual area that reads cleanly in a horizontal/Z pattern

## Validation checklist

Before delivering, verify:
- is there a clear, approved deck.md as source of truth
- is the production mode right per slide (check `standards/slide-archetypes.md` preferred modes)
- if imagery is used, was that decision made per slide
- do all slide `asset_refs` resolve to declared `designer_assets`
- were required designer assets found and prepared before generation
- did the rendered output pass inspection against the approved deck.md and briefing
- are logo placement, safe margins, and overlaps correct in the rendered output
- does every rendered slide include the standard `CR` mark and simple numeric page number
- if this is a review change, is there a new `review-##` deck.md with `## Revision Brief`
- did review generation preserve unchanged slides and regenerate only changed slides
- can a busy reader get the point quickly
- does each slide have one main job
- does the body prove the title
- do all titles pass the action-title rules in `standards/deck-validation.md`
- is the density right for the material type
- are alignment and framing consistent
- does the slide feel occupied enough to look finished
- for consulting-style slides, does the title state one insight and does the body prove it directly
- do source, units, notes, and footer/status markings meet the consulting-slide standard where relevant
- if designer mode was requested, did the workflow stay GPT Image 2-first rather than drifting into an unapproved hybrid
- if the deck is pure designer-mode, is the final deliverable PDF-only rather than PPTX
- was OCR/searchable text added to the designer-mode PDF, or clearly reported as unavailable
- does the result clearly read as a native 16:9 slide rather than a rescued crop
- was the aspect ratio obtained from generation rather than forced later through cropping or squeezing
- is the title area controlled, with no oversized paragraph-like heading
- is there a clear horizontal / Z-reading flow from title to message to visual proof
- are the saved deck artifacts clean and standardized rather than spread across ad hoc temp/output folders
- would this still feel respectable as a standalone example of the skill's quality
- does the slide avoid a dashboard feel and instead present a simple visual argument
- is the text load low enough that the message is understandable in a few seconds
- if the slide still feels crowded, should it be split into two slides instead of squeezed tighter
