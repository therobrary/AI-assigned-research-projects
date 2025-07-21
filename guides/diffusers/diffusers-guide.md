# Hugging Face Diffusers Library with Flux Models Guide

A comprehensive guide to using the Hugging Face Diffusers library for text-to-image and image-to-image generation with Flux models, featuring FLUX.1-Kontext-dev.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Quick Start](#quick-start)
- [Text-to-Image Generation](#text-to-image-generation)
- [Image-to-Image Generation](#image-to-image-generation)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Resources](#resources)

## Overview

### What is Diffusers?

The Hugging Face Diffusers library is a modular toolbox for state-of-the-art pretrained diffusion models for generating images, audio, and even 3D structures. It provides easy-to-use APIs for inference and training.

### Flux Model Family

Flux models, developed by Black Forest Labs, represent cutting-edge text-to-image generation capabilities. The family includes:

- **FLUX.1-pro**: The highest quality model (API-only)
- **FLUX.1-dev**: High-quality model for research and non-commercial use
- **FLUX.1-schnell**: Fast generation model for quick iterations
- **FLUX.1-Kontext-dev**: Enhanced model with improved context understanding

### Why Flux Models?

- **Superior Image Quality**: State-of-the-art generation capabilities
- **Enhanced Context Understanding**: Better interpretation of complex prompts
- **Flexible Conditioning**: Support for various input types
- **Community Support**: Active development and community contributions

## Prerequisites

Before starting, ensure you have:

- **Python 3.8+** (Python 3.10+ recommended)
- **CUDA-compatible GPU** with at least 8GB VRAM (16GB+ recommended)
- **Git and Git LFS** for model downloads
- **Basic knowledge** of Python and image processing concepts

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8+ | 3.10+ |
| GPU Memory | 8GB | 16GB+ |
| System RAM | 16GB | 32GB+ |
| Storage | 50GB free | 100GB+ free |

## Environment Setup

### Step 1: Create Virtual Environment

```bash
# Create and activate virtual environment
python -m venv diffusers-env
source diffusers-env/bin/activate  # On Windows: diffusers-env\Scripts\activate
```

### Step 2: Install Dependencies

```bash
# Install from requirements.txt
pip install -r examples/requirements.txt

# Or install manually
pip install torch torchvision diffusers transformers accelerate safetensors Pillow
```

### Step 3: Verify CUDA Installation

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"Device count: {torch.cuda.device_count()}")
if torch.cuda.is_available():
    print(f"Device name: {torch.cuda.get_device_name(0)}")
```

### Step 4: Hugging Face Authentication

```bash
# Install huggingface-hub if not already installed
pip install huggingface-hub

# Login to Hugging Face (required for some models)
huggingface-cli login
```

## Quick Start

Here's a minimal example to generate your first image:

```python
import torch
from diffusers import FluxPipeline

# Load the pipeline
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev", 
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

# Generate image
prompt = "A serene landscape with mountains and a crystal-clear lake at sunset"
image = pipe(
    prompt,
    height=1024,
    width=1024,
    guidance_scale=3.5,
    num_inference_steps=50,
    generator=torch.Generator("cuda").manual_seed(42)
).images[0]

# Save the result
image.save("my_first_flux_image.png")
print("Image saved as 'my_first_flux_image.png'")
```

## Text-to-Image Generation

### Basic Usage

The `txt2img.py` script provides a command-line interface for text-to-image generation:

```bash
# Basic generation
python examples/txt2img.py \
    --prompt "A futuristic cityscape at night with neon lights" \
    --output futuristic_city.png

# Advanced generation with custom parameters
python examples/txt2img.py \
    --prompt "A detailed portrait of a wise old wizard with a long beard" \
    --model "black-forest-labs/FLUX.1-Kontext-dev" \
    --width 1024 \
    --height 1024 \
    --steps 50 \
    --guidance-scale 3.5 \
    --seed 12345 \
    --output wizard_portrait.png
```

### Key Parameters

- **prompt**: Text description of the desired image
- **model**: Flux model variant to use
- **width/height**: Output image dimensions (multiples of 64)
- **steps**: Number of denoising steps (20-100)
- **guidance-scale**: How closely to follow the prompt (1.0-20.0)
- **seed**: Random seed for reproducible results

### Code Example

```python
from diffusers import FluxPipeline
import torch

def generate_image(prompt, model_id="black-forest-labs/FLUX.1-dev"):
    # Load pipeline with optimizations
    pipe = FluxPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        variant="fp16"  # Use FP16 variant if available
    )
    pipe.to("cuda")
    
    # Enable memory efficient attention
    pipe.enable_model_cpu_offload()
    
    # Generate image
    result = pipe(
        prompt=prompt,
        width=1024,
        height=1024,
        num_inference_steps=50,
        guidance_scale=3.5,
        generator=torch.Generator("cuda").manual_seed(42)
    )
    
    return result.images[0]

# Example usage
image = generate_image("A majestic dragon soaring over ancient ruins")
image.save("dragon_ruins.png")
```

## Image-to-Image Generation

Image-to-image generation allows you to transform existing images based on text prompts.

### Basic Usage

```bash
# Transform an existing image
python examples/img2img.py \
    --input_image photo.jpg \
    --prompt "Transform this into a watercolor painting" \
    --strength 0.7 \
    --output watercolor_result.png
```

### Key Parameters for Image-to-Image

- **input_image**: Path to the source image
- **prompt**: Text description of desired transformation
- **strength**: How much to modify the original (0.0-1.0)
- **guidance_scale**: Prompt adherence strength

### Code Example

```python
from diffusers import FluxImg2ImgPipeline
from PIL import Image
import torch

def transform_image(input_path, prompt, strength=0.7):
    # Load the image-to-image pipeline
    pipe = FluxImg2ImgPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16
    )
    pipe.to("cuda")
    
    # Load and prepare input image
    input_image = Image.open(input_path).convert("RGB")
    
    # Transform the image
    result = pipe(
        prompt=prompt,
        image=input_image,
        strength=strength,
        guidance_scale=3.5,
        num_inference_steps=50
    )
    
    return result.images[0]

