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
