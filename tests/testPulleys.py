#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# -*- coding: utf-8 -*-
"""
Unit tests for pulleys module.
"""

import unittest
from pulleys import calculate2_pulleys, find_driven_diameter


class TestPulleys(unittest.TestCase):

    def test_calculate2_pulleys(self):
        # Use case 1: Original test - standard motor setup
        rpm, length = calculate2_pulleys(1450, 10, 18, 65)
        self.assertAlmostEqual(rpm, 805.6, places=1)
        self.assertAlmostEqual(length, 174.0, places=1)
        
        # Use case 2: Smaller setup
        rpm, length = calculate2_pulleys(1200, 8, 15, 50)
        self.assertAlmostEqual(rpm, 640.0, places=1)
        self.assertAlmostEqual(length, 136.1, places=1)
        
        # Use case 3: Larger setup
        rpm, length = calculate2_pulleys(1800, 12, 20, 80)
        self.assertAlmostEqual(rpm, 1080.0, places=1)
        self.assertAlmostEqual(length, 210.3, places=1)
        
        # Use case 4: Slow speed setup
        rpm, length = calculate2_pulleys(900, 6, 12, 40)
        self.assertAlmostEqual(rpm, 450.0, places=1)
        self.assertAlmostEqual(length, 108.3, places=1)
        
        # Use case 5: High speed setup
        rpm, length = calculate2_pulleys(2400, 15, 25, 100)
        self.assertAlmostEqual(rpm, 1440.0, places=1)
        self.assertAlmostEqual(length, 262.8, places=1)
        
        # Use case 6: Small pulleys
        rpm, length = calculate2_pulleys(1000, 5, 10, 30)
        self.assertAlmostEqual(rpm, 500.0, places=1)
        self.assertAlmostEqual(length, 83.6, places=1)

    def test_find_driven_diameter(self):
        # Use case 1: Same speed (1:1 ratio)
        result = find_driven_diameter(1450, 1450, 10)
        self.assertEqual(result, 10)
        
        # Use case 2: Original test - reduction
        result = find_driven_diameter(1450, 805, 10)
        self.assertAlmostEqual(result, 18.01, places=1)
        
        # Use case 3: Half speed reduction
        result = find_driven_diameter(1200, 600, 8)
        self.assertAlmostEqual(result, 16.0, places=1)
        
        # Use case 4: Half speed, larger pulleys
        result = find_driven_diameter(1800, 900, 12)
        self.assertAlmostEqual(result, 24.0, places=1)
        
        # Use case 5: Large reduction (4:1)
        result = find_driven_diameter(1600, 400, 10)
        self.assertAlmostEqual(result, 40.0, places=1)
        
        # Use case 6: Speed increase (overdrive)
        result = find_driven_diameter(1000, 2000, 5)
        self.assertAlmostEqual(result, 2.5, places=1)


if __name__ == '__main__':
    unittest.main()