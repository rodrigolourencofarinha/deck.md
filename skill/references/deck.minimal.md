---
schema_version: deck-md/v2-alpha
status: draft

deck:
  title: "<your deck title>"
  audience: "<who will see it>"
  language: en

narrative_template: scr

production_defaults:
  default_slide_mode: designer-mode
  aspect_ratio: "16:9"
  footer:
    page_numbers: true
    page_number_format: "{page}"
    cr_mark: true
    cr_text: "CR"
    placement: bottom-left-cr-bottom-right-page
---

# <Your deck title>

## Narrative

```yaml
situation: "<context the audience already accepts>"
complication: "<what changed, broke, or is at stake>"
resolution: "<what you recommend or want the audience to do>"
```

## Slides

### Slide 1 - "<action title>"

```yaml
id: 1
type: situation
```

<Body that proves the title. Keep it short.>

### Slide 2 - "<action title>"

```yaml
id: 2
type: complication
```

<Body that proves the title.>

### Slide 3 - "<action title>"

```yaml
id: 3
type: recommendation
```

<Body that proves the title.>

## Notes to the agent

Use this as the quick-start brief. Keep `status: draft` until the human approves production.
If the request includes data, SQL, CSV/Excel, metrics, or analysis, create `data/` and `analysis/` artifacts first, then reference them in `analysis_artifacts` before approval.
Each slide must have one clear takeaway. Use charts only when they are the simplest proof of that takeaway.
For the richer template with designer assets, revision briefs, design tokens, and detailed generated-image controls, see `deck.full.md`.
