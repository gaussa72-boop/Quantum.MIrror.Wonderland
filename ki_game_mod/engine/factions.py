class FactionSystem:
    def __init__(self): self._rep={}
    def apply(self,faction,delta=0):
        key=str(faction or "neutral")[:80]; value=max(-100,min(100,self._rep.get(key,0)+int(delta))); self._rep[key]=value
        return {"faction":key,"reputation":value,"standing":"hostile" if value<=-50 else "friendly" if value>=50 else "neutral"}
