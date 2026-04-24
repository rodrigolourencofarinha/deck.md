---
document: deck-md-specification
schema_version: deck-md/v2-alpha
---

# The `deck.md` specification

`deck.md` is a Markdown-based file format for specifying presentation decks to AI agents. It is **the brief** a human writes (or co-writes with a model) and hands to an agent, which then produces the slides. One `deck.md` per deck. It is designed to be read and edited comfortably by humans *and* parsed deterministically by agents — the same file serves both audiences.

It follows [AGENTS.md](https://agents.md) conventions: plain Markdown, optional YAML frontmatter, headings for structure, fenced code blocks for machine-parseable fields.

**This document (`SPEC.md`) is the authoritative specification of the format.** For a starter brief to copy and fill in, see [`./deck.md`](./deck.md). For worked examples, see [`./examples/`](./examples/).

## Purpose

`deck.md` separates a deck's **logic and content** (the author's responsibility) from its **composition and visual treatment** (the model's responsibility). The spec prescribes logic. It does not prescribe composition beyond what's needed for deck-wide consistency.

Use `deck.md` when you want:
- Reproducible, reviewable deck specifications.
- A format that covers PowerPoint-shape output and image-generated slides without rewriting.
- Coordination between multiple models or human reviewers on the same deck.

## Agent workflow

`deck.md` supports two authorship modes and a two-phase generation pipeline.

**Authorship modes:**
- **Human-authored brief:** A human writes (or finishes) the `deck.md` and hands it to the agent. The agent validates and goes straight to phase 2.
- **Agent-generated brief:** A human provides a broad idea, raw content, or partial notes. The agent writes the `deck.md` (phase 1), the human validates it, then the agent generates slides (phase 2).

**Phase 1 — Brief generation.** The agent receives raw input and produces a complete `deck.md` with `status: draft`. It populates `## Brief` with a summary of what it received and how it interpreted it. The human reviews, edits if needed, and sets `status: approved` to release generation. The agent MUST NOT proceed to phase 2 while `status: draft`.

**Phase 2 — Slide generation.** The agent reads an `approved` deck.md, validates it against `standards/deck-validation.md`, and produces one rendered image per slide (see `## Output`). `designer-mode` slides are generated via gpt-image-2. `ppt-shapes` slides are rendered as layout images from the design tokens. All slides are assembled into a PDF in slide order.

The two phases are intentionally separate. Phase 1 produces a readable, editable document — not an irreversible side effect. If the brief doesn't match what the human wanted, they edit it before anything is generated.

## File format

A valid `deck.md` is:
1. **YAML frontmatter** between `---` delimiters — deck metadata, design tokens, production defaults.
2. **Markdown sections** with predefined H2 headings.
3. **Fenced `yaml` blocks** inside sections where fields must be machine-parsed (per-slide metadata, chart specs, narrative spine).

Filename convention: `deck.md` at the root of a project, or `<name>.deck.md` for multiple decks in one repo.

## Required surface

At every level of complexity, a valid `deck.md` MUST include:

- `deck.title` in the frontmatter
- A `## Narrative` section (template-based or full block)
- A `## Slides` section with at least one `### Slide N — "Title"` heading

Everything else is optional with sensible defaults.

## Levels of use

Three levels. Each is a superset of the previous. Scaling up never requires reformatting.

| Level | Use case | Adds | Example |
|---|---|---|---|
| **Minimal** | 3–10 slide SCR, update, pitch | Narrative template + slide titles | [`deck.minimal.md`](./deck.minimal.md), [`examples/scr.deck.md`](./examples/scr.deck.md) |
| **Standard** | Most working decks | Slide bodies, sources, speaker notes | [`examples/update.deck.md`](./examples/update.deck.md) |
| **Full** | Client-facing, image-led | `creative_direction`, `required_text`, `chart`, full `key_line` | [`examples/pyramid.deck.md`](./examples/pyramid.deck.md) |

## Authorship

- **Human controls:** narrative structure, action titles, slide types, data, sources, validation rules.
- **Model controls:** composition, metaphor, visual treatment, iconography, layout refinement.
- **Tie-breaker:** human wins on conflict. The model may propose alternatives in a slide's `prompt_notes` but MUST NOT silently override human-set fields.

## Frontmatter schema

```yaml
---
deck:
  title:     "<string, required>"
  objective: "<string, optional>"
  audience:  "<string, optional>"
  language:  "<en|pt|...>"
  author:    "<string, optional>"
  version:   "<string, optional>"

status: "<draft|approved>"                                    # default: draft; set to approved to release generation

narrative_template: "<scr|pyramid|problem-solution|update>"   # required

production_defaults:
  default_slide_mode: "<ppt-shapes|designer-mode>"            # default: ppt-shapes
  aspect_ratio: "16:9"
  default_visual_template: "<path, optional>"
  default_visual_template_scope: "<string, optional>"

image_generation:                                             # only used when mode is designer-mode
  primary_creator: "gpt-image-2"
  size:            "2560x1440"
  quality:         "high"
  output_format:   "png"
  variants:        1

design_tokens:
  palette:       { primary, secondary, accent, accent_soft, background, line }
  typography:    { title, body, emphasis }
  spacing:       { outer_margin, block_gap }
  iconography:   { family }
  shape_language: { corner_style, line_weight }
---
```

Only `deck.title` and `narrative_template` are strictly required. All other frontmatter blocks are optional with defaults.

## Design principles

### Visual intent
Premium, consulting-style. Message-first, not decoration-first. Polished but controlled. High clarity at a glance.

### Text policy
- Every slide title MUST be an **action title** — a full sentence with a verb that states the "so what", not a topic label.
- Body MUST prove the title; nothing in the title should go unproven, nothing in the body should be irrelevant to the title.
- Sentence case. No trailing periods. No stray invented text in generated slides.

Hard limits (word counts, case, bullet counts) live in [`./standards/deck-validation.md`](./standards/deck-validation.md) and MUST be self-checked before emitting.

### Image policy
- Default to `ppt-shapes`. A slide opts into `designer-mode` when a generated visual adds clear value (executive summaries, recommendations, section dividers). Charts, tables, and text-heavy slides should stay as `ppt-shapes` — they render more legibly and image generation adds no value there. Each archetype in [`./standards/slide-archetypes.md`](./standards/slide-archetypes.md) declares a `preferred_mode` as a starting point.
- One strong visual idea per slide.
- When `image_decision: full-generated-visual`, the slide MUST declare `required_text`. The model MUST NOT render any text in the image that is not listed there.
- Reject: poster-like output, background plates, cropped salvage jobs, decorative stock-photo energy.

### Consistency
Stable title treatment, slide-type patterns, palette and emphasis behavior across the deck. No slide drifts into a different visual language.

## Narrative

The deck's logical spine. Set via one of four templates. Every body slide should ladder up to one argument in `key_line` (for `pyramid`) or one named narrative element.

### Templates

| Template | Required fields | Best for |
|---|---|---|
| `scr` | `situation`, `complication`, `resolution` | Short-form consulting (3–10 slides) |
| `pyramid` | `governing_thought`; recommended: `question`, `key_line`, `mece_check` | Long or branching decks (10+ slides, multiple arguments) |
| `problem-solution` | `problem`, `solution`, `why_now` | Pitches, proposals |
| `update` | `plan`, `actual`, `next` | Status updates, retrospectives |

See [`./standards/narrative-templates.md`](./standards/narrative-templates.md) for required fields, canonical examples, and pitfalls per template.

## Slides

Each slide is a `### Slide N — "Action title"` heading, followed by a fenced `yaml` metadata block, then markdown body and optional fenced blocks for `chart`, `creative_direction`, `required_text`.

### Slide field reference

```yaml
id: <integer, required>
type: <see ./standards/slide-archetypes.md, required>
layout: "<string, optional>"
mode: "<ppt-shapes|designer-mode>"                       # inherits from production_defaults
image_decision: "<none|icon-only|cutout|full-generated-visual>"
visual_template_reference: "<path>"                      # overrides deck default
visual_template_scope: "<string>"                        # overrides deck default
```

**`id` and slide ordering.** Integer IDs double as ordering keys. Inserting a slide between two existing slides requires renumbering all subsequent IDs and updating every `supporting_slides` reference. For decks that will evolve significantly, use short stable string IDs (`id: s_organic_lever`) instead — both forms are valid.

**`layout` and unrecognized values.** Layout values recognized by the composition hints table in `standards/image-prompts.md` receive specific composition guidance. An unrecognized value is treated as a freeform hint — the agent infers a reasonable composition from the slide's type, title, and body. No error is thrown, but no composition guarantee is made.

**`image_decision` values.**
- `none` — no image or icon; the slide is pure text.
- `icon-only` — one or two icons placed in the composition; the rest is text.
- `cutout` — a subject (product screenshot, person, object) isolated from its background and composited over the slide. The agent must be told what the cutout subject is via `creative_direction`.
- `full-generated-visual` — the entire slide canvas is a generated image. MUST declare `required_text`.

### Optional per-slide fenced blocks

- `chart:` — when the slide contains a chart. Fields: `type`, `emphasis`, `data_ref`, `annotation`. `emphasis` should echo the action title.
- `creative_direction:` — when `mode: designer-mode`. Fields: `mood`, `metaphor`, `composition_intent`, `prompt_notes[]`, `avoid[]`. This is the model's creative surface.
- `required_text:` — when `image_decision: full-generated-visual`. Fields: `title`, `subtitle`, `labels[]`. The model MUST NOT render text outside this list.

### Prose fields (markdown, not YAML)

- **Body** — the content of the slide.
- **Sources** — attribution line.
- **Speaker notes** — what the presenter says beyond what's on the slide. When a slide is rendered as a generated image (`mode: designer-mode`, `image_decision: full-generated-visual`), speaker notes are NOT embedded in the image. The agent delivers them as PDF presenter notes or a companion notes document. They never appear in the generated image regardless of mode.

### Slide archetypes

The `type` field must be a value in [`./standards/slide-archetypes.md`](./standards/slide-archetypes.md): `executive_summary`, `section_divider`, `situation`, `complication`, `key_takeaways`, `analysis`, `chart`, `framework`, `recommendation`, `roadmap`, `risk_mitigation`, `next_steps`, `appendix`.

## Brief

An optional `## Brief` section appears in agent-generated `deck.md` files. It is absent from human-authored briefs. It documents what the agent received as input and how it interpreted that input — giving the human a clear audit trail to review before setting `status: approved`.

The agent MUST populate `## Brief` when generating a `deck.md` from raw input (idea, content, or partial brief). It MUST NOT add it when refining a human-written `deck.md`.

Contents are a fenced `yaml` block with four fields:

```yaml
input_type: "<idea|content|partial_brief>"
input_summary: "<one or two sentences on what was provided>"
interpretation: "<what the agent inferred: audience, objective, template choice, narrative structure>"
open_questions:
  - "<anything that couldn't be determined and was left as a placeholder>"
```

**Example:**

```yaml
input_type: idea
input_summary: "Founder asked for a Series A pitch deck for a B2B SaaS onboarding product targeting mid-market."
interpretation: "Chose problem-solution template. Audience: VC investors. Objective: secure a first meeting. Tone: confident and evidence-backed."
open_questions:
  - "Traction data — placeholder on Slide 4; replace with real numbers before approving"
  - "Preferred typeface — defaulted to Inter; override typography in design_tokens if needed"
```

## Notes to the agent

An optional `## Notes to the agent` section holds freeform context that doesn't fit elsewhere. It is always agent-facing and never appears in rendered output. No required structure. Typical contents: deadlines and reviewer names; data file locations; related decks or prior versions; output format constraints (PDF, PPTX, Google Slides); post-generation instructions (embed recording, add watermark); things to double-check.

## Output

### Slide files

Every slide produces one PNG regardless of mode:
- `designer-mode` slides are generated via gpt-image-2 per the prompt templates in [`./standards/image-prompts.md`](./standards/image-prompts.md).
- `ppt-shapes` slides are rendered as layout images by the agent from the deck's `design_tokens` — no image generation call is made, but the output is still a PNG sized to `image_generation.size`.

File naming convention: `slides/slide-01.png`, `slides/slide-02.png`, etc. (zero-padded to two digits; three digits for decks over 99 slides). Assembly order follows `id` values ascending. For string IDs, document order applies.

### PDF assembly

The final PDF is assembled from all slide PNGs in order. Default filename: the deck title slugified (e.g., `2026-growth-recovery-plan.pdf`). Override with an explicit filename in `## Notes to the agent`.

Speaker notes, if present, are embedded as PDF presenter notes. They can also be exported as a companion Markdown file (`{slug}-notes.md`) — request this in `## Notes to the agent`.

### Quality

Use `image_generation.quality: low` during brief iteration — fast and inexpensive. Switch to `high` for the approved final pass. Agents MAY auto-downgrade to `low` while `status: draft` and upgrade to `high` when `status: approved`.

## Validation and error handling

If a `deck.md` fails any rule in [`./standards/deck-validation.md`](./standards/deck-validation.md), the agent MUST report all errors and block generation until they are resolved. Warn-and-proceed is not allowed — an invalid brief produces an unpredictable deck. If the `schema_version` is unrecognized, the agent MUST warn and ask the human to confirm before proceeding.

## Accessibility

- Generated images MUST include an alt-text string (set in `required_text.alt` or inferred from the action title and body).
- Palette contrast between `primary` text and `background` MUST meet WCAG AA (4.5:1 for body, 3:1 for large text). The agent SHOULD warn if declared hex values fail this check.
- Minimum readable title size is 36pt at 2560×1440; body text 24pt. The agent SHOULD warn if `creative_direction` or layout hints would push text below this.

## Precedence

1. Per-slide fields override everything else.
2. `## Narrative` defines the logical spine — body slides must ladder up to it.
3. `## Design principles` sets deck-wide behavior.
4. Frontmatter sets defaults.
5. Referenced standards (archetypes, validation, prompts) are authoritative within their domain.

On conflict, the closer-in rule wins. Human-set fields beat model improvisation.

## References

- [`./standards/narrative-templates.md`](./standards/narrative-templates.md) — reference for each `narrative_template` value: required fields, canonical examples, pitfalls.
- [`./standards/slide-archetypes.md`](./standards/slide-archetypes.md) — catalog of valid `type` values with required fields and typical layouts.
- [`./standards/deck-validation.md`](./standards/deck-validation.md) — hard rules the agent self-checks before emitting.
- [`./standards/image-prompts.md`](./standards/image-prompts.md) — prompt templates for `gpt-image-2` calls.

## Examples

- [`./examples/scr.deck.md`](./examples/scr.deck.md) — minimal 5-slide SCR narrative.
- [`./examples/pyramid.deck.md`](./examples/pyramid.deck.md) — full pyramid deck with `executive_summary`, `analysis` (chart), and `recommendation` (designer-mode with `required_text`).
- [`./examples/problem-solution.deck.md`](./examples/problem-solution.deck.md) — a startup pitch deck using the `problem-solution` template.
- [`./examples/update.deck.md`](./examples/update.deck.md) — a quarterly engineering status report using the `update` template.
