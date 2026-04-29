---
deck:
  title: "The Customer Value Chain"
  objective: "Explain the customer value chain as a vivid map of the customer's lived experience, then show how that map reveals decoupling opportunities."
  audience: "Managers, operators, and students learning decoupling"
  language: "en"
  author: "Rodrigo Lourenco Farinha"
  version: "2026-04-24-v04-vision-designer-approved"

status: "approved"
narrative_template: "scr"

production_defaults:
  default_slide_mode: "designer-mode"
  aspect_ratio: "16:9"

image_generation:
  primary_creator: "gpt-image-2"
  size: "2560x1440"
  quality: "high"
  output_format: "png"
  variants: 1

design_tokens:
  palette:
    primary: "#101820"
    secondary: "#56616D"
    accent: "#1E6BFF"
    accent_soft: "#E7F0FF"
    warm: "#FF7A3D"
    positive: "#16A66A"
    negative: "#E5484D"
    background: "#F7F3EC"
    light: "#FFFFFF"
    line: "#D4D9E2"
  typography:
    title: "Aptos Display"
    body: "Aptos"
    emphasis: "Aptos Display"
  iconography:
    family: "human-centered journey pictograms"
  shape_language:
    corner_style: "subtle"
    line_weight: "thin"
---

## Brief

```yaml
input_type: "content"
input_summary: "Rodrigo asked for a 5-slide designer-mode deck explaining the customer value chain in decoupling, then clarified that it should feel more visionary and inspiring by showcasing the overall customer experience and the activities customers need to perform."
interpretation: "Reframe the deck as a visual walkthrough of the customer's lived experience. The CVC is presented as a panoramic activity sequence first, then as a strategic lens for seeing delight, friction, weak links, and decoupling opportunities."
open_questions: []
```

## Narrative

```yaml
situation: "Every market is experienced by customers as a sequence of things they need to get done."
complication: "Companies often see products, channels, and technologies; customers feel activities, effort, waiting, trust, payment, use, service, and exit."
resolution: "The customer value chain makes the whole experience visible, so managers can design the journey deliberately and protect the activities most vulnerable to decoupling."
```

## Slides

### Slide 1 - "A market is an experience customers move through"

```yaml
id: 1
type: "situation"
layout: "cinematic experience panorama"
mode: "designer-mode"
image_decision: "full-generated-visual"
reading_path: "title -> panoramic customer path -> short definition"
```

Body:
- The customer does not experience a market as a product category.
- They experience a sequence of moments: need, search, compare, buy, receive, use, maintain, and leave.
- The customer value chain is the map of that lived sequence.

```yaml
creative_direction:
  mood: "visionary, warm, premium, human-centered, inspiring"
  metaphor: "a wide cinematic path through the customer's day, with each activity appearing as a moment along the path"
  composition_intent: "Make this feel like an opening visual thesis. Large title at top-left; sweeping customer path across the slide; subtle activity moments embedded in the path. The viewer should immediately feel that strategy starts by seeing the customer's whole experience."
  prompt_notes:
    - "Show a human-centered journey, not a corporate process."
    - "Use activity moments as small visual scenes or icons, not many text boxes."
    - "The image should feel expansive and inviting."
  avoid:
    - "dashboard layout"
    - "generic technology disruption imagery"
    - "firm-side value chain"
    - "stock-photo collage"
required_text:
  title: "A market is an experience customers move through"
  subtitle: "The customer value chain maps the activities customers need to do to get value"
  labels:
    - "Need"
    - "Search"
    - "Compare"
    - "Buy"
    - "Receive"
    - "Use"
    - "Maintain"
    - "Exit"
```

Sources:
- Teixeira, "Disruption Starts with Unhappy Customers, Not Technology" (HBR, 2019)
- Teixeira and Mendes, "How to Improve Your Company's Net Promoter Score" (HBR, 2019)

### Slide 2 - "The customer value chain makes invisible work visible"

```yaml
id: 2
type: "framework"
layout: "activity constellation"
mode: "designer-mode"
image_decision: "full-generated-visual"
reading_path: "title -> clustered customer activities -> insight line"
```

Body:
- Many customer activities are hidden because they happen before or after the transaction.
- Naming the activities reveals the work customers perform to create their own value.
- The chain includes practical, emotional, and trust-building moments.

```yaml
creative_direction:
  mood: "illuminating, visual, thoughtful, strategic"
  metaphor: "a constellation of customer activities lighting up around one customer, turning scattered moments into one visible system"
  composition_intent: "Place the customer as the central anchor, surrounded by activity moments organized from before purchase to after use. This should feel more like revealing a hidden map than listing a process."
  prompt_notes:
    - "Use a visually rich activity map with clear sequence cues."
    - "Show that the customer is doing work, making choices, and managing uncertainty."
    - "Keep the labels legible and sparse."
  avoid:
    - "flat swimlane chart"
    - "dense service blueprint"
    - "tiny labels"
    - "company org chart"
required_text:
  title: "The customer value chain makes invisible work visible"
  subtitle: "Customers create value by moving through activities, not by buying in one instant"
  labels:
    - "Discover"
    - "Evaluate"
    - "Choose"
    - "Pay"
    - "Receive"
    - "Use"
    - "Solve problems"
    - "Renew or leave"
```

