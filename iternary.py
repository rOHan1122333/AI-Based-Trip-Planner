from openai import OpenAI, RateLimitError, OpenAIError

client = OpenAI()  # API key optional since we use mock fallback


def mock_travel_normalizer(user_text: str) -> str:
    return (
        "Origin city / airport: Mumbai (BOM)\n"
        "Destination(s): Dubai\n"
        "Travel dates or range: March (flexible within March)\n"
        "Trip length (days): 5 days\n"
        "Budget (total, currency, or 'flexible'): ₹60,000\n"
        "Travel style: not specified\n"
        "Mobility constraints / accessibility needs: none\n"
        "Must-see interests / activities: not specified\n"
        "Preferred airlines/hotels: not specified\n"
        "Any other constraints (no-fly, pet, dietary): none\n\n"
        "Follow-up questions:\n"
        "- Q1) Do you have a preferred travel style (budget / mid-range / luxury)?\n"
        "- Q2) Any specific interests in Dubai (desert safari, malls, beaches, museums)?\n"
        "- Q3) Any preferred airlines or hotel brands?\n"
    )


def call_model(user_text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert travel-planning assistant that normalizes travel requests."
                    ),
                },
                {"role": "user", "content": user_text},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content

    except (RateLimitError, OpenAIError):
        print("⚠️ No quota / billing for this API key. Using mock response instead.\n")
        return mock_travel_normalizer(user_text)


# ✅ Simple wrapper function we will import in main.py
def normalize_travel_request(user_text: str) -> str:
    return call_model(user_text)


if __name__ == "__main__":
    # Optional: local test
    user_text = "I want to fly from Mumbai to Dubai in March for 5 days with a ₹60,000 budget"
    print("Normalizing travel request...\n")
    print(normalize_travel_request(user_text))
