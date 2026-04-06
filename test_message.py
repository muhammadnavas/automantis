#!/usr/bin/env python3
"""Test bot by sending a message to it and checking if handler receives it"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in .env")
    exit(1)

print("Testing bot message reception...")
print(f"Bot ID: {TOKEN.split(':')[0]}")
print(f"Chat ID: {CHAT_ID}")
print("\n📝 Sending test message to bot...")

# Try sending a message TO the bot
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": "/start",
    "parse_mode": "HTML"
}

try:
    response = requests.post(url, json=data, timeout=10)
    result = response.json()
    
    if result.get("ok"):
        print("✓ Test message sent successfully!")
        print(f"  Message ID: {result.get('result', {}).get('message_id')}")
        print("\n🔍 Now check the handler terminal - it should show:")
        print("   DEBUG: Got 1 update(s)")
        print("   DEBUG: Received update:")
    else:
        print(f"❌ Failed to send: {result.get('description')}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n\n💡 Alternative: Disable privacy mode in BotFather")
print("   1. Message @BotFather on Telegram")
print("   2. /mybots → select @automantis_bot")
print("   3. 'Bot Settings' → 'Privacy mode' → toggle OFF")
print("   4. Then try sending /start again")
