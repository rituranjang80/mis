@echo off
title ComfyUI - AL01LAP142 (CPU Mode)
cd /d "%~dp0"

echo ============================================
echo  ComfyUI - Image and Video Generation
echo  Device: Intel i5-1135G7 / 16GB RAM / CPU
echo ============================================
echo.
echo Starting ComfyUI...
echo Open in browser: http://127.0.0.1:8188
echo Press Ctrl+C to stop.
echo.

call venv\Scripts\activate.bat

set TQDM_DISABLE=1
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

python main.py --cpu --cpu-vae --preview-method none --preview-size 256 --listen 127.0.0.1 --port 8188 --enable-manager

pause
