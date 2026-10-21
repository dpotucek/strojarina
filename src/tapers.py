"""Taper reference dimensions and workshop calculations (dimensions in mm)."""

import math


# Large-end diameter and diameter taper ratio from the ISO 296 Morse series.
MORSE_TAPERS = [
    {"name": "MT0", "large_diameter": 9.045, "ratio_denominator": 19.212},
    {"name": "MT1", "large_diameter": 12.065, "ratio_denominator": 20.047},
    {"name": "MT2", "large_diameter": 17.780, "ratio_denominator": 20.020},
    {"name": "MT3", "large_diameter": 23.825, "ratio_denominator": 19.922},
    {"name": "MT4", "large_diameter": 31.267, "ratio_denominator": 19.254},
    {"name": "MT5", "large_diameter": 44.399, "ratio_denominator": 19.002},
    {"name": "MT6", "large_diameter": 63.348, "ratio_denominator": 19.180},
]

# Basic ISO 7:24 taper sizes. The diameter is specified at the gauge line.
ISO_TAPERS = [
    {"name": "ISO 30", "gauge_diameter": 31.750, "ratio_numerator": 7, "ratio_denominator": 24},
    {"name": "ISO 40", "gauge_diameter": 44.450, "ratio_numerator": 7, "ratio_denominator": 24},
    {"name": "ISO 50", "gauge_diameter": 69.850, "ratio_numerator": 7, "ratio_denominator": 24},
]


def ratio_to_angle(denominator, numerator=1):
    """Convert a diameter taper ratio numerator:denominator to cone angles."""
    denominator = _positive(denominator, "ratio denominator")
    numerator = _positive(numerator, "ratio numerator")
    half_angle = math.degrees(math.atan(numerator / (2 * denominator)))
    return {
        "ratio_numerator": numerator,
        "ratio_denominator": denominator,
        "half_angle_deg": half_angle,
        "included_angle_deg": 2 * half_angle,
    }


def angle_to_ratio(included_angle_deg):
    """Convert an included cone angle in degrees to diameter ratio 1:n."""
    angle = _positive(included_angle_deg, "included angle")
    if angle >= 180:
        raise ValueError("Included angle must be less than 180 degrees")
    half_angle = math.radians(angle / 2)
    denominator = 1 / (2 * math.tan(half_angle))
    return {
        "included_angle_deg": angle,
        "half_angle_deg": angle / 2,
        "ratio_numerator": 1,
        "ratio_denominator": denominator,
    }


def calculate_taper(large_diameter, small_diameter, taper_length, work_length):
    """Calculate taper ratio, angles, tailstock offset and inspection diameters."""
    large = _positive(large_diameter, "large diameter")
    small = _positive(small_diameter, "small diameter")
    length = _positive(taper_length, "taper length")
    between_centers = _positive(work_length, "work length")
    if large <= small:
        raise ValueError("Large diameter must be greater than small diameter")

    diameter_difference = large - small
    denominator = length / diameter_difference
    half_angle = math.atan(diameter_difference / (2 * length))
    checkpoints = [
        {
            "distance": length * fraction,
            "diameter": large - diameter_difference * fraction,
        }
        for fraction in (0.25, 0.5, 0.75)
    ]
    return {
        "diameter_difference": diameter_difference,
        "ratio_denominator": denominator,
        "half_angle_deg": math.degrees(half_angle),
        "included_angle_deg": math.degrees(2 * half_angle),
        "tailstock_offset": between_centers * math.tan(half_angle),
        "top_slide_angle_deg": math.degrees(half_angle),
        "checkpoints": checkpoints,
    }


def _positive(value, name):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a number")
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be positive and finite")
    return number
