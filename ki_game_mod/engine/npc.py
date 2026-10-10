import random

class NPCGenerator:
    PERSONALITIES = ["curious", "stern", "kind", "mysterious", "ambitious"]
    def __init__(self, seed=42): self.seed = seed
    def generate(self, level=1, role="merchant"):
        r = random.Random(self.seed + level + len(role))
        return {"id": f"npc-{self.seed}-{r.randint(10000,99999)}", "name": f"{role.title()} {r.randint(1,99)}",
                "role": role, "level": level, "personality": r.choice(self.PERSONALITIES),
                "faction": r.choice(["free", "royal", "outcast", "arcane"]), "alive": True}
