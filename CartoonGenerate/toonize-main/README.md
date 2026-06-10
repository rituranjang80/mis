# Toonize

Turn images and videos into cartoons. Optionally replace video audio with an auto-generated human voice (OpenVoice).

Includes a **REST API with Swagger UI**, **Docker** images (CPU + GPU), and **Kubernetes** manifests for high-performance deployment on any system.

## Requirements

| Requirement | Version / notes |
|-------------|-----------------|
| Python | 3.9 – 3.10 (recommended) |
| ffmpeg | Must be on `PATH` |
| GPU (optional) | NVIDIA + CUDA 12.1 for faster voice step |
| Disk space | ~2 GB for models (cartoon + OpenVoice) |

---

## Quick start (CLI)

**Do not** run `pip install -r requirements.txt` directly — it causes long pip backtracking. Use the staged installer instead.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
python install.py
python setup_models.py
python setup_voice.py

$env:PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"
python toonize.py c.mp4
```

GPU voice (optional):

```powershell
python install.py --gpu
```

Or use the PowerShell installer: `.\install.ps1` / `.\install.ps1 -Gpu`

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python install.py
python setup_models.py
python setup_voice.py

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
python toonize.py c.mp4
```

### CLI examples

```bash
python toonize.py c.mp4
python toonize.py "*.jpg"
python toonize.py c.mp4 --config my_voice.yaml
python toonize.py c.mp4 --no-voice
```

Output files are saved next to inputs with `_toon` suffix (e.g. `c_toon.mp4`).

---

## REST API & Swagger

The API wraps cartoonization in an async job queue — suitable for Docker and Kubernetes.

### Run locally

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | **Swagger UI** (interactive API docs) |
| http://localhost:8000/redoc | ReDoc API reference |
| http://localhost:8000/openapi.json | OpenAPI 3 schema |
| http://localhost:8000/health | Liveness probe |
| http://localhost:8000/ready | Readiness probe |

### API workflow

1. **Upload** — `POST /api/v1/toonize` with multipart file
2. **Poll** — `GET /api/v1/jobs/{job_id}` until `status` is `completed`
3. **Download** — `GET /api/v1/jobs/{job_id}/download`

### Example (curl)

```bash
# Upload
curl -X POST "http://localhost:8000/api/v1/toonize" \
  -F "file=@photo.jpg" \
  -F "no_voice=true"

# Response: {"job_id":"...","status":"queued","message":"..."}

# Check status
curl "http://localhost:8000/api/v1/jobs/<job_id>"

# Download result
curl -OJ "http://localhost:8000/api/v1/jobs/<job_id>/download"
```

### Performance tuning (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| `TOONIZE_MAX_WORKERS` | `2` | Concurrent processing threads per pod |
| `TOONIZE_API_WORKERS` | `1` | Uvicorn worker processes (keep at 1 — models are heavy) |
| `TOONIZE_LIMIT_CONCURRENCY` | `10` | Max in-flight HTTP requests |
| `TOONIZE_DATA_DIR` | `./data` | Job uploads/outputs directory |
| `TOONIZE_CORS_ORIGINS` | `*` | Comma-separated CORS origins |

---

## Docker

Pre-built images bundle TensorFlow, PyTorch, OpenVoice, ffmpeg, and model weights.

### CPU (recommended for most users)

```bash
docker build -t toonize-api:cpu -f Dockerfile .
docker run -d --name toonize -p 8000:8000 -v toonize-data:/data toonize-api:cpu
```

Or with Docker Compose:

```bash
docker compose up -d --build
```

Open Swagger: http://localhost:8000/docs

### GPU (NVIDIA CUDA 12.1)

