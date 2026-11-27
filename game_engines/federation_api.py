"""Safe federation registry and orchestration API for Quantum Mirror game engines.

Remote adapters are read-only health probes until a documented API contract exists.
Quantum KI Ultra is used as an optional AI design-planning adapter; local deterministic
gameplay generators remain the source of structured world modules.
"""
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from flask import jsonify, request

ENGINES = [
    {"id":"quantum-mirror","name":"Quantum Mirror Wonderland","kind":"orchestrator","repository":"gaussa72-boop/Quantum.MIrror.Wonderland","url":"https://quantum-mirror-wonderland.onrender.com","health_path":"/health","adapter":"native-local-api","capabilities":["world","quest","npc","boss","combat","loot","director","mods","game-library"]},
    {"id":"quantum-ultra","name":"Quantum KI Ultra Pro V2","kind":"ai-design-engine","repository":"gaussa72-boop/Quantum.KI.Ultra.Pro.V2","url":"https://quantum-ki-ultra-pro-v2.onrender.com","health_path":"/health","adapter":"openai-compatible-chat-api","capabilities":["ai-game-design","worldbuilding","systems-design","quest-design","technical-planning"]},
    {"id":"ki-game-mod","name":"KI Game Mod","kind":"generation-engine","repository":"gaussa72-boop/KI-Game-Mod","url":"https://ki-game-mod.onrender.com","health_path":"/health","adapter":"standalone-api","capabilities":["world","quest","npc","boss","combat","loot","director","mods"]},
    {"id":"the-lord","name":"THE LORD","kind":"agent-network","repository":"gaussa72-boop/The-Lord","url":"https://the-lord-agent-network.onrender.com","health_path":"/health","adapter":"agent-network-api","capabilities":["agent-routing","worldbuilding","game-studio"]},
    {"id":"lichtkrieger","name":"LICHTKRIEGER","kind":"game-content","repository":"gaussa72-boop/Lichtkrieger","url":"https://lichtkrieger-dark-mirror-realms.onrender.com","health_path":"/","adapter":"static-content-pending-game-api","capabilities":["realms","characters","combat-prototype"]},
    {"id":"dark-wonderland","name":"Quantum Mirror Dark Wonderland","kind":"game-content","repository":"gaussa72-boop/QUANTUM-MIRROR-DARK-WONDERLAND","url":"https://quantum-mirror-dark-wonderland-ejc3.onrender.com","health_path":"/","adapter":"static-content-pending-game-api","capabilities":["browser-game","mirror-world"]},
    {"id":"neuroforge","name":"Neuroforge Systems","kind":"creative-content","repository":"gaussa72-boop/Neuroforge","url":"https://neuroforge-2035.onrender.com","health_path":"/","adapter":"static-content-pending-game-api","capabilities":["creative-concepts","visual-direction"]}
]

GENERATION_PATHS = {
    "world": "/api/ki-game-mod/world",
    "quest": "/api/ki-game-mod/quest",
    "npc": "/api/ki-game-mod/npc",
    "boss": "/api/ki-game-mod/boss",
    "combat": "/api/ki-game-mod/combat",
    "loot": "/api/ki-game-mod/loot",
    "director": "/api/ki-game-mod/director/event",
    "mods": "/api/ki-game-mod/mods/generate"
}

def _probe(engine):
    url = engine["url"].rstrip("/") + engine["health_path"]
    req = urllib.request.Request(url, headers={"User-Agent":"Astralis-Game-Federation/1.1","Accept":"application/json,text/html"})
    try:
        with urllib.request.urlopen(req, timeout=4) as response:
            payload = {}
            if "json" in response.headers.get("Content-Type", ""):
                try: payload = json.loads(response.read().decode("utf-8"))
                except (ValueError, UnicodeDecodeError): pass
            return {"status":"reachable" if 200 <= response.status < 400 else "unhealthy",
                    "http_status":response.status,"ai_configured":payload.get("openai_configured"),
                    "checked_at":datetime.now(timezone.utc).isoformat()}
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"status":"unreachable","error":str(exc)[:180],
                "checked_at":datetime.now(timezone.utc).isoformat()}

