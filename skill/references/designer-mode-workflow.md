# Designer-mode workflow

Use this note when the slide should be more art-directed, image-led, or transformed into a more premium visual composition.

## Core rule

Do not start from an image.
Start from the approved deck.md.

Default behavior for designer-mode requests:
- use `gpt-image-2` through Codex OAuth/Codex image tooling as the primary and default end-to-end slide generator
- use the direct OpenAI Image API key path only as a fallback after the Codex-authenticated path fails and the human approves continuing with the fallback
- do not invent a hybrid background-plus-manual-assembly workflow unless the user explicitly asks for it
- record every asset the visual model should receive in `designer_assets`: logos, existing decks, rendered slide previews, templates, brand guides, screenshots, icons, and reference images
- do not pass undeclared assets to the visual model
- use per-slide `asset_refs` when an asset applies only to specific slides
- deliver pure designer-mode decks as final PDFs only; do not make PPTX wrappers because the slides are not editable
- add OCR/searchable text to the final PDF when tooling is available, and say clearly if OCR could not be applied
- include the standard small footer on every slide unless disabled in the approved deck.md: `CR` lower-left and simple page numbers (`1`, `2`, `3`, ...) lower-right, never total-count formats such as `1/3`
- after generation, render and inspect the slide/PDF against the approved deck.md and briefing before delivery
- if the human asks for post-render changes, create a new review deck.md and regenerate only changed slides
- for targeted text/content edits to an already rendered designer-mode slide, pass the prior rendered slide image back to `gpt-image-2` as an image edit/reference and ask it to preserve the visual while changing only the requested text or concept
- do not patch generated slides by covering text with manual rectangles/banners or downstream overlays unless the user explicitly asks for a hybrid/manual fix; those quick patches create visible artifacts and should not be the default
- treat the generated output as a real 16:9 presentation slide, not just a background image or poster
- request native 16:9 output from the model itself rather than generating first and rescuing it later through crop/resize hacks
- use `size="2560x1440"` and `quality="high"` for final full-slide outputs
- use lower quality only for fast exploration before a final slide is selected
- when the user asks to use a template or visual reference, require an external asset declared in `designer_assets`; do not assume a bundled template exists

Sequence:
1. lock the slide title and content blocks
2. lock the slide layout, reading path, and image role
3. confirm the production mode, whether it is `full-slide` or an explicitly approved hybrid/component mode, and which `designer_assets` / `asset_refs` apply
4. prepare referenced assets for the image model
5. derive the image brief from the spec
6. generate the visual if one is actually needed
7. if hybrid mode was explicitly chosen, place the visual into the intended composition; otherwise expect the generated slide to already respect the slide composition
8. assemble the approved designer-mode slides into a final PDF, adding OCR/searchable text when available
9. inspect the rendered result against the approved deck.md, assets, footer/page numbers, and briefing
10. for targeted review edits, use the prior rendered slide as the first image input and prompt the model to preserve composition, palette, typography feel, spacing, title zone, and all unchanged text
11. regenerate affected slides only until the render review passes

If the output fails the slide contract, regenerate.
Do not default to center-cropping or force-fitting the image just to make it fill the slide.

## When to use designer mode

Use it for:
- premium visual slides
- opening concept slides
- stronger framework slides
- image-backed explanatory pages
- redesigning an existing slide into a more visual version

Do not use it for every slide.
Use it only when a stronger visual treatment materially improves explanation or impact.

## Visual branches inside designer mode

### Clean image-supported slide
Use when one cutout or simple metaphor visual strengthens a mostly analytical slide.

Best for:
- agenda or opening slides
- framing slides
- quote or key-message slides
- concept introduction slides

### Elaborated framework slide
Use when a central visual or crafted framework does real explanatory work.

Best for:
- strategic framework slides
- layered architectures
- funnels, pyramids, and transformation models
- premium synthesis slides

Rules:
- one hero visual per slide
- keep supporting text compact
- annotations should be short and strategic
- do not let the visual overpower the title or reading flow

### Visual redesign
Use when the user already has a slide and wants a stronger, more premium version without changing the core logic.

Keep:
- original title logic
- key explanatory blocks
- main conceptual structure
- message and key evidence from the existing slide

