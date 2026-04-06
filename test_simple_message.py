#!/usr/bin/env python3
"""Test sending a simple message to verify chat ID and connectivity"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"Testing message to chat ID: {CHAT_ID}")
print(f"Bot token: {TOKEN[:20]}...")

# Send a simple test message
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": "🔍 TEST MESSAGE - Can you see this?",
    "parse_mode": "HTML"
}

try:
    response = requests.post(url, json=data, timeout=10)
    result = response.json()
    
    if result.get("ok"):
        print(f"\n✅ Message sent successfully!")
        print(f"Message ID: {result.get('result', {}).get('message_id')}")
        print("Check your Telegram for the test message.")
    else:
        print(f"\n❌ Failed: {result.get('description')}")
        
except Exception as e:
    print(f"❌ Error: {e}")
