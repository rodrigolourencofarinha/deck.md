---
name: deck-architect
description: "Design and build slide decks including consulting-style decks, executive reports, MBA/class presentations, workshops, and talk decks. Use when Codex needs to create, revise, structure, critique, or translate a slide-based narrative; choose the material type and audience; draft the storyline before production; generate editable decks with python-pptx; decide between clean analytical slides and more elaborate image-driven framework slides; use designer-mode visual template references; or use bundled Tabler icons for process flows, roadmaps, comparison cards, callouts, and other slide-native visual framing."
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

The **Unified Specsheet** is the canonical planning artifact.

Hard rules:
- planning markdown must mirror `references/unified-slide-spec-sheet.md` exactly
- do not invent a parallel SQLMD/planning schema
- do not begin production until the user approves the final spec
- save meaningful spec versions under `decks/<deck-slug>/specs/`

## Assets and tools

### Core assets
- `assets/RLF_PPT_Template_v1.pptx` — default editable deck base
- `assets/templates_full.pptx` — source deck for the editable template library
- `assets/templates/` — one-slide editable PPTX templates extracted from `templates_full.pptx`
- `assets/visual-templates/` — designer-mode PNG references; use `default-slide.png` when Rodrigo says "use my default template" and `title-page.png` for designer-mode covers
- `assets/think-cell-selected/` — structural inspiration only, not a shipping template mix
- `assets/tabler-icons/outline/`
- `assets/tabler-icons/filled/`
- `assets/tabler-icons/aliases.json`

### Icon workflow
Use Tabler as the default icon set for clean analytical slides, process flows, roadmaps, comparison cards, status markers, and callouts.

Useful commands:
- `python scripts/tabler_icons.py topics`
- `python scripts/tabler_icons.py suggest roadmap`
- `python scripts/tabler_icons.py search "chart arrow"`
- `python scripts/tabler_icons.py export-png chart-bar tmp/chart-bar.png --size 512`

Rules:
- prefer `outline` by default
- use `filled` only for stronger emphasis or tiny badges
- export PNG before placing icons in PPT; `python-pptx` is not reliable with these SVGs here

## Which reference to read

Read only what the task needs.

### Start here
- `references/unified-slide-spec-sheet.md`
  - canonical deck/spec structure

### Deck logic
- `references/deck-workflow.md`
  - deck-level workflow, density, archetypes, and consulting-style storyline rules
- `references/consulting-slide-standards.md`
  - consulting-grade action-title, body-as-proof, source/footer, and pre-flight standards

### Slide building and critique
- `references/single-slide-workflow.md`
  - build order, chart cleanup, and visual standards for one slide
- `references/consulting-slide-standards.md`
  - use when the slide needs McKinsey/BCG/Bain-style discipline, especially for executive or read-alone materials

### PPT shapes / editable deck output
- `references/pptx-production.md`
  - coded render layer, template-driven `ppt-shapes` workflow, and render standard
- `references/template-catalog.md`
  - catalog of one-slide editable PPTX templates by title, category, and best use
- `scripts/build_pptx.py`
  - renders supported `ppt-shapes` slides from the Unified Specsheet
- `scripts/split_template_deck.py`
  - regenerates `assets/templates/` and `references/template-catalog.md` from `assets/templates_full.pptx`

### Designer mode
- `references/designer-mode-workflow.md`
  - designer-mode workflow, visual branches, image decisions, and iteration loop
- `references/designer-mode-gpt-image-prompt-scaffold.md`
  - convert one slide into a GPT Image 2 prompt
- `references/designer-mode-direct-api-pattern.md`
  - default direct GPT Image 2 API pattern for native 16:9 full-slide generation

### Rendering and icons
- `references/tabler-icon-selection.md`
  - shortlist/safe icon choice guidance

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
- minimal on-slide text; prefer short labels, crisp titles, and a few support points over dense paragraphs

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
Use when the user wants a more art-directed workflow with explicit separation between:
- content design
- slide architecture
- generated visual

Characteristics:
- spec first, image second
- visuals remain subordinate to slide logic
- design language must stay consistent across the deck

## Canonical workflow

### 1. Build the Unified Specsheet
The user may arrive with:
1. raw source material
2. a broad deck idea
3. a mostly formatted structure

In all three cases:
- normalize into the Unified Specsheet
- keep the review artifact as the Unified Specsheet itself
- do not jump straight into production while structure is still unclear
- for consulting-style decks, make the action-title sequence readable as the deck's argument before producing slide bodies

### 2. Use the Unified Specsheet as source of truth
The spec should carry:
- deck metadata
- storyline
- design system
- per-slide structure
- layout choice
- content blocks
- image decisions when relevant
- creative direction when relevant

Mode nuance:
- `ppt-shapes`: tighter, more structural, easier to route into the coded render layer
- `designer-mode`: clearer art direction, but still anchored in the same spec

### 3. Mandatory approval gate
Do not:
- build slides
- generate slide visuals
- assemble the deck
- export PPTX/PDF
until the user has approved the final spec.

