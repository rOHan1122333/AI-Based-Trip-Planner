from flask import Flask, render_template, request, jsonify
import os
import sys

# Make sure Python can import your other modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iternary import normalize_travel_request
from iternary_generator import generate_itinerary
from level2_features import (
    estimate_budget_breakdown,
    format_budget_breakdown,
    suggest_hotels,
    format_hotel_suggestions,
    generate_maps_links,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "empty message"}), 400

    # Step 1: Normalize the request (uses mock fallback if no quota)
    normalized = normalize_travel_request(user_message)

    # Step 2: Generate itinerary (uses mock fallback if no quota)
    itinerary = generate_itinerary(normalized)

    # Step 3: Budget breakdown
    breakdown = estimate_budget_breakdown(normalized)
    budget_text = format_budget_breakdown(breakdown)

    # Step 4: Hotels
    hotels = suggest_hotels(normalized)
    hotels_text = format_hotel_suggestions(hotels, breakdown["currency"])

    # Step 5: Maps
    maps_links = generate_maps_links(normalized)

    # Combined reply (what the chat bubble shows)
    combined_reply = (
        "📦 Normalized Request:\n"
        + normalized
        + "\n🧳 Itinerary:\n"
        + itinerary
        + "\n"
        + budget_text
        + "\n"
        + hotels_text
        + "\n"
        + maps_links
    )

    return jsonify(
        {
            "normalized": normalized,
            "itinerary": itinerary,
            "budget": budget_text,
            "hotels": hotels_text,
            "maps": maps_links,
            "reply": combined_reply,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
