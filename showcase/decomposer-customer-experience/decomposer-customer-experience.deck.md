---
deck:
  title: "Do You Know Where Your Customer Experience Hurts?"
  objective: "Use SCR to show why Decomposer helps companies move beyond aggregate CX scores and see the specific moments customers feel value or pain."
  audience: "Marketing leaders, customer experience leaders, strategy teams, and event or LinkedIn audiences"
  language: "en"
  author: "Rodrigo Lourenco Farinha"
  version: "2026-04-24-v03-full-slide-pdf"

status: "approved"
narrative_template: "scr"

production_defaults:
  default_slide_mode: "designer-mode"
  aspect_ratio: "16:9"
  final_output: "pdf-only"
  editability: "not editable"
  text_rendering: "full slide copy generated inside the slide image"
  logo_treatment: "supplied Decomposer logo flattened into every slide as a small fixed top-left mark, preserving generated slide composition"
  page_numbering: "small numeric page marker in the bottom-right corner of every slide"
  searchable_pdf: "create an OCR/searchable PDF version with Tesseract when OCRmyPDF is unavailable"

image_generation:
  primary_creator: "gpt-image-2"
  size: "2560x1440"
  quality: "high"
  output_format: "png"
  variants: 1

design_tokens:
  palette:
    primary: "#1CE3CC"
    background: "#04090C"
    background_alt: "#0B0F19"
    white: "#FFFFFF"
    gray: "#A0AEC0"
    line: "#1CE3CC40"
    red: "#EF4444"
    red_soft: "#EF444426"
    blue: "#3B82F6"
    purple: "#6D28D9"
    green: "#10B981"
  typography:
    title: "large modern presentation typography"
    body: "clean modern presentation typography"
  visual_style: "inspiring Decomposer-dark visual story; cinematic customer journeys, luminous voice signals, emotional heat, premium LinkedIn/event-ready imagery"
  source_brand: "Decomposer website CSS and supplied white logo"
---

## Brief

```yaml
input_type: "content"
input_summary: "Rodrigo approved the designer-mode SCR storyline, then clarified the production target: no editable PPTX, no text-free visual plates, and no separate overlay workflow. Produce only a PDF. The Decomposer logo should appear on all slides in the same place, without overlapping titles. Add a final contact slide that says Learn more and shows https://www.decomposer.ai/."
interpretation: "Keep the approved SCR narrative and use the generated slide images as the main visual output. Because some generated titles sit high on the canvas, do not rebuild or crop the slides. Instead, flatten a smaller supplied Decomposer logo into the same top-left position on every slide, preserving the generated composition while avoiding title overlap."
open_questions: []
```

## Narrative

```yaml
situation: "A market is an experience customers move through. The customer value chain makes that experience visible by naming the activities customers must perform to get value."
complication: "Most companies still manage experience through aggregate metrics such as NPS. They may know the relationship is warmer or colder, but they do not know which activity is creating pain."
resolution: "Decomposer helps you listen to your customer, maps those voices to the customer value chain, and shows where to fix the experience."
```

## Slides

### Slide 1 - "Do you know where your customer experience hurts?"

```yaml
id: 1
type: "section_divider"
layout: "cinematic branded cover"
mode: "designer-mode"
image_decision: "full-generated-slide-with-text"
required_text:
  title: "Do you know where your customer experience hurts?"
  subtitle: "Decomposer turns customer voices into a map of the moments that create value or pain"
  labels: []
```

### Slide 2 - "A market is an experience customers move through"

```yaml
id: 2
type: "situation"
layout: "human journey through activities"
mode: "designer-mode"
image_decision: "full-generated-slide-with-text"
required_text:
  title:
    - "A market is an experience"
    - "customers move through"
  subtitle: "Customers feel activities, not averages"
  labels:
    - "Discover"
    - "Compare"
    - "Choose"
    - "Pay"
    - "Receive"
    - "Use"
    - "Get help"
    - "Stay or leave"
```

### Slide 3 - "The customer value chain makes invisible work visible"

```yaml
id: 3
type: "situation"
layout: "hidden work revealed as map"
mode: "designer-mode"
image_decision: "full-generated-slide-with-text"
required_text:
  title: "The customer value chain makes invisible work visible"
  subtitle: "Customers create value by moving through activities, not by buying in one instant"
  labels:
    - "Before"
    - "During"
    - "After"
    - "Value created"
    - "Value charged"
    - "Value eroded"
```

