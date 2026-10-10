import random
class QuestGenerator:
    def __init__(self, seed=42): self.seed = seed
    def generate(self, level=1, theme="fantasy"):
        r=random.Random(self.seed+level+len(theme)); goals=[("explore","Explore the forgotten zone"),("defeat","Defeat the emerging threat"),("collect","Recover the lost artifact"),("escort","Escort the traveler safely")]; typ,title=r.choice(goals)
        return {"id":f"quest-{self.seed}-{level}-{r.randint(1000,9999)}","title":title,"type":typ,"level":level,"theme":theme,"reward":{"xp":level*120,"gold":level*25},"status":"available"}
