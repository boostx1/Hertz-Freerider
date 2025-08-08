import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app_openai = OpenAI(api_key=OPENAI_API_KEY)

async def start(update, context):
    await update.message.reply_text("Hej! Skicka 'startstad - slutstad' för att få rutt.")

async def handle_message(update, context):
    text = update.message.text
    if '-' in text:
        start, end = map(str.strip, text.split('-', 1))
        # Här ska du anropa bfs_find_routes och formatera svaret
        # Än så länge hardcodad test
        await update.message.reply_text(f"Söker rutt från {start} till {end} ...")
        # Exempel, ersätt med riktig anrop
        # routes = bfs_find_routes(graph, start, end)
        # Skriv ut första rutten etc
    else:
        await update.message.reply_text("Skriv i format: startstad - slutstad")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