# Example usage
transformed = transform_image(
    "landscape.jpg", 
    "Transform into a cyberpunk scene with neon lights and flying cars",
    strength=0.8
)
transformed.save("cyberpunk_landscape.png")
```

## Advanced Usage

### Memory Optimization

For systems with limited GPU memory:

```python
# Enable CPU offloading
pipe.enable_model_cpu_offload()

# Enable attention slicing
pipe.enable_attention_slicing(1)

# Enable VAE slicing for large images
pipe.enable_vae_slicing()

# Use lower precision
pipe = FluxPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,  # or torch.bfloat16
    low_cpu_mem_usage=True
)
```

### Batch Generation

Generate multiple images efficiently:

```python
def batch_generate(prompts, batch_size=2):
    results = []
    
    for i in range(0, len(prompts), batch_size):
        batch_prompts = prompts[i:i+batch_size]
        
        images = pipe(
            prompt=batch_prompts,
            num_images_per_prompt=1,
            num_inference_steps=50,
            guidance_scale=3.5
        ).images
        
        results.extend(images)
    
    return results

# Example usage
prompts = [
    "A red rose in full bloom",
    "A blue butterfly on a flower",
    "A golden sunset over mountains"
]

images = batch_generate(prompts)
for i, img in enumerate(images):
    img.save(f"batch_image_{i}.png")
```

### Custom Schedulers

Experiment with different noise schedulers:

```python
from diffusers import DPMSolverMultistepScheduler

# Use DPM-Solver for faster generation
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config
)

# Generate with fewer steps
image = pipe(
    prompt,
    num_inference_steps=25,  # Reduced from 50
    guidance_scale=3.5
).images[0]
```

## Best Practices

### Prompt Engineering

1. **Be Specific**: Include details about style, lighting, composition
2. **Use Descriptive Words**: Adjectives enhance image quality
3. **Specify Art Styles**: "in the style of...", "digital art", "oil painting"
4. **Include Technical Terms**: "8K resolution", "highly detailed", "professional photography"

### Example Prompts

```python
# Good prompts for Flux models
prompts = [
    "A highly detailed portrait of a cyberpunk warrior, neon-lit cityscape background, digital art, 8K resolution",
    "Ancient library with floating books and magical glowing orbs, warm lighting, fantasy art style",
    "Minimalist modern architecture, clean lines, natural lighting, architectural photography",
    "Vibrant coral reef underwater scene, tropical fish, crystal clear water, nature photography"
]
```

### Performance Optimization

1. **Choose Appropriate Model Size**: Balance quality vs. speed
2. **Optimize Inference Steps**: 20-50 steps usually sufficient
3. **Use Mixed Precision**: bfloat16 or float16 for speed
4. **Enable Memory Optimizations**: CPU offload, attention slicing

### Quality Settings

```python
# High quality settings
high_quality_config = {
    "num_inference_steps": 50,
    "guidance_scale": 3.5,
    "width": 1024,
    "height": 1024
}

