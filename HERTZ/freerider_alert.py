import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]

CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.hertzfreerider.se/api/transport-routes/?country=SWEDEN"

MONITORED_CITIES = [
    "stockholm", "ronneby", "karlshamn", "uppsala",
    "karlskrona", "kalmar", "växjö", "kristianstad"
]

def send_telegram(msg):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(telegram_url, data=data)

def fetch_routes():
    try:
        response = requests.get(URL)
        if response.status_code != 200:
            send_telegram(f"⚠️ Hertz returned HTTP {response.status_code}.")
            return []
        return response.json()
    except Exception as e:
        send_telegram(f"🚨 API request failed: {str(e)}")
        return []

def is_monitored_city(city):
    city = city.lower()
    for monitored in MONITORED_CITIES:
        if monitored in city:
            return True
    return False

def match_routes(routes):
    matches = []
    for route in routes:
        start = route.get("pickupLocationName", "").lower()
        end = route.get("returnLocationName", "").lower()

        if is_monitored_city(start) and is_monitored_city(end):
            matches.append(route)
    return matches

def format_route(route):
    date = route.get("transportStartDate", "unknown date")
    date = date[:10] if "T" in date else date
    return (
        f"🚗 Free trip available!\n"
        f"From: {route.get('pickupLocationName', 'unknown')}\n"
        f"To: {route.get('returnLocationName', 'unknown')}\n"
        f"Date: {date}"
    )

def main():
    print("🚦 Checking Hertz Freerider trips between monitored cities...")
    routes = fetch_routes()
    if not routes:
        return

    matched_routes = match_routes(routes)

    if matched_routes:
        for r in matched_routes:
            send_telegram(format_route(r))
        print(f"{len(matched_routes)} trips sent via Telegram.")
    else:
        send_telegram("🚫 No trips between monitored cities are currently available.")
        print("No matching trips.")

if __name__ == "__main__":
    main()
