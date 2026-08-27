import json
import os
import random
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from nvidia_cosmos import generate_with_cosmos

ROOT = Path(__file__).resolve().parent
COMFYUI_URL = os.getenv("COMFYUI_URL", "http://127.0.0.1:8188").rstrip("/")
CHARACTERS_FILE = ROOT / "characters.json"
WORKFLOW_FILE = ROOT / "workflows" / "wan2.1_i2v_api.json"

app = FastAPI(title="Beboki Video Engine", version="0.3.0")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in os.getenv("CORS_ORIGINS", "*").split(",")], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

def load_characters() -> dict[str, Any]:
    return json.loads(CHARACTERS_FILE.read_text(encoding="utf-8"))

def comfy_request(path: str, payload: bytes | None = None, method: str = "GET") -> Any:
    req = urllib.request.Request(f"{COMFYUI_URL}{path}", data=payload, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"ComfyUI unavailable: {exc}") from exc

def download_reference(url: str) -> tuple[str, bytes]:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.headers.get_content_type(), response.read()
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"Reference image unavailable: {exc}") from exc

def upload_image(filename: str, image_bytes: bytes, content_type: str) -> str:
    boundary = f"----BebokiBoundary{uuid.uuid4().hex}"
    body = b"".join([f"--{boundary}\r\n".encode(), f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'.encode(), f"Content-Type: {content_type}\r\n\r\n".encode(), image_bytes, f"\r\n--{boundary}--\r\n".encode()])
    req = urllib.request.Request(f"{COMFYUI_URL}/upload/image", data=body, method="POST", headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return f"{result['subfolder']}/{result['name']}" if result.get("subfolder") else result["name"]
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=502, detail=f"Could not upload reference image to ComfyUI: {exc}") from exc

class GenerateRequest(BaseModel):
    character_id: str
    scene_prompt: str = Field(min_length=3, max_length=4000)
    seed: int | None = None
    width: int = Field(default=512, ge=256, le=1280)
    height: int = Field(default=512, ge=256, le=1280)
    frames: int = Field(default=33, ge=17, le=189)
    provider: str = Field(default="nvidia", pattern="^(nvidia|comfy)$")
    workflow: dict[str, Any] | None = None

def build_prompt(character: dict[str, Any], scene_prompt: str) -> tuple[str, str]:
    prompt = f"{character['continuity_prompt']}\n\nScene: {scene_prompt}\nKeep the canonical character identity unchanged. Same proportions, face, fur, hair, clothing, accessories and signature item. Cinematic high-quality 3D animated film, natural motion, coherent lighting, stable character design."
    negative = "different character, changed face, changed fur color, changed hairstyle, changed clothes, missing signature item, extra limbs, extra fingers, deformed hands, duplicate character, flicker, jitter, warped face, text, subtitles, watermark"
    return prompt, negative

@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True, "providers": {"nvidia": bool(os.getenv("NVIDIA_API_KEY")) and bool(os.getenv("NVIDIA_COSMOS_URL")), "comfy": bool(os.getenv("COMFYUI_URL"))}}

@app.get("/characters")
def characters() -> dict[str, Any]:
    return load_characters()

@app.post("/generate")
def generate(request: GenerateRequest) -> dict[str, Any]:
    registry = load_characters()
    character = next((c for c in registry["characters"] if c["id"] == request.character_id), None)
    if not character:
        raise HTTPException(status_code=404, detail="Unknown Bebok character")
    seed = request.seed if request.seed is not None else random.randint(1, 2**32 - 1)
    job_id = uuid.uuid4().hex[:12]
    prompt, negative = build_prompt(character, request.scene_prompt)
    content_type, image_bytes = download_reference(character["reference_image"])

    if request.provider == "nvidia":
        result = generate_with_cosmos(prompt=prompt, image_bytes=image_bytes, image_content_type=content_type, seed=seed, width=request.width, height=request.height, frames=request.frames)
        return {"ok": True, "job_id": job_id, "provider": "nvidia", "character_id": character["id"], "seed": seed, "result": result, "continuity": {"identity_locked": registry["rules"]["identity_locked"], "signature_items_preserved": registry["rules"]["preserve_signature_items"]}}

    workflow = request.workflow
    if workflow is None:
        if not WORKFLOW_FILE.exists():
            raise HTTPException(status_code=500, detail="Wan workflow missing")
        workflow = json.loads(WORKFLOW_FILE.read_text(encoding="utf-8"))
    else:
        workflow = json.loads(json.dumps(workflow))
    comfy_image = upload_image(f"bebok_{character['id']}_{job_id}.png", image_bytes, content_type)
    raw = json.dumps(workflow)
    for key, value in {"{{PROMPT}}": prompt, "{{NEGATIVE_PROMPT}}": negative, "{{SEED}}": str(seed), "{{CHARACTER_ID}}": character["id"], "{{JOB_ID}}": job_id, "{{INPUT_IMAGE}}": comfy_image}.items():
        raw = raw.replace(key, value)
    workflow = json.loads(raw)
    workflow["13"]["inputs"]["width"] = request.width
    workflow["13"]["inputs"]["height"] = request.height
    workflow["13"]["inputs"]["length"] = request.frames
    workflow["18"]["inputs"]["filename_prefix"] = f"beboki/{character['id']}/{job_id}"
    client_id = str(uuid.uuid4())
    result = comfy_request("/prompt", json.dumps({"prompt": workflow, "client_id": client_id}).encode(), method="POST")
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result)
    return {"ok": True, "job_id": job_id, "provider": "comfy", "prompt_id": result.get("prompt_id"), "client_id": client_id, "character_id": character["id"], "seed": seed, "generation": {"width": request.width, "height": request.height, "frames": request.frames}, "continuity": {"identity_locked": registry["rules"]["identity_locked"], "signature_items_preserved": registry["rules"]["preserve_signature_items"]}}

@app.get("/jobs/{prompt_id}")
def job(prompt_id: str) -> Any:
    return comfy_request(f"/history/{prompt_id}")
