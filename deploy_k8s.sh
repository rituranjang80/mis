#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

MODE="${1:-cpu}"
REGISTRY="${COMFYUI_REGISTRY:-}"
TAG="${COMFYUI_TAG:-latest}"

echo "============================================"
echo " ComfyUI Kubernetes Deploy ($MODE)"
echo "============================================"

if ! command -v kubectl &>/dev/null; then
  echo "ERROR: kubectl not found. Install kubectl first."
  exit 1
fi

echo "[1/4] Building Docker image..."
if [ "$MODE" = "gpu" ]; then
  docker build --build-arg TORCH_VARIANT=cuda -t comfyui-local:gpu .
  IMAGE="comfyui-local:gpu"
else
  docker build --build-arg TORCH_VARIANT=cpu -t comfyui-local:cpu .
  IMAGE="comfyui-local:cpu"
fi

if [ -n "$REGISTRY" ]; then
  REMOTE="${REGISTRY}/comfyui:${TAG}"
  echo "[2/4] Pushing to registry: $REMOTE"
  docker tag "$IMAGE" "$REMOTE"
  docker push "$REMOTE"
  kubectl set image deployment/comfyui comfyui="$REMOTE" -n comfyui --record 2>/dev/null || true
else
  echo "[2/4] Using local image (set COMFYUI_REGISTRY to push to a cluster registry)"
fi

echo "[3/4] Applying Kubernetes manifests..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml

if [ "$MODE" = "gpu" ]; then
  kubectl apply -f k8s/deployment-gpu.yaml
else
  kubectl apply -f k8s/deployment.yaml
fi

kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/pdb.yaml
kubectl apply -f k8s/ingress.yaml

echo "[4/4] Waiting for rollout..."
kubectl rollout status deployment/comfyui -n comfyui --timeout=300s

echo
echo "Deployed! Useful commands:"
echo "  kubectl get pods -n comfyui"
echo "  kubectl get hpa -n comfyui"
echo "  kubectl port-forward svc/comfyui 8188:8188 -n comfyui"
echo
echo "Download models (first time):"
echo "  kubectl apply -f k8s/job-download-models.yaml"
echo "  kubectl logs -f job/comfyui-download-models -n comfyui"
