# Deck validation rules

Hard rules an agent MUST self-check before emitting a deck from a `deck.md`. These are not preferences; they are constraints. Violating any rule is an error.

---

## Title rules

- Every slide title MUST be a full sentence with a verb.
- Every slide title MUST state the "so what" — a takeaway or claim, not a topic label.
- Sentence case only (first word capitalized; rest lowercase unless proper nouns).
- No trailing period.
- Maximum 14 words.

Examples:
- ✅ "Acquisition, not retention, broke in Q3"
- ✅ "Three levers recover growth in two quarters at $4M"
- ❌ "Q3 results" (topic label, no verb)
- ❌ "Growth recovery options" (topic label, no claim)
- ❌ "Our analysis shows that growth recovery will require multiple levers and a significant investment" (>14 words)

## Body rules

- Maximum 5 bullets per slide.
- Maximum 12 words per bullet.
- One idea per slide — if a slide has more than one claim, split it.
- Every claim in the body MUST either support the title or be removed.
- Nothing in the title should go unproven in the body; nothing in the body should be irrelevant to the title.

## Narrative rules

- The deck MUST have a valid `narrative_template` value: `scr`, `pyramid`, `problem-solution`, or `update`.
- All required fields for the chosen template MUST be filled (see [`./narrative-templates.md`](./narrative-templates.md)).
- For `pyramid`: every `key_line` argument MUST have at least one entry in `supporting_slides`. Every body slide SHOULD appear in at least one `supporting_slides` list (orphan slides are flagged).
- `mece_check` (for pyramid) MUST address both the "mutually exclusive" property and the "collectively exhaustive" property.

## Horizontal logic

- Reading ONLY the slide titles of the deck should reproduce the deck's argument.
- The agent MUST self-check this: extract all titles, read them top-to-bottom, verify they tell the story. If not, flag.

## Image rules

- When `image_decision: full-generated-visual`, the slide MUST declare `required_text`.
- The model MUST NOT render any text in the generated image that is not listed in `required_text`.
- The generated image MUST preserve the deck's `design_tokens` (palette, shape language, iconography).
- The generated image MUST NOT contain photographic or cinematic imagery unless explicitly enabled in `creative_direction`.
- Any slide `asset_refs` MUST point to ids declared in frontmatter `designer_assets`.
- Any `designer_assets` entry with `required: true` MUST resolve to an available asset before production.
- Non-image designer assets, such as `.pptx` templates, MUST be prepared as model-readable references before generation.

## Source rules

- Any slide presenting quantitative data or a factual claim MUST carry a `Sources:` line.
- Sources MUST be specific (report name and date, not just "internal data").

## Footer rules

- Every generated slide MUST include the standard small footer unless the approved deck.md explicitly disables it.
- Default footer: `CR` in the lower-left corner and a simple numeric page number in the lower-right corner.
- Page numbers MUST render as `1`, `2`, `3`, ... in slide order, not as zero-padded filenames.
- Page numbers MUST NOT include the total slide count, slash formats, or "of" wording; use `1`, not `1/3` or `1 of 3`.
- Footer elements MUST follow the deck typography and color system and MUST NOT overlap sources, logos, charts, labels, or body content.
- For designer-mode slides, the computed footer text MUST be included in the prompt's allowed text list.

## Mode rules

- If a slide is set to `mode: ppt-shapes`, the `creative_direction` block SHOULD be omitted (it applies to designer-mode only).
- If a slide is set to `mode: designer-mode` and includes a `chart:` block, the agent SHOULD warn — charts are typically more legible as ppt-shapes.

## Speaker notes

- Speaker notes MUST NOT duplicate the slide's body. They are what the presenter says BEYOND what's on the slide.
- Speaker notes are for the presenter; they MUST NOT appear in the rendered slide output.

## Render review rules

- The agent MUST render the produced deck or slide outputs before delivery.
- The rendered output MUST be compared against the approved deck.md, original briefing, and any `## Revision Brief`.
- Every rendered slide MUST show the required footer mark and page number in the approved placement.
- Required logos and assets MUST appear in the approved placement and MUST NOT overlap text or important visuals.
- Text, labels, charts, logos, and visual blocks MUST NOT overlap or be clipped.
- If rendered output fails review, the agent MUST revise the spec or regenerate/rebuild the affected slide, then render and inspect again.

## Revision rules

- Human change requests after a rendered output MUST create a new review deck.md version such as `review-01` or `review-02`.
- Review versions MUST be created from the previous approved deck.md plus the new human change request.
- Review versions SHOULD include `## Revision Brief` with previous deck path, review round, change request, changed slides, unchanged slides, and regeneration scope.
- Designer-mode review changes SHOULD regenerate only changed slides and preserve unchanged slide images/specs.

---

## Self-check checklist

Before emitting a deck, the agent validates:

1. [ ] All titles are action titles: full sentence, verb, sentence case, no trailing period, ≤14 words
2. [ ] All slide `type` values are valid archetypes (see [`./slide-archetypes.md`](./slide-archetypes.md))
3. [ ] Narrative template is valid and required fields are filled
4. [ ] Key line (if present) has MECE arguments with supporting_slides
5. [ ] Every body slide appears in at least one `supporting_slides` list (pyramid only)
6. [ ] Reading only the titles reproduces the deck's argument
7. [ ] Every quantitative claim has a source
8. [ ] Generated images contain only text listed in `required_text`
9. [ ] No slide exceeds 5 bullets
10. [ ] No bullet exceeds 12 words
11. [ ] All `asset_refs` resolve to declared `designer_assets`
12. [ ] Required designer assets exist or production is blocked
13. [ ] Rendered output has been inspected against the approved deck.md and briefing
14. [ ] Logos/assets are correctly placed with no overlap or clipping
15. [ ] Standard footer mark and simple numeric page number appear on every rendered slide
16. [ ] Review changes use a new review deck.md version and regenerate only changed slides

If any check fails, the agent MUST fix before finalizing.
