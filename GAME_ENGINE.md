# Quantum Game Engine

Quantum Mirror Wonderland now contains a practical prompt-to-project pipeline.

## Capabilities
- **Game generation:** prompt -> project scaffold -> ZIP.
- **DLC generation:** creates a content manifest and target-engine scaffold.
- **Mod generation:** creates a mod manifest and adapter-ready structure.
- **Targets:** Web, Godot, Unity and Unreal scaffolds.
- **AI mode:** when `OPENAI_API_KEY` is configured, the backend asks an OpenAI model for a JSON file plan and code. The server validates paths and file sizes before writing.
- **Local mode:** without an API key, deterministic templates still produce a runnable starter project.

## Run
```bash
pip install -r requirements.txt
python app.py
```
Open `/studio`.

## Environment
`OPENAI_API_KEY` enables LLM-backed generation.
`OPENAI_MODEL` optionally selects the model; the default is `gpt-5-mini`.
`CORS_ORIGINS` controls CORS origins.

## Important boundary
The engine generates original project code and generic adapters. A game-specific mod/DLC can require the original game's official SDK, mod loader, file formats and license. The generator does not bypass DRM, anti-cheat or access controls.
