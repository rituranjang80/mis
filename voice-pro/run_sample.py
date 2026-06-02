"""Minimal Voice-Pro sample: download test audio and transcribe with faster-whisper."""
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

SAMPLE_URL = "https://github.com/openai/whisper/raw/main/tests/jfk.flac"
SAMPLE_PATH = os.path.join(ROOT, "workspace", "sample_jfk.flac")


def main():
    os.makedirs(os.path.dirname(SAMPLE_PATH), exist_ok=True)
    if not os.path.isfile(SAMPLE_PATH):
        print(f"Downloading sample audio to {SAMPLE_PATH} ...")
        urllib.request.urlretrieve(SAMPLE_URL, SAMPLE_PATH)
    else:
        print(f"Using cached sample: {SAMPLE_PATH}")

    from faster_whisper import WhisperModel

    device = "cuda"
    try:
        import torch
        if not torch.cuda.is_available():
            device = "cpu"
    except ImportError:
        device = "cpu"

    print(f"Loading faster-whisper 'tiny' on {device} (first run downloads the model)...")
    model = WhisperModel("tiny", device=device, compute_type="int8" if device == "cpu" else "float16")

    print("Transcribing...")
    segments, info = model.transcribe(SAMPLE_PATH, beam_size=1)
    print(f"Detected language: {info.language} (probability {info.language_probability:.2f})")
    print("-" * 60)
    text = []
    for seg in segments:
        line = f"[{seg.start:6.1f}s -> {seg.end:6.1f}s] {seg.text.strip()}"
        print(line)
        text.append(seg.text.strip())
    print("-" * 60)
    print("Full text:", " ".join(text))
    print("Sample completed successfully.")


if __name__ == "__main__":
    main()