### Slide 3 - "Every activity has an emotional signature"

```yaml
id: 3
type: "analysis"
layout: "experience emotion curve"
mode: "designer-mode"
image_decision: "full-generated-visual"
reading_path: "title -> experience curve -> three emotional zones"
```

Body:
- Customers feel pleasure in some activities, neutrality in others, and annoyance in others.
- One final satisfaction score hides these shifts.
- The strategic question is where the experience lifts the customer up and where it drains them.

```yaml
creative_direction:
  mood: "emotional, elegant, memorable, clear"
  metaphor: "a customer experience curve flowing over the same activity path, with bright peaks and darker friction valleys"
  composition_intent: "A large flowing curve over the journey should dominate the slide. Use color to show value-creating, value-charging, and value-eroding moments. The slide should help the audience feel the journey, not just analyze it."
  prompt_notes:
    - "Make the experience curve visually beautiful and readable."
    - "Show emotional movement across activities."
    - "Use the hotel/NPS article logic without making this a hotel case slide."
  avoid:
    - "busy analytics dashboard"
    - "many plotted series"
    - "paragraph-heavy annotations"
required_text:
  title: "Every activity has an emotional signature"
  subtitle: "Some moments create value, some charge for value, and some erode value"
  labels:
    - "Value-creating"
    - "Value-charging"
    - "Value-eroding"
    - "WOW moment"
    - "Friction"
```

### Slide 4 - "Weak activities are where decoupling begins"

```yaml
id: 4
type: "complication"
layout: "activity peel-away moment"
mode: "designer-mode"
image_decision: "full-generated-visual"
reading_path: "title -> weak activity in the journey -> challenger peel-away"
```

Body:
- Disruptors do not need to steal the whole customer relationship.
- They can take the activity customers dislike, delay, or overpay for.
- The customer value chain shows exactly which activity is exposed.

```yaml
creative_direction:
  mood: "dramatic but disciplined, strategic, high-trust"
  metaphor: "one painful activity segment lifting away from the customer journey into the hands of a focused challenger"
  composition_intent: "Show the same customer path, but now one friction-heavy activity is visibly peeling out of the chain. The visual should make decoupling feel obvious: the vulnerable customer activity separates from the incumbent bundle."
  prompt_notes:
    - "Make the weak activity the focal point."
    - "Show a challenger capturing one activity, not the whole journey."
    - "Keep the visual inspiring and strategic, not alarmist."
  avoid:
    - "battlefield metaphors"
    - "crisis imagery"
    - "startup logo collage"
    - "over-detailed arrows"
required_text:
  title: "Weak activities are where decoupling begins"
  subtitle: "A challenger can win by making one painful customer activity easier"
  labels:
    - "Weak activity"
    - "Focused challenger"
    - "Incumbent bundle"
```

### Slide 5 - "The strategic task is to redesign the experience before customers unbundle it"

```yaml
id: 5
type: "recommendation"
layout: "future-state customer experience"
mode: "designer-mode"
image_decision: "full-generated-visual"
reading_path: "title -> redesigned journey -> three manager moves"
```

Body:
- Map the complete customer experience, including activities outside the transaction.
- Amplify the WOW moments that create advocacy and momentum.
- Remove or recouple the weak moments before someone else owns them.

```yaml
creative_direction:
  mood: "optimistic, visionary, managerial, polished"
  metaphor: "the customer journey redesigned into a smoother, brighter future-state path"
  composition_intent: "End with a hopeful redesigned experience: the journey is smoother, weak links are repaired, and managers have three clear moves. This should feel like a call to design the whole experience, not just defend against disruption."
  prompt_notes:
    - "Make the ending inspiring and actionable."
    - "Show a before-to-future improvement without creating a dense roadmap."
    - "Use the 119% referral example only as a small proof cue if it fits cleanly."
  avoid:
    - "metric-card grid"
    - "generic transformation roadmap"
    - "technology-threat cliches"
    - "overstuffed playbook"
required_text:
  title: "The strategic task is to redesign the experience before customers unbundle it"
  subtitle: "Map the whole journey, amplify delight, repair friction"
  labels:
    - "Map the whole experience"
    - "Amplify WOW moments"
    - "Repair weak links"
```

## Notes to the agent

- Rodrigo approved this `deck.md` in chat on 2026-04-24.
- Designer-mode generation should use GPT Image 2 directly, one slide at a time, at `2560x1440`, high quality.
- After approval, produce both PPTX and PDF.
- Use a visionary customer-experience visual language: panoramic journeys, human activity moments, experience curves, and redesigned paths.
- The deck should showcase what customers need to do across the overall experience, not feel like a framework table.
- Source PDF: `/Users/rodrigo/Zotero/storage/DMJIUR8S/Teixeira - 2019 - Disruption Starts with Unhappy Customers, Not Technology.pdf`
- Source HTML: `/Users/rodrigo/Zotero/storage/M9NBZ3F6/Teixeira and Mendes - 2019 - How to Improve Your Company’s Net Promoter Score.html`
- Avoid dense article quotation; paraphrase the source concepts.
- Add an editable source footer in the assembled PPTX/PDF rather than relying on generated text inside images.
