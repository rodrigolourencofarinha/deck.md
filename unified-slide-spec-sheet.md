# Unified slide spec sheet

Use this as the single canonical YAML-first spec format for slide planning before production.

The goal is simple:
- one deck-level spec sheet
- one stable structure the model can read quickly
- one source of truth before building PPT shapes or designer-mode outputs
- one durable spec artifact that can be saved and revisited later if the deck needs rollback or comparison

This format should replace scattered slide-spec guidance whenever the user wants a structured, reviewable, reusable deck blueprint.

## What this spec is for

Use this format when:
- the deck should be planned before production
- the user arrives with raw resources, a broad idea, or an already formatted deck idea
- the user wants exact text and layout intent captured clearly
- slides may later be converted into PPT templates or production pipelines
- the deck may use `ppt-shapes`, `designer-mode`, or `mixed`

Treat the spec sheet as the canonical blueprint for the deck.
It is not a loose brainstorm.
It is the handoff between idea and slide production.

Production must not begin until the user has explicitly approved the final spec sheet.

## Core principles

- one slide = one message
- avoid duplicated meaning across fields when one field is enough
- titles should be takeaway titles, not topic labels
- visuals must support the argument
- layout names should stay stable across decks
- production choices should be explicit only where they help the build
- prefer editable structures unless visual treatment materially improves the slide
- when designer mode is chosen, default to GPT Image 2 end-to-end slide generation unless the user explicitly asks for a hybrid workflow
- designer-mode slides must still obey real slide grammar: 16:9 widescreen framing, title-safe zone, compact message hierarchy, and a fast reading path
- save spec-sheet history during meaningful revisions so the workflow can step back when needed

## Recommended top-level structure

```md
---
title: How the Slide Skill Works
objective: Show that the skill follows a rigorous workflow in which message clarity comes before design and production
audience: People learning how the slide skill works
tone: Clear, modern, disciplined, presentation-grade
aspect_ratio: 16:9
language: en
deliverable_mode: designer-mode
author: Rodrigo Lourenço Farinha
date: 2026-04-23
version: v1
---

## Storyline
- slide: 1
  key_takeaway: A deliberate workflow turns slide creation into a reliable system.

## Design
style:
- clean premium process slide
- light background
- modern consulting aesthetic
- strong visual rhythm
- high clarity at a glance
- structured but polished

palette:
  primary: "#111111"
  secondary: "#5B5B5B"
  accent: "#2F6BFF"
  accent_soft: "#DCE7FF"
  background: "#FFFFFF"
  line: "#B8C7E6"

typography:
- restrained analytical headline
- compact step labels
- short supporting copy
- emphasis through hierarchy, not decoration

visual_system:
- connected pathway or pipeline spine
- numbered stage markers
- modular step containers
- subtle directional flow cues
- final-stage emphasis on output

rules:
- one slide, one message
- title must state the takeaway, not just the topic
- process must read instantly from left to right
- keep text compact and scannable
- avoid generic SmartArt or chevron clichés
- emphasize disciplined progression and trustworthiness
- visual polish must support clarity, not overpower it

## Slides

### Slide 1
id: 1
title: A deliberate workflow turns slide creation into a reliable system
subtitle: From message clarity to final render, each step improves consistency and quality.
layout: horizontal process
image_decision: full-generated-visual
content:
  steps:
  - title: Define the message
    body: Decide what the slide must actually say.
  - title: Define the structure
    body: Choose the layout and organize the logic.
  - title: Write the slide spec
    body: Capture the slide instructions in structured form.
  - title: Review and refine
    body: Improve clarity, flow, and emphasis before production.
  - title: Generate the slide
    body: Build the slide in PPT shapes or designer mode.
  - title: Render the deck
    body: Export the final presentation for review or delivery.
creative_direction:
  visual_ambition: Premium process slide with stronger presence than a standard infographic, while remaining presentation-clean and highly legible.
  mood: intelligent, systematic, modern, trustworthy, controlled
  metaphor: a clean journey pipeline or structured progression path rather than a literal factory or software flowchart
  composition_intent: A dominant horizontal spine or pathway across the slide with six evenly paced stages, each integrated into one coherent visual system; strong title area above; balanced occupancy with no dead zones
  prompt_notes:
  - Favor a polished journey/pipeline composition over generic boxes in a row.
  - The slide should feel designed, not templated.
  - Preserve strong rhythm and even spacing across all six steps.
  - Make the flow feel disciplined and reliable, not playful.
  - Keep the design presentation-grade and executive-friendly.
```

