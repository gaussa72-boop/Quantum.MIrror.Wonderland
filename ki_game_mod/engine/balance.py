class BalanceEngine:
    def recommend(self, state):
        player = state.player or {}
        level = max(1, int(player.get("level", 1)))
        deaths = int(player.get("deaths", 0)); kills = int(player.get("kills", 0))
        ratio = deaths / max(1, kills)
        if ratio > 1.5: difficulty = "easy"
        elif ratio < 0.25: difficulty = "hard"
        else: difficulty = "normal"
        return {"suggested_difficulty": difficulty, "enemy_damage_multiplier": {"easy":.8,"normal":1.0,"hard":1.15}[difficulty], "player_level": level}
