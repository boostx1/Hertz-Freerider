import requests

# === INSTÄLLNINGAR ===
BOT_TOKEN = "7456631399:AAGy_n-wKptRw7mF--AYg0-ft5z7QlU4MBU"
CHAT_ID = "7695542862"
URL = "https://www.hertzfreerider.se/api/transport-routes/?country=SWEDEN"

# Lista över bevakade städer, lowercase för enkel jämförelse
BEVAKADE_STÄDER = [
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
            send_telegram(f"⚠️ API-fel {response.status_code} vid hämtning från Hertz.")
            return []
        return response.json()
    except Exception as e:
        send_telegram(f"🚨 Fel vid API-anrop: {str(e)}")
        return []

def är_stad_i_listan(stad):
    stad = stad.lower()
    for bevakad in BEVAKADE_STÄDER:
        if bevakad in stad:
            return True
    return False

def match_routes(routes):
    matches = []
    for route in routes:
        start = route.get("pickupLocationName", "").lower()
        end = route.get("returnLocationName", "").lower()

        # Kolla om båda städerna är i bevakade listan (oavsett ordning)
        if är_stad_i_listan(start) and är_stad_i_listan(end):
            matches.append(route)
    return matches

def format_route(route):
    datum = route.get("transportStartDate", "okänt datum")
    datum = datum[:10] if "T" in datum else datum
    return (
        f"🚗 Gratisresa hittad!\n"
        f"Från: {route.get('pickupLocationName', 'okänd')}\n"
        f"Till: {route.get('returnLocationName', 'okänd')}\n"
        f"Datum: {datum}"
    )

def main():
    print("🚦 Kontrollerar Hertz FreeRider för alla bevakade städer...")
    routes = fetch_routes()
    if not routes:
        return

    matched_routes = match_routes(routes)

    if matched_routes:
        for r in matched_routes:
            send_telegram(format_route(r))
        print(f"{len(matched_routes)} resor skickade via Telegram.")
    else:
        send_telegram("🚫 Inga resor mellan bevakade städer just nu.")
        print("Inga matchande resor.")

if __name__ == "__main__":
    main()