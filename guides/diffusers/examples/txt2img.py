#!/usr/bin/env python3
"""
Text-to-Image Generation with Flux Models

A minimal CLI script for generating images from text prompts using 
the Hugging Face Diffusers library and Flux models.

Usage:
    python txt2img.py "A beautiful sunset over mountains" --output sunset.png
    python txt2img.py "A cute cat wearing a hat" --steps 30 --guidance 7.5
"""

import argparse
import torch
from diffusers import FluxPipeline
from PIL import Image
import os
import time


def main():
    parser = argparse.ArgumentParser(description='Generate images from text prompts using Flux models')
    parser.add_argument('prompt', type=str, help='Text prompt for image generation')
    parser.add_argument('--model', type=str, default='black-forest-labs/FLUX.1-Kontext-dev',
                      help='Model name from Hugging Face Hub')
    parser.add_argument('--output', '-o', type=str, default='generated_image.png',
                      help='Output image filename')
    parser.add_argument('--width', type=int, default=1024,
                      help='Image width (must be multiple of 64)')
    parser.add_argument('--height', type=int, default=1024,
                      help='Image height (must be multiple of 64)')
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
    
    args = parser.parse_args()
    
    # Validate dimensions
    if args.width % 64 != 0 or args.height % 64 != 0:
        print("Warning: Width and height should be multiples of 64 for best results")
    
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
        pipeline = FluxPipeline.from_pretrained(
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
        
        # Set up generator for reproducible results
        generator = None
        if args.seed is not None:
            generator = torch.Generator(device=device).manual_seed(args.seed)
            print(f"Using seed: {args.seed}")
        
        print(f"\nGenerating image for prompt: '{args.prompt}'")
        print(f"Resolution: {args.width}x{args.height}")
        print(f"Steps: {args.steps}, Guidance: {args.guidance}")
        
        start_time = time.time()
        
        # Generate the image
        result = pipeline(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt if args.negative_prompt else None,
            width=args.width,
            height=args.height,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance,
            generator=generator
        )
        
        image = result.images[0]
        generation_time = time.time() - start_time
        
        # Save the image
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
        image.save(args.output)
        
        print(f"\nImage generated successfully!")
        print(f"Output saved to: {args.output}")
        print(f"Generation time: {generation_time:.2f} seconds")
        
        # Display image info
        print(f"Image size: {image.size}")
        print(f"Image mode: {image.mode}")
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return 1
    
    finally:
        # Clean up GPU memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    return 0


if __name__ == "__main__":
    exit(main())