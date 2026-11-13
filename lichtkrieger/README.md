# LICHTKRIEGER — Cloud Gaming Universe

A standalone browser portal and creator dashboard, deployed from the `lichtkrieger/` directory.

## Current MVP
- Responsive dark-fantasy gaming portal.
- Game discovery cards and launch link to the existing Dark Mirror HTML5 game.
- Game concept builder that calls the Quantum Mirror KI Game Mod world endpoint when CORS/API access is available; otherwise it saves a local draft.
- Local project metadata import for JSON and HTML; ZIP file metadata only (not unpacked or executed).
- Engine URL setting and JSON concept export.
- Local profile and premium-interest preview.
- Admin console blueprint for owner `gaussa72@gmail.com`.

## Deploy on Render
Create a Static Site using this repository and branch `main`.
- Build command: `echo "Lichtkrieger static portal ready"`
- Publish directory: `lichtkrieger`

## Important production requirements
This is a browser portal MVP, not a GPU streaming farm. Real cloud streaming for native/AAA games requires remote GPU workers, a streaming protocol such as WebRTC, session orchestration, queueing, monitoring, and a separately provisioned GPU runtime. HTML5/WebGL builds can run in the browser when their assets and runtime are published.

Profiles and preferences in this MVP are stored in the visitor's browser only. There is no server-side authentication, authoritative admin role, database, billing provider, multiplayer service, or persistent cross-device library yet. Never treat client-side state as an authorization mechanism. Before opening public registrations or paid memberships, add secure server-side identity, role checks, database persistence, rate limits, and payment webhooks.

## Existing engine integration points
- Quantum Mirror Engine: `https://quantum-mirror-wonderland.onrender.com`
- Existing Dark Mirror browser game: `/dark-mirror-game/`
- KI Game Mod world generation: `POST /api/ki-game-mod/world`

The engine must allow the portal origin via CORS for browser-side API requests. Do not put private API keys or admin credentials in this static frontend.
