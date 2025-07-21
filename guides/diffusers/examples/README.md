# Diffusers Examples

This directory contains working Python examples for using Hugging Face Diffusers with Flux models.

## Files Overview

### Scripts

- **`txt2img.py`** - Text-to-image generation script
  - Command-line interface for generating images from text prompts
  - Supports all Flux model variants
  - Includes memory optimization options
  - Rich CLI with progress bars and helpful output

- **`img2img.py`** - Image-to-image transformation script
  - Transform existing images based on text prompts
  - Configurable transformation strength
  - Supports batch processing patterns
  - Automatic image resizing and preprocessing

### Configuration

- **`requirements.txt`** - Python dependencies
  - All required packages with tested versions
  - Includes optional performance enhancements
  - Compatible with Python 3.8+

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Login to Hugging Face (required for model access)
huggingface-cli login
```

### Basic Usage

#### Text-to-Image

```bash
# Simple generation
python txt2img.py --prompt "A serene mountain landscape at sunset"

# Advanced generation
python txt2img.py \
    --prompt "A cyberpunk cityscape with neon lights" \
    --model flux-kontext \
    --width 1024 \
    --height 1024 \
    --steps 50 \
    --guidance-scale 3.5 \
    --seed 42 \
    --output cyberpunk_city.png
```

#### Image-to-Image

```bash
# Transform an existing image
python img2img.py \
    --input photo.jpg \
    --prompt "Transform into a watercolor painting" \
    --strength 0.7 \
    --output watercolor_result.png

# Strong transformation
python img2img.py \
    --input landscape.jpg \
    --prompt "Make it look like a cyberpunk scene" \
    --strength 0.9 \
    --model flux-dev \
    --steps 75
```

## Command-Line Options

### txt2img.py Options

| Option | Description | Default |
|--------|-------------|---------|
| `--prompt`, `-p` | Text prompt (required) | - |
| `--model`, `-m` | Model variant (flux-dev, flux-kontext, flux-schnell) | flux-dev |
| `--width`, `-w` | Image width (multiple of 64) | 1024 |
| `--height`, `-h` | Image height (multiple of 64) | 1024 |
| `--steps`, `-s` | Inference steps (20-100) | 50 |
| `--guidance-scale`, `-g` | Prompt adherence (1.0-20.0) | 3.5 |
| `--seed` | Random seed for reproducibility | Random |
| `--output`, `-o` | Output file path | generated_image.png |
| `--cpu-offload` | Enable CPU offloading | False |
| `--attention-slicing` | Enable attention slicing | False |

### img2img.py Options

| Option | Description | Default |
|--------|-------------|---------|
| `--input`, `-i` | Input image path (required) | - |
| `--prompt`, `-p` | Transformation prompt (required) | - |
| `--model`, `-m` | Model variant | flux-dev |
| `--strength`, `-t` | Transformation strength (0.0-1.0) | 0.7 |
| `--width`, `-w` | Output width (multiple of 64) | Keep original |
| `--height`, `-h` | Output height (multiple of 64) | Keep original |
| `--steps`, `-s` | Inference steps | 50 |
| `--guidance-scale`, `-g` | Prompt adherence | 3.5 |
| `--seed` | Random seed | Random |
| `--output`, `-o` | Output file path | {input}_transformed.{ext} |
| `--cpu-offload` | Enable CPU offloading | False |
| `--attention-slicing` | Enable attention slicing | False |

## Performance Tips

### Memory Optimization

For systems with limited GPU memory:

```bash
# Enable all memory optimizations
python txt2img.py \
    --prompt "Your prompt here" \
    --cpu-offload \
    --attention-slicing \
    --width 512 \
    --height 512
```

### Speed Optimization

For faster generation:

```bash
# Use flux-schnell for speed
python txt2img.py \
    --prompt "Your prompt here" \
    --model flux-schnell \
    --steps 25 \
    --guidance-scale 2.5
