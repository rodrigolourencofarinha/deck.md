---
schema_version: deck-md/v2-alpha

deck:
  title:     "Engineering — Q3 status update"
  objective: "Align leadership on Q3 delivery, risks, and Q4 commitments"
  audience:  "Exec leadership team"
  language:  en
  author:    "Engineering leadership"

narrative_template: update

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
    primary:     "#111111"
    secondary:   "#5B5B5B"
    accent:      "#2F6BFF"
    accent_soft: "#DCE7FF"
    background:  "#FFFFFF"
    line:        "#B8C7E6"
  typography:
    title: "Inter 600"
    body:  "Inter 400"
  shape_language:
    corner_style: subtle
    line_weight:  medium
  iconography:
    family: tabler-outline
---

# Engineering Q3 status update

## What this deck is for

Quarterly leadership review. Report honestly on what we committed to, what we shipped, what slipped, and what comes next. Tone: direct, no spin. Leadership has heard the stories behind every number; this is the summary.

## Narrative

```yaml
plan:   "Ship 3 flagship features, reduce infra tech debt by 30%, hit 99.9% uptime."
actual: "Shipped 2 of 3 features (Insights delayed 3 weeks); reduced tech debt by 40%; hit 99.87% uptime."
next:   "Close Insights by Oct 15, scale infra for Q4 launches, begin 2026 platform planning."
```

## Design

Mood: matter-of-fact. Status decks fail when they feel defensive; keep titles as facts, use color to flag risk rather than emotion, and never bury what went wrong.

### Consistency
- Status icons: green check for on-track, yellow dot for at-risk, red square for off-track.
- Every slide shows the commitment alongside the actual — no claim without the baseline.
- Numbers are bold; commentary is regular weight.

### Avoid
- Phrases like "despite challenges" or "as expected."
- Deep dives into individual incidents — link to postmortem docs instead.
- Victory-lap slides that only show what went well.

## Slides

---

### Slide 1 — "On track overall — Insights delayed three weeks; all other Q3 commitments met or exceeded"

```yaml
id: 1
type: executive_summary
mode: ppt-shapes
```

**Body**
- 2 of 3 features shipped; Insights on track for Oct 15
- Tech debt reduction: 40% (goal: 30%)
- Uptime: 99.87% (goal: 99.9% — 3 minutes over SLO)

**Speaker notes:** Land the headline honestly. The one miss (uptime) is a rounding-error miss; don't oversell recovery.

---

### Slide 2 — "Features: shipped Dashboards and Exports; Insights slipped on data-model scope"

```yaml
id: 2
type: analysis
mode: ppt-shapes
```

**Body**
- **Dashboards** — shipped Sept 12, adoption 41% in week 1 (target 30%)
- **Exports** — shipped Sept 28, adoption climbing, no incidents
- **Insights** — delayed to Oct 15; underestimated data-model migration complexity

**Speaker notes:** The Insights miss is a scoping failure, not an execution one. The plan for Q4 addresses scoping explicitly.

---

### Slide 3 — "Reliability: 99.87% uptime — three minutes over SLO from one incident"

```yaml
id: 3
type: analysis
mode: ppt-shapes
```

**Body**
- Single incident: database failover on Sept 3 (23 min)
- All other months: above 99.95%
- Root cause addressed in postmortem — see [link]

```yaml
chart:
  type: line
  emphasis: "September 3 incident is the only deviation"
  data_ref: ./data/uptime_by_day_q3.csv
```

---

### Slide 4 — "Tech debt: infra modernization 40% complete — two quarters ahead of plan"

```yaml
id: 4
type: analysis
image_decision: icon-only
```

<Body: what was retired, what was migrated, what the velocity impact has been.>

- Retired: legacy auth service, v1 event pipeline
- Migrated: primary data store to new cluster
- Developer velocity up 18% on migrated services

---

### Slide 5 — "Q4 commitments: close Insights, scale for launches, begin 2026 planning"

```yaml
id: 5
type: next_steps
mode: designer-mode
image_decision: full-generated-visual
```

**Body**
- **Close Insights** by Oct 15 — no scope additions
- **Scale infra** for the three marketing launches (Nov 5, Nov 18, Dec 2)
- **Begin 2026 planning** — platform architecture review kicks off Oct 28

```yaml
creative_direction:
  mood: focused, forward
  metaphor: three milestones on a timeline
  composition_intent: horizontal timeline with three equally-spaced markers
  prompt_notes:
    - use accent color only for the milestone markers
    - label each milestone with date and one-line description
  avoid:
    - decorative gradients
    - extra marketing flourishes

required_text:
  title: "Q4 commitments: close Insights, scale for launches, begin 2026 planning"
  labels:
    - "Oct 15 — Insights ships"
    - "Nov 5–Dec 2 — launches"
    - "Oct 28 — 2026 planning begins"
```

---

## Notes to the agent

- Uptime number must match the value in `./data/uptime_by_day_q3.csv` exactly.
- Do not include incident details; those live in `/postmortems/2025-09-03.md`.
- Reviewed by: VP Eng, CTO before the Oct 8 leadership meeting.