## Canonical section definitions

### Frontmatter

Use frontmatter for deck-level metadata.

Required fields:
- `title`
- `objective`
- `audience`
- `tone`
- `aspect_ratio`
- `language`
- `deliverable_mode`

Optional fields:
- `author`
- `date`
- `version`
- `brand`
- `client`
- `context`

Recommended controlled values:
- `aspect_ratio`: `16:9` by default
- `deliverable_mode`: `ppt-shapes` | `designer-mode` | `mixed`

Compatibility note:
- `deck_title` is accepted as a legacy alias, but `title` is now the canonical field name.
- `material_type` is no longer part of the canonical schema.

### `## Storyline`

This is the deck narrative in compact structured form.

Each item should capture:
- slide number
- slide key takeaway

Rules:
- one entry per slide
- write the core message, not a topic label
- keep it short enough to scan quickly
- make the sequence read like a coherent argument
- do not duplicate the slide title here unless there is a strong reason

Recommended shape:

```md
## Storyline
- slide: 1
  key_takeaway: ...
- slide: 2
  key_takeaway: ...
```

### `## Design`

This is the shared visual system for the whole deck.

Recommended fields:
- `style`
- `palette`
- `typography`
- `visual_system`
- `rules`

Use this section to define the main design guidelines before any slide production begins.
This is where color, typography, framing, icon behavior, connectors, and overall visual behavior should be made explicit.

### `## Slides`

This contains one structured block per slide.

Use stable headings:
- `### Slide 1`
- `### Slide 2`
- `### Slide 3`

Each slide block should be specific enough that production can happen without guessing.

## Canonical per-slide template

The slide schema changes slightly depending on the deck production mode.
Keep the YAML tight and avoid duplicated fields.

### Common slide core

```md
### Slide 1
id: 1
title: <mandatory>
subtitle: <optional>
layout: <mandatory>
image_decision: <none | icon-only | cutout | full-generated-visual>
content:
  <mandatory content blocks>
```

Required slide fields:
- `id`
- `title`
- `layout`
- `content`

Optional slide fields:
- `subtitle`
- `image_decision`
- `template`
- `slide_mode`
- `creative_direction`
- `source_notes`
- `reading_path`
- `title_zone`
- `title_line_limit`
- `message_zone`
- `visual_zone`
- `production_strategy`
- `asset_role`

### `ppt-shapes`

Use a tighter, more structural spec.
This version should be template-ready and operationally explicit.

Rules:
- `template` is required
- use the chosen `layout` as the unique layout name for the slide
- keep the content block structurally tight and template-ready
- prefer exact fields over prose

Example:

```md
### Slide 2
id: 2
title: This skill solves the problem in two ways
layout: two-columns
template: two-columns-basic
image_decision: none
content:
  left_column:
    title: PPT shapes
    bullets:
    - Better for analytical slides
    - Fully editable
    - Best when clarity and control matter
  right_column:
    title: Designer mode
    bullets:
    - Better for premium visual slides
    - More art-directed
    - Best when visual impact matters
```

### `designer-mode`

Use a more open art-direction spec.
Keep the title and content clear, but do not over-constrain the visual solution.

Rules:
- do not use `template`
- when Rodrigo asks to "use my default template", use `visual_template_reference`, not `template`; this is a designer-mode image reference, not an editable PPTX template
- allow richer art direction where it helps
- express the visual intent through `creative_direction`
- do not duplicate a separate `visual_logic` field
- default `production_strategy` to `full-slide-gpt-image-2`
- only use a hybrid/component workflow when the user explicitly asks for it
- always preserve a real 16:9 slide composition
- request native 16:9 generation rather than planning to crop later
- define enough slide grammar that the output has a credible title area, message hierarchy, and reading flow

Designer-mode slides may include:
- `creative_direction`
- `visual_ambition`
- `mood`
- `metaphor`
- `composition_intent`
- `prompt_notes`
- `required_text`
- `text_rules`
- `preserve`
- `reference_images`
- `visual_template_reference`
- `visual_template_scope`
- `visual_template_freedom`
- `generation_params`
- `avoid`

Use `required_text` when exact text must appear in the generated slide image.
Use `preserve` to name invariants that should survive prompt revisions, such as title zone, reading path, palette, label text, arrows, and framework geometry.
Use `reference_images` only when an approved slide or style frame should guide later slide generations.
Use `visual_template_reference` when a fixed template image should be passed to the image model as layout/style context. For Rodrigo's default content template, set it to `assets/visual-templates/default-slide.png` and preserve only the white background, title typography/placement, spacious margins, and footer safe area. Body visuals, diagrams, metaphors, and accent colors remain free.