```

### Quality Optimization

For highest quality:

```bash
# Maximum quality settings
python txt2img.py \
    --prompt "Your detailed prompt here" \
    --model flux-kontext \
    --steps 75 \
    --guidance-scale 4.0 \
    --width 1024 \
    --height 1024
```

## Example Workflows

### Batch Generation

Create a script to generate multiple variations:

```bash
#!/bin/bash
PROMPT="A majestic dragon in a fantasy landscape"

for i in {1..5}; do
    python txt2img.py \
        --prompt "$PROMPT" \
        --seed $i \
        --output "dragon_variation_$i.png"
done
```

### Style Exploration

Test different artistic styles:

```bash
# Photography style
python txt2img.py --prompt "Portrait of a wise elder, professional photography, studio lighting"

# Digital art style
python txt2img.py --prompt "Portrait of a wise elder, digital art, fantasy style"

# Oil painting style
python txt2img.py --prompt "Portrait of a wise elder, oil painting, Renaissance style"
```

### Progressive Transformation

Gradually transform an image:

```bash
# Light transformation
python img2img.py --input original.jpg --prompt "Add subtle magical elements" --strength 0.3

# Medium transformation
python img2img.py --input original.jpg --prompt "Add magical elements" --strength 0.6

# Strong transformation
python img2img.py --input original.jpg --prompt "Transform into fantasy scene" --strength 0.9
```

## Troubleshooting

### Common Issues

#### CUDA Out of Memory
```bash
# Solution: Enable memory optimizations
python txt2img.py --prompt "Your prompt" --cpu-offload --attention-slicing
```

#### Slow Generation
```bash
# Solution: Use faster settings
python txt2img.py --prompt "Your prompt" --model flux-schnell --steps 25
```

#### Poor Quality
```bash
# Solution: Increase quality settings
python txt2img.py --prompt "Detailed prompt" --steps 75 --guidance-scale 4.0
```

### Error Messages

| Error | Solution |
|-------|----------|
| "CUDA not available" | Install PyTorch with CUDA or use `--cpu-offload` |
| "Model not found" | Run `huggingface-cli login` |
| "Out of memory" | Reduce image size or enable memory optimizations |
| "Invalid dimensions" | Ensure width/height are multiples of 64 |

## Integration Examples

### Python Script Integration

```python
# Import and use the modules
import sys
sys.path.append('path/to/examples')

from txt2img import generate_image, load_pipeline

# Load pipeline once
pipe = load_pipeline("flux-dev")

# Generate multiple images
prompts = [
    "A red rose",
    "A blue butterfly", 
    "A golden sunset"
]

for i, prompt in enumerate(prompts):
    image = generate_image(pipe, prompt)
    image.save(f"image_{i}.png")
```

### Jupyter Notebook Usage

```python
# In a Jupyter cell
%run txt2img.py --prompt "A beautiful landscape" --output notebook_output.png

# Or import and use directly
from PIL import Image
import torch
from diffusers import FluxPipeline

# Your generation code here
```

## Best Practices

1. **Start Simple**: Begin with basic prompts and default settings
2. **Iterate**: Refine prompts based on results
3. **Use Seeds**: Set seeds for reproducible results during experimentation
4. **Monitor Memory**: Watch GPU memory usage, enable optimizations as needed
5. **Batch Process**: Generate multiple variations efficiently
6. **Save Metadata**: Include prompt information in output filenames

## Support

For issues with these examples:

1. Check the main [Diffusers Guide](../diffusers-guide.md)
2. Review the [Flux Prompting Guide](../flux-prompting-guide.md)
3. Verify your environment meets the prerequisites
4. Ensure all dependencies are correctly installed

---

**Last Updated**: December 2024  
**Python Compatibility**: 3.8+  
**Tested Models**: FLUX.1-dev, FLUX.1-Kontext-dev, FLUX.1-schnell