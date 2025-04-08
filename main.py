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

# Set up Google Sheets API
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

# Telegram Bot
bot = Bot(token=BOT_TOKEN)

def fetch_price():
    """
    Simulate fetching rubber price data.
    Replace this with real scraping or API logic.
    """
    return {
        "date": str(datetime.date.today()),
        "price": "₹178/kg",
        "trend": "Stable",
        "summary": "No major changes in global market."
    }

def post_to_telegram(data):
    """
    Send the rubber price update message to Telegram.
    Includes both English and Malayalam summaries.
    """
    message = (
        f"🟢 *Rubber Price Update ({data['date']})*\n\n"
        f"• Price: {data['price']}\n"
        f"• Trend: {data['trend']}\n"
        f"• Summary: {data['summary']}\n\n"
        f"_Malayalam Summary Below_\n"
        f"• വില: {data['price']}\n"
        f"• പ്രവണതി: {data['trend']}\n"
        f"• സംഗ്രഹം: അന്താരാഷ്ട്ര വിപണിയില്‍ വലിയ മാറ്റമില്ല."
    )
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def update_sheet(data):
    """
    Append the fetched data to the Google Sheet.
    """
    sheet.append_row([data['date'], data['price'], data['trend'], data['summary']])

def should_sleep_now():
    """
    Check if the current time is between 10 PM and 8 AM.
    Returns True if the script should sleep.
    """
    now = datetime.datetime.now()
    return now.hour >= SLEEP_START or now.hour < SLEEP_END

def main():
    """
    Main loop to fetch, post, and log data.
    Operates only between 8 AM to 10 PM IST.
    """
    while True:
        if not should_sleep_now():
            data = fetch_price()
            post_to_telegram(data)
            update_sheet(data)
            time.sleep(60 * 60 * 6)  # Check every 6 hours
        else:
            time.sleep(60 * 10)  # Sleep for 10 minutes before checking again

if __name__ == "__main__":
    main()