Example:

```md
### Slide 4
id: 4
title: The business works as an integrated system
layout: hero-visual-right
production_strategy: full-slide-gpt-image-2
reading_path: horizontal-z
title_zone: top-left
title_line_limit: 2
message_zone: directly below title
visual_zone: right-dominant visual body
image_decision: full-generated-visual
visual_template_reference: assets/visual-templates/default-slide.png
visual_template_scope: preserve white background, title typography/placement, spacious margins, and footer safe area only
visual_template_freedom: body visuals, diagrams, metaphors, icons, and accent colors may change to fit the slide
content:
  body:
  - Show that operations, technology, and commercial decisions reinforce one another.
  - The slide should make interdependence feel obvious, not abstract.
creative_direction:
  visual_ambition: premium consulting visual with strong conceptual clarity
  mood: intelligent, modern, integrated, high-trust
  metaphor: a coordinated system of interconnected moving parts, but not a literal stock gear diagram
  composition_intent: large dominant visual on the right, explanatory synthesis on the left, enough negative space for a premium feel
  prompt_notes:
  - surprise us with strong visual thinking
  - avoid generic corporate stock-photo energy
  - prioritize a concept that reads immediately on a presentation slide
  - keep it presentation-grade rather than cinematic-for-its-own-sake
  - preserve a believable title area with a short title and compact support line
  avoid:
  - cheesy 3D gears
  - cluttered dashboards
  - random futuristic UI overlays
  - decorative complexity without explanatory value
```

### `mixed`

For mixed decks, add explicit per-slide mode.

Rules:
- use `slide_mode: ppt-shapes | designer-mode`
- only add `template` on `ppt-shapes` slides
- only add `creative_direction` on `designer-mode` slides unless there is a very specific reason otherwise

Example:

```md
### Slide 5
id: 5
title: The deck combines clear analysis with selected premium visuals
slide_mode: designer-mode
layout: hero-visual-left
image_decision: full-generated-visual
content:
  body:
  - Use a stronger visual on the key synthesis slide.
creative_direction:
  mood: premium, modern, controlled
```

Rule of thumb:
- `ppt-shapes` specs should be tighter
- `designer-mode` specs should be more guided than constrained
- mixed mode should be explicit per slide to avoid ambiguity

## Stable layout vocabulary

Keep layout names reusable and controlled.
Do not casually invent synonyms.

Recommended starter set:
- `takeaway + support`
- `two-columns`
- `three-cards`
- `horizontal process`
- `matrix`
- `hero-visual-left`
- `hero-visual-right`
- `section-divider`
- `quote`
- `agenda`

If a new layout is needed, define it once and then reuse the exact same name.

## Layout-specific content guidance

### `takeaway + support`

Use for:
- one strong claim
- a short explanatory lead
- a support list, proof points, or structured evidence

Recommended content shape:

```md
content:
  lead:
  - ...
  - ...
  support:
  - ...
  - ...
  - ...
```

### `two-columns`

Use for:
- comparisons
- mode splits
- before/after
- tensions or paired ideas

Recommended content shape:

```md
content:
  left_column:
    title: ...
    bullets:
    - ...
    - ...
  right_column:
    title: ...
    bullets:
    - ...
    - ...
  footer:
  - ...
```

### `horizontal process`

Use for:
- workflows
- sequences
- operating models
- phased build logic

Recommended content shape:

```md
content:
  steps:
  - title: ...
    body: ...
  - title: ...
    body: ...
```

### `three-cards`

Use for:
- three drivers
- three options
- three principles

Recommended content shape:

```md
content:
  cards:
  - title: ...
    body: ...
  - title: ...
    body: ...
  - title: ...
    body: ...
```

### `matrix`

Use for:
- 2x2 frameworks
- segmentation
- option mapping

Recommended content shape:

```md
content:
  axes:
    x: ...
    y: ...
  quadrants:
  - title: ...
    body: ...
  - title: ...
    body: ...
  - title: ...
    body: ...
  - title: ...
    body: ...
```

## Production mode rules

The user chooses the production mode whenever possible.
If the user has not chosen yet, recommend the simpler mode that best fits the deck.

### `ppt-shapes`

