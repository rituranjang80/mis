"""Load and validate voice settings from YAML."""
import os
import random
from copy import deepcopy
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

_PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = _PROJECT_DIR / "voice_config.yaml"

_BUILTIN_SPEAKERS = (
    "default",
    "friendly",
    "cheerful",
    "excited",
    "sad",
    "angry",
    "terrified",
    "shouting",
    "whispering",
)

_DEFAULTS = {
    "voice": {
        "enabled": True,
        "mode": "auto",
        "reference_file": None,
        "language": "EN",
        "speaker_style": "friendly",
        "speed": 1.0,
        "reference_text": (
            "Hello. This is an automatically generated human voice sample."
        ),
        "speakers_pool": list(_BUILTIN_SPEAKERS),
        "random_seed": None,
        "sample_rate": 24000,
        "vad": True,
    }
}


def _deep_merge(base, override):
    out = deepcopy(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load_voice_config(config_path=None, config_required=False):
    explicit = config_path or os.environ.get("TOONIZE_VOICE_CONFIG")
    path = Path(explicit) if explicit else DEFAULT_CONFIG_PATH
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve()

    if config_required and not path.is_file():
        raise FileNotFoundError(
            "Voice config not found: {}\n"
            "Create it (e.g. copy voice_config.yaml to my_voice.yaml).".format(path)
        )

    data = deepcopy(_DEFAULTS)
    if path.is_file():
        if yaml is None:
            raise RuntimeError(
                "PyYAML is required to read {}. Run: python install.py".format(
                    path
                )
            )
        with open(path, "r", encoding="utf-8") as f:
            user = yaml.safe_load(f) or {}
        data = _deep_merge(data, user)
        print("Loaded voice config: {}".format(path))
    elif config_required:
        raise FileNotFoundError("Voice config not found: {}".format(path))

    return data["voice"]


def pick_speaker_style(voice_cfg):
    style = voice_cfg.get("speaker_style", "friendly")
    if style != "random":
        return style
    pool = voice_cfg.get("speakers_pool") or list(_BUILTIN_SPEAKERS)
    pool = [s for s in pool if s in _BUILTIN_SPEAKERS]
    if not pool:
        pool = list(_BUILTIN_SPEAKERS)
    seed = voice_cfg.get("random_seed")
    rng = random.Random(seed)
    return rng.choice(pool)


def voice_enabled_for_video(voice_cfg, cli_no_voice=False):
    if cli_no_voice:
        return False
    return bool(voice_cfg.get("enabled", True))
