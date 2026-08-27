# Hanys AI Demo

Pipeline: reference image → local image-to-3D generator → `hanys.glb` → mobile web viewer.

## 1. Generate Hanys GLB

Recommended local generator: PIXFORM. It supports image-to-3D backends including TripoSR, Hunyuan3D and TRELLIS depending on the machine/GPU. Hunyuan3D is the preferred quality path; TripoSR is the quick prototype path.

Input: `assets/hanys-reference.png`
Output: `public/models/hanys.glb`

Model weights and generated binary assets are intentionally not committed to GitHub.

## 2. Run the viewer

From `hanys-demo/`:

```bash
npm install
npm run dev
```

Open the Vite URL on desktop or on the phone on the same network.

## 3. Viewer goals

- Three.js / React Three Fiber viewer
- GLB loading
- mobile-first UI
- idle animation layer
- tap-to-react jump
- emotion controls
- graceful placeholder when the GLB is missing

## 4. Next stages

1. Replace generated GLB with the final Hanys model.
2. Add a rigged/animated GLB or VRM.
3. Add facial expressions and lip-sync.
4. Add speech-to-text and TTS.
5. Add AI conversation and memory.

## Licensing

Only use source repositories and model weights according to their individual licenses. The Hanys character asset should be original or otherwise properly licensed.
