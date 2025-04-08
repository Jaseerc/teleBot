import time
import requests
import datetime
import gspread
from google.oauth2.service_account import Credentials
from telegram import Bot

# Constants
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
SPREADSHEET_NAME = "Rubber Price Tracker"
SLEEP_START = 22  # 10 PM IST
SLEEP_END = 8     # 8 AM IST

# Set up Google Sheets
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

# Telegram Bot
bot = Bot(token=BOT_TOKEN)

def fetch_price():
    # Simulate fetching price (replace with real scraping or API)
    return {"date": str(datetime.date.today()), "price": "₹178/kg", "trend": "Stable", "summary": "No major changes in global market."}

def post_to_telegram(data):
    message = f"🟢 *Rubber Price Update ({data['date']})*

"               f"• Price: {data['price']}
"               f"• Trend: {data['trend']}
"               f"• Summary: {data['summary']}

"               f"_Malayalam Summary Below_
"               f"• വില: {data['price']}
"               f"• പ്രവണതി: {data['trend']}
"               f"• സംഗ്രഹം: അന്താരാഷ്ട്ര വിപണിയില്‍ വലിയ മാറ്റമില്ല."
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def update_sheet(data):
    sheet.append_row([data['date'], data['price'], data['trend'], data['summary']])

def should_sleep_now():
    now = datetime.datetime.now()
    return now.hour >= SLEEP_START or now.hour < SLEEP_END

def main():
    while True:
        if not should_sleep_now():
            data = fetch_price()
            post_to_telegram(data)
            update_sheet(data)
            time.sleep(60 * 60 * 6)  # Check every 6 hours
        else:
            time.sleep(60 * 10)  # Sleep 10 minutes

if __name__ == "__main__":
    main()