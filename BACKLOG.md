# Backlog

Open product/documentation ideas for `deck.md` and the bundled `deck-builder` skill.

## Open

### Integrate with think-cell

- **Status:** idea
- **Added:** 2026-05-05
- **Source:** Rodrigo request

Explore support for think-cell as an optional production path for analytical, chart-heavy decks.

Candidate integration paths:
1. **Python library path** — investigate available think-cell-related Python libraries. Rodrigo notes these may be outdated, but they are worth testing as a direct programmatic bridge if they can still create or manipulate think-cell-compatible chart objects.
2. **think-cell automation JSON path** — investigate think-cell's automation workflow that uses JSON/data specs to drive chart creation or updates. This may be the cleaner target for `deck.md` because the deck spec already separates chart intent, data refs, and production mode.

Reference links:
- think-cell manual: [Automatically create presentations using JSON data](https://www.think-cell.com/en/resources/manual/jsondataautomation)
  - Notes: uses `.ppttc` JSON files plus PowerPoint templates with named elements; supports filling templates with slide titles/charts, reusing/reordering templates, local or remote JSON/template sources, and web-service-driven presentation creation.
- TBD — Python library docs/repos

Questions to resolve:
- Should `deck.md` support a chart-level option such as `chart.engine: think-cell`, or should think-cell be a deck/output-level renderer?
- Should the first implementation generate `.ppttc` JSON plus a required PowerPoint template, target the outdated Python libraries, or support both behind one abstraction?
- Can the workflow generate think-cell-compatible editable charts directly, or should it generate structured chart/data specs for a human/PowerPoint automation step to convert?
- Which chart types matter first: waterfall, Mekko, stacked bars, Gantt/timeline, scatter/bubble, and CAGR/bridge visuals?
- What should happen when think-cell is unavailable or unlicensed on the local machine?
- How should the skill validate that rendered think-cell charts remain editable and visually correct?

Potential acceptance criteria:
- Document the intended think-cell integration model and prerequisites.
- Add schema guidance for selecting think-cell where appropriate.
- Add a safe fallback to native `ppt-shapes`/PowerPoint charts when think-cell is unavailable.
- Include at least one chart-heavy example deck that demonstrates the intended workflow.
