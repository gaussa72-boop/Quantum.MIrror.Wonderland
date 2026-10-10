from dataclasses import dataclass
@dataclass
class SelfOptimizer:
    max_step: float = 0.10
    def tune(self, metric: float, target: float) -> dict:
        error=target-metric; step=max(-self.max_step,min(self.max_step,error*0.1))
        return {"metric":metric,"target":target,"proposed_step":round(step,4),"requires_review":True}
