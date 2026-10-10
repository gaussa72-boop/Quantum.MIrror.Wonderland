from collections import deque
class GameMemory:
    def __init__(self,limit=100): self._events=deque(maxlen=limit)
    def remember(self,event): self._events.append(dict(event or {}))
    def recent(self): return list(self._events)
