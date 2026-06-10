#!/usr/bin/env python3
"""
Fast staged install — avoids pip dependency backtracking.

Usage (from project folder, venv activated):
    python install.py
    python install.py --gpu
"""
from __future__ import print_function

import subprocess
import sys


def run(cmd, label):
    print("\n=== {} ===".format(label))
    print(" ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("\nFailed at step: {}".format(label))
        sys.exit(result.returncode)


def main():
    gpu = "--gpu" in sys.argv
    py = sys.executable
    pip = [py, "-m", "pip", "install"]

    run([py, "-m", "pip", "install", "--upgrade", "pip"], "Upgrade pip")

    run(
        pip + ["numpy>=1.23.5,<2", "protobuf>=4.23.5,<5"],
        "Base numeric stack",
    )

    run(
        pip + ["tensorflow==2.15.0"],
        "TensorFlow (cartoon model)",
    )

    run(
        pip
        + [
            "opencv-python==4.9.0.80",
            "scikit-video==1.1.11",
            "ffmpeg-python==0.2.0",
            "tqdm==4.66.5",
            "tf-slim==1.1.0",
            "imageio[ffmpeg]==2.31.6",
        ],
        "Cartoon utilities",
    )

    if gpu:
        run(
            pip
            + [
                "torch==2.2.2",
                "torchaudio==2.2.2",
                "--index-url",
                "https://download.pytorch.org/whl/cu121",
            ],
            "PyTorch (GPU CUDA 12.1)",
        )
    else:
        run(
            pip
            + [
                "torch==2.2.2",
                "torchaudio==2.2.2",
                "--index-url",
                "https://download.pytorch.org/whl/cpu",
            ],
            "PyTorch (CPU — faster download)",
        )

    # OpenVoice runtime (no faster-whisper — fails to build on Windows)
    run(
        pip
        + [
            "pyyaml>=6.0,<7",
            "librosa==0.9.1",
            "pydub==0.25.1",
            "wavmark==0.0.3",
            "soundfile>=0.12.0",
            "eng-to-ipa==0.0.2",
            "inflect==7.0.0",
            "unidecode==1.3.7",
            "langid==1.1.6",
            "pypinyin==0.50.0",
            "cn2an==0.5.22",
            "jieba==0.42.1",
            "more-itertools>=10.0.0",
        ],
        "Voice libraries (OpenVoice runtime)",
    )

    # --no-deps: OpenVoice pins numpy==1.22.0 which breaks TensorFlow 2.15
    run(
        pip
        + [
            "--no-deps",
            "git+https://github.com/myshell-ai/OpenVoice.git",
        ],
        "OpenVoice (no-deps — keeps TensorFlow numpy)",
    )

    run(
        pip
        + [
            "fastapi>=0.110,<1",
            "uvicorn[standard]>=0.27,<1",
            "python-multipart>=0.0.9,<1",
        ],
        "API server (FastAPI + Swagger)",
    )

    print("\nDone. Next:")
    print("  python setup_models.py")
    print("  python setup_voice.py")
    print("  python toonize.py c.mp4 --config my_voice.yaml")
    print("  uvicorn api.main:app --host 0.0.0.0 --port 8000")


if __name__ == "__main__":
    main()
