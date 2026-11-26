# ULTIMA Game Universe Integration Contract

## Goal
Connect Quantum Mirror Wonderland, Dark Mirror Wonderland, KI Game Mod, Lichtkrieger, The Lord, Quantenformel simulations and future game engines through a shared library without merging away independent game identities or repositories.

## Canonical integration
- Quantum Mirror Wonderland remains the primary studio/API host.
- The Game Library reads a versioned manifest.
- Every game/engine retains its own runtime, repository, asset pipeline and release lifecycle.
- Cross-game identity, saves, inventory and alliances are future opt-in APIs; no shared player data is assumed until authentication and consent are implemented.

## Manifest
Each registration must declare: id, title, owner/creator, engine id/version, runtime URL/path, repository, supported features, asset formats, API contract, licence, visibility, moderation status and compatibility range.

## Current entries
See `game-library/manifest.json`. Only the Quantum Mirror routes are currently verified from the repository README. Lichtkrieger, The Lord and Quantenformel are listed as pending integration.

## Community submissions
Do not auto-publish user generated content. Require authenticated creator, explicit licence/consent, malware and content review, moderation status, versioning, takedown path and asset size limits. Private drafts must not appear in public catalogue.

## Update Matrix
Future release pipeline: discover upstream changes -> generate a proposed update -> attach sources and affected game IDs -> run build, API, gameplay and security tests -> human approval for production -> deploy -> record version, commit, tests and rollback reference in the visible Update Matrix. Never deploy generated code without review.

## Quality roadmap
1. Browser playable prototype (current): 2D top-down exploration and alliance loop.
2. Engine integration: adapt existing world, quest, NPC, combat and faction generators through documented adapters.
3. 3D vertical slice: terrain streaming, character controller, combat, NPC schedules, faction diplomacy and save system.
4. 4K target: 4K assets/output, physically based lighting, LOD/occlusion, audio, performance budgets and target-device testing.
5. Multiplayer: authoritative server, anti-cheat, persistence, moderation and privacy controls.

## Explicit status
This repository addition does not claim a finished 4K open world, production multiplayer, live integration of all listed engines, or enabled public creator uploads.
