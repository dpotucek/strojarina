import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../DaPTools/src"))

from gui_deleni_web import app
from hardness_conversion import convert_hardness


class TestHardnessConversion(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_interpolates_all_three_scales(self):
        self.assertEqual(convert_hardness(40, "HRC"), {"HRC": 40.0, "HB": 371.0, "HV": 392.0})
        self.assertEqual(convert_hardness(226, "HB"), {"HRC": 20.0, "HB": 226.0, "HV": 238.0})
        self.assertEqual(convert_hardness(940, "HV"), {"HRC": 68.0, "HB": 818.0, "HV": 940.0})
        midpoint = convert_hardness(42.5, "HRC")
        self.assertEqual(midpoint, {"HRC": 42.5, "HB": 396.0, "HV": 419.0})

    def test_rejects_invalid_scale_and_values_outside_reference_range(self):
        for value, scale in ((19, "HRC"), (819, "HB"), (237, "HV"), (40, "shore")):
            with self.subTest(value=value, scale=scale):
                with self.assertRaises(ValueError):
                    convert_hardness(value, scale)
        with self.assertRaises(ValueError):
            convert_hardness(float("nan"), "HRC")

    def test_api_returns_converted_values_and_rejects_out_of_range_input(self):
        response = self.client.post("/api/hardness/convert", json={"value": 40, "scale": "hrc"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["HB"], 371.0)
        self.assertEqual(response.get_json()["HV"], 392.0)
        response = self.client.post("/api/hardness/convert", json={"value": 19, "scale": "HRC"})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.get_json()["success"])

    def test_localized_pages_show_metal_table_without_nonmetal_table(self):
        for path, title in (
            ("/hardness", "Převod tvrdosti HRC, HB a HV"),
            ("/en/hardness", "HRC, HB and HV Hardness Conversion"),
        ):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            page = response.get_data(as_text=True)
            self.assertIn(title, page)
            if path.startswith("/en"):
                self.assertIn("Rockwell hardness", page)
                self.assertIn("Brinell hardness", page)
                self.assertIn("Vickers hardness", page)
            else:
                self.assertIn("Rockwellovu stupnici C", page)
                self.assertIn("Brinellovu tvrdost", page)
                self.assertIn("Vickersovu tvrdost", page)
            self.assertIn("hardness of metallic materials" if path.startswith("/en") else "kovových materiálů", page)
            self.assertNotIn("hardness of non-metallic materials", page)
            self.assertNotIn("nekovových materiálů", page)
            self.assertIn("HRC", page)
            self.assertIn("N/A", page)


if __name__ == "__main__":
    unittest.main()
