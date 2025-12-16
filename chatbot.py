from iternary import normalize_travel_request
from iternary_generator import generate_itinerary
from level2_features import (
    estimate_budget_breakdown,
    format_budget_breakdown,
    suggest_hotels,
    format_hotel_suggestions,
    generate_maps_links,
)


def chat():
    print("🤖 AI Travel Planner Chatbot")
    print("--------------------------------")
    print("Type your trip in one sentence.")
    print("Example: I want to go from Chennai to Singapore in February for 4 days with a budget of ₹80,000")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_text = input("You: ")

        if user_text.strip().lower() in ("exit", "quit", "q"):
            print("Bot: Bye! Happy travels ✈️")
            break

        if not user_text.strip():
            print("Bot: Please describe your trip in one sentence 🙂")
            continue

        # Step 1: Normalize
        print("\nBot: Let me understand your trip...\n")
        normalized = normalize_travel_request(user_text)
        print("📦 Normalized Request:")
        print(normalized)

        # Step 2: Itinerary
        print("\n🧳 Itinerary:")
        itinerary = generate_itinerary(normalized)
        print(itinerary)

        # Step 3: Budget breakdown
        print("\n💰 Budget Breakdown:")
        breakdown = estimate_budget_breakdown(normalized)
        print(format_budget_breakdown(breakdown))

        # Step 4: Hotels
        print("\n🏨 Hotel Suggestions:")
        hotels = suggest_hotels(normalized)
        print(format_hotel_suggestions(hotels, currency=breakdown["currency"]))

        # Step 5: Google Maps links
        print("\n🗺️ Google Maps Links:")
        print(generate_maps_links(normalized))

        print("\n--------------------------------\n")


if __name__ == "__main__":
    chat()
