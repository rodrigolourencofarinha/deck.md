---
schema_version: deck-md/v2-alpha
status: approved

deck:
  title: "What's new with Codex"
  objective: "Update the Codex pitch deck with a branded OpenAI cover, high-resolution Codex logo usage, more explanatory sales copy on the feature slides, a strategic enterprise-adoption slide, and a final Learn more slide."
  audience: "Product, GTM, and enterprise audiences that need a fast, attractive Codex feature story"
  language: en
  author: "Claw for Rodrigo Lourenço Farinha"
  version: "2026-04-29-review-10-right-image-swap"
  expected_slide_count: 7

narrative_template: problem-solution

production_defaults:
  default_slide_mode: designer-mode
  aspect_ratio: "16:9"
  footer:
    page_numbers: true
    page_number_format: "{page}"
    cr_mark: false
    cr_text: ""
    placement: bottom-left-cr-bottom-right-page

image_generation:
  model: "gpt-image-2"
  primary_auth: "codex-oauth"
  fallback_auth: "openai-api-key"
  fallback_requires_user_approval: true
  size: "2048x1152"
  quality: "high"
  output_format: "png"
  variants: 1

designer_assets:
  - id: openai_wordmark
    type: logo
    path: "assets/source/official-openai/openai-wordmark-black.svg"
    prepared_path: "assets/prepared/logos/openai-wordmark-black.png"
    usage: "Official OpenAI wordmark/logo reference. Use on the cover and final learn-more slide; keep crisp, minimal, and secondary to the title."
    scope: deck
    required: false
  - id: codex_lockup
    type: logo
    path: "assets/source/official-openai/codex-lockup-black.svg"
    prepared_path: "assets/prepared/logos/codex-lockup-black.png"
    usage: "Official black Codex identity reference. Place small and cleanly where requested; do not distort."
    scope: deck
    required: false
  - id: codex_high_res_logo
    type: logo
    path: "assets/source/user-logos/codex-logo-high-res.tiff"
    prepared_path: "assets/prepared/imagegen/codex-logo-high-res.png"
    usage: "Rodrigo-supplied high-resolution Codex/color logo. Use as the primary color logo asset in the cover and selected brand moments; keep rounded/clean, high resolution, and do not recolor."
    scope: deck
    required: true
  - id: codex_color_logo_reference
    type: logo
    path: "assets/source/user-logos/codex-color-logo-reference.jpg"
    source_url: "https://pnghdpro.com/openai-codex-logo/"
    usage: "Earlier Rodrigo-supplied color Codex logo/reference. Secondary fallback only; prefer codex_high_res_logo."
    scope: deck
    required: false
  - id: computer_use_logo_rounded_primary
    type: logo
    path: "assets/source/user-logos/computer-use-logo-rounded-01.jpg"
    usage: "Rodrigo-supplied Computer Use logo with rounded-corner treatment. Use on the browser/computer-use slide near or over the central Computer Use image card."
    scope: slide
    required: true
  - id: computer_use_logo_rounded_wide
    type: logo
    path: "assets/source/user-logos/computer-use-logo-rounded-02.jpg"
    usage: "Rodrigo-supplied alternate Computer Use logo/reference. Use only if the wider format fits better than the square logo."
    scope: slide
    required: false
  - id: slide_3_current_reference
    type: slide-preview
    path: "assets/source/user-reference/slide-3-current-reference.jpg"
    usage: "Rodrigo-supplied screenshot of the previous Computer Use slide. Use as a composition reference for regenerating the browser/computer-use slide with the Computer Use logo added."
    scope: slide
    required: true
  - id: codex_multitask_screenshot
    type: screenshot
    path: "assets/source/official-openai/codex-app-multitask-light.webp"
    usage: "Official Codex app screenshot. Use as source visual for the workspace/multitask idea; can be cropped or framed inside a device/window."
    scope: slide
    required: false
  - id: codex_browser_screenshot
    type: screenshot
    path: "assets/source/official-openai/codex-app-browser-light.webp"
    usage: "Official Codex in-app browser screenshot. Use for browser/verification slide as a real product image reference."
    scope: slide
    required: false
  - id: codex_computer_use_screenshot
    type: screenshot
    path: "assets/source/official-openai/codex-app-computer-use-approval-light.webp"
    usage: "Official Codex Computer Use approval screenshot. Use for computer-use/verification slide as a real product image reference."
    scope: slide
    required: false
  - id: codex_artifact_viewer_screenshot
    type: screenshot
    path: "assets/source/official-openai/codex-app-artifact-viewer-light.webp"
    usage: "Official Codex artifact viewer screenshot. Use for artifact-generation/workspace slide."
    scope: slide
    required: false
  - id: codex_automation_screenshot
    type: screenshot
    path: "assets/source/official-openai/codex-app-automation-light.webp"
    usage: "Official Codex automation screenshot. Use for automations/reusable workflow slide."
    scope: slide
    required: false
  - id: codex_skills_screenshot
    type: screenshot
    path: "assets/source/official-openai/codex-app-skills-light.webp"
    usage: "Official Codex skills picker screenshot. Use for plugins/skills/reusable workflow slide."
    scope: slide
    required: false
  - id: codex_wallpaper
    type: reference-image
    path: "assets/source/official-openai/codex-wallpaper-1.webp"
    usage: "Official Codex abstract wallpaper. Use as subtle atmospheric reference/background texture only if it does not make the deck too decorative."
    scope: deck
    required: false
  - id: openai_presentation_reference
    type: reference-image
    path: "assets/source/user-reference/openai-presentation-reference.jpg"
    usage: "Rodrigo-supplied OpenAI presentation reference: big editorial title, clean white background, product/news image cards, restrained black typography, minimal chrome. Use as style/mood reference only."
    scope: deck
    required: false
  - id: explanatory_text_reference_01
    type: reference-image
    path: "assets/source/user-reference/explanatory-text-reference-01.jpg"
    usage: "Rodrigo-supplied reference for adding slightly more explanatory text while keeping an OpenAI-style visual rhythm. Use for text density guidance only."
    scope: deck
    required: false
  - id: explanatory_text_reference_02
    type: reference-image
    path: "assets/source/user-reference/explanatory-text-reference-02.jpg"
    usage: "Rodrigo-supplied reference for concise section labels and explanatory rows. Use for text density guidance only."
    scope: deck
    required: false
  - id: explanatory_text_reference_03
    type: reference-image
    path: "assets/source/user-reference/explanatory-text-reference-03.jpg"
    usage: "Rodrigo-supplied reference for balancing product imagery with a bit more explanatory copy. Use for text density guidance only."
    scope: deck
    required: false
  - id: slide_6_overload_reference
    type: slide-preview
    path: "assets/source/user-reference/slide-6-overload-reference.jpg"
    usage: "Rodrigo-supplied reference showing slide 6/text-density concern. Use to avoid overloaded required text and favor factual proof cards."
    scope: slide
    required: false
  - id: slide_4_middle_photo_new
    type: screenshot
    path: "assets/source/user-reference/queued-edits/mid-photo-new-02.jpg"
    prepared_path: "assets/prepared/queued-edits/mid-photo-new-02.png"
    usage: "Rodrigo-supplied replacement image for the middle product card on the workflows slide."
    scope: slide
    required: true
  - id: slide_4_middle_photo_change_reference
    type: slide-preview
    path: "assets/source/user-reference/queued-edits/mid-photo-new-01.jpg"
    prepared_path: "assets/prepared/queued-edits/mid-photo-new-01.png"
    usage: "Rodrigo-supplied reference screenshot indicating the slide/card to change: replace the middle photo/card with the new supplied image."
    scope: slide
    required: false
  - id: slide_7_remove_photo_reference
    type: slide-preview
    path: "assets/source/user-reference/queued-edits/slide-7-remove-photo-reference.jpg"
    prepared_path: "assets/prepared/queued-edits/slide-7-remove-photo-reference.png"
    usage: "Rodrigo-supplied reference for final slide change: remove the photo/product screenshot and keep only the OpenAI logo/closing text."
    scope: slide
    required: false
  - id: slide_3_right_image_change_reference
    type: slide-preview
    path: "assets/source/user-reference/queued-edits/right-image-change-reference.jpg"
    prepared_path: "assets/prepared/queued-edits/right-image-change-reference.png"
    usage: "Rodrigo-supplied reference screenshot indicating the right image/card to swap on the GPT-5.5 proof slide."
    scope: slide
    required: false
  - id: slide_3_right_image_new
    type: screenshot
    path: "assets/source/user-reference/queued-edits/right-image-new.jpg"
    prepared_path: "assets/prepared/queued-edits/right-image-new.png"
    usage: "Rodrigo-supplied replacement image for the right product card on the GPT-5.5 proof slide."
    scope: slide
    required: true

