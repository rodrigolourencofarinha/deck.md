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

## Source rules

- Any slide presenting quantitative data or a factual claim MUST carry a `Sources:` line.
- Sources MUST be specific (report name and date, not just "internal data").

## Mode rules

- If a slide is set to `mode: ppt-shapes`, the `creative_direction` block SHOULD be omitted (it applies to designer-mode only).
- If a slide is set to `mode: designer-mode` and includes a `chart:` block, the agent SHOULD warn — charts are typically more legible as ppt-shapes.

## Speaker notes

- Speaker notes MUST NOT duplicate the slide's body. They are what the presenter says BEYOND what's on the slide.
- Speaker notes are for the presenter; they MUST NOT appear in the rendered slide output.

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

If any check fails, the agent MUST fix before finalizing.
