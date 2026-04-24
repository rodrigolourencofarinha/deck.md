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
| [`standards/slide-archetypes.md`](./standards/slide-archetypes.md) | Valid `type` values for slides |
| [`standards/deck-validation.md`](./standards/deck-validation.md) | Hard rules the agent self-checks before emitting |
| [`standards/narrative-templates.md`](./standards/narrative-templates.md) | Required fields and pitfalls per template |
| [`standards/image-prompts.md`](./standards/image-prompts.md) | Prompt templates for `gpt-image-2` |

## Examples

| File | Template | Description |
|---|---|---|
| [`examples/scr.deck.md`](./examples/scr.deck.md) | `scr` | Minimal 5-slide Q3 results review |
| [`examples/pyramid.deck.md`](./examples/pyramid.deck.md) | `pyramid` | Full deck with analysis and recommendation |
| [`examples/problem-solution.deck.md`](./examples/problem-solution.deck.md) | `problem-solution` | Startup pitch deck |
| [`examples/update.deck.md`](./examples/update.deck.md) | `update` | Quarterly engineering status report |

## The skill

`skill/` is a reference implementation of the deck-architect agent skill. It shows how to wire deck.md into a working agent: narrative-to-brief generation, approval gate, slide production via GPT Image 2 or python-pptx, and PDF assembly.

| Path | Purpose |
|---|---|
| [`skill/SKILL.md`](./skill/SKILL.md) | Skill entry point — the agent reads this first |
| [`skill/references/`](./skill/references/) | Production and workflow guides |
| [`skill/scripts/`](./skill/scripts/) | `build_pptx.py`, `tabler_icons.py`, `split_template_deck.py` |

## Deploying to your own agent

When you copy this skill into your own project, the format files (spec, standards, examples) need to be accessible to the agent alongside the skill. The recommended layout is to bring them into `skill/references/` so the whole skill is self-contained:

```
your-project/
└── skill/
    ├── SKILL.md
    ├── references/
    │   ├── SPEC.md                     ← from repo root
    │   ├── deck.md                     ← from repo root
    │   ├── deck.minimal.md             ← from repo root
    │   ├── standards/                  ← from repo root
    │   ├── examples/                   ← from repo root
    │   ├── deck-workflow.md
    │   ├── consulting-slide-standards.md
    │   ├── single-slide-workflow.md
    │   ├── pptx-production.md
    │   ├── template-catalog.md
    │   ├── designer-mode-workflow.md
    │   ├── designer-mode-gpt-image-prompt-scaffold.md
    │   ├── designer-mode-direct-api-pattern.md
    │   └── tabler-icon-selection.md
    └── scripts/
        ├── build_pptx.py
        ├── split_template_deck.py
        └── tabler_icons.py
```

Then update the paths in `SKILL.md` to reflect the new locations — for example, `SPEC.md` becomes `references/SPEC.md`, `standards/slide-archetypes.md` becomes `references/standards/slide-archetypes.md`, and so on.

If you just want the simplest path: clone this repo and point your agent at the root. `skill/SKILL.md` references `SPEC.md`, `standards/`, and `examples/` as root-relative paths — no reorganization needed as long as your agent runs from the repo root.

## License

[MIT](./LICENSE)