analysis_artifacts:
  manifest: "analysis/manifest.yaml"
  notes: "analysis/notes.md"

design_tokens:
  palette:
    primary: "#000000"
    secondary: "#333333"
    accent: "#000000"
    accent_soft: "#F4F4F4"
    background: "#FFFFFF"
    line: "#D9D9D9"
    color_logo_only: "Use color only inside supplied OpenAI/Codex/Computer Use logo assets; avoid decorative color elsewhere."
  typography:
    title: "OpenAI Sans Semibold, Inter, Helvetica Neue, Arial"
    body: "OpenAI Sans Regular, Inter, Helvetica Neue, Arial"
    emphasis: "OpenAI Sans Medium, Inter Medium"
  spacing:
    outer_margin: "88px"
    block_gap: "28px"
  shape_language:
    corner_style: "soft-rounded, 18-28px radius"
    line_weight: "1px hairline rules"
---

# What's new with Codex

## Revision Brief

Rodrigo supplied a high-resolution Codex/logo file and tightened the slide sequence:

- Use the high-resolution logo asset instead of the lower-resolution color logo where possible
- Keep the branded cover: “What's new with Codex”
- Use these core content slides in order:
  1. “Codex turns coding into an AI workspace for real work”
  2. “GPT-5.5 makes Codex stronger on complex, long-running work”
  3. “Codex turns repeat work into reusable workflows”
  4. “Browser and computer use let Codex automate real work, not just write code”
