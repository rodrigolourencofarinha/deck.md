# Deck artifact structure

Use this structure for generated deck work so every production round is easy to inspect, rerun, or compare.

## Core idea

One **instance** equals one human-visible production round:
- `001-initial` — the first generation from an approved deck.md
- `002-review-01` — the first post-render human review change
- `003-review-02` — the second post-render human review change

Never overwrite an earlier instance. A review creates a new instance even when only one slide changes. Unchanged slides can be copied or referenced, but the new instance must record what was reused.

## Standard tree

```text
decks/<deck-slug>/
  specs/
    YYYY-MM-DD-v01-deck.md
    YYYY-MM-DD-review-01-deck.md

  assets/
    source/
    prepared/

  instances/
    001-initial/
      deck.md
      manifest.yaml
      method/
        generation-plan.md
        slide-01.prompt.md
        slide-01.request.json
        slide-01.response.json
        manipulation-log.md
        render-review.md
        ocr-check.txt
      images/
        raw/
          slide-01.raw.png
        composed/
          slide-01.composed.png
        reviewed/
          slide-01.review.png
      outputs/
        deck.pdf

    002-review-01/
      deck.md
      revision-brief.md
      manifest.yaml
      method/
      images/
        raw/
        composed/
        reviewed/
      outputs/
        deck.pdf

  outputs/
    final/
    review/
```

## Folder meanings

- `specs/` stores approved and review deck.md versions. These are the logical source of truth.
- `assets/source/` stores human-provided source assets such as logos, templates, screenshots, and brand guides.
- `assets/prepared/` stores prepared reference assets such as rendered template PNGs or normalized logos.
- `instances/` stores production attempts and review rounds.
- `images/raw/` stores direct model outputs or direct render outputs before manipulation.
- `images/composed/` stores manipulated/composited slide images, such as logo placement, footer fixes, padding, OCR prep, or other post-processing.
- `images/reviewed/` stores the exact slide images that passed render inspection and were assembled into the instance output.
- `method/` stores how the instance was produced: prompts, model parameters, request/response metadata, manipulation logs, render-review notes, OCR notes, and blockers.
- `outputs/` inside an instance stores artifacts assembled from that instance.
- root `outputs/final/` stores only the clean human-facing final deliverables copied from the accepted instance.
- root `outputs/review/` stores contact sheets, review PDFs, or other review-facing artifacts.

## Instance manifest

Each instance must include `manifest.yaml`:

```yaml
instance: 002-review-01
source_spec: ../../specs/YYYY-MM-DD-review-01-deck.md
previous_instance: ../001-initial
status: passed_review
changed_slides: [3]
reused_slides: [1, 2, 4, 5]
raw_images:
  - images/raw/slide-03.raw.png
composed_images:
  - images/composed/slide-03.composed.png
reviewed_images:
  - images/reviewed/slide-01.review.png
  - images/reviewed/slide-02.review.png
  - images/reviewed/slide-03.review.png
final_pdf: outputs/deck.pdf
notes: "Regenerated slide 3 only; reused reviewed images for other slides."
```

## Naming rules

- Instance folders are zero-padded and semantic: `001-initial`, `002-review-01`, `003-review-02`.
- Slide files are zero-padded: `slide-01.raw.png`, `slide-01.composed.png`, `slide-01.review.png`.
- Use `.raw` only for untouched model or render outputs.
- Use `.composed` only after post-processing or manual/automated manipulation.
- Use `.review` only for images that passed visual inspection.

## Review-round rules

When the human asks for a post-render change:
- create a new review deck.md in `specs/`
- create a new instance folder
- include `revision-brief.md` or copy the deck.md `## Revision Brief` into the instance
- regenerate only changed slides unless the new brief affects the whole deck
- copy or reference unchanged reviewed slides
- update `manifest.yaml` with `changed_slides` and `reused_slides`
- assemble and inspect the full output from the instance's `images/reviewed/`

## Guardrails

- Do not mix raw generated images and manipulated images in the same folder.
- Do not store throwaway scratch crops as durable artifacts.
- Do not scatter final PDFs across multiple ad hoc folders.
- Do not overwrite earlier prompts, request metadata, or reviewed images.
- If a raw image is accepted without manipulation, copy it into `images/reviewed/` and record that no composition step was needed.
