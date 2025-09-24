#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# -*- coding: utf-8 -*-
"""
Unit tests for plochyNaHrideli module.
"""

import unittest
from plochyNaHrideli import PlochyNaHrideli, hloubka_plosky, hloubka_ctverce


class TestPlochyNaHrideli(unittest.TestCase):

    def setUp(self):
        self.pnh = PlochyNaHrideli()

    def test_hloubka_plosky_class(self):
        # Use case 1: Standard shaft with flat
        result = self.pnh.hloubka_plosky(25, 7)
        self.assertAlmostEqual(result, 13.00, places=2)
        
        # Use case 2: Small shaft, narrow flat
        result = self.pnh.hloubka_plosky(20, 5)
        self.assertAlmostEqual(result, 10.32, places=2)
        
        # Use case 3: Large shaft, wide flat
        result = self.pnh.hloubka_plosky(30, 10)
        self.assertAlmostEqual(result, 15.86, places=2)
        
        # Use case 4: Small diameter, narrow flat
        result = self.pnh.hloubka_plosky(15, 4)
        self.assertAlmostEqual(result, 7.77, places=2)
        
        # Use case 5: Medium large shaft
        result = self.pnh.hloubka_plosky(35, 12)
        self.assertAlmostEqual(result, 18.56, places=2)
        
        # Use case 6: Large shaft, medium flat
        result = self.pnh.hloubka_plosky(50, 15)
        self.assertAlmostEqual(result, 26.15, places=2)

    def test_hloubka_ctverce_class(self):
        # Use case 1: Standard 25mm shaft
        hloubka, delka = self.pnh.hloubka_ctverce(25)
        self.assertEqual(hloubka, 3.125)
        
        # Use case 2: Small 20mm shaft
        hloubka, delka = self.pnh.hloubka_ctverce(20)
        self.assertEqual(hloubka, 2.5)
        
        # Use case 3: Large 40mm shaft
        hloubka, delka = self.pnh.hloubka_ctverce(40)
        self.assertEqual(hloubka, 5.0)
        
        # Use case 4: Small 15mm shaft
        hloubka, delka = self.pnh.hloubka_ctverce(15)
        self.assertEqual(hloubka, 1.875)
        
        # Use case 5: Medium 35mm shaft
        hloubka, delka = self.pnh.hloubka_ctverce(35)
        self.assertEqual(hloubka, 4.375)
        
        # Use case 6: Large 50mm shaft
        hloubka, delka = self.pnh.hloubka_ctverce(50)
        self.assertEqual(hloubka, 6.25)

    def test_hloubka_plosky_function(self):
        # Use case 1: Standard shaft with flat
        result = hloubka_plosky(25, 7)
        self.assertAlmostEqual(result, 13.00, places=2)
        
        # Use case 2: Small shaft, narrow flat
        result = hloubka_plosky(20, 5)
        self.assertAlmostEqual(result, 10.32, places=2)
        
        # Use case 3: Large shaft, wide flat
        result = hloubka_plosky(30, 10)
        self.assertAlmostEqual(result, 15.86, places=2)
        
        # Use case 4: Very small shaft
        result = hloubka_plosky(12, 3)
        self.assertAlmostEqual(result, 6.19, places=2)
        
        # Use case 5: Medium shaft, narrow flat
        result = hloubka_plosky(40, 8)
        self.assertAlmostEqual(result, 20.40, places=2)
        
        # Use case 6: Large shaft, wide flat
        result = hloubka_plosky(60, 20)
        self.assertAlmostEqual(result, 31.72, places=2)

    def test_hloubka_ctverce_function(self):
        # Use case 1: Standard 25mm shaft
        result = hloubka_ctverce(25)
        self.assertEqual(result, 3.125)
        
        # Use case 2: Small 20mm shaft
        result = hloubka_ctverce(20)
        self.assertEqual(result, 2.5)
        
        # Use case 3: Large 40mm shaft
        result = hloubka_ctverce(40)
        self.assertEqual(result, 5.0)
        
        # Use case 4: Very small 12mm shaft
        result = hloubka_ctverce(12)
        self.assertEqual(result, 1.5)
        
        # Use case 5: Medium large 45mm shaft
        result = hloubka_ctverce(45)
        self.assertEqual(result, 5.625)
        
        # Use case 6: Large 60mm shaft
        result = hloubka_ctverce(60)
        self.assertEqual(result, 7.5)


if __name__ == '__main__':
    unittest.main()