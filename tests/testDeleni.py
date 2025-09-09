#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for deleni module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from deleni import DeliciHlava, prozkoumej_deleni, vypocti_pocet_der


class TestDeleni(unittest.TestCase):

    def setUp(self):
        self.hlava = DeliciHlava()

    def test_prozkoumej_deleni_class(self):
        # Use case 1: Standard hole count
        result = self.hlava.prozkoumej_deleni(43)
        self.assertIn(40, result)
        self.assertIn(43, result)
        self.assertTrue(all(isinstance(x, int) for x in result))
        
        # Use case 2: Small hole count
        result = self.hlava.prozkoumej_deleni(24)
        self.assertEqual(len(result), 27)
        self.assertTrue(all(isinstance(x, int) for x in result))
        
        # Use case 3: Medium hole count
        result = self.hlava.prozkoumej_deleni(30)
        self.assertEqual(len(result), 29)
        self.assertTrue(all(isinstance(x, int) for x in result))
        
        # Use case 4: Prime number holes
        result = self.hlava.prozkoumej_deleni(37)
        self.assertEqual(len(result), 15)
        self.assertTrue(all(isinstance(x, int) for x in result))

    def test_vypocti_pocet_der_class(self):
        # Original use cases
        self.assertEqual(self.hlava.vypocti_pocet_der(40), 1)
        self.assertEqual(self.hlava.vypocti_pocet_der(20), 1)
        self.assertEqual(self.hlava.vypocti_pocet_der(17), 17)
        self.assertEqual(self.hlava.vypocti_pocet_der(28), 7)
        self.assertEqual(self.hlava.vypocti_pocet_der(105), 21)
        
        # Additional use cases
        self.assertEqual(self.hlava.vypocti_pocet_der(8), 1)
        self.assertEqual(self.hlava.vypocti_pocet_der(12), 3)
        self.assertEqual(self.hlava.vypocti_pocet_der(15), 3)
        self.assertEqual(self.hlava.vypocti_pocet_der(24), 3)
        self.assertEqual(self.hlava.vypocti_pocet_der(30), 3)
        self.assertEqual(self.hlava.vypocti_pocet_der(60), 3)

    def test_prozkoumej_deleni_function(self):
        # Use case 1: Standard hole count
        result = prozkoumej_deleni(43, 40)
        self.assertIn(40, result)
        self.assertIn(43, result)
        self.assertTrue(all(isinstance(x, int) for x in result))
        
        # Use case 2: Large hole count
        result = prozkoumej_deleni(49, 40)
        self.assertEqual(len(result), 23)
        self.assertTrue(all(isinstance(x, int) for x in result))
        
        # Use case 3: Even larger hole count
        result = prozkoumej_deleni(54, 40)
        self.assertEqual(len(result), 39)
        self.assertTrue(all(isinstance(x, int) for x in result))
        
        # Use case 4: Very large hole count
        result = prozkoumej_deleni(66, 40)
        self.assertEqual(len(result), 39)
        self.assertTrue(all(isinstance(x, int) for x in result))

    def test_vypocti_pocet_der_function(self):
        # Original use cases
        self.assertEqual(vypocti_pocet_der(40, 40), 1)
        self.assertEqual(vypocti_pocet_der(20, 40), 1)
        self.assertEqual(vypocti_pocet_der(17, 40), 17)
        self.assertEqual(vypocti_pocet_der(28, 40), 7)
        self.assertEqual(vypocti_pocet_der(105, 40), 21)
        
        # Additional use cases - simple divisions
        self.assertEqual(vypocti_pocet_der(8, 40), 1)
        self.assertEqual(vypocti_pocet_der(12, 40), 3)
        self.assertEqual(vypocti_pocet_der(15, 40), 3)
        
        # Additional use cases - common divisions
        self.assertEqual(vypocti_pocet_der(24, 40), 3)
        self.assertEqual(vypocti_pocet_der(30, 40), 3)
        self.assertEqual(vypocti_pocet_der(60, 40), 3)


if __name__ == '__main__':
    unittest.main()