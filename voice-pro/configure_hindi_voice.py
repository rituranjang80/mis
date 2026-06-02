"""Merge F5 Hindi voice-cloning prefs into config-user.json5 without removing other settings."""
import json5
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "app" / "config-user.json5"
HEADER = (
    "// Optional user overrides — merged with built-in defaults.\n"
    "// Hindi voice cloning only; all other languages stay in the UI.\n"
)

config = {}
if CONFIG_PATH.exists():
    try:
        config = json5.load(CONFIG_PATH.open(encoding="utf-8"))
    except Exception:
        config = {}

config["f5_single_language"] = "Hindi"
config["f5_model"] = "SPRINGLab/F5-Hindi"

CONFIG_PATH.write_text(HEADER + json5.dumps(config, indent=4) + "\n", encoding="utf-8")
print(f"Updated {CONFIG_PATH}")
