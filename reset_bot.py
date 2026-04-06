#!/usr/bin/env python3
"""Reset Telegram bot polling state - clears all pending updates"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN not set in .env")
    exit(1)

print("🔄 Resetting bot polling state...")

# Step 1: Get current webhook info
webhook_url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
webhook_response = requests.get(webhook_url)
if webhook_response.json().get("result", {}).get("url"):
    print("⚠️  Webhook is set, removing it...")
    delete_url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    requests.get(delete_url)

# Step 2: Clear all pending updates
print("🗑️  Clearing pending updates...")
updates_url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
while True:
    response = requests.get(updates_url, params={"timeout": 0})
    data = response.json()
    if data.get("ok"):
        updates = data.get("result", [])
        if not updates:
            print(f"✓ All {len(updates)} pending updates cleared")
            break
        
        last_update_id = updates[-1].get("update_id")
        print(f"  Clearing batch of {len(updates)} updates (last ID: {last_update_id})")
        
        # Mark as processed by requesting next offset
        offset_url = f"{updates_url}?offset={last_update_id + 1}"
        requests.get(offset_url)
    else:
        print(f"Error: {data.get('description')}")
        break

print("\n✅ Bot reset complete!")
print("📌 Now:")
print("   1. Run: python handlers.py")
print("   2. Send /start to @automantis_bot in a DIRECT message (not a group)")
print("   3. Watch the handler output for 'Received update'")
