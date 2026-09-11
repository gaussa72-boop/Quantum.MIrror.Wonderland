"""Dunkle-Spiegel design layer: the user's creative idea becomes game systems."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass
class DunkleSpiegelConcept:
    title: str
    world: str
    player_goal: str
    mechanics: list[str]
    atmosphere: str = "dark quantum fantasy"
    companion: str = "Master-Kater"
    mirror_world: bool = True
    sacred_geometry: bool = True

    def to_design_document(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "world": self.world,
            "player_goal": self.player_goal,
            "mechanics": self.mechanics,
            "atmosphere": self.atmosphere,
            "systems": {
                "mirror_world": self.mirror_world,
                "ai_companion": self.companion,
                "sacred_geometry": self.sacred_geometry,
                "personal_avatar": True,
                "procedural_world": True,
            },
        }

def concept_from_prompt(prompt: str) -> DunkleSpiegelConcept:
    """Create a neutral design seed; an LLM can refine it later."""
    text = prompt.strip()
    return DunkleSpiegelConcept(
        title=(text.split(".")[0] or "Dunkle Spiegel").strip()[:80],
        world="A reactive mirror-world shaped by the player's idea.",
        player_goal="Explore, create, and transform the generated world.",
        mechanics=["exploration", "AI-driven encounters", "world transformation", "progression"],
    )
