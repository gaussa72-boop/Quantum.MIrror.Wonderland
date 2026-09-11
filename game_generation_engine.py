"""Quantum AI Game Studio - secure prompt-to-game/mod/DLC generation core."""
from __future__ import annotations

import json, os, re, tempfile, zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import OpenAI

ALLOWED_TARGETS = {"web", "godot", "unity", "unreal"}
ALLOWED_MODES = {"game", "mod", "dlc"}
MAX_FILES = 80
MAX_FILE_BYTES = 250_000
MAX_TOTAL_BYTES = 5_000_000

SYSTEM_PROMPT = """You are Quantum AI Game Studio, a senior game architect and programmer.
Turn a user's idea into a small but coherent, runnable project or extension.
Return ONLY valid JSON: {title, description, target, mode, files:[{path,content}], run_instructions, test_plan}.
Never include secrets, credentials, tokens, private keys, shell commands that delete data, or paths outside the project.
Prefer self-contained starter projects. For mods/DLC, create a clean adapter/plugin structure and clearly document integration points.
Keep generated files concise and executable. Use forward-slash relative paths only.
"""

@dataclass
class GenerationResult:
    project: dict[str, Any]
    zip_path: str | None

class GenerationError(Exception):
    pass

def _safe_path(value: str) -> str:
    p = value.replace("\\", "/").strip()
    if not p or p.startswith("/") or re.match(r"^[A-Za-z]:", p) or ".." in Path(p).parts:
        raise GenerationError(f"Unsafe path: {value}")
    if "\x00" in p:
        raise GenerationError("NUL byte in path")
    return p

def _validate(project: dict[str, Any], target: str, mode: str) -> dict[str, Any]:
    if target not in ALLOWED_TARGETS: raise GenerationError("Unsupported target")
    if mode not in ALLOWED_MODES: raise GenerationError("Unsupported generation mode")
    files = project.get("files")
    if not isinstance(files, list) or not files or len(files) > MAX_FILES:
        raise GenerationError("Invalid file set")
    clean, total = [], 0
    seen = set()
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("content"), str):
            raise GenerationError("Invalid file entry")
        path = _safe_path(item["path"])
        if path in seen: raise GenerationError(f"Duplicate path: {path}")
        data = item["content"].encode("utf-8")
        if len(data) > MAX_FILE_BYTES: raise GenerationError(f"File too large: {path}")
        total += len(data)
        if total > MAX_TOTAL_BYTES: raise GenerationError("Project too large")
        seen.add(path); clean.append({"path": path, "content": item["content"]})
    project["target"], project["mode"], project["files"] = target, mode, clean
    return project

def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I|re.S)
    try: return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if not match: raise GenerationError("Model did not return JSON")
        return json.loads(match.group(0))

def _fallback(prompt: str, target: str, mode: str) -> dict[str, Any]:
    safe = re.sub(r"[^a-zA-Z0-9 _-]", "", prompt)[:80] or "Quantum Game"
    if target == "web":
        files = [{"path":"index.html","content":f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{safe}</title><style>body{{margin:0;background:#090a12;color:#fff;font:16px system-ui;display:grid;place-items:center;min-height:100vh}}main{{max-width:720px;padding:32px;text-align:center}}button{{padding:14px 22px;border-radius:12px;border:0;cursor:pointer}}</style></head><body><main><h1>{safe}</h1><p>Quantum AI generated {mode}.</p><button id="play">Start</button><p id="status"></p></main><script>play.onclick=()=>status.textContent='Game initialized — expand this prototype with your prompt.';</script></body></html>'''}]
    elif target == "godot":
        files = [{"path":"project.godot","content":"[application]\nconfig/name=\"Quantum Generated Game\"\nrun/main_scene=\"res://main.tscn\"\n[display]\nwindow/size/viewport_width=1280\nwindow/size/viewport_height=720\n"},{"path":"main.tscn","content":"[gd_scene load_steps=2 format=3]\n\n[ext_resource path=\"res://main.gd\" type=\"Script\" id=\"1\"]\n\n[node name=\"Main\" type=\"Node2D\"]\nscript = ExtResource(\"1\")\n"},{"path":"main.gd","content":"extends Node2D\nfunc _ready():\n    print(\"Quantum generated project ready\")\n"}]
    else:
        files = [{"path":"README.md","content":f"# {safe}\n\nGenerated {mode} target: {target}.\n\nThis starter contains documented integration points for the selected engine.\n"}]
    return {"title":safe,"description":prompt,"target":target,"mode":mode,"files":files,"run_instructions":"See generated README/project files.","test_plan":["Validate file paths","Open the generated project","Run the target build/test workflow"]}

class GameGenerationEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
    def generate(self, prompt: str, target: str="web", mode: str="game") -> GenerationResult:
        prompt = (prompt or "").strip()
        if not prompt: raise GenerationError("Prompt is required")
        if len(prompt) > 12_000: raise GenerationError("Prompt too long")
        if self.client:
            response = self.client.chat.completions.create(model=os.getenv("GAME_STUDIO_MODEL", "gpt-4o-mini"), temperature=0.2, response_format={"type":"json_object"}, messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":f"Target: {target}\nMode: {mode}\nIdea:\n{prompt}"}])
            project = _extract_json(response.choices[0].message.content or "")
        else:
            project = _fallback(prompt, target, mode)
        project = _validate(project, target, mode)
        return GenerationResult(project=project, zip_path=None)
    def package(self, project: dict[str, Any]) -> str:
        fd, path = tempfile.mkstemp(prefix="quantum-game-", suffix=".zip"); os.close(fd)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("quantum-manifest.json", json.dumps({k:v for k,v in project.items() if k != "files"}, indent=2))
            for f in project["files"]: z.writestr(f["path"], f["content"])
        return path
