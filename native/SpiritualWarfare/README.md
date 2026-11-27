# Spiritual Warfare — Unreal Engine 5.6 native starter

This is the native C++ project foundation for the Astralis open-world RPG. It is separate from the Flask/Render orchestration service.

## Open locally

1. Install Unreal Engine 5.6 through Epic Games Launcher.
2. Open `SpiritualWarfare.uproject` and allow Unreal to generate project files.
3. Build the `SpiritualWarfareEditor` target in Visual Studio 2022 with the matching C++ workload.
4. Open the project in Unreal Editor and create the initial map at `Content/Maps/L_MainWorld`.
5. Add landscape, world-partition settings, lighting, player controller, input assets, original character/creature assets and animation blueprints.

## Included foundation

- UE 5.6 C++ game and editor targets.
- Runtime game module and game mode.
- Blueprint-callable Astralis world subsystem.
- Deterministic seeded region profiles with five fantasy biomes.
- NPC profile registry with stable character IDs, faction, disposition and memory summary.
- Starter renderer configuration for Lumen, virtual shadow maps and texture streaming.

## Production boundaries

The repository does not contain finished AAA art, voice acting, mocap, a complete gameplay loop, multiplayer persistence or an Xbox package. Those require content production, Unreal Editor builds, performance profiling and platform-holder approval/SDK access. A 4K preset is a target, not a measured performance guarantee.

## Build

On a Windows machine with UE 5.6 installed:

```powershell
& "$env:UE_ROOT\Engine\Build\BatchFiles\Build.bat" SpiritualWarfareEditor Win64 Development "$PWD\SpiritualWarfare.uproject" -WaitMutex
```

The optional self-hosted GitHub Actions build requires a Windows runner tagged `unreal-engine-5` with UE 5.6 installed and `UE_ROOT` configured.
