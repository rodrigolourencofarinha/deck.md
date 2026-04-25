# Tabler Icon Selection

## When to read this

Read this when a slide needs one or more icons and the choice is not obvious.
Use it to avoid random browsing across thousands of icons.

## What labeling exists

Yes — the bundled Tabler icons are labeled.

They are labeled mainly by canonical filenames such as:
- `chart-bar`
- `users-plus`
- `arrow-ramp-right`
- `shield-check`
- `calendar-week`

Common alternate names are also mapped in `assets/tabler-icons/aliases.json`.
That means search works well for direct nouns and simple concepts, but the library is **not** labeled with slide-specific consulting intent by default. Use the curated topics below for that.

## Quick selection rules

1. Prefer `outline` icons by default.
2. Use `filled` icons only for tiny badges, strong emphasis, or status chips.
3. Choose the most literal business-safe icon, not the cleverest or cutest one.
4. If several cards sit side by side, keep the icon family consistent across them.
5. Prefer generic symbols over very specific objects unless the slide is truly about that object.
6. Avoid brand icons, novelty icons, mascots, food, anatomy, vehicles, or hobby objects unless the content is literally about them.
7. For PPTX output, export a PNG first and place the PNG, not the raw SVG.

## Fast workflow

1. Start with a curated topic:
   - `python scripts/tabler_icons.py topics`
   - `python scripts/tabler_icons.py suggest roadmap`
2. If the shortlist is close but not perfect, run a keyword search:
   - `python scripts/tabler_icons.py search "chart arrow"`
   - `python scripts/tabler_icons.py search "team"`
3. Export the chosen icon:
   - `python scripts/tabler_icons.py export-png chart-bar tmp/chart-bar.png --size 512`
4. Place the PNG and keep icon size visually subordinate to the actual message.

## Curated presentation topics

### Process / workflow

Use for step flows, operating models, transformations, and handoffs.

Recommended icons:
- `route`
- `route-2`
- `hierarchy-2`
- `arrow-ramp-right`
- `arrows-right`

### Roadmap / timeline

Use for phased plans, milestones, delivery sequences, and future-state pathing.

Recommended icons:
- `map-route`
- `flag`
- `calendar-week`
- `calendar-time`
- `target-arrow`

### Analytics / evidence

Use for charts, dashboards, proof points, and quantitative argument.

Recommended icons:
- `chart-bar`
- `chart-line`
- `chart-pie-2`
- `chart-donut`
- `report-analytics`

### Growth / performance

Use for growth stories, momentum, upside, and progress framing.

Recommended icons:
- `trending-up`
- `trending-up-2`
- `growth`
- `rocket`
- `target-arrow`

### People / stakeholders

Use for org slides, audiences, team structures, and user groups.

Recommended icons:
- `users`
- `users-group`
- `users-plus`
- `message-user`
- `hierarchy-2`

### Product / platform / system

Use for tech stacks, applications, digital services, and system views.

Recommended icons:
- `devices`
- `devices-2`
- `stack`
- `stack-2`
- `app-window`

### Communication / collaboration

Use for feedback loops, messaging, workshops, and adoption/change slides.

Recommended icons:
- `message`
- `messages`
- `message-dots`
- `message-user`
- `speakerphone`

### Risk / security / control

Use for risks, mitigations, controls, compliance, and issue framing.

Recommended icons:
- `shield`
- `shield-check`
- `shield-lock`
- `alert-triangle`
- `alert-circle`

### Finance / value

Use for revenue, cost, savings, pricing, and value creation.

Recommended icons:
- `coin`
- `coins`
- `wallet`
- `report-money`
- `pig-money`

### Timing / schedule

Use for cadence, planning, deadlines, and delivery timing.

Recommended icons:
- `calendar`
- `calendar-week`
- `calendar-time`
- `clock`
- `alarm`

### Geography / footprint

Use for markets, site networks, presence, and multi-location framing.

Recommended icons:
- `globe`
- `building`
- `buildings`
- `map-route`
- `flag`

### Quality / validation / completion

Use for checklists, validation, assurance, and done-state signaling.

Recommended icons:
- `check`
- `checklist`
- `list-check`
- `flag-check`
- `target-arrow`

## Preference heuristics when two icons are both acceptable

- Prefer `chart-bar` over `report-analytics` when the point is data.
- Prefer `target-arrow` over `rocket` when the point is focus rather than hype.
- Prefer `users-group` over `users-plus` when the point is an existing audience rather than growth.
- Prefer `shield-check` over `alert-triangle` when the story is control, not risk.
- Prefer `map-route` over `flag` when the story is journey, not milestone.
- Prefer `stack-2` or `devices` over very specific hardware icons unless the hardware matters.

## Safe defaults

If in doubt, start with one of these:
- `route`
- `map-route`
- `chart-bar`
- `users-group`
- `shield-check`
- `calendar-week`
- `stack-2`
- `checklist`
