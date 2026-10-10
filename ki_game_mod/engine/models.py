from dataclasses import dataclass, field
from typing import Any

@dataclass
class GameState:
    player: dict[str, Any] = field(default_factory=dict)
    world: dict[str, Any] = field(default_factory=dict)
    quests: list[dict[str, Any]] = field(default_factory=list)
    entities: list[dict[str, Any]] = field(default_factory=list)
    inventory: list[dict[str, Any]] = field(default_factory=list)
    flags: dict[str, bool] = field(default_factory=dict)

@dataclass(frozen=True)
class ModManifest:
    id: str
    name: str
    version: str = "1.0.0"
    description: str = ""
    modules: tuple[str, ...] = ()
