@echo off
title ComfyUI - Install Video Generation Nodes
cd /d "%~dp0"

echo ============================================
echo  Installing video generation custom nodes
echo ============================================
echo.

call venv\Scripts\activate.bat

echo [1/4] Installing ComfyUI Manager package...
pip install -r manager_requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install comfyui-manager
    pause
    exit /b 1
)

echo.
echo [2/4] Installing AnimateDiff-Evolved...
if not exist "custom_nodes\ComfyUI-AnimateDiff-Evolved" (
    git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git custom_nodes\ComfyUI-AnimateDiff-Evolved
) else (
    echo Already installed: ComfyUI-AnimateDiff-Evolved
)

echo.
echo [3/4] Installing VideoHelperSuite...
if not exist "custom_nodes\ComfyUI-VideoHelperSuite" (
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git custom_nodes\ComfyUI-VideoHelperSuite
) else (
    echo Already installed: ComfyUI-VideoHelperSuite
)

echo.
echo [4/4] Installing node dependencies and motion model...
pip install -r custom_nodes\ComfyUI-VideoHelperSuite\requirements.txt
python download_models.py

echo.
echo ============================================
echo  Video nodes installed successfully!
echo  IMPORTANT: Restart ComfyUI now.
echo  Run: run_comfyui.bat
echo ============================================
pause
