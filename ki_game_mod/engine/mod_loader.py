import json
from pathlib import Path
from .models import ModManifest

class ModLoader:
    def load_manifest(self, path: str | Path) -> ModManifest:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return ModManifest(id=data["id"], name=data["name"], version=data.get("version","1.0.0"), description=data.get("description",""), modules=tuple(data.get("modules",())))
