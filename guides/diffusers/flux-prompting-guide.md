# Prompt Engineering Guide for Flux Kontext Models

## Table of Contents
- [Introduction](#introduction)
- [Understanding Flux Kontext](#understanding-flux-kontext)
- [Basic Prompting Principles](#basic-prompting-principles)
- [Advanced Techniques](#advanced-techniques)
- [Example Prompts](#example-prompts)
- [Common Pitfalls](#common-pitfalls)
- [Prompt Templates](#prompt-templates)

## Introduction

Flux Kontext models excel at understanding spatial relationships, context, and detailed scene composition. This guide provides strategies for crafting effective prompts to get the best results from these powerful text-to-image models.

## Understanding Flux Kontext

### Key Strengths
- **Spatial Understanding**: Excellent at positioning objects relative to each other
- **Context Awareness**: Understands scene relationships and environmental context
- **Detail Retention**: Maintains fine details across complex compositions
- **Natural Language**: Responds well to conversational, descriptive language
- **Style Flexibility**: Can adapt to various artistic styles and photographic approaches

### Model Characteristics
- **Optimal Guidance Scale**: 3.0-7.5 (lower than many models)
- **Resolution**: Works best at 1024x1024 or higher
- **Steps**: 30-50 steps for best quality
- **Prompt Length**: Can handle long, detailed descriptions effectively

## Basic Prompting Principles

### 1. Structure Your Prompts

Use this general structure for best results:

```
[Subject] [Action/Pose] [Environment/Setting] [Style/Quality] [Technical specifications]
```

**Example:**
```
A golden retriever puppy playing in a sunny meadow filled with wildflowers, soft natural lighting, photorealistic, high detail, 8k resolution
```

### 2. Be Specific About Spatial Relationships

Flux Kontext excels when you clearly describe where things are:

```
A red apple sitting on top of a wooden table, next to a blue ceramic mug, with sunlight streaming through a window in the background
```

### 3. Use Natural Language

Write as if describing a scene to another person:

```
A cozy reading nook by a large window, where an elderly man in a cardigan sits in a comfortable armchair, reading a leather-bound book while his cat sleeps peacefully on the windowsill beside him
```

## Advanced Techniques

### 1. Layered Descriptions

Build complexity by describing multiple layers of a scene:

```
Foreground: A steaming cup of coffee on a rustic wooden table
Middle ground: A person reading a newspaper in soft morning light
Background: A bustling café with warm Edison bulb lighting and brick walls
Style: Cinematic composition, warm color palette, shallow depth of field
```

### 2. Contextual Modifiers

Use context-aware descriptions:

```
A medieval knight standing guard at the entrance of an ancient castle, his armor reflecting the orange glow of torches mounted on stone walls, while storm clouds gather ominously in the twilight sky above
```

### 3. Emotional and Atmospheric Cues

Include mood and atmosphere:

```
A melancholic scene of an empty swing set in a fog-covered park at dawn, with dew-covered grass and bare trees creating a sense of solitude and nostalgia
```

### 4. Technical Photography Terms

Use photography terminology for specific looks:

```
A portrait of a young woman with curly hair, shot with a 85mm lens, bokeh background, golden hour lighting, shallow depth of field, professional headshot style
```

## Example Prompts

### Portrait Photography
```
A professional headshot of a confident businesswoman in her 30s, wearing a navy blue blazer, sitting in a modern office with floor-to-ceiling windows showing a city skyline, natural lighting, shot with 85mm lens, shallow depth of field
```

### Landscape/Nature
```
A majestic mountain range reflected in a pristine alpine lake during golden hour, with wildflower meadows in the foreground, dramatic clouds in the sky, and a lone eagle soaring overhead, captured in the style of Ansel Adams
```

### Fantasy/Sci-Fi
```
A futuristic cityscape at night with towering glass spires reaching into a star-filled sky, flying vehicles leaving light trails between buildings, while holographic advertisements cast colorful reflections on wet streets below
```

### Still Life/Product
```
An elegant arrangement of fresh vegetables on a rustic wooden cutting board, with a chef's knife positioned alongside, natural window light creating soft shadows, shot from above in the style of food photography
```

### Architectural
```
The interior of a Gothic cathedral with soaring stone arches, colorful stained glass windows casting rainbow light patterns on ancient stone floors, wooden pews arranged in perfect symmetry leading to an ornate altar
```

### Abstract/Artistic
```
A dynamic abstract composition featuring flowing liquid metal forms in gold and silver, suspended in mid-air against a deep black background, with dramatic studio lighting creating sharp highlights and deep shadows
```

## Common Pitfalls

### 1. Overcomplicated Prompts
❌ **Avoid**: Cramming too many conflicting elements
```
A cat dog bird flying swimming running jumping red blue green big small old new...
```

✅ **Better**: Focus on one clear scene
```
A tabby cat gracefully leaping from one rooftop to another against a sunset sky
```

### 2. Vague Descriptions
❌ **Avoid**: Generic or unclear terms
```
A nice picture of something cool
```

✅ **Better**: Specific, descriptive language
```
A steampunk airship floating above a Victorian city at dusk, with brass gears and copper pipes visible on its hull
```

### 3. Ignoring Spatial Context
❌ **Avoid**: Objects without clear positioning
```
A chair, a lamp, a book, a window
```

✅ **Better**: Clear spatial relationships
```
A reading chair positioned next to a tall floor lamp, with an open book resting on its arm, all situated near a large window with flowing curtains
```

### 4. Inconsistent Style References
❌ **Avoid**: Mixing incompatible styles
```
Photorealistic cartoon anime oil painting photograph
```

✅ **Better**: Consistent style direction
```
A character in the style of Studio Ghibli animation, with soft watercolor textures and whimsical details
```

## Prompt Templates

### Basic Template
```
[Subject] [in/at/on] [Location], [Lighting], [Style], [Quality modifiers]
```

### Detailed Scene Template
```
[Main subject] [action] in [environment] with [secondary elements], [lighting conditions], [mood/atmosphere], [artistic style], [technical specifications]
```

### Portrait Template
```
[Age/gender descriptor] [subject] [clothing/appearance] [pose/expression], [setting/background], [lighting type], [camera/lens details], [style reference]
```

### Landscape Template
```
[Landscape type] [time of day] with [weather/atmospheric conditions], [foreground elements], [background elements], [color palette], [artistic influence]
```

### Product/Still Life Template
```
[Product/object] [arrangement] on [surface] in [environment], [lighting setup], [angle/perspective], [style reference], [quality modifiers]
```

## Quality and Style Modifiers

### Quality Enhancers
- `high detail`, `ultra detailed`, `8k resolution`
- `sharp focus`, `crisp details`, `professional quality`
- `masterpiece`, `award winning`, `gallery quality`

### Lighting Terms
- `golden hour lighting`, `soft natural light`, `dramatic lighting`
- `studio lighting`, `cinematic lighting`, `volumetric lighting`
- `rim lighting`, `backlighting`, `side lighting`

### Camera/Photography Terms
- `shot with 85mm lens`, `shallow depth of field`, `bokeh`
- `wide angle`, `macro photography`, `long exposure`
- `high dynamic range`, `professional photography`

### Artistic Styles
- `in the style of [artist name]`
- `oil painting`, `watercolor`, `digital art`
- `photorealistic`, `hyperrealistic`, `painterly`
- `minimalist`, `surreal`, `impressionistic`

## Tips for Optimal Results

1. **Start Simple**: Begin with basic prompts and add complexity gradually
2. **Test Variations**: Experiment with different phrasings for the same concept
3. **Use Negative Prompts**: Specify what you don't want (e.g., "blurry, low quality")
4. **Consider Composition**: Think about framing, angles, and visual balance
5. **Match Style to Subject**: Choose artistic styles that complement your subject matter
6. **Iterate and Refine**: Use successful prompts as starting points for variations

## Negative Prompt Suggestions

Useful negative prompts to improve quality:
```
blurry, low quality, distorted, deformed, ugly, bad anatomy, extra limbs, text, watermark, signature, out of frame, cropped
```

For photorealistic images:
```
cartoon, anime, painting, drawing, sketch, rendered, CGI, fake, artificial
```

For artistic images:
```
photographic, realistic, photo, camera, lens flare, noise, grain
```

Remember: Flux Kontext responds well to natural, descriptive language. Think of yourself as describing a scene to an artist who will paint exactly what you describe.