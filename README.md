# 🪞 Dunkle Spiegel — Quantum AI Game Engine

Quantum Mirror Wonderland ist jetzt die **Dunkle-Spiegel-Plattform mit integrierter KI-Game-Generation-Engine**.

## 🎮 Was die Engine erzeugt

Aus einer natürlichen Idee kann das Studio ein strukturiertes **Game, DLC oder Mod** für Web, Godot, Unity oder Unreal vorbereiten.

Generation Pipeline:

`Idee → Concept → Game Design → Gameplay → Welt → Charaktere/NPCs → Quests → Items → UI → Assets → Audio → Rendering → Tests → Package`

## 🧠 Dunkle-Spiegel-Systeme

- Mirror-World / Spiegelwelten
- KI-Begleiter **Master-Kater**
- persönliche Avatar-Systeme
- prozedurale Welt- und Quest-Strukturen
- NPC-KI-Blueprints
- datengetriebene Items und Inhalte
- Game / DLC / Mod-Pipeline
- engine-agnostische Projektverträge

## 🖥️ High-End Rendering

Das Studio enthält ein `4k_ultra` Zielprofil mit 3840×2160, HDR, Raytracing, dynamischer Auflösung, Adaptive Quality, Texture Streaming, LOD, Occlusion Culling, Instancing und DLSS/FSR/XeSS-Optionen.

**Hinweis:** Zielprofile garantieren keine bestimmte FPS-Zahl. Die reale Leistung hängt von Engine, GPU, Szene, Shadern und Assets ab.

## 🚀 Game Studio

Starte den Flask-Server und öffne `/studio`.

Das Studio bietet:

1. Prompt eingeben
2. Game / DLC / Mod auswählen
3. Ziel-Engine auswählen
4. Qualitäts- und FPS-Profil wählen
5. Blueprint planen
6. KI-generiertes Projekt erzeugen
7. ZIP-Projekt herunterladen

Mit `OPENAI_API_KEY` wird die KI-gestützte Code-Architektur aktiviert; ohne Schlüssel steht ein lokaler Fallback zur Verfügung.

## 🔐 Architektur

Generierter Code wird nicht automatisch im Flask-Prozess ausgeführt. Für Godot/Unity/Unreal sind isolierte Build-Worker vorgesehen. Dadurch kann die Web-Anwendung vom späteren Build-System getrennt werden.

## 🧪 Qualitätssicherung

GitHub Actions prüft Python-Kompilierung, Game-Engine-Tests und API-Smoke-Tests.

## 📁 Zentrale Engine-Dateien

- `game_engine.py` — Code-/Projektgenerator
- `studio_api.py` — Game-Studio-API
- `quantum_game_engine/pipeline.py` — Generation Pipeline
- `quantum_game_engine/generation_v2.py` — V2-Orchestrator
- `quantum_game_engine/dunkle_spiegel.py` — Welt-/Designschicht
- `quantum_game_engine/rendering.py` — High-End Renderingprofile
- `quantum_game_engine/schemas.py` — stabile Datenverträge
- `game_studio.html/js/css` — Web Studio

## ⚠️ Aktueller Entwicklungsstand

Die Engine ist ein funktionierendes **Generator-Framework und Projekt-Scaffold**. Vollautomatische AAA-Asset-Erzeugung, native Engine-Builds und sichere Build-Worker sind separate Produktionsstufen und werden nicht als bereits fertig behauptet.
