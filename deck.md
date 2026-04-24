---
# deck.md — your deck brief.
#
# Fill this in; hand it to the agent. It produces the slides.
# Meant to be read and edited by humans, and parsed by agents.
# Minimum required: deck.title (below), a ## Narrative section, and at least one slide.
# Everything else is optional. For a stripped-down starter, see deck.minimal.md.

schema_version: deck-md/v2-alpha

deck:
  title:     "<your deck title>"
  objective: "<what you want this deck to achieve — a decision, action, alignment>"
  audience:  "<who will see it>"
  language:  en
  author:    "<your name or team>"

# Narrative shape: how the argument is structured.
#   pyramid          — governing thought + key line + supporting slides  (default)
#   scr              — Situation / Complication / Resolution             (short decks)
#   problem-solution — Problem / Solution / Why now                      (pitches)
#   update           — Plan / Actual / Next                              (status, retros)
narrative_template: pyramid

# Output: designer-mode generates each slide as an image via gpt-image-2, using
# the narrative and design tokens below. A slide can opt out with `mode: ppt-shapes`
# when it's simple enough that generation isn't worth the cost.
production_defaults:
  default_slide_mode: ppt-shapes          # ppt-shapes | designer-mode
  aspect_ratio: "16:9"
  # default_visual_template: assets/visual-templates/default-slide.png

# image_generation is only used for slides with mode: designer-mode.
# Remove this block if your deck has no designer-mode slides.
image_generation:
  primary_creator: gpt-image-2
  size:            "2560x1440"
  quality:         high
  output_format:   png

# Design tokens drive the look and feel. Edit these to change the deck's aesthetic.
design_tokens:
  palette:
    primary:     "#111111"     # titles, body text
    secondary:   "#5B5B5B"     # subtitles, secondary text
    accent:      "#2F6BFF"     # emphasis, callouts
    accent_soft: "#DCE7FF"     # backgrounds for highlights
    background:  "#FFFFFF"
    line:        "#B8C7E6"
  typography:
    title: "Inter 600"
    body:  "Inter 400"
  shape_language:
    corner_style: subtle        # subtle | sharp | rounded
    line_weight:  medium        # light | medium
  iconography:
    family: tabler-outline
---

# <Your deck title>

## What this deck is for

<!-- Human-facing framing. This section is for you and any co-authors — not parsed by the agent.
     Cover: who the audience is, what you want from them by the end (a decision, approval, action),
     and the tone the deck should carry. Two or three sentences is enough. -->

<Audience context, objective, tone.>

## Narrative

<!-- Agent-facing logic. This is the argument structure the agent uses to validate and produce slides.
     "What this deck is for" says what you want; this section says how the argument is built.
     They are complementary: one is framing, the other is proof. -->

<The deck's logical spine. This is the `pyramid` template — a governing thought, a narrative arc, and the argument structure that supports it. For other templates (`scr`, `problem-solution`, `update`), see [`./standards/narrative-templates.md`](./standards/narrative-templates.md).>

```yaml
question: "<the core question the deck answers — what the audience is asking, or should be asking>"
governing_thought: "<the logical apex — the precise, evidenced answer that the key_line arguments prove>"

# Narrative arc — how the argument unfolds.
# resolution echoes governing_thought but is written as a plain-language close for human readers.
# If they conflict, governing_thought wins — it is what the deck proves.
situation:    "<context the audience already accepts as true>"
complication: "<what's wrong, what changed, what's at stake>"
resolution:   "<what you're recommending>"

# Argument structure — how the resolution is proven.
# Each argument is a MECE claim; supporting_slides are the slides that prove it.
# Reading only the action titles of the supporting slides should reproduce each argument.
key_line:
  - argument: "<argument 1 — a claim that supports the governing thought, as a full sentence>"
    supporting_slides: [3, 4]
  - argument: "<argument 2>"
    supporting_slides: [5, 6]
  - argument: "<argument 3>"
    supporting_slides: [7, 8]

mece_check: "<one line on why these arguments together prove the governing thought, with no overlap and no missing piece>"
```

## Design

