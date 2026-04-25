# Designer-mode image prompt scaffold

Use this reference when converting a slide spec into the actual prompt for `gpt-image-2` through Codex OAuth/Codex image tooling. The same prompt can be reused for the direct OpenAI Image API key fallback only after the Codex-authenticated path fails and the human approves continuing with the fallback.

This is not the canonical deck spec.
It is the downstream prompt scaffold for the visual layer of one designer-mode slide.

Primary upstream source:
- `deck.md` (see `SPEC.md` for the full field reference)

## Purpose

Turn a designer-mode slide block into a strong image-generation brief that:
- preserves the slide message
- inherits the deck design language
- gives the image generator enough context to create a presentation-grade slide output
- keeps the model inside real slide constraints such as 16:9 framing, title-safe zones, and reading flow
- avoids over-constraining the model when creativity is useful

## Core rule

Do not dump the raw slide spec into the image prompt.
Translate it.

The image prompt should express:
- what the slide means
- what the visual must accomplish
- what design language it belongs to
- what literal text must appear, if any
- what layout, typography, and hierarchy must be preserved
- what should be avoided
- how much freedom the model has

## Prompt inputs

Build the prompt from five layers.

### 1. Slide meaning

Use:
- slide `title`
- the slide storyline takeaway when useful
- essential supporting points from `content`
- `creative_direction` when present

Ask:
- what is the slide trying to make obvious
- what should the audience understand in one glance
- what belongs in the visual versus in text on the slide

### 2. Deck design language

Use:
- deck-level style system
- palette
- mood
- image behavior
- framing rules
- consistency rules

Ask:
- what visual language should this slide inherit
- how polished, restrained, bold, or premium should it feel
- what kind of presentation world does this deck live in

### 3. Designer assets

Use:
- deck-level `designer_assets`
- slide-level `asset_refs`
- prepared image inputs, such as rendered old-slide previews, rendered `.pptx` template previews, or logo files
- asset `usage`, `placement`, and `required` flags

Ask:
- which assets apply to this slide
- whether each asset should be copied exactly, used as a loose reference, or used only for placement/style
- whether a required asset is missing and should block generation
- how to name each prepared input image in the prompt

### 4. Creative direction

Use:
- `creative_direction`
- `metaphor`
- `composition_intent`
- `prompt_notes`
- `avoid`
- any slide-level notes that materially affect the visual

Ask:
- what kind of concept should the model invent
- how much visual freedom should it have
- what clichés or failure modes should be excluded

### 5. Literal text and invariants

Use:
- slide `title`
- subtitle or key-message line
- labels, callouts, section names, and axis/category text that must appear
- computed footer text from `production_defaults.footer`, normally `CR` plus the simple slide-order page number, with no total slide count
- `preserve` or `text_rules` fields when present

Ask:
- which text must render exactly
- which text should be omitted from the visual and handled elsewhere
- which footer tokens must be allowed by the text lock and where they should sit
- what must not change across iterations: layout, palette, title zone, arrows, labels, framing, or reference-image geometry

## Prompt-writing style

For designer-mode generation, prefer prompts that are:
- concept-first
- presentation-aware
- organized in a consistent order: goal/use case, canvas/layout, required text, key visual details, style/materials, constraints
- visually specific where it matters
- open enough to allow strong model solutions
- explicit about preserve rules and forbidden extra text

Avoid prompts that are:
- just a raw YAML dump
- overloaded with literal slide-building instructions
- overly cinematic when the output is meant for a slide
- so rigid that the image becomes generic or lifeless
- vague about text placement, label accuracy, or what must stay fixed

## Recommended prompt structure

Use this structure when writing the final prompt.

```text
Create a real presentation slide image for a 16:9 business presentation, not a loose background illustration.

Slide intent:
<what the slide is trying to communicate in one or two sentences>

What the audience should understand at a glance:
<the key idea the slide must land quickly>

Required slide grammar:
- clear top title zone, usually top-left
- title should be short and fit in one or two lines
- optional compact key-message or support line below the title
- main visual body should carry the proof or concept
- composition should read cleanly in a horizontal / Z pattern

Deck design language:
- <mood>
- <style>
- <palette / tone>
- <overall level of polish>
- <consistency instruction>

Asset references:
- <Image 1 / asset id / type / usage / placement>
- <Image 2 / asset id / type / usage / placement>

Required text to render exactly:
- Title: "<exact title>"
- Support line: "<exact support line if used>"
- Labels: "<exact label 1>", "<exact label 2>", "<exact label 3>"
- Footer: "CR" at lower-left; "<page number>" at lower-right

Text rules:
- render only the listed text
- keep all text large enough for presentation use
- preserve quoted spelling, capitalization, and punctuation
- no extra headings, captions, watermarks, logos, numbers, or invented labels

Visual direction:
- <metaphor or concept>
- <what kind of scene / framework / object / system to depict>
- <what role the visual plays on the slide>
- <how open-ended the model can be>

Composition guidance for slide use:
- designed as a widescreen 16:9 slide
- preserve a credible title-safe area
- make the title/message area feel integrated, not floating randomly
- prioritize immediate readability in a presentation context
- presentation-grade, not merely cinematic or decorative
- compose natively for 16:9 rather than assuming the image will be cropped or reframed later

Avoid:
- <clichés>
- <wrong styles>
- <things that dilute the explanation>
- square, portrait, or poster-like compositions
- backgrounds that leave no believable room for the title and key message
- compositions that would only work after center-cropping or destructive reframing
```

