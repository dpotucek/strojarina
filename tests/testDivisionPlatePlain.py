#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# -*- coding: utf-8 -*-
"""
Unit tests for DivisionPlatePlain module.
"""

import unittest
from DivisionPlatePlain import calculate_disks_radius


class TestDivisionPlatePlain(unittest.TestCase):

    def test_calculate_disks_radius(self):
        # Use case 1: 6 divisions, 100mm diameter
        result = calculate_disks_radius(6, 100)
        self.assertAlmostEqual(result, 50.0, places=2)
        self.assertIsInstance(result, float)
        
        # Use case 2: 4 divisions, 50mm diameter
        result = calculate_disks_radius(4, 50)
        self.assertAlmostEqual(result, 60.355, places=2)
        
        # Use case 3: 8 divisions, 120mm diameter
        result = calculate_disks_radius(8, 120)
        self.assertAlmostEqual(result, 37.195, places=2)
        
        # Use case 4: Many divisions, smaller diameter
        result = calculate_disks_radius(12, 80)
        self.assertAlmostEqual(result, 13.968, places=2)
        
        # Use case 5: Few divisions, large diameter
        result = calculate_disks_radius(3, 200)
        self.assertAlmostEqual(result, 646.410, places=2)
        
        # Use case 6: Many divisions, small diameter
        result = calculate_disks_radius(16, 60)
        self.assertAlmostEqual(result, 7.271, places=2)
        
        # Use case 7: Odd divisions
        result = calculate_disks_radius(5, 150)
        self.assertAlmostEqual(result, 106.944, places=2)
        
        # Use case 8: Decimal divisions
        result = calculate_disks_radius(10, 90)
        self.assertAlmostEqual(result, 20.125, places=2)
        
        # Use case 9: Very many divisions, small diameter
        result = calculate_disks_radius(24, 40)
        self.assertAlmostEqual(result, 3.002, places=2)


if __name__ == '__main__':
    unittest.main()