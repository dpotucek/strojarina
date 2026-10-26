import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../DaPTools/src"))

from dilution_tables import DILUTION_WATER_TABLE, MIXING_COMPONENTS_TABLE
from flask_app import app


class TestDilutionTables(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_table_data_matches_source_table_dimensions_and_values(self):
        self.assertEqual(len(DILUTION_WATER_TABLE), 9)
        self.assertTrue(all(len(row) == 2 and len(row[1]) == 11 for row in DILUTION_WATER_TABLE))
        self.assertEqual(DILUTION_WATER_TABLE[0], (
            "50%", ("2.5", "5", "6.2", "7.5", "10", "12.5", "25", "50", "62.5", "125", "187.5")
        ))
        self.assertEqual(len(MIXING_COMPONENTS_TABLE), 9)
        self.assertTrue(all(len(row) == 2 and len(row[1]) == 9 for row in MIXING_COMPONENTS_TABLE))
        self.assertEqual(MIXING_COMPONENTS_TABLE[0][1][0], "160 + 40")
        self.assertEqual(MIXING_COMPONENTS_TABLE[-1][1][-1], "444.4 + 555.6")

    def test_bilingual_pages_render_both_reference_tables_after_calculators(self):
        page_expectations = (
            ("/redeni", "Tabulky pro cílovou koncentraci 40 %", "Voda potřebná k naředění alkoholu"),
            ("/en/solution-dilution", "Reference tables for a 40% target concentration", "Water needed to dilute alcohol"),
        )
        for path, first_heading, second_heading in page_expectations:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                page = response.get_data(as_text=True)
                self.assertIn(first_heading, page)
                self.assertIn(second_heading, page)
                self.assertIn("187.5", page)
                self.assertIn("160 + 40", page)
                self.assertGreater(page.index(first_heading), page.index('id="mixingResult"'))
                self.assertEqual(page.count("<table>"), 2)


if __name__ == "__main__":
    unittest.main()
