# Beboki Memory

This directory is the canonical, Git-versioned knowledge layer for the Beboki world.

## Two memory systems

- `world/` — canonical facts, characters, places, episodes, relationships and timeline. Markdown is intentionally Obsidian-compatible.
- `schemas/` — machine-readable contracts used by the application.
- `adapters/` — integration boundary for Mem0/user memory and future vector search.
- `index/` — generated indexes; never treat generated indexes as canonical truth.

## Source of truth

The canonical story/world state lives in Markdown files under `world/`. The application may retrieve and summarize them, but should not silently rewrite canon.

User-specific memories are separate. They belong in the memory provider (initially Mem0) and must never be mixed into public Bebok canon.

## Design rules

1. Canon is versioned in Git.
2. Character identity is immutable unless an explicit story event changes it.
3. Every episode can reference characters, locations and previous events.
4. User memory is isolated by `user_id`.
5. Retrieval should return source paths so the agent can explain where a canon fact came from.
6. Generated video must store the episode/scene IDs and character IDs used to create it.

Obsidian stores notes as plain Markdown files in a vault, which makes this directory directly usable as an Obsidian vault or as a synchronized copy of one. citeturn0search7turn0search4

Mem0 is used as the planned long-term user/agent memory layer; its open-source version can run as a library or self-hosted server. citeturn0search0turn0search2
