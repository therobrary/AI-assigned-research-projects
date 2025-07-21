# Hugging Face Diffusers Library with Flux Models Guide

## Table of Contents
- [Overview](#overview)
- [Environment Setup](#environment-setup)
- [Quick Start: Text-to-Image](#quick-start-text-to-image)
- [Image-to-Image Generation](#image-to-image-generation)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [Safety and Licensing](#safety-and-licensing)

## Overview

The Hugging Face Diffusers library provides state-of-the-art pretrained diffusion models for generating high-quality images. This guide focuses on using Flux models, particularly the `FLUX.1-Kontext-dev` model, for both text-to-image and image-to-image workflows.

### What is Flux?

Flux is a family of open-source text-to-image models developed by Black Forest Labs. The Flux.1-Kontext model is specifically designed for understanding and generating images with spatial context and relationships.

Key features:
- **High-quality output**: Produces detailed, coherent images
- **Spatial understanding**: Excels at positioning objects and understanding spatial relationships
- **Open source**: Available for research and commercial use (check licensing)
- **Efficient**: Optimized for performance on modern GPUs

### Diffusers Ecosystem

The Diffusers library provides:
- Pre-trained models from Hugging Face Hub
- Schedulers for different sampling strategies
- Pipelines for common workflows
- Memory optimization techniques
- Safety filters and content moderation

## Environment Setup

### System Requirements

- **GPU**: NVIDIA GPU with at least 8GB VRAM (16GB+ recommended for larger models)
- **CUDA**: CUDA 11.8 or 12.x
- **Python**: Python 3.8 or higher
- **Disk space**: ~10-20GB for model weights

### Installation

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install PyTorch with CUDA support**:
```bash
# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

3. **Install Diffusers and dependencies**:
```bash
pip install diffusers[torch] transformers accelerate xformers
pip install Pillow numpy matplotlib
```

4. **Verify installation**:
```python
import torch
import diffusers
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Diffusers version: {diffusers.__version__}")
```

### Hugging Face Authentication

Some models require authentication. Create a Hugging Face account and generate an access token:

```bash
pip install huggingface-hub
huggingface-cli login
```

## Quick Start: Text-to-Image

Here's a minimal example using the Flux.1-Kontext model:

```python
import torch
from diffusers import FluxPipeline

# Load the model
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype=torch.bfloat16
)
pipe = pipe.to("cuda")

# Generate an image
prompt = "A majestic lion sitting on a rock in the African savanna, golden hour lighting"
image = pipe(
    prompt=prompt,
    height=1024,
    width=1024,
    num_inference_steps=50,
    guidance_scale=3.5
).images[0]

# Save the image
image.save("generated_image.png")
```

### Key Parameters

- **`prompt`**: The text description of the desired image
- **`height/width`**: Output image dimensions (multiples of 64)
- **`num_inference_steps`**: Number of denoising steps (more = higher quality, slower)
- **`guidance_scale`**: How closely to follow the prompt (1.0-20.0, ~3.5 is typical for Flux)
- **`seed`**: For reproducible results (optional)

### Memory Optimization

For GPUs with limited VRAM:

```python
# Enable CPU offloading
pipe.enable_model_cpu_offload()

# Enable attention slicing
pipe.enable_attention_slicing()

# Use lower precision
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype=torch.float16  # Instead of bfloat16
)
```

## Image-to-Image Generation

Use an existing image as a starting point:

```python
import torch
from diffusers import FluxImg2ImgPipeline
from PIL import Image

# Load the img2img pipeline
pipe = FluxImg2ImgPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    torch_dtype=torch.bfloat16
)
pipe = pipe.to("cuda")

# Load and prepare the input image
init_image = Image.open("input_image.jpg").convert("RGB")
init_image = init_image.resize((1024, 1024))

# Generate the modified image
prompt = "Transform this into a painting in the style of Van Gogh"
image = pipe(
    prompt=prompt,
    image=init_image,
    strength=0.75,  # How much to change the original (0.0-1.0)
    guidance_scale=3.5,
    num_inference_steps=50
).images[0]

image.save("transformed_image.png")
```

### Img2Img Parameters

- **`image`**: Input PIL Image or tensor
- **`strength`**: Transformation strength (0.0 = no change, 1.0 = complete transformation)
- **`guidance_scale`**: Prompt adherence (lower values for subtle changes)

## Advanced Usage

### Using Different Schedulers

Schedulers control the denoising process:

```python
from diffusers import DPMSolverMultistepScheduler

# Change scheduler for different quality/speed tradeoffs
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# Reduce steps with better scheduler
image = pipe(prompt, num_inference_steps=25).images[0]
```

### Batch Generation

Generate multiple images efficiently:

```python
prompts = [
    "A red apple on a table",
    "A blue car in a parking lot", 
    "A green tree in a park"
]

images = pipe(prompts, num_images_per_prompt=2).images
# Returns 6 images total (2 per prompt)
```

### Negative Prompts

Specify what you don't want:

```python
image = pipe(
    prompt="A beautiful landscape",
    negative_prompt="blurry, low quality, distorted, ugly",
    guidance_scale=7.5
).images[0]
```

### Reproducible Generation

```python
import torch

# Set seed for reproducibility
generator = torch.Generator(device="cuda").manual_seed(42)

image = pipe(
    prompt="A cosmic nebula in space",
    generator=generator,
    num_inference_steps=50
).images[0]
```

## Best Practices

### Prompt Engineering

1. **Be specific and descriptive**:
   - ❌ "A dog"
   - ✅ "A golden retriever puppy sitting in a sunny meadow, soft lighting, high detail"

2. **Use artistic and quality modifiers**:
   - "masterpiece, best quality, highly detailed"
   - "8k, ultra high resolution, photorealistic"
   - "cinematic lighting, dramatic composition"

3. **Specify camera angles and perspectives**:
   - "bird's eye view", "close-up portrait", "wide angle landscape"

4. **Include style references**:
   - "in the style of Studio Ghibli"
   - "digital art", "oil painting", "photography"

### Performance Optimization

1. **Use appropriate image sizes**:
   - Flux works best with 1024x1024 or similar high resolutions
   - Always use multiples of 64 for dimensions

2. **Optimize inference steps**:
   - Start with 50 steps for quality
   - Reduce to 25-30 for faster generation
   - Use better schedulers to maintain quality with fewer steps

3. **Memory management**:
   ```python
   # Clear cache between generations
   torch.cuda.empty_cache()
   
   # Use gradient checkpointing for lower memory
   pipe.enable_attention_slicing("max")
   ```

4. **Batch processing**:
   - Process multiple prompts together when possible
   - Use `torch.no_grad()` context for inference

### Safety Considerations

1. **Content filtering**: Diffusers includes safety filters by default
2. **Resource monitoring**: Monitor GPU memory and temperature
3. **Rate limiting**: Don't overload the system with too many concurrent requests

## Troubleshooting & FAQ

### Common Issues

**Q: "CUDA out of memory" error**
```python
# Solutions:
pipe.enable_model_cpu_offload()
pipe.enable_attention_slicing()
# Or reduce image size/batch size
```

**Q: Images are blurry or low quality**
```python
# Increase inference steps
num_inference_steps=75

# Adjust guidance scale
guidance_scale=7.5  # Higher for more prompt adherence

# Use better scheduler
from diffusers import DDIMScheduler
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
```

**Q: Generation is too slow**
```python
# Enable xformers for faster attention
pipe.enable_xformers_memory_efficient_attention()

# Use fewer inference steps
num_inference_steps=25

# Smaller image size
height=512, width=512
```

**Q: Can't load the model**
```
# Check if you need authentication
huggingface-cli login

# Verify model name and availability
# Some models may require approval
```

### Performance Benchmarks

Typical generation times on various hardware:
- **RTX 4090**: ~10-15 seconds (1024x1024, 50 steps)
- **RTX 3080**: ~20-30 seconds (1024x1024, 50 steps)
- **RTX 3060**: ~45-60 seconds (1024x1024, 30 steps)

### Model Variants

- **FLUX.1-Kontext-dev**: Main model for development/research
- **FLUX.1-schnell**: Faster variant with fewer steps required
- **FLUX.1-pro**: Commercial version (via API)

## Safety and Licensing

### Model Licensing

- **FLUX.1-Kontext-dev**: Apache 2.0 license for research and commercial use
- Always check the specific model's license before commercial deployment
- Respect usage guidelines and content policies

### Ethical Considerations

1. **Content responsibility**: Be mindful of generated content
2. **Bias awareness**: Models may reflect training data biases
3. **Attribution**: Credit model creators when appropriate
4. **Privacy**: Don't generate content that violates privacy

### Compute Costs

- **GPU usage**: Monitor cloud compute costs
- **Energy consumption**: Consider environmental impact
- **Optimization**: Use efficient settings for production

### Content Safety

The Diffusers library includes safety filters by default. For production use:

```python
# Keep safety checker enabled (default)
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-Kontext-dev",
    safety_checker=None,  # Only disable for research if needed
    requires_safety_checker=False
)
```

---

For more examples and code samples, see the `examples/` directory in this guide.
For prompt engineering tips specific to Flux models, see `flux-prompting-guide.md`.