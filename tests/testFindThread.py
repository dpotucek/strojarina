#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# -*- coding: utf-8 -*-
"""
Unit tests for findThread module.
"""

import unittest
from findThread import Thread, ThreadPool


class TestFindThread(unittest.TestCase):

    def setUp(self):
        self.thread = Thread("M6", "N/A", 6.0, "N/A", 1.0, "N/A", "N/A", "N/A", "N/A")
        self.thread_m8 = Thread("M8", "N/A", 8.0, "N/A", 1.25, "N/A", "N/A", "N/A", "N/A")
        self.thread_m10 = Thread("M10", "N/A", 10.0, "N/A", 1.5, "N/A", "N/A", "N/A", "N/A")
        self.thread_m12 = Thread("M12", "N/A", 12.0, "N/A", 1.75, "N/A", "N/A", "N/A", "N/A")

    def test_thread_creation(self):
        # Use case 1: M6 thread
        self.assertEqual(self.thread.name, "M6")
        self.assertEqual(self.thread.diaMM, 6.0)
        self.assertEqual(self.thread.pitchMM, 1.0)
        
        # Use case 2: M8 thread
        self.assertEqual(self.thread_m8.name, "M8")
        self.assertEqual(self.thread_m8.diaMM, 8.0)
        self.assertEqual(self.thread_m8.pitchMM, 1.25)
        
        # Use case 3: M10 thread
        self.assertEqual(self.thread_m10.name, "M10")
        self.assertEqual(self.thread_m10.diaMM, 10.0)
        self.assertEqual(self.thread_m10.pitchMM, 1.5)
        
        # Use case 4: M12 thread
        self.assertEqual(self.thread_m12.name, "M12")
        self.assertEqual(self.thread_m12.diaMM, 12.0)
        self.assertEqual(self.thread_m12.pitchMM, 1.75)

    def test_get_pitch(self):
        # Use case 1: M6 pitch
        self.assertEqual(self.thread.get_pitch(), 1.0)
        
        # Use case 2: M8 pitch
        self.assertEqual(self.thread_m8.get_pitch(), 1.25)
        
        # Use case 3: M10 pitch
        self.assertEqual(self.thread_m10.get_pitch(), 1.5)
        
        # Use case 4: M12 pitch
        self.assertEqual(self.thread_m12.get_pitch(), 1.75)

    def test_get_diameter(self):
        # Use case 1: M6 diameter
        self.assertEqual(self.thread.get_diameter(), 6.0)
        
        # Use case 2: M8 diameter
        self.assertEqual(self.thread_m8.get_diameter(), 8.0)
        
        # Use case 3: M10 diameter
        self.assertEqual(self.thread_m10.get_diameter(), 10.0)
        
        # Use case 4: M12 diameter
        self.assertEqual(self.thread_m12.get_diameter(), 12.0)

    def test_fits_dimension(self):
        # Use case 1: M6 fits its own dimensions
        self.assertTrue(self.thread.fits_dimension(6.0))
        self.assertTrue(self.thread.fits_dimension(1.0))
        self.assertFalse(self.thread.fits_dimension(5.0))
        
        # Use case 2: M8 fits its dimensions
        self.assertTrue(self.thread_m8.fits_dimension(8.0))
        self.assertTrue(self.thread_m8.fits_dimension(1.25))
        self.assertFalse(self.thread_m8.fits_dimension(7.0))
        
        # Use case 3: M10 fits its dimensions
        self.assertTrue(self.thread_m10.fits_dimension(10.0))
        self.assertTrue(self.thread_m10.fits_dimension(1.5))
        self.assertFalse(self.thread_m10.fits_dimension(9.0))
        
        # Use case 4: M12 fits its dimensions
        self.assertTrue(self.thread_m12.fits_dimension(12.0))
        self.assertTrue(self.thread_m12.fits_dimension(1.75))
        self.assertFalse(self.thread_m12.fits_dimension(11.0))

    def test_fits_major_diameter_mm(self):
        # Use case 1: M6 diameter matching
        self.assertTrue(self.thread.fits_major_diameter_mm(6.0))
        self.assertFalse(self.thread.fits_major_diameter_mm(5.0))
        
        # Use case 2: M8 diameter matching
        self.assertTrue(self.thread_m8.fits_major_diameter_mm(8.0))
        self.assertFalse(self.thread_m8.fits_major_diameter_mm(10.0))
        
        # Use case 3: M10 diameter matching
        self.assertTrue(self.thread_m10.fits_major_diameter_mm(10.0))
        self.assertFalse(self.thread_m10.fits_major_diameter_mm(8.0))
        
        # Use case 4: M12 diameter matching
        self.assertTrue(self.thread_m12.fits_major_diameter_mm(12.0))
        self.assertFalse(self.thread_m12.fits_major_diameter_mm(10.0))

    def test_fits_pitch_mm(self):
        # Use case 1: M6 pitch matching
        self.assertTrue(self.thread.fits_pitch_mm(1.0))
        self.assertFalse(self.thread.fits_pitch_mm(0.5))
        
        # Use case 2: M8 pitch matching
        self.assertTrue(self.thread_m8.fits_pitch_mm(1.25))
        self.assertFalse(self.thread_m8.fits_pitch_mm(1.5))
        
        # Use case 3: M10 pitch matching
        self.assertTrue(self.thread_m10.fits_pitch_mm(1.5))
        self.assertFalse(self.thread_m10.fits_pitch_mm(1.25))
        
        # Use case 4: M12 pitch matching
        self.assertTrue(self.thread_m12.fits_pitch_mm(1.75))
        self.assertFalse(self.thread_m12.fits_pitch_mm(1.5))

    def test_is_metric(self):
        # Use case 1: M6 is metric
        self.assertTrue(self.thread.is_metric())
        
        # Use case 2: M8 is metric
        self.assertTrue(self.thread_m8.is_metric())
        
        # Use case 3: M10 is metric
        self.assertTrue(self.thread_m10.is_metric())
        
        # Use case 4: Inch threads are not metric
        inch_thread_1_4 = Thread("1/4-20", 0.25, 6.35, 20, 1.27, "N/A", "N/A", "N/A", "N/A")
        self.assertFalse(inch_thread_1_4.is_metric())
        
        inch_thread_3_8 = Thread("3/8-16", 0.375, 9.525, 16, 1.588, "N/A", "N/A", "N/A", "N/A")
        self.assertFalse(inch_thread_3_8.is_metric())
        
        inch_thread_1_2 = Thread("1/2-13", 0.5, 12.7, 13, 1.954, "N/A", "N/A", "N/A", "N/A")
        self.assertFalse(inch_thread_1_2.is_metric())


if __name__ == '__main__':
    unittest.main()