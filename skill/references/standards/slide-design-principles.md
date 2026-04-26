# Slide Design Principles
**A visual execution guide. Layout, typography, whitespace, and visual hierarchy.**

> This document covers *how a slide should look*, not what it should say. It assumes the action title, storyline, and content decisions are already made.

---

## 1. Canvas and margins

**Slide aspect ratio: 16:9.** Standard dimensions: 13.33" × 7.5" (or 1920 × 1080 px).

**Margins are non-negotiable.** Content never touches the edge of the slide.

- Left and right margin: **0.5"–0.7"** (≈ 4–5% of slide width)
- Top margin: **0.4"–0.5"**
- Bottom margin: **0.4"–0.5"**, with footer content sitting inside this zone

The margin is the slide's frame. Text, charts, photos, and shapes all stop at the margin line. Crossing it makes the slide feel cramped and amateurish; staying too far inside it wastes canvas.

**Do not stretch content edge-to-edge** unless intentionally creating a full-bleed slide (background photo, color block). Even then, foreground text still respects the margin.

---

## 2. Layout zones

Every slide divides into four horizontal bands, top to bottom:

| Zone | Vertical share | Contents |
|---|---|---|
| **Title band** | top ~15% | Title, optional subtitle |
| **Body** | middle ~75% | Chart, diagram, text, image — the proof |
| **Footer band** | bottom ~5–8% | Source, page number |
| **Margin** | edges | Empty by definition |

A thin horizontal rule (0.5–0.75pt, light gray) may sit just above the footer to separate it from the body. Optional, but if used, apply consistently to every slide.

### Title band
- Title sits flush with the **top margin**, aligned **left**
- Maximum **2 lines**
- **No terminal period.** Titles are statements, not sentences in prose.
- Optional subtitle below the title, smaller, lighter weight, also left-aligned

### Body
- Begins ~0.3" below the title band
- Centered horizontally within the margins, OR left-anchored to the left margin (pick one rule per deck)
- Should breathe — typically only 60–80% of the body zone is occupied; the rest is whitespace

### Footer
- Source line, **lower-left**, sitting on the bottom margin
- Page number, **lower-right**, sitting on the bottom margin
- Both share the same baseline (vertical alignment)
- Both in the same font, same size, same color

---

## 3. Typography hierarchy

Use **two type families**: one for headlines, one for body. Never more.

### Sizes (16:9 slide, 13.33" wide)

