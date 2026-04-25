# Image prompt templates

How to convert a `deck.md` slide into a Codex image generation request. This file defines the prompt structure, token injection, and guardrails that produce consistent designer-mode slides. Direct OpenAI Image API calls are a fallback only after Codex image generation is unavailable or fails and the human explicitly approves continuing with the API.

Applies when a slide has `mode: designer-mode` AND `image_decision: full-generated-visual` (or `cutout`).

---

## Base prompt structure

Every generated slide prompt is assembled from six parts, in order:

1. **Format directive** — aspect ratio, size, output constraints
2. **Design context** — from `design_tokens` and deck-level `## Design` rules
3. **Asset references** — from deck-level `designer_assets` and slide-level `asset_refs`
4. **Slide content** — title, body, type, layout
5. **Slide-specific direction** — from `creative_direction` and `required_text`
6. **Computed footer** — from `production_defaults.footer` and slide order

### Template

```
You are producing one slide of a presentation deck.

FORMAT:
- Aspect ratio: {production_defaults.aspect_ratio}
- Size: {image_generation.size}
- Output: {image_generation.output_format}
- Flat vector-style design. No photography unless explicitly requested.

DESIGN LANGUAGE:
- Palette: primary {primary}, secondary {secondary}, accent {accent}, background {background}
- Typography: title {typography.title}; body {typography.body}
- Shape language: corners {corner_style}, line weight {line_weight}
- Icons: {iconography.family}

CONSISTENCY RULES:
{deck-level consistency rules from ## Design}

AVOID:
{deck-level avoid list + slide-level creative_direction.avoid}

ASSET REFERENCES:
{declared designer_assets that apply to this slide, including id, type, usage, placement, and prepared image input label}

SLIDE CONTENT:
- Type: {slide.type}
- Layout: {slide.layout}
- Action title: "{slide.title}"
- Body: {slide.body, rendered as short labels/bullets}
- Footer: lower-left "{footer.cr_text}" when enabled; lower-right "{footer.page_number}" when enabled

CREATIVE DIRECTION:
- Mood: {creative_direction.mood}
- Metaphor: {creative_direction.metaphor}
- Composition: {creative_direction.composition_intent}
- Notes: {creative_direction.prompt_notes}

TEXT LOCK:
The ONLY text that may appear in the image is:
- Title: "{required_text.title}"
- Subtitle: "{required_text.subtitle}" (if present)
- Labels: {required_text.labels}
- Footer: "{footer.cr_text}" and "{footer.page_number}" (if enabled)

Do NOT render any other text, numbers, watermarks, or signatures.
```

---

## Token injection

Values from `design_tokens` in the frontmatter are injected directly into the prompt. Pass actual hex codes, not variable names.

```yaml
# In deck.md:
design_tokens:
  palette:
    primary: "#111111"
    accent:  "#2F6BFF"
```

```
# Rendered into prompt:
Palette: primary #111111, accent #2F6BFF, …
```

---

## Required_text guardrail

This is the single most important rule: **the model MUST NOT invent text in the generated image.**

Enforcement:
1. The prompt explicitly lists the allowed text under `TEXT LOCK`.
2. The prompt explicitly instructs "Do NOT render any other text".
3. Footer text computed from `production_defaults.footer` is appended to the allowed text list.
4. After generation, a vision check (OCR or visual inspection) verifies no extra text appears.
5. If extra text is detected, regenerate with a stronger TEXT LOCK ("Render ONLY the following labels and footer tokens; reject all other text").

If `image_decision: full-generated-visual` and `required_text` is absent, generation MUST be blocked — this is a validation error.

---

## Negative prompts

Compile the avoid list from three sources:
- Deck-level `## Design > Avoid`
- Slide-level `creative_direction.avoid`
- Global defaults: no photographic imagery, no cinematic lighting, no decorative stock-image energy, no dashboard clutter

Pass these as negative instructions in the prompt.

---

## Layout-specific hints

Certain `layout` values map to common composition patterns. Inject layout-specific hints:

| Layout | Composition hint |
|---|---|
| `three-column-scr` | Title top-left; three equal columns below labeled situation/complication/resolution |
| `horizontal-three-column` | Title top-left; three equal columns below with icon + label + caption |
| `chart-left-text-right` | Title top-left; chart area on left 55%; text block on right 40% |
| `chart-full-bleed-with-callout` | Chart fills most of the slide; one callout annotation with an arrow |
| `2x2-matrix` | Title top-left; 2×2 grid centered; axis labels on left and bottom |
| `horizontal-timeline` | Title top-left; timeline horizontal with milestones as nodes |
| `full-bleed-title` | Single large title centered; accent color background |
| `hero-number-with-caption` | One large number centered, short caption below |
| `numbered-list` | Title top-left; numbered items stacked vertically, generous whitespace |
| `risk-table` | Title top-left; table with columns for risk, likelihood, impact, mitigation |
| `owner-action-date-table` | Title top-left; three-column table of action, owner, date |