### 4. Choose production mode
Modes:
- `ppt-shapes`
- `designer-mode`
- `mixed`

If the user has not chosen, recommend the simplest mode that fits the deck.

### 5. Produce in the chosen mode

#### `ppt-shapes`
Use editable PPTX structures.

Rules:
- for now, build through the coded `python-pptx` render layer driven by the Unified Specsheet
- when a user asks for template-driven output, read `references/template-catalog.md` first and choose a one-slide template from `assets/templates/` by slide job
- treat template files as editable structural references; adapt the message, title, chart/table content, and visual hierarchy instead of copying placeholder text
- in the spec, suggest the selected template for each `ppt-shapes` slide and give a short reason before building
- after creating a populated PPTX slide, render it to PNG and inspect the image for wrapping, clipped text, tiny fonts, overlaps, alignment, and density before final delivery
- if the render has problems, revise the slide and re-render until it reads cleanly
- later, explicit template families can replace or enrich this layer
- prefer editable shapes, text, icons, and charts
- use Tabler icons when a small pictogram, connector, or status cue helps

#### `designer-mode`
Use GPT Image 2 as the default production engine for the slide visual output.

Rules:
- do not generate before the spec is clear
- generate slide by slide, not all at once
- allow creative freedom only after the slide logic is locked
- keep the user updated during longer runs
- default to GPT Image 2 end-to-end slide generation for designer mode unless the user explicitly asks for a hybrid workflow
- do not quietly fall back to a hybrid background-plus-assembly approach just because it feels safer
- enforce `aspect_ratio: 16:9` in both the spec and the image-generation call
- prefer native 16:9 generation with `size="2560x1440"` as the default full-slide resolution when using direct GPT Image 2 API calls
- treat `2560x1440` as the preferred 2K/QHD slide target for `gpt-image-2`; it is the recommended upper reliability boundary in current OpenAI guidance
- do not downgrade to older fixed landscape sizes just because local SDK type hints look stale; try the documented `2560x1440` string first, then fall back only if the live API rejects it
- use `quality="high"` for final designer-mode slides, text-heavy slides, detailed diagrams, and exportable PDF/PPT assets
- use `quality="medium"` only for layout or mood previews, and `quality="low"` only for fast exploration where visual precision is not yet important
- use `output_format="png"` and `n=1` for final slides; request multiple variants only during exploration
- request the target aspect ratio from GPT Image 2 directly and prefer native 16:9 outputs over any post-generation aspect correction
- use a direct GPT Image 2 invocation pattern when a concrete runnable example helps avoid API drift; see `references/designer-mode-direct-api-pattern.md`
- treat the slide as a real presentation slide, not a loose poster or background image
- require a visible slide structure: title zone, key-message/support zone, and main visual body arranged in a fast left-to-right / Z-reading flow
- put literal slide text in a dedicated prompt block with quoted strings for title, support line, and labels
- explicitly prohibit extra invented text, watermarks, logos, decorative captions, and unrequested labels
- if one generated slide establishes the desired style, save it as a reference candidate for later slides when tighter deck consistency matters

#### `mixed`
Use when some slides should stay editable and others benefit from designer-mode visuals.

Rules:
- use `slide_mode` explicitly per slide
- do not invent mode decisions late in the process

### 6. Save history and outputs
Save deck work under a tight standard structure:
- `decks/<deck-slug>/specs/`
- `decks/<deck-slug>/outputs/final/`
- optional: `decks/<deck-slug>/outputs/review/`
- optional: `decks/<deck-slug>/assets/source/`
- optional: `decks/<deck-slug>/assets/generated/`
- optional: `decks/<deck-slug>/work/` only for durable helper scripts that are clearly worth keeping

Preferred filenames:
- `decks/<deck-slug>/specs/YYYY-MM-DD-v01-spec.md`
- `decks/<deck-slug>/specs/YYYY-MM-DD-v02-spec.md`
- `decks/<deck-slug>/outputs/final/YYYY-MM-DD-v02-deck.pptx`
- `decks/<deck-slug>/outputs/final/YYYY-MM-DD-v02-deck.pdf`
- `decks/<deck-slug>/outputs/review/YYYY-MM-DD-v02-slide-01.png`

Rules:
- save meaningful revisions, not every trivial wording tweak
- keep the latest approved spec easy to find
- keep earlier major versions when structure changes materially
- do not scatter duplicate export trees like `png/`, `png-v04/`, `fullslides/`, and `prepared-*` unless there is a very clear operational reason
- do not persist scratch crops, temporary resized variants, or throwaway assembly files in the deck folder as if they were real assets
- if temporary files are needed during assembly, keep them in ephemeral `tmp/` and clean them up or ignore them

### 7. Keep the user informed
Especially in designer mode, use concise progress updates such as:
- “Slide 1 generated. Going to the next.”

## Fast operating sequence

