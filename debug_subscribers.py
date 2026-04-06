#!/usr/bin/env python3
"""Debug: Check what chat IDs mantis.py will send to"""

import os
import json
from dotenv import load_dotenv

load_dotenv()
SUBSCRIBERS_FILE = os.getenv("SUBSCRIBERS_FILE", "subscribers.json")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"TELEGRAM_CHAT_ID from .env: {CHAT_ID} (type: {type(CHAT_ID).__name__})")

# Check subscribers file
if os.path.exists(SUBSCRIBERS_FILE):
    with open(SUBSCRIBERS_FILE, "r") as f:
        data = json.load(f)
        users = data.get("users", {})
        print(f"\nSubscribers in file: {len(users)}")
        for user_id, info in users.items():
            chat_id = info.get("chat_id")
            print(f"  User ID: {user_id}")
            print(f"  Chat ID: {chat_id} (type: {type(chat_id).__name__})")
            print(f"  Active: {info.get('active')}")
else:
    print(f"\n❌ {SUBSCRIBERS_FILE} not found!")
