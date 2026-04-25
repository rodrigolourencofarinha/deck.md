---
schema_version: deck-md/v2-alpha

status: draft

deck:
  title:    "<your deck title>"
  audience: "<who will see it>"
  language: en

narrative_template: scr    # scr | pyramid | problem-solution | update

production_defaults:
  default_slide_mode: designer-mode
  aspect_ratio: "16:9"
  footer:
    page_numbers: true
    page_number_format: "{page}"
    cr_mark: true
    cr_text: "CR"
    placement: bottom-left-cr-bottom-right-page

image_generation:
  model: gpt-image-2
  primary_auth: codex-oauth
  fallback_auth: openai-api-key
  fallback_requires_user_approval: true
  size: "2560x1440"
  quality: high
  output_format: png

# Optional: declare every asset the visual model should receive.
# Delete unused examples before approval.
designer_assets:
  - id: brand_logo
    type: logo
    path: assets/source/logo.png
    usage: "Place exact logo on slides where referenced"
    scope: deck
    placement: top-right
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
    path: assets/source/default-slide-template.png
    usage: "Use as title, margin, typography, and footer-safe-area reference; do not copy placeholder text"
    scope: deck
    required: false
---

# <Your deck title>

## Narrative

```yaml
situation:    "<context the audience already accepts>"
complication: "<what's wrong or at stake>"
resolution:   "<what you're recommending>"
```

## Slides

### Slide 1 — "<action title>"

```yaml
id: 1
type: situation
```

### Slide 2 — "<action title>"

```yaml
id: 2
type: complication
```

### Slide 3 — "<action title>"

```yaml
id: 3
type: recommendation
```
