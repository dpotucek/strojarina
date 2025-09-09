#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# -*- coding: utf-8 -*-
"""
Unit tests for strojarinaRuzna module.
"""

import unittest
from strojarinaRuzna import sine_bar_radius, revolver_regular, variable_revolver


class TestStrojarinaRuzna(unittest.TestCase):

    def test_sine_bar_radius(self):
        # Use case 1: Standard setup - 100mm bar, 30mm cylinder, 10°
        result = sine_bar_radius(100, 30, 10)
        self.assertAlmostEqual(result, 47.43, places=1)
        self.assertIsInstance(result, float)
        
        # Use case 2: Longer bar, smaller cylinder - 150mm bar, 25mm cylinder, 15°
        result = sine_bar_radius(150, 25, 15)
        self.assertAlmostEqual(result, 64.16, places=1)
        
        # Use case 3: Shorter bar, larger cylinder - 80mm bar, 35mm cylinder, 5°
        result = sine_bar_radius(80, 35, 5)
        self.assertAlmostEqual(result, 41.98, places=1)
        
        # Use case 4: Medium bar, large angle - 120mm bar, 20mm cylinder, 20°
        result = sine_bar_radius(120, 20, 20)
        self.assertAlmostEqual(result, 61.68, places=1)
        
        # Use case 5: Long bar, medium angle - 200mm bar, 40mm cylinder, 7.5°
        result = sine_bar_radius(200, 40, 7.5)
        self.assertAlmostEqual(result, 66.16, places=1)
        
        # Use case 6: Short bar, large angle - 60mm bar, 15mm cylinder, 30°
        result = sine_bar_radius(60, 15, 30)
        self.assertAlmostEqual(result, 46.06, places=1)

    def test_revolver_regular(self):
        # Use case 1: Standard setup - 7 holes, 12mm diameter
        r, rr = revolver_regular(7, 12, 6, 6)
        self.assertAlmostEqual(r, 20.05, places=1)
        self.assertAlmostEqual(rr, 64.11, places=1)
        self.assertGreater(rr, r)
        
        # Use case 2: Fewer holes, smaller - 6 holes, 10mm diameter
        r, rr = revolver_regular(6, 10, 5, 4)
        self.assertAlmostEqual(r, 14.32, places=1)
        self.assertAlmostEqual(rr, 46.65, places=1)
        
        # Use case 3: More holes, larger - 8 holes, 15mm diameter
        r, rr = revolver_regular(8, 15, 8, 8)
        self.assertAlmostEqual(r, 29.28, places=1)
        self.assertAlmostEqual(rr, 89.57, places=1)
        
        # Use case 4: Few holes, small setup - 5 holes, 8mm diameter
        r, rr = revolver_regular(5, 8, 4, 3)
        self.assertAlmostEqual(r, 9.55, places=1)
        self.assertAlmostEqual(rr, 33.10, places=1)
        
        # Use case 5: Many holes, large setup - 10 holes, 20mm diameter
        r, rr = revolver_regular(10, 20, 10, 10)
        self.assertAlmostEqual(r, 47.75, places=1)
        self.assertAlmostEqual(rr, 135.49, places=1)
        
        # Use case 6: Minimal setup - 4 holes, 6mm diameter
        r, rr = revolver_regular(4, 6, 3, 2)
        self.assertAlmostEqual(r, 5.73, places=1)
        self.assertAlmostEqual(rr, 21.46, places=1)

    def test_variable_revolver(self):
        # Use case 1: Standard mixed sizes
        holes = [8, 8, 10, 10, 12]
        r, rr = variable_revolver(holes, 6, 6)
        self.assertAlmostEqual(r, 12.41, places=1)
        self.assertAlmostEqual(rr, 48.83, places=1)
        self.assertGreater(rr, r)
        
        # Use case 2: Fewer holes, smaller sizes
        holes = [6, 8, 10]
        r, rr = variable_revolver(holes, 5, 4)
        self.assertAlmostEqual(r, 6.21, places=1)
        self.assertAlmostEqual(rr, 30.41, places=1)
        
        # Use case 3: Larger holes
        holes = [10, 12, 14, 16]
        r, rr = variable_revolver(holes, 8, 8)
        self.assertAlmostEqual(r, 13.37, places=1)
        self.assertAlmostEqual(rr, 58.74, places=1)
        
        # Use case 4: Many small holes
        holes = [5, 5, 6, 6, 7, 7]
        r, rr = variable_revolver(holes, 4, 3)
        self.assertAlmostEqual(r, 9.55, places=1)
        self.assertAlmostEqual(rr, 32.10, places=1)
        
        # Use case 5: Large holes
        holes = [15, 18, 20]
        r, rr = variable_revolver(holes, 10, 10)
        self.assertAlmostEqual(r, 13.21, places=1)
        self.assertAlmostEqual(rr, 66.42, places=1)
        
        # Use case 6: Progressive sizes
        holes = [4, 6, 8, 10, 12, 14]
        r, rr = variable_revolver(holes, 7, 5)
        self.assertAlmostEqual(r, 15.28, places=1)
        self.assertAlmostEqual(rr, 54.56, places=1)


if __name__ == '__main__':
    unittest.main()