"""Quantum Game Engine: prompt-to-game, DLC and mod generation."""
from __future__ import annotations
import json, os, re, uuid, zipfile
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")

class GameGenerationError(Exception):
    pass

class QuantumGameEngine:
    """Engine-agnostic project generator with optional LLM-backed code generation."""
    def __init__(self, output_dir: str = "generated_games"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    def _safe_name(self, value: str, default: str = "quantum-game") -> str:
        value = SAFE_NAME.sub("-", (value or "").strip()).strip("-.")
        return (value[:64] or default).lower()

    def _system_prompt(self) -> str:
        return """You are Quantum Game Engine, a senior game architect and programmer. Turn a user's game, DLC or mod idea into a small, coherent, runnable project scaffold. Return ONLY valid JSON: {\"name\":string,\"description\":string,\"files\":[{\"path\":string,\"content\":string}],\"next_steps\":[string]}. Never use absolute paths, .., secrets, credentials, malware, exploit code, or copyrighted game assets. Prefer original code and placeholder assets. Keep files focused and runnable."""

    def _llm(self, prompt: str, target: str, kind: str) -> dict[str, Any] | None:
        key = os.getenv("OPENAI_API_KEY")
        if not key or OpenAI is None:
            return None
        client = OpenAI(api_key=key)
        request = f"Target: {target}\nArtifact type: {kind}\nUser idea:\n{prompt}"
        try:
            response = client.responses.create(model=self.model, instructions=self._system_prompt(), input=request)
            text = getattr(response, "output_text", "")
            data = json.loads(text)
            if not isinstance(data, dict) or not isinstance(data.get("files"), list):
                return None
            return data
        except Exception:
            return None

    def _fallback(self, prompt: str, target: str, kind: str) -> dict[str, Any]:
        name = self._safe_name(prompt.split()[0] if prompt.split() else "quantum-game")
        if target.lower() == "godot":
            files = {
                "project.godot": """[application]\nconfig/name=\"Quantum Generated Game\"\nrun/main_scene=\"res://main.tscn\"\n[display]\nwindow/size/viewport_width=1280\nwindow/size/viewport_height=720\n[rendering]\nrenderer/rendering_method=\"gl_compatibility\"\n""",
                "main.tscn": """[gd_scene load_steps=2 format=3]\n\n[ext_resource path=\"res://main.gd\" type=\"Script\" id=\"1\"]\n\n[node name=\"Main\" type=\"Node2D\"]\nscript = ExtResource(\"1\")\n""",
                "main.gd": """extends Node2D\n\nfunc _ready():\n    print(\"Quantum Game Engine generated project: " + str(%s) + \"\")\n\nfunc _process(delta):\n    queue_redraw()\n\nfunc _draw():\n    draw_circle(Vector2(640,360), 110, Color(0.8,0.7,1.0,0.25))\n    draw_string(ThemeDB.fallback_font, Vector2(470,360), \"QUANTUM GENERATED GAME\")\n""" % json.dumps(prompt),
            }
        elif target.lower() == "unity":
            files = {
                "Assets/Scripts/QuantumGameBootstrap.cs": """using UnityEngine;\npublic class QuantumGameBootstrap : MonoBehaviour {\n    void Start() { Debug.Log(\"Quantum Game Engine generated project\"); }\n}\n""",
                "Assets/Scenes/GeneratedGame.unity": "# Placeholder Unity scene. Open the project and attach QuantumGameBootstrap to a GameObject.\n",
                "README.md": "# Quantum Generated Unity Game\n\nGenerated from a prompt. Add original assets and configure the scene in Unity.\n",
            }
        elif target.lower() == "unreal":
            files = {
                "Source/QuantumGeneratedGame/QuantumGeneratedGame.Build.cs": "using UnrealBuildTool;\npublic class QuantumGeneratedGame : ModuleRules { public QuantumGeneratedGame(ReadOnlyTargetRules Target) : base(Target) { PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs; } }\n",
                "Source/QuantumGeneratedGame/QuantumGeneratedGame.cpp": "#include \"Modules/ModuleManager.h\"\nIMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, QuantumGeneratedGame, \"QuantumGeneratedGame\");\n",
                "README.md": "# Quantum Generated Unreal Project\n\nScaffold generated from a prompt; add project-specific assets and maps in Unreal Editor.\n",
            }
        else:
            files = {
                "index.html": "<!doctype html><html><head><meta charset='utf-8'><title>Quantum Generated Game</title></head><body><canvas id='game' width='1280' height='720'></canvas><script src='game.js'></script></body></html>\n",
                "game.js": "const c=document.getElementById('game'),x=c.getContext('2d'); let t=0; function loop(){t+=.016;x.clearRect(0,0,c.width,c.height);x.beginPath();x.arc(640+Math.cos(t)*180,360+Math.sin(t)*100,50,0,7);x.fillStyle='#b98cff';x.fill();x.fillStyle='white';x.font='28px sans-serif';x.fillText('QUANTUM GENERATED GAME',470,360);requestAnimationFrame(loop)} loop();\n",
                "README.md": "# Quantum Generated Web Game\n\nPrompt: " + prompt.replace("\n", " ") + "\n",
            }
        if kind == "mod":
            files["mod/manifest.json"] = json.dumps({"id": name, "type": "mod", "version": "1.0.0", "description": prompt}, indent=2)
            files["mod/README.md"] = "# Generated Mod\n\nThis is an engine-neutral mod scaffold. Connect the adapter for your target game.\n"
        elif kind == "dlc":
            files["dlc/content.json"] = json.dumps({"id": name + "-dlc", "type": "dlc", "title": name.replace("-", " ").title(), "idea": prompt, "content": ["new area", "new quest", "new rewards"]}, indent=2)
        return {"name": name, "description": f"Generated {kind} scaffold for {target}.", "files": [{"path": p, "content": c} for p,c in files.items()], "next_steps": ["Open the project in the target engine.", "Replace placeholders with original assets.", "Run the project's tests/build pipeline."]}

    def generate(self, prompt: str, target: str = "web", kind: str = "game") -> dict[str, Any]:
        prompt = (prompt or "").strip()
        if len(prompt) < 3:
            raise GameGenerationError("Prompt is too short.")
        target = (target or "web").lower()
        kind = (kind or "game").lower()
        if target not in {"web", "godot", "unity", "unreal"}:
            raise GameGenerationError("Unsupported target engine.")
        if kind not in {"game", "mod", "dlc"}:
            raise GameGenerationError("Unsupported artifact type.")
        data = self._llm(prompt, target, kind) or self._fallback(prompt, target, kind)
        files = []
        for item in data.get("files", []):
            path = str(item.get("path", "")).replace("\\", "/").lstrip("/")
            if not path or ".." in Path(path).parts:
                continue
            content = str(item.get("content", ""))
            if len(content) > 300_000:
                content = content[:300_000]
            files.append({"path": path, "content": content})
        if not files:
            raise GameGenerationError("Generator returned no safe files.")
        project_id = uuid.uuid4().hex[:12]
        root = self.output_dir / project_id
        root.mkdir(parents=True, exist_ok=True)
        for item in files:
            destination = root / item["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(item["content"], encoding="utf-8")
        manifest = {"id": project_id, "created_at": datetime.now(timezone.utc).isoformat(), "kind": kind, "target": target, "prompt": prompt, "files": [f["path"] for f in files]}
        (root / "quantum.manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        zip_path = self.output_dir / f"{project_id}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for item in root.rglob("*"):
                if item.is_file():
                    archive.write(item, item.relative_to(root))
        return {"id": project_id, "name": data.get("name", project_id), "description": data.get("description", ""), "kind": kind, "target": target, "files": [f["path"] for f in files], "next_steps": data.get("next_steps", []), "download": f"/api/generator/download/{project_id}"}

    def download_path(self, project_id: str) -> Path:
        if not re.fullmatch(r"[a-f0-9]{12}", project_id):
            raise GameGenerationError("Invalid project id.")
        path = self.output_dir / f"{project_id}.zip"
        if not path.is_file():
            raise GameGenerationError("Generated project not found.")
        return path
