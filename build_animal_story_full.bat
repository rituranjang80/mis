@echo off
title ComfyUI - Build Animal Story FULL 1-minute workflow
cd /d "%~dp0"
call venv\Scripts\activate.bat
python build_animal_story_workflow.py --full
echo.
echo Full workflow ready. Reload animal_story_1min.json in ComfyUI and Queue Prompt.
echo Output: output\animal_story_1min_final_*.mp4  (60 seconds)
pause
