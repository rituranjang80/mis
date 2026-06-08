#!/bin/sh
set -eu

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

LISTEN="${COMFYUI_LISTEN:-0.0.0.0}"
PORT="${COMFYUI_PORT:-8188}"
EXTRA="${COMFYUI_EXTRA_ARGS:-}"

if [ "${COMFYUI_CPU:-1}" = "1" ] && ! echo "$EXTRA" | grep -q -- "--cpu"; then
  EXTRA="--cpu --cpu-vae --preview-method none --preview-size 256 --enable-manager ${EXTRA}"
elif [ "${COMFYUI_CPU:-1}" = "0" ] && ! echo "$EXTRA" | grep -q -- "--enable-manager"; then
  EXTRA="--enable-manager ${EXTRA}"
fi

# shellcheck disable=SC2086
exec python main.py --listen "$LISTEN" --port "$PORT" $EXTRA
