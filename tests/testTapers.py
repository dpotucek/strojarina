import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from gui_deleni_web import app
from tapers import ISO_TAPERS, MORSE_TAPERS, angle_to_ratio, calculate_taper, ratio_to_angle


class TestTaperCalculations(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_localized_pages_show_standard_taper_tables(self):
        czech = self.client.get("/tapers")
        english = self.client.get("/en/tapers")
        self.assertEqual(czech.status_code, 200)
        self.assertIn("Kužely".encode(), czech.data)
        self.assertIn(b'/static/data/KuzelyGeometrie.png', czech.data)
        self.assertIn("Délka kužele l (mm)".encode(), czech.data)
        self.assertIn("Poměr".encode(), czech.data)
        self.assertIn("Velký průměr (mm)".encode(), czech.data)
        self.assertIn("Vrcholový úhel (°)".encode(), czech.data)
        self.assertIn(b"MT6", czech.data)
        self.assertIn(b"ISO 50", czech.data)
        self.assertIn(b'id="ratio-numerator"', czech.data)
        self.assertEqual(english.status_code, 200)
        self.assertIn(b"Tapers", english.data)
        self.assertIn(b"Taper length l (mm)", english.data)
        self.assertIn(b"gauge line", english.data)
        image = self.client.get("/static/data/KuzelyGeometrie.png")
        self.assertEqual(image.status_code, 200)
        self.assertEqual(image.mimetype, "image/png")

    def test_reference_dimensions_cover_requested_standard_sizes(self):
        self.assertEqual([row["name"] for row in MORSE_TAPERS], [f"MT{i}" for i in range(7)])
        self.assertEqual([row["name"] for row in ISO_TAPERS], ["ISO 30", "ISO 40", "ISO 50"])
        self.assertAlmostEqual(ratio_to_angle(24 / 7)["included_angle_deg"], 16.5943, places=3)

    def test_ratio_and_included_angle_are_inverse_conversions(self):
        converted = ratio_to_angle(20)
        self.assertAlmostEqual(converted["included_angle_deg"], 2.864, places=3)
        restored = angle_to_ratio(converted["included_angle_deg"])
        self.assertAlmostEqual(restored["ratio_denominator"], 20, places=8)
        proportional = ratio_to_angle(20, numerator=2)
        self.assertAlmostEqual(proportional["included_angle_deg"], 5.725, places=3)
        self.assertEqual(proportional["ratio_numerator"], 2)

    def test_taper_calculation_includes_lathe_setup_and_check_dimensions(self):
        result = calculate_taper(30, 20, 100, 200)
        self.assertAlmostEqual(result["ratio_denominator"], 10)
        self.assertAlmostEqual(result["included_angle_deg"], 5.725, places=3)
        self.assertAlmostEqual(result["tailstock_offset"], 10)
        self.assertAlmostEqual(result["top_slide_angle_deg"], result["half_angle_deg"])
        self.assertEqual(len(result["checkpoints"]), 3)
        self.assertEqual([point["diameter"] for point in result["checkpoints"]], [27.5, 25, 22.5])

    def test_calculation_api_and_validation(self):
        response = self.client.post("/api/tapers/calculate", json={
            "large_diameter": 30,
            "small_diameter": 20,
            "taper_length": 100,
            "work_length": 200,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["success"])
        invalid = self.client.post("/api/tapers/calculate", json={
            "large_diameter": 10,
            "small_diameter": 20,
            "taper_length": 100,
            "work_length": 200,
        })
        self.assertEqual(invalid.status_code, 400)

    def test_conversion_endpoints(self):
        ratio = self.client.post("/api/tapers/ratio-to-angle", json={"ratio_denominator": 20})
        proportional_ratio = self.client.post(
            "/api/tapers/ratio-to-angle",
            json={"ratio_numerator": 2, "ratio_denominator": 20},
        )
        angle = self.client.post("/api/tapers/angle-to-ratio", json={"included_angle_deg": 2.864})
        self.assertEqual(ratio.status_code, 200)
        self.assertAlmostEqual(ratio.get_json()["included_angle_deg"], 2.864, places=3)
        self.assertEqual(proportional_ratio.status_code, 200)
        self.assertAlmostEqual(proportional_ratio.get_json()["included_angle_deg"], 5.725, places=3)
        self.assertEqual(angle.status_code, 200)
        self.assertAlmostEqual(angle.get_json()["ratio_denominator"], 20, places=1)

    def test_rejects_invalid_ratio_and_angle(self):
        with self.assertRaises(ValueError):
            ratio_to_angle(0)
        with self.assertRaises(ValueError):
            angle_to_ratio(180)
        with self.assertRaises(ValueError):
            calculate_taper(20, 20, 10, 50)


if __name__ == "__main__":
    unittest.main()
