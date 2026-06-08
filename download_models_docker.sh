#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Downloading starter models into ./models ..."
docker compose --profile setup run --rm download-models

echo
echo "Done. Start ComfyUI with ./run_docker.sh"
