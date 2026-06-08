@echo off
title ComfyUI - Download Starter Models
cd /d "%~dp0"

echo ============================================
echo  Downloading starter AI models
echo  This may take 10-30 minutes (~4 GB)
echo ============================================
echo.

call venv\Scripts\activate.bat
python download_models.py

echo.
echo Done. You can now run run_comfyui.bat
pause
