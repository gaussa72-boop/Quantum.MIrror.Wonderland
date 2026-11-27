import unittest
from app import app

class GameEngineFederationTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_registry_contains_all_engine_projects(self):
        response = self.client.get("/api/game-engines/federation")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        ids = {engine["id"] for engine in data["engines"]}
        self.assertTrue({"quantum-mirror", "ki-game-mod", "the-lord", "lichtkrieger", "dark-wonderland", "neuroforge"}.issubset(ids))
        self.assertFalse(data["native_build_verified"])

    def test_dashboard_and_shared_sdk_are_served(self):
        self.assertEqual(self.client.get("/game-engines/").status_code, 200)
        sdk = self.client.get("/game-engines/astralis-engine-link.js")
        self.assertEqual(sdk.status_code, 200)
        self.assertIn(b"/api/game-engines/generate", sdk.data)

    def test_multi_module_generation_pipeline(self):
        response = self.client.post("/api/game-engines/generate", json={
            "idea": "A lost star kingdom guarded by a living nebula",
            "style": "Mythic Science Fantasy",
            "regions": 4,
            "level": 20
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["generation"]["requested"], 8)
        self.assertGreater(data["generation"]["succeeded"], 0)
        self.assertIn("world", data["generation"]["modules"])
        self.assertIn("boss", data["generation"]["modules"])
        self.assertEqual(data["native_engine_build"], "not_created")

if __name__ == "__main__":
    unittest.main()
