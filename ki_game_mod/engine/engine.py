import hashlib, json, random
from .models import GameState
from .quests import QuestGenerator
from .world import WorldGenerator
from .npc import NPCGenerator
from .combat import CombatAI
from .loot import LootGenerator
from .dialogue import DialogueEngine
from .balance import BalanceEngine
from .analyzer import GameAnalyzer
from .events import EventDirector
from .boss import BossAI
from .factions import FactionSystem
from .memory import GameMemory

class AIEngine:
    def __init__(self, seed: int = 42):
        self.seed=seed; self.world=WorldGenerator(seed); self.quests=QuestGenerator(seed); self.npcs=NPCGenerator(seed)
        self.combat=CombatAI(seed); self.loot=LootGenerator(seed); self.dialogue=DialogueEngine(); self.balance=BalanceEngine(); self.analyzer=GameAnalyzer()
        self.events=EventDirector(seed); self.bosses=BossAI(seed); self.factions=FactionSystem(); self.memory=GameMemory()
    def generate_mod_pack(self, theme="fantasy", level=10):
        rng=random.Random(self.seed); world=self.world.generate(theme,4)
        return {"world":world,"quests":[self.quests.generate(level,theme) for _ in range(5)],"npcs":[self.npcs.generate(level,rng.choice(["merchant","guardian","scholar","hunter"])) for _ in range(6)],"enemies":[self.combat.enemy(level+i,theme) for i in range(5)],"loot":[self.loot.drop(level+i,"rare" if i%3==0 else "common") for i in range(8)],"dynamic_event":self.events.generate(world,level),"boss":self.bosses.create(max(level,20))}
    def apply(self,state,event):
        self.memory.remember(event); kind=event.get("type")
        if kind=="combat": return self.combat.resolve(event)
        if kind=="dialogue": return self.dialogue.reply(event.get("npc",{}),event.get("message",""))
        if kind=="balance": return self.balance.recommend(state)
        if kind=="analyze": return self.analyzer.analyze(state)
        raise ValueError(f"Unknown event type: {kind}")
    @staticmethod
    def stable_id(*parts): return hashlib.sha256(json.dumps(parts,sort_keys=True).encode()).hexdigest()[:16]
