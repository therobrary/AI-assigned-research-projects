# FLUX.1-Kontext-dev Prompting Guide

An advanced guide for crafting effective prompts to achieve optimal results with the FLUX.1-Kontext-dev model.

## Table of Contents

- [Overview](#overview)
- [Understanding FLUX.1-Kontext-dev](#understanding-flux1-kontext-dev)
- [Prompt Structure](#prompt-structure)
- [Style and Quality Modifiers](#style-and-quality-modifiers)
- [Advanced Prompting Techniques](#advanced-prompting-techniques)
- [Category-Specific Prompts](#category-specific-prompts)
- [Common Prompting Patterns](#common-prompting-patterns)
- [Troubleshooting Prompts](#troubleshooting-prompts)
- [Examples and Templates](#examples-and-templates)

## Overview

FLUX.1-Kontext-dev is an enhanced version of the FLUX.1 model with improved context understanding and better adherence to complex prompts. This guide will help you craft prompts that leverage its advanced capabilities.

### Key Advantages of FLUX.1-Kontext-dev

- **Enhanced Context Understanding**: Better interpretation of spatial relationships and scene composition
- **Improved Object Placement**: More accurate positioning of elements in the scene
- **Better Style Consistency**: More consistent application of artistic styles
- **Advanced Text Integration**: Superior handling of text elements in images
- **Complex Scene Handling**: Better management of multi-element compositions

## Understanding FLUX.1-Kontext-dev

### How It Differs from Other Models

FLUX.1-Kontext-dev processes prompts with enhanced contextual awareness:

1. **Spatial Understanding**: Better grasps "in front of", "behind", "to the left of"
2. **Compositional Logic**: Understands how elements should relate to each other
3. **Style Coherence**: Maintains consistent artistic styles across all elements
4. **Detail Hierarchy**: Distinguishes between primary and secondary elements

### Optimal Parameters for FLUX.1-Kontext-dev

```python
# Recommended settings
optimal_settings = {
    "guidance_scale": 3.5,  # Sweet spot for quality vs. creativity
    "num_inference_steps": 50,  # Good balance of quality and speed
    "width": 1024,
    "height": 1024,
    "scheduler": "default"  # Built-in scheduler works best
}
```

## Prompt Structure

### Basic Structure

The most effective prompts for FLUX.1-Kontext-dev follow this structure:

```
[MAIN_SUBJECT] [ACTION/POSE] [SETTING/BACKGROUND] [STYLE] [QUALITY_MODIFIERS] [TECHNICAL_SPECS]
```

### Example Breakdown

**Prompt:** "A majestic dragon perched on ancient stone ruins, overlooking a misty valley at sunset, digital art style, highly detailed, 8K resolution, cinematic lighting"

- **MAIN_SUBJECT**: A majestic dragon
- **ACTION/POSE**: perched on ancient stone ruins
- **SETTING/BACKGROUND**: overlooking a misty valley at sunset
- **STYLE**: digital art style
- **QUALITY_MODIFIERS**: highly detailed, 8K resolution
- **TECHNICAL_SPECS**: cinematic lighting

### Essential Elements

#### 1. Subject Description
Be specific about the main subject:

```
❌ "A person"
✅ "A young woman with curly auburn hair wearing a flowing blue dress"

❌ "A building"
✅ "A gothic cathedral with intricate stone carvings and stained glass windows"
```

#### 2. Context and Setting
Provide environmental context:

```
❌ "A cat"
✅ "A sleek black cat sitting on a windowsill overlooking a rain-soaked city street"
```

#### 3. Style Specification
Define the artistic approach:

```
❌ "Make it look good"
✅ "In the style of Renaissance oil painting with chiaroscuro lighting"
```

## Style and Quality Modifiers

### Style Categories

#### Photographic Styles
```
- "professional photography"
- "portrait photography with shallow depth of field"
- "architectural photography"
- "macro photography"
- "street photography"
- "landscape photography with golden hour lighting"
```

#### Artistic Styles
```
- "oil painting in the style of Van Gogh"
- "watercolor illustration"
- "digital art with vibrant colors"
- "pencil sketch with detailed shading"
- "anime art style"
- "concept art for video games"
```

#### Technical Specifications
```
- "8K resolution"
- "highly detailed"
- "photorealistic"
- "ultra-wide angle"
- "macro lens"
- "bokeh background"
```

### Quality Enhancement Keywords

#### High-Impact Quality Terms
```
- "masterpiece"
- "award-winning"
- "professionally lit"
- "museum quality"
- "gallery exhibition"
- "critically acclaimed"
```

#### Technical Quality Terms
```
- "sharp focus"
- "perfect composition"
- "dynamic lighting"
- "rich colors"
- "fine details"
- "texture detail"
```

## Advanced Prompting Techniques

### 1. Layered Prompting

Build complexity gradually:

```python
# Layer 1: Basic subject
base_prompt = "A steampunk airship"

# Layer 2: Add context
detailed_prompt = base_prompt + " flying through clouds above a Victorian city"

# Layer 3: Add style
styled_prompt = detailed_prompt + " in the style of detailed technical illustration"

# Layer 4: Add quality
final_prompt = styled_prompt + " with intricate brass details, warm lighting, highly detailed"
```

### 2. Contextual Relationships

Use relational terms for complex scenes:

```
Spatial Relations:
- "in the foreground"
- "in the background"
- "to the left of"
- "behind"
- "above"
- "nestled between"

Size Relations:
- "towering over"
- "dwarfed by"
- "same scale as"
- "miniature version"
```

### 3. Atmospheric Descriptors

Create mood and atmosphere:

```
Lighting:
- "golden hour lighting"
- "dramatic chiaroscuro"
- "soft diffused light"
- "neon lighting"
- "moonlit scene"
- "candlelit atmosphere"

Weather/Environment:
- "misty morning"
- "storm clouds gathering"
- "gentle snowfall"
- "humid summer evening"
- "crisp autumn air"
```

### 4. Emotional Tone

Guide the emotional impact:

```
Mood Keywords:
- "serene and peaceful"
- "mysterious and ethereal"
- "dramatic and intense"
- "whimsical and playful"
- "melancholic and contemplative"
- "epic and heroic"
```

## Category-Specific Prompts

### Portrait Photography

```
Template:
"[DESCRIPTION] of [PERSON], [POSE/EXPRESSION], [SETTING], [LIGHTING], [CAMERA_SPECS], [STYLE_NOTES]"

Example:
"Professional headshot of a confident business executive, slight smile, modern office background, soft studio lighting, shot with 85mm lens, shallow depth of field, corporate photography style"
```

### Landscape Photography

```
Template:
"[LOCATION_TYPE] [TIME_OF_DAY], [WEATHER_CONDITIONS], [FOREGROUND_ELEMENTS], [BACKGROUND_ELEMENTS], [LIGHTING_CONDITIONS], [CAMERA_TECHNIQUE]"

Example:
"Mountain lake at sunrise, clear skies with wispy clouds, wildflowers in foreground, snow-capped peaks in background, golden hour lighting, landscape photography with polarizing filter"
```

### Fantasy Art

```
Template:
"[FANTASY_SUBJECT] [ACTION] in [MAGICAL_SETTING], [MAGICAL_ELEMENTS], [ART_STYLE], [COLOR_PALETTE], [MOOD]"

Example:
"Ancient wizard casting a spell in enchanted forest clearing, glowing runes floating in air, digital fantasy art, rich blues and purples with golden highlights, mystical and powerful atmosphere"
```

### Architecture

```
Template:
"[BUILDING_TYPE] [ARCHITECTURAL_STYLE], [KEY_FEATURES], [SURROUNDINGS], [LIGHTING], [PERSPECTIVE], [PHOTOGRAPHY_STYLE]"

Example:
"Modern glass skyscraper with curved facade, LED lighting integrated into structure, urban cityscape at night, dramatic uplighting, low angle perspective, architectural photography"
```

### Product Photography

```
Template:
"[PRODUCT] [PRODUCT_DETAILS], [BACKGROUND], [LIGHTING_SETUP], [CAMERA_ANGLE], [STYLE_NOTES]"

Example:
"Luxury Swiss watch with leather band, clean white background, professional studio lighting, slight angle showing face and band, commercial product photography"
```

## Common Prompting Patterns

### The "Golden Hour" Pattern

Perfect for warm, cinematic lighting:

```
"[SUBJECT] during golden hour, warm sunlight, long shadows, cinematic lighting, professional photography"
```

### The "Detailed Study" Pattern

For highly detailed, almost scientific illustrations:

```
"Detailed study of [SUBJECT], scientific illustration style, precise linework, educational diagram, museum quality"
```

### The "Artistic Interpretation" Pattern

For creative, stylized renderings:

```
"Artistic interpretation of [SUBJECT] in the style of [ARTIST/MOVEMENT], [COLOR_PALETTE], [MOOD], gallery exhibition quality"
```

### The "Cinematic Scene" Pattern

For movie-like compositions:

```
"Cinematic scene of [SUBJECT] [ACTION], [DRAMATIC_LIGHTING], [CAMERA_ANGLE], film still quality, directed by [DIRECTOR_STYLE]"
```

## Troubleshooting Prompts

### Common Issues and Solutions

#### Issue: Blurry or Soft Details
```
❌ "A detailed face"
✅ "A face with sharp focus, crisp details, high resolution, professional portrait photography"
```

#### Issue: Poor Composition
```
❌ "A landscape"
✅ "A landscape with rule of thirds composition, foreground rocks, midground lake, background mountains"
```

#### Issue: Inconsistent Style
```
❌ "A painting photo"
✅ "An oil painting in Renaissance style" OR "A photograph with painterly lighting"
```

#### Issue: Wrong Colors
```
❌ "Colorful"
✅ "Vibrant blue and gold color palette with complementary orange accents"
```

#### Issue: Missing Context
```
❌ "A cat sitting"
✅ "A tabby cat sitting on a weathered wooden fence post in a garden setting"
```

### Negative Prompting Tips

While FLUX.1-Kontext-dev doesn't use negative prompts, you can guide it away from unwanted elements:

```
Instead of: "beautiful woman, no glasses"
Use: "beautiful woman with clear, unobstructed eyes"

Instead of: "landscape, no people"
Use: "pristine wilderness landscape, untouched nature"
```

## Examples and Templates

### Template Collection

#### Portrait Template
```
"[AGE] [GENDER] with [HAIR_DESCRIPTION] and [EYE_DESCRIPTION], [EXPRESSION], wearing [CLOTHING], [POSE], [SETTING], [LIGHTING_TYPE], shot with [CAMERA_DETAILS], [STYLE_NOTES]"
```

#### Landscape Template
```
"[LANDSCAPE_TYPE] at [TIME_OF_DAY], [WEATHER], [FOREGROUND], [MIDGROUND], [BACKGROUND], [LIGHTING_QUALITY], captured with [CAMERA_TECHNIQUE], [STYLE_REFERENCE]"
```

#### Fantasy Template
```
"[FANTASY_CREATURE/CHARACTER] [ACTION] in [MAGICAL_LOCATION], [MAGICAL_ELEMENTS], [ATMOSPHERE], [ART_MEDIUM], [COLOR_SCHEME], [ARTISTIC_REFERENCE]"
```

#### Still Life Template
```
"[OBJECTS] arranged [ARRANGEMENT_STYLE], [BACKGROUND], [LIGHTING_SETUP], [MOOD], [PHOTOGRAPHY_STYLE], [TECHNICAL_DETAILS]"
```

### Complete Example Prompts

#### Example 1: Fantasy Portrait
```
"A wise elven sorceress with long silver hair and glowing blue eyes, serene expression, wearing flowing midnight blue robes with intricate star patterns, hands raised casting a spell with glowing magical energy, ancient library background with floating books, soft mystical lighting with lens flares, digital fantasy art in the style of Luis Royo, rich blues and purples with golden highlights, masterpiece quality"
```

#### Example 2: Architectural Photography
```
"Modern minimalist house with floor-to-ceiling windows and concrete structure, situated on a cliff overlooking the ocean, sunset lighting creating warm reflections, architectural photography with wide-angle lens, clean lines and geometric composition, luxury real estate photography style, dramatic sky with scattered clouds, professional lighting, award-winning architecture"
```

#### Example 3: Product Photography
```
"Artisanal coffee cup with latte art, steam rising, placed on rustic wooden table with coffee beans scattered around, warm morning light streaming through window, shallow depth of field focusing on the cup, commercial product photography, rich brown and cream tones, cozy cafe atmosphere, shot with macro lens, advertising quality"
```

#### Example 4: Nature Photography
```
"Monarch butterfly perched on vibrant orange marigold flower, dewdrops on petals catching morning sunlight, garden setting with soft bokeh background, macro photography with 100mm lens, shallow depth of field, nature documentary style, rich oranges and yellows, crisp focus on butterfly wings, National Geographic quality"
```

### Advanced Prompt Formulas

#### The "Cinematic Formula"
```
"[SUBJECT] [ACTION], cinematic composition, [LIGHTING_TYPE], shot on [CAMERA], [LENS], directed by [DIRECTOR_STYLE], [COLOR_GRADING], film still quality"
```

#### The "Gallery Formula"
```
"[ARTWORK_DESCRIPTION], [ARTISTIC_MEDIUM], in the style of [ARTIST/MOVEMENT], [COLOR_PALETTE], [COMPOSITION_NOTES], gallery exhibition quality, museum piece"
```

#### The "Technical Formula"
```
"[SUBJECT], technical illustration, precise details, [SPECIFICATION_LEVEL], educational diagram, scientific accuracy, [COLOR_SCHEME], professional documentation style"
```

## Best Practices Summary

1. **Be Specific**: Use precise, descriptive language
2. **Layer Information**: Build complexity gradually
3. **Include Context**: Provide environmental and situational details
4. **Specify Style**: Define the artistic approach clearly
5. **Use Quality Terms**: Include technical and aesthetic quality indicators
6. **Consider Relationships**: Use spatial and contextual relationship terms
7. **Test Iterations**: Refine prompts based on results
8. **Study Examples**: Learn from successful prompt patterns

---

**Last Updated**: December 2024  
**Model Version**: FLUX.1-Kontext-dev  
**Tested Parameters**: guidance_scale=3.5, steps=50  

For the main implementation guide, see [Diffusers Guide](diffusers-guide.md).