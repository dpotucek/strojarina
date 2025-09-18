#!/usr/bin/env python3
'''
Pocita trojuhelniky a overuje je Mollweide rovnici

Created by David Potucek on Sep 18, 2025
Project: strojarina
File: triangles.py
'''

import math


class RightTriangle:
    """Class for right triangle calculations with Mollweide equation verification."""
    
    def __init__(self, **kwargs):
        """Initialize triangle with various parameter combinations.
        
        Supported combinations:
        - sides: a, b (calculates c and angles)
        - side_angle: a, angle_A or b, angle_B
        - hypotenuse_side: c, a or c, b
        - hypotenuse_angle: c, angle_A or c, angle_B
        """
        self.a = None  # side opposite to angle A
        self.b = None  # side opposite to angle B  
        self.c = None  # hypotenuse
        self.angle_A = None  # angle opposite to side a (degrees)
        self.angle_B = None  # angle opposite to side b (degrees)
        self.angle_C = 90.0  # right angle
        
        self._validate_and_calculate(**kwargs)
    
    def _validate_input(self, value, name, min_val=0, max_val=None):
        """Validate numeric input parameters."""
        if value is None:
            return None
        
        try:
            val = float(value)
            if math.isnan(val) or math.isinf(val):
                raise ValueError(f"{name} cannot be NaN or infinite")
            if val <= min_val:
                raise ValueError(f"{name} must be greater than {min_val}")
            if max_val and val >= max_val:
                raise ValueError(f"{name} must be less than {max_val}")
            return val
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid {name}: {e}")
    
    def _validate_and_calculate(self, **kwargs):
        """Validate inputs and calculate missing parameters."""
        # Validate inputs
        a = self._validate_input(kwargs.get('a'), 'side a')
        b = self._validate_input(kwargs.get('b'), 'side b')
        c = self._validate_input(kwargs.get('c'), 'hypotenuse c')
        angle_A = self._validate_input(kwargs.get('angle_A'), 'angle A', 0, 90)
        angle_B = self._validate_input(kwargs.get('angle_B'), 'angle B', 0, 90)
        
        # Count non-None parameters
        params = [a, b, c, angle_A, angle_B]
        given_count = sum(1 for p in params if p is not None)
        
        if given_count < 2:
            raise ValueError("At least 2 parameters required")
        if given_count > 2:
            raise ValueError("Maximum 2 parameters allowed")
        
        # Check for impossible combinations
        if c and (angle_A or angle_B) and (a or b):
            # If we have hypotenuse, angle, and side, verify consistency
            temp_triangle = None
            try:
                if c and angle_A and not (a or b):
                    temp_triangle = True  # This is valid
                elif c and angle_B and not (a or b):
                    temp_triangle = True  # This is valid
                elif c and a and not (angle_A or angle_B):
                    temp_triangle = True  # This is valid
                elif c and b and not (angle_A or angle_B):
                    temp_triangle = True  # This is valid
                else:
                    # Over-constrained system - check consistency
                    if c and a and angle_A:
                        expected_a = c * math.sin(math.radians(angle_A))
                        if abs(a - expected_a) > 1e-10:
                            raise ValueError(f"Inconsistent parameters: side a={a} doesn't match angle A={angle_A}° with hypotenuse c={c}")
                    elif c and b and angle_B:
                        expected_b = c * math.sin(math.radians(angle_B))
                        if abs(b - expected_b) > 1e-10:
                            raise ValueError(f"Inconsistent parameters: side b={b} doesn't match angle B={angle_B}° with hypotenuse c={c}")
            except ValueError:
                raise
        
        # Validate angle combinations
        # Validate angle combinations before processing
        if angle_A and angle_B:
            if abs(angle_A + angle_B - 90) > 1e-10:
                raise ValueError(f"Angles A({angle_A}°) + B({angle_B}°) must equal 90° for right triangle")
        
        # Calculate based on input combination
        if a and b:
            self._from_two_sides(a, b)
        elif a and angle_A:
            self._from_side_opposite_angle(a, angle_A)
        elif b and angle_B:
            self._from_side_opposite_angle(b, angle_B, is_b=True)
        elif a and angle_B:
            self._from_side_adjacent_angle(a, angle_B)
        elif b and angle_A:
            self._from_side_adjacent_angle(b, angle_A, is_b=True)
        elif c and a:
            self._from_hypotenuse_side(c, a)
        elif c and b:
            self._from_hypotenuse_side(c, b, is_b=True)
        elif c and angle_A:
            self._from_hypotenuse_angle(c, angle_A)
        elif c and angle_B:
            self._from_hypotenuse_angle(c, angle_B, is_b=True)
        elif angle_A and angle_B:
            raise ValueError("Cannot determine triangle size from two angles only - need at least one side")
        else:
            raise ValueError("Unsupported parameter combination")
    
    def _from_two_sides(self, a, b):
        """Calculate from two sides."""
        self.a = a
        self.b = b
        self.c = math.sqrt(a**2 + b**2)
        self.angle_A = math.degrees(math.atan(a / b))
        self.angle_B = 90.0 - self.angle_A
    
    def _from_side_opposite_angle(self, side, angle, is_b=False):
        """Calculate from side and its opposite angle."""
        angle_rad = math.radians(angle)
        if is_b:
            self.b = side
            self.angle_B = angle
            self.angle_A = 90.0 - angle
            self.a = side * math.tan(math.radians(self.angle_A))
        else:
            self.a = side
            self.angle_A = angle
            self.angle_B = 90.0 - angle
            self.b = side * math.tan(math.radians(self.angle_B))
        self.c = self.a / math.sin(math.radians(self.angle_A))
    
    def _from_side_adjacent_angle(self, side, angle, is_b=False):
        """Calculate from side and adjacent angle."""
        if is_b:
            self.b = side
            self.angle_A = angle
            self.angle_B = 90.0 - angle
            self.a = side * math.tan(math.radians(angle))
        else:
            self.a = side
            self.angle_B = angle
            self.angle_A = 90.0 - angle
            self.b = side * math.tan(math.radians(angle))
        self.c = math.sqrt(self.a**2 + self.b**2)
    
    def _from_hypotenuse_side(self, c, side, is_b=False):
        """Calculate from hypotenuse and one side."""
        if side >= c:
            raise ValueError("Side cannot be greater than or equal to hypotenuse")
        
        self.c = c
        if is_b:
            self.b = side
            self.a = math.sqrt(c**2 - side**2)
            self.angle_B = math.degrees(math.asin(side / c))
            self.angle_A = 90.0 - self.angle_B
        else:
            self.a = side
            self.b = math.sqrt(c**2 - side**2)
            self.angle_A = math.degrees(math.asin(side / c))
            self.angle_B = 90.0 - self.angle_A
    
    def _from_hypotenuse_angle(self, c, angle, is_b=False):
        """Calculate from hypotenuse and one angle."""
        self.c = c
        angle_rad = math.radians(angle)
        if is_b:
            self.angle_B = angle
            self.angle_A = 90.0 - angle
            self.b = c * math.sin(angle_rad)
            self.a = c * math.cos(angle_rad)
        else:
            self.angle_A = angle
            self.angle_B = 90.0 - angle
            self.a = c * math.sin(angle_rad)
            self.b = c * math.cos(angle_rad)
    
    def verify_mollweide(self, tolerance=1e-6):
        """Verify triangle using Mollweide's equation.
        
        Mollweide's formula: (a - b) / c = sin((A - B)/2) / cos(C/2)
        For right triangle where C = 90°: cos(C/2) = cos(45°) = √2/2
        
        Returns True if triangle satisfies the equation within tolerance.
        """
        try:
            # Mollweide equation: (a - b) / c = sin((A - B)/2) / cos(C/2)
            left_side = (self.a - self.b) / self.c
            
            angle_diff = math.radians(self.angle_A - self.angle_B)
            right_side = math.sin(angle_diff / 2) / math.cos(math.radians(45))
            
            return abs(left_side - right_side) < tolerance
        except (TypeError, ValueError, ZeroDivisionError):
            return False
    
    def get_area(self):
        """Calculate triangle area."""
        return (self.a * self.b) / 2
    
    def get_perimeter(self):
        """Calculate triangle perimeter."""
        return self.a + self.b + self.c
    
    def __str__(self):
        return (f"Right Triangle: a={self.a:.3f}, b={self.b:.3f}, c={self.c:.3f}, "
                f"∠A={self.angle_A:.1f}°, ∠B={self.angle_B:.1f}°, ∠C=90.0°")
    
    def __repr__(self):
        return f"RightTriangle(a={self.a}, b={self.b}, c={self.c})"