@echo off
title ComfyUI Docker (CPU)
cd /d "%~dp0"

echo ============================================
echo  ComfyUI Docker - CPU mode
echo  Works on Windows and Linux (Docker required)
echo ============================================
echo.

docker compose up -d --build
if errorlevel 1 (
    echo ERROR: Docker failed. Is Docker Desktop running?
    pause
    exit /b 1
)

echo.
echo ComfyUI is starting in Docker.
echo Open in browser: http://127.0.0.1:8188
echo.
echo Download models (first time only):
echo   docker compose --profile setup run --rm download-models
echo.
echo Stop: docker compose down
echo Logs: docker compose logs -f comfyui
echo.
pause
