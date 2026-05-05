# Backlog

Open product/documentation ideas for `deck.md` and the bundled `deck-builder` skill.

## Open

### Integrate with think-cell

- **Status:** idea
- **Added:** 2026-05-05
- **Source:** Rodrigo request

Explore support for think-cell as an optional production path for analytical, chart-heavy decks.

Questions to resolve:
- Should `deck.md` support a chart-level option such as `chart.engine: think-cell`, or should think-cell be a deck/output-level renderer?
- Can the workflow generate think-cell-compatible editable charts directly, or should it generate structured chart/data specs for a human/PowerPoint automation step to convert?
- Which chart types matter first: waterfall, Mekko, stacked bars, Gantt/timeline, scatter/bubble, and CAGR/bridge visuals?
- What should happen when think-cell is unavailable or unlicensed on the local machine?
- How should the skill validate that rendered think-cell charts remain editable and visually correct?

Potential acceptance criteria:
- Document the intended think-cell integration model and prerequisites.
- Add schema guidance for selecting think-cell where appropriate.
- Add a safe fallback to native `ppt-shapes`/PowerPoint charts when think-cell is unavailable.
- Include at least one chart-heavy example deck that demonstrates the intended workflow.
