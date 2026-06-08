@echo off
title ComfyUI - Download Models (Docker)
cd /d "%~dp0"

echo Downloading starter models into ./models ...
docker compose --profile setup run --rm download-models

echo.
echo Done. Start ComfyUI with run_docker.bat
pause
