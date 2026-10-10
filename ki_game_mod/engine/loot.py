import random

class LootGenerator:
    def __init__(self, seed=42): self.rng = random.Random(seed)
    def drop(self, level=1, rarity="common"):
        mult = {"common":1,"rare":1.8,"epic":3.0,"legendary":5.0}.get(rarity,1)
        return {"id": f"loot-{self.rng.randint(100000,999999)}", "rarity": rarity,
                "name": f"{rarity.title()} Relic", "level": level,
                "value": round(level*20*mult), "power": round(level*4*mult, 1)}
