"""Approximate hardness conversions and reference material values."""

import math


# Approximate steel conversions based on common ASTM E140 reference tables.
# Columns are HRC, Brinell HB, and Vickers HV.
STEEL_HARDNESS_TABLE = (
    (20, 226, 238),
    (25, 253, 266),
    (30, 286, 302),
    (35, 327, 345),
    (40, 371, 392),
    (45, 421, 446),
    (50, 481, 513),
    (55, 552, 595),
    (60, 653, 697),
    (65, 739, 832),
    (68, 818, 940),
)

METAL_REFERENCE_MATERIALS = (
    {"name_cs": "Ocel, měkká (žíhaná)", "name_en": "Mild steel (annealed)", "hrc": None, "hb": 120, "hv": 126},
    {"name_cs": "Ocel, středně uhlíková (normalizovaná)", "name_en": "Medium-carbon steel (normalized)", "hrc": None, "hb": 180, "hv": 190},
    {"name_cs": "Ocel, kalená", "name_en": "Hardened steel", "hrc": 45, "hb": 421, "hv": 446},
    {"name_cs": "Nástrojová ocel, kalená", "name_en": "Hardened tool steel", "hrc": 60, "hb": 653, "hv": 697},
    {"name_cs": "Nerezová ocel, kalená", "name_en": "Hardened stainless steel", "hrc": 35, "hb": 327, "hv": 345},
    {"name_cs": "Litina, šedá", "name_en": "Gray cast iron", "hrc": None, "hb": 200, "hv": 210},
    {"name_cs": "Hliníková slitina 6061-T6", "name_en": "6061-T6 aluminum alloy", "hrc": None, "hb": 95, "hv": 107},
    {"name_cs": "Měď, žíhaná", "name_en": "Annealed copper", "hrc": None, "hb": 40, "hv": 45},
    {"name_cs": "Mosaz", "name_en": "Brass", "hrc": None, "hb": 100, "hv": 110},
)

def convert_hardness(value, scale):
    """Convert between HRC, HB, and HV by linear interpolation for steel."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Hardness must be a finite number")
    if scale not in ("HRC", "HB", "HV"):
        raise ValueError("Scale must be HRC, HB, or HV")

    column = {"HRC": 0, "HB": 1, "HV": 2}[scale]
    values = [row[column] for row in STEEL_HARDNESS_TABLE]
    if value < values[0] or value > values[-1]:
        raise ValueError(
            f"{scale} value is outside the steel conversion range "
            f"({values[0]} to {values[-1]})"
        )

    for lower, upper in zip(STEEL_HARDNESS_TABLE, STEEL_HARDNESS_TABLE[1:]):
        x0, x1 = lower[column], upper[column]
        if x0 <= value <= x1:
            ratio = (value - x0) / (x1 - x0)
            return {
                target: round(lower[index] + ratio * (upper[index] - lower[index]), 1)
                for target, index in (("HRC", 0), ("HB", 1), ("HV", 2))
            }
    raise ValueError(f"Cannot convert {scale} value")