# Fast generation settings
fast_config = {
    "num_inference_steps": 20,
    "guidance_scale": 2.5,
    "width": 512,
    "height": 512
}
```

## Troubleshooting

### Common Issues

#### CUDA Out of Memory

```python
# Solutions:
# 1. Enable CPU offloading
pipe.enable_model_cpu_offload()

# 2. Reduce image size
image = pipe(prompt, width=512, height=512)

# 3. Use attention slicing
pipe.enable_attention_slicing(1)

# 4. Clear cache
torch.cuda.empty_cache()
```

#### Slow Generation

```python
# Solutions:
# 1. Reduce inference steps
image = pipe(prompt, num_inference_steps=25)

# 2. Use float16 precision
pipe = FluxPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

# 3. Enable attention slicing for memory vs speed trade-off
pipe.enable_attention_slicing("auto")
```

#### Model Loading Issues

```bash
# Ensure you're logged into Hugging Face
huggingface-cli login

# Update to latest versions
pip install --upgrade diffusers transformers

# Clear Hugging Face cache if needed
rm -rf ~/.cache/huggingface/
```

### Error Messages and Solutions

| Error | Solution |
|-------|----------|
| "CUDA out of memory" | Enable CPU offloading, reduce image size, or use attention slicing |
| "Model not found" | Check model name, ensure HF login, verify internet connection |
| "Slow inference" | Reduce steps, use lower precision, enable optimizations |
| "Poor image quality" | Increase steps, adjust guidance scale, improve prompt |

## FAQ

### Q: Which Flux model should I use?

**A:** Choose based on your needs:
- **FLUX.1-dev**: Best quality for research/non-commercial use
- **FLUX.1-Kontext-dev**: Enhanced context understanding
- **FLUX.1-schnell**: Fastest generation for prototyping

### Q: How much VRAM do I need?

**A:** 
- Minimum: 8GB (with optimizations)
- Recommended: 16GB+ for comfortable usage
- Professional: 24GB+ for batch processing

### Q: Can I use Flux models commercially?

**A:** Check the specific model license:
- FLUX.1-dev: Research and non-commercial use only
- FLUX.1-pro: Commercial license available
- Always verify current licensing terms

### Q: How do I improve image quality?

**A:**
1. Use more inference steps (50-100)
2. Increase guidance scale (3.0-7.0)
3. Improve prompt specificity
4. Use higher resolution (1024x1024+)
5. Experiment with different schedulers

### Q: Can I run this on CPU only?

**A:** While possible, it's extremely slow. GPU is strongly recommended for practical use.

## Resources

### Official Documentation

- [Hugging Face Diffusers Documentation](https://huggingface.co/docs/diffusers/en/index)
- [Diffusers GitHub Repository](https://github.com/huggingface/diffusers)
- [FLUX.1-Kontext-dev Model Card](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev)
- [Black Forest Labs Blog Post](https://bfl.ai/announcements/flux-1-kontext-dev)

### Community Resources

- [Hugging Face Community](https://huggingface.co/spaces)
- [Diffusers Discord](https://discord.gg/JfAtkvEtRb)
- [Reddit r/StableDiffusion](https://reddit.com/r/StableDiffusion)

### Research Papers

- [FLUX.1 Technical Report](https://github.com/black-forest-labs/flux)
- [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
- [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752)

### Additional Tools

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - Node-based interface
- [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) - Web interface
- [Fooocus](https://github.com/lllyasviel/Fooocus) - Simplified interface

---

**Last Updated**: December 2024  
**Contributors**: AI Research Team  
**License**: Educational and Research Use

For additional prompting guidance specific to FLUX.1-Kontext-dev, see our [Flux Prompting Guide](flux-prompting-guide.md).