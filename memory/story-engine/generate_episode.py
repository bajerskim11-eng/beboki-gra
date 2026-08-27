import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "memory/story-engine/episode-001.json"
OUT = ROOT / "memory/story-engine/jobs"


def build_jobs():
    episode = json.loads(PLAN.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = []
    for scene in episode["scenes"]:
        jobs.append({
            "episode_id": episode["episode_id"],
            "episode_title": episode["title"],
            "scene_id": scene["id"],
            "character_id": episode["character"],
            "duration_seconds": scene["duration_seconds"],
            "provider": "nvidia",
            "prompt": scene["prompt"],
            "status": "queued"
        })
    output = OUT / "episode-001-jobs.json"
    output.write_text(json.dumps(jobs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created {len(jobs)} video jobs: {output}")


if __name__ == "__main__":
    build_jobs()
