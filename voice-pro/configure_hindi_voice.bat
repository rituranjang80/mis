@echo off
cd /D "%~dp0"
echo Adding Hindi voice cloning (all other languages remain available)...
echo.

if not exist "installer_files\env\python.exe" (
    echo Run configure.bat and start.bat first to install the environment.
    pause
    exit /b 1
)

set PYTHONNOUSERSITE=1
call "installer_files\conda\condabin\conda.bat" activate "installer_files\env" >nul 2>&1

echo [1/2] Setting F5 Hindi preference in app\config-user.json5 ...
python configure_hindi_voice.py

echo [2/2] Pre-downloading SPRINGLab/F5-Hindi model...
python -c "from cached_path import cached_path; cached_path('hf://SPRINGLab/F5-Hindi-24KHz/model_2500000.safetensors'); cached_path('hf://SPRINGLab/F5-Hindi-24KHz/vocab.txt'); print('F5-Hindi model ready.')"

echo.
echo Done. F5 languages in UI: English, Chinese, Japanese, Hindi, Finnish, French, Italian, Russian, Spanish.
echo Start: start.bat  -^>  Speech Generation -^> F5-TTS (Single)
pause
