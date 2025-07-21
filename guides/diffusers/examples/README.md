# Diffusers Examples

This directory contains runnable Python scripts demonstrating text-to-image and image-to-image generation using Flux models.

## Files

- **`txt2img.py`** - Text-to-image generation script
- **`img2img.py`** - Image-to-image transformation script  
- **`requirements.txt`** - Python package dependencies

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate an image from text:**
   ```bash
   python txt2img.py "A beautiful sunset over mountains"
   ```

3. **Transform an existing image:**
   ```bash
   python img2img.py input.jpg "Transform into a painting"
   ```

## Usage Examples

### Text-to-Image
```bash
# Basic generation
python txt2img.py "A red sports car in a desert"

# With custom settings
python txt2img.py "A castle in the clouds" --steps 30 --guidance 7.5 --output castle.png

# Memory optimization for smaller GPUs
python txt2img.py "A forest scene" --cpu-offload --attention-slicing --half-precision
```

### Image-to-Image
```bash
# Basic transformation
python img2img.py photo.jpg "Make it look like a watercolor painting"

# With strength control
python img2img.py portrait.jpg "Add dramatic lighting" --strength 0.5

# Preserve aspect ratio
python img2img.py landscape.jpg "Convert to autumn colors" --preserve-aspect
```

## System Requirements

- NVIDIA GPU with 8GB+ VRAM (16GB+ recommended)
- CUDA 11.8 or 12.x
- Python 3.8+

For detailed setup instructions, see the main guide: `../diffusers-guide.md`