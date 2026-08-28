#!/usr/bin/env bash
set -euo pipefail

# Beboki Story Studio - NVIDIA/Colab bootstrap
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMFY_DIR="${COMFY_DIR:-$ROOT/.comfyui}"

python3 -m venv "$ROOT/.gpu-venv" || true
source "$ROOT/.gpu-venv/bin/activate"
python -m pip install --upgrade pip

if [ ! -d "$COMFY_DIR" ]; then
  git clone https://github.com/comfyanonymous/ComfyUI.git "$COMFY_DIR"
fi

cd "$COMFY_DIR"
python -m pip install -r requirements.txt
mkdir -p models/checkpoints models/diffusion_models models/vae models/text_encoders models/clip_vision input output

cat <<'EOF'

Beboki GPU environment prepared.

Next:
  1. Put/download the required model weights into .comfyui/models/.
  2. Run: studio/scripts/run_comfy.sh
  3. Start the Story Studio backend from studio/.

For the first video test use Wan2.1 1.3B (low VRAM). Upgrade to Wan2.2 TI2V-5B when the GPU can handle it.
EOF