- Change slide 6 to an enterprise-adoption slide with acceleration, flywheel, what-changed, and execution-layer takeaway
- Keep the final “Learn more” slide with https://openai.com/codex/code
- Keep the browser/computer-use slide using the supplied Computer Use logo with rounded corners
- Add slightly more explanatory sales copy to the core feature slides so each slide explains what is new, not just names the feature
- Make slide 6 more strategic and less overloaded: fewer required lines, clearer hierarchy, and a concise enterprise-adoption story
- Revise slide 6 again to reduce required text further and replace general points with source-backed facts: adoption growth, named enterprise examples, use-case categories, and Codex Labs/GSI scale path

## Narrative

```yaml
problem: "Codex is still easy to describe too narrowly as a coding assistant, even though the latest announcements broaden it into an AI workspace."
solution: "Pitch Codex as the workspace layer that can reason, use tools, verify work, create artifacts, remember context, automate workflows, and scale across teams."
why_now: "April 2026 updates introduced GPT-5.5 in Codex, browser/computer use, richer app workflows, memory/automation improvements, and a new enterprise scale motion."
```

## Creative Direction

**Direction: Product-native OpenAI launch deck.** Use real Codex product screenshots as visual anchors, then let GPT Image 2 compose around them in OpenAI's clean product-marketing language.

- **No overlay look:** main titles must be part of the generated slide composition, not post-added text boxes
- **Brand cover:** the first slide should feel like an OpenAI announcement page: clean white canvas, OpenAI logo, strong title, high-resolution Codex logo accent
- **High-res logo:** use `codex_high_res_logo` as the preferred color logo asset; place it sparingly in cover, proof, and closing moments
- **More product reality:** screenshots/logos should appear as real product objects: cropped windows, floating panels, elegant product cards, or logo tiles
- **Color discipline:** keep the deck white/black/grey; use color only inside the supplied logo assets and only in a few deliberate places
- **Computer Use logo:** the browser/computer-use slide must add the supplied Computer Use logo as a rounded-corner logo tile near the Computer Use card
- **Sales-copy density:** slides 2–5 should include a title plus 2–3 short benefit/explainer lines so the audience understands what is new; keep copy punchy, not paragraph-heavy
- **Slide 6 strategy:** avoid listing every detail as required text; use a few headline cards to communicate adoption acceleration, the flywheel, and the platform shift
- **Reference rhythm:** use Rodrigo's supplied OpenAI-presentation reference and the new explanatory-text references for the big editorial title + product/news-card rhythm, but replace generic news tiles with official Codex product screenshots
- **Footer/source:** acceptable as small post-production footer only if needed, but not the title or main content

## Slides

### Slide 1 — "What's new with Codex"

