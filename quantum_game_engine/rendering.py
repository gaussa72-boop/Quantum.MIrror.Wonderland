"""High-end rendering profile used by generated projects."""
from __future__ import annotations

ULTRA_4K_PROFILE = {
    "resolution": [3840, 2160],
    "render_scale": 1.0,
    "hdr": True,
    "target_fps": 120,
    "dynamic_resolution": True,
    "adaptive_quality": True,
    "texture_quality": "ultra",
    "shadow_quality": "ultra",
    "global_illumination": "high",
    "ray_tracing": True,
    "anisotropic_filtering": 16,
    "texture_streaming": True,
    "lod": True,
    "occlusion_culling": True,
    "instancing": True,
    "upscaling": ["DLSS", "FSR", "XeSS"],
}

def profile_for(target: str, quality: str = "4k_ultra") -> dict:
    """Return a copy so generators can safely customize the profile."""
    if quality == "4k_ultra":
        return {**ULTRA_4K_PROFILE, "target": target}
    return {"target": target, "quality": quality, "target_fps": 60, "dynamic_resolution": True}