1. Classify the request.
2. Draft the storyline.
3. Create the Unified Specsheet.
4. Save the current version under `decks/<deck-slug>/specs/`.
5. Get approval.
6. Produce slides in the chosen mode.
7. Save outputs under `decks/<deck-slug>/outputs/`.
8. Review against visual standards.

If the build is simple, keep the workflow simple.
Do not create extra planning files unless they materially help.

## Designer-mode sequence

When the request implies designer mode:

1. **Content design**
- define the slide objective and audience takeaway
- decide what belongs on the slide and what stays off it
- write the title and supporting content before choosing imagery

2. **Slide structure proposal**
- propose the composition before generating visuals
- decide the layout and image role
- keep the slide aligned to the deck design system

3. **Spec lock**
- make sure the slide block is clear enough to produce without guessing
- confirm the image role for that slide

4. **Image generation**
- derive the prompt from the approved spec using `references/designer-mode-gpt-image-prompt-scaffold.md`
- write the image prompt in this order: goal/use case, canvas and layout, required text, key visual details, deck style, preserve/avoid constraints
- include a `Required text to render exactly` block whenever the slide has known text
- prefer one strong visual idea per slide
- use `gpt-image-2`, `size="2560x1440"`, `quality="high"`, `output_format="png"`, and `n=1` for final full-slide generation
- for exploratory variants, use `n>1` or lower quality only before the final slide is selected
- revise the image prompt if the result does not fit the structure
- when iterating, change one clear prompt section at a time and repeat the preserve rules for text, layout, palette, and title-safe area

5. **Slide assembly**
- if using full-slide designer mode, the generated image itself should already respect the intended slide composition
- if the user explicitly chose a hybrid/component workflow, place the visual into the intended composition after generation
- keep the slide legible and presentation-grade
- native 16:9 generation is required for the standard full-slide workflow; post-generation cropping is not the standard workflow
- do not crop, squeeze, or force-fit generated slide images into 16:9 after the fact as a default workflow
- if the generated result is not truly usable as a 16:9 slide, fix the prompt or regenerate the slide instead of salvaging it through destructive reframing

The image is a downstream artifact of the slide concept, not the first step.

## Editable deck production

Use when the user wants a `.pptx`.

Preferred build path:
- use `scripts/build_pptx.py OUTPUT_PPTX SPEC_YAML [TEMPLATE_PPTX]`
- pass the Unified Specsheet directly into the builder
- keep `ppt-shapes` simple for now through the coded render layer
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

### Editable deck production
Use when the user wants a `.pptx` and possibly a `.pdf`.

## Reuse rule

When the user wants a reviewable planning artifact, keep one canonical spec.
Do not split deck logic across multiple files unless the extra structure is operationally useful.

## Guardrails

- do not let visuals drive the message
- do not force images across the whole deck
- do not use decorative stock imagery where icons or clean structure would work better
- do not treat one deck-level image as enough for a designer-mode deck; decide imagery per slide
- do not let templates, icons, or photos overpower the message
- do not accept title-only opening slides with too much empty space
- do not compress overcrowded content when the right answer is to split the slide
- do not invent unstable layout names from one deck to the next
- do not build slides that read like dashboards, control panels, or crowded BI screens unless the user explicitly asks for that format
- do not cram many equal-weight boxes, metrics, legends, and callouts onto one slide
- do not use long paragraphs, tiny text, or sprawling bullet stacks to “fit everything in”
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
- framing devices

Consistency rules:
- do not let each slide invent a different art direction
- keep repeated elements structurally similar
- keep prompts aligned to one visual language per section or deck
- align to requested brand styling without turning the deck into an ad mockup
- preserve a stable slide grammar when requested: short top title, optional two-line max, compact supporting key-message line, and a main visual area that reads cleanly in a horizontal/Z pattern

## Validation checklist

Before delivering, verify:
- is there a clear source of truth for the deck
- is the production mode right per slide
- if imagery is used, was that decision made per slide
- can a busy reader get the point quickly
- does each slide have one main job
- does the body prove the title
- is the density right for the material type
- are alignment and framing consistent
- does the slide feel occupied enough to look finished
- for consulting-style slides, does the title state one insight and does the body prove it directly
- do source, units, notes, and footer/status markings meet the consulting-slide standard where relevant
- if designer mode was requested, did the workflow stay GPT Image 2-first rather than drifting into an unapproved hybrid
- does the result clearly read as a native 16:9 slide rather than a rescued crop
- was the aspect ratio obtained from generation rather than forced later through cropping or squeezing
- is the title area controlled, with no oversized paragraph-like heading
- is there a clear horizontal / Z-reading flow from title to message to visual proof
- are the saved deck artifacts clean and standardized rather than spread across ad hoc temp/output folders
- would this still feel respectable as a standalone example of the skill’s quality
- does the slide avoid a dashboard feel and instead present a simple visual argument
- is the text load low enough that the message is understandable in a few seconds
- if the slide still feels crowded, should it be split into two slides instead of squeezed tighter
