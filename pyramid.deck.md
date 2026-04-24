---
schema_version: deck-md/v2-alpha

deck:
  title:     "2026 growth recovery plan"
  objective: "Secure board approval for Q1 investment"
  audience:  "Board of directors"
  language:  en
  author:    "Strategy team"
  version:   v2

narrative_template: pyramid

production_defaults:
  default_slide_mode: designer-mode
  aspect_ratio: "16:9"
  default_visual_template: assets/visual-templates/default-slide.png

image_generation:
  primary_creator: gpt-image-2
  size:            "2560x1440"
  quality:         high
  output_format:   png

design_tokens:
  palette:
    primary:     "#111111"
    secondary:   "#5B5B5B"
    accent:      "#2F6BFF"
    accent_soft: "#DCE7FF"
    background:  "#FFFFFF"
    line:        "#B8C7E6"
  typography:
    title: "Inter, 600"
    body:  "Inter, 400"
  shape_language:
    corner_style: subtle
    line_weight:  medium
  iconography:
    family: tabler-outline
---

# 2026 growth recovery plan

## What this deck is for

Present the Q3 2025 growth slowdown to the board, show that the cause is acquisition (not retention), and secure approval for $4M of Q1 investment across three levers. Tone is decisive and evidence-backed; the audience is technical but time-constrained, so every slide must read top-down in 20 seconds.

## Narrative

```yaml
question: "How do we restore growth to 20%+ by end of Q2 2026?"
governing_thought: "Three levers — organic, paid mix, reactivation — will recover growth in two quarters at $4M investment."

situation:    "Growth is our #1 KPI. Board committed to 20% YoY in 2026."
complication: "Q3 2025 growth fell 34% YoY. Acquisition, not retention, is the cause."
resolution:   "Rebuild organic, rebalance paid mix, reactivate dormant users."

key_line:
  - argument: "Organic channel collapsed; content engine can restore 30% channel share by Q2"
    supporting_slides: [3, 4, 5]
  - argument: "Paid mix is over-concentrated in Meta; reallocation recovers 15% of lost CAC"
    supporting_slides: [6, 7]
  - argument: "180-day dormant cohort is large and responsive to lifecycle campaigns"
    supporting_slides: [8, 9]

mece_check: "The three levers cover the acquisition funnel (organic) + paid mix + reactivation. At our scale there is no fourth growth channel, and no overlap between levers."
```

## Design

Decisive and forward-looking. Strong accent color on recommendations, restrained typography, high whitespace. Every slide must be readable from the back of a 20-person boardroom.

### Consistency
- Section dividers use full-bleed accent color with white title
- Chart emphasis always uses `accent`; de-emphasis in `secondary`
- Action titles top-left, max two lines, sentence case
- Three-column slides use equal-weight columns with tabler icons anchoring each block

### Avoid
- Cinematic or photographic imagery of any kind
- Decorative gradients or full-bleed background plates
- Dashboard-style multi-metric clutter

## Slides

### Slide 1 — "Three levers will recover growth in two quarters at $4M"

```yaml
id: 1
type: executive_summary
layout: three-column-scr
image_decision: full-generated-visual
```

**Situation.** Growth is our #1 KPI; board committed to 20% YoY in 2026.
**Complication.** Q3 growth fell 34% YoY — acquisition broke, not retention.
**Resolution.** Three levers — organic, paid mix, reactivation — recover growth in two quarters at $4M.

```yaml
creative_direction:
  mood: decisive, assured
  metaphor: three parallel tracks rising from left to right
  composition_intent: title top-left; three equal-weight columns below, each with icon + label + short caption
  prompt_notes:
    - flat design; no photography
    - preserve white background
    - tabler-outline icons above each column label
  avoid:
    - cinematic or gradient backgrounds
    - drop shadows or heavy depth

required_text:
  title: "Three levers will recover growth in two quarters at $4M"
  labels:
    - "Rebuild organic"
    - "Rebalance paid mix"
    - "Reactivate dormant users"
```

**Sources:** Internal funnel dashboard Q3 2025; board commitments 2025-09-12
**Speaker notes:** Land the governing thought in the first 30 seconds. Don't walk through the body — that's what the rest of the deck is for.

---

### Slide 3 — "Growth stalled because acquisition, not retention, broke"

```yaml
id: 3
type: analysis
layout: chart-left-text-right
mode: ppt-shapes                          # charts render better as shapes than generated images
image_decision: none
```

**Body**
- New-user signups fell 34% YoY while retention held flat
- Paid-channel CAC rose 2.1× across Q2–Q3
- Organic traffic share dropped from 42% to 19%

```yaml
chart:
  type: stacked-bar
  emphasis: "Acquisition decline, not retention"
  data_ref: ./data/signups_by_channel.csv
  annotation: "Paid-channel CAC doubled"
```

**Sources:** Internal funnel dashboard Q3 2025; Google Analytics
**Speaker notes:** Anchor by contrasting with the retention cohort slide that follows.

---

### Slide 7 — "Three levers will recover growth in two quarters"

```yaml
id: 7
type: recommendation
layout: horizontal-three-column
image_decision: full-generated-visual
visual_template_reference: assets/visual-templates/default-slide.png
visual_template_scope: preserve title placement, margins, footer
```

**Body**
- **Rebuild organic** — ship the content engine; target 30% channel share by Q2
- **Rebalance paid mix** — cut Meta by 40%, reallocate to search and partnerships
- **Reactivate dormant users** — lifecycle campaign targeting the 180-day inactive cohort

```yaml
creative_direction:
  mood: decisive, forward-looking
  metaphor: three distinct levers or tracks
  composition_intent: equal-weight three-column with tabler icons anchoring each block
  prompt_notes:
    - keep white background
    - line-weight medium, corner style subtle
    - icons sit above, not beside, the labels
  avoid:
    - cinematic lighting
    - photographic imagery
    - decorative backgrounds

required_text:
  title: "Three levers will recover growth in two quarters"
  labels:
    - "Rebuild organic"
    - "Rebalance paid mix"
    - "Reactivate dormant users"
```

**Sources:** Strategy working session, Oct 2025
**Speaker notes:** Pace this slowly — each lever gets its own body slide after.

---

## Notes to the agent

- Board meeting is Dec 15; final deck must be ready by Dec 8 for internal review.
- Data files live in `./data/`; primary source is `signups_by_channel.csv`.
- Slides 4–6, 8, 9 follow the pattern of slides 3 and 7. The agent should produce them following the three-argument structure in the key line.
- Primary reviewer: CFO. Secondary: Head of Growth.
