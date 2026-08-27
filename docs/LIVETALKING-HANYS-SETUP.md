# Hanys AI Avatar — LiveTalking integration

## Architecture
Shopify Hanys reference → avatar video/frames → LiveTalking (MuseTalk/Wav2Lip) → WebRTC → browser. LLM is a separate service and can be DeepSeek Harness/OpenRouter.

## Why LiveTalking
LiveTalking supports custom digital-human avatars, WebRTC, TTS modules and LLM dialogue. For a custom avatar it expects a silent source video and generates avatar assets; MuseTalk/Wav2Lip then drives lip-sync from speech.

Official project: https://github.com/lipku/LiveTalking

## Required runtime
GPU machine with CUDA. The project documents Python 3.10, PyTorch/CUDA combinations and WebRTC port requirements. Vercel should host only the frontend/API proxy; the realtime inference service must run on a GPU host.

## Hanys
Use `public/hanys-reference.json` / the Shopify `hanys.jpg` as the visual reference. For LiveTalking, first create a short silent Hanys source video with a consistent front-facing face; then run the appropriate avatar generator.

## Next integration
1. Run LiveTalking on GPU.
2. Generate a Hanys avatar with MuseTalk or Wav2Lip.
3. Expose WebRTC endpoint.
4. Add `VITE_LIVETALKING_URL` to frontend.
5. Route chat text to DeepSeek Harness and pass returned text to LiveTalking `/human`.

Do not put GPU inference inside Vercel serverless functions.
