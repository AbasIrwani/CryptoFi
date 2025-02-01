from flask import Flask, request
from telegram import Bot, Update
import os

TOKEN = "YOUR_BOT_TOKEN"
WEBHOOK_URL = "https://your-deployed-url.com"  # Replace with your actual domain

bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    chat_id = update.message.chat_id
    text = update.message.text

    # Respond to messages
    if text == "/start":
        bot.send_message(chat_id=chat_id, text="Welcome to my bot! 🚀")
    else:
        bot.send_message(chat_id=chat_id, text=f"You said: {text}")

    return "OK", 200

# Set webhook on Telegram
def set_webhook():
    bot.setWebhook(f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
