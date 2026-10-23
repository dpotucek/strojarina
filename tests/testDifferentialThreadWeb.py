import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../DaPTools/src"))

from gui_deleni_web import app


class TestDifferentialThreadWeb(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_differential_pages_display_image(self):
        for page in ("/differential", "/en/differential-thread"):
            with self.subTest(page=page):
                response = self.client.get(page)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"/static/data/DifferentialThread.png", response.data)

    def test_differential_thread_image_is_available(self):
        response = self.client.get("/static/data/DifferentialThread.png")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/png")


if __name__ == "__main__":
    unittest.main()
