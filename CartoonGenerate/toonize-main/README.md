## Turn your image or video into a cartoon

Cartoonize images/videos and optionally replace video audio with an auto-generated human voice.

## Install (fast — recommended)

**Do not** run `pip install -r requirements.txt` as one big install on old pip — it backtracks for a long time.

```powershell
python -m venv .venv
.venv\Scripts\activate
python install.py
python setup_voice.py
```

GPU voice (optional, NVIDIA CUDA 12.1):

```powershell
python install.py --gpu
```

Windows PowerShell before run:

```powershell
$env:PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"
```

Requires **ffmpeg** on PATH. Python **3.9–3.10** recommended.

## Run

```powershell
python toonize.py c.mp4
python toonize.py c.mp4 --config my_voice.yaml
python toonize.py c.mp4 --no-voice
```

## Voice config

| File | Purpose |
|------|---------|
| `voice_config.yaml` | Default settings |
| `my_voice.yaml` | Custom profile for `--config` |

## Why install was slow

The old `requirements.txt` pinned **every** transitive package (full `pip freeze`) plus both `tensorflow` and `tensorflow-intel`, plus loose `torch` ranges and OpenVoice — pip spent minutes backtracking.

**Fix:** `install.py` installs in **7 small steps** (numpy → tensorflow → cartoon → torch → voice → openvoice). Each step finishes in 1–3 minutes instead of one 30+ minute resolver loop.

## Troubleshooting

| Error | Fix |
|-------|-----|
| `librosa` conflict | Use `python install.py` (pins `librosa==0.9.1` for OpenVoice) |
| Pip stuck / backtracking | Stop (Ctrl+C), run `python install.py` |
| `checkpoints are missing` | `python setup_voice.py` |
| `Python packages are missing` | `python install.py` |
| `Voice config not found` | Create `my_voice.yaml` or fix `--config` path |


🎬 Top Picks for Video Dubbing & Voice Cloning
Here is a comparison of the most promising tools for your project:

Project Name	Best For	Key Features	Setup & Ease of Use
Voice-Pro	All-in-one video dubbing	All-in-one pipeline: video download, vocal isolation, transcription, translation, voice cloning, and video synthesis.	Easiest: Gradio web UI, designed for non-technical users. Requires no coding.
OmniVoice Studio	Local ElevenLabs alternative	Zero-shot cloning from 3-second clips, supports 646 languages, batch video dubbing.	Easy: Desktop App (Windows, macOS, Linux) or Docker available.
auto dubbing - local	Long-form content	Specifically for dubbing long MP4s (like webinars). Works offline, keeps original video intact.	Intermediate: Python script using faster-whisper, pyannote, and XTTS v2. Requires some setup.
clone-voice	Zero-shot voice cloning	Lightweight, Web UI, supports 12+ languages. Highly focused on voice cloning itself.	Easy: Web UI, simple 5-step process.
video_dubbing_tool	Streamlit-based dubbing	Modern GUI, voice cloning, background music preservation, adjustable speech/music volumes.	Intermediate: Streamlit app. Requires Python 3.9+, ffmpeg, and CUDA for best performance.
🚀 Installation Tips
Here are some quick tips to help you get started:

Essential Dependency: Before running any of these projects, ensure you have FFmpeg installed and added to your system's PATH. It's a core tool for processing audio and video files.

GPU Acceleration: While some tools can run on a CPU, having an NVIDIA GPU with CUDA support will dramatically speed up processing, especially for longer videos.

Hugging Face Token: Some projects, like the auto dubbing - local tool, require a Hugging Face token to download certain models. You'll need to sign up for a free account and accept the model's terms of use before starting.

I hope this helps you find the perfect tool for your voice conversion project! Which of these features is most important for what you're trying to do?


