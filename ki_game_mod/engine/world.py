import random
class WorldGenerator:
    BIOMES=["forest","ruins","desert","tundra","coast","undercity"]
    def __init__(self,seed=42): self.seed=seed
    def generate(self,theme="fantasy",regions=4):
        r=random.Random(self.seed)
        return {"theme":theme,"seed":self.seed,"regions":[{"id":f"region_{i}","name":f"{theme.title()} Frontier {i+1}","biome":r.choice(self.BIOMES),"danger":r.randint(1,10),"points_of_interest":r.randint(2,6)} for i in range(regions)]}
