import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
FINNHUB_KEY = os.environ["FINNHUB_KEY"]

print("TOKEN LENGTH:", len(TELEGRAM_TOKEN))
print("TOKEN START:", TELEGRAM_TOKEN[:10])
print("TOKEN HAS COLON:", ":" in TELEGRAM_TOKEN)

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

now = datetime.now().strftime("%d.%m.%Y %H:%M")

message = f"📊 ОБНОВЛЕНИЕ АКЦИЙ\n🕒 {now}\n\n"

for symbol in SYMBOLS:
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"
    data = requests.get(url).json()

    price = data.get("c")
    change_sum = data.get("d")
    change_percent = data.get("dp")

    if price is None or change_sum is None or change_percent is None:
        message += f"⚠️ {symbol}\nНет данных\n\n"
        continue

    if change_sum > 0:
        icon = "🟢"
        action = "Выросла"
        arrow = "📈"
        sign = "+"
    elif change_sum < 0:
        icon = "🔴"
        action = "Упала"
        arrow = "📉"
        sign = ""
    else:
        icon = "⚪"
        action = "Без изменений"
        arrow = "➖"
        sign = ""

    message += (
        f"{icon} {symbol}\n"
        f"💰 Цена: {price}\n"
        f"{arrow} {action}: {sign}{change_sum:.2f}\n"
        f"📊 Процент: {sign}{change_percent:.2f}%\n"
        f"──────────────\n"
    )

send_url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"

r = requests.post(send_url, data={
    "chat_id": CHAT_ID,
    "text": message
})

print("STOCK TELEGRAM:", r.status_code, r.text)

CRYPTO_SYMBOLS = [
    "BINANCE:BTCUSDT",
    "BINANCE:ETHUSDT",
    "BINANCE:SOLUSDT",
    "BINANCE:XRPUSDT",
    "BINANCE:DOGEUSDT",
]

crypto_message = f"₿ ОБНОВЛЕНИЕ КРИПТЫ\n🕒 {now}\n\n"

for symbol in CRYPTO_SYMBOLS:
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"
    data = requests.get(url).json()

    name = symbol.replace("BINANCE:", "").replace("USDT", "")

    price = data.get("c")
    change_sum = data.get("d")
    change_percent = data.get("dp")

    if price is None or change_sum is None or change_percent is None:
        crypto_message += f"⚠️ {name}\nНет данных\n\n"
        continue

    if change_sum > 0:
        icon = "🟢"
        action = "Вырос"
        arrow = "📈"
        sign = "+"
    elif change_sum < 0:
        icon = "🔴"
        action = "Упал"
        arrow = "📉"
        sign = ""
    else:
        icon = "⚪"
        action = "Без изменений"
        arrow = "➖"
        sign = ""

    crypto_message += (
        f"{icon} {name}\n"
        f"💰 Цена: {price}\n"
        f"{arrow} {action}: {sign}{change_sum:.2f}\n"
        f"📊 Процент: {sign}{change_percent:.2f}%\n"
        f"──────────────\n"
    )
r = requests.post(send_url, data={
    "chat_id": CHAT_ID,
    "text": crypto_message
})

print("CRYPTO TELEGRAM:", r.status_code, r.text)
