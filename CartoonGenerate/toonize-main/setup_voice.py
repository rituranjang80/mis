"""
Download OpenVoice V1 converter checkpoints for local voice cloning.

Run once: python setup_voice.py
"""
import shutil
import urllib.request
import zipfile
from pathlib import Path

CHECKPOINTS_URL = (
    "https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip"
)
PROJECT_DIR = Path(__file__).resolve().parent
CHECKPOINTS_DIR = PROJECT_DIR / "checkpoints"
ZIP_PATH = PROJECT_DIR / "checkpoints_1226.zip"


def main():
    if (CHECKPOINTS_DIR / "converter" / "checkpoint.pth").is_file():
        print("Checkpoints already present at", CHECKPOINTS_DIR)
        return

    print("Downloading OpenVoice checkpoints (~500 MB)...")
    urllib.request.urlretrieve(CHECKPOINTS_URL, ZIP_PATH)

    print("Extracting...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        zf.extractall(PROJECT_DIR)

    ZIP_PATH.unlink(missing_ok=True)

    if not (CHECKPOINTS_DIR / "converter" / "checkpoint.pth").is_file():
        raise SystemExit(
            "Extraction failed: expected checkpoints/converter/checkpoint.pth"
        )

    print("Done. If not installed yet:")
    print("  python install.py")


if __name__ == "__main__":
    main()
