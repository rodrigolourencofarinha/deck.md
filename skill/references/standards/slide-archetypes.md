# Slide archetypes

Catalog of valid values for the `type` field on a slide. Every slide in a `deck.md` MUST set `type` to one of the values below.

Each entry specifies:
- **Purpose** — what the slide does in the deck
- **Typical layout** — a common composition (not prescriptive)
- **Required/recommended fields** — beyond the base slide metadata
- **Example** — short illustration
- **Pitfalls** — common failure modes

See [`./narrative-templates.md`](./narrative-templates.md) for how slides fit into each template's narrative spine.

---

## `executive_summary`

**Purpose.** Opens the deck by making the governing thought visible in one slide. Should stand alone — a busy reader consuming only this slide should still understand the deck's answer.

**Preferred mode.** `designer-mode` — the opening slide benefits from a strong generated visual.

**Typical layout.** `three-column-scr` (SCR columns) or `title-with-three-bullets`.

**Recommended fields.** Body containing the SCR arc (situation / complication / resolution), or a 3-point decomposition of the governing thought.

**Example.**
```yaml
id: 1
type: executive_summary
layout: three-column-scr
```

**Situation.** Growth is our #1 KPI; board committed to 20% YoY in 2026.
**Complication.** Q3 growth fell 34% YoY — acquisition broke, not retention.
**Resolution.** Three levers recover growth in two quarters at $4M.

**Pitfalls.** Titles like "Executive summary" (topic, not answer); restating the question instead of answering it; more than three points.

---

## `section_divider`

**Purpose.** Transitions between sections of a longer deck. Gives the audience a beat and signals what's coming.

**Preferred mode.** `designer-mode` — a full-bleed generated visual makes a clean section break.

**Typical layout.** `full-bleed-title` with section number.

**Required fields.** Title only; body is typically absent or minimal.

**Example.**
```yaml
id: 12
type: section_divider
layout: full-bleed-title
```

**Body.** "Section 2 of 3: How we got here"

**Pitfalls.** Overusing (every 2–3 slides is too much); burying real content in the divider body.

---

## `situation`

**Purpose.** Establishes context the audience already accepts as true. Grounds the rest of the deck in shared reality.

**Preferred mode.** `ppt-shapes` — typically a chart or hero metric; shapes render more legibly.

**Typical layout.** `hero-number-with-caption` or `bullets-with-chart`.

**Recommended fields.** A chart or hero metric proving the situation; sources.

**Example.**
```yaml
id: 2
type: situation
layout: hero-number-with-caption
```

**Body.** "20% YoY growth is our 2026 commitment — the highest bar we've ever set."

**Pitfalls.** Stating a situation the audience doesn't actually accept; over-contextualizing something the audience already knows.

---

## `complication`

**Purpose.** Introduces the problem or change that creates the deck's reason for being. The "something happened" beat.

**Preferred mode.** `ppt-shapes` — data proving the complication renders more clearly as shapes.

**Typical layout.** `chart-with-title` or `before-after`.

**Recommended fields.** Data proving the complication; sources.

**Example.**
```yaml
id: 3
type: complication
```

**Body.** "Q3 growth fell 34% YoY — the steepest drop in four years, driven entirely by acquisition."

**Pitfalls.** Complication that isn't news; complication that doesn't clearly motivate the resolution.

---

## `key_takeaways`

**Purpose.** Summarizes findings at the end of a section or deck. Lets the audience consolidate before moving on.

**Preferred mode.** `ppt-shapes` — a numbered text list; generation adds nothing.

**Typical layout.** `numbered-list` with 3–5 items.

**Required fields.** Body as 3–5 takeaway statements, each a full sentence.

**Example.**
```yaml
id: 11
type: key_takeaways
layout: numbered-list
```

**Body.**
1. Acquisition, not retention, is the cause of the 2025 slowdown
2. Paid channels are hitting diminishing returns at current mix
3. Organic content engine has highest ROI but longest ramp

