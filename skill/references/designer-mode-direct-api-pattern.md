# Designer-mode direct API fallback pattern

Use this only when the `gpt-image-2` Codex OAuth/Codex image path is unavailable or fails, the user has been told what failed, and the user has approved continuing with the direct OpenAI Image API key fallback.

Default rule:
- use `gpt-image-2` through Codex OAuth/Codex image tooling first; do not start with the direct API-key path
- if the Codex-authenticated path fails, report the failure and ask whether to continue with the OpenAI API-key fallback
- prefer native 16:9 generation
- default full-slide size: `2560x1440`
- use `2560x1440` as the preferred 2K/QHD slide target for `gpt-image-2`; current OpenAI guidance treats it as the upper reliability boundary before larger outputs become more experimental
- if local SDK type hints list only older fixed sizes, still try the documented `2560x1440` string against the live API first
- use `quality="high"` for final designer-mode slides, text-heavy slides, detailed diagrams, and exportable PDF/PPT assets
- use `quality="medium"` for layout or mood previews, and `quality="low"` only for fast exploration where visual precision is not yet important
- use `output_format="png"` and `n=1` for final slides; request multiple variants only during exploration
- include the computed footer in the prompt unless disabled in deck.md: small `CR` lower-left and simple page number lower-right, never `1/3`
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

Use this only as the approved fallback for designer-mode full-slide generation when writing direct Python examples.

Reference-asset pattern:

Use this when the approved deck declares an external image reference in `designer_assets`. This uses the Image API edit/reference path so the model can see the prepared image.

```python
result = client.images.edit(
    model="gpt-image-2",
    image=open(prepared_reference_path, "rb"),
    prompt=prompt,
    size="2560x1440",
    quality="high",
    output_format="png",
    n=1,
)
```

The prompt must say exactly what the declared reference is allowed to influence, such as title typography/placement, spacious margins, visual rhythm, density, or footer safe area. Body visuals, diagrams, metaphors, icons, and accent colors can change to fit the slide message unless the approved brief says otherwise.

Interpretation notes:
- the prompt should already describe a real presentation slide, not just an illustration
- preserve slide grammar: title zone, support/key-message zone, and main visual body
- include footer grammar: `CR` mark and simple page number in a subtle lower safe area
- keep the composition presentation-grade and legible at slide scale
- if the output does not land, regenerate with a better prompt rather than salvaging it through destructive cropping
