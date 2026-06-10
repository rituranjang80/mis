@echo off
title ComfyUI - Build Animal Story QUICK TEST workflow
cd /d "%~dp0"
call venv\Scripts\activate.bat
python build_animal_story_workflow.py --quick
echo.
echo Quick test workflow ready. Reload animal_story_1min.json in ComfyUI and Queue Prompt.
echo Output: output\animal_story_quick_test_*.mp4  (~12 seconds)
pause
