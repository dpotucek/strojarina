#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# -*- coding: utf-8 -*-
"""
Unit tests for sineBar module.
"""

import unittest
from sineBar import calculate_link_sine_bar, calculate_contact_sine_bar


class TestSineBar(unittest.TestCase):

    def test_calculate_link_sine_bar(self):
        # Use case 1: Original test - 10°, 0.375" cylinder, 3" distance
        import unittest.mock
        with unittest.mock.patch('sineBar.tools.num_usr_in', return_value=3):
            result = calculate_link_sine_bar(10, 0.375)
            self.assertAlmostEqual(result, 0.8979, places=3)
            self.assertIsInstance(result, float)
        
        # Use case 2: Larger angle - 15°, 0.5" cylinder, 4" distance
        with unittest.mock.patch('sineBar.tools.num_usr_in', return_value=4):
            result = calculate_link_sine_bar(15, 0.5)
            self.assertAlmostEqual(result, 1.5442, places=3)
        
        # Use case 3: Smaller angle - 5°, 0.25" cylinder, 2" distance
        with unittest.mock.patch('sineBar.tools.num_usr_in', return_value=2):
            result = calculate_link_sine_bar(5, 0.25)
            self.assertAlmostEqual(result, 0.4245, places=3)
        
        # Use case 4: Large angle - 20°, 0.75" cylinder, 5" distance
        with unittest.mock.patch('sineBar.tools.num_usr_in', return_value=5):
            result = calculate_link_sine_bar(20, 0.75)
            self.assertAlmostEqual(result, 2.4865, places=3)
        
        # Use case 5: Medium angle - 7.5°, 0.3" cylinder, 2.5" distance
        with unittest.mock.patch('sineBar.tools.num_usr_in', return_value=2.5):
            result = calculate_link_sine_bar(7.5, 0.3)
            self.assertAlmostEqual(result, 0.6270, places=3)
        
        # Use case 6: Different setup - 12°, 0.4" cylinder, 3.5" distance
        with unittest.mock.patch('sineBar.tools.num_usr_in', return_value=3.5):
            result = calculate_link_sine_bar(12, 0.4)
            self.assertAlmostEqual(result, 1.1317, places=3)

    def test_calculate_contact_sine_bar(self):
        # Use case 1: Original test - 1.5°, 0.75" cylinder
        result = calculate_contact_sine_bar(1.5, 0.75)
        self.assertAlmostEqual(result, 0.7306, places=3)
        
        # Use case 2: Larger angle and cylinder - 5°, 1.0" cylinder
        result = calculate_contact_sine_bar(5.0, 1.0)
        self.assertAlmostEqual(result, 0.9164, places=3)
        
        # Use case 3: Even larger - 10°, 2.0" cylinder
        result = calculate_contact_sine_bar(10.0, 2.0)
        self.assertAlmostEqual(result, 1.6793, places=3)
        
        # Use case 4: Medium angle, small cylinder - 2.5°, 0.5" cylinder
        result = calculate_contact_sine_bar(2.5, 0.5)
        self.assertAlmostEqual(result, 0.4787, places=3)
        
        # Use case 5: Large angle - 15°, 3.0" cylinder
        result = calculate_contact_sine_bar(15.0, 3.0)
        self.assertAlmostEqual(result, 2.3073, places=3)
        
        # Use case 6: Very small angle - 0.5°, 0.25" cylinder
        result = calculate_contact_sine_bar(0.5, 0.25)
        self.assertAlmostEqual(result, 0.2478, places=3)


if __name__ == '__main__':
    unittest.main()