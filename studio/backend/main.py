import os
import random
from pathlib import Path
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from .memory import add, list_memories, search, seed_from_canon
from .comfy import load_workflow, queue_prompt, patch_text_node, patch_seed_node

ROOT = Path(__file__).resolve().parents[1]
COMFY_URL = os.getenv("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3")
app = FastAPI(title="Beboki Story Studio")

class MemoryIn(BaseModel):
    kind: str = "note"
    title: str
    content: str
    tags: list[str] = []

class PromptIn(BaseModel):
    idea: str
    scene: str = ""
    character: str = ""
    save: bool = True
    seed: int | None = None

@app.on_event("startup")
def startup():
    seed_from_canon()

@app.get("/", response_class=HTMLResponse)
def index():
    return (ROOT / "index.html").read_text(encoding="utf-8")

@app.get("/api/memory")
def memory():
    return {"items": list_memories()}

@app.get("/api/memory/search")
def memory_search(q: str):
    return {"items": search(q)}

@app.post("/api/memory")
def memory_add(item: MemoryIn):
    add(item.kind, item.title, item.content, item.tags)
    return {"ok": True}

async def ollama(prompt: str):
    async with httpx.AsyncClient(timeout=180) as client:
        r = await client.post(f"{OLLAMA_URL}/api/chat", json={
            "model": OLLAMA_MODEL, "stream": False,
            "messages": [
                {"role":"system","content":"Jesteś głównym scenarzystą świata Beboków. Pilnuj kanonu, Katowic, czterech Beboków i psów. Pisz po polsku. Nie zmieniaj wyglądu postaci."},
                {"role":"user","content":prompt}
            ]})
        r.raise_for_status()
        return r.json()["message"]["content"]

@app.post("/api/story")
async def story(item: PromptIn):
    prompt = f'''Stwórz scenę do bajki „Beboki i Serce Śląska”.

Pomysł autora:\n{item.idea}\n\nMiejsce/scena:\n{item.scene}\n\nBebok:\n{item.character}

Zwróć: 1. krótki opis sceny, 2. narrację, 3. dialogi, 4. prompt do ilustracji komiksowej, 5. prompt image-to-video na 5–8 sekund, 6. dźwięki/atmosferę, 7. cel sceny w historii. Nie wymyślaj nowych głównych postaci. Zachowaj ciepły, filmowy klimat.'''
    try:
        result = await ollama(prompt)
    except Exception as e:
        raise HTTPException(502, f"Ollama niedostępne: {e}")
    if item.save:
        add("scene", item.idea, result, ["generated", "story"])
    return {"result": result}

def make_workflow(kind: str, prompt: str, seed: int):
    env = "IMAGE_WORKFLOW" if kind == "image" else "VIDEO_WORKFLOW"
    default = ROOT / "workflows" / ("image_api.json" if kind == "image" else "video_api.json")
    path = Path(os.getenv(env, str(default)))
    if not path.exists():
        raise HTTPException(400, f"Brak workflow: {path}")
    wf = load_workflow(path)
    patch_text_node(wf, os.getenv("COMFY_POSITIVE_NODE"), prompt)
    patch_seed_node(wf, os.getenv("COMFY_SEED_NODE"), seed)
    return wf

@app.post("/api/generate/image")
async def generate_image(item: PromptIn):
    seed = item.seed if item.seed is not None else random.randint(1, 2**31-1)
    prompt = f'''{item.idea}\n{item.scene}\n{item.character}\n\nSTYLE: cinematic comic-book illustration, Katowice Silesia, handcrafted textures, dramatic but warm lighting, expressive characters, consistent Beboki designs, high detail, coherent environment, no photorealistic redesign of the characters.'''
    try:
        result = await queue_prompt(make_workflow("image", prompt, seed))
    except Exception as e:
        raise HTTPException(502, f"ComfyUI niedostępne: {e}")
    return {"prompt_id": result.get("prompt_id"), "seed": seed, "prompt": prompt}

@app.post("/api/generate/video")
async def generate_video(item: PromptIn):
    seed = item.seed if item.seed is not None else random.randint(1, 2**31-1)
    prompt = f'''{item.idea}\n{item.scene}\n{item.character}\n\nSTYLE: cinematic animated storybook, Silesian Katowice, gentle camera motion, natural character movement, warm lantern light, consistent Bebok appearance, 5–8 seconds, no text unless explicitly requested.'''
    try:
        result = await queue_prompt(make_workflow("video", prompt, seed))
    except Exception as e:
        raise HTTPException(502, f"ComfyUI niedostępne: {e}")
    return {"prompt_id": result.get("prompt_id"), "seed": seed, "prompt": prompt}

@app.get("/api/comfy/history/{prompt_id}")
async def comfy_history(prompt_id: str):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(f"{COMFY_URL}/history/{prompt_id}")
        r.raise_for_status()
        return r.json()
