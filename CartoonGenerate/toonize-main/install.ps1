# Fast staged install for Windows (avoids pip backtracking)
# Usage:
#   .venv\Scripts\activate
#   .\install.ps1
#   .\install.ps1 -Gpu

param([switch]$Gpu)

$ErrorActionPreference = "Stop"
$Py = (Get-Command python).Source

Write-Host "=== Upgrade pip ===" -ForegroundColor Cyan
& $Py -m pip install --upgrade pip

Write-Host "`n=== Base numeric stack ===" -ForegroundColor Cyan
& $Py -m pip install "numpy>=1.23.5,<2" "protobuf>=4.23.5,<5"

Write-Host "`n=== TensorFlow ===" -ForegroundColor Cyan
& $Py -m pip install tensorflow==2.15.0

Write-Host "`n=== Cartoon utilities ===" -ForegroundColor Cyan
& $Py -m pip install opencv-python==4.9.0.80 scikit-video==1.1.11 ffmpeg-python==0.2.0 tqdm==4.66.5 tf-slim==1.1.0 "imageio[ffmpeg]==2.31.6"

if ($Gpu) {
    Write-Host "`n=== PyTorch GPU ===" -ForegroundColor Cyan
    & $Py -m pip install torch==2.2.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu121
} else {
    Write-Host "`n=== PyTorch CPU ===" -ForegroundColor Cyan
    & $Py -m pip install torch==2.2.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu
}

Write-Host "`n=== Voice libraries (OpenVoice runtime) ===" -ForegroundColor Cyan
& $Py -m pip install "pyyaml>=6.0,<7" librosa==0.9.1 pydub==0.25.1 wavmark==0.0.3 "soundfile>=0.12.0" eng-to-ipa==0.0.2 inflect==7.0.0 unidecode==1.3.7 langid==1.1.6 pypinyin==0.50.0 cn2an==0.5.22 jieba==0.42.1 "more-itertools>=10.0.0"

Write-Host "`n=== OpenVoice (no-deps) ===" -ForegroundColor Cyan
& $Py -m pip install --no-deps git+https://github.com/myshell-ai/OpenVoice.git

Write-Host "`nDone. Next:" -ForegroundColor Green
Write-Host "  python setup_voice.py"
Write-Host "  python toonize.py c.mp4 --config my_voice.yaml"
