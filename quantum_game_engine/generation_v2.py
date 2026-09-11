"""V2 orchestration layer: turn one idea into a complete, ordered game blueprint."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
from .dunkle_spiegel import concept_from_prompt
from .rendering import profile_for

STAGES = (
    "concept", "game_design", "gameplay", "world", "characters",
    "quests", "items", "ui", "assets", "audio", "rendering", "tests", "package",
)

@dataclass
class GenerationBlueprint:
    concept: dict[str, Any]
    game_design: dict[str, Any]
    gameplay: dict[str, Any]
    world: dict[str, Any]
    characters: dict[str, Any]
    quests: dict[str, Any]
    items: dict[str, Any]
    ui: dict[str, Any]
    assets: dict[str, Any]
    audio: dict[str, Any]
    rendering: dict[str, Any]
    tests: dict[str, Any]
    package: dict[str, Any]

class GenerationOrchestrator:
    """Produces a stable contract that code/asset/build workers can consume."""
    def build_blueprint(self, prompt: str, target: str = "web", kind: str = "game", quality: str = "4k_ultra") -> dict[str, Any]:
        concept = concept_from_prompt(prompt).to_design_document()
        return asdict(GenerationBlueprint(
            concept=concept,
            game_design={"genre": "AI-derived", "core_loop": ["explore", "discover", "create", "progress"], "original_content": True},
            gameplay={"systems": ["movement", "combat", "interaction", "inventory", "progression", "save/load"], "difficulty": "adaptive"},
            world={"generation": "procedural-ready", "biomes": ["mirror", "void", "light"], "streaming": True},
            characters={"player": "customizable avatar", "companions": [concept["systems"]["ai_companion"]], "npc_ai": "state-machine + utility scoring"},
            quests={"generator": "data-driven", "types": ["main", "side", "discovery"], "branching": True},
            items={"generator": "data-driven", "categories": ["equipment", "consumable", "artifact", "quest"], "rarity": True},
            ui={"style": "Dunkle Spiegel", "responsive": True, "accessibility": True},
            assets={"manifest": "assets/manifest.json", "original_only": True, "lod": True, "streaming": True, "placeholders": True},
            audio={"manifest": "audio/manifest.json", "adaptive_music": True, "spatial_audio_ready": True},
            rendering=profile_for(target, quality),
            tests={"static": True, "unit": True, "integration": True, "performance": True, "build_isolation": target != "web"},
            package={"artifact": kind, "target": target, "stages": list(STAGES), "release_ready": False},
        ))

    def stage_order(self) -> list[str]:
        return list(STAGES)
