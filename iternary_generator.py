from openai import OpenAI, RateLimitError, OpenAIError

client = OpenAI()


def parse_normalized(normalized_text: str) -> dict:
    data = {}
    for line in normalized_text.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            data[key.strip()] = value.strip()
    return data


def mock_itinerary(data: dict) -> str:
    destination = data.get("Destination(s)", "your destination")
    days = data.get("Trip length (days)", "a few days")

    return f"""
🏖️ Your Trip Itinerary — {destination}

📅 Duration: {days}

Day 1:
- Arrival
- Hotel check-in
- Visit Dubai Mall & Burj Khalifa
- Fountain show

Day 2:
- Desert Safari + BBQ Dinner

Day 3:
- Marina Beach
- Skydiving or Yacht Cruise (optional)

Day 4:
- Abu Dhabi Day Trip
- Sheikh Zayed Grand Mosque

Day 5:
- Shopping at Global Village
- Departure

✨ Estimated Cost Breakdown:
- Flights: ~₹25,000
- Hotel: ~₹18,000 (budget)
- Activities: ~₹10,000
- Food: ~₹7,000
Total ~₹60,000

💡 Tips:
- Book attraction tickets online
- Carry UAE SIM or eSIM
- Best time to visit: December–March
"""


def generate_itinerary(normalized_text: str) -> str:
    data = parse_normalized(normalized_text)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a travel planner."},
                {"role": "user", "content": f"Generate itinerary:\n{normalized_text}"},
            ],
        )
        return response.choices[0].message.content

    except (RateLimitError, OpenAIError):
        print("⚠️ Using mock itinerary due to missing quota/billing.\n")
        return mock_itinerary(data)


if __name__ == "__main__":
    # quick test
    example = """
Origin city / airport: Mumbai (BOM)
Destination(s): Dubai
Travel dates or range: March
Trip length (days): 5 days
Budget (total, currency, or 'flexible'): ₹60,000
"""
    print(generate_itinerary(example))
