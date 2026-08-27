#!/usr/bin/env bash
set -euo pipefail

# Run on a Linux machine with an NVIDIA GPU and CUDA drivers.
# This installs ComfyUI and downloads the official Comfy-Org Wan 2.1 I2V assets.

ROOT="${COMFYUI_ROOT:-$HOME/ComfyUI}"
mkdir -p "$ROOT"

if [ ! -d "$ROOT/.git" ]; then
  git clone https://github.com/comfyanonymous/ComfyUI.git "$ROOT"
else
  git -C "$ROOT" pull --ff-only
fi

cd "$ROOT"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python -m pip install -U huggingface_hub

mkdir -p models/diffusion_models models/text_encoders models/vae models/clip_vision

hf download Comfy-Org/Wan_2.1_ComfyUI_repackaged \
  split_files/diffusion_models/wan2.1_i2v_480p_14B_fp16.safetensors \
  --local-dir "$ROOT/models"

hf download Comfy-Org/Wan_2.1_ComfyUI_repackaged \
  split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors \
  --local-dir "$ROOT/models"

hf download Comfy-Org/Wan_2.1_ComfyUI_repackaged \
  split_files/vae/wan_2.1_vae.safetensors \
  --local-dir "$ROOT/models"

hf download Comfy-Org/Wan_2.1_ComfyUI_repackaged \
  split_files/clip_vision/clip_vision_h.safetensors \
  --local-dir "$ROOT/models"

echo
printf 'ComfyUI + Wan 2.1 I2V assets installed in %s\n' "$ROOT"
printf 'Start with: cd %s && source .venv/bin/activate && python main.py --listen 0.0.0.0 --port 8188\n' "$ROOT"