---

## Quality settings

Defaults for `image_generation.quality`:
- `high` — final decks, client-facing
- `medium` — internal decks, iterations
- `low` — drafts, thumbnails

Use `low` during iteration; switch to `high` for final.

## Prompt and metadata storage

For every generated slide, store the prompt and generation metadata in the active instance's `method/` folder:
- `slide-01.prompt.md` — final prompt sent to the image model
- `slide-01.request.json` — model, size, quality, seed or variant count if available, asset input labels, and other request parameters
- `slide-01.response.json` — response metadata, output filenames, model identifiers, warnings, and provider ids when available
- `model-inputs.yaml` — source asset ids, prepared paths, image input labels, slide scope, and usage for every asset passed to the image model

Do not rely on chat history as the only record of how a slide was generated.

---

## Visual template reference

When `visual_template_reference` is set, the agent passes the referenced image as a style/layout reference to the Codex image generation path. The `visual_template_scope` field specifies what to preserve:

- `"preserve title placement, margins, footer"` — structural elements only
- `"preserve everything"` — full template lock
- `"preserve palette and typography"` — aesthetic only

Default scope: title typography, outer margins, footer safe area. Body composition is free.

## Footer prompt rules

Every designer-mode slide prompt should include the computed footer unless the approved deck.md disables it:
- Place the small `CR` mark in the lower-left corner.
- Place the simple page number (`1`, `2`, `3`, ...) in the lower-right corner.
- Do not include the total slide count; render `1`, not `1/3` or `1 of 3`.
- Use subtle footer styling that matches the deck typography and muted color system.
- Keep footer elements inside the safe area and away from logos, sources, charts, and body content.

The footer is the only numeric text allowed by default besides slide-approved labels. If a slide also contains chart labels or other required numbers, those must still appear in `required_text.labels`.

## Designer asset references

When `designer_assets` is set, the agent prepares every relevant asset before generation and injects a short asset block into the prompt.

Asset prompt rules:
- Identify each prepared image input by id, e.g. `Image 1 is asset brand_logo`.
- State the asset `type`, `usage`, and `placement` if present.
- For logos, state whether the logo must appear exactly and where.
- For `.pptx` templates and existing `.pptx` or `.pdf` decks, render representative slide(s) to PNG first, then state whether to match layout, density, typography, visual rhythm, or palette.
- For existing slides/decks, default to content-and-style reference behavior: preserve message and key evidence, borrow useful visual rhythm, and redesign composition freely.
- Do not allow template or brand assets to override required text, slide logic, or the deck's approved narrative.
- Do not pass any visual input to the model unless it is declared in `designer_assets` and listed in `method/model-inputs.yaml`.
- If `required: true` and the asset cannot be prepared, block generation rather than silently proceeding.

## Generation path and fallback

Default path:
- Use Codex's built-in image generation capability for designer-mode slide images.
- Use the same prompt, prepared image inputs, text lock, footer rules, and output constraints described in this file.
- Store prompts, prepared-input metadata, and output metadata in the active instance's `method/` folder.

Fallback path:
- Do not start with the direct OpenAI Image API.
- If Codex image generation is unavailable, errors, or cannot accept the required prepared inputs, tell the human what failed.
- Ask the human whether to continue with the direct OpenAI Image API fallback.
- Only after approval, use `image_generation.fallback_creator` and record the fallback approval and reason in `method/model-inputs.yaml` or the slide request metadata.

Example prompt block:

```text
ASSET REFERENCES:
- Image 1 is asset brand_logo, type logo. Place the exact logo in the top-right corner on slides where referenced.
- Image 2 is asset existing_slide_previews, type slide-preview. Use the matching old slide as a content-and-style reference; preserve message and key evidence, but redesign the composition freely.
- Image 3 is asset visual_template, type reference-image. Use it only for title placement, margins, typography, and footer safe area; do not copy placeholder text.
```

---

## Failure modes and fixes

| Failure | Fix |
|---|---|
| Extra text appears in image | Strengthen TEXT LOCK; regenerate |
| Image is photographic when deck avoids it | Add explicit "flat vector design, no photography" to prompt |
| Title is cut off or illegible | Increase title area in layout hint; reduce body content |
| Colors don't match palette | Pass hex codes explicitly (not color names); emphasize palette in prompt |
| Icons look wrong style | Name the icon family explicitly ("tabler-outline icons"); provide example icon names |
| Slide feels generic | Add a specific metaphor in `creative_direction.metaphor`; increase specificity of `composition_intent` |
| Designer-mode chart is unreadable | Switch that slide to `mode: ppt-shapes` — charts render better as shapes |
| Logo, old slide, or template is ignored | Add an `ASSET REFERENCES` block with the asset id, input image label, usage, and placement |
| Review change alters too much | Use the prior rendered slide plus old/new slide specs and ask for only the exact delta |
