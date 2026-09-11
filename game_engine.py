"""Quantum Game Engine: prompt-to-game, DLC and mod generation."""
from __future__ import annotations

import json, os, re, uuid, zipfile
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

try:
    from openai import OpenAI
except Exception:  # optional dependency for local fallback mode
    OpenAI = None

SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")
PROJECT_ID = re.compile(r"^[a-f0-9]{12}$")
ALLOWED_TARGETS = {"web", "godot", "unity", "unreal"}
ALLOWED_KINDS = {"game", "mod", "dlc"}
MAX_FILES = 80
MAX_FILE_BYTES = 300_000
MAX_TOTAL_BYTES = 8_000_000
MAX_PROMPT = 16_000

class GameGenerationError(Exception):
    """Expected, user-facing generation error."""

class QuantumGameEngine:
    """Engine-agnostic generator with an optional OpenAI-backed code architect."""
    def __init__(self, output_dir: str = "generated_games"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")

    @staticmethod
    def _safe_name(value: str, default: str = "quantum-game") -> str:
        value = SAFE_NAME.sub("-", (value or "").strip()).strip("-.")
        return (value[:64] or default).lower()

    @staticmethod
    def _safe_path(value: str) -> str:
        path = value.replace("\\", "/").strip()
        if not path or path.startswith("/") or re.match(r"^[A-Za-z]:", path):
            raise GameGenerationError("Generated file path is unsafe.")
        parts = Path(path).parts
        if ".." in parts or "\x00" in path:
            raise GameGenerationError("Generated file path is unsafe.")
        return path

    def _system_prompt(self) -> str:
        return """You are Quantum AI Game Studio, a senior game architect, gameplay programmer and technical designer.
Transform the user's idea into an ORIGINAL, coherent, runnable game, DLC or mod project.
Return ONLY JSON with this exact shape:
{"name":string,"description":string,"files":[{"path":string,"content":string}],"next_steps":[string],"test_plan":[string]}
Rules: relative paths only; no '..', absolute paths, secrets, credentials, private keys, malware, destructive shell commands, copyrighted game assets or instructions to bypass another game's protections. Use original placeholder assets. For mods, create an engine-neutral adapter/API boundary unless a target modding API is explicitly supplied. For DLC, create content manifests and integration points. Keep code focused and runnable. Maximum 80 files."""

    def _llm(self, prompt: str, target: str, kind: str) -> dict[str, Any] | None:
        key = os.getenv("OPENAI_API_KEY")
        if not key or OpenAI is None:
            return None
        client = OpenAI(api_key=key)
        request = f"Target: {target}\nArtifact type: {kind}\nUser idea:\n{prompt}"
        try:
            response = client.responses.create(
                model=self.model,
                instructions=self._system_prompt(),
                input=request,
            )
            text = getattr(response, "output_text", "")
            data = json.loads(text)
            return data if isinstance(data, dict) else None
        except Exception:
            # A generation failure must never expose provider credentials or a traceback.
            return None

    def _fallback(self, prompt: str, target: str, kind: str) -> dict[str, Any]:
        name = self._safe_name("-".join(prompt.split()[:4]))
        if target == "godot":
            files = {
                "project.godot": """[application]\nconfig/name=\"Quantum Generated Game\"\nrun/main_scene=\"res://main.tscn\"\n[display]\nwindow/size/viewport_width=1280\nwindow/size/viewport_height=720\n[rendering]\nrenderer/rendering_method=\"gl_compatibility\"\n""",
                "main.tscn": """[gd_scene load_steps=2 format=3]\n\n[ext_resource path=\"res://main.gd\" type=\"Script\" id=\"1\"]\n\n[node name=\"Main\" type=\"Node2D\"]\nscript = ExtResource(\"1\")\n""",
                "main.gd": """extends Node2D\n\nfunc _ready():\n    queue_redraw()\n\nfunc _draw():\n    draw_circle(Vector2(640, 360), 110, Color(0.55, 0.35, 0.95, 0.55))\n    draw_string(ThemeDB.fallback_font, Vector2(500, 360), \"QUANTUM GENERATED GAME\")\n""",
            }
        elif target == "unity":
            files = {
                "Assets/Scripts/QuantumGameBootstrap.cs": "using UnityEngine;\npublic sealed class QuantumGameBootstrap : MonoBehaviour { void Start() { Debug.Log(\"Quantum Game Engine ready\"); } }\n",
                "README.md": "# Quantum Generated Unity Project\nOpen in Unity, create a scene, add a GameObject and attach QuantumGameBootstrap.\n",
            }
        elif target == "unreal":
            files = {
                "Source/QuantumGeneratedGame/QuantumGeneratedGame.Build.cs": "using UnrealBuildTool;\npublic class QuantumGeneratedGame : ModuleRules { public QuantumGeneratedGame(ReadOnlyTargetRules Target) : base(Target) { PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs; } }\n",
                "Source/QuantumGeneratedGame/QuantumGeneratedGame.cpp": "#include \"Modules/ModuleManager.h\"\nIMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, QuantumGeneratedGame, \"QuantumGeneratedGame\");\n",
                "README.md": "# Quantum Generated Unreal Project\nCreate the matching Unreal project in the editor, then integrate these source files.\n",
            }
        else:
            files = {
                "index.html": "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Quantum Generated Game</title></head><body><canvas id='game' width='1280' height='720'></canvas><script src='game.js'></script></body></html>\n",
                "game.js": "const c=document.getElementById('game'),x=c.getContext('2d');let t=0;function loop(){t+=.016;x.clearRect(0,0,c.width,c.height);x.fillStyle='#0b1020';x.fillRect(0,0,c.width,c.height);x.beginPath();x.arc(640+Math.cos(t)*180,360+Math.sin(t)*100,50,0,Math.PI*2);x.fillStyle='#b98cff';x.fill();x.fillStyle='white';x.font='28px sans-serif';x.fillText('QUANTUM GENERATED GAME',470,360);requestAnimationFrame(loop)}loop();\n",
                "README.md": f"# {name}\n\nPrompt-generated web prototype.\n\nIdea: {prompt.replace(chr(10), ' ')}\n",
            }
        if kind == "mod":
            files["mod/manifest.json"] = json.dumps({"id": name, "type": "mod", "version": "1.0.0", "description": prompt}, indent=2)
            files["mod/README.md"] = "# Generated Mod\n\nConnect this adapter to the target game's documented mod API.\n"
        elif kind == "dlc":
            files["dlc/content.json"] = json.dumps({"id": name + "-dlc", "type": "dlc", "title": name.replace("-", " ").title(), "idea": prompt, "content": ["new area", "new quest", "new rewards"]}, indent=2)
        return {"name": name, "description": f"Generated {kind} scaffold for {target}.", "files": [{"path": p, "content": c} for p, c in files.items()], "next_steps": ["Open the project in the target engine.", "Replace placeholders with original assets.", "Run the project's tests/build pipeline."], "test_plan": ["Validate the project opens.", "Run the main scene/build.", "Verify the generated feature described in the prompt."]}

    def _validate(self, data: dict[str, Any], target: str, kind: str) -> dict[str, Any]:
        if not isinstance(data, dict) or not isinstance(data.get("files"), list):
            raise GameGenerationError("Generator returned an invalid project.")
        raw = data["files"]
        if not raw or len(raw) > MAX_FILES:
            raise GameGenerationError("Generator returned an invalid file set.")
        files, seen, total = [], set(), 0
        for item in raw:
            if not isinstance(item, dict):
                raise GameGenerationError("Invalid generated file.")
            path = self._safe_path(str(item.get("path", "")))
            if path in seen:
                raise GameGenerationError(f"Duplicate generated path: {path}")
            content = str(item.get("content", ""))
            size = len(content.encode("utf-8"))
            if size > MAX_FILE_BYTES:
                raise GameGenerationError(f"Generated file is too large: {path}")
            total += size
            if total > MAX_TOTAL_BYTES:
                raise GameGenerationError("Generated project is too large.")
            seen.add(path); files.append({"path": path, "content": content})
        return {"name": str(data.get("name") or "Quantum Generated Project"), "description": str(data.get("description") or ""), "files": files, "next_steps": list(data.get("next_steps") or []), "test_plan": list(data.get("test_plan") or []), "target": target, "kind": kind}

    def generate(self, prompt: str, target: str = "web", kind: str = "game") -> dict[str, Any]:
        prompt = (prompt or "").strip()
        target, kind = (target or "web").lower(), (kind or "game").lower()
        if len(prompt) < 3: raise GameGenerationError("Prompt is too short.")
        if len(prompt) > MAX_PROMPT: raise GameGenerationError("Prompt is too long.")
        if target not in ALLOWED_TARGETS: raise GameGenerationError("Unsupported target engine.")
        if kind not in ALLOWED_KINDS: raise GameGenerationError("Unsupported artifact type.")
        data = self._llm(prompt, target, kind) or self._fallback(prompt, target, kind)
        data = self._validate(data, target, kind)
        project_id = uuid.uuid4().hex[:12]
        root = self.output_dir / project_id
        root.mkdir(parents=True, exist_ok=False)
        for item in data["files"]:
            destination = root / item["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(item["content"], encoding="utf-8")
        manifest = {"id": project_id, "created_at": datetime.now(timezone.utc).isoformat(), "target": target, "kind": kind, "prompt": prompt, "files": [f["path"] for f in data["files"]]}
        (root / "quantum.manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        zip_path = self.output_dir / f"{project_id}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for item in root.rglob("*"):
                if item.is_file(): archive.write(item, item.relative_to(root))
        return {"id": project_id, "name": data["name"], "description": data["description"], "kind": kind, "target": target, "files": [f["path"] for f in data["files"]], "next_steps": data["next_steps"], "test_plan": data["test_plan"], "download": f"/api/generator/download/{project_id}"}

    def download_path(self, project_id: str) -> Path:
        if not PROJECT_ID.fullmatch(project_id): raise GameGenerationError("Invalid project id.")
        path = self.output_dir / f"{project_id}.zip"
        if not path.is_file(): raise GameGenerationError("Generated project not found.")
        return path
