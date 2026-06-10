@echo off
title ComfyUI - Install Face Swap (ReActor)
cd /d "%~dp0"

echo ============================================
echo  Installing ReActor face swap nodes
echo ============================================
echo.

call venv\Scripts\activate.bat

if not exist "custom_nodes\ComfyUI-ReActor" (
    echo [1/3] Cloning ComfyUI-ReActor...
    git clone --depth 1 https://github.com/Gourieff/ComfyUI-ReActor.git custom_nodes\ComfyUI-ReActor
) else (
    echo [1/3] ComfyUI-ReActor already installed
)

echo.
echo [2/3] Installing Python dependencies...
pip install -r custom_nodes\ComfyUI-ReActor\requirements.txt onnxruntime

echo.
echo [3/4] Downloading inswapper face swap model...
python custom_nodes\ComfyUI-ReActor\install.py

echo.
echo [4/4] Downloading CodeFormer face restoration (HQ)...
python download_faceswap_models.py

echo.
echo ============================================
echo  Face swap nodes installed!
echo  Restart ComfyUI, then load:
echo  user\default\workflows\face_swap_replace.json
echo ============================================
pause
