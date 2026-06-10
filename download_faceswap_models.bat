@echo off
title ComfyUI - Download Face Swap HQ Models
cd /d "%~dp0"
call venv\Scripts\activate.bat
python download_faceswap_models.py
pause
