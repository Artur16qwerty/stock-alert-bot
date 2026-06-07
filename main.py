import os
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
FINNHUB_KEY = os.environ["FINNHUB_KEY"]

SYMBOLS = [
    "AAPL",
    "NVDA",
    "NVD.DE",
    "9MW.HA",
    "INL.DE",
    "AMD",
    "NBIS",
    "NOKIA.HE",
    "IBM",
    "MU",
    "QCI.DE",
    "SSUN.F",
    "DELL",
]

message = "📊 Обновление акций:\n\n"

for symbol in SYMBOLS:
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"
    data = requests.get(url).json()

    price = data.get("c")
    change_sum = data.get("d")
    change_percent = data.get("dp")

    if price is None or change_sum is None or change_percent is None:
        message += f"⚠️ {symbol}: нет данных\n\n"
        continue

    if change_sum > 0:
        icon = "🟢"
        word = "выросла"
        sign = "+"
    elif change_sum < 0:
        icon = "🔴"
        word = "упала"
        sign = ""
    else:
        icon = "⚪"
        word = "без изменений"
        sign = ""

    message += (
        f"{icon} {symbol}\n"
        f"Цена: {price}\n"
        f"{word}: {sign}{change_sum:.2f} / {sign}{change_percent:.2f}%\n\n"
    )

send_url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"

requests.post(send_url, data={
    "chat_id": CHAT_ID,
    "text": message
})
