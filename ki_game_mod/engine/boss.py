import random
class BossAI:
    def __init__(self,seed=42): self.rng=random.Random(seed)
    def create(self,level=20):
        level=max(1,min(int(level),999))
        return {"id":f"boss-{self.rng.randint(10000,99999)}","name":"The Mirror Sovereign","level":level,"hp":level*500,"phases":[{"name":"Sentinel","threshold":1.0},{"name":"Reflected Fury","threshold":0.6},{"name":"Fractured Core","threshold":0.25}],"telegraph_seconds":2.0,"weakness":"exposed core after heavy attack","fairness":"telegraphed attacks; no unavoidable damage"}
