#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Unit tests for materialOhyb module.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
sys.path.append(os.path.join(os.path.dirname(__file__), '../DaPTools/src'))
import daptools.mathPhys as mathPhys
import daptools.myTools as myTools


class MaterialOhyb:
    """Trida pro vypocet materialu na ohyb."""
    
    def calculate_bend_length(self, tloustka_mm, radius_mm, uhel_deg):
        """Vypocte delku materialu potrebnou pro ohyb.
        :param tloustka_mm: tloustka materialu v mm
        :param radius_mm: radius ohybu v mm  
        :param uhel_deg: uhel ohybu ve stupnich
        :return: tuple (delka_vnejs, delka_vnitrek, delka_material) v mm
        """
        tloustka = myTools.convert_mm_2_in(tloustka_mm)
        radius = myTools.convert_mm_2_in(radius_mm)
        ang = mathPhys.deg2rad(uhel_deg)
        
        x = 0.4 * tloustka
        if radius < (2 * tloustka):
            x = 0.3333 * tloustka
        if radius > (4 * tloustka):
            x = 0.5 * tloustka
            
        pridavek = ang * (radius + x)
        lvnejsi = ang * (radius + tloustka)
        lvnitrni = ang * radius
        
        return (myTools.convert_in_2_mm(lvnejsi), 
                myTools.convert_in_2_mm(lvnitrni), 
                myTools.convert_in_2_mm(pridavek))


class TestMaterialOhyb(unittest.TestCase):

    def setUp(self):
        self.material = MaterialOhyb()

    def test_calculate_bend_length_90_degrees(self):
        # Use case 1: Standard steel sheet
        vnejs, vnitrek, material = self.material.calculate_bend_length(3, 76, 90.0)
        self.assertAlmostEqual(vnejs, 124.09, places=1)
        self.assertAlmostEqual(vnitrek, 119.38, places=1)
        self.assertAlmostEqual(material, 121.74, places=1)
        
        # Use case 2: Thin material, medium radius
        vnejs, vnitrek, material = self.material.calculate_bend_length(2, 20, 90.0)
        self.assertAlmostEqual(vnejs, 34.56, places=1)
        self.assertAlmostEqual(vnitrek, 31.42, places=1)
        self.assertAlmostEqual(material, 32.99, places=1)
        
        # Use case 3: Thick material, large radius
        vnejs, vnitrek, material = self.material.calculate_bend_length(4, 100, 90.0)
        self.assertAlmostEqual(vnejs, 163.36, places=1)
        self.assertAlmostEqual(vnitrek, 157.08, places=1)
        self.assertAlmostEqual(material, 160.22, places=1)

    def test_calculate_bend_length_45_degrees(self):
        # Use case 1: Medium thickness, medium radius
        vnejs, vnitrek, material = self.material.calculate_bend_length(2, 50, 45.0)
        self.assertAlmostEqual(vnejs, 40.84, places=1)
        self.assertAlmostEqual(vnitrek, 39.27, places=1)
        self.assertAlmostEqual(material, 40.06, places=1)
        
        # Use case 2: Thin material, small angle
        vnejs, vnitrek, material = self.material.calculate_bend_length(1, 10, 30.0)
        self.assertAlmostEqual(vnejs, 5.76, places=1)
        self.assertAlmostEqual(vnitrek, 5.24, places=1)
        self.assertAlmostEqual(material, 5.50, places=1)
        
        # Use case 3: Thick material, large radius, small angle
        vnejs, vnitrek, material = self.material.calculate_bend_length(3, 80, 60.0)
        self.assertAlmostEqual(vnejs, 86.92, places=1)
        self.assertAlmostEqual(vnitrek, 83.78, places=1)
        self.assertAlmostEqual(material, 85.35, places=1)

    def test_calculate_bend_length_small_radius(self):
        # Use case 1: Very small radius (< 2 * thickness)
        vnejs, vnitrek, material = self.material.calculate_bend_length(5, 8, 90.0)
        self.assertAlmostEqual(vnejs, 20.42, places=1)
        self.assertAlmostEqual(vnitrek, 12.57, places=1)
        self.assertAlmostEqual(material, 15.18, places=1)
        
        # Use case 2: Small radius, thin material
        vnejs, vnitrek, material = self.material.calculate_bend_length(2, 3, 90.0)
        self.assertAlmostEqual(vnejs, 7.85, places=1)
        self.assertAlmostEqual(vnitrek, 4.71, places=1)
        self.assertAlmostEqual(material, 5.76, places=1)
        
        # Use case 3: Small radius, 180 degree bend
        vnejs, vnitrek, material = self.material.calculate_bend_length(3, 5, 180.0)
        self.assertAlmostEqual(vnejs, 25.13, places=1)
        self.assertAlmostEqual(vnitrek, 15.71, places=1)
        self.assertAlmostEqual(material, 18.85, places=1)

    def test_calculate_bend_length_large_radius(self):
        # Use case 1: Large radius (> 4 * thickness)
        vnejs, vnitrek, material = self.material.calculate_bend_length(2, 20, 90.0)
        self.assertAlmostEqual(vnejs, 34.56, places=1)
        self.assertAlmostEqual(vnitrek, 31.42, places=1)
        self.assertAlmostEqual(material, 32.99, places=1)
        
        # Use case 2: Very large radius, full circle
        vnejs, vnitrek, material = self.material.calculate_bend_length(4, 100, 180.0)
        self.assertAlmostEqual(vnejs, 326.73, places=1)
        self.assertAlmostEqual(vnitrek, 314.16, places=1)
        self.assertAlmostEqual(material, 320.44, places=1)
        
        # Use case 3: Large radius, thin material
        vnejs, vnitrek, material = self.material.calculate_bend_length(1, 50, 120.0)
        self.assertAlmostEqual(vnejs, 106.81, places=1)
        self.assertAlmostEqual(vnitrek, 104.72, places=1)
        self.assertAlmostEqual(material, 105.77, places=1)


if __name__ == '__main__':
    unittest.main()