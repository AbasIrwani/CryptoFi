import asyncio  # To handle async tasks
import requests  # To make async API requests
import telegram  # Async Telegram bot

    # 🔹 Replace with your actual bot token
BOT_TOKEN = "7905964403:AAFRfDSpAsyyt6I17Xzen4xBfV7ZdrZF494"

    # 🔹 Replace with your actual Telegram channel username
CHANNEL_ID = "@CryptoFiAgency"

    # Create an async bot instance
bot = telegram.Bot(token=BOT_TOKEN)

    # 🔹 List of cryptocurrencies to track (OKX format)
CRYPTO_SYMBOLS = ["BTC-USDT", "ETH-USDT", "BNB-USDT", "SOL-USDT", "XRP-USDT"]

    # 🔹 Assign emojis to each cryptocurrency
CRYPTO_EMOJIS = {
        "BTC": "🟡",  # Bitcoin (Orange)
        "ETH": "🔵",  # Ethereum (Blue)
        "BNB": "🟡",  # Binance Coin (Yellow)
        "SOL": "🟣",  # Solana (Purple)
        "XRP": "🟢"   # Ripple (Green)
    }

    # Store the last sent message ID
LAST_MESSAGE_ID = None  

    # Function to get prices from OKX API (async-friendly)
async def get_crypto_prices():
        prices = {}
        for symbol in CRYPTO_SYMBOLS:
            url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"

            # Get data from OKX API
            response = requests.get(url).json()

            if response["code"] == "0":  # Check if request is successful
                prices[symbol] = float(response["data"][0]["last"])
            else:
                prices[symbol] = "Error"  # Handle API errors

        return prices

    # 🔹 Function to delete the old message and send a new one
async def send_crypto_updates():
        global LAST_MESSAGE_ID  # Allow modifying the global variable

        while True:
            prices = await get_crypto_prices()  # Get updated prices
            message = "🔥 **Live Crypto Prices (OKX)** 🔥\n"

            # 🔹 Format the message with emojis
            for symbol, price in prices.items():
                coin_name = symbol.replace("-USDT", "")  # Clean display
                emoji = CRYPTO_EMOJIS.get(coin_name, "💰")  # Get emoji or use default
                price_text = f"**${price:,.2f}**" if isinstance(price, float) else "❌ Error"
                message += f"{emoji} {coin_name}: {price_text}\n"

            # 🔹 Delete old message if it exists
            try:
                if LAST_MESSAGE_ID:
                    await bot.delete_message(chat_id=CHANNEL_ID, message_id=LAST_MESSAGE_ID)
                    print("🗑️ Deleted old message.")
            except Exception as e:
                print(f"⚠️ Could not delete old message: {e}")

            # 🔹 Send a new message
            try:
                sent_message = await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
                LAST_MESSAGE_ID = sent_message.message_id  # Save new message ID
                print("✅ Sent new message at the bottom!")
            except Exception as e:
                print(f"❌ Failed to send message: {e}")

            await asyncio.sleep(60)  # Wait 60 seconds before sending again

    # Run the async function properly
if __name__ == "__main__":
        asyncio.run(send_crypto_updates())