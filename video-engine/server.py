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

ROOT = Path(__file__).resolve().parent
COMFYUI_URL = os.getenv("COMFYUI_URL", "http://127.0.0.1:8188").rstrip("/")
CHARACTERS_FILE = ROOT / "characters.json"
WORKFLOW_FILE = ROOT / "comfyui_workflow.template.json"

app = FastAPI(title="Beboki Video Engine", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in os.getenv("CORS_ORIGINS", "*").split(",")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_characters() -> dict[str, Any]:
    return json.loads(CHARACTERS_FILE.read_text(encoding="utf-8"))


def comfy_request(path: str, payload: bytes | None = None, method: str = "GET") -> Any:
    req = urllib.request.Request(
        f"{COMFYUI_URL}{path}",
        data=payload,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"ComfyUI unavailable: {exc}") from exc


class GenerateRequest(BaseModel):
    character_id: str
    scene_prompt: str = Field(min_length=3, max_length=4000)
    seed: int | None = None
    workflow: dict[str, Any] | None = None


@app.get("/health")
def health() -> dict[str, Any]:
    try:
        comfy_request("/system_stats")
        return {"ok": True, "comfyui": "online"}
    except HTTPException:
        return {"ok": True, "comfyui": "offline"}


@app.get("/characters")
def characters() -> dict[str, Any]:
    return load_characters()


@app.post("/generate")
def generate(request: GenerateRequest) -> dict[str, Any]:
    registry = load_characters()
    character = next((c for c in registry["characters"] if c["id"] == request.character_id), None)
    if not character:
        raise HTTPException(status_code=404, detail="Unknown Bebok character")

    seed = request.seed if request.seed is not None else random.randint(1, 2**63 - 1)
    prompt = (
        f"{character['continuity_prompt']}\n\n"
        f"Scene: {request.scene_prompt}\n"
        "Keep the canonical character identity unchanged. Cinematic 3D animated film quality."
    )

    workflow = request.workflow
    if workflow is None:
        if not WORKFLOW_FILE.exists():
            raise HTTPException(status_code=500, detail="Workflow template missing")
        workflow = json.loads(WORKFLOW_FILE.read_text(encoding="utf-8"))

    raw = json.dumps(workflow)
    raw = raw.replace("{{PROMPT}}", json.dumps(prompt)[1:-1])
    raw = raw.replace("{{SEED}}", str(seed))
    raw = raw.replace("{{CHARACTER_ID}}", character["id"])
    raw = raw.replace("{{REFERENCE_IMAGE}}", character["reference_image"])
    workflow = json.loads(raw)

    client_id = str(uuid.uuid4())
    payload = json.dumps({"prompt": workflow, "client_id": client_id}).encode("utf-8")
    result = comfy_request("/prompt", payload, method="POST")

    return {
        "ok": True,
        "prompt_id": result.get("prompt_id"),
        "client_id": client_id,
        "character_id": character["id"],
        "seed": seed,
        "continuity": {
            "identity_locked": registry["rules"]["identity_locked"],
            "signature_items_preserved": registry["rules"]["preserve_signature_items"],
        },
    }


@app.get("/jobs/{prompt_id}")
def job(prompt_id: str) -> Any:
    return comfy_request(f"/history/{prompt_id}")
