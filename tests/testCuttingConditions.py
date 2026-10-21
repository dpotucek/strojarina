import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from gui_deleni_web import app


class TestCuttingConditions(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_localized_pages(self):
        czech = self.client.get("/cutting-conditions")
        english = self.client.get("/en/cutting-conditions")
        self.assertEqual(czech.status_code, 200)
        self.assertIn("Řezné podmínky".encode(), czech.data)
        self.assertEqual(english.status_code, 200)
        self.assertIn(b"Cutting Conditions", english.data)

    def test_recommendations_include_every_operation_and_combination(self):
        response = self.client.get("/api/cutting-conditions/recommendations")
        self.assertEqual(response.status_code, 200)
        rows = response.get_json()["recommendations"]
        self.assertEqual(len(rows), 40)
        self.assertEqual(
            {row["operation"] for row in rows},
            {"turning", "milling", "drilling", "reaming"},
        )

    def test_selects_available_rpm_without_exceeding_target(self):
        response = self.client.post("/api/cutting-conditions/calculate", json={
            "material": "steel",
            "tool": "carbide",
            "operation": "turning",
            "diameter": 50,
            "cutting_speed": 100,
            "feed": 0.2,
            "machine_speeds": "200, 400, 800",
        })
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertAlmostEqual(result["ideal_rpm"], 636.6, places=1)
        self.assertEqual(result["selected_rpm"], 400)
        self.assertAlmostEqual(result["actual_cutting_speed"], 62.8, places=1)
        self.assertEqual(result["feed_rate"], 80)
        self.assertEqual(result["safe_machine_speeds"], [200, 400])

    def test_milling_feed_rate_uses_number_of_teeth(self):
        response = self.client.post("/api/cutting-conditions/calculate", json={
            "material": "steel",
            "tool": "carbide",
            "operation": "milling",
            "diameter": 10,
            "cutting_speed": 100,
            "feed": 0.05,
            "teeth": 4,
            "machine_speeds": [500, 1500, 3000],
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["selected_rpm"], 3000)
        self.assertEqual(response.get_json()["feed_rate"], 600)

    def test_rejects_invalid_parameters(self):
        response = self.client.post("/api/cutting-conditions/calculate", json={
            "material": "steel",
            "tool": "hss",
            "operation": "turning",
            "diameter": 0,
            "cutting_speed": 20,
            "feed": 0.1,
            "machine_speeds": "100,abc",
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.get_json()["success"])


if __name__ == "__main__":
    unittest.main()
