"""
Voice transformation for cartoon videos using OpenVoice.

By default, builds a synthetic target voice from built-in speakers (no WAV file).
Optional file mode via voice_config.yaml.
"""
import os
import subprocess
import tempfile
from pathlib import Path

_PROJECT_DIR = Path(__file__).resolve().parent
_CHECKPOINTS_DIR = _PROJECT_DIR / "checkpoints"
_CONVERTER_DIR = _CHECKPOINTS_DIR / "converter"
_CONVERTER_CKPT = _CONVERTER_DIR / "checkpoint.pth"
_CONVERTER_CFG = _CONVERTER_DIR / "config.json"


def checkpoints_ready():
    if not (_CONVERTER_CKPT.is_file() and _CONVERTER_CFG.is_file()):
        return False
    en_base = _CHECKPOINTS_DIR / "base_speakers" / "EN" / "checkpoint.pth"
    return en_base.is_file()


def voice_deps_ready():
    """Return (ok, error_message)."""
    try:
        import torch  # noqa: F401
        import yaml  # noqa: F401
        import soundfile  # noqa: F401
        import pypinyin  # noqa: F401
        from openvoice.api import BaseSpeakerTTS, ToneColorConverter  # noqa: F401
    except ImportError as exc:
        return False, str(exc)
    return True, ""


def _split_audio_segments(audio_path, tmp_dir, split_seconds=10.0):
    """Split audio into chunks for OpenVoice speaker embedding (no faster-whisper)."""
    import numpy as np
    from pydub import AudioSegment

    audio = AudioSegment.from_file(str(audio_path))
    duration = audio.duration_seconds
    if duration < 0.5:
        raise ValueError("Audio too short for voice extraction: {}".format(audio_path))

    segments = []
    num_splits = max(1, int(np.round(duration / split_seconds)))
    interval = duration / num_splits
    start = 0.0
    for i in range(num_splits):
        end = duration if i == num_splits - 1 else min(start + interval, duration)
        seg_path = Path(tmp_dir) / "seg_{:03d}.wav".format(i)
        audio[int(start * 1000): int(end * 1000)].export(str(seg_path), format="wav")
        segments.append(str(seg_path))
        start = end
    return segments


def extract_speaker_embedding(audio_path, converter, split_seconds=10.0):
    """Extract tone-color embedding without OpenVoice se_extractor (Windows-safe)."""
    with tempfile.TemporaryDirectory() as tmp:
        segments = _split_audio_segments(audio_path, tmp, split_seconds=split_seconds)
        return converter.extract_se(segments)


def _base_speaker_dir(language):
    lang = (language or "EN").upper()
    return _CHECKPOINTS_DIR / "base_speakers" / lang


def extract_audio_wav(video_path, wav_path, sample_rate=24000):
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", str(sample_rate),
        "-ac", "1",
        str(wav_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            "ffmpeg failed to extract audio from {}:\n{}".format(
                video_path, result.stderr
            )
        )


def _load_converter():
    import torch
    from openvoice.api import ToneColorConverter

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    converter = ToneColorConverter(str(_CONVERTER_CFG), device=device)
    converter.load_ckpt(str(_CONVERTER_CKPT))
    return converter, device


def _load_base_tts(language):
    from openvoice.api import BaseSpeakerTTS

    ckpt_base = _base_speaker_dir(language)
    if not (ckpt_base / "checkpoint.pth").is_file():
        raise RuntimeError(
            "Base speaker checkpoints not found at {}. "
            "Run: python setup_voice.py".format(ckpt_base)
        )
    import torch

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    tts = BaseSpeakerTTS(str(ckpt_base / "config.json"), device=device)
    tts.load_ckpt(str(ckpt_base / "checkpoint.pth"))
    return tts, device


def _language_label(code):
    return {"EN": "English", "ZH": "Chinese"}.get(code.upper(), "English")


def generate_target_embedding(converter, voice_cfg):
    """Build target speaker embedding automatically (no user reference file)."""
    from voice_config import pick_speaker_style

    split_seconds = float(voice_cfg.get("segment_seconds", 10.0))
    mode = (voice_cfg.get("mode") or "auto").lower()
    ref_file = voice_cfg.get("reference_file")
    if mode == "file" and ref_file:
        path = Path(ref_file).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError("reference_file not found: {}".format(path))
        target_se = extract_speaker_embedding(path, converter, split_seconds)
        return target_se, "file:{}".format(path.name)

    speaker = pick_speaker_style(voice_cfg)
    language = voice_cfg.get("language", "EN")
    speed = float(voice_cfg.get("speed", 1.0))
    text = (voice_cfg.get("reference_text") or "").strip()
    if not text:
        text = "Hello. This is a generated human voice sample."

    tts, _ = _load_base_tts(language)
    with tempfile.TemporaryDirectory() as tmp:
        ref_wav = Path(tmp) / "auto_reference.wav"
        tts.tts(
            text,
            str(ref_wav),
            speaker=speaker,
            language=_language_label(language),
            speed=speed,
        )
        target_se = extract_speaker_embedding(ref_wav, converter, split_seconds)
    return target_se, "auto:{}:{}".format(language, speaker)


def transform_audio(source_audio_path, voice_cfg, output_wav_path):
    """Convert source speech to configured target voice."""
    if not checkpoints_ready():
        raise RuntimeError(
            "OpenVoice checkpoints missing. Run:\n"
            "  python setup_voice.py\n"
            "Then:\n"
            "  python install.py"
        )

    converter, _ = _load_converter()
    split_seconds = float(voice_cfg.get("segment_seconds", 10.0))

    source_se = extract_speaker_embedding(source_audio_path, converter, split_seconds)
    target_se, target_desc = generate_target_embedding(converter, voice_cfg)
    print("Target voice: {}".format(target_desc))

    converter.convert(
        audio_src_path=str(source_audio_path),
        src_se=source_se,
        tgt_se=target_se,
        output_path=str(output_wav_path),
        message="@MyShell",
    )
    return output_wav_path


def transform_video_audio(video_path, voice_cfg, output_wav_path=None):
    video_path = Path(video_path).resolve()
    if output_wav_path is None:
        fd, output_wav_path = tempfile.mkstemp(suffix="_voice.wav")
        os.close(fd)
        output_wav_path = Path(output_wav_path)
    else:
        output_wav_path = Path(output_wav_path)

    sample_rate = int(voice_cfg.get("sample_rate", 24000))
    with tempfile.TemporaryDirectory() as tmp:
        src_wav = Path(tmp) / "source.wav"
        extract_audio_wav(video_path, src_wav, sample_rate=sample_rate)
        transform_audio(src_wav, voice_cfg, output_wav_path)

    return output_wav_path
