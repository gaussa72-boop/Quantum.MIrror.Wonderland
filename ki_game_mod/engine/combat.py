import random

class CombatAI:
    def __init__(self, seed=42): self.rng = random.Random(seed)
    def enemy(self, level, theme="fantasy"):
        roles = ["brute", "ranger", "mage", "assassin", "beast"]
        role = self.rng.choice(roles)
        return {"id": f"enemy-{level}-{self.rng.randint(1000,9999)}", "theme": theme, "role": role,
                "level": level, "hp": 80 + level*18, "damage": 8 + level*3,
                "behavior": ["patrol", "flank", "retreat", "ambush"][level % 4]}
    def resolve(self, event):
        hp = max(1, int(event.get("player_hp", 100))); enemy_hp = max(1, int(event.get("enemy_hp", 100)))
        pd = max(1, int(event.get("player_damage", 15))); ed = max(1, int(event.get("enemy_damage", 10)))
        turns = 0
        while hp > 0 and enemy_hp > 0 and turns < 100:
            enemy_hp -= pd; turns += 1
            if enemy_hp <= 0: break
            hp -= ed
        return {"winner": "player" if hp > 0 else "enemy", "turns": turns, "player_hp": max(0,hp), "enemy_hp": max(0,enemy_hp)}
