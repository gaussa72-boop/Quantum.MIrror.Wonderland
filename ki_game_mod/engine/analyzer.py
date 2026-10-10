class GameAnalyzer:
    def analyze(self, state):
        p = state.player or {}; inv = state.inventory or []
        return {"player_level": p.get("level", 1), "deaths": p.get("deaths", 0),
                "kills": p.get("kills", 0), "inventory_size": len(inv),
                "active_quests": sum(1 for q in state.quests if q.get("status") in ("available","active")),
                "recommendations": ["Keep quests within 3 levels of the player.", "Reward exploration with varied loot."]}
