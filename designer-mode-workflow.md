# Designer-mode workflow

Use this note when the slide should be more art-directed, image-led, or transformed into a more premium visual composition.

## Core rule

Do not start from an image.
Start from the approved Unified Specsheet.

Default behavior for Rodrigo's designer-mode requests:
- use GPT Image 2 as the primary and default end-to-end slide generator
- do not invent a hybrid background-plus-manual-assembly workflow unless the user explicitly asks for it
- treat the generated output as a real 16:9 presentation slide, not just a background image or poster
- request native 16:9 output from the model itself rather than generating first and rescuing it later through crop/resize hacks
- use `size="2560x1440"` and `quality="high"` for final full-slide outputs
- use lower quality only for fast exploration before a final slide is selected
- when Rodrigo says "use my default template", pass `assets/visual-templates/default-slide.png` as a reference image for normal slides; use `assets/visual-templates/title-page.png` for cover/title slides

Sequence:
1. lock the slide title and content blocks
2. lock the slide layout, reading path, and image role
3. confirm the production mode, whether it is `full-slide` or an explicitly approved hybrid/component mode, and whether a visual template reference is being used
4. derive the image brief from the spec
5. generate the visual if one is actually needed
6. if hybrid mode was explicitly chosen, place the visual into the intended composition; otherwise expect the generated slide to already respect the slide composition
7. review the rendered result and iterate

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

Change:
- composition
- occupancy
- hierarchy
- image use
- framing devices

Prefer composition over ornament.

## Image decision rules

Only add an image when it materially improves the slide.

Good fits:
- hero concept visual
- isolated object or subject
- explanatory metaphor
- dominant framework visual
- full-slide art-directed pages where GPT Image 2 can carry both the composition and the visual language cleanly

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
- how the eye should move horizontally or in a Z pattern across the slide

Use `references/designer-mode-gpt-image-prompt-scaffold.md` to turn that brief into the actual GPT Image 2 prompt.

## Generation parameter defaults

For final full-slide designer-mode output:
- `model="gpt-image-2"`
- `size="2560x1440"`
- `quality="high"`
- `output_format="png"`
- `n=1`

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

Use this path when Rodrigo asks for designer mode and says "use my default template" or otherwise points to a template image.

Default references:
- normal content slide: `assets/visual-templates/default-slide.png`
- cover or title page: `assets/visual-templates/title-page.png`

Behavior:
- pass the template PNG as `Image 1` in the image edit/reference call
- treat the template as a placement and typography reference, not a full visual style lock
- preserve the white background, large title typography, title placement, spacious margins, and footer/page-number safe area
- replace all placeholder text with the real slide title, subtitle, footer, and slide number if those are requested
- ignore the template's placeholder body emptiness, dashed footer box, and any placeholder wording
- allow the model to freely create body visuals, diagrams, metaphors, icons, accent colors, and visual composition that fit the slide message
- keep the generated body content inside the open white area so it can be copied or placed back into a deck using the same look and feel
- repeat the reference instructions on every slide generation; do not rely on the model remembering the template from a prior slide

Spec convention:
- add `visual_template_reference: assets/visual-templates/default-slide.png` for content slides when the default template is requested
- add `visual_template_scope: preserve white background, title typography/placement, spacious margins, and footer safe area only`
- add `visual_template_freedom: body visuals, colors, diagrams, and metaphors may change to fit the slide`

## Optional multi-file workspace

Use a larger deck workspace only when there is a real operational reason, such as:
- a larger deck needs review in parts
- multiple people will edit different pieces
- production assets need clearer organization
- the deck mixes many source visuals and intermediate assets

Default structure:
- `decks/<deck-slug>/specs/`
- `decks/<deck-slug>/assets/source/`
- `decks/<deck-slug>/assets/generated/`
- `decks/<deck-slug>/outputs/final/`
- optional: `decks/<deck-slug>/outputs/review/`
- optional: `decks/<deck-slug>/work/`

Rules:
- keep generated source images in one place, not split across ad hoc folders like `generated/` and `fullslides/` unless they truly mean different durable asset classes
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
- evidence of crop-rescue or force-fit behavior

Trust the rendered slide, not just the spec or raw content.

## Guardrails

- do not let the image determine the slide message
- do not generate visuals before the structure is clear
- do not assume every designer-mode slide needs a generated image
- do not turn every slide into a cinematic poster
- do not add visuals just because they look cool
