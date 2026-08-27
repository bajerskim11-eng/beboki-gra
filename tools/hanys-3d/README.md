# Hanys — image → 3D generator

This folder integrates the open-source **TripoSR** single-image 3D reconstruction pipeline into the Beboki project.

Source project: https://github.com/VAST-AI-Research/TripoSR
License: MIT.

## Reference image

The source image currently lives in the companion repository:
`bajerskim11-eng/beboki-katowice-mis/public/beboki/hanys.jpeg`

Raw reference URL:
https://raw.githubusercontent.com/bajerskim11-eng/beboki-katowice-mis/main/public/beboki/hanys.jpeg

## Generate Hanys

This generator is intended to run on a machine with an NVIDIA GPU (or a compatible local backend). TripoSR can export GLB and needs roughly 6 GB VRAM for a single-image inference in the default configuration.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py https://raw.githubusercontent.com/bajerskim11-eng/beboki-katowice-mis/main/public/beboki/hanys.jpeg --output-dir output --bake-texture
```

If the upstream CLI does not accept URLs in the installed revision, download the image first and pass the local file:

```bash
curl -L 'https://raw.githubusercontent.com/bajerskim11-eng/beboki-katowice-mis/main/public/beboki/hanys.jpeg' -o hanys-reference.jpeg
python run.py hanys-reference.jpeg --output-dir output --bake-texture
```

The target asset for the web avatar is:

`public/models/hanys.glb`

After generation, copy the best GLB there and the avatar can load it with Three.js.

## Important

The generated mesh is an **image-to-3D reconstruction**, not a production character rig. After generation we still need to rig/weight Hanys and add idle, walk, gesture and facial/lip-sync animations. Those animation steps are deliberately separate so the same Hanys asset can later be used in WebXR/AR.
