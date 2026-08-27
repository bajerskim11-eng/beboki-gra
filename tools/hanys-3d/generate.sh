#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -d TripoSR ]; then
  git clone --depth 1 https://github.com/VAST-AI-Research/TripoSR.git
fi

python -m pip install -r requirements.txt
python -m pip install -r TripoSR/requirements.txt

curl -L 'https://raw.githubusercontent.com/bajerskim11-eng/beboki-katowice-mis/main/public/beboki/hanys.jpeg' -o hanys-reference.jpeg

python TripoSR/run.py hanys-reference.jpeg --output-dir output --bake-texture

mkdir -p ../../public/models
cp output/0/mesh.glb ../../public/models/hanys.glb

echo "Generated public/models/hanys.glb"