| Element | Size | Weight | Notes |
|---|---|---|---|
| Title | **24–28pt** | Bold or Regular (decide once per deck) | Max 2 lines, no period |
| Subtitle | 14–16pt | Regular | Smaller and lighter than title |
| Body text | **14–18pt** | Regular | Never below 12pt |
| Chart axis labels | **10–12pt** | Regular | Never below 9pt |
| Chart data labels | 11–14pt | Bold on focal series | Direct on chart, not in legend |
| Chart titles / subtitles inside the body | 12–14pt | Bold | Distinct from slide title |
| Footer (source, page #) | **9–10pt** | Regular | Light gray, never black |
| Footnote markers (¹, ²) | 7–8pt | Regular | Superscript |

### Hierarchy ratios
The size ratio between levels matters more than the absolute size:
- Title to body: roughly **1.6×–2×**
- Body to footer: roughly **1.5×–1.8×**

If the title is only slightly larger than the body, the hierarchy collapses and the eye doesn't know where to start.

### Line spacing
- Title leading: **1.1–1.15×** font size
- Body leading: **1.2–1.3×** font size
- Tight leading on titles; generous on body

### Alignment
- **Left-align by default.** Centered text is reserved for hero stats and quote slides.
- Justified text never. It creates rivers of whitespace.

---

## 4. Whitespace

Whitespace is the most underused design tool. **A slide that feels too empty is usually correct.**

### Rules

- The body zone should occupy at most **80%** of its allotted area. The remaining 20% is breathing room.
- Around any focal element (a hero stat, a key callout, a single chart), reserve **at least one line-height of clearance** on all sides.
- Do not add elements *to fill space.* Empty space is not a problem to solve.
- If the slide feels sparse, the answer is rarely "add content." It is usually "make the existing content larger."

### Test
If you removed every element except the action title and one chart/diagram, would the slide still be informative? If yes, the rest is probably clutter.

---

## 5. Visual hierarchy — focusing attention

Every slide must answer: **where does the eye go first?**

### One focal element per slide
Pick the one thing that proves the title. Make it visually dominant by combining at most two of:
- **Larger size** than surrounding elements
- **Stronger color** (the accent color)
- **Bolder weight**

Do not combine all three on the same element — it becomes shouting. Two is enough.

### Demote everything else
The non-focal elements support the focal one. Make them recede:
- Smaller, lighter, gray
- Thinner lines
- Muted versions of the accent color, or simply gray scale

### Use of color
- **One accent color per slide.** Used to mark exactly the part the title talks about.
- Everything else: grays, blacks, whites, or muted tones.
- Color used "to look nice" or "for variety" destroys hierarchy. Each color application should answer: *what does this color tell the reader?*

### Direction of reading
The eye reads top-left → bottom-right (in Latin scripts). Place the focal element where the eye lands first: upper-left for the title, then the focal body element along the diagonal toward lower-right.

---

## 6. Charts — design principles

Default chart settings from any tool are wrong for presentation slides. They are designed for analyst screens, not projected slides. Override them.

### Sizing
- Chart fonts must be **at least 10pt**, ideally 12pt. Default chart fonts (often 8pt) are unreadable when projected.
- Bars and lines should be thick enough to read from across a room. Default thin lines (1pt) often need to become 2–3pt.

### Highlight the focal series
- The series the title talks about is rendered in the **accent color** with **bold data labels**.
- All other series are rendered in **gray** with **lighter labels** or no labels at all.
- This single move is what transforms a default chart into a presentation chart.

### Direct labeling > legends
- Place series labels **directly next to the line/bar/segment they identify**, in the same color as the data.
- Legends sitting in a corner force the eye to bounce. Direct labels keep the eye on the data.
- Delete the legend entirely once labels are direct.

### Annotations on the chart
- The "so what" of the chart goes ON the chart itself: a callout circle, an arrow, a bracket, or a brief text annotation pointing to the key data point.
- Annotations are in the accent color, body font, ~11–12pt.
- Use sparingly: 1–2 annotations per chart. More than that and the chart becomes an infographic.

### Strip the chrome
Default charts include visual debris that obscures the data. Remove or mute:
- Heavy borders around the plot area → delete
- Background fill → make white/transparent
- Gridlines → keep only one direction (usually horizontal), in light gray; or delete entirely
- Tick marks → delete
- Trailing zeros on axis labels (1,000.00 → 1,000) → simplify
- Diagonal axis text → rotate to horizontal; if it doesn't fit, abbreviate the labels

### Axis discipline
- **Bar charts must start at zero.** Truncating a bar chart's baseline is misleading.
- Line charts may use a non-zero baseline if it improves readability — but be honest about it.
- Axis titles should be brief and include units: `Revenue ($M)` not `Revenue in millions of dollars`.
- Y-axis title may be set in light gray and rotated 90° on the left, or replaced by a horizontal label above the axis.

### One chart per slide
If two charts compete for attention on the same slide, the eye chooses neither. Either combine into one chart, or split into two slides. Exception: a deliberate side-by-side comparison where the parallel structure is the point — then both charts use identical formatting and are clearly framed as a pair.

---

## 7. Color discipline

A slide deck needs a **color palette of roughly 5 colors**, no more:

| Role | Quantity | Purpose |
|---|---|---|
| **Background** | 1–2 | Usually white; a dark/colored alternate for special slides |
| **Primary text** | 1 | Near-black on light bg, near-white on dark bg |
| **Muted text / non-focal data** | 1–2 grays | For secondary information |
| **Accent** | 1 | The one color that signals focus |
| **Optional second accent** | 1 | For semantic dual-coding (e.g., positive vs. negative); use only if needed |

### Rules
- The accent color is used **exactly once per slide**, on the focal element. If it's used decoratively elsewhere, it loses its function.
- Grays are used to demote. They are not "filler" colors — they are deliberate signals that "this is context, not the point."
- Backgrounds are solid or very subtle gradient. No textures, patterns, or images behind text.
- Text on colored backgrounds must meet contrast ratios: 4.5:1 minimum for body, 3:1 for large headlines.

---

## 8. Alignment and grid

**Every element on every slide should align to a consistent grid.** This is what makes a deck look professional rather than thrown together.

### Across the deck
- Title baseline: identical Y-position on every slide
- Footer baseline: identical Y-position on every slide
- Page number: identical X-position on every slide
- Source line: identical X-position on every slide
- Body content: anchored to a consistent left edge (the left margin)

When you flip through the deck, the title should not move. The footer should not move. Only the body changes.

### Within a slide
- Multi-column layouts: equal column widths, equal gutters
- Bulleted lists: bullets aligned vertically, text indented uniformly
- Logos in a row: equalized to the same visual height (not the same pixel height — visual height accounts for differing logo aspect ratios)
- Numbers in a column: right-aligned (digits line up by place value)

### Tools
Use slide guides / snap-to-grid in the design tool. Eyeballing alignment fails; the eye catches misalignment of even 1–2 pixels and registers the slide as "off" without knowing why.

---

## 9. The pre-design checklist

Before starting design, answer these. The answers dictate every visual choice.

- [ ] What is the **focal element** of this slide? (The one thing the eye should land on first.)
- [ ] What part of the body **proves the title**? (That is what gets the accent color.)
- [ ] What is **context** vs. what is **the point**? (Context goes gray; the point gets the accent.)
- [ ] What can be **removed**? (Iterate; remove until removing more would weaken the slide.)
- [ ] Are the **margins respected**?
- [ ] Are the **typography sizes** within the hierarchy ranges in §3?
- [ ] Is the **footer aligned** correctly (source lower-left, page number lower-right, same baseline)?
- [ ] Do the **chart fonts** meet the 10pt minimum?
- [ ] Is the **focal chart series** in the accent color while the rest is gray?
- [ ] Is the chart **directly labeled** (no legend, or minimal legend)?
- [ ] Across the deck: do **title, footer, and page number** all sit at identical positions?

If every box is checked, the slide is design-complete.

---

## 10. Default values — quick reference

When the design tool asks for a number, use these defaults unless there is a reason not to:

| Element | Default |
|---|---|
| Slide size | 13.33" × 7.5" (16:9) |
| Margin (all sides) | 0.5" |
| Title font size | 24pt |
| Title max lines | 2 |
| Title terminal period | None |
| Subtitle font size | 14pt |
| Body font size | 16pt |
| Chart axis label size | 11pt |
| Chart data label size (focal) | 12pt bold |
| Chart data label size (non-focal) | 11pt regular |
| Footer font size | 10pt |
| Footer color | Light gray (~#888) |
| Body line spacing | 1.25× |
| Title line spacing | 1.1× |
| Accent color uses per slide | Exactly 1 |
| Charts per slide | 1 |

---

*End of guide.*
