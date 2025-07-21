#!/usr/bin/env python3
"""
Image-to-Image Generation with Flux Models

A minimal CLI script for transforming existing images using text prompts
with the Hugging Face Diffusers library and Flux models.

Usage:
    python img2img.py input.jpg "Transform into a painting" --output painting.png
    python img2img.py photo.jpg "Make it look like a sketch" --strength 0.8
"""

import argparse
import torch
from diffusers import FluxImg2ImgPipeline
from PIL import Image
import os
import time


def load_and_resize_image(image_path, target_width, target_height):
    """Load and resize an image to target dimensions."""
    try:
        image = Image.open(image_path).convert("RGB")
        original_size = image.size
        
        # Resize to target dimensions
        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        print(f"Loaded image: {image_path}")
        print(f"Original size: {original_size}, Resized to: {image.size}")
        
        return image
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Transform images using text prompts with Flux models')
    parser.add_argument('input_image', type=str, help='Path to input image')
    parser.add_argument('prompt', type=str, help='Text prompt for transformation')
    parser.add_argument('--model', type=str, default='black-forest-labs/FLUX.1-Kontext-dev',
                      help='Model name from Hugging Face Hub')
    parser.add_argument('--output', '-o', type=str, default='transformed_image.png',
                      help='Output image filename')
    parser.add_argument('--width', type=int, default=1024,
                      help='Output image width (must be multiple of 64)')
    parser.add_argument('--height', type=int, default=1024,
                      help='Output image height (must be multiple of 64)')
    parser.add_argument('--strength', type=float, default=0.75,
                      help='Transformation strength (0.0-1.0, higher = more change)')
    parser.add_argument('--steps', type=int, default=50,
                      help='Number of inference steps')
    parser.add_argument('--guidance', type=float, default=3.5,
                      help='Guidance scale for prompt adherence')
    parser.add_argument('--seed', type=int, default=None,
                      help='Random seed for reproducible results')
    parser.add_argument('--negative-prompt', type=str, default='',
                      help='Negative prompt (what to avoid)')
    parser.add_argument('--cpu-offload', action='store_true',
                      help='Enable CPU offloading for memory optimization')
    parser.add_argument('--attention-slicing', action='store_true',
                      help='Enable attention slicing for memory optimization')
    parser.add_argument('--half-precision', action='store_true',
                      help='Use float16 instead of bfloat16 (may reduce quality)')
    parser.add_argument('--preserve-aspect', action='store_true',
                      help='Preserve aspect ratio of input image')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_image):
        print(f"Error: Input image '{args.input_image}' not found")
        return 1
    
    # Validate dimensions
    if args.width % 64 != 0 or args.height % 64 != 0:
        print("Warning: Width and height should be multiples of 64 for best results")
    
    # Validate strength
    if not 0.0 <= args.strength <= 1.0:
        print("Error: Strength must be between 0.0 and 1.0")
        return 1
    
    # Check CUDA availability
    if not torch.cuda.is_available():
        print("Warning: CUDA not available, using CPU (will be very slow)")
        device = "cpu"
        dtype = torch.float32
    else:
        device = "cuda"
        dtype = torch.float16 if args.half_precision else torch.bfloat16
    
    print(f"Loading model: {args.model}")
    print(f"Device: {device}, Dtype: {dtype}")
    
    try:
        # Load the pipeline
        pipeline = FluxImg2ImgPipeline.from_pretrained(
            args.model,
            torch_dtype=dtype
        )
        pipeline = pipeline.to(device)
        
        # Apply memory optimizations
        if args.cpu_offload:
            print("Enabling CPU offloading...")
            pipeline.enable_model_cpu_offload()
        
        if args.attention_slicing:
            print("Enabling attention slicing...")
            pipeline.enable_attention_slicing()
        
        # Try to enable xformers if available
        try:
            pipeline.enable_xformers_memory_efficient_attention()
            print("XFormers acceleration enabled")
        except Exception:
            print("XFormers not available, using default attention")
        
        # Load and prepare the input image
        if args.preserve_aspect:
            # Load image and calculate dimensions preserving aspect ratio
            temp_image = Image.open(args.input_image)
            aspect_ratio = temp_image.width / temp_image.height
            
            if aspect_ratio > 1:  # Landscape
                width = args.width
                height = int(args.width / aspect_ratio)
                # Round to nearest multiple of 64
                height = (height // 64) * 64
            else:  # Portrait or square
                height = args.height
                width = int(args.height * aspect_ratio)
                # Round to nearest multiple of 64
                width = (width // 64) * 64
        else:
            width, height = args.width, args.height
        
        # Load and resize the input image
        input_image = load_and_resize_image(args.input_image, width, height)
        if input_image is None:
            return 1
        
        # Set up generator for reproducible results
        generator = None
        if args.seed is not None:
            generator = torch.Generator(device=device).manual_seed(args.seed)
            print(f"Using seed: {args.seed}")
        
        print(f"\nTransforming image with prompt: '{args.prompt}'")
        print(f"Output resolution: {width}x{height}")
        print(f"Strength: {args.strength}, Steps: {args.steps}, Guidance: {args.guidance}")
        
        start_time = time.time()
        
        # Generate the transformed image
        result = pipeline(
            prompt=args.prompt,
            image=input_image,
            negative_prompt=args.negative_prompt if args.negative_prompt else None,
            strength=args.strength,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance,
            generator=generator
        )
        
        output_image = result.images[0]
        generation_time = time.time() - start_time
        
        # Save the image
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
        output_image.save(args.output)
        
        print(f"\nImage transformation completed!")
        print(f"Output saved to: {args.output}")
        print(f"Generation time: {generation_time:.2f} seconds")
        
        # Display image info
        print(f"Output image size: {output_image.size}")
        print(f"Output image mode: {output_image.mode}")
        
        # Optional: Save a side-by-side comparison
        if args.output.endswith('.png'):
            comparison_path = args.output.replace('.png', '_comparison.png')
        else:
            comparison_path = args.output.rsplit('.', 1)[0] + '_comparison.png'
        
        # Create side-by-side comparison
        comparison_width = width * 2
        comparison_height = height
        comparison = Image.new('RGB', (comparison_width, comparison_height))
        comparison.paste(input_image, (0, 0))
        comparison.paste(output_image, (width, 0))
        comparison.save(comparison_path)
        print(f"Side-by-side comparison saved to: {comparison_path}")
        
    except Exception as e:
        print(f"Error transforming image: {e}")
        return 1
    
    finally:
        # Clean up GPU memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    return 0


if __name__ == "__main__":
    exit(main())