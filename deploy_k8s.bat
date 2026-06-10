@echo off
title ComfyUI - Kubernetes Deploy
cd /d "%~dp0"

set MODE=%1
if "%MODE%"=="" set MODE=cpu

echo ============================================
echo  ComfyUI Kubernetes Deploy (%MODE%)
echo ============================================
echo.

where kubectl >nul 2>&1
if errorlevel 1 (
    echo ERROR: kubectl not found. Install kubectl and connect to your cluster.
    pause
    exit /b 1
)

echo [1/4] Building Docker image...
if /i "%MODE%"=="gpu" (
    docker build --build-arg TORCH_VARIANT=cuda -t comfyui-local:gpu .
) else (
    docker build --build-arg TORCH_VARIANT=cpu -t comfyui-local:cpu .
)
if errorlevel 1 (
    echo ERROR: Docker build failed.
    pause
    exit /b 1
)

echo.
echo [2/4] Applying Kubernetes manifests...
kubectl apply -f k8s\namespace.yaml
kubectl apply -f k8s\configmap.yaml
kubectl apply -f k8s\pvc.yaml

if /i "%MODE%"=="gpu" (
    kubectl apply -f k8s\deployment-gpu.yaml
) else (
    kubectl apply -f k8s\deployment.yaml
)

kubectl apply -f k8s\service.yaml
kubectl apply -f k8s\hpa.yaml
kubectl apply -f k8s\pdb.yaml
kubectl apply -f k8s\ingress.yaml

echo.
echo [3/4] Waiting for rollout...
kubectl rollout status deployment/comfyui -n comfyui --timeout=300s

echo.
echo [4/4] Done!
echo.
echo Useful commands:
echo   kubectl get pods -n comfyui
echo   kubectl get hpa -n comfyui
echo   kubectl port-forward svc/comfyui 8188:8188 -n comfyui
echo.
echo Download models (first time):
echo   kubectl apply -f k8s\job-download-models.yaml
echo.
pause
