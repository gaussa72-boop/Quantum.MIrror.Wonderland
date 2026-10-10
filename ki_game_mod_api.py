"""Flask adapter exposing the merged KI Game Mod engine."""
from flask import jsonify, request
from ki_game_mod.engine import AIEngine, GameState
from ki_game_mod.engine.events import EventDirector
from ki_game_mod.engine.boss import BossAI
from ki_game_mod.engine.factions import FactionSystem
from ki_game_mod.engine.memory import GameMemory
from ki_game_mod.engine.ai_service import AIService

def register_ki_game_mod_routes(app):
    engine = AIEngine(seed=42)
    director = EventDirector(seed=42)
    boss = BossAI(seed=42)
    factions = FactionSystem()
    memory = engine.memory
    ai = AIService()

    @app.get("/api/ki-game-mod/health")
    def ki_game_mod_health():
        return jsonify({"ok": True, "name": "KI Game Mod", "version": "merged-1.2", "provider": "offline-template", "engine": "Quantum Mirror Wonderland"})

    @app.post("/api/ki-game-mod/mods/generate")
    def ki_game_mod_generate():
        data = request.get_json(silent=True) or {}
        theme = str(data.get("theme") or "fantasy")[:80]
        try:
            level = max(1, min(999, int(data.get("level", 10))))
            return jsonify(engine.generate_mod_pack(theme, level))
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/world")
    def ki_game_mod_world():
        data = request.get_json(silent=True) or {}
        theme = str(data.get("theme") or "fantasy")[:80]
        try:
            regions = max(1, min(20, int(data.get("regions", 4))))
            return jsonify(engine.world.generate(theme, regions))
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/quest")
    def ki_game_mod_quest():
        data = request.get_json(silent=True) or {}
        try:
            level = max(1, min(999, int(data.get("level", 1))))
            return jsonify(engine.quests.generate(level, str(data.get("theme") or "fantasy")[:80]))
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/npc")
    def ki_game_mod_npc():
        data = request.get_json(silent=True) or {}
        try:
            level = max(1, min(999, int(data.get("level", 1))))
            role = str(data.get("role") or "merchant")[:60]
            return jsonify(engine.npcs.generate(level, role))
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/combat")
    def ki_game_mod_combat():
        data = request.get_json(silent=True) or {}
        if data.get("action") == "resolve":
            return jsonify(engine.combat.resolve(data))
        try:
            level = max(1, min(999, int(data.get("level", 1))))
            return jsonify(engine.combat.enemy(level, str(data.get("theme") or "fantasy")[:80]))
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/loot")
    def ki_game_mod_loot():
        data = request.get_json(silent=True) or {}
        try:
            level = max(1, min(999, int(data.get("level", 1))))
            rarity = str(data.get("rarity") or "common")
            if rarity not in {"common", "rare", "epic", "legendary"}:
                return jsonify({"error": "Unsupported rarity"}), 400
            return jsonify(engine.loot.drop(level, rarity))
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/boss")
    def ki_game_mod_boss():
        data = request.get_json(silent=True) or {}
        try:
            level = max(1, min(999, int(data.get("level", 20))))
            return jsonify(boss.create(level))
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/events")
    def ki_game_mod_event():
        data = request.get_json(silent=True) or {}
        event_type = str(data.get("type") or "")
        event_data = data.get("data") if isinstance(data.get("data"), dict) else {}
        try:
            result = engine.apply(GameState(), {"type": event_type, **event_data})
            memory.remember({"type": event_type, "data": event_data})
            return jsonify({"result": result})
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/director/event")
    def ki_game_mod_director_event():
        data = request.get_json(silent=True) or {}
        try:
            level = max(1, min(999, int(data.get("level", 10))))
            world = engine.world.generate(str(data.get("theme") or "fantasy")[:80], 4)
            return jsonify(director.generate(world, level))
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/factions/<faction>")
    def ki_game_mod_faction(faction):
        data = request.get_json(silent=True) or {}
        try:
            delta = max(-100, min(100, int(data.get("delta", 0))))
            return jsonify(factions.apply(faction, delta))
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/ki-game-mod/ai")
    def ki_game_mod_ai():
        data = request.get_json(silent=True) or {}
        prompt = str(data.get("prompt") or "").strip()
        if not prompt:
            return jsonify({"error": "prompt is required"}), 400
        if len(prompt) > 12000:
            return jsonify({"error": "prompt is too long"}), 413
        context = data.get("context") if isinstance(data.get("context"), dict) else {}
        return jsonify(ai.generate(prompt, context))

    @app.get("/api/ki-game-mod/memory")
    def ki_game_mod_memory():
        return jsonify({"events": memory.recent(), "count": len(memory.recent())})
