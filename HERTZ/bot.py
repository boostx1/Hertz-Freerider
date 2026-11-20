import os
import asyncio
from collections import defaultdict, deque
import asyncio

import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from google.generativeai import client as genai

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

GENAI_API_KEY = os.environ["GENAI_API_KEY"]

genai.configure(api_key=GENAI_API_KEY)

user_state = defaultdict(dict)
locations = []
routes = []
from_routes = {}

START, END = range(2)

def fetch_locations():
    url = "https://www.hertzfreerider.se/api/locations/"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def fetch_routes():
    url = "https://www.hertzfreerider.se/api/transport-routes/?country=SWEDEN"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def build_route_map(data):
    mapping = defaultdict(list)
    for d in data:
        start = d.get("pickupLocationName")
        end = d.get("returnLocationName")
        if start and end:
            mapping[start].append(end)
    return mapping

def fuzzy_match_location(user_input, location_names):
    user_input = user_input.lower()
    matches = [loc for loc in location_names if user_input in loc.lower()]
    return matches[0] if matches else None

def find_routes(start, end, from_routes, max_depth=4):
    all_routes = []
    queue = deque()
    queue.append(([start], set([start])))

    while queue:
        path, visited = queue.popleft()
        last = path[-1]
        if last == end and len(path) > 1:
            all_routes.append(path)
            continue
        if len(path) >= max_depth:
            continue
        for next_place in from_routes.get(last, []):
            if next_place not in visited:
                queue.append((path + [next_place], visited | {next_place}))

    return all_routes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global locations, routes, from_routes
    locations = fetch_locations()
    routes = fetch_routes()
    from_routes = build_route_map(routes)

    await update.message.reply_text(
        "Welcome! I can help you find a Hertz Freerider route.\n"
        "Enter your departure city."
    )
    return START

async def get_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    location_names = [r.get("pickupLocationName", "") for r in routes]
    matched = fuzzy_match_location(user_input, location_names)
    if not matched:
        await update.message.reply_text("Departure location not found. Try again.")
        return START

    user_state[update.effective_user.id]['start'] = matched
    await update.message.reply_text(f"Departure location: {matched}\nWhich city would you like to travel to?")
    return END

async def get_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    location_names = [r.get("returnLocationName", "") for r in routes]
    matched = fuzzy_match_location(user_input, location_names)
    if not matched:
        await update.message.reply_text("Destination not found. Try again.")
        return END

    user_id = update.effective_user.id
    start = user_state[user_id]['start']
    end = matched

    possible_routes = find_routes(start, end, from_routes, max_depth=4)
    if possible_routes:
        response = f"✅ Found {len(possible_routes)} routes:\n"
        for i, route in enumerate(possible_routes[:5], 1):
            response += f"{i}: {' → '.join(route)}\n"
    else:
        response = "❌ No route found."

    await update.message.reply_text(response)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_start)],
            END: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_end)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "already running" in str(e):
            import nest_asyncio
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise
