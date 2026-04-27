---
schema_version: deck-md/v2-alpha
status: draft

deck:
  title: "Pipeline recovery example"
  objective: "Show how data analysis becomes a consulting storyline"
  audience: "Revenue leadership"
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

analysis_artifacts:
  manifest: analysis/manifest.yaml
  notes: analysis/notes.md
  queries:
    - id: pipeline_extract
      path: analysis/queries/pipeline_extract.sql
  tables:
    - id: pipeline_by_segment
      path: data/analysis/pipeline_by_segment.csv
      kind: analysis
      used_by_slides: [2]
      required_columns: [segment, revenue_gap]
    - id: chart_segment_gap
      path: data/charts/segment_gap.csv
      kind: chart
      used_by_slides: [2]
      required_columns: [segment, revenue_gap]
---

# Pipeline recovery example

## Brief

```yaml
input_type: content
input_summary: "Illustrative pipeline export and SQL note for a revenue gap analysis."
interpretation: "Chose SCR because the deck needs to move from current gap to one focused recovery action."
model_inputs: []
open_questions:
  - "Confirm whether renewals should be excluded from the source export"
```

## Narrative

```yaml
situation: "Revenue leadership needs a short readout on the pipeline gap."
complication: "The gap is concentrated enough to require focus, not a broad campaign."
resolution: "Prioritize enterprise conversion and move secondary diagnostics to appendix."
```

## Slides

### Slide 1 - "Pipeline recovery example"

```yaml
id: cover
type: cover
layout: title-page
```

Revenue leadership | Illustrative data-to-deck workflow

### Slide 2 - "Enterprise conversion is the recovery priority"

```yaml
id: 1
type: executive_summary
```

**Body**
- Enterprise explains the largest shortfall
- Smaller segments matter, but do not change the decision
- The next step is a focused conversion sprint

**Sources:** Illustrative pipeline export, refreshed 2026-04-25

### Slide 3 - "Enterprise accounts explain most of the revenue gap"

```yaml
id: 2
type: chart
mode: ppt-shapes
layout: chart-left-text-right
```

**Body**
- Enterprise has the largest and most actionable gap
- Mid-market is secondary evidence, not a second storyline
- SMB is too small to drive the plan

```yaml
chart:
  type: bar
  emphasis: "Enterprise accounts explain most of the revenue gap"
  data_ref: data/charts/segment_gap.csv
  annotation: "Focus the recovery motion where the gap is largest"
```

**Sources:** Illustrative pipeline export; see analysis/manifest.yaml

### Slide 4 - "A focused sprint can recover the gap faster"

```yaml
id: 3
type: recommendation
```

**Body**
- Assign enterprise owners this week
- Review blockers by stage
- Move diagnostics that do not change the decision to appendix

**Sources:** analysis/notes.md

## Notes to the agent

This example demonstrates the analysis-first contract. Do not produce slides until the human approves the draft.