Requires [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

```bash
docker build -t toonize-api:gpu -f Dockerfile.gpu .
docker compose -f docker-compose.gpu.yml up -d --build
```

### Docker resource recommendations

| Variant | CPU | RAM | GPU |
|---------|-----|-----|-----|
| CPU | 2–4 cores | 4–8 GB | — |
| GPU | 4–8 cores | 8–16 GB | 1× NVIDIA (CUDA 12.1) |

---

## Kubernetes

Manifests are in `k8s/` for production deployment with autoscaling.

### Prerequisites — start a local cluster first

`kubectl apply` needs a **running** Kubernetes API. If you see `connection refused` on `127.0.0.1`, no cluster is up.

**Option A — Docker Desktop (easiest on Windows)**

1. Docker Desktop → **Settings** → **Kubernetes** → enable **Enable Kubernetes** → Apply
2. Wait until Kubernetes shows **Running** (green)
3. Switch context:
   ```powershell
   kubectl config use-context docker-desktop
   kubectl cluster-info
   ```

**Option B — Minikube**

```powershell
kubectl config use-context minikube
minikube start --driver=docker
kubectl cluster-info
```

### Deploy (CPU)

```bash
# Build and load image (local cluster example)
docker build -t toonize-api:cpu -f Dockerfile .

# Load image into minikube (skip if using Docker Desktop — it shares the local daemon)
minikube image load toonize-api:cpu

# Apply all resources
kubectl apply -k k8s/

# Check status
kubectl -n toonize get pods,svc,hpa
```

### What gets deployed

| Resource | Purpose |
|----------|---------|
| `namespace.yaml` | `toonize` namespace |
| `configmap.yaml` | Runtime environment variables |
| `pvc.yaml` | Optional shared storage (apply manually if needed) |
| `deployment.yaml` | 2-replica API deployment with probes |
| `service.yaml` | ClusterIP service on port 80 |
| `hpa.yaml` | Auto-scale 2–10 pods (CPU 70%, memory 80%) |
| `ingress.yaml` | NGINX ingress with 500 MB upload limit |

### GPU deployment (optional)

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment-gpu.yaml
kubectl apply -f k8s/service.yaml
```

Label GPU nodes: `accelerator=nvidia-gpu`

### Port-forward for local testing

```bash
kubectl -n toonize port-forward svc/toonize-api 8000:80
```

Then open http://localhost:8000/docs

### Push to a registry

```bash
docker tag toonize-api:cpu your-registry/toonize-api:cpu
docker push your-registry/toonize-api:cpu
# Update image in k8s/deployment.yaml before applying
```

---

## Voice configuration

| File | Purpose |
|------|---------|
| `voice_config.yaml` | Default settings |
| `my_voice.yaml` | Custom profile for `--config` |

| Setting | Values |
|---------|--------|
| `enabled` | `true` / `false` |
| `mode` | `auto` (built-in speakers) or `file` (reference WAV) |
| `language` | `EN` or `ZH` |
| `speaker_style` | `friendly`, `cheerful`, `excited`, `sad`, `angry`, etc. |

Environment override: `TOONIZE_VOICE_CONFIG=/path/to/voice.yaml`

---

## Model setup

| Script | Downloads |
|--------|-----------|
| `python setup_models.py` | Cartoon TF weights → `white_box_cartoonizer/saved_models/` |
| `python setup_voice.py` | OpenVoice checkpoints (~500 MB) → `checkpoints/` |

Both run automatically during Docker image build. For manual setup, run them after `install.py`.

---

## Project layout

```
toonize-main/
├── api/                  # FastAPI + Swagger REST API
│   ├── main.py
│   ├── jobs.py
│   └── schemas.py
├── k8s/                  # Kubernetes manifests
├── docker/               # Container entrypoint
├── white_box_cartoonizer/  # Cartoon model
├── toonize.py            # CLI entry point
├── install.py            # Staged dependency installer
├── setup_models.py       # Cartoon weight downloader
├── setup_voice.py        # OpenVoice checkpoint downloader
├── Dockerfile            # CPU production image
├── Dockerfile.gpu        # GPU production image
└── docker-compose.yml
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `librosa` conflict | Use `python install.py` (pins `librosa==0.9.1`) |
| Pip stuck / backtracking | Stop (Ctrl+C), run `python install.py` |
| `checkpoints are missing` | `python setup_voice.py` |
| OpenVoice download 404 / AccessDenied | `setup_voice.py` uses HuggingFace mirror automatically; re-run `python setup_voice.py` |
| `Cartoon model weights missing` | `python setup_models.py` |
| `Python packages are missing` | `python install.py` |
| `Voice config not found` | Create `my_voice.yaml` or fix `--config` path |
| `kubectl apply` connection refused | Start a cluster first (Docker Desktop K8s or `minikube start`) |
| K8s pod not ready | Check `kubectl -n toonize logs deploy/toonize-api` and `/ready` endpoint |
| `ImagePullBackOff` on minikube | Run `minikube image load toonize-api:cpu` after `docker build` |
| Docker OOM | Increase memory limit; reduce `TOONIZE_MAX_WORKERS` |

### Why install was slow

The old `requirements.txt` pinned every transitive package plus both `tensorflow` and `tensorflow-intel`. Pip spent 30+ minutes backtracking.

**Fix:** `install.py` installs in **8 small steps** (numpy → tensorflow → cartoon → torch → voice → openvoice → API). Each step finishes in 1–3 minutes.

---

## Performance notes

- **Cartoonization** runs on CPU (TensorFlow). Image resize is capped at 1080px.
- **Voice transformation** auto-detects GPU (`cuda:0`) when available.
- For Kubernetes, keep `TOONIZE_API_WORKERS=1` — each worker loads full ML models (~2 GB RAM).
- Use HPA for horizontal scaling under load; each pod handles 2 concurrent jobs by default.
- Video processing is frame-by-frame; longer videos take proportionally longer.

---

## License

CC BY-NC-SA 4.0 — see [LICENSE](LICENSE). Non-commercial use with attribution.