Change:
- composition
- occupancy
- hierarchy
- image use
- framing devices

Default use of old slides/decks:
- treat them as content-and-style references, not as layout locks
- preserve the message and key evidence
- borrow useful density, typography mood, visual rhythm, and brand cues
- redesign the composition freely unless the approved brief asks for close redesign

Prefer composition over ornament.

## Image decision rules

Only add an image when it materially improves the slide.

Good fits:
- hero concept visual
- isolated object or subject
- explanatory metaphor
- dominant framework visual
- full-slide art-directed pages where `gpt-image-2` can carry both the composition and the visual language cleanly

Usually poor fits:
- dense process slides
- KPI dashboards
- matrices
- content-heavy synthesis pages that already have enough structure

## Slide-format contract

When the request is for a designer-mode slide rather than a loose visual, the prompt and review loop should enforce a real slide grammar.

Default contract:
- widescreen 16:9 composition
- clear top title zone, usually top-left
- title should be short and preferably fit in one or two lines
- optional compact key-message or support line under the title
- main visual body should carry the proof or concept
- composition should read in a fast horizontal / Z pattern
- leave enough safe space so the title and support text feel intentionally placed, not floating randomly

Reject outputs that feel like:
- a square or portrait image awkwardly stretched into a slide
- a poster with no presentation hierarchy
- a background plate with nowhere credible for the slide title to live
- a cinematic artwork that ignores the top message zone
- a cropped salvage job where important composition got cut off just to force the slide into 16:9

## Image style rules

Prefer:
- one strong visual idea per slide
- clean silhouettes or business-legible framework visuals
- visual language consistent with the deck
- enough whitespace and contrast for presentation use

Avoid:
- busy scenes
- decorative collage feel
- unrelated multiple objects
- visuals that solve a different problem than the slide

## Prompt derivation rule

If a slide is in `designer-mode` and the image decision is not `none`, derive the prompt from:
- the deck design system
- declared `designer_assets` with `scope: deck`
- slide-specific `asset_refs`
- prepared model inputs listed in `method/model-inputs.yaml`
- the slide title
- the slide layout
- the slide reading path
- the image role
- the slide content blocks
- creative-direction fields such as mood, metaphor, composition intent, prompt notes, and avoid-list

The prompt should explicitly state:
- that the output is a 16:9 presentation slide
- where the title zone lives
- whether the title must fit in one or two lines
- whether a key-message/support line sits below the title
- the exact quoted text to render, including title, support line, and required labels
- that no extra text, watermarks, logos, or invented captions should appear
- how each referenced asset should be used, including its image input label and whether a logo must appear and where
- the computed footer text and placement for this slide
- how the eye should move horizontally or in a Z pattern across the slide

Use `references/designer-mode-gpt-image-prompt-scaffold.md` to turn that brief into the actual image generation prompt.

## Designer assets

Record every designer-mode asset in the approved deck.md before production:

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
  - id: existing_deck
    type: existing-deck
    path: assets/source/original-deck.pptx
    usage: "Use as source content and style context; preserve message and key evidence, but redesign composition freely"
    scope: deck
    required: false
  - id: existing_slide_previews
    type: slide-preview
    path: assets/prepared/original-slides/
    usage: "Use corresponding old-slide previews as content-and-style references for visual redesign"
    scope: deck
    required: false
  - id: visual_template
    type: reference-image
    path: assets/source/supplied-slide-reference.png
    usage: "Use as title, margin, typography, and footer-safe-area reference; do not copy placeholder text"
    scope: deck
    required: false