### Slide 4 - "Every activity has an emotional signature"

```yaml
id: 4
type: "analysis"
layout: "emotional signal curve"
mode: "designer-mode"
image_decision: "full-generated-slide-with-text"
required_text:
  title:
    - "Every activity has an"
    - "emotional signature"
  subtitle: "Some moments create value, some charge for value, and some erode value"
  labels:
    - "Strong link"
    - "WOW"
    - "Weak link"
    - "Friction"
```

### Slide 5 - "You measure NPS. But do you know where it hurts?"

```yaml
id: 5
type: "complication"
layout: "aggregate score masking pain"
mode: "designer-mode"
image_decision: "full-generated-slide-with-text"
required_text:
  title: "You measure NPS. But do you know where it hurts?"
  subtitle: "A score can show the symptom, but not the activity causing the pain"
  labels:
    - "NPS"
    - "Hidden friction"
    - "Which activity?"
```

### Slide 6 - "Decomposer helps you listen to your customer"

```yaml
id: 6
type: "recommendation"
layout: "customer voices becoming experience intelligence"
mode: "designer-mode"
image_decision: "full-generated-slide-with-text"
required_text:
  title: "Decomposer helps you listen to your customer"
  subtitle: "Thousands of voices become clear experience signals"
  labels:
    - "Voices"
    - "Feedback"
    - "Signals"
    - "Experience"
```

### Slide 7 - "Now you know where to fix the experience"

```yaml
id: 7
type: "analysis"
layout: "fix-priority experience map"
mode: "designer-mode"
image_decision: "full-generated-slide-with-text"
required_text:
  title: "Now you know where to fix the experience"
  subtitle: "Customer voices point to the moments that need repair first"
  labels:
    - "Fix here"
    - "Repair first"
    - "Strong link"
    - "Protect"
```

### Slide 8 - "Stop scorekeeping. Start repairing."

```yaml
id: 8
type: "next_steps"
layout: "final keynote hook"
mode: "designer-mode"
image_decision: "full-generated-slide-with-text"
required_text:
  title: "Stop scorekeeping. Start repairing."
  subtitle: "Start improving your customer experience"
  labels:
    - "Stop scorekeeping"
    - "Keep listening"
    - "Repair"
    - "Improve"
```

### Slide 9 - "Learn more"

```yaml
id: 9
type: "contact"
layout: "final contact slide"
mode: "designer-mode"
image_decision: "rasterized-contact-slide"
required_text:
  title: "Learn more"
  subtitle: "https://www.decomposer.ai/"
  labels: []
```

## Notes to the agent

- Produce PDF only. Do not create a PPTX.
- Generate complete slide images, not text-free plates.
- The final PDF should be non-editable: all text and visuals are rasterized inside page images.
- Use the supplied Decomposer white horizontal logo from `/Users/rodrigo/Downloads/logo_color_horizontal_branco_flat-eF-a0nfr.png`, flattened into final images.
- Put the logo in the same place on every slide: 56 px from the left, 56 px from the top, 220 px wide on a 2560 x 1440 canvas.
- Keep the real logo small enough that it does not overlap generated titles. Do not crop, shrink, or rebuild the slide composition to solve logo overlap.
- Prompts should instruct the image model to leave the top-left region calm; if a future slide still overlaps, regenerate that slide with a stronger logo-safe instruction rather than distorting the final image.
- Add small slide page numbers in the bottom-right corner as `1`, `2`, `3`, etc. Do not show the total page count.
- Build a searchable OCR copy of the final PDF when OCR tooling is available.
- Treat the Decomposer website as brand inspiration: near-black background, white logo/type, electric turquoise primary signal, cool gray support text, red for friction, and blue/purple/green as secondary activity signals.
- The final deck should feel suitable for LinkedIn carousel screenshots, event talks, and premium thought-leadership use.

## Sources

- Decomposer website: https://www.decomposer.ai
- Supplied Decomposer white logo: `/Users/rodrigo/Downloads/logo_color_horizontal_branco_flat-eF-a0nfr.png`
