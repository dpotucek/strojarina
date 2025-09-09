#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# -*- coding: utf-8 -*-
"""
Unit tests for knurling module.
"""

import unittest
from knurling import count_knurling_american, count_crest_num4_dia


class TestKnurling(unittest.TestCase):

    def test_count_knurling_american(self):
        # Use case 1: Standard setup
        deltaK, crestNum = count_knurling_american(20, 30, 25)
        self.assertAlmostEqual(deltaK, 2.094, places=2)
        self.assertEqual(crestNum, 37)
        self.assertIsInstance(crestNum, int)
        
        # Use case 2: Smaller wheel
        deltaK, crestNum = count_knurling_american(15, 24, 20)
        self.assertAlmostEqual(deltaK, 1.963, places=2)
        self.assertEqual(crestNum, 32)
        
        # Use case 3: Larger wheel
        deltaK, crestNum = count_knurling_american(25, 36, 30)
        self.assertAlmostEqual(deltaK, 2.182, places=2)
        self.assertEqual(crestNum, 43)
        
        # Use case 4: Different combination
        deltaK, crestNum = count_knurling_american(18, 28, 15)
        self.assertAlmostEqual(deltaK, 2.020, places=2)
        self.assertEqual(crestNum, 23)
        
        # Use case 5: Larger piece
        deltaK, crestNum = count_knurling_american(22, 32, 35)
        self.assertAlmostEqual(deltaK, 2.160, places=2)
        self.assertEqual(crestNum, 50)
        
        # Use case 6: Small piece
        deltaK, crestNum = count_knurling_american(16, 20, 12)
        self.assertAlmostEqual(deltaK, 2.513, places=2)
        self.assertEqual(crestNum, 15)

    def test_count_crest_num4_dia(self):
        # Use case 1: Standard pitch and diameter
        pocetVrypu, potrebnyObvod, idealniObvod = count_crest_num4_dia(2.0, 30)
        self.assertEqual(pocetVrypu, 47)
        self.assertAlmostEqual(potrebnyObvod, 94.0, places=1)
        self.assertAlmostEqual(idealniObvod, 29.92, places=1)
        
        # Use case 2: Finer pitch
        pocetVrypu, potrebnyObvod, idealniObvod = count_crest_num4_dia(1.5, 25)
        self.assertEqual(pocetVrypu, 52)
        self.assertAlmostEqual(potrebnyObvod, 78.0, places=1)
        self.assertAlmostEqual(idealniObvod, 24.83, places=1)
        
        # Use case 3: Coarser pitch
        pocetVrypu, potrebnyObvod, idealniObvod = count_crest_num4_dia(2.5, 35)
        self.assertEqual(pocetVrypu, 43)
        self.assertAlmostEqual(potrebnyObvod, 107.5, places=1)
        self.assertAlmostEqual(idealniObvod, 34.22, places=1)
        
        # Use case 4: Very fine pitch
        pocetVrypu, potrebnyObvod, idealniObvod = count_crest_num4_dia(1.0, 20)
        self.assertEqual(pocetVrypu, 62)
        self.assertAlmostEqual(potrebnyObvod, 62.0, places=1)
        self.assertAlmostEqual(idealniObvod, 19.74, places=1)
        
        # Use case 5: Coarse pitch, large diameter
        pocetVrypu, potrebnyObvod, idealniObvod = count_crest_num4_dia(3.0, 40)
        self.assertEqual(pocetVrypu, 41)
        self.assertAlmostEqual(potrebnyObvod, 123.0, places=1)
        self.assertAlmostEqual(idealniObvod, 39.15, places=1)
        
        # Use case 6: Fine pitch, small diameter
        pocetVrypu, potrebnyObvod, idealniObvod = count_crest_num4_dia(1.2, 15)
        self.assertEqual(pocetVrypu, 39)
        self.assertAlmostEqual(potrebnyObvod, 46.8, places=1)
        self.assertAlmostEqual(idealniObvod, 14.90, places=1)


if __name__ == '__main__':
    unittest.main()