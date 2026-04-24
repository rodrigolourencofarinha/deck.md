# Designer-mode direct API pattern

Use this when designer mode should generate a full slide directly with GPT Image 2 and a concrete runnable example will reduce tool/API drift.

Default rule:
- prefer native 16:9 generation
- default full-slide size: `2560x1440`
- use `2560x1440` as the preferred 2K/QHD slide target for `gpt-image-2`; current OpenAI guidance treats it as the upper reliability boundary before larger outputs become more experimental
- if local SDK type hints list only older fixed sizes, still try the documented `2560x1440` string against the live API first
- use `quality="high"` for final designer-mode slides, text-heavy slides, detailed diagrams, and exportable PDF/PPT assets
- use `quality="medium"` for layout or mood previews, and `quality="low"` only for fast exploration where visual precision is not yet important
- use `output_format="png"` and `n=1` for final slides; request multiple variants only during exploration
- do not treat cropping/reframing as the normal rescue path
- if the result is weak, improve the prompt and regenerate

Size constraints for `gpt-image-2`:
- both edges must be multiples of 16
- the long edge cannot exceed a 3:1 ratio against the short edge
- total pixels must be within the documented model range
- sizes above `2560x1440` are possible but more experimental for slide production

Reference pattern:

```python
result = client.images.generate(
    model="gpt-image-2",
    prompt=prompt,
    size="2560x1440",
    quality="high",
    output_format="png",
    n=1,
)
```

Use this as the preferred default for designer-mode full-slide generation when writing direct Python examples.

Reference-template pattern:

Use this when Rodrigo asks to "use my default template" in designer mode. This uses the Image API edit/reference path so the model can see the template PNG.

```python
result = client.images.edit(
    model="gpt-image-2",
    image=open("assets/visual-templates/default-slide.png", "rb"),
    prompt=prompt,
    size="2560x1440",
    quality="high",
    output_format="png",
    n=1,
)
```

For cover/title slides, use `assets/visual-templates/title-page.png`.
The prompt must say that the template is only a reference for the white background, title typography/placement, spacious margins, and footer safe area. Body visuals, diagrams, metaphors, icons, and accent colors can change to fit the slide message.

Interpretation notes:
- the prompt should already describe a real presentation slide, not just an illustration
- preserve slide grammar: title zone, support/key-message zone, and main visual body
- keep the composition presentation-grade and legible at slide scale
- if the output does not land, regenerate with a better prompt rather than salvaging it through destructive cropping
