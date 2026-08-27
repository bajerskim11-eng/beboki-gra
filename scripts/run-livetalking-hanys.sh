#!/usr/bin/env bash
set -euo pipefail
# Run on a CUDA GPU host, not Vercel.
# LiveTalking expects a silent source video for custom avatar generation.
# Place the prepared Hanys silent video at data/hanys_source.mp4.

python -m avatars.wav2lip.genavatar --video_path data/hanys_source.mp4 --img_size 256 --avatar_id hanys
python app.py --transport webrtc --model wav2lip --avatar_id hanys