```

Use slide-level `asset_refs` when only some slides use an asset:

```yaml
asset_refs: [brand_logo, existing_slide_previews, visual_template]
```

Asset handling rules:
- resolve every `asset_refs` id against `designer_assets`
- stop before production if a required asset cannot be found
- render `.pptx`, `.pdf`, or prior-deck references to PNG previews before using them with the image model
- save prepared previews and normalized images under `assets/prepared/`
- write `method/model-inputs.yaml` with source asset id, prepared path, image input label, slide scope, and usage
- pass logos as image inputs when exact placement is required; state the desired `placement`
- use template assets as layout, typography, density, or visual-rhythm references, not as permission to copy placeholder text
- use existing slide/deck assets as content-and-style references by default: preserve message and key evidence, borrow useful visual rhythm, and redesign composition freely
- keep the asset role narrow in the prompt so a reference deck or logo does not overpower the slide message

## Generation parameter defaults

For final full-slide designer-mode output:
- `model="gpt-image-2"`
- `primary_auth="codex-oauth"`
- `fallback_auth="openai-api-key"` only after Codex OAuth/Codex image tooling fails and the human approves the fallback
- `size="2560x1440"`
- `quality="high"`
- `output_format="png"`
- `n=1`

Final deck assembly for pure designer-mode:
- create one final PDF from the approved slide PNGs
- run OCR or add a searchable text layer when tooling is available
- do not create a PPTX wrapper around generated slide images
- verify the standard `CR` mark and simple page number appear on every slide before assembly
- keep per-slide PNGs inside the active production instance, not scattered as loose final deliverables
- save untouched model outputs in `images/raw/`
- save manipulated/composited images in `images/composed/`
- save inspected accepted slide images in `images/reviewed/`
- save prompts, request/response metadata, manipulation logs, render-review notes, and OCR notes in `method/`
- save the exact prepared model input map in `method/model-inputs.yaml`

Final render review:
- inspect the PDF or rendered slide PNGs before delivery
- compare against the approved deck.md, original briefing, and any `## Revision Brief`
- verify text accuracy, title hierarchy, slide count/order, and required labels
- verify the `CR` footer mark and simple numeric page numbers are present, small, consistent, and not overlapping other content
- verify logos and designer assets are in the intended placement and do not overlap text or visuals
- reject clipped content, unsafe margins, unreadable text, accidental extra labels, and weak reading flow
- regenerate only failed slides, then reassemble and inspect again

Use `quality="medium"` for layout or mood previews.
Use `quality="low"` only for fast exploration where text, fine detail, and export quality are not yet important.
Use multiple variants only during exploration, then regenerate or select one final candidate at `quality="high"`.

## Reference-image consistency

Prompt repetition is the baseline consistency method.
When tighter consistency matters:
- save the best approved slide or style frame as a reference candidate
- pass it as an input image if the chosen image operation supports it
- identify it clearly, such as `Image 1: approved deck style reference`
- state whether to match palette, typography mood, framing, spacing, icon treatment, or overall visual grammar
- still repeat exact text, title-safe zone, reading path, and avoid-list in the new prompt

Do not use a reference image to override the slide's actual content logic.

## Visual template references

Use this path when the user points to an external template image, existing slide, or slide reference asset in `designer_assets`.

Behavior:
- pass the prepared reference as an image input in the image edit/reference call
- treat the template as a placement and typography reference, not a full visual style lock
- preserve the white background, large title typography, title placement, spacious margins, and footer/page-number safe area
- replace all placeholder text with the real slide title, subtitle, standard `CR` footer mark, and simple slide number unless the approved deck.md disables the footer
- ignore the template's placeholder body emptiness, dashed footer box, and any placeholder wording
- allow the model to freely create body visuals, diagrams, metaphors, icons, accent colors, and visual composition that fit the slide message
- keep the generated body content inside the open white area so it can be copied or placed back into a deck using the same look and feel
- repeat the reference instructions on every slide generation; do not rely on the model remembering the template from a prior slide

Spec convention:
- add a `designer_assets` entry with `type: reference-image` or `type: ppt-template`
- add slide-level `asset_refs` when only specific slides should use the reference
- capture the preservation scope in the asset `usage` or slide `creative_direction.prompt_notes`

## Standard artifact workspace

Use the standard instance workspace for generated deck production. One instance equals one human-visible production round, such as first generation, first review, second review, and so on.

Default structure:
- `decks/<deck-slug>/specs/`
- `decks/<deck-slug>/assets/source/`
- `decks/<deck-slug>/assets/prepared/`
- `decks/<deck-slug>/instances/001-initial/deck.md`
- `decks/<deck-slug>/instances/001-initial/manifest.yaml`
- `decks/<deck-slug>/instances/001-initial/method/`
- `decks/<deck-slug>/instances/001-initial/images/raw/`
- `decks/<deck-slug>/instances/001-initial/images/composed/`
- `decks/<deck-slug>/instances/001-initial/images/reviewed/`
- `decks/<deck-slug>/instances/001-initial/outputs/`
- `decks/<deck-slug>/instances/002-review-01/`
- `decks/<deck-slug>/outputs/final/`
- optional: `decks/<deck-slug>/outputs/review/`
- optional: `decks/<deck-slug>/work/`

