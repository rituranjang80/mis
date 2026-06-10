# ComfyUI Setup Guide — Image, Video & Face Swap

This guide explains how to install, configure, and run ComfyUI for **image generation**, **short video clips**, and **face swap**. Supports **Windows** and **Linux** via local Python, **Docker**, or **Kubernetes** (auto-scaling).

Written for laptops/PCs **without an NVIDIA GPU** (Intel integrated graphics or CPU-only). GPU mode is available for Docker and Kubernetes when NVIDIA hardware is present.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start (Already Installed)](#quick-start-already-installed)
3. [Full Installation From Scratch](#full-installation-from-scratch)
4. [Folder Structure](#folder-structure)
5. [Download Models](#download-models)
6. [Run ComfyUI](#run-comfyui)
7. [Run with Docker (Windows & Linux)](#run-with-docker-windows--linux)
8. [Run with Kubernetes (Auto-scaling)](#run-with-kubernetes-auto-scaling)
9. [Generate Images](#generate-images)
10. [Face Swap Workflow](#face-swap-workflow)
11. [Undersea Photo Workflow](#undersea-photo-workflow)
12. [Install Video Nodes](#install-video-nodes)
13. [Generate Small Videos](#generate-small-videos)
14. [Copy Motion to AI Character](#copy-motion-to-ai-character)
15. [Animal Story 1-Minute Video](#animal-story-1-minute-video)
16. [Lion Play With Girl Video Workflow](#lion-play-with-girl-video-workflow)
17. [Recommended Settings](#recommended-settings)
18. [Install More Models & Nodes](#install-more-models--nodes)
19. [Troubleshooting](#troubleshooting)
20. [Quick Reference](#quick-reference)

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

### Choose your deployment method

| Method | Script | Best for |
|--------|--------|----------|
| **Local Python** | `run_comfyui.bat` | Windows laptop, development |
| **Docker** | `run_docker.bat` / `run_docker.sh` | Same setup on Windows & Linux |
| **Kubernetes** | `deploy_k8s.bat` / `deploy_k8s.sh` | Production, auto-scaling, high availability |

---

## Quick Start (Already Installed)

If this folder is already set up, follow these steps:

### Step 1 — Download models (first time only)

Double-click:

```
download_models.bat
```

Wait until you see **"All starter models ready"** (~5 GB download, 10–30 minutes depending on internet speed).

### Step 2 — Install video nodes (first time only, for video workflows)

Double-click:

```
install_video_nodes.bat
```

### Step 3 — Install face swap nodes (first time only, for face swap)

Double-click:

```
install_faceswap_nodes.bat
```

Then run (downloads CodeFormer + GFPGAN):

```
download_faceswap_models.bat
```

### Step 4 — Start ComfyUI

Double-click:

```
run_comfyui.bat
```

### Step 5 — Open in browser

Go to:

```
http://127.0.0.1:8188
```

> **Docker:** See [Run with Docker](#run-with-docker-windows--linux) — `docker compose up -d --build`  
> **Kubernetes:** See [Run with Kubernetes](#run-with-kubernetes-auto-scaling) — `deploy_k8s.bat`

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
├── run_comfyui.bat              # Start ComfyUI locally (CPU)
├── run_docker.bat / .sh         # Start ComfyUI in Docker
├── deploy_k8s.bat / .sh         # Deploy to Kubernetes
├── download_models.bat          # Download SD 1.5, VAE, AnimateDiff, BiRefNet
├── download_faceswap_models.bat # Download CodeFormer, GFPGAN, inswapper
├── install_video_nodes.bat      # Install AnimateDiff + video nodes
├── install_faceswap_nodes.bat   # Install ReActor face swap
├── docker-compose.yml           # Docker CPU config
├── docker-compose.gpu.yml       # Docker GPU overlay
├── Dockerfile                   # Container image
├── k8s/                         # Kubernetes manifests (HPA, ingress, PVC)
├── README2.md                   # This guide
├── main.py                      # ComfyUI entry point
├── venv/                        # Python virtual environment
├── models/
│   ├── checkpoints/             # Main image models (.safetensors)
│   ├── vae/                     # VAE models
│   ├── animatediff_models/      # AnimateDiff motion models
│   ├── background_removal/      # BiRefNet (NOT checkpoints/)
│   ├── insightface/             # inswapper_128.onnx, buffalo_l
│   └── facerestore_models/      # CodeFormer, GFPGAN
├── input/                       # Put input images here
│   ├── p.jpg                    # Face swap source face
│   ├── replaceFace.jpg          # Face swap target image
│   └── PR.jpg                   # Undersea workflow input
├── output/                      # Generated images and videos
├── custom_nodes/
│   ├── ComfyUI-Manager/
│   ├── ComfyUI-AnimateDiff-Evolved/
│   ├── ComfyUI-VideoHelperSuite/
│   ├── ComfyUI-KJNodes/
│   └── ComfyUI-ReActor/         # Face swap
└── user/default/workflows/
    ├── face_swap_replace.json   # Full human (p.jpg → replaceFace.jpg)
    ├── replaceface.json         # Same as face_swap_replace.json
    ├── undersea_surrender_pr.json  # Undersea background composite
    ├── motion_copy_video_to_character.json  # Video motion → p.jpg character
    ├── animal_story_1min.json      # 10 segments → stitched 60 sec MP4
├── build_animal_story_workflow.py  # Regenerate animal story workflow
    └── video_lion_play_girl.json   # Lion video workflow
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
| BiRefNet | `birefnet.safetensors` | ~420 MB | Background removal (undersea workflow) |

**Face swap models** (run `download_faceswap_models.bat`):

| Model | Path | Purpose |
|-------|------|---------|
| Inswapper | `models\insightface\inswapper_128.onnx` | Face swap engine |
| CodeFormer | `models\facerestore_models\codeformer-v0.1.0.pth` | Face restoration |
| GFPGAN | `models\facerestore_models\GFPGANv1.4.pth` | Face enhancement |
| Buffalo_l | `models\insightface\models\buffalo_l\` | Auto-downloaded on first ReActor run (~275 MB) |

### Manual download

Place files in these folders:

- Checkpoints → `models\checkpoints\`
- VAE → `models\vae\`
- AnimateDiff → `models\animatediff_models\`
- Background removal → `models\background_removal\` (**not** checkpoints)
- Face swap → `models\insightface\` and `models\facerestore_models\`

Download links:

- SD 1.5: https://huggingface.co/runwayml/stable-diffusion-v1-5
- VAE: https://huggingface.co/stabilityai/sd-vae-ft-mse
- AnimateDiff: https://huggingface.co/guoyww/animatediff
- BiRefNet: https://huggingface.co/Comfy-Org/BiRefNet/resolve/main/background_removal/birefnet.safetensors

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

### CPU mode (no GPU) — default

Use this on laptops/PCs **without an NVIDIA GPU** (Intel integrated graphics, AMD, or CPU-only).

**Do not** use `docker-compose.gpu.yml` for CPU mode.

| OS | Command |
|----|---------|
| Windows | Double-click `run_docker.bat` |
| Linux | `./run_docker.sh` |
| Manual (Windows & Linux) | `docker compose up -d --build` |

This uses `docker-compose.yml` only, builds CPU PyTorch, and runs ComfyUI with `--cpu --cpu-vae`.

### GPU mode (optional, NVIDIA only)

Use this only if the machine has an **NVIDIA GPU** and the **NVIDIA Container Toolkit** is installed.

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build
```

### CPU vs GPU — quick reference

| Mode | When to use | Start command |
|------|-------------|---------------|
| **CPU (no GPU)** | Intel/AMD integrated GPU, no CUDA, most laptops | `docker compose up -d --build` |
| **GPU (NVIDIA)** | NVIDIA GPU + Container Toolkit installed | `docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build` |

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

### Docker vs local Python

| Method | Best for |
|--------|----------|
| `run_comfyui.bat` | Windows laptop without Docker |
| `run_docker.bat` / `run_docker.sh` | Same setup on Windows and Linux servers |
| `deploy_k8s.bat` / `deploy_k8s.sh` | Production cluster with auto-scaling |

---

## Run with Kubernetes (Auto-scaling)

Deploy ComfyUI on Kubernetes for **auto-scaling**, **high availability**, and **better response** under load.

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Kubernetes cluster** | EKS, AKS, GKE, or local (minikube, kind, Docker Desktop K8s) |
| **kubectl** | Connected to your cluster |
| **Docker** | To build the ComfyUI image |
| **Storage class** | With `ReadWriteMany` support (NFS, EFS, Azure Files) for shared models |
| **NVIDIA GPU nodes** (optional) | For high-speed inference — required for real performance gains |

### Quick deploy

**CPU mode:**
```bash
deploy_k8s.bat          # Windows
./deploy_k8s.sh cpu     # Linux
```

**GPU mode (high speed):**
```bash
deploy_k8s.bat gpu
./deploy_k8s.sh gpu
```

**Or apply manifests manually:**
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml      # CPU
# kubectl apply -f k8s/deployment-gpu.yaml  # GPU
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/pdb.yaml
kubectl apply -f k8s/ingress.yaml
```

### First time — download models into cluster storage

```bash
kubectl apply -f k8s/job-download-models.yaml
kubectl logs -f job/comfyui-download-models -n comfyui
```

### Access ComfyUI

```bash
kubectl port-forward svc/comfyui 8188:8188 -n comfyui
```

Open: **http://127.0.0.1:8188**

Or use the LoadBalancer service:
```bash
kubectl get svc comfyui-lb -n comfyui
```

### Auto-scaling (HPA)

The Horizontal Pod Autoscaler scales pods based on CPU and memory:

| Setting | Value |
|---------|-------|
| Min replicas | 1 |
| Max replicas | 5 |
| Scale up when | CPU > 70% or Memory > 75% |
| Scale down delay | 5 minutes (avoids flapping) |

Check autoscaler status:
```bash
kubectl get hpa -n comfyui
kubectl describe hpa comfyui -n comfyui
```

### Kubernetes files

| File | Purpose |
|------|---------|
| `k8s/namespace.yaml` | `comfyui` namespace |
| `k8s/deployment.yaml` | CPU deployment (2–4 CPU, 4–8 GB RAM) |
| `k8s/deployment-gpu.yaml` | GPU deployment (NVIDIA, 8–16 GB RAM) |
| `k8s/hpa.yaml` | Auto-scaling 1–5 pods |
| `k8s/service.yaml` | ClusterIP + LoadBalancer |
| `k8s/ingress.yaml` | NGINX ingress with long timeouts |
| `k8s/pvc.yaml` | Persistent storage for models + data |
| `k8s/pdb.yaml` | Keeps at least 1 pod during updates |
| `k8s/job-download-models.yaml` | One-time model download job |

### Performance tips

| Goal | Action |
|------|--------|
| **High speed** | Use `deployment-gpu.yaml` on NVIDIA GPU nodes |
| **More concurrent users** | HPA scales to 5 pods automatically |
| **Faster cold start** | Pre-download models via Job; use shared PVC |
| **Production registry** | Set `COMFYUI_REGISTRY=your-registry.azurecr.io` before deploy |
| **Long workflows** | Ingress timeouts set to 3600s for image/video generation |

### Push image to a registry (production)

```bash
docker build -t your-registry.azurecr.io/comfyui:v1 .
docker push your-registry.azurecr.io/comfyui:v1
# Edit k8s/deployment.yaml image: field to your-registry.azurecr.io/comfyui:v1
```

### Useful commands

| Action | Command |
|--------|---------|
| Status | `kubectl get pods,hpa,svc -n comfyui` |
| Logs | `kubectl logs -f deployment/comfyui -n comfyui` |
| Scale manually | `kubectl scale deployment comfyui --replicas=3 -n comfyui` |
| Restart | `kubectl rollout restart deployment/comfyui -n comfyui` |
| Delete all | `kubectl delete namespace comfyui` |

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

## Face Swap Workflow

Place the **full human** from `p.jpg` onto the scene in `replaceFace.jpg` (entire body/person — not face-only).

### Install (first time only)

```
download_models.bat
```

This downloads BiRefNet for background removal (`models\background_removal\birefnet.safetensors`).

### Workflow file

Use **one of these** (both are the same full-human composite workflow):

```
user\default\workflows\face_swap_replace.json
user\default\workflows\replaceface.json
```

> **Important:** Do **not** use `undersea_surrender_pr.json` or other image-generation workflows here. Those regenerate the whole image.

| Role | File | What happens |
|------|------|--------------|
| **SOURCE HUMAN** | `input\p.jpg` | Full person cut out and placed on target |
| **TARGET SCENE** | `input\replaceFace.jpg` | Background/scene kept |

**Result:** `replaceFace.jpg` scene with the **full human from `p.jpg`** composited on top.

### How it works

| Step | Node | Purpose |
|------|------|---------|
| 1 | Scale target | `replaceFace.jpg` → 768×512 |
| 2 | Detect + erase old person | BiRefNet mask + blur-fill removes target person |
| 3 | Scale source | `p.jpg` human resized (height 512) |
| 4 | Remove Background | Cuts out **full human** from `p.jpg` |
| 5 | Image Composite | Places `p.jpg` human onto cleaned scene (one person only) |

### Position tuning

In **Image Composite Masked** node:

| Setting | Default | Adjust if... |
|---------|---------|--------------|
| `x` | 280 | Move human left/right |
| `y` | 0 | Move human up/down |
| Source height | 512 | Match target height; lower if person too large |
| Target Grow Mask | 35 | Increase if old person still visible |

### Run

1. Restart ComfyUI
2. Load `face_swap_replace.json` or `replaceface.json`
3. **Verify** Load Image nodes:
   - **SOURCE HUMAN** = `p.jpg`
   - **TARGET** = `replaceFace.jpg`
4. Click **Queue Prompt**
5. Output: `output\human_replace_p_to_replaceface_*.png`

### Prerequisites

- BiRefNet model at `models\background_removal\birefnet.safetensors` (run `download_models.bat`)

---

## Undersea Photo Workflow

Place a person from a photo underwater with sea animals, keeping the **same person** from the input image.

### Workflow file

```
user\default\workflows\undersea_surrender_pr.json
```

| Input | File | Role |
|-------|------|------|
| Photo | `input\PR.jpg` | Person to place underwater |

### How it works

1. Removes background from `PR.jpg` (BiRefNet)
2. Generates underwater scene with sea animals
3. Composites the **original person** onto the underwater background

### Prerequisites

- `download_models.bat` (includes BiRefNet in `models\background_removal\`)
- **Not** checkpoints — BiRefNet must be in `models\background_removal\birefnet.safetensors`

### Run

1. Load `undersea_surrender_pr.json`
2. Click **Queue Prompt**
3. Output: `output\undersea_surrender_pr_*.png`

> Do **not** use this workflow for human replace. Use `face_swap_replace.json` instead.

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

## Copy Motion to AI Character

Copy **motion from a video** onto an **AI character** from a reference photo.

| Role | File | Purpose |
|------|------|---------|
| **Motion source** | `input\Sadi Gali.mp4` | Dance/movement copied frame-by-frame |
| **AI character** | `input\p.jpg` | Face/identity applied to every frame |

### Workflow file

```
user\default\workflows\motion_copy_video_to_character.json
```

### Prerequisites

1. Run `install_video_nodes.bat` (VideoHelperSuite)
2. Run `install_faceswap_nodes.bat` (ReActor)
3. Run `download_faceswap_models.bat` (CodeFormer, inswapper)
4. Place `Sadi Gali.mp4` in `input\` folder
5. Restart ComfyUI

### How it works

| Step | Node | Purpose |
|------|------|---------|
| 1 | Load Video | Reads `Sadi Gali.mp4` frames + audio |
| 2 | Load Image | Loads `p.jpg` as AI character reference |
| 3 | ReActor Face Boost | HQ face restoration |
| 4 | ReActor Face Swap | Applies `p.jpg` face to each video frame (motion preserved) |
| 5 | Video Combine | Exports MP4 with original audio |

### Run

1. Load `motion_copy_video_to_character.json`
2. Verify:
   - **MOTION SOURCE** = `Sadi Gali.mp4`
   - **AI CHARACTER** = `p.jpg`
3. Click **Queue Prompt**
4. Output: `output\motion_copy_p_sadi_gali_*.mp4`

### CPU-friendly defaults (16 GB RAM)

| Setting | Value | Notes |
|---------|-------|-------|
| `force_rate` | 12 fps | Lower = faster (try 8) |
| `frame_load_cap` | 48 | ~4 seconds; raise for longer clip |
| `select_every_nth` | 2 | Skips every other frame |
| Resolution | 384×512 | Portrait video crop |

> **Note:** On CPU, 48 frames can take **30–90+ minutes**. Start with `frame_load_cap` = 24 for a quick test.

### Tune quality

| If result is... | Change this |
|-----------------|-------------|
| Face does not look like `p.jpg` | Raise `codeformer_weight` to `0.75` |
| Face looks blurry | Raise `face_restore_visibility` to `0.95` |
| Wrong person in video | Change `input_faces_index` to `1` |
| Too slow on CPU | Lower `frame_load_cap` to 24, `force_rate` to 8 |
| Need longer clip | Raise `frame_load_cap` (slower) |

---

## Animal Story 1-Minute Video

A **10-scene animal storytelling** video — **one Queue Prompt** generates all segments and **auto-stitches** into one **60-second MP4**.

### Workflow file

```
user\default\workflows\animal_story_1min.json
```

Regenerate after editing chapters:

```
python build_animal_story_workflow.py
```

### How it works (10 segments → 1 perfect MP4)

| Step | What happens |
|------|----------------|
| 1–10 | Each **segment** generates **48 frames** (6 sec) with its own chapter prompt + KSampler |
| Stitch | **9× Merge Images** nodes concatenate all segments → **480 frames** |
| Export | **Video Combine** → `animal_story_1min_final_*.mp4` @ **8 fps = 60 seconds** |

No manual stitching. No running 10 times. **One workflow, one output.**

### Story scenes

| Scene | Animals / moment |
|-------|------------------|
| 1 | Lion + Elephant at dawn watering hole |
| 2 | Lion + Zebra under acacia tree |
| 3 | Monkey joins playfully |
| 4 | Parrot arrives |
| 5 | Giraffe bends down to group |
| 6 | Owl shares wisdom |
| 7 | Turtle arrives slowly |
| 8 | Fox storyteller |
| 9 | All animals gather in circle |
| 10 | Sunset finale — everyone together |

### Run

1. Run `install_video_nodes.bat` and `download_models.bat`
2. Load `animal_story_1min.json`
3. Click **Queue Prompt** once
4. Output: `output\animal_story_1min_final_*.mp4` (**60 seconds**)

### Progress on CPU

Watch **KSampler 1/10** through **KSampler 10/10** in the workflow — each segment completes before the next starts.

| Phase | Approx. time (CPU) |
|-------|---------------------|
| KSampler × 10 (48 frames, 12 steps each) | **5–15+ hours total** |
| Merge + VAE Decode + MP4 | 10–30 min |

### Quality settings (built-in)

| Setting | Value |
|---------|-------|
| Resolution | 512×512 |
| Frames per segment | 48 |
| Total frames | 480 |
| Steps | 12 |
| CFG | 7.5 |
| CRF (video) | 18 (high quality) |
| Style | Shared prefix/suffix on all chapters for consistent look |

### Quick test (before full 1-minute run)

Double-click:

```
build_animal_story_quick_test.bat
```

Or:

```
python build_animal_story_workflow.py --quick
```

Then reload `animal_story_1min.json` in ComfyUI → **Queue Prompt**.

| Quick test | Value |
|------------|-------|
| Segments | 2 |
| Frames | 96 total |
| Duration | ~12 sec @ 8 fps |
| Steps | 8 (faster on CPU) |
| Output | `output\animal_story_quick_test_*.mp4` |

For full 60-second video:

```
build_animal_story_full.bat
```

Or `python build_animal_story_workflow.py --full`

Optional — queue from terminal (ComfyUI must be running):

```
python queue_animal_story.py
```

### Edit the story

1. Edit chapter text in `build_animal_story_workflow.py` (`CHAPTERS` list)
2. Run `python build_animal_story_workflow.py`
3. Reload workflow in ComfyUI

Or edit each **Chapter N prompt** node directly in ComfyUI.

### KSampler not starting

If an old version used **480 frames + Prompt Scheduling lerp**, cancel the job and **reload** the latest `animal_story_1min.json`. The new version uses **10 separate KSamplers** (no slow prompt scheduling).

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
| ComfyUI-ReActor | Face swap (already installed) |

### Model folders

| Type | Folder |
|------|--------|
| Checkpoints | `models\checkpoints\` |
| VAE | `models\vae\` |
| AnimateDiff | `models\animatediff_models\` |
| Background removal | `models\background_removal\` |
| Face swap (insightface) | `models\insightface\` |
| Face restore | `models\facerestore_models\` |
| LoRA | `models\loras\` |
| ControlNet | `models\controlnet\` |
| Upscale | `models\upscale_models\` |

---

## Troubleshooting

### Missing model `birefnet.safetensors`

ComfyUI looks for BiRefNet in **`models\background_removal\`**, not in `models\checkpoints\`.

**Correct path:**

```
models\background_removal\birefnet.safetensors
```

**Wrong path (will show "missing model"):**

```
models\checkpoints\birefnet.safetensors
```

Move the file to the correct folder, then restart ComfyUI and reload the workflow.

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

### Face / human replace — both people visible or wrong position

1. **Check roles:** SOURCE = `p.jpg`, TARGET = `replaceFace.jpg`
2. BiRefNet must be in `models\background_removal\` (not checkpoints)
3. Increase **Grow Mask** on target (35 → 50) to fully erase old person
4. Increase **Blur Image** radius (25 → 35) if erase area looks patchy
5. Adjust **STEP 2 Image Composite** `x` / `y` to position `p.jpg` human
6. Change source **height** in Scale node if person too big/small

### Kubernetes pod not starting

```bash
kubectl describe pod -l app.kubernetes.io/name=comfyui -n comfyui
kubectl logs deployment/comfyui -n comfyui
```

Common fixes:
- PVC needs `ReadWriteMany` storage class
- Image not found — build with `docker build -t comfyui-local:cpu .`
- GPU pods need NVIDIA device plugin + `accelerator: nvidia` node label

---

## Quick Reference

### Local (Windows)

| Action | Command / File |
|--------|----------------|
| Download models | `download_models.bat` |
| Download face swap models | `download_faceswap_models.bat` |
| Install video nodes | `install_video_nodes.bat` |
| Install face swap | `install_faceswap_nodes.bat` |
| Start ComfyUI | `run_comfyui.bat` |
| Open UI | http://127.0.0.1:8188 |
| Stop server | `Ctrl + C` in terminal |

### Workflows

| Workflow | File | Purpose |
|----------|------|---------|
| Face / human replace | `user\default\workflows\face_swap_replace.json` | Full `p.jpg` human → `replaceFace.jpg` |
| Undersea photo | `user\default\workflows\undersea_surrender_pr.json` | `PR.jpg` underwater composite |
| Motion copy | `user\default\workflows\motion_copy_video_to_character.json` | `Sadi Gali.mp4` motion → `p.jpg` character |
| Animal story | `user\default\workflows\animal_story_1min.json` | 10 scenes auto-stitched → 60 sec MP4 |
| Lion video | `user\default\workflows\video_lion_play_girl.json` | Short animated video |

### Docker

| Action | Command |
|--------|---------|
| Start (CPU) | `run_docker.bat` or `docker compose up -d --build` |
| Start (GPU) | `docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build` |
| Download models | `download_models_docker.bat` |
| Stop | `docker compose down` |
| Logs | `docker compose logs -f comfyui` |

### Kubernetes

| Action | Command |
|--------|---------|
| Deploy (CPU) | `deploy_k8s.bat` |
| Deploy (GPU) | `deploy_k8s.bat gpu` |
| Download models | `kubectl apply -f k8s/job-download-models.yaml` |
| Port forward | `kubectl port-forward svc/comfyui 8188:8188 -n comfyui` |
| Check scaling | `kubectl get hpa -n comfyui` |
| Delete | `kubectl delete namespace comfyui` |

### Folders

| Folder | Purpose |
|--------|---------|
| `output\` | Generated images and videos |
| `input\` | Input images (`p.jpg`, `replaceFace.jpg`, `PR.jpg`) |
| `models\` | AI model weights |
| `user\default\workflows\` | Saved workflow JSON files |

---

## Support & Links

- ComfyUI official repo: https://github.com/comfyanonymous/ComfyUI
- ComfyUI Manager: https://github.com/ltdrdata/ComfyUI-Manager
- Video Helper Suite: https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
- AnimateDiff Evolved: https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
- ReActor (face swap): https://github.com/Gourieff/ComfyUI-ReActor
- SD 1.5 model: https://huggingface.co/runwayml/stable-diffusion-v1-5
- AnimateDiff motion model: https://huggingface.co/guoyww/animatediff
- BiRefNet: https://huggingface.co/Comfy-Org/BiRefNet
- ReActor models: https://huggingface.co/datasets/Gourieff/ReActor

---

*Last updated: June 2026 — Local Python, Docker, Kubernetes. CPU mode for Intel i5 / 16 GB RAM. GPU optional for Docker/K8s.*