```yaml
id: 1
type: cover
layout: openai-brand-cover
mode: designer-mode
image_decision: full-generated-visual
asset_refs: [openai_wordmark, codex_high_res_logo, codex_lockup, openai_presentation_reference]
source_label: "OpenAI Codex"
```

Create a premium OpenAI-style cover: white canvas, OpenAI logo/wordmark, high-resolution Codex logo accent, and a strong native title. No busy product screenshot grid here; keep it clean and announcement-like.

```yaml
required_text:
  - "What's new with Codex"
```

### Slide 2 — "Codex turns coding into an AI workspace for real work"

```yaml
id: 2
type: executive_summary
layout: product-hero-with-system-map
mode: designer-mode
image_decision: full-generated-visual
asset_refs: [codex_high_res_logo, codex_lockup, codex_multitask_screenshot, codex_artifact_viewer_screenshot, codex_wallpaper, explanatory_text_reference_03]
source_label: "Source: OpenAI Codex changelog, Apr 16 2026; OpenAI enterprise post, Apr 21 2026"
```

Use the official Codex app multitask screenshot as the anchor image. Compose it like a premium product launch hero: screenshot window on the right, minimal system map around it, native title on the left. Add 2–3 concise explainer lines to clarify what changed: Codex now supports parallel work, product artifacts, and an end-to-end work loop.

```yaml
required_text:
  - "Codex turns coding into an AI workspace for real work"
  - "Plan, code, test, and ship in one loop"
  - "Run multiple tasks in parallel"
  - "Turn outputs into artifacts teams can review"
```

### Slide 3 — "GPT-5.5 makes Codex stronger on complex, long-running work"

```yaml
id: 3
type: analysis
layout: model-core-with-product-context
mode: designer-mode
image_decision: full-generated-visual
asset_refs: [codex_high_res_logo, codex_lockup, codex_multitask_screenshot, explanatory_text_reference_01]
source_label: "Source: OpenAI GPT-5.5 launch post, Apr 23 2026; OpenAI Codex changelog, Apr 23 2026"
```

Make this feel like a performance/proof slide, not a benchmark chart. Use one product screenshot panel plus a model-core motif. Keep the two benchmark proof points, but add short benefit copy that explains why GPT-5.5 matters for Codex: stronger long-horizon work, better terminal performance, and more reliable professional software engineering.

```yaml
required_text:
  - "GPT-5.5 makes Codex stronger on complex, long-running work"
  - "Built for longer agent sessions"
  - "82.7% Terminal-Bench 2.0"
  - "58.6% SWE-Bench Pro"
  - "More reliable on debugging, tests, and multi-step refactors"
```

### Slide 4 — "Codex turns repeat work into reusable workflows"

```yaml
id: 4
type: framework
layout: workflow-stack-with-product-cards
mode: designer-mode
image_decision: full-generated-visual
asset_refs: [codex_automation_screenshot, codex_skills_screenshot, codex_multitask_screenshot, codex_high_res_logo, explanatory_text_reference_02]
source_label: "Source: OpenAI Codex app features; plugins; memories; Chronicle documentation"
```

Use official skills and automation screenshots as product cards inside a layered workflow stack. Make the benefit feel reusable and scalable: Codex captures repeat work and turns it into workflows that teams can run again.

```yaml
required_text:
  - "Codex turns repeat work into reusable workflows"
  - "Plugins connect tools"
  - "Memories keep context"
  - "Automations make repeat work systematic"
```

### Slide 5 — "Browser and computer use let Codex automate real work, not just write code"

```yaml
id: 5
type: framework
layout: product-verification-triptych
mode: designer-mode
image_decision: regenerate-from-current-reference
asset_refs: [slide_3_current_reference, codex_browser_screenshot, codex_computer_use_screenshot, codex_artifact_viewer_screenshot, computer_use_logo_rounded_primary, computer_use_logo_rounded_wide, explanatory_text_reference_03]
source_label: "Source: OpenAI Codex app features; in-app browser; computer use; review documentation"
```

Regenerate the same visual direction as the current browser/computer-use slide: browser / Computer Use / artifact viewer. Make the wording feel like a sales pitch: Codex moves from writing code to automating real work in the browser and on the computer. Preserve the clean triptych structure and add the supplied Computer Use logo with rounded corners as a distinct logo tile near or partially over the central Computer Use card.

