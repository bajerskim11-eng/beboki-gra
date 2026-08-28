import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = os.getenv("STUDIO_DB", "./studio.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    tags TEXT DEFAULT '',
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_memories_kind ON memories(kind);
"""

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    return c

def add(kind: str, title: str, content: str, tags=None):
    with conn() as c:
        c.execute(
            "INSERT INTO memories(kind,title,content,tags,created_at) VALUES(?,?,?,?,?)",
            (kind, title, content, ",".join(tags or []), datetime.now(timezone.utc).isoformat())
        )

def list_memories(limit=100):
    with conn() as c:
        rows = c.execute("SELECT * FROM memories ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

def search(query: str, limit=20):
    terms = [t.strip() for t in query.lower().split() if t.strip()]
    rows = list_memories(500)
    if not terms:
        return rows[:limit]
    scored = []
    for r in rows:
        hay = f"{r['title']} {r['content']} {r['tags']}".lower()
        score = sum(1 for t in terms if t in hay)
        if score:
            scored.append((score, r))
    scored.sort(key=lambda x: (-x[0], -x[1]["id"]))
    return [r for _, r in scored[:limit]]

def seed_from_canon(path="studio/story/canon.json"):
    if not Path(path).exists() or list_memories(1):
        return
    canon = json.loads(Path(path).read_text(encoding="utf-8"))
    add("canon", canon["title"], json.dumps(canon, ensure_ascii=False, indent=2), ["canon", "beboki", "katowice"])