Rules:
- do not overwrite an earlier instance
- keep generated source images in `images/raw/`, not split across ad hoc folders like `generated/` and `fullslides/`
- keep manipulated/composited images in `images/composed/`
- keep only inspected accepted images in `images/reviewed/`
- record prompts, generation parameters, request/response metadata, manipulation logs, render-review notes, and OCR notes in `method/`
- record every image/deck/template/logo input passed to the model in `method/model-inputs.yaml`
- add `manifest.yaml` with source spec, previous instance, changed slides, reused slides, reviewed images, status, and final output paths
- keep review renders separate from final deliverables
- do not keep `prepared-*` crops or resized rescue files as durable deck artifacts
- use `work/` only for scripts worth preserving; otherwise keep scratch work in ephemeral `tmp/`

Do not split deck logic across multiple files unless it is genuinely useful.

## Visual iteration loop

1. generate or revise the slide
2. render or export the result
3. review the slide visually
4. diagnose concrete issues
5. revise the layout, prompt, or slide content
6. regenerate and compare

When revising:
- change one prompt section at a time when possible
- repeat preserve rules for exact text, layout, palette, title zone, arrows, labels, and reference-image behavior
- prefer a clean targeted prompt revision over adding a long list of compensating instructions
- keep the previous output until the replacement has passed visual review

Inspect for:
- weak hierarchy
- too much empty space
- timid occupancy
- title too small or too long
- text too dense
- image dominating instead of explaining
- framework not landing fast enough
- output not actually reading as a 16:9 slide
- missing title-safe zone
- broken horizontal / Z-reading flow
- logo or asset placement wrong, overlapping, or off-margin
- rendered slide no longer matching the briefing or action title
- evidence of crop-rescue or force-fit behavior

Trust the rendered slide, not just the spec or raw content.

## Post-render human changes

Use this when the human has seen the rendered output and asks for a change.

Workflow:
1. Keep the previous approved deck.md and rendered slide images as the baseline.
2. Create a new spec file named like `YYYY-MM-DD-review-01-deck.md` or `YYYY-MM-DD-review-02-deck.md`.
3. Create a new instance folder such as `002-review-01`.
4. Add `## Revision Brief` with the previous deck path, review round, human change request, changed slides, unchanged slides, regeneration scope, and preserve list.
5. Patch only the deck.md fields needed for the requested change.
6. For each changed designer-mode slide, always pass to the model: the previous rendered slide image, the previous slide spec, the updated slide spec, and the human's exact change request verbatim. Do not paraphrase the review or omit any part of it.
7. State in the prompt exactly and only what must change. List each requested change as a concrete, specific instruction. If something is not listed as a change, the model must treat it as approved and preserve it exactly.
8. Do not use overlay or compositing to apply the change on top of the previous render. Regenerate the slide from the prompt with the change integrated.
9. Explicitly instruct the model to keep everything that is not being changed: composition, palette, typography, spacing, logo placement, footer, reading flow, and any other approved element. The goal is the minimum necessary change, not a fresh interpretation of the slide.
10. Reuse unchanged slide images by copying or referencing prior `images/reviewed/` files.
11. Update `manifest.yaml` with changed slides, reused slides, source spec, previous instance, status, and output paths.
12. Reassemble the PDF, render/inspect the full artifact, and repeat only for failed changed slides.

Do not treat a small review change as a fresh deck generation. The point of review versions is to make the delta explicit and keep approved work stable.

## Guardrails

- do not let the image determine the slide message
- do not generate visuals before the structure is clear
- do not assume every designer-mode slide needs a generated image
- do not turn every slide into a cinematic poster
- do not add visuals just because they look cool
- do not regenerate unchanged slides during a review change unless the new brief truly changes them
- do not use overlay or compositing to apply review changes; regenerate with the change integrated into the prompt
- always pass the human's review verbatim when prompting for a changed slide; do not paraphrase or summarize
- always tell the model explicitly what must NOT change so it does not drift the approved parts of the slide
