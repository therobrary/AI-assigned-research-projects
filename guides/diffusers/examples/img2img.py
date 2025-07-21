#!/usr/bin/env python3
"""
Image-to-Image Transformation with Flux Models

A command-line tool for transforming existing images based on text prompts
using Hugging Face Diffusers library with Flux models.

Usage:
    python img2img.py --input photo.jpg --prompt "Transform into a watercolor painting"
    python img2img.py --input landscape.jpg --prompt "Make it cyberpunk" --strength 0.8
"""

import argparse
import os
import sys
import torch
from pathlib import Path
from PIL import Image
from typing import Optional

try:
    from diffusers import FluxImg2ImgPipeline
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

console = Console()

# Model configurations
MODELS = {
    "flux-dev": "black-forest-labs/FLUX.1-dev",
    "flux-kontext": "black-forest-labs/FLUX.1-Kontext-dev",
    "flux-schnell": "black-forest-labs/FLUX.1-schnell"
}

def check_cuda_availability():
    """Check if CUDA is available and provide helpful information."""
    if not torch.cuda.is_available():
        console.print("[red]❌ CUDA not available. Using CPU (very slow).[/red]")
        console.print("💡 For better performance, ensure you have:")
        console.print("   • NVIDIA GPU with CUDA support")
        console.print("   • PyTorch with CUDA enabled")
        return False
    
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    
    console.print(f"[green]✅ CUDA available[/green]")
    console.print(f"   GPU: {gpu_name}")
    console.print(f"   Memory: {gpu_memory:.1f} GB")
    
    if gpu_memory < 8:
        console.print("[yellow]⚠️  Low GPU memory detected. Consider using --cpu-offload.[/yellow]")
    
    return True

def load_pipeline(model_name: str, cpu_offload: bool = False, attention_slicing: bool = False):
    """Load the Flux img2img pipeline with specified optimizations."""
    
    if model_name not in MODELS:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(MODELS.keys())}")
    
    model_id = MODELS[model_name]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Loading {model_name} for img2img...", total=None)
        
        try:
            # Determine optimal dtype
            dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
            
            # Load pipeline
            pipe = FluxImg2ImgPipeline.from_pretrained(
                model_id,
                torch_dtype=dtype,
                low_cpu_mem_usage=True
            )
            
            # Apply optimizations
            if torch.cuda.is_available():
                if cpu_offload:
                    pipe.enable_model_cpu_offload()
                    console.print("[cyan]🔧 CPU offloading enabled[/cyan]")
                else:
                    pipe.to("cuda")
                
                if attention_slicing:
                    pipe.enable_attention_slicing(1)
                    console.print("[cyan]🔧 Attention slicing enabled[/cyan]")
                    
                # Enable VAE slicing for memory efficiency
                pipe.enable_vae_slicing()
                console.print("[cyan]🔧 VAE slicing enabled[/cyan]")
            
            progress.update(task, completed=True)
            console.print(f"[green]✅ Model {model_name} loaded successfully[/green]")
            
            return pipe
            
        except Exception as e:
            console.print(f"[red]❌ Failed to load model: {e}[/red]")
            raise

def load_and_prepare_image(image_path: str, target_width: int, target_height: int) -> Image.Image:
    """Load and prepare the input image."""
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")
    
    try:
        # Load image
        image = Image.open(image_path).convert("RGB")
        original_size = image.size
        
        console.print(f"[cyan]📷 Loaded image: {image_path}[/cyan]")
        console.print(f"   Original size: {original_size[0]}x{original_size[1]}")
        
        # Resize if needed
        if target_width and target_height:
            if image.size != (target_width, target_height):
                image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                console.print(f"   Resized to: {target_width}x{target_height}")
        
        return image
        
    except Exception as e:
        console.print(f"[red]❌ Failed to load image: {e}[/red]")
        raise

def transform_image(
    pipe,
    input_image: Image.Image,
    prompt: str,
    strength: float = 0.7,
    steps: int = 50,
    guidance_scale: float = 3.5,
    seed: Optional[int] = None
) -> Image.Image:
    """Transform an image based on a text prompt."""
    
    # Setup generator for reproducible results
    generator = None
    if seed is not None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        generator = torch.Generator(device).manual_seed(seed)
        console.print(f"[cyan]🎲 Using seed: {seed}[/cyan]")
    
    # Display transformation parameters
    params_panel = Panel(
        f"[bold]Prompt:[/bold] {prompt}\n"
        f"[bold]Input Size:[/bold] {input_image.width}x{input_image.height}\n"
        f"[bold]Strength:[/bold] {strength} (0.0=no change, 1.0=full change)\n"
        f"[bold]Steps:[/bold] {steps}\n"
        f"[bold]Guidance Scale:[/bold] {guidance_scale}\n"
        f"[bold]Seed:[/bold] {seed if seed else 'Random'}",
        title="Transformation Parameters",
        border_style="blue"
    )
    console.print(params_panel)
    
    # Transform image with progress tracking
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Transforming image...", total=None)
        
        try:
            result = pipe(
                prompt=prompt,
                image=input_image,
                strength=strength,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                generator=generator
            )
            
            progress.update(task, completed=True)
            console.print("[green]✅ Image transformed successfully[/green]")
            
            return result.images[0]
            
        except Exception as e:
            console.print(f"[red]❌ Transformation failed: {e}[/red]")
            raise

