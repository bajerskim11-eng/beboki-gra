from fastapi import FastAPI

app = FastAPI(title="Builder AI API")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "builder-ai"}
