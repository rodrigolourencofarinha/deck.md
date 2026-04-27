---
schema_version: deck-md/v2-alpha

deck:
  title:     "Reviewr — AI-assisted code review for engineering teams"
  objective: "Secure a 30-day pilot with 10 engineers"
  audience:  "VP Engineering at a 200-person SaaS company"
  language:  en
  author:    "Reviewr founding team"

narrative_template: problem-solution

production_defaults:
  default_slide_mode: designer-mode       # designer-mode | ppt-shapes
  aspect_ratio: "16:9"
  footer:
    page_numbers: true
    page_number_format: "{page}"
    cr_mark: true
    cr_text: "CR"
    placement: bottom-left-cr-bottom-right-page

image_generation:
  primary_creator: gpt-image-2
  size:            "2560x1440"
  quality:         high
  output_format:   png

design_tokens:
  palette:
    primary:     "#0B0B0F"
    secondary:   "#5B5B5B"
    accent:      "#7C5CFF"
    accent_soft: "#EEE8FF"
    background:  "#FFFFFF"
    line:        "#D5CCEB"
  typography:
    title: "Söhne Kräftig"
    body:  "Söhne Buch"
  shape_language:
    corner_style: rounded
    line_weight:  medium
---

# Reviewr

## What this deck is for

Eng leaders know code review is slow and inconsistent, but they've been burned by "AI review" tools that just grep for lint. We want a 30-day pilot — enough time to show quantified reviewer-time savings and catch-rate data on real PRs. Tone: confident, technical, and honest about limitations.

## Narrative

```yaml
problem:  "Senior engineers spend 8+ hours a week on code review, quality varies wildly by reviewer, and bugs still ship."
solution: "Reviewr pre-reviews every PR — flagging the 80% of issues that don't need a human, so human review focuses on design and logic."
why_now:  "Model capability just crossed the threshold for reliable review; cost per review dropped 20× in 18 months."
```

## Design

Mood: confident and unflashy. Engineers distrust marketing polish, so keep it dense with information and honest about what's uncertain. Purple accent signals AI-native without feeling like a pitch deck.

### Consistency
- Code snippets in slides use a monospace font and the same dark-gray background as the docs site.
- Screenshots of the product use a 4px radius frame with a 1px border in `line` color.
- Every claim that cites a number must show the source on the same slide.

### Avoid
- Stock imagery of developers at laptops.
- Abstract "AI brain" imagery.
- Vague phrases like "revolutionary" or "game-changing."

## Slides

---

### Slide 1 — "Reviewr — AI-assisted code review for engineering teams"

```yaml
id: cover
type: cover
layout: title-page
mode: designer-mode
```

30-day pilot proposal | VP Engineering

---

### Slide 2 — "Your best engineers spend a day a week on review — and bugs still ship"

```yaml
id: 1
type: situation
mode: designer-mode
image_decision: full-generated-visual
```

<Body opens with the pain your audience already feels. Prove the title with two data points: average review hours, and escaped-defect rate.>

```yaml
creative_direction:
  mood: serious, knowing
  metaphor: a stack of PRs, the top ones annotated
  composition_intent: left half shows the stack; right half shows the two statistics
  prompt_notes:
    - use accent color for the stat callouts only
    - keep monospace feel on the PR annotations
  avoid:
    - any photographic imagery of people

required_text:
  title: "Your best engineers spend a day a week on review — and bugs still ship"
  labels:
    - "8+ hrs/week per senior"
    - "1 in 12 PRs ships a regression"
```

**Sources:** Stack Overflow Dev Survey 2024; GitClear State of the Codebase 2024

---

### Slide 3 — "Quality varies 3× between reviewers — so you can't staff your way out"

```yaml
id: 2
type: complication
```

<Body: data on reviewer-to-reviewer catch-rate variance. Make the point that hiring more reviewers doesn't fix inconsistency, it compounds it.>

---

### Slide 4 — "Reviewr pre-reviews every PR before a human opens it"

```yaml
id: 3
type: recommendation
mode: designer-mode
image_decision: full-generated-visual
```

<Body: the core product loop in three steps. PR opens → Reviewr analyzes → human sees the curated findings.>

```yaml
creative_direction:
  mood: clear, mechanical
  metaphor: three-step pipeline flowing left to right
  composition_intent: horizontal flow diagram; each step has a short label underneath
  prompt_notes:
    - use accent color for the middle step (the Reviewr layer)
    - thin arrows between steps
  avoid:
    - 3D effects or gradients

required_text:
  title: "Reviewr pre-reviews every PR before a human opens it"
  labels:
    - "PR opens"
    - "Reviewr analyzes"
    - "Human reviews what matters"
```

---

### Slide 4 — "Why now: capability is up, cost is down, and the data is on your disk"

```yaml
id: 4
type: analysis
mode: ppt-shapes
```

**Body**
- Code review benchmark accuracy: 61% (2023) → 84% (Q3 2025)
- Cost per 10k-line review: $14 (2023) → $0.70 (Q3 2025)
- Your PRs, style guide, and prior review decisions all already exist as training signal

**Sources:** SWE-Bench Review subset; internal benchmark on public OSS PRs

---

### Slide 5 — "The ask: 30 days, 10 engineers, one repo"

```yaml
id: 5
type: next_steps
mode: ppt-shapes
```

**Body**
- Pick one repo with steady PR volume
- 10 engineers opt in for 30 days
- We instrument: reviewer-hours per PR, catch rate, false-positive rate
- Decision gate at day 30: continue or stop, your call

---

## Notes to the agent

- The audience has seen many AI pitch decks. Weight the deck toward evidence and concrete asks; strip anything that reads as hype.
- Leave space on the Slide 3 generated visual for a demo recording to be embedded later.
