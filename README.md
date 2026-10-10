# Quantum Mirror Wonderland — Dunkle Spiegel KI Game Engine

Kanonische Python-Game-Studio-Anwendung. Sie vereint das bestehende Quantum Game Studio, das Dark Mirror HTML5-Spiel und die modularen KI-Game-Mod-Generatoren.

## Integrierte Oberflächen
- `/studio` — Game/DLC/Mod Blueprint und Projektgenerator
- `/dark-mirror-game/` — integriertes HTML5-Canvas-Spiel
- `/dark-mirror-game/ki-game-mod.html` — KI Game Mod Studio mit 12 Modulen
- `/health` — Dienststatus

## KI Game Mod API
- `GET /api/ki-game-mod/health`
- `POST /api/ki-game-mod/mods/generate`
- `POST /api/ki-game-mod/world`
- `POST /api/ki-game-mod/quest`
- `POST /api/ki-game-mod/npc`
- `POST /api/ki-game-mod/combat`
- `POST /api/ki-game-mod/loot`
- `POST /api/ki-game-mod/boss`
- `POST /api/ki-game-mod/events`
- `POST /api/ki-game-mod/director/event`
- `POST /api/ki-game-mod/factions/<faction>`
- `POST /api/ki-game-mod/ai`
- `GET /api/ki-game-mod/memory`

The merged mod engine uses deterministic/offline generation by default and never executes generated code. The frontend keeps local draft fallback behavior if the backend is unavailable.

## Start / deploy
```bash
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:$PORT app:app
```

Set `OPENAI_API_KEY` only in Render environment variables if the optional remote AI is required. Do not commit secrets. Target FPS and quality presets are goals, not hardware performance guarantees.

## Source lineage
- `QUANTUM-MIRROR-DARK-WONDERLAND`: browser game and KI Game Mod frontend copied into `dark_mirror_game/`.
- `KI-Game-Mod`: modular generators copied into `ki_game_mod/engine/` and exposed through `ki_game_mod_api.py`.
- `Quantum.MIrror.Wonderland`: existing Flask API, pipeline and generation workflow retained as the primary backend.
