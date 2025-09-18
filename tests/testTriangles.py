#!/usr/bin/env python3
"""
Unit tests for triangles.py

Created by David Potucek on Sep 18, 2025
Project: strojarina
"""

import unittest
import math
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from triangles import RightTriangle, CommonTriangle


class TestRightTriangle(unittest.TestCase):
    """Test cases for RightTriangle class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tolerance = 1e-10
    
    def test_two_sides_3_4_5(self):
        """Test classic 3-4-5 right triangle."""
        triangle = RightTriangle(a=3, b=4)
        
        self.assertAlmostEqual(triangle.a, 3.0, places=10)
        self.assertAlmostEqual(triangle.b, 4.0, places=10)
        self.assertAlmostEqual(triangle.c, 5.0, places=10)
        self.assertAlmostEqual(triangle.angle_A, 36.869897645844, places=6)
        self.assertAlmostEqual(triangle.angle_B, 53.130102354156, places=6)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_side_and_opposite_angle(self):
        """Test calculation from side and its opposite angle."""
        triangle = RightTriangle(a=3, angle_A=30)
        
        self.assertAlmostEqual(triangle.a, 3.0, places=10)
        self.assertAlmostEqual(triangle.angle_A, 30.0, places=10)
        self.assertAlmostEqual(triangle.angle_B, 60.0, places=10)
        self.assertAlmostEqual(triangle.b, 3 * math.sqrt(3), places=6)
        self.assertAlmostEqual(triangle.c, 6.0, places=6)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_side_and_adjacent_angle(self):
        """Test calculation from side and adjacent angle."""
        triangle = RightTriangle(a=5, angle_B=45)
        
        self.assertAlmostEqual(triangle.a, 5.0, places=10)
        self.assertAlmostEqual(triangle.b, 5.0, places=10)
        self.assertAlmostEqual(triangle.angle_A, 45.0, places=10)
        self.assertAlmostEqual(triangle.angle_B, 45.0, places=10)
        self.assertAlmostEqual(triangle.c, 5 * math.sqrt(2), places=6)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_hypotenuse_and_side(self):
        """Test calculation from hypotenuse and one side."""
        triangle = RightTriangle(c=10, a=6)
        
        self.assertAlmostEqual(triangle.c, 10.0, places=10)
        self.assertAlmostEqual(triangle.a, 6.0, places=10)
        self.assertAlmostEqual(triangle.b, 8.0, places=10)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_hypotenuse_and_angle(self):
        """Test calculation from hypotenuse and angle."""
        triangle = RightTriangle(c=10, angle_A=30)
        
        self.assertAlmostEqual(triangle.c, 10.0, places=10)
        self.assertAlmostEqual(triangle.angle_A, 30.0, places=10)
        self.assertAlmostEqual(triangle.angle_B, 60.0, places=10)
        self.assertAlmostEqual(triangle.a, 5.0, places=6)
        self.assertAlmostEqual(triangle.b, 5 * math.sqrt(3), places=6)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_area_calculation(self):
        """Test area calculation."""
        triangle = RightTriangle(a=3, b=4)
        self.assertAlmostEqual(triangle.get_area(), 6.0, places=10)
    
    def test_perimeter_calculation(self):
        """Test perimeter calculation."""
        triangle = RightTriangle(a=3, b=4)
        self.assertAlmostEqual(triangle.get_perimeter(), 12.0, places=10)
    
    def test_invalid_inputs(self):
        """Test error handling for invalid inputs."""
        
        # Test insufficient parameters
        with self.assertRaises(ValueError):
            RightTriangle(a=3)
        
        # Test too many parameters
        with self.assertRaises(ValueError):
            RightTriangle(a=3, b=4, c=5)
        
        # Test negative values
        with self.assertRaises(ValueError):
            RightTriangle(a=-3, b=4)
        
        # Test zero values
        with self.assertRaises(ValueError):
            RightTriangle(a=0, b=4)
        
        # Test invalid angle (>= 90)
        with self.assertRaises(ValueError):
            RightTriangle(a=3, angle_A=90)
        
        # Test side >= hypotenuse
        with self.assertRaises(ValueError):
            RightTriangle(c=5, a=6)
        
        # Test NaN values
        with self.assertRaises(ValueError):
            RightTriangle(a=float('nan'), b=4)
        
        # Test infinite values
        with self.assertRaises(ValueError):
            RightTriangle(a=float('inf'), b=4)
        
        # Test non-numeric values
        with self.assertRaises(ValueError):
            RightTriangle(a="invalid", b=4)
    
    def test_insolvable_combinations(self):
        """Test error handling for insolvable parameter combinations."""
        
        # Test two angles only (no size information)
        with self.assertRaises(ValueError):
            RightTriangle(angle_A=30, angle_B=60)
        
        # Test inconsistent angles (don't sum to 90°)
        with self.assertRaises(ValueError):
            RightTriangle(angle_A=30, angle_B=70)
        
        # Test inconsistent parameters (over-constrained)
        with self.assertRaises(ValueError):
            # This should fail: if c=10 and angle_A=30°, then a should be 5, not 6
            RightTriangle(c=10, a=6, angle_A=30)
        
        with self.assertRaises(ValueError):
            # This should fail: if c=10 and angle_B=45°, then b should be ~7.07, not 5
            RightTriangle(c=10, b=5, angle_B=45)
    
    def test_edge_cases(self):
        """Test edge cases."""
        
        # Very small triangle
        triangle = RightTriangle(a=0.001, b=0.001)
        self.assertTrue(triangle.verify_mollweide())
        
        # Very large triangle
        triangle = RightTriangle(a=1000000, b=1000000)
        self.assertTrue(triangle.verify_mollweide())
        
        # Very acute angle
        triangle = RightTriangle(a=1, angle_A=1)
        self.assertTrue(triangle.verify_mollweide())
        
        # Very obtuse angle (close to 90°)
        triangle = RightTriangle(a=1, angle_A=89)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_string_representations(self):
        """Test string representations."""
        triangle = RightTriangle(a=3, b=4)
        
        str_repr = str(triangle)
        self.assertIn("3.000", str_repr)
        self.assertIn("4.000", str_repr)
        self.assertIn("5.000", str_repr)
        
        repr_str = repr(triangle)
        self.assertIn("RightTriangle", repr_str)
        self.assertIn("a=3", repr_str)
        self.assertIn("b=4", repr_str)
    
    def test_mollweide_verification(self):
        """Test Mollweide equation verification with various triangles."""
        
        # Test multiple triangle configurations
        test_cases = [
            {'a': 3, 'b': 4},
            {'a': 5, 'b': 12},
            {'a': 8, 'b': 15},
            {'c': 13, 'a': 5},
            {'c': 25, 'angle_A': 30},
        ]
        
        for case in test_cases:
            triangle = RightTriangle(**case)
            self.assertTrue(triangle.verify_mollweide(), 
                          f"Mollweide verification failed for {case}")
    
    def test_pythagorean_theorem(self):
        """Test that all triangles satisfy Pythagorean theorem."""
        
        test_cases = [
            {'a': 3, 'b': 4},
            {'a': 5, 'b': 12},
            {'c': 10, 'a': 6},
            {'c': 15, 'angle_A': 45},
        ]
        
        for case in test_cases:
            triangle = RightTriangle(**case)
            # Check a² + b² = c²
            self.assertAlmostEqual(
                triangle.a**2 + triangle.b**2, 
                triangle.c**2, 
                places=10,
                msg=f"Pythagorean theorem failed for {case}"
            )
    
    def test_angle_sum(self):
        """Test that angles sum to 180°."""
        
        test_cases = [
            {'a': 3, 'b': 4},
            {'c': 10, 'angle_A': 30},
            {'a': 7, 'angle_B': 60},
        ]
        
        for case in test_cases:
            triangle = RightTriangle(**case)
            angle_sum = triangle.angle_A + triangle.angle_B + triangle.angle_C
            self.assertAlmostEqual(angle_sum, 180.0, places=10,
                                 msg=f"Angle sum failed for {case}")
    
    def test_consistency_validation(self):
        """Test that consistent over-constrained parameters are accepted."""
        
        # These should work because parameters are consistent
        # c=10, angle_A=30° implies a=5
        triangle = RightTriangle(c=10, angle_A=30)
        self.assertAlmostEqual(triangle.a, 5.0, places=6)
        
        # Verify the triangle is valid
        self.assertTrue(triangle.verify_mollweide())
        
        # Test with exact consistent values (within tolerance)
        triangle2 = RightTriangle(a=3, b=4)  # This creates c=5
        # Now verify we can create the same triangle with c and one side
        triangle3 = RightTriangle(c=5, a=3)
        self.assertAlmostEqual(triangle3.b, 4.0, places=10)


    def test_mathematical_limits(self):
        """Test mathematical edge cases and limits."""
        
        # Test very small angles
        triangle = RightTriangle(a=1, angle_A=0.1)  # Very small angle
        self.assertTrue(triangle.verify_mollweide())
        
        # Test angles very close to 90°
        triangle = RightTriangle(a=1000, angle_A=89.9)  # Very large angle
        self.assertTrue(triangle.verify_mollweide())
        
        # Test extreme aspect ratios
        triangle = RightTriangle(a=0.001, b=1000)  # Very thin triangle
        self.assertTrue(triangle.verify_mollweide())


class TestCommonTriangle(unittest.TestCase):
    """Test cases for CommonTriangle class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tolerance = 1e-6
    
    def test_three_sides_3_4_5(self):
        """Test triangle from three sides (3-4-5 right triangle)."""
        triangle = CommonTriangle(a=3, b=4, c=5)
        
        self.assertAlmostEqual(triangle.a, 3.0, places=10)
        self.assertAlmostEqual(triangle.b, 4.0, places=10)
        self.assertAlmostEqual(triangle.c, 5.0, places=10)
        self.assertTrue(triangle.is_right_triangle())
        self.assertTrue(triangle.verify_mollweide())
    
    def test_equilateral_triangle(self):
        """Test equilateral triangle."""
        triangle = CommonTriangle(a=5, b=5, c=5)
        
        self.assertAlmostEqual(triangle.angle_A, 60.0, places=6)
        self.assertAlmostEqual(triangle.angle_B, 60.0, places=6)
        self.assertAlmostEqual(triangle.angle_C, 60.0, places=6)
        self.assertTrue(triangle.is_equilateral())
        self.assertTrue(triangle.verify_mollweide())
    
    def test_isosceles_triangle(self):
        """Test isosceles triangle."""
        triangle = CommonTriangle(a=5, b=5, c=8)
        
        self.assertAlmostEqual(triangle.angle_A, triangle.angle_B, places=6)
        self.assertTrue(triangle.is_isosceles())
        self.assertTrue(triangle.verify_mollweide())
    
    def test_two_sides_one_angle(self):
        """Test calculation from two sides and included angle."""
        triangle = CommonTriangle(a=7, b=10, angle_C=60)
        
        # Using law of cosines: c² = a² + b² - 2ab*cos(C)
        expected_c = math.sqrt(7**2 + 10**2 - 2*7*10*math.cos(math.radians(60)))
        self.assertAlmostEqual(triangle.c, expected_c, places=6)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_one_side_two_angles(self):
        """Test calculation from one side and two angles."""
        triangle = CommonTriangle(a=10, angle_B=45, angle_C=75)
        
        # Third angle should be 180 - 45 - 75 = 60
        self.assertAlmostEqual(triangle.angle_A, 60.0, places=6)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_area_calculation(self):
        """Test area calculation using Heron's formula."""
        triangle = CommonTriangle(a=3, b=4, c=5)
        self.assertAlmostEqual(triangle.get_area(), 6.0, places=10)
        
        # Test equilateral triangle area
        triangle_eq = CommonTriangle(a=6, b=6, c=6)
        expected_area = (math.sqrt(3) / 4) * 6**2
        self.assertAlmostEqual(triangle_eq.get_area(), expected_area, places=6)
    
    def test_perimeter_calculation(self):
        """Test perimeter calculation."""
        triangle = CommonTriangle(a=3, b=4, c=5)
        self.assertAlmostEqual(triangle.get_perimeter(), 12.0, places=10)
    
    def test_invalid_inputs(self):
        """Test error handling for invalid inputs."""
        
        # Test insufficient parameters
        with self.assertRaises(ValueError):
            CommonTriangle(a=3, b=4)
        
        # Test too many parameters
        with self.assertRaises(ValueError):
            CommonTriangle(a=3, b=4, c=5, angle_A=60)
        
        # Test triangle inequality violation
        with self.assertRaises(ValueError):
            CommonTriangle(a=1, b=2, c=5)  # 1 + 2 < 5
        
        # Test invalid angle sum
        with self.assertRaises(ValueError):
            CommonTriangle(angle_A=90, angle_B=100, angle_C=50)  # Sum > 180
        
        # Test negative values
        with self.assertRaises(ValueError):
            CommonTriangle(a=-3, b=4, c=5)
        
        # Test zero values
        with self.assertRaises(ValueError):
            CommonTriangle(a=0, b=4, c=5)
        
        # Test angles >= 180
        with self.assertRaises(ValueError):
            CommonTriangle(a=5, angle_A=180, angle_B=45)
    
    def test_triangle_types(self):
        """Test triangle type detection."""
        
        # Right triangle
        right_triangle = CommonTriangle(a=3, b=4, c=5)
        self.assertTrue(right_triangle.is_right_triangle())
        self.assertFalse(right_triangle.is_equilateral())
        self.assertFalse(right_triangle.is_isosceles())
        
        # Equilateral triangle
        equilateral = CommonTriangle(a=5, b=5, c=5)
        self.assertTrue(equilateral.is_equilateral())
        self.assertTrue(equilateral.is_isosceles())  # Equilateral is also isosceles
        self.assertFalse(equilateral.is_right_triangle())
        
        # Isosceles triangle
        isosceles = CommonTriangle(a=5, b=5, c=8)
        self.assertTrue(isosceles.is_isosceles())
        self.assertFalse(isosceles.is_equilateral())
        self.assertFalse(isosceles.is_right_triangle())
    
    def test_mollweide_verification(self):
        """Test Mollweide equation verification with various triangles."""
        
        test_cases = [
            {'a': 3, 'b': 4, 'c': 5},
            {'a': 6, 'b': 8, 'c': 10},
            {'a': 5, 'b': 5, 'c': 5},
            {'a': 7, 'b': 10, 'angle_C': 60},
            {'a': 10, 'angle_B': 45, 'angle_C': 75},
        ]
        
        for case in test_cases:
            triangle = CommonTriangle(**case)
            self.assertTrue(triangle.verify_mollweide(), 
                          f"Mollweide verification failed for {case}")
    
    def test_angle_sum(self):
        """Test that angles sum to 180°."""
        
        test_cases = [
            {'a': 3, 'b': 4, 'c': 5},
            {'a': 7, 'b': 10, 'angle_C': 60},
            {'a': 10, 'angle_B': 45, 'angle_C': 75},
        ]
        
        for case in test_cases:
            triangle = CommonTriangle(**case)
            angle_sum = triangle.angle_A + triangle.angle_B + triangle.angle_C
            self.assertAlmostEqual(angle_sum, 180.0, places=10,
                                 msg=f"Angle sum failed for {case}")
    
    def test_string_representations(self):
        """Test string representations."""
        triangle = CommonTriangle(a=3, b=4, c=5)
        
        str_repr = str(triangle)
        self.assertIn("3.000", str_repr)
        self.assertIn("4.000", str_repr)
        self.assertIn("5.000", str_repr)
        
        repr_str = repr(triangle)
        self.assertIn("CommonTriangle", repr_str)
        self.assertIn("a=3", repr_str)
        self.assertIn("b=4", repr_str)
    
    def test_edge_cases(self):
        """Test edge cases and extreme triangles."""
        
        # Very thin triangle
        triangle = CommonTriangle(a=0.001, b=1000, c=1000)
        self.assertTrue(triangle.verify_mollweide())
        
        # Very obtuse triangle
        triangle = CommonTriangle(a=10, angle_A=150, angle_B=15)
        self.assertTrue(triangle.verify_mollweide())
        
        # Very acute triangle
        triangle = CommonTriangle(a=10, b=10, c=2)
        self.assertTrue(triangle.verify_mollweide())


