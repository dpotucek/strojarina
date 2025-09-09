#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# -*- coding: utf-8 -*-
"""
Unit tests for tappingDrills module.
"""

import unittest
import tempfile
import os
from tappingDrills import TappingDrills, MetricThread
from findThread import Thread


class TestTappingDrills(unittest.TestCase):

    def setUp(self):
        self.test_thread = Thread("M6", "N/A", 6.0, "N/A", 1.0, "N/A", "N/A", "N/A", "N/A")
        self.metric_thread = MetricThread(self.test_thread)
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.tapping_drills = TappingDrills(self.temp_file.name, debug=False)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_tapping_drills_class(self):
        # Use case 1: Default initialization
        self.assertEqual(self.tapping_drills.output_file, self.temp_file.name)
        self.assertFalse(self.tapping_drills.debug)
        
        # Use case 2: Debug enabled
        td_debug = TappingDrills('/tmp/test.txt', debug=True)
        self.assertTrue(td_debug.debug)
        self.assertEqual(td_debug.output_file, '/tmp/test.txt')
        
        # Use case 3: Default file path
        td_default = TappingDrills()
        self.assertEqual(td_default.output_file, '/home/david/Downloads/ThreadOutput.txt')
        self.assertFalse(td_default.debug)
        
        # Use case 4: Custom file, debug off
        td_custom = TappingDrills('/custom/path/output.txt', debug=False)
        self.assertEqual(td_custom.output_file, '/custom/path/output.txt')
        self.assertFalse(td_custom.debug)

    def test_put_header(self):
        # Use case 1: Standard header write
        with open(self.temp_file.name, 'w') as f:
            self.tapping_drills.put_header(f)
        
        with open(self.temp_file.name, 'r') as f:
            content = f.read()
            self.assertIn('LaTeX', content)
            self.assertIn('copy/paste', content)
        
        # Use case 2: Multiple header writes
        with open(self.temp_file.name, 'w') as f:
            self.tapping_drills.put_header(f)
            self.tapping_drills.put_header(f)
        
        with open(self.temp_file.name, 'r') as f:
            content = f.read()
            self.assertEqual(content.count('LaTeX'), 2)
        
        # Use case 3: Header with different TappingDrills instance
        td2 = TappingDrills(debug=True)
        with open(self.temp_file.name, 'w') as f:
            td2.put_header(f)
        
        with open(self.temp_file.name, 'r') as f:
            content = f.read()
            self.assertIn('LaTeX', content)

    def test_count_tap_drill_single(self):
        # Use case 1: M4 thread, 75% strength
        result = MetricThread.countTapDrillSingle(4.0, 0.7, 75)
        self.assertAlmostEqual(result, 3.43, places=2)
        
        # Use case 2: M6 thread, 60% strength
        result = MetricThread.countTapDrillSingle(6.0, 1.0, 60)
        self.assertAlmostEqual(result, 5.35, places=2)
        
        # Use case 3: M8 thread, 80% strength
        result = MetricThread.countTapDrillSingle(8.0, 1.25, 80)
        self.assertAlmostEqual(result, 6.92, places=2)
        
        # Use case 4: M10 thread, 70% strength
        result = MetricThread.countTapDrillSingle(10.0, 1.5, 70)
        self.assertAlmostEqual(result, 8.86, places=2)
        
        # Use case 5: M12 thread, 65% strength
        result = MetricThread.countTapDrillSingle(12.0, 1.75, 65)
        self.assertAlmostEqual(result, 10.77, places=2)
        
        # Use case 6: M5 thread, 85% strength
        result = MetricThread.countTapDrillSingle(5.0, 0.8, 85)
        self.assertAlmostEqual(result, 4.26, places=2)

    def test_get_drill(self):
        # Use case 1: M6 thread, 75% strength
        drill = self.metric_thread.getDrill(75)
        self.assertAlmostEqual(drill, 5.19, places=2)
        self.assertGreater(drill, 0)
        self.assertLess(drill, 6.0)
        
        # Use case 2: M6 thread, 60% strength
        drill = self.metric_thread.getDrill(60)
        self.assertAlmostEqual(drill, 5.35, places=2)
        
        # Use case 3: M6 thread, 80% strength
        drill = self.metric_thread.getDrill(80)
        self.assertAlmostEqual(drill, 5.13, places=2)
        
        # Use case 4: M6 thread, 65% strength
        drill = self.metric_thread.getDrill(65)
        self.assertAlmostEqual(drill, 5.30, places=2)
        
        # Use case 5: M6 thread, 70% strength
        drill = self.metric_thread.getDrill(70)
        self.assertAlmostEqual(drill, 5.24, places=2)
        
        # Use case 6: M6 thread, 85% strength
        drill = self.metric_thread.getDrill(85)
        self.assertAlmostEqual(drill, 5.08, places=2)

    def test_count_tap_drill(self):
        # Use case 1: M6 thread, 75% strength
        result = self.metric_thread.countTapDrill(6.0, 1.0, 75)
        self.assertAlmostEqual(result, 5.19, places=2)
        
        # Use case 2: M6 thread, 60% strength
        result = self.metric_thread.countTapDrill(6.0, 1.0, 60)
        self.assertAlmostEqual(result, 5.35, places=2)
        
        # Use case 3: M6 thread, 80% strength
        result = self.metric_thread.countTapDrill(6.0, 1.0, 80)
        self.assertAlmostEqual(result, 5.13, places=2)
        
        # Use case 4: M8 thread, 75% strength
        result = self.metric_thread.countTapDrill(8.0, 1.25, 75)
        self.assertAlmostEqual(result, 6.98, places=2)
        
        # Use case 5: M10 thread, 70% strength
        result = self.metric_thread.countTapDrill(10.0, 1.5, 70)
        self.assertAlmostEqual(result, 8.86, places=2)
        
        # Use case 6: M12 thread, 65% strength
        result = self.metric_thread.countTapDrill(12.0, 1.75, 65)
        self.assertAlmostEqual(result, 10.77, places=2)

    def test_invalid_strength(self):
        # Use case 1: Too low strength (10%)
        with self.assertRaises(ValueError):
            self.metric_thread.getDrill(10)
        
        # Use case 2: Too high strength (101%)
        with self.assertRaises(ValueError):
            self.metric_thread.getDrill(101)
        
        # Use case 3: Boundary case - exactly 20% (should fail)
        with self.assertRaises(ValueError):
            self.metric_thread.getDrill(20)
        
        # Use case 4: Valid boundary case - exactly 100% (should work)
        result = self.metric_thread.getDrill(100)
        self.assertAlmostEqual(result, 4.92, places=2)
        
        # Use case 5: Valid boundary case - 21% (should work)
        result = self.metric_thread.getDrill(21)
        self.assertAlmostEqual(result, 5.77, places=2)
        
        # Use case 6: Negative strength (should fail)
        with self.assertRaises(ValueError):
            self.metric_thread.getDrill(-10)


if __name__ == '__main__':
    unittest.main()