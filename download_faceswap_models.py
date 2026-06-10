"""Download ReActor face swap and face restoration models."""

import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
FACE_RESTORE = BASE / "models" / "facerestore_models"
INSIGHTFACE = BASE / "models" / "insightface"

FACE_RESTORE.mkdir(parents=True, exist_ok=True)
INSIGHTFACE.mkdir(parents=True, exist_ok=True)

MODELS = [
    (
        "https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/facerestore_models/codeformer-v0.1.0.pth",
        FACE_RESTORE / "codeformer-v0.1.0.pth",
        "CodeFormer face restoration",
    ),
    (
        "https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/facerestore_models/GFPGANv1.4.pth",
        FACE_RESTORE / "GFPGANv1.4.pth",
        "GFPGAN face restoration",
    ),
    (
        "https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/inswapper_128.onnx",
        INSIGHTFACE / "inswapper_128.onnx",
        "Inswapper face swap model",
    ),
]


def download(url: str, dest: Path, label: str) -> None:
    if dest.exists():
        print(f"[skip] {label} already exists: {dest.name}")
        return
    print(f"[download] {label}...")
    urllib.request.urlretrieve(url, dest)
    print(f"[done] {dest}")


def main() -> None:
    print("Downloading face swap HQ models\n")
    for url, dest, label in MODELS:
        download(url, dest, label)
    print("\nFace swap models ready.")
    print(f"  Face restore: {FACE_RESTORE}")
    print(f"  InsightFace:  {INSIGHTFACE}")
    print("  buffalo_l downloads automatically on first ReActor run.")


if __name__ == "__main__":
    main()
