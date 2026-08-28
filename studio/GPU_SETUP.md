# GPU setup — first render

## 1. Prepare

Use a Linux NVIDIA GPU runtime. The first video workflow uses **Wan2.1 T2V 1.3B**, whose official ComfyUI documentation states the lightweight model can run with about 8 GB VRAM. The first image workflow currently uses the NVIDIA FLUX workflow as a technical fallback; for commercial publishing we should switch the image stage to Qwen-Image (Apache-2.0) before monetization.

## 2. Install

```bash
git clone https://github.com/bajerskim11-eng/beboki-gra.git
cd beboki-gra
bash studio/scripts/bootstrap_gpu.sh
```

Then start ComfyUI:

```bash
bash studio/scripts/run_comfy.sh
```

Start Story Studio in another shell:

```bash
cd studio
source .venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8787
```

## 3. Models

Wan2.1 1.3B:

- `wan2.1_t2v_1.3B_fp16.safetensors` → `models/diffusion_models/`
- `umt5_xxl_fp8_e4m3fn_scaled.safetensors` → `models/text_encoders/`
- `wan_2.1_vae.safetensors` → `models/vae/`

The official ComfyUI guide documents these model locations and the 1.3B workflow. See the project research notes before downloading any checkpoint.

## 4. Generate

Open the Story Studio UI and use `/api/story` to create a scene, then `/api/generate/image` or `/api/generate/video` to queue a ComfyUI job.

## 5. Production rule

Keep every generated asset referenced by episode/scene/shot/seed in the SQLite memory. Never overwrite a good keyframe. A scene should be regenerated from the same seed/workflow when continuity needs to be restored.
