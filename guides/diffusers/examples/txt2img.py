#!/usr/bin/env python3
"""
Text-to-Image Generation with Flux Models

A command-line tool for generating images from text prompts using Hugging Face
Diffusers library with Flux models.

Usage:
    python txt2img.py --prompt "A beautiful sunset over mountains"
    python txt2img.py --prompt "A cyberpunk city" --model flux-dev --steps 50
"""

import argparse
import os
import sys
import torch
from pathlib import Path
from PIL import Image
from typing import Optional

try:
    from diffusers import FluxPipeline
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
    """Load the Flux pipeline with specified optimizations."""
    
    if model_name not in MODELS:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(MODELS.keys())}")
    
    model_id = MODELS[model_name]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Loading {model_name}...", total=None)
        
        try:
            # Determine optimal dtype
            dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
            
            # Load pipeline
            pipe = FluxPipeline.from_pretrained(
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
            
            progress.update(task, completed=True)
            console.print(f"[green]✅ Model {model_name} loaded successfully[/green]")
            
            return pipe
            
        except Exception as e:
            console.print(f"[red]❌ Failed to load model: {e}[/red]")
            raise

def generate_image(
    pipe,
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    steps: int = 50,
    guidance_scale: float = 3.5,
    seed: Optional[int] = None
) -> Image.Image:
    """Generate an image from a text prompt."""
    
    # Setup generator for reproducible results
    generator = None
    if seed is not None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        generator = torch.Generator(device).manual_seed(seed)
        console.print(f"[cyan]🎲 Using seed: {seed}[/cyan]")
    
    # Display generation parameters
    params_panel = Panel(
        f"[bold]Prompt:[/bold] {prompt}\n"
        f"[bold]Dimensions:[/bold] {width}x{height}\n"
        f"[bold]Steps:[/bold] {steps}\n"
        f"[bold]Guidance Scale:[/bold] {guidance_scale}\n"
        f"[bold]Seed:[/bold] {seed if seed else 'Random'}",
        title="Generation Parameters",
        border_style="blue"
    )
    console.print(params_panel)
    
    # Generate image with progress tracking
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Generating image...", total=None)
        
        try:
            result = pipe(
                prompt=prompt,
                width=width,
                height=height,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                generator=generator
            )
            
            progress.update(task, completed=True)
            console.print("[green]✅ Image generated successfully[/green]")
            
            return result.images[0]
            
        except Exception as e:
            console.print(f"[red]❌ Generation failed: {e}[/red]")
            raise

def save_image(image: Image.Image, output_path: str, prompt: str):
    """Save the generated image with metadata."""
    
    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Add metadata to image
    metadata = {
        "prompt": prompt,
        "generator": "Hugging Face Diffusers with Flux"
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
        description="Generate images from text prompts using Flux models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --prompt "A serene mountain landscape at sunset"
  %(prog)s --prompt "Cyberpunk city at night" --model flux-dev --steps 50
  %(prog)s --prompt "Portrait of a cat" --width 512 --height 768 --seed 42
  %(prog)s --prompt "Abstract art" --cpu-offload --attention-slicing
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Text prompt describing the image to generate"
    )
    
    # Model selection
    parser.add_argument(
        "--model", "-m",
        choices=list(MODELS.keys()),
        default="flux-dev",
        help="Flux model to use (default: flux-dev)"
    )
    
    # Image parameters
    parser.add_argument(
        "--width", "-w",
        type=int,
        default=1024,
        help="Image width in pixels (default: 1024, must be multiple of 64)"
    )
    
    parser.add_argument(
        "--height", "-h",
        type=int,
        default=1024,
        help="Image height in pixels (default: 1024, must be multiple of 64)"
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
        default="generated_image.png",
        help="Output image path (default: generated_image.png)"
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
    
    # Validate arguments
    if args.width % 64 != 0 or args.height % 64 != 0:
        console.print("[red]❌ Width and height must be multiples of 64[/red]")
        sys.exit(1)
    
    if not (20 <= args.steps <= 100):
        console.print("[yellow]⚠️  Steps outside recommended range (20-100)[/yellow]")
    
    if not (1.0 <= args.guidance_scale <= 20.0):
        console.print("[yellow]⚠️  Guidance scale outside recommended range (1.0-20.0)[/yellow]")
    
    # Display welcome message
    console.print(Panel(
        "[bold cyan]Flux Text-to-Image Generator[/bold cyan]\n"
        "Generate beautiful images from text prompts using state-of-the-art Flux models",
        border_style="cyan"
    ))
    
    try:
        # Check system capabilities
        check_cuda_availability()
        
        # Load pipeline
        pipe = load_pipeline(
            args.model,
            cpu_offload=args.cpu_offload,
            attention_slicing=args.attention_slicing
        )
        
        # Generate image
        image = generate_image(
            pipe=pipe,
            prompt=args.prompt,
            width=args.width,
            height=args.height,
            steps=args.steps,
            guidance_scale=args.guidance_scale,
            seed=args.seed
        )
        
        # Save result
        save_image(image, args.output, args.prompt)
        
        console.print(Panel(
            "[green]🎉 Generation completed successfully![/green]\n"
            f"Your image has been saved to: [bold]{args.output}[/bold]",
            border_style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Generation interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()