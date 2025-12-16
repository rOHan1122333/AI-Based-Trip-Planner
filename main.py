from iternary import normalize_travel_request
from iternary_generator import generate_itinerary
from level2_features import (
    estimate_budget_breakdown,
    format_budget_breakdown,
    suggest_hotels,
    format_hotel_suggestions,
    generate_maps_links,
)


def main():
    print("🌍 AI Travel Planner")
    print("---------------------")
    user_text = input("👉 Describe your trip in one sentence:\n> ")

    # Step 1: Normalize the request
    print("\n📦 Normalizing your request...\n")
    normalized = normalize_travel_request(user_text)
    print("=== Normalized Travel Request ===")
    print(normalized)

    # ✅ Step 2: Generate itinerary (spelling fixed here)
    print("\n🧳 Generating your itinerary...\n")
    itinerary = generate_itinerary(normalized)   # ← use generate_itinerary
    print("=== Suggested Itinerary ===")
    print(itinerary)

    # Step 3: Level 2 – Budget Breakdown
    print("\n💰 Calculating budget breakdown...\n")
    breakdown = estimate_budget_breakdown(normalized)
    print(format_budget_breakdown(breakdown))

    # Step 4: Level 2 – Hotel Suggestions
    print("\n🏨 Finding suggested hotels...\n")
    hotels = suggest_hotels(normalized)
    print(format_hotel_suggestions(hotels, currency=breakdown["currency"]))

    # Step 5: Level 2 – Google Maps Links
    print("\n🗺️ Generating Google Maps links...\n")
    print(generate_maps_links(normalized))


if __name__ == "__main__":
    main()
