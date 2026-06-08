"""Download starter models for ComfyUI on CPU (Intel i5 / 16GB RAM)."""

import os
from pathlib import Path

from huggingface_hub import hf_hub_download

BASE = Path(__file__).resolve().parent
CHECKPOINTS = BASE / "models" / "checkpoints"
VAE = BASE / "models" / "vae"
ANIMATEDIFF = BASE / "models" / "animatediff_models"

CHECKPOINTS.mkdir(parents=True, exist_ok=True)
VAE.mkdir(parents=True, exist_ok=True)
ANIMATEDIFF.mkdir(parents=True, exist_ok=True)


def download(repo_id: str, filename: str, local_dir: Path, label: str) -> None:
    dest = local_dir / filename
    if dest.exists():
        print(f"[skip] {label} already exists: {dest.name}")
        return
    print(f"[download] {label} ({repo_id}/{filename})...")
    path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=str(local_dir),
    )
    print(f"[done] {path}")


def main() -> None:
    print("Downloading models optimized for CPU / 16GB RAM\n")

    # SD 1.5 - best balance of quality and speed on CPU
    download(
        "runwayml/stable-diffusion-v1-5",
        "v1-5-pruned-emaonly.safetensors",
        CHECKPOINTS,
        "Stable Diffusion 1.5 checkpoint",
    )

    # External VAE improves image quality for SD 1.5
    download(
        "stabilityai/sd-vae-ft-mse",
        "diffusion_pytorch_model.safetensors",
        VAE,
        "SD 1.5 VAE",
    )

    # AnimateDiff motion model for short video generation
    download(
        "guoyww/animatediff",
        "mm_sd_v15_v2.ckpt",
        ANIMATEDIFF,
        "AnimateDiff motion model (SD 1.5)",
    )

    print("\nAll starter models ready.")
    print(f"  Checkpoints:   {CHECKPOINTS}")
    print(f"  VAE:           {VAE}")
    print(f"  AnimateDiff:   {ANIMATEDIFF}")


if __name__ == "__main__":
    main()
