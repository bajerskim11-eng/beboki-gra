# BEBOKI — TECH ARCHITECTURE

## Target stack
- Phaser 4 + TypeScript
- Vite
- Tiled for authored 2D maps
- Vercel for web deployment
- Shopify CDN only for approved existing character/media assets where practical
- Supabase later for auth + persistent player state

## Structure
src/
  game/
    scenes/
      BootScene
      PreloadScene
      SettlementScene
      WorldMapScene
      MissionScene
      RewardScene
    entities/
      Bebok
      Dog
      Building
    systems/
      MissionSystem
      QuestSystem
      InventorySystem
      SaveSystem
      PathfindingSystem
    data/
      characters
      missions
      buildings

## Scene flow
Boot → Preload → Settlement
Settlement → WorldMap
WorldMap → Mission
Mission → Reward
Reward → Settlement

## Core architecture rule
Game state must not live inside DOM event handlers. UI renders from a central game/player state. This prevents the current prototype from becoming unmaintainable.

## First technical milestone
Build one playable MissionScene with:
- a Tiled map
- collision layer
- four Bebok entities
- click/touch selection
- basic pathfinding
- one interactive obstacle per Bebok
- dog entity
- win condition
- restart

## Assets
Do not depend on remote Shopify images for core gameplay indefinitely. For production, copy/optimize approved assets into the game asset pipeline so gameplay is not broken by external CDN changes/CORS.

## Backend boundary
Frontend:
- rendering
- input
- gameplay simulation
- temporary local state

Supabase later:
- users
- profiles
- save slots
- settlement state
- inventory
- mission completion
- social data

Never expose private API keys in client code.
