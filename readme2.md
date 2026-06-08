# ComfyUI Setup Guide — Image & Small Video Generation

This guide explains how to install, configure, and run ComfyUI on **Windows** for **image generation** and **short video clips**. It is written for laptops/PCs **without an NVIDIA GPU** (Intel integrated graphics or CPU-only).

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start (Already Installed)](#quick-start-already-installed)
3. [Full Installation From Scratch](#full-installation-from-scratch)
4. [Folder Structure](#folder-structure)
5. [Download Models](#download-models)
6. [Run ComfyUI](#run-comfyui)
7. [Run with Docker (Windows & Linux)](#run-with-docker-windows--linux)
8. [Generate Images](#generate-images)
9. [Install Video Nodes](#install-video-nodes)
10. [Generate Small Videos](#generate-small-videos)
11. [Lion Play With Girl Video Workflow](#lion-play-with-girl-video-workflow)
12. [Recommended Settings](#recommended-settings)
13. [Install More Models & Nodes](#install-more-models--nodes)
14. [Troubleshooting](#troubleshooting)

---

## System Requirements

| Requirement | Minimum | Notes |
|-------------|---------|-------|
| **OS** | Windows 10/11 (64-bit) | Tested on Windows 10/11 |
| **RAM** | 16 GB | 8 GB may work but is not recommended |
| **Disk space** | 20 GB free | ~5 GB for app + ~4 GB for starter models |
| **GPU** | None required | CPU mode is used when no NVIDIA GPU is present |
| **Python** | 3.12 | Installed automatically in `venv` during setup |
| **Git** | Required | For cloning ComfyUI and custom nodes |
| **Internet** | Required | For first-time model download |

### Tested hardware (example)

| Item | Value |
|------|-------|
| Device | AL01LAP142 |
| CPU | Intel Core i5-1135G7 (11th Gen) |
| RAM | 16 GB |
| GPU | Intel Iris Xe (integrated) |
| Mode | CPU (no CUDA) |

> **Important:** Intel integrated graphics (Iris Xe / UHD) does **not** support NVIDIA CUDA. ComfyUI runs in **CPU mode**. Image generation works but is slower than on a dedicated NVIDIA GPU.

---

## Quick Start (Already Installed)

If this folder is already set up, follow these 3 steps:

### Step 1 — Download models (first time only)

Double-click:

```
download_models.bat
```

Wait until you see **"All starter models ready"** (~4.5 GB download, 10–30 minutes depending on internet speed).

### Step 2 — Install video nodes (first time only, for video workflows)

Double-click:

```
install_video_nodes.bat
```

Wait until it finishes, then continue to Step 3.

### Step 3 — Start ComfyUI

Double-click:

```
run_comfyui.bat
```

### Step 4 — Open in browser

Go to:

```
http://127.0.0.1:8188
```

---

## Full Installation From Scratch

Use this section if you are setting up ComfyUI on a **new PC** from an empty folder.

### Prerequisites

Install these first:

1. **Python 3.12** — https://www.python.org/downloads/
   - During install, check **"Add Python to PATH"**
2. **Git** — https://git-scm.com/download/win

Verify in PowerShell or Command Prompt:

```powershell
py -3.12 --version
git --version
```

### Step 1 — Clone ComfyUI

Open PowerShell and run:

```powershell
cd C:\path\to\your\folder
git clone https://github.com/comfyanonymous/ComfyUI.git comfyUI
cd comfyUI
```

### Step 2 — Create virtual environment

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### Step 3 — Install PyTorch (CPU version)

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Step 4 — Install ComfyUI dependencies

```powershell
pip install -r requirements.txt
```

### Step 5 — Install custom nodes

```powershell
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
git clone https://github.com/kijai/ComfyUI-KJNodes.git
cd ..
```

Install node dependencies:

```powershell
pip install -r custom_nodes\ComfyUI-Manager\requirements.txt
pip install -r custom_nodes\ComfyUI-VideoHelperSuite\requirements.txt
pip install -r custom_nodes\ComfyUI-KJNodes\requirements.txt
```

### Step 6 — Download starter models

```powershell
python download_models.py
```

Or double-click `download_models.bat`.

### Step 7 — Start ComfyUI

Double-click `run_comfyui.bat` or run manually:

```powershell
.\venv\Scripts\Activate.ps1
python main.py --cpu --cpu-vae --preview-method none --preview-size 256 --listen 127.0.0.1 --port 8188 --enable-manager
```

---

## Folder Structure

```
comfyUI/
├── run_comfyui.bat          # Start ComfyUI (double-click this)
├── download_models.bat      # Download starter AI models
├── install_video_nodes.bat  # Install AnimateDiff + video nodes
├── download_models.py       # Model download script
├── README2.md               # This guide
├── main.py                  # ComfyUI entry point
├── venv/                    # Python virtual environment (do not delete)
├── models/
│   ├── checkpoints/         # Main image models (.safetensors)
│   │   └── v1-5-pruned-emaonly.safetensors
│   └── vae/                 # VAE models
│       └── diffusion_pytorch_model.safetensors
├── output/                  # Generated images and videos appear here
├── input/                   # Put input images here
├── custom_nodes/
│   ├── animatediff_models/  # AnimateDiff motion models
│   │   └── mm_sd_v15_v2.ckpt
│   ├── ComfyUI-Manager/     # Install nodes & models from UI
│   ├── ComfyUI-AnimateDiff-Evolved/  # Text-to-video animation
│   ├── ComfyUI-VideoHelperSuite/  # Export frames to MP4/GIF
│   └── ComfyUI-KJNodes/     # Extra utility nodes
└── user/
    └── default/
        └── workflows/
            └── video_lion_play_girl.json  # Ready-made video workflow
```

---

## Download Models

### Automatic (recommended)

Double-click:

```
download_models.bat
```

This downloads:

| Model | File | Size | Purpose |
|-------|------|------|---------|
| Stable Diffusion 1.5 | `v1-5-pruned-emaonly.safetensors` | ~4 GB | Main image generation |
| SD VAE | `diffusion_pytorch_model.safetensors` | ~320 MB | Better image quality |
| AnimateDiff motion | `mm_sd_v15_v2.ckpt` | ~1.8 GB | Short video animation |

### Manual download

Place files in these folders:

- Checkpoints → `models\checkpoints\`
- VAE → `models\vae\`
- AnimateDiff → `models\animatediff_models\`

Download links:

- SD 1.5: https://huggingface.co/runwayml/stable-diffusion-v1-5
- VAE: https://huggingface.co/stabilityai/sd-vae-ft-mse
- AnimateDiff: https://huggingface.co/guoyww/animatediff

---

## Run ComfyUI

### Option A — Batch file (easiest)

Double-click:

```
run_comfyui.bat
```

### Option B — Command line

```powershell
cd C:\Users\YourName\path\to\comfyUI
.\venv\Scripts\Activate.ps1
python main.py --cpu --cpu-vae --preview-method none --preview-size 256 --listen 127.0.0.1 --port 8188 --enable-manager
```

### Open the UI

Open your browser and go to:

```
http://127.0.0.1:8188
```

### Stop ComfyUI

Press `Ctrl + C` in the terminal window, or close the command prompt window.

### Launch flags explained

| Flag | Purpose |
|------|---------|
| `--cpu` | Use CPU for all processing (required without NVIDIA GPU) |
| `--cpu-vae` | Run VAE decoder on CPU (saves memory) |
| `--preview-method none` | Disable live previews (saves RAM) |
| `--preview-size 256` | Smaller preview size if previews are enabled |
| `--listen 127.0.0.1` | Only allow local access (safer) |
| `--port 8188` | Web UI port (default) |
| `--enable-manager` | Enable built-in node manager (required for missing-node install prompts) |

---

## Run with Docker (Windows & Linux)

Use Docker when you want the same setup on **Windows** and **Linux** without installing Python locally.

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Docker Desktop** (Windows) or **Docker Engine** (Linux) | https://docs.docker.com/get-docker/ |
| **Docker Compose v2** | Included with Docker Desktop |
| **Disk space** | ~8 GB for image + models |
| **RAM** | 16 GB recommended for CPU mode |

### Quick start (Docker)

**Windows** — double-click:

```
run_docker.bat
```

**Linux / macOS** — in terminal:

```bash
chmod +x run_docker.sh download_models_docker.sh
./run_docker.sh
```

**First time only** — download models (~4.5 GB):

| OS | Command |
|----|---------|
| Windows | `download_models_docker.bat` |
| Linux | `./download_models_docker.sh` |

Or manually:

```bash
docker compose --profile setup run --rm download-models
```

Open: **http://127.0.0.1:8188**

### Docker commands

| Action | Command |
|--------|---------|
| Start | `docker compose up -d --build` |
| Stop | `docker compose down` |
| View logs | `docker compose logs -f comfyui` |
| Restart | `docker compose restart comfyui` |

### What is persisted

These host folders are mounted into the container:

| Folder | Purpose |
|--------|---------|
| `models/` | Checkpoints, VAE, AnimateDiff weights |
| `input/` | Input images/videos |
| `output/` | Generated images and videos |
| `user/` | Workflows, settings, ComfyUI Manager config |

Video nodes (AnimateDiff, VideoHelperSuite, Manager) are baked into the Docker image.

### GPU mode (optional, NVIDIA only)

If the machine has an NVIDIA GPU and the NVIDIA Container Toolkit is installed:

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build
```

### Docker vs local Python

| Method | Best for |
|--------|----------|
| `run_comfyui.bat` | Windows laptop without Docker |
| `run_docker.bat` / `run_docker.sh` | Same setup on Windows and Linux servers |

---

## Install Video Nodes

Video workflows need **AnimateDiff** and **VideoHelperSuite**. Install them once:

### Automatic (recommended)

Double-click:

```
install_video_nodes.bat
```

This script:

1. Installs `comfyui-manager` Python package
2. Clones **ComfyUI-AnimateDiff-Evolved**
3. Clones **ComfyUI-VideoHelperSuite** (if missing)
4. Installs node dependencies
5. Downloads the AnimateDiff motion model

### Manual install

```powershell
cd C:\path\to\comfyUI
.\venv\Scripts\Activate.ps1
pip install -r manager_requirements.txt
cd custom_nodes
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
cd ..
pip install -r custom_nodes\ComfyUI-VideoHelperSuite\requirements.txt
python download_models.py
```

### After installing — always restart ComfyUI

Close the ComfyUI terminal window completely, then run `run_comfyui.bat` again. Custom nodes only load at startup.

---

## Generate Images

### Using a built-in template (easiest)

1. Open **http://127.0.0.1:8188**
2. Click **Workflow** → **Browse Templates**
3. Choose an **Image** template (e.g. "Text to Image")
4. In the **Load Checkpoint** node, select: `v1-5-pruned-emaonly.safetensors`
5. In the **Load VAE** node, select: `diffusion_pytorch_model.safetensors`
6. Type your prompt, for example:
   ```
   a sunset over mountains, photorealistic, 4k
   ```
7. Click **Queue Prompt**
8. Wait for generation to finish
9. Find the output image in the `output\` folder

### Recommended image settings (16 GB RAM / CPU)

| Setting | Value |
|---------|-------|
| Resolution | **512 × 512** |
| Steps | **15–20** |
| CFG Scale | **7** |
| Sampler | `euler` or `dpmpp_2m` |
| Batch size | **1** |

### Expected speed (CPU, i5-class laptop)

| Task | Approximate time |
|------|------------------|
| 512×512 image, 20 steps | 5–15 minutes |
| 768×768 image | 15–30+ minutes |
| SDXL models | Not recommended on CPU |

---

## Generate Small Videos

ComfyUI supports short video clips using **AnimateDiff** + **VideoHelperSuite**. On CPU this is **much slower** than images.

### Prerequisites

1. Run `install_video_nodes.bat` (first time only)
2. Run `download_models.bat` (includes AnimateDiff motion model)
3. Start ComfyUI with `run_comfyui.bat` (includes `--enable-manager`)
4. **Restart ComfyUI** after installing any new nodes

### Video tips for CPU / 16 GB RAM

| Setting | Recommended value |
|---------|-------------------|
| Resolution | 512 × 512 |
| Frame count | 12 frames (about 1.5 seconds at 8 fps) |
| Steps | 15–20 |
| Model | SD 1.5 only |

> Expect **30–60+ minutes** for a short animated clip on CPU.

---

## Lion Play With Girl Video Workflow

A ready-made workflow is included for generating a short video of a girl playing with a friendly lion.

### Workflow file

```
user\default\workflows\video_lion_play_girl.json
```

### How to load and run

1. Run `install_video_nodes.bat` if you have not already
2. Run `download_models.bat` if you have not already
3. Start ComfyUI with `run_comfyui.bat`
4. Open **http://127.0.0.1:8188**
5. Load the workflow:
   - **Workflow** → **Open** → select `video_lion_play_girl.json`
   - Or drag the JSON file into the ComfyUI window
6. Verify these nodes are **not red** on the canvas:
   - **AnimateDiff Loader** (node #10)
   - **Video Combine** (VHS node)
7. Click **Queue Prompt**
8. Wait for generation to finish
9. Output video saves to `output\` as `lion_play_girl_*.mp4`

### What the workflow contains

| Node | Purpose |
|------|---------|
| CheckpointLoaderSimple | Loads SD 1.5 (`v1-5-pruned-emaonly.safetensors`) |
| ADE_AnimateDiffLoaderGen1 | Adds motion using `mm_sd_v15_v2.ckpt` |
| CLIPTextEncode (positive) | Prompt: girl playing with friendly lion in savanna |
| CLIPTextEncode (negative) | Blocks low quality, violence, scary content |
| EmptyLatentImage | 512×512, 12 frames |
| KSampler | 15 steps, CFG 7, euler sampler |
| VAEDecode | Converts latent frames to images |
| VHS_VideoCombine | Exports MP4 at 8 fps |

### Required models

| Model | Path |
|-------|------|
| SD 1.5 checkpoint | `models\checkpoints\v1-5-pruned-emaonly.safetensors` |
| AnimateDiff motion | `models\animatediff_models\mm_sd_v15_v2.ckpt` |

### Customize the prompt

Double-click the **positive CLIP Text Encode** node and edit the text. Example:

```
masterpiece, best quality, a young girl playing with a friendly lion
in a sunny savanna meadow, gentle playful interaction, warm sunlight
```

---

## Recommended Settings

### Do use

- SD 1.5 models (`v1-5-pruned-emaonly.safetensors`)
- 512×512 resolution
- 15–20 sampling steps
- Batch size of 1
- Built-in workflow templates

### Avoid on this hardware

- SDXL models (too large and slow on CPU)
- 1024×1024 or higher resolution
- Large video models (SVD, Wan, etc.)
- Batch size greater than 1

---

## Install More Models & Nodes

### Using ComfyUI Manager (recommended)

1. Start ComfyUI
2. Click the **Manager** button in the UI
3. Use **Model Manager** to search and install models
4. Use **Install Custom Nodes** to add new features
5. Restart ComfyUI after installing nodes

### Popular add-ons for video

| Node pack | Purpose |
|-----------|---------|
| ComfyUI-AnimateDiff-Evolved | Text/image to short animation |
| ComfyUI-VideoHelperSuite | Export frames to MP4/GIF (already installed) |

### Model folders

| Type | Folder |
|------|--------|
| Checkpoints | `models\checkpoints\` |
| VAE | `models\vae\` |
| AnimateDiff | `models\animatediff_models\` |
| LoRA | `models\loras\` |
| ControlNet | `models\controlnet\` |
| Upscale | `models\upscale_models\` |

---

## Troubleshooting

### "Missing Node Packs" or "Node has no class_type" (AnimateDiff)

```
Missing Node Packs (1)
comfyui-animatediff-evolved (1)
Node 'ID #10' has no class_type. The workflow may be corrupted or a custom node is missing.
```

**Fix (do all steps in order):**

1. **Close ComfyUI completely** (close the terminal window)

2. **Install video nodes:**
   ```
   install_video_nodes.bat
   ```

3. **Start ComfyUI with manager enabled** (use the batch file — it now includes `--enable-manager`):
   ```
   run_comfyui.bat
   ```

4. **Verify nodes loaded** — in the ComfyUI terminal you should see:
   ```
   ComfyUI-AnimateDiff-Evolved
   ComfyUI-VideoHelperSuite
   ```

5. **Reload the workflow** — open `video_lion_play_girl.json` again

6. If the UI still shows "Install missing nodes", click **Install** in the dialog, then restart ComfyUI again

**Manual fix via command line:**

```powershell
cd C:\path\to\comfyUI
.\venv\Scripts\Activate.ps1
pip install -U --pre comfyui-manager
python main.py --cpu --cpu-vae --enable-manager --listen 127.0.0.1 --port 8188
```

> **Important:** Custom nodes are only loaded when ComfyUI **starts**. Installing nodes while ComfyUI is running will not work until you restart.

### KSampler error: `OSError: [Errno 22] Invalid argument`

**Error example:**

```
Node Type: KSampler
OSError: [Errno 22] Invalid argument
```

This is **not** a model or workflow problem. On Windows, it happens when the **progress bar (tqdm)** conflicts with ComfyUI Manager's stderr logging during sampling.

**Fix:**

1. Close ComfyUI completely
2. Start again using **`run_comfyui.bat`**
3. Re-run the workflow

Do **not** use `launch_comfyui.py` — start with **`run_comfyui.bat`** only.

**Note:** Progress bars will not show in the terminal, but generation will work. Video may take **30–60+ minutes** on CPU — that is normal.

If you still run out of memory, reduce **Empty Latent Image → batch_size** from `12` to `8` in the workflow.

### ComfyUI does not open in browser

- Make sure `run_comfyui.bat` is running (terminal window must stay open)
- Try: http://127.0.0.1:8188
- Check if port 8188 is in use:
  ```powershell
  netstat -ano | findstr ":8188"
  ```

### "No checkpoint models found"

Run `download_models.bat` and wait for it to finish. Verify this file exists:

```
models\checkpoints\v1-5-pruned-emaonly.safetensors
```

### Out of memory / PC freezes

- Lower resolution to **512×512**
- Reduce steps to **15**
- Set batch size to **1**
- Close other applications before generating
- Restart ComfyUI

### Very slow generation

This is normal on CPU. Tips:

- Use SD 1.5, not SDXL
- Use 512×512 resolution
- Use fewer steps (15–20)
- Be patient — 5–15 minutes per image is expected

### `python` or `pip` not found

Activate the virtual environment first:

```powershell
.\venv\Scripts\Activate.ps1
```

Or use the full path:

```powershell
.\venv\Scripts\python.exe main.py --cpu
```

### CUDA / GPU errors

This setup uses **CPU mode** on purpose. Always start with:

```
run_comfyui.bat
```

Do not remove the `--cpu` flag unless you have an NVIDIA GPU and CUDA installed.

### Custom node import errors

Run the video nodes installer, or reinstall manually:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r manager_requirements.txt
pip install -r custom_nodes\ComfyUI-Manager\requirements.txt
pip install -r custom_nodes\ComfyUI-VideoHelperSuite\requirements.txt
pip install -r custom_nodes\ComfyUI-KJNodes\requirements.txt
```

Then restart ComfyUI.

### "No motion models found" (AnimateDiff)

Verify this file exists:

```
models\animatediff_models\mm_sd_v15_v2.ckpt
```

If missing, run `download_models.bat`.

### Re-download models

```powershell
.\venv\Scripts\Activate.ps1
python download_models.py
```

Already-downloaded files are skipped automatically.

---

## Quick Reference

| Action | Command / File |
|--------|----------------|
| Download models | `download_models.bat` |
| Install video nodes | `install_video_nodes.bat` |
| Start ComfyUI | `run_comfyui.bat` |
| Lion video workflow | `user\default\workflows\video_lion_play_girl.json` |
| Open UI | http://127.0.0.1:8188 |
| Output images/videos | `output\` folder |
| Input images | `input\` folder |
| Stop server | `Ctrl + C` in terminal |

---

## Support & Links

- ComfyUI official repo: https://github.com/comfyanonymous/ComfyUI
- ComfyUI Manager: https://github.com/ltdrdata/ComfyUI-Manager
- Video Helper Suite: https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
- AnimateDiff Evolved: https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
- SD 1.5 model: https://huggingface.co/runwayml/stable-diffusion-v1-5
- AnimateDiff motion model: https://huggingface.co/guoyww/animatediff

---

*Last updated: June 2026 — Configured for Windows, CPU mode, 16 GB RAM, Intel integrated graphics.*