class TestTrianglePerformance(unittest.TestCase):
    """Performance and stress tests for triangle classes."""
    
    def test_large_scale_calculations(self):
        """Test calculations with large numbers."""
        triangle = RightTriangle(a=1e6, b=1e6)
        self.assertAlmostEqual(triangle.c, math.sqrt(2) * 1e6, places=0)
        self.assertTrue(triangle.verify_mollweide())
        
        triangle = RightTriangle(a=1e-6, b=1e-6)
        self.assertAlmostEqual(triangle.c, math.sqrt(2) * 1e-6, places=12)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_special_triangles(self):
        """Test special mathematical triangles."""
        # 30-60-90 triangle
        triangle = RightTriangle(angle_A=30, c=2)
        self.assertAlmostEqual(triangle.a, 1.0, places=6)
        self.assertAlmostEqual(triangle.b, math.sqrt(3), places=6)
        
        # 45-45-90 triangle
        triangle = RightTriangle(angle_A=45, c=math.sqrt(2))
        self.assertAlmostEqual(triangle.a, 1.0, places=6)
        self.assertAlmostEqual(triangle.b, 1.0, places=6)


class TestTriangleEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_degenerate_cases(self):
        """Test near-degenerate triangles."""
        triangle = CommonTriangle(a=1000, b=1000, c=0.001)
        self.assertTrue(triangle.verify_mollweide())
        
        triangle = CommonTriangle(a=0.001, b=1000, c=1000)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_boundary_angles(self):
        """Test triangles with angles at boundaries."""
        triangle = CommonTriangle(a=1, angle_A=179.9, angle_B=0.05)
        self.assertTrue(triangle.verify_mollweide())
        
        triangle = CommonTriangle(a=1, angle_A=0.1, angle_B=89.9)
        self.assertTrue(triangle.verify_mollweide())
    
    def test_consistency_across_methods(self):
        """Test that different calculation methods give consistent results."""
        triangle1 = RightTriangle(a=3, b=4)
        triangle2 = RightTriangle(c=5, a=3)
        triangle3 = RightTriangle(c=5, angle_A=36.869897645844)
        
        self.assertAlmostEqual(triangle1.c, triangle2.c, places=6)
        self.assertAlmostEqual(triangle1.c, triangle3.c, places=6)
        self.assertAlmostEqual(triangle1.angle_A, triangle3.angle_A, places=6)
    
    def test_area_calculations_comprehensive(self):
        """Test area calculations for various triangle types."""
        triangle = RightTriangle(a=6, b=8)
        self.assertAlmostEqual(triangle.get_area(), 24.0, places=10)
        
        side = 6
        triangle = CommonTriangle(a=side, b=side, c=side)
        expected_area = (math.sqrt(3) / 4) * side**2
        self.assertAlmostEqual(triangle.get_area(), expected_area, places=6)
        
        triangle = CommonTriangle(a=13, b=14, c=15)
        self.assertAlmostEqual(triangle.get_area(), 84.0, places=6)


class TestTriangleIntegration(unittest.TestCase):
    """Integration tests combining multiple features."""
    
    def test_triangle_conversion(self):
        """Test converting between RightTriangle and CommonTriangle."""
        right_tri = RightTriangle(a=3, b=4)
        common_tri = CommonTriangle(a=3, b=4, c=5)
        
        self.assertAlmostEqual(right_tri.a, common_tri.a, places=10)
        self.assertAlmostEqual(right_tri.b, common_tri.b, places=10)
        self.assertAlmostEqual(right_tri.c, common_tri.c, places=10)
        self.assertAlmostEqual(right_tri.get_area(), common_tri.get_area(), places=10)
        self.assertTrue(common_tri.is_right_triangle())
    
    def test_batch_calculations(self):
        """Test batch processing of multiple triangles."""
        triangles = [
            RightTriangle(a=3, b=4),
            RightTriangle(a=5, b=12),
            CommonTriangle(a=7, b=8, c=9),
            CommonTriangle(a=10, b=10, c=10),
        ]
        
        for triangle in triangles:
            self.assertTrue(triangle.verify_mollweide())
            self.assertGreater(triangle.get_area(), 0)
            self.assertGreater(triangle.get_perimeter(), 0)


if __name__ == '__main__':
    unittest.main()