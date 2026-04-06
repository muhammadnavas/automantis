#!/usr/bin/env python3
"""Add a new subscriber by chat ID"""

import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
SUBSCRIBERS_FILE = os.getenv("SUBSCRIBERS_FILE", "subscribers.json")

# Get chat ID from command line or prompt
if len(sys.argv) > 1:
    chat_id = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else "User"
else:
    chat_id = input("Enter chat ID: ").strip()
    username = input("Enter username (optional): ").strip() or "User"

if not chat_id:
    print("❌ Chat ID is required")
    exit(1)

# Load existing subscribers
if os.path.exists(SUBSCRIBERS_FILE):
    with open(SUBSCRIBERS_FILE, "r") as f:
        data = json.load(f)
        users = data.get("users", {})
else:
    users = {}

# Add subscriber
users[chat_id] = {
    "chat_id": chat_id,
    "username": username,
    "subscribed_at": datetime.now().isoformat(),
    "active": True
}

# Save
with open(SUBSCRIBERS_FILE, "w") as f:
    json.dump({"users": users}, f, indent=2)

print(f"✅ Added subscriber: {username} (Chat ID: {chat_id})")
print(f"\n📋 Total subscribers: {len(users)}")
for uid, info in users.items():
    print(f"   - {info.get('username')} ({uid})")
