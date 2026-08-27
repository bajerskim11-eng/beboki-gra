import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from fastapi import HTTPException

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_COSMOS_URL = os.getenv("NVIDIA_COSMOS_URL", "").rstrip("/")
NVIDIA_COSMOS_MODEL = os.getenv("NVIDIA_COSMOS_MODEL", "nvidia/cosmos3-nano")
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def generate_with_cosmos(
    *,
    prompt: str,
    image_bytes: bytes,
    image_content_type: str,
    seed: int,
    width: int,
    height: int,
    frames: int,
) -> dict[str, Any]:
    """Call the NVIDIA Build Cosmos3 Nano hosted endpoint.

    NVIDIA's current model card documents image conditioning as a base64/data URI
    and returns MP4 as `b64_video`. The exact hosted endpoint URL is kept in an
    environment variable because NVIDIA may change the catalog routing URL.
    """
    if not NVIDIA_API_KEY:
        raise HTTPException(status_code=503, detail="NVIDIA_API_KEY is not configured")
    if not NVIDIA_COSMOS_URL:
        raise HTTPException(status_code=503, detail="NVIDIA_COSMOS_URL is not configured")

    data_uri = f"data:{image_content_type};base64,{base64.b64encode(image_bytes).decode('ascii')}"
    payload = {
        "model": NVIDIA_COSMOS_MODEL,
        "prompt": prompt,
        "image": data_uri,
        "resolution": f"{width}x{height}",
        "num_output_frames": frames,
        "seed": seed,
    }

    req = urllib.request.Request(
        NVIDIA_COSMOS_URL,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise HTTPException(status_code=502, detail=f"NVIDIA Cosmos error {exc.code}: {detail[:2000]}") from exc
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=502, detail=f"NVIDIA Cosmos unavailable: {exc}") from exc

    encoded = result.get("b64_video")
    if not encoded:
        raise HTTPException(status_code=502, detail={"message": "NVIDIA response did not contain b64_video", "response": result})

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"bebok-cosmos-{seed}.mp4"
    output_path = OUTPUT_DIR / filename
    output_path.write_bytes(base64.b64decode(encoded))

    return {
        "provider": "nvidia",
        "model": NVIDIA_COSMOS_MODEL,
        "filename": filename,
        "path": str(output_path),
        "bytes": output_path.stat().st_size,
        "seed": seed,
    }
