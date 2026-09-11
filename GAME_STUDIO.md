# Quantum AI Game Studio

Quantum Mirror Wonderland now contains a prompt-driven game generation service.

## Workflow

1. Open `/studio`.
2. Describe the game, mod or DLC.
3. Select artifact type: `game`, `mod` or `dlc`.
4. Select target: `web`, `godot`, `unity` or `unreal`.
5. The backend asks the configured OpenAI model to act as game architect/programmer.
6. Generated paths and file sizes are validated before anything is written.
7. A project manifest and ZIP package are produced under `generated_games/`.
8. Download the ZIP from the generated result.

## AI configuration

Set `OPENAI_API_KEY` on the server. The model defaults to `gpt-5.6-sol` and can be changed with `OPENAI_MODEL`.

Without an API key, the system intentionally uses a deterministic local fallback so the UI remains testable.

## API

- `GET /api/generator/health`
- `POST /api/generator/generate`
- `GET /api/generator/download/<project_id>`

Example request:

```json
{
  "prompt": "A dark fantasy roguelite with three realms, a hub, procedural rooms, inventory and a final boss.",
  "kind": "game",
  "target": "godot"
}
```

## Security boundaries

Generated paths must be relative and cannot contain `..`. Individual files and the complete project have size limits. Generated output is ignored by Git. The generator does not receive GitHub write access and does not automatically execute generated code.

## Production next step

For full engine automation, add isolated build workers for Godot/Unity/Unreal, asset generation pipelines, sandboxed test execution and signed release artifacts. The current service deliberately generates and packages code without executing untrusted generated code on the web server.
