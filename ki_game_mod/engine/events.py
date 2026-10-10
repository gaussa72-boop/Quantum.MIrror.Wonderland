import random
class EventDirector:
    def __init__(self,seed=42): self.rng=random.Random(seed)
    def generate(self,world,level=1):
        regions=(world or {}).get("regions",[])
        return {"id":f"event-{self.rng.randint(10000,99999)}","type":"dynamic_world_event","title":"Mirror Storm","level":max(1,int(level)),"region":(regions[0].get("id") if regions else "region_0"),"warning_seconds":10,"duration_seconds":45,"effects":["temporary portals","bonus shard drops"],"recoverable":True}
