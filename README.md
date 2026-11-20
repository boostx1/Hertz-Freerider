# Hertz Freerider Route Planner

Python tools for exploring one-way Hertz Freerider trips in Sweden. The project models available trips as a directed graph, with pickup and return locations as its vertices.

## Entry points

- [Distance-based route search](HERTZ/get_routes.py) prompts for an exact pickup location and destination. Install `requests` and run `python3 HERTZ/get_routes.py`.
- [Flask application](HERTZ/hertz_app/app.py) provides a web form for finding connecting trips.
- [Trip alerts](HERTZ/freerider_alert.py) checks routes between a list of monitored cities. Provide `BOT_TOKEN` and `CHAT_ID` in the environment for Telegram delivery.
- [Conversational bot](HERTZ/bot.py) prompts for pickup and return locations. It reads `TELEGRAM_TOKEN` and `GENAI_API_KEY` from the environment.

Live results depend on the Hertz Freerider service and current vehicle availability.