Use for:
- analytical slides
- editable slides
- process, matrix, agenda, chart, and text-led pages
- slides where precision and editability matter most

Production rule:
- build from PPT templates when those mappings exist
- prefer editable shapes, text, icons, and charts

### `designer-mode`

Use for:
- premium visual slides
- image-backed slides
- stronger art direction
- pages where one visual materially improves communication

Production rule:
- default to `production_strategy: full-slide-gpt-image-2`
- use GPT Image 2 for the slide visuals
- generate slide by slide after the spec is clear
- keep progress visible during longer builds
- preserve `aspect_ratio: 16:9` in both the spec and the generation call
- default final generation params to `model="gpt-image-2"`, `size="2560x1440"`, `quality="high"`, `output_format="png"`, and `n=1`
- keep exact in-image text in a `required_text` block and quote literal strings in the downstream prompt
- use reference images only to preserve style or framing, not to replace the slide's content logic
- request native 16:9 output from the model instead of relying on downstream crop/resize fixes
- reject outputs that behave like posters, background plates, or square images widened into slides
- if the result is wrong, regenerate or improve the prompt rather than forcing the asset into shape

### `mixed`

A deck may mix both.
Only use designer mode on slides that actually benefit from it.
When mixed mode is chosen, `slide_mode` should be explicit on each slide.

## Image decision rules

Supported values:
- `none`
- `icon-only`
- `cutout`
- `full-generated-visual`

Rules:
- default to `none` or `icon-only` unless imagery clearly helps
- do not force images across the whole deck
- if `designer-mode` is used, still decide image usage per slide
- when `full-generated-visual` is chosen for designer mode, default to a full-slide GPT Image 2 output unless the user explicitly requests hybrid assembly

## Writing rules

- write exact slide text whenever it is known
- prefer short scannable bullets
- keep structural decisions in fields, not buried in prose
- make the slide block readable by both a human and a production model
- do not duplicate the same message across multiple fields unless there is a clear operational need

## Spec history rule

Save meaningful spec-sheet revisions during the workflow.

Guidance:
- keep the latest approved spec easy to find
- preserve earlier major versions when the structure changes materially
- save specs under `decks/<deck-slug>/specs/` in the active workspace
- save final deliverables under `decks/<deck-slug>/outputs/final/`
- optionally save review renders under `decks/<deck-slug>/outputs/review/`
- optionally keep durable source materials under `decks/<deck-slug>/assets/source/`
- optionally keep durable generated assets under `decks/<deck-slug>/assets/generated/`
- only keep helper scripts in `decks/<deck-slug>/work/` when they are genuinely worth preserving
- use versioned filenames or archived copies so the workflow can step back if needed
- include date and revision context in the filenames
- preferred names:
  - `YYYY-MM-DD-v01-spec.md`
  - `YYYY-MM-DD-v02-spec.md`
  - `YYYY-MM-DD-v02-deck.pptx`
  - `YYYY-MM-DD-v02-deck.pdf`
  - `YYYY-MM-DD-v02-slide-01.png`
- do not clutter the workspace with tiny throwaway snapshots for every trivial wording change
- do not treat temporary cropped, resized, or prepared variants as durable assets

## Approval gate

The final spec sheet must be approved by the user before any production starts.

Do not begin any of the following before approval:
- PPT slide building
- designer-mode image generation
- deck assembly
- PPTX export
- PDF export

## Deliverables and progress

Default deliverables when feasible:
- `.pptx`
- `.pdf`

During production, keep the user informed of meaningful progress.
Especially in designer mode, concise slide-by-slide updates are preferred during multi-slide generation.

## Guardrails

- do not split the canonical schema across multiple markdown files unless there is a strong reason
- do not make the spec vague or essay-like
- do not use topic titles when a conclusion title is possible
- do not hide layout intent inside freeform notes
- do not let image generation lead the thinking
- do not invent unstable layout labels from one deck to the next
- do not let designer mode drift into an unapproved hybrid workflow
- do not accept a designer-mode slide that lacks a credible title-safe zone and reading path
- do not normalize bad generations by silently cropping or force-fitting them into the slide

## Recommendation for the skill

Going forward, prefer this unified spec-sheet format as the main planning artifact.
The markdown review artifact shown to the user should mirror this structure exactly rather than introducing a parallel planning format.

Possible future evolution:
- the same spec can later connect to PPT layout templates
- each `layout` value can map to a real template family
- each slide block can become machine-readable input for automated deck generation

That means this format should stay stable, explicit, and reusable.