def save_image(image: Image.Image, output_path: str, prompt: str, input_path: str):
    """Save the transformed image with metadata."""
    
    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Add metadata to image
    metadata = {
        "prompt": prompt,
        "input_image": input_path,
        "generator": "Hugging Face Diffusers with Flux (img2img)"
    }
    
    # Save image
    image.save(output_path, format="PNG", pnginfo=metadata)
    
    # Display file info
    file_size = output_path.stat().st_size / (1024**2)  # MB
    console.print(f"[green]💾 Image saved: {output_path}[/green]")
    console.print(f"   Size: {file_size:.2f} MB")
    console.print(f"   Dimensions: {image.width}x{image.height}")

def main():
    parser = argparse.ArgumentParser(
        description="Transform images with text prompts using Flux models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input photo.jpg --prompt "Transform into a watercolor painting"
  %(prog)s --input landscape.jpg --prompt "Make it cyberpunk" --strength 0.8
  %(prog)s --input portrait.jpg --prompt "Add fantasy elements" --model flux-kontext
  %(prog)s --input sketch.jpg --prompt "Realistic photo" --strength 0.9 --steps 75

Strength Guide:
  0.1-0.3: Subtle changes, preserve most details
  0.4-0.6: Moderate transformation
  0.7-0.9: Strong transformation
  0.9-1.0: Complete reimagining
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input image"
    )
    
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Text prompt describing the desired transformation"
    )
    
    # Model selection
    parser.add_argument(
        "--model", "-m",
        choices=list(MODELS.keys()),
        default="flux-dev",
        help="Flux model to use (default: flux-dev)"
    )
    
    # Transformation parameters
    parser.add_argument(
        "--strength", "-t",
        type=float,
        default=0.7,
        help="Transformation strength (default: 0.7, range: 0.0-1.0)"
    )
    
    # Image parameters
    parser.add_argument(
        "--width", "-w",
        type=int,
        help="Output image width (default: keep original, must be multiple of 64)"
    )
    
    parser.add_argument(
        "--height", "-h",
        type=int,
        help="Output image height (default: keep original, must be multiple of 64)"
    )
    
    # Generation parameters
    parser.add_argument(
        "--steps", "-s",
        type=int,
        default=50,
        help="Number of inference steps (default: 50, range: 20-100)"
    )
    
    parser.add_argument(
        "--guidance-scale", "-g",
        type=float,
        default=3.5,
        help="Guidance scale for prompt adherence (default: 3.5, range: 1.0-20.0)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible results"
    )
    
    # Output options
    parser.add_argument(
        "--output", "-o",
        help="Output image path (default: adds '_transformed' to input filename)"
    )
    
    # Performance options
    parser.add_argument(
        "--cpu-offload",
        action="store_true",
        help="Enable CPU offloading to save GPU memory"
    )
    
    parser.add_argument(
        "--attention-slicing",
        action="store_true",
        help="Enable attention slicing to reduce memory usage"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set default output path if not provided
    if not args.output:
        input_path = Path(args.input)
        args.output = input_path.parent / f"{input_path.stem}_transformed{input_path.suffix}"
    
    # Validate arguments
    if args.width and args.width % 64 != 0:
        console.print("[red]❌ Width must be a multiple of 64[/red]")
        sys.exit(1)
    
    if args.height and args.height % 64 != 0:
        console.print("[red]❌ Height must be a multiple of 64[/red]")
        sys.exit(1)
    
    if not (0.0 <= args.strength <= 1.0):
        console.print("[red]❌ Strength must be between 0.0 and 1.0[/red]")
        sys.exit(1)
    
    if not (20 <= args.steps <= 100):
        console.print("[yellow]⚠️  Steps outside recommended range (20-100)[/yellow]")
    
    if not (1.0 <= args.guidance_scale <= 20.0):
        console.print("[yellow]⚠️  Guidance scale outside recommended range (1.0-20.0)[/yellow]")
    
    # Display welcome message
    console.print(Panel(
        "[bold magenta]Flux Image-to-Image Transformer[/bold magenta]\n"
        "Transform existing images with text prompts using state-of-the-art Flux models",
        border_style="magenta"
    ))
    
    try:
        # Check system capabilities
        check_cuda_availability()
        
        # Load and prepare input image
        input_image = load_and_prepare_image(args.input, args.width, args.height)
        
        # Load pipeline
        pipe = load_pipeline(
            args.model,
            cpu_offload=args.cpu_offload,
            attention_slicing=args.attention_slicing
        )
        
        # Transform image
        transformed_image = transform_image(
            pipe=pipe,
            input_image=input_image,
            prompt=args.prompt,
            strength=args.strength,
            steps=args.steps,
            guidance_scale=args.guidance_scale,
            seed=args.seed
        )
        
        # Save result
        save_image(transformed_image, args.output, args.prompt, args.input)
        
        console.print(Panel(
            "[green]🎨 Transformation completed successfully![/green]\n"
            f"Your transformed image has been saved to: [bold]{args.output}[/bold]",
            border_style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Transformation interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()