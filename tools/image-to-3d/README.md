# Hanys image → GLB

The input image has been uploaded to the `hanys-demo` branch. The repository is prepared to receive the generated model at:

`public/models/hanys.glb`

## Recommended generator

Use an open-source image-to-3D project locally. Start with PIXFORM and its TripoSR backend for a quick test; use Hunyuan3D/TRELLIS on a suitable NVIDIA GPU when quality is the priority.

PIXFORM: https://github.com/dmonfrooij/pixform
TripoSR: https://github.com/VAST-AI-Research/TripoSR
Hunyuan3D-2: https://github.com/Tencent/Hunyuan3D-2
TRELLIS: https://github.com/microsoft/TRELLIS

## Output

Export the generated mesh as GLB and copy it to:

```text
public/models/hanys.glb
```

Then the web app loads it automatically.

## Important

The generator weights are not committed to this repository. Check each model's current license and hardware requirements before using it commercially. A generated mesh is only a first prototype: for convincing animation we will need a rigged model and facial/viseme blendshapes or a VRM-ready rig.
