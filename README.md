# deck.md

An open Markdown format for writing presentation briefs that AI agents turn into slide decks.

You write the logic — narrative structure, action titles, data, sources. The agent handles composition, visual treatment, and image generation. One `deck.md` file per deck; designed to be read by humans and parsed deterministically by agents.

## How it works

1. Copy `deck.md` and fill it in (title, narrative, slide titles, body).
2. Hand the file to an agent.
3. The agent produces slides — as generated images (`designer-mode`) or PowerPoint shapes (`ppt-shapes`).

## Levels of use

| Level | Use case | What you write |
|---|---|---|
| **Minimal** | 3–10 slide SCR, update, pitch | Narrative template + slide titles |
| **Standard** | Most working decks | Slide bodies, sources, speaker notes |
| **Full** | Client-facing, image-led | `creative_direction`, `required_text`, `chart`, full `key_line` |

Each level is a superset of the previous. Scaling up never requires reformatting.

## Narrative templates

| Template | Best for | Required fields |
|---|---|---|
| `scr` | Short consulting decks (3–10 slides) | `situation`, `complication`, `resolution` |
| `pyramid` | Long or branching decks (10+ slides) | `governing_thought`, `key_line` |
| `problem-solution` | Pitches and proposals | `problem`, `solution`, `why_now` |
| `update` | Status updates and retrospectives | `plan`, `actual`, `next` |

## Key rules

- Every slide title must be an **action title**: a full sentence with a verb, sentence case, no trailing period, ≤14 words.
- Body must prove the title. Nothing more, nothing less.
- Reading only the slide titles should reproduce the deck's argument.

## Files

| File | Purpose |
|---|---|
| [`deck.md`](./deck.md) | Starter template — copy and fill in |
| [`SPEC.md`](./SPEC.md) | Authoritative format specification |
| [`slide-archetypes.md`](./slide-archetypes.md) | Valid `type` values for slides |
| [`deck-validation.md`](./deck-validation.md) | Hard rules the agent self-checks before emitting |
| [`narrative-templates.md`](./narrative-templates.md) | Required fields and pitfalls per template |
| [`image-prompts.md`](./image-prompts.md) | Prompt templates for `gpt-image-2` |

## Examples

| File | Template | Description |
|---|---|---|
| [`scr.deck.md`](./scr.deck.md) | `scr` | Minimal 5-slide Q3 results review |
| [`pyramid.deck.md`](./pyramid.deck.md) | `pyramid` | Full deck with analysis and recommendation |
| [`problem-solution.deck.md`](./problem-solution.deck.md) | `problem-solution` | Startup pitch deck |
| [`update.deck.md`](./update.deck.md) | `update` | Quarterly engineering status report |

## License

[MIT](./LICENSE)
