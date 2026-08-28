#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMFY_DIR="${COMFY_DIR:-$ROOT/.comfyui}"
source "$ROOT/.gpu-venv/bin/activate"
cd "$COMFY_DIR"
python main.py --listen 0.0.0.0 --port "${COMFY_PORT:-8188}" "$@"
