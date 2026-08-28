import os
import uuid
import httpx

COMFY_URL = os.getenv("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")

async def queue_prompt(workflow: dict):
    payload = {"prompt": workflow, "client_id": str(uuid.uuid4())}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{COMFY_URL}/prompt", json=payload)
        r.raise_for_status()
        return r.json()

def patch_text_node(workflow, node_id, text):
    if not node_id:
        return
    node = workflow.get(str(node_id)) or workflow.get(node_id)
    if not node:
        return
    inputs = node.setdefault("inputs", {})
    if "text" in inputs:
        inputs["text"] = text
    elif "prompt" in inputs:
        inputs["prompt"] = text

def patch_seed_node(workflow, node_id, seed):
    if not node_id:
        return
    node = workflow.get(str(node_id)) or workflow.get(node_id)
    if node:
        node.setdefault("inputs", {})["seed"] = seed

def load_workflow(path):
    with open(path, "r", encoding="utf-8") as f:
        import json
        return json.load(f)
