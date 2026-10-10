class DialogueEngine:
    def reply(self, npc, message):
        personality = npc.get("personality", "neutral")
        msg = message.lower().strip()
        if any(x in msg for x in ["hello", "hi", "hallo"]):
            return f"Greetings, traveler. A {personality} soul can always find a path forward."
        if "quest" in msg or "mission" in msg:
            return "There is work nearby. Ask about the frontier, the threat, or the lost relic."
        if "help" in msg:
            return "Tell me what you need, and I will point you toward the next useful step."
        return "Interesting. The world changes with every choice you make."
