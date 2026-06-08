# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm

ARG TORCH_VARIANT=cpu

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TQDM_DISABLE=1 \
    COMFYUI_LISTEN=0.0.0.0 \
    COMFYUI_PORT=8188

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt manager_requirements.txt ./

RUN if [ "$TORCH_VARIANT" = "cpu" ]; then \
      pip install --no-cache-dir torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cpu; \
    else \
      pip install --no-cache-dir torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu124; \
    fi \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r manager_requirements.txt \
    && pip install --no-cache-dir huggingface_hub opencv-python imageio-ffmpeg

RUN mkdir -p custom_nodes \
    && git clone --depth 1 https://github.com/ltdrdata/ComfyUI-Manager.git custom_nodes/ComfyUI-Manager \
    && git clone --depth 1 https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git custom_nodes/ComfyUI-AnimateDiff-Evolved \
    && git clone --depth 1 https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git custom_nodes/ComfyUI-VideoHelperSuite

COPY . .

RUN sed -i 's/\r$//' docker/entrypoint.sh && chmod +x docker/entrypoint.sh

EXPOSE 8188

HEALTHCHECK --interval=30s --timeout=10s --start-period=180s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8188')" || exit 1

ENTRYPOINT ["/app/docker/entrypoint.sh"]
