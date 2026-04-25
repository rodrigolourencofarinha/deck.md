# Data analysis workflow

Use this reference when a deck request includes raw data, CSV/Excel files, SQL, database exports, metrics, benchmark results, or asks the agent to "analyze", "interpret", "find the rationale", or "build the story from the data".

The goal is not to make a chart inventory. The goal is to create a clear consulting argument where every table, chart, and number supports a slide takeaway.

## Core rule

Data work happens before `deck.md` approval:

1. Preserve the source data.
2. Profile the data and state the grain, scope, units, and caveats.
3. Create derived CSVs for analysis and chart use.
4. Write the interpretation and candidate storyline.
5. Draft `deck.md` with links to the analysis artifacts.
6. Ask the human to approve `deck.md` before slide production.

Do not produce slides directly from a spreadsheet, query, or chat prompt. The approved `deck.md` must point to the data artifacts that support the deck.

## Standard folders

```text
decks/<deck-slug>/
  data/
    source/      # raw files, exports, or user-supplied CSVs
    working/     # intermediate cleaned files
    analysis/    # derived analysis tables
    charts/      # small CSVs ready for chart.data_ref
  analysis/
    queries/     # SQL files or query notes
    notes.md     # findings, caveats, and storyline logic
    manifest.yaml
  specs/
    YYYY-MM-DD-v01-deck.md
```

For a one-off deck in a flat folder, the same relative layout can sit next to `deck.md`:

```text
data/source/
data/analysis/
data/charts/
analysis/queries/
analysis/notes.md
analysis/manifest.yaml
deck.md
```

## Intake

When the user provides data:

- Save raw files unchanged in `data/source/` when the workspace allows file management.
- If the data is external and cannot be copied, record the source path or URL in `analysis/manifest.yaml`.
- If the input is SQL, save the query in `analysis/queries/` and save query results as CSV under `data/analysis/`.
- If database credentials or access are missing, stop and ask for a connection, export, or sample. Do not invent results.
- Record refresh date, filters, geography, period, unit, currency, and sample restrictions when known.

## Analysis outputs

Create files that are small, inspectable, and named for their role:

- `data/analysis/<question-or-metric>.csv` for evidence tables.
- `data/charts/<slide-or-claim>.csv` for chart-ready data.
- `analysis/notes.md` for interpretation and caveats.
- `analysis/manifest.yaml` for traceability.

The chart-ready CSV should contain only the columns the chart needs. Keep fuller analysis tables in `data/analysis/`.

## Manifest schema

```yaml
input_files:
  - id: raw_pipeline
    path: data/source/pipeline_export.csv
    description: "Raw pipeline export"
    grain: "opportunity"
    refreshed_at: "2026-04-25"

questions:
  - "Where is conversion slowing?"
  - "Which segment explains the revenue gap?"

transformations:
  - "Filtered to FY2026 open and closed opportunities"
  - "Grouped by segment and stage"

output_tables:
  - id: pipeline_by_segment
    path: data/analysis/pipeline_by_segment.csv
    grain: "segment"
    used_by_slides: [2]
  - id: chart_segment_gap
    path: data/charts/segment_gap.csv
    grain: "segment"
    used_by_slides: [3]

queries:
  - id: pipeline_extract
    path: analysis/queries/pipeline_extract.sql

claims:
  - claim: "Enterprise accounts explain most of the gap"
    evidence_file: data/analysis/pipeline_by_segment.csv
    used_by_slides: [3]

caveats:
  - "Pipeline stage definitions changed in March"

open_questions:
  - "Confirm whether renewals should be excluded"
```

## `deck.md` link

Declare the analysis artifacts in frontmatter when a deck is data-driven:

```yaml
analysis_artifacts:
  manifest: analysis/manifest.yaml
  notes: analysis/notes.md
  queries:
    - id: pipeline_extract
      path: analysis/queries/pipeline_extract.sql
  tables:
    - id: chart_segment_gap
      path: data/charts/segment_gap.csv
      kind: chart
      used_by_slides: [3]
      required_columns: [segment, revenue_gap]
```

Then each chart slide points to the chart-ready CSV:

```yaml
chart:
  type: bar
  emphasis: "Enterprise accounts explain most of the gap"
  data_ref: data/charts/segment_gap.csv
  annotation: "Enterprise is the largest and most actionable shortfall"
```

## Consulting filter

Before drafting `deck.md`, turn the analysis into an argument:

- Write the answer first in one sentence.
- Pick the minimum evidence needed to make the answer credible.
- Use one slide for one insight.
- Use a chart only when it is the simplest proof of the takeaway.
- Do not include a chart just because the analysis produced one.
- Move secondary diagnostics to appendix or leave them in `analysis/notes.md`.
- Prefer a chart plus one implication over multiple charts on the same slide.

If more than half the deck wants to be charts, challenge the structure. The deck may need an executive synthesis, a recommendation framework, or an appendix separation.

## Validation

Before approval or production:

- `analysis_artifacts.manifest` exists when data analysis drove the deck.
- Every `analysis_artifacts.tables[].path` exists and is non-empty.
- Every `chart.data_ref` exists, is local, is non-empty, and has at least one numeric series.
- Chart `emphasis` echoes the slide takeaway.
- Quantitative slides include `Sources:`.
- The title sequence tells the argument without requiring the charts.
- SQL files and query assumptions are saved when SQL was used.

Use:

```bash
python skill/scripts/validate_deck_data.py deck.md
```
