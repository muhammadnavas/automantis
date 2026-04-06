#!/usr/bin/env python3
"""Manually add subscribers to subscribers.json without needing polling"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
SUBSCRIBERS_FILE = os.getenv("SUBSCRIBERS_FILE", "subscribers.json")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not CHAT_ID:
    print("ERROR: TELEGRAM_CHAT_ID not set in .env")
    exit(1)

# Load existing subscribers
if os.path.exists(SUBSCRIBERS_FILE):
    with open(SUBSCRIBERS_FILE, "r") as f:
        data = json.load(f)
        users = data.get("users", {})
else:
    users = {}

# Add subscriber
user_id = CHAT_ID
users[user_id] = {
    "chat_id": CHAT_ID,
    "username": "You",
    "subscribed_at": datetime.now().isoformat(),
    "active": True
}

# Save
with open(SUBSCRIBERS_FILE, "w") as f:
    json.dump({"users": users}, f, indent=2)

print(f"✅ Added subscriber: {CHAT_ID}")
print(f"📁 File saved: {SUBSCRIBERS_FILE}")

with open(SUBSCRIBERS_FILE, "r") as f:
    print("\n📋 Current subscribers.json:")
    print(f.read())
