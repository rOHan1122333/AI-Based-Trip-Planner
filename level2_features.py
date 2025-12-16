import math
import urllib.parse
import re


def parse_normalized(normalized_text: str) -> dict:
    data = {}
    for line in normalized_text.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            data[key.strip()] = value.strip()
    return data


def days_from_field(days_text: str) -> int:
    try:
        parts = days_text.split()
        for p in parts:
            if p.isdigit():
                return int(p)
    except Exception:
        pass
    return 1


def estimate_budget_breakdown(normalized_text: str) -> dict:
    data = parse_normalized(normalized_text)

    raw_budget = data.get("Budget (total, currency, or 'flexible')", "flexible")
    days_text = data.get("Trip length (days)", "1 day")
    destination = data.get("Destination(s)", "Destination")

    days = days_from_field(days_text)

    if raw_budget.lower() == "flexible":
        total_budget = 60000
        currency = "₹"
    else:
        digits = "".join(ch for ch in raw_budget if ch.isdigit())
        total_budget = int(digits) if digits else 60000
        currency = "₹" if "₹" in raw_budget else "₹"

    flight_pct = 0.4
    hotel_pct = 0.3
    food_pct = 0.15
    activities_pct = 0.1

    breakdown = {
        "destination": destination,
        "days": days,
        "currency": currency,
        "total_budget": total_budget,
        "flights": math.floor(total_budget * flight_pct),
        "hotel": math.floor(total_budget * hotel_pct),
        "food": math.floor(total_budget * food_pct),
        "activities": math.floor(total_budget * activities_pct),
        "misc": total_budget - (
            math.floor(total_budget * flight_pct)
            + math.floor(total_budget * hotel_pct)
            + math.floor(total_budget * food_pct)
            + math.floor(total_budget * activities_pct)
        ),
    }

    breakdown["hotel_per_night"] = math.floor(
        breakdown["hotel"] / days
    ) if days > 0 else breakdown["hotel"]

    return breakdown


def format_budget_breakdown(b: dict) -> str:
    c = b["currency"]
    return (
        f"💰 Budget Breakdown for {b['destination']} ({b['days']} days)\n"
        f"- Total: {c}{b['total_budget']}\n"
        f"- Flights: {c}{b['flights']}\n"
        f"- Hotel: {c}{b['hotel']} (~{c}{b['hotel_per_night']} per night)\n"
        f"- Food: {c}{b['food']}\n"
        f"- Activities: {c}{b['activities']}\n"
        f"- Misc/Shopping: {c}{b['misc']}\n"
    )


HOTEL_DATABASE = {
    "Dubai": [
        {"name": "Dubai Budget Inn", "type": "Budget", "approx_per_night": 3000},
        {"name": "Marina View Hotel", "type": "Mid-range", "approx_per_night": 6000},
        {"name": "Downtown Luxury Suites", "type": "Premium", "approx_per_night": 12000},
    ],
    "Singapore": [
        {"name": "Little India Lodge", "type": "Budget", "approx_per_night": 4000},
        {"name": "Orchard City Hotel", "type": "Mid-range", "approx_per_night": 8000},
        {"name": "Marina Bay Panorama", "type": "Premium", "approx_per_night": 15000},
    ],
}


def suggest_hotels(normalized_text: str) -> list:
    data = parse_normalized(normalized_text)
    destination = data.get("Destination(s)", "Destination")
    days = days_from_field(data.get("Trip length (days)", "1 day"))

    hotels = HOTEL_DATABASE.get(destination, [])

    suggestions = []
    for h in hotels:
        total_cost = h["approx_per_night"] * days
        suggestions.append(
            {
                "name": h["name"],
                "type": h["type"],
                "approx_per_night": h["approx_per_night"],
                "approx_total": total_cost,
            }
        )

    return suggestions


def format_hotel_suggestions(hotels: list, currency: str = "₹") -> str:
    if not hotels:
        return "No pre-defined hotel suggestions for this destination yet.\n"

    lines = ["🏨 Suggested Hotels:\n"]
    for h in hotels:
        lines.append(
            f"- {h['name']} ({h['type']}) — ~{currency}{h['approx_per_night']} per night, "
            f"~{currency}{h['approx_total']} for stay"
        )
    return "\n".join(lines) + "\n"


PLACE_TEMPLATES = {
    "Dubai": [
        "Burj Khalifa",
        "Dubai Mall",
        "Dubai Marina",
        "Palm Jumeirah",
    ],
    "Singapore": [
        "Marina Bay Sands",
        "Gardens by the Bay",
        "Sentosa Island",
        "Merlion Park",
    ],
}


def generate_maps_links(normalized_text: str) -> str:
    data = parse_normalized(normalized_text)
    destination = data.get("Destination(s)", "Destination")
    places = PLACE_TEMPLATES.get(destination, [])

    if not places:
        return "🗺️ No predefined map links for this destination yet.\n"

    lines = ["🗺️ Useful Google Maps Links:\n"]
    base = "https://www.google.com/maps/search/"

    for p in places:
        query = urllib.parse.quote(f"{p} {destination}")
        url = base + query
        lines.append(f"- {p}: {url}")

    return "\n".join(lines) + "\n"
