#!/usr/bin/env python3
'''
Pocita trojuhelniky a overuje je Mollweide rovnici

Created by David Potucek on Sep 18, 2025
Project: strojarina
File: triangles.py
'''

import math


class PrecisionSettings:
    """Precision settings for triangle calculations based on angular precision."""
    
    PRECISIONS = {
        '10min': 3,    # 10 angular minutes -> 3 significant digits
        '1min': 4,     # 1 angular minute -> 4 significant digits  
        '10sec': 5,    # 10 angular seconds -> 5 significant digits
        '1sec': 6      # 1 angular second -> 6 significant digits
    }
    
    DEFAULT = '10min'
    
    @classmethod
    def get_digits(cls, precision=None):
        """Get number of significant digits for given precision."""
        if precision is None:
            precision = cls.DEFAULT
        return cls.PRECISIONS.get(precision, cls.PRECISIONS[cls.DEFAULT])
    
    @classmethod
    def round_value(cls, value, precision=None):
        """Round value to specified precision."""
        if value == 0:
            return 0.0
        digits = cls.get_digits(precision)
        return round(value, digits - int(math.floor(math.log10(abs(value)))) - 1)


class RightTriangle:
    """Class for right triangle calculations with Mollweide equation verification."""
    
    def __init__(self, precision=None, **kwargs):
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
        self.precision = precision  # angular precision setting
        
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
    
    def get_area_heron(self):
        """Calculate area using Heron's formula for verification."""
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def get_perimeter(self):
        """Calculate triangle perimeter."""
        return self.a + self.b + self.c
    
    def get_height_to_side(self, side):
        """Calculate height to specified side.
        
        Args:
            side: 'a', 'b', or 'c' - the side to calculate height to
        
        Returns:
            Height to the specified side
        """
        area = self.get_area()
        if side == 'a':
            return PrecisionSettings.round_value((2 * area) / self.a, self.precision)
        elif side == 'b':
            return PrecisionSettings.round_value((2 * area) / self.b, self.precision)
        elif side == 'c':
            return PrecisionSettings.round_value((2 * area) / self.c, self.precision)
        else:
            raise ValueError("Side must be 'a', 'b', or 'c'")
    
    def get_all_heights(self):
        """Get heights to all three sides.
        
        Returns:
            Dictionary with heights to sides a, b, and c
        """
        area = self.get_area()
        return {
            'h_a': PrecisionSettings.round_value((2 * area) / self.a, self.precision),
            'h_b': PrecisionSettings.round_value((2 * area) / self.b, self.precision),
            'h_c': PrecisionSettings.round_value((2 * area) / self.c, self.precision)
        }
    
    def get_rounded_values(self):
        """Get all triangle values rounded to current precision."""
        return {
            'a': PrecisionSettings.round_value(self.a, self.precision),
            'b': PrecisionSettings.round_value(self.b, self.precision),
            'c': PrecisionSettings.round_value(self.c, self.precision),
            'angle_A': PrecisionSettings.round_value(self.angle_A, self.precision),
            'angle_B': PrecisionSettings.round_value(self.angle_B, self.precision),
            'angle_C': 90.0,
            'area': PrecisionSettings.round_value(self.get_area(), self.precision),
            'perimeter': PrecisionSettings.round_value(self.get_perimeter(), self.precision)
        }
    
    def __str__(self):
        digits = PrecisionSettings.get_digits(self.precision)
        a = PrecisionSettings.round_value(self.a, self.precision)
        b = PrecisionSettings.round_value(self.b, self.precision)
        c = PrecisionSettings.round_value(self.c, self.precision)
        angle_A = PrecisionSettings.round_value(self.angle_A, self.precision)
        angle_B = PrecisionSettings.round_value(self.angle_B, self.precision)
        return (f"Right Triangle: a={a}, b={b}, c={c}, "
                f"∠A={angle_A}°, ∠B={angle_B}°, ∠C=90.0°")
    
    def __repr__(self):
        return f"RightTriangle(a={self.a}, b={self.b}, c={self.c})"


