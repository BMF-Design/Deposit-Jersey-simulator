import random

EVENTS = [
    "drain_blocked",
    "boiler_leaking",
    "roof_leak",
    "broken_window",
    "pet_request",
    "new_child",
    "tenant_divorce",
    "family_visiting",
    "long_holiday",
    "neighbour_complaint",
    None,
    None,
]

def get_random_event():
    return random.choice(EVENTS)

def apply_event(engine, event: str | None) -> str:
    """Apply event effects; return a short event message for the UI."""
    if event is None:
        return ""

    msg = ""

    if event == "drain_blocked":
        msg = "🚿 **Random event:** Drain becomes blocked."
        engine.property.damage("plumbing", 10)
        engine.stats["evidence"] += 1  # encourage documenting/reporting

    elif event == "boiler_leaking":
        msg = "🔥 **Random event:** Boiler starts leaking."
        engine.property.damage("heating", 15)
        engine.stats["legal_risk"] += 1

    elif event == "roof_leak":
        msg = "🌧️ **Random event:** Roof/ceiling leak appears during rain."
        engine.property.damage("structure", 20)
        engine.stats["legal_risk"] += 1

    elif event == "broken_window":
        msg = "🪟 **Random event:** A window breaks."
        engine.property.damage("interior", 10)
        engine.stats["trust"] -= 1

    elif event == "pet_request":
        msg = "🐶 **Random event:** Tenant asks to keep a pet."
        engine.stats["trust"] += 1

    elif event == "new_child":
        msg = "👶 **Random event:** Tenant has a new child."
        engine.stats["trust"] += 1

    elif event == "tenant_divorce":
        msg = "💔 **Random event:** Tenants divorce; one partner wants to leave."
        engine.stats["legal_risk"] += 1

    elif event == "family_visiting":
        msg = "👨‍👩‍👧 **Random event:** Family visits for an extended stay."
        engine.stats["trust"] += 1

    elif event == "long_holiday":
        msg = "✈️ **Random event:** Tenant goes away for a long holiday."
        engine.stats["trust"] += 1

    elif event == "neighbour_complaint":
        msg = "🔊 **Random event:** Neighbour complains about noise."
        engine.stats["trust"] -= 1

    return msg