def _quantum_ultra_design(idea, style, level, regions):
    """Ask the separately deployed Quantum KI Ultra service for a design brief."""
    base = os.getenv("QUANTUM_ULTRA_API_URL", "https://quantum-ki-ultra-pro-v2.onrender.com").rstrip("/")
    prompt = (
        "Erstelle einen konkreten Game-Design- und Produktionsentwurf für das Spiel Spiritual Warfare. "
        "Antworte auf Deutsch, strukturiert mit Weltidentität, Biomen, Fraktionen, Charakter-Archetypen, "
        "NPC-Verhalten, Quest-Arcs, dynamischen Ereignissen, Boss-Phasen, Progression, Barrierefreiheit "
        "und einem realistischen technischen Produktionsplan. Keine Behauptung, dass Assets oder Builds "
        "bereits erstellt wurden. Kennzeichne Vorschläge als Designentwurf.\n"
        f"Stil: {style}\nLevel: {level}\nRegionen: {regions}\nIdee: {idea[:5000]}"
    )
    body = json.dumps({"message":prompt,"history":[]}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(base + "/api/chat", data=body,
        headers={"Content-Type":"application/json","Accept":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=28) as response:
            data = json.loads(response.read().decode("utf-8"))
            if response.status >= 400 or not data.get("ok") or not data.get("reply"):
                return {"status":"unavailable","reason":data.get("error","AI design adapter returned no answer")}
            return {"status":"generated","engine":"Quantum KI Ultra Pro V2",
                    "model":data.get("model"),"provider":data.get("provider"),
                    "design_brief":data["reply"]}
    except (urllib.error.URLError, TimeoutError, ValueError, UnicodeDecodeError) as exc:
        return {"status":"unavailable","reason":str(exc)[:220]}

def register_game_engine_federation(app):
    @app.get("/api/game-engines/federation")
    def game_engine_federation():
        return jsonify({"schema":"astralis.engine-federation.v1","primary":"quantum-mirror",
                        "strategy":"adapter-based; independent repositories preserved",
                        "engines":ENGINES,"native_build_verified":False,
                        "note":"Registered engines are not automatically API-connected. Quantum KI Ultra is an optional design adapter; native game builds require a separate engine toolchain."})

    @app.get("/api/game-engines/health")
    def game_engine_health():
        return jsonify({"checked_at":datetime.now(timezone.utc).isoformat(),
                        "engines":[{**engine,"probe":_probe(engine)} for engine in ENGINES]})

    @app.post("/api/game-engines/generate")
    def game_engine_generate():
        body=request.get_json(silent=True) or {}
        idea=str(body.get("idea") or "").strip()
        if not idea or len(idea)>6000:
            return jsonify({"error":"idea is required and must be at most 6000 characters"}),400
        try:
            level=max(1,min(999,int(body.get("level",20))))
            regions=max(1,min(20,int(body.get("regions",4))))
        except (TypeError,ValueError):
            return jsonify({"error":"level and regions must be integers"}),400
        style=str(body.get("style") or "Mythic Science Fantasy")[:80]
        theme=style+" · "+idea[:500]
        common={"theme":theme,"level":level}
        jobs={
            "world":{**common,"regions":regions},
            "quest":common,
            "npc":{"role":"Wächter / Verbündeter","level":level},
            "boss":{"level":level},
            "combat":common,
            "loot":{"level":level,"rarity":"legendary"},
            "director":common,
            "mods":common
        }
        generated={}
        client=app.test_client()
        for key,path in GENERATION_PATHS.items():
            response=client.post(path,json=jobs[key])
            try: payload=response.get_json()
            except Exception: payload={"error":"Generator returned non-JSON"}
            generated[key]=payload if response.status_code < 400 else {"error":payload or "generator failed","http_status":response.status_code}
        successful=sum(1 for value in generated.values() if not (isinstance(value,dict) and value.get("error")))
        ai_design=_quantum_ultra_design(idea,style,level,regions)
        result={"schema":"astralis.game-world.v1","project":"Spiritual Warfare",
                "created_at":datetime.now(timezone.utc).isoformat(),"idea":idea,
                "style":style,"quality_target":body.get("quality_target") or "AAA-4K-target",
                "generation":{"requested":len(generated),"succeeded":successful,"modules":generated},
                "ai_design":ai_design,
                "release_lifecycle":{"mode":"versioned-content-roadmap","post_release_updates":"requires persisted build pipeline and human QA approval"},
                "status":"blueprint_generated" if successful==len(generated) else "partial_generation",
                "native_engine_build":"not_created"}
        return jsonify(result), (200 if successful else 502)
