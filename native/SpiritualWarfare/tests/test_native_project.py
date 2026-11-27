import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class NativeProjectTests(unittest.TestCase):
    def test_unreal_project_descriptor_is_valid(self):
        project = json.loads((ROOT / "SpiritualWarfare.uproject").read_text(encoding="utf-8"))
        self.assertEqual(project["EngineAssociation"], "5.6")
        self.assertIn("SpiritualWarfare", {item["Name"] for item in project["Modules"]})

    def test_targets_and_core_subsystem_exist(self):
        required = [
            "Source/SpiritualWarfare.Target.cs",
            "Source/SpiritualWarfareEditor.Target.cs",
            "Source/SpiritualWarfare/Public/AstralisWorldSubsystem.h",
            "Source/SpiritualWarfare/Private/AstralisWorldSubsystem.cpp",
            "Config/DefaultEngine.ini",
        ]
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_world_schema_has_seed_and_regions(self):
        schema = json.loads((ROOT / "astralis-world.schema.json").read_text(encoding="utf-8"))
        self.assertIn("seed", schema["required"])
        self.assertIn("regions", schema["required"])

if __name__ == "__main__":
    unittest.main()
