from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Builder AI")

@app.get("/builder")
@app.get("/builder.html")
def builder():
    return FileResponse(ROOT / "builder.html", media_type="text/html")

@app.get("/api/health")
def health():
    return JSONResponse({"ok": True, "service": "builder-ai", "version": "0.1"})