<A sentence or two on the visual mood you want — decisive, calm, serious, optimistic, urgent. What feeling should the audience carry away from each slide? The concrete palette, typography, and shape language are set in `design_tokens` in the frontmatter above.>

### Consistency
- <Slide-type patterns specific to this deck: e.g. section dividers use full-bleed accent>
- <Title treatment: e.g. titles top-left, max two lines>
- <Chart style: e.g. always use accent color for the highlighted series>
- <Anything else>

### Avoid
- <Visual anti-patterns specific to this deck: e.g. cinematic photography, decorative gradients, dashboard clutter, stock-image energy>

## Slides

Each slide is one `### Slide N — "action title"` heading, followed by a small YAML metadata block and a body that proves the title. Titles are full sentences in sentence case, no trailing period.

**Horizontal logic.** Reading only the action titles of all your slides should reproduce the deck's argument. If it doesn't, either the titles or the argument structure above needs work.

**Output mode.** Default is `designer-mode` — each slide becomes a generated image. The agent infers a reasonable composition from the action title, body, and design tokens. For finer control on a specific slide, add a `creative_direction` and `required_text` block (see Slide 4). For simple text-only slides that don't need generation, opt out with `mode: ppt-shapes`.

Valid `type` values are listed in [`./standards/slide-archetypes.md`](./standards/slide-archetypes.md).

---

### Slide 1 — "<action title: restates the governing thought as a takeaway>"

<!-- Validation rules (agent self-checks before emitting):
     Title: full sentence with verb, sentence case, no trailing period, ≤14 words
     Body:  ≤5 bullets, ≤12 words per bullet, one idea per slide
     See standards/deck-validation.md for the full checklist. -->

```yaml
id: 1
type: executive_summary
```

<Body — typically three bullets matching situation / complication / resolution. This slide IS the governing thought in visible form.>

**Sources:** <optional>

---

### Slide 2 — "<action title>"

```yaml
id: 2
type: situation
```

<Body — establish what the audience already accepts.>

---

### Slide 3 — "<action title — supports argument 1 from the key line>"

```yaml
id: 3
type: analysis
```

<Body — the evidence that proves argument 1. A few bullets or a short paragraph.>

---

### Slide 4 — "<action title — a slide with fine-grained visual control>"

<This slide shows how to add explicit `creative_direction` and `required_text`. Use these when you want to dictate the metaphor, composition, or the exact text that appears in the generated image. Leave them off when the narrative and design tokens are enough for the agent to produce a good slide on its own.>

```yaml
id: 4
type: recommendation
image_decision: full-generated-visual     # none | icon-only | cutout | full-generated-visual
```

<Body — what the slide communicates in words.>

```yaml
creative_direction:
  mood: "<one or two words>"
  metaphor: "<the visual idea — e.g. three parallel tracks, a rising curve, a cross-section>"
  composition_intent: "<how the visual should be composed on the slide>"
  prompt_notes:
    - "<specific guidance for gpt-image-2>"
  avoid:
    - "<anti-patterns, e.g. photographic imagery, cinematic lighting>"

required_text:
  title: "<exact title as it should appear in the image>"
  labels:
    - "<label 1>"
    - "<label 2>"
```

---

## Notes to the agent

<Freeform context the agent should know but that doesn't fit above: deadlines, reviewers, data file locations, related decks, things to double-check, constraints on output.>

---

## References

- [`./SPEC.md`](./SPEC.md) — the `deck.md` specification
- [`./standards/narrative-templates.md`](./standards/narrative-templates.md) — narrative template reference
- [`./standards/slide-archetypes.md`](./standards/slide-archetypes.md) — slide type catalog
- [`./standards/deck-validation.md`](./standards/deck-validation.md) — hard rules the agent self-checks
- [`./standards/image-prompts.md`](./standards/image-prompts.md) — gpt-image-2 prompt templates
- [`./examples/scr.deck.md`](./examples/scr.deck.md) — minimal filled SCR example
- [`./examples/pyramid.deck.md`](./examples/pyramid.deck.md) — full pyramid example
- [`./examples/problem-solution.deck.md`](./examples/problem-solution.deck.md) — pitch deck example
- [`./examples/update.deck.md`](./examples/update.deck.md) — status update example
