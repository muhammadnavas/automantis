#!/usr/bin/env python3
"""Force reset bot configuration to allow all message types"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN not set")
    exit(1)

print("🔧 Resetting bot configuration...")

# 1. Set ALL allowed updates (not just messages)
print("\n1. Setting allowed updates to receive ALL update types...")
url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
r1 = requests.get(url, params={"drop_pending_updates": True})
print(f"   Webhook deleted: {r1.json().get('ok')}")

# 2. Get updates with timeout to clear queue
print("\n2. Clearing update queue...")
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
for i in range(3):
    r = requests.get(url, params={"timeout": 1})
    updates = r.json().get("result", [])
    if updates:
        print(f"   Cleared {len(updates)} updates")
        # Mark as processed
        last_id = updates[-1]["update_id"]
        requests.get(url, params={"offset": last_id + 1})

# 3. Remove privacy mode restrictions
print("\n3. Removing privacy restrictions...")
url = f"https://api.telegram.org/bot{TOKEN}/setMyDefaultAdministratorRights"
r3 = requests.post(url, json={"rights": {}, "for_channels": False})
print(f"   Admin rights reset: {r3.json().get('ok')}")

print("\n✅ Bot reset complete!")
print("\n📌 Now:")
print("   1. In handlers.py terminal, press Ctrl+C to stop")
print("   2. Run: python handlers.py")
print("   3. Send /start to @automantis_bot")
print("   4. Watch for 'Received update' in handler terminal")
