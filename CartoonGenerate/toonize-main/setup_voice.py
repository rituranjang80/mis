"""
Download OpenVoice V1 converter checkpoints for local voice cloning.

Run once: python setup_voice.py
"""
import shutil
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

# Primary mirror (HuggingFace) — official MyShell S3 link often returns 404/AccessDenied
CHECKPOINTS_URLS = (
    "https://huggingface.co/camenduru/OpenVoice/resolve/main/checkpoints_1226.zip",
    "https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip",
)

PROJECT_DIR = Path(__file__).resolve().parent
CHECKPOINTS_DIR = PROJECT_DIR / "checkpoints"
ZIP_PATH = PROJECT_DIR / "checkpoints_1226.zip"
CONVERTER_CKPT = CHECKPOINTS_DIR / "converter" / "checkpoint.pth"


def checkpoints_ready() -> bool:
    return CONVERTER_CKPT.is_file()


def download_checkpoints() -> None:
    errors = []
    for url in CHECKPOINTS_URLS:
        try:
            print("Downloading OpenVoice checkpoints (~500 MB)...")
            print("  source: {}".format(url))
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "toonize-setup/1.0"},
            )
            with urllib.request.urlopen(req, timeout=600) as resp:
                with open(ZIP_PATH, "wb") as out:
                    shutil.copyfileobj(resp, out)
            return
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            errors.append("  {} -> {}".format(url, exc))
            ZIP_PATH.unlink(missing_ok=True)

    raise SystemExit(
        "Failed to download OpenVoice checkpoints from all mirrors:\n"
        + "\n".join(errors)
        + "\n\nManual fix: download checkpoints_1226.zip and extract to:\n  "
        + str(CHECKPOINTS_DIR)
    )


def extract_checkpoints() -> None:
    print("Extracting...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        zf.extractall(PROJECT_DIR)
    ZIP_PATH.unlink(missing_ok=True)

    if not checkpoints_ready():
        raise SystemExit(
            "Extraction failed: expected {}".format(CONVERTER_CKPT)
        )


def main():
    if checkpoints_ready():
        print("Checkpoints already present at", CHECKPOINTS_DIR)
        return

    download_checkpoints()
    extract_checkpoints()
    print("Done. If not installed yet:")
    print("  python install.py")


if __name__ == "__main__":
    main()