**Pitfalls.** More than 5 takeaways (they're notes, not takeaways); takeaways phrased as topics rather than claims.

---

## `analysis`

**Purpose.** Presents an argument backed by evidence. The workhorse body slide. One claim (the action title), proof in the body.

**Preferred mode.** `ppt-shapes` — charts and evidence tables render best as shapes. Switch to `designer-mode` only when the visual metaphor carries the argument better than a chart.

**Typical layout.** `chart-left-text-right`, `text-left-chart-right`, or `chart-with-annotations`.

**Recommended fields.** A `chart:` block if the proof is quantitative; sources.

**Example.**
```yaml
id: 4
type: analysis
layout: chart-left-text-right
```

**Body.**
- Paid-channel CAC rose 2.1× across Q2–Q3
- Organic traffic share dropped from 42% to 19%
- Retention cohorts held flat at 73% D30

```yaml
chart:
  type: stacked-bar
  emphasis: "Acquisition decline, not retention"
  data_ref: ./data/signups_by_channel.csv
```

**Pitfalls.** Body that doesn't prove the title; charts without an emphasis; too many bullets.

---

## `chart`

**Purpose.** A slide where the chart IS the message. The chart carries the argument; text is annotation.

**Preferred mode.** `ppt-shapes` — always. Generated images cannot render data-accurate charts.

**Typical layout.** `chart-full-bleed-with-callout`.

**Required fields.** A `chart:` block with `emphasis` echoing the action title and an `annotation` highlighting the key insight.

**Example.**
```yaml
id: 5
type: chart
layout: chart-full-bleed-with-callout
```

```yaml
chart:
  type: line
  emphasis: "Organic share collapse, not paid saturation"
  data_ref: ./data/channel_mix_2020_2025.csv
  annotation: "Organic fell from 42% to 19% between Jan and Oct 2025"
```

**Pitfalls.** Chart too busy to read in 10 seconds; emphasis that doesn't match the title; multiple stories in one chart.

---

## `framework`

**Purpose.** Presents a conceptual model, matrix, or diagram. The deck pauses to give the audience a mental map.

**Preferred mode.** `designer-mode` — conceptual diagrams (2×2s, funnels, pyramids) benefit from generated visuals when the structure is simple and label-only.

**Typical layout.** `2x2-matrix`, `quadrant-grid`, `layered-pyramid`, `funnel`.

**Recommended fields.** Body as labels and short explanations per quadrant/layer.

**Example.**
```yaml
id: 6
type: framework
layout: 2x2-matrix
```

**Body.** Axes: impact (y) × feasibility (x). Four quadrants: quick wins, long-term bets, distractions, do-not-bothers.

**Pitfalls.** 2×2s where the axes aren't the real tension; labels that don't map to actual decisions.

---

## `recommendation`

**Purpose.** States what to do. Often a major beat in the deck — the governing thought restated with specificity.

**Preferred mode.** `designer-mode` — this is a visually high-leverage slide; a generated visual reinforces the recommendation's weight.

**Typical layout.** `horizontal-three-column` (three levers, options, pillars).

**Recommended fields.** `creative_direction` and `required_text` when in designer-mode — this is a visually high-leverage slide.

**Example.**
```yaml
id: 7
type: recommendation
layout: horizontal-three-column
image_decision: full-generated-visual
```

**Body.**
- **Rebuild organic** — ship the content engine; target 30% channel share
- **Rebalance paid mix** — cut Meta by 40%, reallocate to search and partnerships
- **Reactivate dormant users** — lifecycle campaign targeting 180-day inactive cohort

**Pitfalls.** Recommendations that are actually conclusions ("we should think about X"); more than five recommendations; recommendations without owners.

---

## `roadmap`

**Purpose.** Shows a plan over time. Sequences actions, phases, or milestones.

**Preferred mode.** `ppt-shapes` — timelines with dates, phases, and owners are more legible as shapes.

**Typical layout.** `horizontal-timeline`, `gantt-simple`, `phase-bands`.

**Required fields.** Body as phases or milestones with dates; one line per phase.

**Example.**
```yaml
id: 9
type: roadmap
layout: horizontal-timeline
```

**Body.**
- **Q1 2026** — Content engine v1 ships; paid mix rebalanced; lifecycle campaign launched
- **Q2 2026** — Organic reaches 25% share; dormant reactivation at 15% rate; $4M cumulative spend
- **Q3 2026** — Growth back to 20%+ YoY; channel mix rebalanced and durable

**Pitfalls.** Dates without owners; phases that aren't really sequenced; implausible timelines.

---

## `risk_mitigation`

**Purpose.** Identifies risks and the specific mitigations. Signals that the author has thought about what could go wrong.

**Preferred mode.** `ppt-shapes` — a table with four columns cannot be faithfully rendered by image generation.

**Typical layout.** `risk-table` (risk, likelihood, impact, mitigation).

**Required fields.** Body as a table or structured list: each risk paired with a mitigation.

**Example.**
```yaml
id: 10
type: risk_mitigation
layout: risk-table
```

**Body.**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Content engine ramps slower than 30% target | Medium | High | Maintain paid spend at 80% through Q2 as bridge |
| Reactivation campaign has <10% response | Medium | Medium | Pre-test on cohort before full rollout |

**Pitfalls.** Generic risks ("market changes"); mitigations that don't actually address the risk; missing the most obvious risks.

---

## `next_steps`

**Purpose.** Lists concrete actions, with owners and dates. The "what happens Monday" slide.

**Preferred mode.** `ppt-shapes` — action/owner/date tables render best as shapes. Use `designer-mode` only for a milestone-on-timeline visual.

**Typical layout.** `owner-action-date-table`.

**Required fields.** Body with action, owner, date per line.

**Example.**
```yaml
id: 13
type: next_steps
layout: owner-action-date-table
```

**Body.**
- **Ship content engine v1** — Head of Growth, Jan 15
- **Reallocate $800K from Meta** — VP Marketing, Jan 22
- **Launch reactivation pilot (10K cohort)** — Lifecycle Lead, Feb 1

**Pitfalls.** Actions without owners; actions without dates; vague actions ("explore X").

---

## `appendix`

**Purpose.** Supporting material that backs up claims in the main deck without interrupting the flow. Lives at the end.

**Preferred mode.** Inherits from the underlying archetype it mirrors.

**Typical layout.** Any — mirrors body slide archetypes (analysis, chart, etc.).

**Required fields.** Same as the underlying archetype it supports.

**Example.**
```yaml
id: 20
type: appendix
```

**Body.** Detail on cohort definitions used in retention analysis (slide 3).

**Pitfalls.** Using appendix for slides that should actually be in the body; appendix longer than the main deck.
