"""Deterministic, engine-agnostic generation pipeline for Dunkle Spiegel."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

TARGETS = ("web", "godot", "unity", "unreal")
KINDS = ("game", "mod", "dlc")
QUALITY_PRESETS = ("4k_ultra", "1440p_high", "1080p_balanced")

@dataclass(frozen=True)
class GenerationSpec:
    prompt: str
    kind: str = "game"
    target: str = "web"
    quality: str = "4k_ultra"
    target_fps: int = 120
    ray_tracing: bool = True
    hdr: bool = True
    dlss_or_upscaling: bool = True
    assets: bool = True
    tests: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if len(self.prompt.strip()) < 3:
            raise ValueError("Prompt is too short.")
        if self.kind not in KINDS:
            raise ValueError("Unsupported artifact type.")
        if self.target not in TARGETS:
            raise ValueError("Unsupported target engine.")
        if self.quality not in QUALITY_PRESETS:
            raise ValueError("Unsupported quality preset.")
        if self.target_fps not in (30, 60, 90, 120, 144, 165, 240):
            raise ValueError("Unsupported target FPS.")

class GenerationPipeline:
    """Builds a machine-readable generation plan before code generation.

    It intentionally does not execute generated code on the Flask process.
    A production deployment can hand the plan to isolated build workers.
    """
    def plan(self, spec: GenerationSpec) -> dict[str, Any]:
        spec.validate()
        return {
            "pipeline_version": "1.0",
            "project": {"kind": spec.kind, "target": spec.target},
            "design": {
                "prompt": spec.prompt.strip(),
                "original_content": True,
                "systems": ["core-loop", "input", "camera", "save-state", "settings"],
            },
            "visual": {
                "preset": spec.quality,
                "resolution": "3840x2160" if spec.quality == "4k_ultra" else "auto",
                "target_fps": spec.target_fps,
                "hdr": spec.hdr,
                "ray_tracing": spec.ray_tracing,
                "upscaling": spec.dlss_or_upscaling,
                "adaptive_quality": True,
            },
            "asset_pipeline": {
                "enabled": spec.assets,
                "original_assets_only": True,
                "lod": True,
                "texture_streaming": True,
                "shader_variants": True,
            },
            "quality": {
                "automated_tests": spec.tests,
                "static_validation": True,
                "build_isolation_required": spec.target in {"godot", "unity", "unreal"},
            },
        }
