#!/usr/bin/env python3
"""Check and clean up Telegram bot webhook configuration"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN not set in .env")
    exit(1)

# Get webhook info
print("Checking webhook configuration...")
url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
response = requests.get(url)
info = response.json()

if info.get("ok"):
    webhook_data = info.get("result", {})
    print(f"\nWebhook URL: {webhook_data.get('url') or 'NOT SET (good for polling)'}")
    
    if webhook_data.get('url'):
        print("\n⚠️  WARNING: Webhook is active! This blocks polling.")
        print("Removing webhook to enable polling...\n")
        
        remove_url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
        remove_response = requests.get(remove_url)
        if remove_response.json().get("ok"):
            print("✓ Webhook removed. Polling should now work.")
        else:
            print(f"❌ Error removing webhook: {remove_response.json()}")
    else:
        print("✓ No webhook set. Polling is active.")
else:
    print(f"❌ Error: {info.get('description')}")
