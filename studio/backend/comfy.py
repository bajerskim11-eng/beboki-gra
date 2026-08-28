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

def _node(workflow, node_id):
    if not node_id:
        return None
    return workflow.get(str(node_id)) or workflow.get(node_id)

def find_text_node(workflow):
    for node_id, node in workflow.items():
        if not str(node_id).isdigit() or not isinstance(node, dict):
            continue
        if node.get("class_type") in {"CLIPTextEncode", "TextEncodeQwenImageEdit", "TextEncodeQwenImage"}:
            inputs = node.get("inputs", {})
            if "text" in inputs or "prompt" in inputs:
                return node_id
    return None

def find_seed_node(workflow):
    for node_id, node in workflow.items():
        if not str(node_id).isdigit() or not isinstance(node, dict):
            continue
        if "seed" in node.get("inputs", {}):
            return node_id
    return None

def patch_text_node(workflow, node_id, text):
    node = _node(workflow, node_id) or _node(workflow, find_text_node(workflow))
    if not node:
        return False
    inputs = node.setdefault("inputs", {})
    if "text" in inputs:
        inputs["text"] = text
        return True
    if "prompt" in inputs:
        inputs["prompt"] = text
        return True
    return False

def patch_seed_node(workflow, node_id, seed):
    node = _node(workflow, node_id) or _node(workflow, find_seed_node(workflow))
    if not node:
        return False
    inputs = node.setdefault("inputs", {})
    if "seed" in inputs:
        inputs["seed"] = seed
        return True
    return False

def load_workflow(path):
    import json
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