```yaml
required_text:
  - "Browser and computer use let Codex automate real work, not just write code"
  - "Browse live sites"
  - "Operate apps and desktops"
  - "Deliver verified outputs"
```

### Slide 6 — "Codex is scaling from developer tool to enterprise execution layer"

```yaml
id: 6
type: recommendation
layout: enterprise-proof-and-scale-path
mode: designer-mode
image_decision: full-generated-visual
asset_refs: [codex_high_res_logo, codex_lockup, openai_wordmark, codex_multitask_screenshot, explanatory_text_reference_01, slide_6_overload_reference]
source_label: "Source: OpenAI enterprise post, Apr 21 2026"
```

Create a polished enterprise proof slide, not a generic strategy slide. Reduce required text and use factual proof cards. Suggested hierarchy: one big title, one adoption-growth stat card, one enterprise-proof card, and one scale-path card. Do not render all examples as equal-weight bullets; keep the slide visually strategic.

```yaml
required_text:
  - "Codex is scaling from developer tool to enterprise execution layer"
  - "3M+ → 4M+ weekly developers in two weeks"
  - "Enterprise proof: Virgin Atlantic, Ramp, Notion, Cisco, Rakuten"
  - "Use cases: test coverage, code review, new features, incident response"
  - "Scale path: Codex Labs + 7 GSI partners"
```

Factual backing to use in design notes or small secondary text only if space allows:

```yaml
fact_bank:
  adoption: "OpenAI reported weekly Codex usage grew from more than 3M developers in early April to more than 4M two weeks later."
  examples:
    - "Virgin Atlantic: increase test coverage and team velocity"
    - "Ramp: accelerate code review"
    - "Notion: quickly build new features"
    - "Cisco: reason across large, interconnected repositories"
    - "Rakuten: incident response"
  scale_path:
    - "Codex Labs: workshops and working sessions for real enterprise problems"
    - "GSI partners: Accenture, Capgemini, CGI, Cognizant, Infosys, PwC, TCS"
```

### Slide 7 — "Learn more"

```yaml
id: 7
type: closing
layout: openai-learn-more-close
mode: designer-mode
image_decision: full-generated-visual
asset_refs: [openai_wordmark, codex_lockup, codex_high_res_logo, codex_multitask_screenshot]
source_label: "Source: OpenAI Codex page"
```

End with a clean OpenAI-style close. Large native title, small brand marks, one elegant URL treatment, and optional product screenshot crop as a quiet proof object. The URL must be legible.

```yaml
required_text:
  - "Learn more"
  - "openai.com/codex/code"
```

## Polish Pass

Rodrigo approved the content and requested a final image-generation polish pass because the rendered slides still felt like text overlays. The polish pass should use the existing slides as reference images, preserve the approved text/content, integrate typography natively into the slide composition, improve polish/spacing, and remove the confusing CR footer.

## Sources

- OpenAI Codex page: https://openai.com/codex/code
- OpenAI Developers — Codex app features: https://developers.openai.com/codex/app/features
- OpenAI Developers — In-app browser: https://developers.openai.com/codex/app/browser
- OpenAI Developers — Computer Use: https://developers.openai.com/codex/app/computer-use
- OpenAI Developers — Use your computer with Codex: https://developers.openai.com/codex/use-cases/use-your-computer-with-codex
- OpenAI Developers — Plugins: https://developers.openai.com/codex/plugins
- OpenAI Developers — Memories: https://developers.openai.com/codex/memories
- OpenAI — Introducing GPT-5.5: https://openai.com/index/introducing-gpt-5-5/
- OpenAI — Scaling Codex to enterprises worldwide: https://openai.com/index/scaling-codex-to-enterprises-worldwide/
- Rodrigo-supplied Codex color logo reference: https://pnghdpro.com/openai-codex-logo/


## Queued Edit Pass

After the polished review-08 PDF, Rodrigo requested two targeted edits:

- Slide 4: change the middle photo/card to the newly supplied Codex Memories image.
- Slide 7: remove the photo/product screenshot; keep only the OpenAI logo and closing copy.

Only the affected slides should be regenerated/updated, then the final polished PDF should be reassembled.


## Right Image Swap Pass

Rodrigo requested one more targeted edit after review-09: swap the right image/card on the GPT-5.5 proof slide with the newly supplied image. Regenerate/update only the affected slide and reassemble the PDF with prior accepted slides unchanged.
