from quantum_game_engine.pipeline import GenerationPipeline, GenerationSpec
from quantum_game_engine.rendering import profile_for
from quantum_game_engine.dunkle_spiegel import concept_from_prompt


def test_4k_pipeline_defaults():
    plan = GenerationPipeline().plan(GenerationSpec(prompt="Dark mirror RPG"))
    assert plan["visual"]["resolution"] == "3840x2160"
    assert plan["visual"]["target_fps"] == 120
    assert plan["visual"]["adaptive_quality"] is True


def test_render_profile_is_engine_specific():
    profile = profile_for("unreal")
    assert profile["resolution"] == [3840, 2160]
    assert profile["target"] == "unreal"


def test_dunkle_spiegel_concept_contains_core_systems():
    design = concept_from_prompt("A world behind a living mirror").to_design_document()
    assert design["systems"]["ai_companion"] == "Master-Kater"
    assert design["systems"]["mirror_world"] is True
