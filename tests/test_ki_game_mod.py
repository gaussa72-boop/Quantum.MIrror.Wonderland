from ki_game_mod.engine import AIEngine, GameState
from ki_game_mod.engine.boss import BossAI
from ki_game_mod.engine.factions import FactionSystem


def test_mod_pack_has_expected_modules():
    pack = AIEngine(seed=7).generate_mod_pack("mirror", 8)
    assert len(pack["quests"]) == 5
    assert len(pack["npcs"]) == 6
    assert len(pack["enemies"]) == 5
    assert len(pack["loot"]) == 8
    assert pack["boss"]["level"] >= 20


def test_combat_event_is_bounded_and_returns_result():
    engine = AIEngine(seed=7)
    result = engine.apply(GameState(), {
        "type": "combat", "player_hp": 100, "enemy_hp": 20,
        "player_damage": 15, "enemy_damage": 5
    })
    assert result["winner"] == "player"
    assert result["turns"] <= 100


def test_adaptive_balance_and_analyzer_use_player_state():
    engine = AIEngine(seed=7)
    state = GameState(player={"level": 8, "deaths": 8, "kills": 2}, inventory=[{"id": "x"}])
    assert engine.apply(state, {"type": "balance"})["suggested_difficulty"] == "easy"
    report = engine.apply(state, {"type": "analyze"})
    assert report["player_level"] == 8
    assert report["inventory_size"] == 1


def test_faction_reputation_is_clamped():
    factions = FactionSystem()
    result = factions.apply("Mirror Keepers", 1000)
    assert result["reputation"] == 100
    assert result["standing"] == "friendly"


def test_boss_has_telegraphed_phases():
    boss = BossAI(seed=7).create(20)
    assert len(boss["phases"]) >= 3
    assert boss["telegraph_seconds"] > 0
