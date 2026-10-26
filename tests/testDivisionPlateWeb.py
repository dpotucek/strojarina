import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../DaPTools/src'))

from flask_app import app


class TestDivisionPlateWeb(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_division_plate_pages_display_image(self):
        for page in ("/division-plate", "/en/division-plate"):
            with self.subTest(page=page):
                response = self.client.get(page)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"/static/data/deleniKotoucky.png", response.data)

    def test_division_plate_image_is_available(self):
        response = self.client.get("/static/data/deleniKotoucky.png")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/png")


if __name__ == "__main__":
    unittest.main()