## Reusable scaffold

```text
Create a real presentation slide image for a widescreen 16:9 slide, not a generic poster or background.

This slide communicates: {{slide_message}}
The title of the slide is: {{slide_title}}
The title should fit in {{title_line_limit}} lines.
{{key_message_line}}

The audience should immediately grasp: {{audience_takeaway}}

Use this deck design language:
{{deck_design_language}}

Use these prepared asset references:
{{asset_reference_block}}

Required text to render exactly:
{{required_text_block}}

Footer text to render exactly:
{{footer_text_block}}

Text rules:
- render only the listed text
- keep text large enough for presentation use
- preserve spelling, capitalization, punctuation, and line hierarchy
- do not invent extra headings, labels, watermarks, logos, numbers, or captions

The visual should support this slide role:
{{image_role}}

Important supporting context from the slide:
{{supporting_points}}

Creative direction:
{{creative_direction}}

Composition intent:
{{composition_intent}}

Slide-format requirements:
- preserve a clear title-safe zone in {{title_zone}}
- place the footer in the approved safe area: {{footer_placement}}
- keep the eye moving in this pattern: {{reading_path}}
- make the main visual body support the title and message rather than fight them
- the result should feel like a finished business slide, not an artwork waiting for later assembly
- the composition must work without later crop-rescue or forced aspect correction

Avoid:
{{avoid_list}}
```

## Translation guidance

When filling the scaffold:
- compress the slide text into visual meaning
- keep only the support points that matter to the image
- put exact title, support line, and labels in quoted form in the required-text block
- put computed footer tokens in quoted form in the footer-text block; default is `CR` and the slide number (`1`, `2`, `3`, ...)
- translate bullets into concepts, relationships, tensions, or systems
- preserve the deck style language without repeating unnecessary metadata
- include every relevant `designer_assets` / `asset_refs` item by id and usage
- describe prepared asset inputs by image number or filename when the image API receives them
- repeat preserve rules on each iteration when text, layout, or style consistency matters

## Text discipline

For slides with in-image text:
- use `quality="high"` for final generation
- quote exact strings instead of paraphrasing
- include computed footer text in the allowed text list
- keep the required text list short
- specify placement, hierarchy, and approximate size when legibility matters
- avoid asking for dense paragraphs, many small labels, or long tables inside a generated image
- if text accuracy is more important than visual richness, consider a hybrid workflow with editable PPT text

## Reference images and consistency

When a generated slide establishes the right deck style:
- save it as a durable reference candidate under `assets/generated/` or `assets/source/`
- if the API call supports image inputs for the chosen operation, reference it explicitly as `Image 1`
- describe how to use it: match style, palette, typography mood, spacing, hierarchy, or framing
- still repeat critical text and layout instructions; do not rely on "same style as before" alone
- do not use reference images to force a mismatched layout onto a slide with a different job

## Designer assets in prompts

Use `designer_assets` when the approved deck includes external visual inputs such as logos, brand guides, PowerPoint templates, screenshots, existing decks, rendered slide previews, icons, or reference images.

Before writing the prompt:
- resolve each slide `asset_refs` id against deck-level `designer_assets`
- prepare non-image assets as model-readable images, e.g. render `.pptx` templates and existing `.pptx`/`.pdf` decks to PNG previews
- stop if an asset has `required: true` and cannot be found or prepared
- assign clear input labels such as `Image 1: brand_logo`, `Image 2: existing_slide_previews`, and `Image 3: visual_template`
- record the same mapping in `method/model-inputs.yaml`

Prompt each asset narrowly:
- logos: whether to place the exact logo, where to place it, and how large it should feel
- PowerPoint templates: what to borrow, such as layout, density, typography, margins, or visual rhythm
- existing decks and slide previews: preserve message and key evidence, borrow useful visual rhythm, and redesign composition freely unless the approved brief says close redesign
- brand guides: what to follow, such as palette, type mood, icon style, or spacing
- screenshots/reference images: whether to reproduce, abstract, crop, or merely use as context

Do not let an asset override the slide message or text lock. If a template or old slide has placeholder text or outdated wording, explicitly tell the model not to copy it.

Default existing-slide redesign block:

```text
Image {n} is asset existing_slide_previews, a prepared preview of the original slide for this page.
Use it as a content-and-style reference: preserve the message, key evidence, and any essential relationship shown on the original slide.
Borrow useful density, visual rhythm, and brand cues, but redesign the composition freely so the new slide is more visual and presentation-ready.
Do not copy outdated wording, placeholder text, low-quality spacing, or cramped layout from the reference.
```

## Default visual template prompt block

