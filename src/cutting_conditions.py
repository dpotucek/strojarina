"""Indicative cutting data and spindle-speed calculations."""

MATERIALS = {
    "steel": {"cs": "Ocel (do cca 700 MPa)", "en": "Steel (up to approx. 700 MPa)"},
    "stainless": {"cs": "Nerezová ocel", "en": "Stainless steel"},
    "cast_iron": {"cs": "Litina", "en": "Cast iron"},
    "aluminum": {"cs": "Hliník a slitiny", "en": "Aluminum alloys"},
    "brass": {"cs": "Mosaz", "en": "Brass"},
}

TOOLS = {
    "hss": {"cs": "HSS (rychlořezná ocel)", "en": "HSS (high-speed steel)"},
    "carbide": {"cs": "SK (sintrovaný karbid)", "en": "Carbide"},
}

OPERATIONS = {
    "turning": {"cs": "Soustružení", "en": "Turning", "feed_unit": "mm/rev"},
    "milling": {"cs": "Frézování", "en": "Milling", "feed_unit": "mm/tooth"},
    "drilling": {"cs": "Vrtání", "en": "Drilling", "feed_unit": "mm/rev"},
    "reaming": {"cs": "Vystružování", "en": "Reaming", "feed_unit": "mm/rev"},
}

# Cutting speed in m/min; feed is mm/rev except milling (mm/tooth).
# Values are practical starting ranges, not guaranteed tool-maker data.
_CUTTING_DATA = {
    "steel": {
        "hss": {"turning": ((20, 35), (.10, .30)), "milling": ((18, 30), (.02, .08)), "drilling": ((18, 25), (.08, .20)), "reaming": ((5, 10), (.15, .35))},
        "carbide": {"turning": ((120, 220), (.15, .50)), "milling": ((100, 180), (.03, .12)), "drilling": ((70, 120), (.10, .25)), "reaming": ((15, 30), (.20, .50))},
    },
    "stainless": {
        "hss": {"turning": ((12, 20), (.08, .20)), "milling": ((10, 18), (.02, .06)), "drilling": ((8, 15), (.08, .18)), "reaming": ((3, 7), (.12, .30))},
        "carbide": {"turning": ((60, 120), (.10, .30)), "milling": ((50, 100), (.02, .08)), "drilling": ((35, 70), (.08, .20)), "reaming": ((10, 20), (.15, .40))},
    },
    "cast_iron": {
        "hss": {"turning": ((18, 30), (.10, .30)), "milling": ((15, 25), (.02, .08)), "drilling": ((15, 22), (.10, .22)), "reaming": ((5, 10), (.15, .35))},
        "carbide": {"turning": ((80, 160), (.15, .40)), "milling": ((70, 140), (.03, .12)), "drilling": ((50, 90), (.10, .25)), "reaming": ((15, 30), (.20, .50))},
    },
    "aluminum": {
        "hss": {"turning": ((80, 150), (.10, .40)), "milling": ((60, 120), (.03, .10)), "drilling": ((50, 100), (.10, .25)), "reaming": ((15, 30), (.15, .40))},
        "carbide": {"turning": ((300, 800), (.15, .50)), "milling": ((250, 600), (.03, .12)), "drilling": ((150, 400), (.10, .30)), "reaming": ((40, 100), (.20, .50))},
    },
    "brass": {
        "hss": {"turning": ((50, 100), (.10, .30)), "milling": ((40, 80), (.02, .08)), "drilling": ((35, 70), (.10, .25)), "reaming": ((10, 20), (.15, .40))},
        "carbide": {"turning": ((200, 500), (.10, .40)), "milling": ((150, 400), (.03, .12)), "drilling": ((100, 250), (.10, .30)), "reaming": ((30, 70), (.20, .50))},
    },
}

DEFAULT_MACHINE_SPEEDS = [50, 100, 200, 400, 800, 1400, 2800]


def get_recommendations():
    """Return the full material/tool/operation reference table."""
    rows = []
    for material, tools in _CUTTING_DATA.items():
        for tool, operations in tools.items():
            for operation, (speed, feed) in operations.items():
                rows.append({
                    "material": material,
                    "tool": tool,
                    "operation": operation,
                    "speed_min": speed[0],
                    "speed_max": speed[1],
                    "feed_min": feed[0],
                    "feed_max": feed[1],
                    "feed_unit": OPERATIONS[operation]["feed_unit"],
                })
    return rows


def calculate_conditions(material, tool, operation, diameter, cutting_speed, feed, machine_speeds, teeth=1):
    """Calculate ideal and safe available spindle speeds plus feed rate."""
    if material not in MATERIALS or tool not in TOOLS or operation not in OPERATIONS:
        raise ValueError("Unknown material, tool or operation")
    if diameter <= 0 or cutting_speed <= 0 or feed <= 0 or teeth < 1:
        raise ValueError("Diameter, cutting speed and feed must be positive; teeth must be at least 1")
    if not machine_speeds or any(speed <= 0 for speed in machine_speeds):
        raise ValueError("Enter one or more positive machine spindle speeds")

    ideal_rpm = 1000 * cutting_speed / (3.141592653589793 * diameter)
    available = sorted(set(machine_speeds))
    safe_speeds = [speed for speed in available if speed <= ideal_rpm]
    selected_rpm = safe_speeds[-1] if safe_speeds else None
    actual_speed = 3.141592653589793 * diameter * selected_rpm / 1000 if selected_rpm else None
    feed_rate = feed * selected_rpm * (teeth if operation == "milling" else 1) if selected_rpm else None

    return {
        "ideal_rpm": round(ideal_rpm, 1),
        "selected_rpm": selected_rpm,
        "actual_cutting_speed": round(actual_speed, 1) if actual_speed is not None else None,
        "feed_rate": round(feed_rate, 1) if feed_rate is not None else None,
        "safe_machine_speeds": safe_speeds,
    }
