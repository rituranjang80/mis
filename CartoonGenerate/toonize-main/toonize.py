import argparse
import os
import sys
from pathlib import Path

_project_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, _project_dir)
sys.path.insert(0, os.path.join(_project_dir, 'white_box_cartoonizer'))

from voice_config import load_voice_config, voice_enabled_for_video
from voice_clone import checkpoints_ready, voice_deps_ready

_wb_cartoonizer = None


def get_cartoonizer():
    global _wb_cartoonizer
    if _wb_cartoonizer is None:
        import cv2  # noqa: F401 — loaded after voice preflight
        from cartoonize import WB_Cartoonize

        _wb_cartoonizer = WB_Cartoonize(
            os.path.abspath("white_box_cartoonizer/saved_models/"), False
        )
    return _wb_cartoonizer


def is_video(file_path):
    import ffmpeg

    video_stream = ffmpeg.probe(file_path, select_streams='v')['streams']
    return bool(video_stream)


def validate_voice_stack(apply_voice):
    if not apply_voice:
        return
    if not checkpoints_ready():
        print(
            "Voice is enabled but OpenVoice checkpoints are missing.\n"
            "Run: python setup_voice.py"
        )
        sys.exit(1)
    ok, err = voice_deps_ready()
    if not ok:
        print(
            "Voice is enabled but Python packages are missing.\n"
            "Run: python install.py\n"
            "Detail: {}".format(err)
        )
        sys.exit(1)


def process_images(pattern, voice_cfg=None, apply_voice=False):
    import cv2

    validate_voice_stack(apply_voice)
    wb = get_cartoonizer()

    directory = Path(pattern).parent
    file_pattern = Path(pattern).name

    for img_path in directory.glob(file_pattern):
        if not img_path.is_file():
            continue
        img = cv2.imread(str(img_path))
        if img is not None:
            print("Processing image: {}".format(img_path))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cartoon_image = wb.infer(img)
            new_img_path = img_path.with_name(img_path.stem + '_toon' + img_path.suffix)
            cv2.imwrite(
                str(new_img_path),
                cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR),
            )
        elif is_video(str(img_path)):
            print("Processing video: {}".format(img_path))
            cap = cv2.VideoCapture(str(img_path))
            fps = str(round(cap.get(cv2.CAP_PROP_FPS), 2))
            cap.release()
            vcfg = voice_cfg if apply_voice else None
            wb.process_video(str(img_path), fps, voice_config=vcfg)
        else:
            print("Unknown format of {}. Skipping".format(img_path))


def main():
    parser = argparse.ArgumentParser(
        description="Cartoonize images/videos. Video audio can be auto-changed via YAML config."
    )
    parser.add_argument(
        "pattern",
        help="File path or glob (e.g. c.mp4 or '*.jpg')",
    )
    parser.add_argument(
        "--config",
        "-c",
        metavar="my_voice.yaml",
        help="Voice settings YAML (default: voice_config.yaml in project folder)",
    )
    parser.add_argument(
        "--no-voice",
        action="store_true",
        help="Skip voice change; keep original audio",
    )
    args = parser.parse_args()

    try:
        voice_cfg = load_voice_config(
            args.config,
            config_required=bool(args.config),
        )
    except FileNotFoundError as e:
        print("Error: {}".format(e))
        sys.exit(1)
    except RuntimeError as e:
        print("Error: {}".format(e))
        sys.exit(1)

    apply_voice = voice_enabled_for_video(voice_cfg, cli_no_voice=args.no_voice)

    if apply_voice:
        print(
            "Voice: enabled | mode={} | language={} | style={}".format(
                voice_cfg.get("mode", "auto"),
                voice_cfg.get("language", "EN"),
                voice_cfg.get("speaker_style", "friendly"),
            )
        )

    process_images(args.pattern, voice_cfg=voice_cfg, apply_voice=apply_voice)


if __name__ == "__main__":
    main()