class CommonTriangle:
    """Class for general triangle calculations with law of sines/cosines and Mollweide verification."""
    
    def __init__(self, precision=None, **kwargs):
        """Initialize triangle with various parameter combinations.
        
        Supported combinations:
        - three_sides: a, b, c
        - two_sides_angle: a, b, angle_C (or other combinations)
        - side_two_angles: a, angle_B, angle_C (or other combinations)
        """
        self.a = None  # side opposite to angle A
        self.b = None  # side opposite to angle B  
        self.c = None  # side opposite to angle C
        self.angle_A = None  # angle opposite to side a (degrees)
        self.angle_B = None  # angle opposite to side b (degrees)
        self.angle_C = None  # angle opposite to side c (degrees)
        self.precision = precision  # angular precision setting
        
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
        c = self._validate_input(kwargs.get('c'), 'side c')
        angle_A = self._validate_input(kwargs.get('angle_A'), 'angle A', 0, 180)
        angle_B = self._validate_input(kwargs.get('angle_B'), 'angle B', 0, 180)
        angle_C = self._validate_input(kwargs.get('angle_C'), 'angle C', 0, 180)
        
        # Count non-None parameters
        sides = [a, b, c]
        angles = [angle_A, angle_B, angle_C]
        side_count = sum(1 for s in sides if s is not None)
        angle_count = sum(1 for a in angles if a is not None)
        total_params = side_count + angle_count
        
        if total_params < 3:
            raise ValueError("At least 3 parameters required")
        if total_params > 3:
            raise ValueError("Maximum 3 parameters allowed")
        
        # Validate triangle inequality for three sides
        if side_count == 3:
            if not self._check_triangle_inequality(a, b, c):
                raise ValueError("Triangle inequality violated: sum of any two sides must be greater than the third")
        
        # Validate angle sum
        if angle_count >= 2:
            known_angles = [ang for ang in angles if ang is not None]
            if angle_count == 2 and sum(known_angles) >= 180:
                raise ValueError(f"Sum of two angles ({sum(known_angles):.1f}°) must be less than 180°")
            elif angle_count == 3 and abs(sum(known_angles) - 180) > 1e-10:
                raise ValueError(f"Sum of three angles must equal 180°, got {sum(known_angles):.1f}°")
        
        # Calculate based on input combination
        if side_count == 3:
            self._from_three_sides(a, b, c)
        elif side_count == 2 and angle_count == 1:
            self._from_two_sides_one_angle(a, b, c, angle_A, angle_B, angle_C)
        elif side_count == 1 and angle_count == 2:
            self._from_one_side_two_angles(a, b, c, angle_A, angle_B, angle_C)
        else:
            raise ValueError("Unsupported parameter combination")
    
    def _check_triangle_inequality(self, a, b, c):
        """Check if three sides satisfy triangle inequality."""
        return (a + b > c) and (a + c > b) and (b + c > a)
    
    def _from_three_sides(self, a, b, c):
        """Calculate angles from three sides using law of cosines."""
        self.a, self.b, self.c = a, b, c
        
        # Law of cosines: cos(A) = (b² + c² - a²) / (2bc)
        cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
        cos_B = (a**2 + c**2 - b**2) / (2 * a * c)
        cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
        
        # Clamp to [-1, 1] to handle floating point errors
        cos_A = max(-1, min(1, cos_A))
        cos_B = max(-1, min(1, cos_B))
        cos_C = max(-1, min(1, cos_C))
        
        self.angle_A = math.degrees(math.acos(cos_A))
        self.angle_B = math.degrees(math.acos(cos_B))
        self.angle_C = math.degrees(math.acos(cos_C))
    
    def _from_two_sides_one_angle(self, a, b, c, angle_A, angle_B, angle_C):
        """Calculate missing parameters from two sides and one angle."""
        sides = [a, b, c]
        angles = [angle_A, angle_B, angle_C]
        
        # Find which sides and angle we have
        side_indices = [i for i, s in enumerate(sides) if s is not None]
        angle_index = [i for i, a in enumerate(angles) if a is not None][0]
        
        # Assign known values
        if a is not None: self.a = a
        if b is not None: self.b = b
        if c is not None: self.c = c
        if angle_A is not None: self.angle_A = angle_A
        if angle_B is not None: self.angle_B = angle_B
        if angle_C is not None: self.angle_C = angle_C
        
        # Use law of cosines to find missing side
        if angle_index in side_indices:
            # Angle is opposite to one of the known sides - use law of cosines
            self._solve_with_law_of_cosines(side_indices, angle_index)
        else:
            # Angle is not opposite to known sides - use law of sines
            self._solve_with_law_of_sines_two_sides(side_indices, angle_index)
    
    def _from_one_side_two_angles(self, a, b, c, angle_A, angle_B, angle_C):
        """Calculate missing parameters from one side and two angles."""
        sides = [a, b, c]
        angles = [angle_A, angle_B, angle_C]
        
        # Find which side and angles we have
        side_index = [i for i, s in enumerate(sides) if s is not None][0]
        angle_indices = [i for i, a in enumerate(angles) if a is not None]
        
        # Calculate third angle
        known_angles = [angles[i] for i in angle_indices]
        missing_angle = 180 - sum(known_angles)
        
        # Assign known values
        if a is not None: self.a = a
        if b is not None: self.b = b
        if c is not None: self.c = c
        if angle_A is not None: self.angle_A = angle_A
        if angle_B is not None: self.angle_B = angle_B
        if angle_C is not None: self.angle_C = angle_C
        
        # Assign missing angle
        missing_angle_index = [i for i in range(3) if i not in angle_indices][0]
        if missing_angle_index == 0: self.angle_A = missing_angle
        elif missing_angle_index == 1: self.angle_B = missing_angle
        else: self.angle_C = missing_angle
        
        # Use law of sines to find missing sides
        known_side = sides[side_index]
        known_angle = angles[side_index] if angles[side_index] is not None else [self.angle_A, self.angle_B, self.angle_C][side_index]
        
        # Law of sines: a/sin(A) = b/sin(B) = c/sin(C)
        ratio = known_side / math.sin(math.radians(known_angle))
        
        if self.a is None: self.a = ratio * math.sin(math.radians(self.angle_A))
        if self.b is None: self.b = ratio * math.sin(math.radians(self.angle_B))
        if self.c is None: self.c = ratio * math.sin(math.radians(self.angle_C))
    
    def _solve_with_law_of_cosines(self, side_indices, angle_index):
        """Solve using law of cosines when angle is opposite to one known side."""
        sides = [self.a, self.b, self.c]
        angles = [self.angle_A, self.angle_B, self.angle_C]
        
        if angle_index == 0:  # angle_A known, need to find side a
            b, c = sides[1], sides[2]
            angle_A = angles[0]
            self.a = math.sqrt(b**2 + c**2 - 2*b*c*math.cos(math.radians(angle_A)))
        elif angle_index == 1:  # angle_B known, need to find side b
            a, c = sides[0], sides[2]
            angle_B = angles[1]
            self.b = math.sqrt(a**2 + c**2 - 2*a*c*math.cos(math.radians(angle_B)))
        else:  # angle_C known, need to find side c
            a, b = sides[0], sides[1]
            angle_C = angles[2]
            self.c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(angle_C)))
        
        # Calculate remaining angles using law of cosines
        self._calculate_remaining_angles()
    
    def _solve_with_law_of_sines_two_sides(self, side_indices, angle_index):
        """Solve using law of sines when angle is not opposite to known sides."""
        # This is more complex - need to use law of cosines first
        # Find the missing side using law of cosines, then use law of sines
        sides = [self.a, self.b, self.c]
        angles = [self.angle_A, self.angle_B, self.angle_C]
        
        # Use law of cosines to find the third side
        missing_side_index = [i for i in range(3) if i not in side_indices][0]
        
        if missing_side_index == 0:  # need side a
            b, c = sides[1], sides[2]
            angle_A = angles[0] if angles[0] is not None else 180 - sum(a for a in angles[1:] if a is not None)
            self.a = math.sqrt(b**2 + c**2 - 2*b*c*math.cos(math.radians(angle_A)))
        elif missing_side_index == 1:  # need side b
            a, c = sides[0], sides[2]
            angle_B = angles[1] if angles[1] is not None else 180 - sum(a for a in [angles[0], angles[2]] if a is not None)
            self.b = math.sqrt(a**2 + c**2 - 2*a*c*math.cos(math.radians(angle_B)))
        else:  # need side c
            a, b = sides[0], sides[1]
            angle_C = angles[2] if angles[2] is not None else 180 - sum(a for a in angles[:2] if a is not None)
            self.c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(angle_C)))
        
        self._calculate_remaining_angles()
    
    def _calculate_remaining_angles(self):
        """Calculate any missing angles using law of cosines."""
        if self.angle_A is None:
            cos_A = (self.b**2 + self.c**2 - self.a**2) / (2 * self.b * self.c)
            cos_A = max(-1, min(1, cos_A))
            self.angle_A = math.degrees(math.acos(cos_A))
        
        if self.angle_B is None:
            cos_B = (self.a**2 + self.c**2 - self.b**2) / (2 * self.a * self.c)
            cos_B = max(-1, min(1, cos_B))
            self.angle_B = math.degrees(math.acos(cos_B))
        
        if self.angle_C is None:
            cos_C = (self.a**2 + self.b**2 - self.c**2) / (2 * self.a * self.b)
            cos_C = max(-1, min(1, cos_C))
            self.angle_C = math.degrees(math.acos(cos_C))
    
    def verify_mollweide(self, tolerance=1e-6):
        """Verify triangle using Mollweide's equation.
        
        Mollweide's formula: (a - b) / c = sin((A - B)/2) / cos(C/2)
        
        Returns True if triangle satisfies the equation within tolerance.
        """
        try:
            # Mollweide equation: (a - b) / c = sin((A - B)/2) / cos(C/2)
            left_side = (self.a - self.b) / self.c
            
            angle_diff = math.radians(self.angle_A - self.angle_B)
            angle_C_half = math.radians(self.angle_C / 2)
            right_side = math.sin(angle_diff / 2) / math.cos(angle_C_half)
            
            return abs(left_side - right_side) < tolerance
        except (TypeError, ValueError, ZeroDivisionError):
            return False
    
    def get_area(self):
        """Calculate triangle area using Heron's formula."""
        s = (self.a + self.b + self.c) / 2  # semi-perimeter
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def get_perimeter(self):
        """Calculate triangle perimeter."""
        return self.a + self.b + self.c
    
    def get_height_to_side(self, side):
        """Calculate height to specified side.
        
        Args:
            side: 'a', 'b', or 'c' - the side to calculate height to
        
        Returns:
            Height to the specified side
        """
        area = self.get_area()
        if side == 'a':
            return PrecisionSettings.round_value((2 * area) / self.a, self.precision)
        elif side == 'b':
            return PrecisionSettings.round_value((2 * area) / self.b, self.precision)
        elif side == 'c':
            return PrecisionSettings.round_value((2 * area) / self.c, self.precision)
        else:
            raise ValueError("Side must be 'a', 'b', or 'c'")
    
    def get_all_heights(self):
        """Get heights to all three sides.
        
        Returns:
            Dictionary with heights to sides a, b, and c
        """
        area = self.get_area()
        return {
            'h_a': PrecisionSettings.round_value((2 * area) / self.a, self.precision),
            'h_b': PrecisionSettings.round_value((2 * area) / self.b, self.precision),
            'h_c': PrecisionSettings.round_value((2 * area) / self.c, self.precision)
        }
    
    def get_rounded_values(self):
        """Get all triangle values rounded to current precision."""
        return {
            'a': PrecisionSettings.round_value(self.a, self.precision),
            'b': PrecisionSettings.round_value(self.b, self.precision),
            'c': PrecisionSettings.round_value(self.c, self.precision),
            'angle_A': PrecisionSettings.round_value(self.angle_A, self.precision),
            'angle_B': PrecisionSettings.round_value(self.angle_B, self.precision),
            'angle_C': PrecisionSettings.round_value(self.angle_C, self.precision),
            'area': PrecisionSettings.round_value(self.get_area(), self.precision),
            'perimeter': PrecisionSettings.round_value(self.get_perimeter(), self.precision)
        }
    
    def is_right_triangle(self, tolerance=1e-6):
        """Check if triangle is a right triangle."""
        angles = [self.angle_A, self.angle_B, self.angle_C]
        return any(abs(angle - 90) < tolerance for angle in angles)
    
    def is_isosceles(self, tolerance=1e-6):
        """Check if triangle is isosceles."""
        sides = [self.a, self.b, self.c]
        return (abs(sides[0] - sides[1]) < tolerance or 
                abs(sides[0] - sides[2]) < tolerance or 
                abs(sides[1] - sides[2]) < tolerance)
    
    def is_equilateral(self, tolerance=1e-6):
        """Check if triangle is equilateral."""
        return (abs(self.a - self.b) < tolerance and 
                abs(self.b - self.c) < tolerance and 
                abs(self.a - self.c) < tolerance)
    
    def __str__(self):
        digits = PrecisionSettings.get_digits(self.precision)
        a = PrecisionSettings.round_value(self.a, self.precision)
        b = PrecisionSettings.round_value(self.b, self.precision)
        c = PrecisionSettings.round_value(self.c, self.precision)
        angle_A = PrecisionSettings.round_value(self.angle_A, self.precision)
        angle_B = PrecisionSettings.round_value(self.angle_B, self.precision)
        angle_C = PrecisionSettings.round_value(self.angle_C, self.precision)
        return (f"Triangle: a={a}, b={b}, c={c}, "
                f"∠A={angle_A}°, ∠B={angle_B}°, ∠C={angle_C}°")
    
    def __repr__(self):
        return f"CommonTriangle(a={self.a}, b={self.b}, c={self.c})"