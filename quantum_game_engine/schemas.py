"""Stable schemas shared by generation stages."""
from __future__ import annotations

from typing import Any


def stage_contract(stage: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not stage or not isinstance(payload, dict):
        raise ValueError("Invalid generation stage contract.")
    return {"schema_version": "1.0", "stage": stage, "payload": payload}


def asset_manifest(entries: list[dict[str, Any]]) -> dict[str, Any]:
    clean = []
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("id") or not entry.get("type"):
            raise ValueError("Invalid asset manifest entry.")
        clean.append({
            "id": str(entry["id"]),
            "type": str(entry["type"]),
            "path": str(entry.get("path", "")),
            "source": "generated-original",
            "lod": bool(entry.get("lod", True)),
        })
    return {"schema_version": "1.0", "assets": clean}
