# Deck workflow

Use this note to choose the right deck shape, density, and storyline before building slides.

For consulting-style, executive, or read-alone decks, also use `consulting-slide-standards.md`.

## Start with the decision

Clarify:
- audience
- what decision, understanding, or action the deck should create
- whether the deck will be read alone or presented live
- required output: outline, approved spec, editable deck, or polished visual slides

Do not start from PowerPoint decoration.
Do not produce slides until the human has validated and approved the current `deck.md`.
When the human supplies logos, existing slides, templates, brand guides, screenshots, icons, or other visual inputs, declare every asset the model should receive in `designer_assets` before approval. Do not pass undeclared assets to the visual model.
For existing-slide redesigns, treat old decks/slides as content-and-style references by default: preserve message and key evidence, borrow useful visual rhythm, and redesign composition freely.
For pure designer-mode decks, produce PDF output only and add OCR/searchable text when tooling is available.
Every generated slide should include the standard small footer unless the approved deck.md disables it: `CR` lower-left and simple page numbers (`1`, `2`, `3`, ...) lower-right. Do not use total-count formats such as `1/3`.
Save generated work in production instances: source assets in `assets/source/`, model-readable prepared inputs in `assets/prepared/`, raw model/render outputs in `images/raw/`, manipulated/composed slide images in `images/composed/`, inspected accepted slide images in `images/reviewed/`, and prompts/metadata/review notes plus `model-inputs.yaml` in `method/`.
After production, render and inspect the output against the approved `deck.md` and briefing; repair and rerender before delivery.

## Material types and density

### Proposal deck
Use when the deck must sell an approach.

Optimize for:
- showing understanding of the situation
- framing why the problem matters
- explaining the proposed approach
- making workplan, team, and timing easy to scan

Density:
- moderate
- persuasive but still analytical

### Decision or report pack
Use when the material must stand alone and support careful reading.

Optimize for:
- read-alone clarity
- evidence on the page
- conclusion-led titles
- substantial appendix or backup where needed

Density:
- medium to high
- allow more explanation, but protect hierarchy aggressively

### Public thought-leadership deck
Use for external-facing or editorial material.

Optimize for:
- cleaner thematic modules
- stronger visual rhythm
- modular proof blocks
- high polish without losing analytical clarity

Density:
- lower
- more selective evidence and clearer rhythm

### Training, class, or workshop deck
Use when the presenter carries part of the explanation.

Optimize for:
- teaching flow
- frameworks and examples
- lower reading burden per slide
- strong sectioning and visual teaching aids

Density:
- low to medium
- less text than a leave-behind pack

## Default deck architecture

Use this unless the task clearly needs another shape:
1. cover or session objective
2. agenda or framing
3. core body of analysis or teaching logic
4. synthesis, recommendation, or recap
5. next steps, roadmap, or application
6. appendix or backup when useful

## Storyline rules

- lead with the answer
- draft the storyline before production
- draft action titles before slide bodies
- read the action-title sequence alone; it should tell the full deck argument
- make each slide do one job
- keep horizontal flow coherent across slides
- keep vertical flow coherent inside each slide
- write action titles, not topic labels
- let the body prove the title

Useful deck-level frames:
- situation, complication, resolution
- problem, analysis, solution
- current state, opportunity or risk, recommendation

## Consulting-style principles

### Action title
Write a title that states the slide's conclusion.
It should be a complete sentence, ideally under 15 words, and fit in at most two lines.

### Body as proof
The body should prove the title with the minimum evidence needed.
Nothing in the body should be unrelated to the title, and nothing in the title should be unsupported by the body.

### Horizontal flow
A reader should understand why slide N leads to slide N+1.

### Vertical flow
Inside the slide, guide the eye through title, main proof, and supporting detail in that order.

## Review questions

Before moving into production, check:
- what decision should this deck support
- could the audience understand the main story quickly
- is this deck read alone or presented live
- has the human approved the current `deck.md`, not just the initial briefing
- if this is pure designer-mode, is the deliverable PDF-only with OCR attempted
- after rendering, will footer/page numbers, logo placement, overlaps, safe margins, and briefing match be inspected
- will the production round have an instance folder with raw, composed, reviewed, method, and output artifacts
- is the density right for that mode
- does each title communicate a conclusion
- can the title sequence stand alone as the argument
- do source, units, footer, and status markings meet the needs of the deck type
- is anything still storyline work rather than design work

## Rule

If the storyline is still fuzzy, stay in the spec.
Do not jump into slide production early.
Default to designer-mode for production unless the human asks for `ppt-shapes` or the slide needs charts, tables, or precise editability.

## Review-version rule

When the human asks for changes after seeing a rendered deck:
- create a new review deck.md version, such as `YYYY-MM-DD-review-01-deck.md`
- create a new production instance, such as `002-review-01`
- include `## Revision Brief`
- use the previous approved deck.md plus the new change request as inputs
- patch only what changed
- regenerate only changed slides
- reuse unchanged reviewed slide images from the previous instance
- update the instance manifest with changed slides and reused slides
- render and inspect the full deck again before delivery
