import os
import requests

TELEGRAM_TOKEN = os.environ["8801940769:AAFbZTgouG5x0v7a3RMq2
S4GRIciXAbAAwk"]
CHAT_ID = os.environ["8362317084"]
FINNHUB_KEY = os.environ["d8i9cepr01qm63bapa5gd8i9cepr01qm63bapa60"]

SYMBOLS = {
    "TSLA": 5,
    "NVDA": 5,
    "AAPL": 5,
}

def send_message(text):
    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

for symbol, alert_percent in SYMBOLS.items():
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"
    data = requests.get(url).json()

    price = data.get("c")
    change_percent = data.get("dp")

    print(symbol, price, change_percent)

    if price and change_percent is not None and abs(change_percent) >= alert_percent:
        if change_percent > 0:
            text = f"🚀 {symbol} выросла на {change_percent:.2f}%\nЦена: ${price}"
        else:
            text = f"🔻 {symbol} упала на {change_percent:.2f}%\nЦена: ${price}"

        send_message(text)
