import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../DaPTools/src'))

from findThread import ThreadPool
from flask_app import app
from tappingDrills import MetricThread


class TestTappingDrillsWeb(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.threads = ThreadPool().threadBin

    def test_bilingual_pages_include_thread_lists_and_metric_table(self):
        for path in ('/tapping-drills', '/en/tapping-drills'):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            page = response.get_data(as_text=True)
            self.assertIn('M6 Coarse', page)
            self.assertIn('1/4 UNEF', page)
            for strength in MetricThread.sily:
                self.assertIn(f'{strength}%', page)

    def test_selected_metric_and_inch_threads_use_tapping_drill_formula(self):
        test_threads = (
            ('M6 Coarse', 'mm'),
            ('1/4 UNEF', 'in'),
        )
        for name, unit in test_threads:
            thread_id = next(i for i, thread in enumerate(self.threads) if thread.name == name)
            thread = self.threads[thread_id]
            response = self.client.post('/api/tapping-drills', json={
                'thread_id': thread_id,
                'thread_strength': 75,
            })
            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(result['thread_name'], name)
            self.assertEqual(result['unit'], unit)
            expected = MetricThread.countTapDrillSingle(thread.diaMM, thread.pitchMM, 75)
            self.assertEqual(result['drill_diameter_mm'], round(expected, 3))
            self.assertEqual(result['drill_diameter_in'], round(expected / 25.4, 4))

    def test_invalid_thread_id_and_strength_are_rejected(self):
        self.assertEqual(
            self.client.post('/api/tapping-drills', json={'thread_id': -1}).status_code,
            400,
        )
        self.assertEqual(
            self.client.post('/api/tapping-drills', json={
                'thread_id': 0,
                'thread_strength': 20,
            }).status_code,
            400,
        )


if __name__ == '__main__':
    unittest.main()