When Rodrigo asks to "use my default template", pass `assets/visual-templates/default-slide.png` as `Image 1` and include this block in the prompt. For cover/title slides, use `assets/visual-templates/title-page.png` instead and adapt the wording to the cover layout.

```text
Image 1 is Rodrigo's default slide template reference.
Use Image 1 only for the white canvas, large bold title typography, title placement, spacious margins, and footer/page-number safe area.
Do not copy any placeholder text from Image 1.
Do not copy the dashed footer placeholder as a visible design element.

The body of the slide is intentionally open.
Create new body visuals, diagrams, metaphors, icons, and accent colors that fit this slide's message.
Keep the new body content inside the open white area below the title and above the footer so the generated slide works naturally inside the same deck template.
The result should feel compatible with Image 1's font scale and overall clean look, while the visual concept and colors can be invented for this specific slide.
```

## Standard footer block

Include this block in designer-mode prompts unless the approved deck.md disables the footer:

```text
Footer:
- Place a small "CR" mark in the lower-left corner.
- Place the simple slide number "{{page_number}}" in the lower-right corner.
- Do not include the total slide count; render "{{page_number}}", not "{{page_number}}/{{total_pages}}".
- Use the deck's muted footer style; keep both elements subtle and consistent.
- Keep the footer inside the safe area and away from logos, sources, charts, labels, and body content.
- These are the only extra text tokens allowed beyond the required text list.
```

## Iteration protocol

When a slide misses:
1. Diagnose one concrete issue, such as title too small, extra text, weak hierarchy, wrong metaphor, or off-brand palette.
2. Revise only the relevant prompt section.
3. Repeat preserve rules for exact text, layout, palette, title-safe area, and reference-image behavior.
4. Regenerate and compare against the prior output.
5. Replace the accepted output only after visual review.

## Review-change prompt protocol

Use this when the human asks for changes after seeing a rendered slide or deck.

Inputs:
- previous approved deck.md
- new review deck.md with `## Revision Brief`
- prior rendered slide image when available
- old slide spec
- updated slide spec
- exact human change request

The prompt should say:
- this is a targeted revision, not a new slide
- what changed in the approved spec
- what must be preserved from the prior rendered slide
- whether logo placement, template reference, text lock, palette, title zone, or composition should stay fixed
- that only the requested elements should change

Reusable review-change block:

```text
This is a targeted revision of an already approved slide, not a new slide.

Previous rendered slide:
<Image 1 or filename, if available>

Human change request:
{{human_change_request}}

Old slide spec summary:
{{old_slide_spec_summary}}

Updated slide spec summary:
{{updated_slide_spec_summary}}

Change only:
{{exact_delta}}

Preserve:
- approved composition and reading path unless listed in the change request
- approved title zone, palette, typography mood, and safe margins
- approved logo/template/reference asset behavior unless listed in the change request
- all required text not listed in the change request

Return a revised 16:9 presentation slide that implements only the requested delta.
```

## Freedom dial

Use three levels of freedom.

### Tight

Use when:
- the user wants close composition control
- the slide has a very specific visual role
- the image must fit a narrowly defined space

Behavior:
- specify structure more tightly
- reduce invention range
- make layout intent more explicit

### Balanced

Default.

Use when:
- the slide needs clear direction but benefits from model creativity

Behavior:
- specify the concept and role clearly
- leave the exact visual solution open

### Loose

Use when:
- the user wants surprise
- the goal is a strong conceptual visual rather than precise placement

Behavior:
- emphasize mood, metaphor, and visual ambition
- avoid over-specifying objects or composition
- still anchor the prompt in the slide message

## Example

Input idea:
- message: The business works as an integrated system
- role: premium concept visual for the right side of the slide
- mood: intelligent, modern, high-trust
- metaphor: interconnected system, but not cheesy gears

Derived prompt:

```text
Create a presentation-grade visual for a 16:9 slide.

This slide communicates that the business works as an integrated system rather than a loose collection of departments. The audience should immediately understand coordinated interdependence across functions.

Use a premium consulting-style design language: modern, intelligent, restrained, high-trust, clean composition, visually strong but not flashy.

Create a conceptual visual that suggests interconnected operations, technology, and commercial decisions reinforcing one another. Avoid literal stock diagrams or cliché gears. The image should feel like a coherent operating system with elegant interdependence, suitable for the hero visual area of a business presentation slide.

Leave enough compositional discipline for slide use. The result should be clear, presentation-grade, and immediately legible rather than cinematic for its own sake.

Avoid cheesy 3D gears, dashboard clutter, generic corporate stock imagery, and decorative sci-fi overlays.
```

## Guardrails

- do not drift into a hybrid workflow unless the user explicitly approved it
- do not ask the image model for a background plate when the requested output is the slide itself
- do not rely on downstream cropping, squeezing, or rescue framing as part of the normal workflow
- do not blindly copy every field from the slide spec
- do not use an undeclared logo, template, or reference asset in designer mode
- do not ignore required designer assets
- do not ask for a full redesign when the human requested a targeted review change
- do not let art direction overpower communication
- do not let the prompt drift away from the slide message
- do not use decorative prompts that could apply to any slide in any deck
