#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# -*- coding: utf-8 -*-
"""
Unit tests for differentialThread module.
"""

import unittest
from differentialThread import DifferentialThread, calculate_diff_thread, parse_data, vyzkousej_kombinace


class TestDifferentialThread(unittest.TestCase):

    def setUp(self):
        self.dt = DifferentialThread()

    def test_calculate_diff_thread_class(self):
        # Use case 1: Original test
        result = self.dt.calculate_diff_thread(2.0, 1.5)
        self.assertAlmostEqual(result, 6.0, places=2)
        
        # Use case 2: Close pitches
        result = self.dt.calculate_diff_thread(3.0, 2.5)
        self.assertAlmostEqual(result, 15.0, places=2)
        
        # Use case 3: Small pitches
        result = self.dt.calculate_diff_thread(1.0, 0.8)
        self.assertAlmostEqual(result, 4.0, places=2)
        
        # Use case 4: Large difference
        result = self.dt.calculate_diff_thread(4.0, 1.5)
        self.assertAlmostEqual(result, 2.4, places=2)
        
        # Use case 5: 2:1 ratio
        result = self.dt.calculate_diff_thread(2.5, 1.25)
        self.assertAlmostEqual(result, 2.5, places=2)
        
        # Use case 6: Very close pitches
        result = self.dt.calculate_diff_thread(1.5, 1.2)
        self.assertAlmostEqual(result, 6.0, places=2)
        
        # Error cases
        with self.assertRaises(ValueError):
            self.dt.calculate_diff_thread(0, 1.5)
        
        with self.assertRaises(ValueError):
            self.dt.calculate_diff_thread(2.0, 2.0)

    def test_parse_data_class(self):
        # Use case 1: Original test
        test_data = ['tpi\n', '20\n', '24\n', 'mm\n', '1.5\n', '2.0\n']
        tpi, mm = self.dt.parse_data(test_data)
        self.assertEqual(tpi, (20.0, 24.0))
        self.assertEqual(mm, (1.5, 2.0))
        
        # Use case 2: More TPI values
        test_data2 = ['tpi\n', '16\n', '18\n', '20\n', 'mm\n', '1.0\n', '1.25\n', '1.5\n']
        tpi, mm = self.dt.parse_data(test_data2)
        self.assertEqual(tpi, (16.0, 18.0, 20.0))
        self.assertEqual(mm, (1.0, 1.25, 1.5))
        
        # Use case 3: Fewer values
        test_data3 = ['tpi\n', '24\n', '28\n', 'mm\n', '0.8\n', '1.0\n']
        tpi, mm = self.dt.parse_data(test_data3)
        self.assertEqual(tpi, (24.0, 28.0))
        self.assertEqual(mm, (0.8, 1.0))
        
        # Use case 4: More MM values
        test_data4 = ['tpi\n', '12\n', '14\n', '16\n', '18\n', 'mm\n', '2.0\n', '2.5\n', '3.0\n']
        tpi, mm = self.dt.parse_data(test_data4)
        self.assertEqual(tpi, (12.0, 14.0, 16.0, 18.0))
        self.assertEqual(mm, (2.0, 2.5, 3.0))

    def test_vyzkousej_kombinace_class(self):
        # Use case 1: Original test
        tpi = (20.0, 24.0)
        mm = (1.5, 2.0)
        result = self.dt.vyzkousej_kombinace(6.0, tpi, mm, 'mm')
        self.assertEqual(len(result), 3)
        
        # Use case 2: More values, mm units
        tpi = (16.0, 18.0, 20.0, 24.0)
        mm = (1.0, 1.25, 1.5, 2.0)
        result = self.dt.vyzkousej_kombinace(3.5, tpi, mm, 'mm')
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[2], 3.333, places=2)
        
        # Use case 3: Different target value
        result = self.dt.vyzkousej_kombinace(8.0, tpi, mm, 'mm')
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[2], 7.5, places=1)
        
        # Use case 4: Inch units
        result = self.dt.vyzkousej_kombinace(15.0, tpi, mm, 'in')
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[2], 48.0, places=1)
        
        # Use case 5: Small target value
        result = self.dt.vyzkousej_kombinace(2.8, tpi, mm, 'mm')
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[2], 3.0, places=1)
        
        # Use case 6: Different combination
        result = self.dt.vyzkousej_kombinace(5.2, tpi, mm, 'mm')
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[2], 5.0, places=1)

    def test_calculate_diff_thread_function(self):
        # Use case 1: Original test
        result = calculate_diff_thread(2.0, 1.5)
        self.assertAlmostEqual(result, 6.0, places=2)
        
        # Use case 2: Large pitches
        result = calculate_diff_thread(5.0, 2.0)
        self.assertAlmostEqual(result, 3.333, places=2)
        
        # Use case 3: Very close pitches
        result = calculate_diff_thread(1.5, 1.2)
        self.assertAlmostEqual(result, 6.0, places=2)
        
        # Use case 4: Different ratio
        result = calculate_diff_thread(2.5, 1.25)
        self.assertAlmostEqual(result, 2.5, places=2)
        
        # Error cases
        with self.assertRaises(ValueError):
            calculate_diff_thread(0, 1.5)
        
        with self.assertRaises(ValueError):
            calculate_diff_thread(2.0, 2.0)

    def test_parse_data_function(self):
        # Use case 1: Original test
        test_data = ['tpi\n', '20\n', '24\n', 'mm\n', '1.5\n', '2.0\n']
        tpi, mm = parse_data(test_data)
        self.assertEqual(tpi, (20.0, 24.0))
        self.assertEqual(mm, (1.5, 2.0))
        
        # Use case 2: Extended dataset
        test_data2 = ['tpi\n', '16\n', '18\n', '20\n', 'mm\n', '1.0\n', '1.25\n', '1.5\n']
        tpi, mm = parse_data(test_data2)
        self.assertEqual(tpi, (16.0, 18.0, 20.0))
        self.assertEqual(mm, (1.0, 1.25, 1.5))
        
        # Use case 3: Minimal dataset
        test_data3 = ['tpi\n', '24\n', '28\n', 'mm\n', '0.8\n', '1.0\n']
        tpi, mm = parse_data(test_data3)
        self.assertEqual(tpi, (24.0, 28.0))
        self.assertEqual(mm, (0.8, 1.0))

    def test_vyzkousej_kombinace_function(self):
        # Use case 1: Original test
        tpi = (20.0, 24.0)
        mm = (1.5, 2.0)
        result = vyzkousej_kombinace(6.0, tpi, mm, 'mm')
        self.assertEqual(len(result), 3)
        
        # Use case 2: Extended values
        tpi = (16.0, 18.0, 20.0, 24.0)
        mm = (1.0, 1.25, 1.5, 2.0)
        result = vyzkousej_kombinace(3.5, tpi, mm, 'mm')
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[2], 3.333, places=2)
        
        # Use case 3: Inch units test
        result = vyzkousej_kombinace(12.0, tpi, mm, 'in')
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[2], 48.0, places=1)
        
        # Use case 4: High precision target
        result = vyzkousej_kombinace(5.2, tpi, mm, 'mm')
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[2], 5.0, places=1)


if __name__ == '__main__':
    unittest.main()