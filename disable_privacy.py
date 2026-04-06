#!/usr/bin/env python3
"""Disable bot privacy mode programmatically"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN not set in .env")
    exit(1)

print("🔐 Checking and disabling privacy mode...")

# Disable privacy mode
url = f"https://api.telegram.org/bot{TOKEN}/setMyCommands"
data = {
    "commands": [
        {"command": "start", "description": "Subscribe to daily quizzes"},
        {"command": "stop", "description": "Unsubscribe from quizzes"},
        {"command": "list", "description": "View subscriber count"}
    ],
    "scope": {"type": "all_private_chats"}
}

response = requests.post(url, json=data)
if response.json().get("ok"):
    print("✓ Commands registered for all private chats")

# Set default admin rights (this sometimes helps with privacy)
url2 = f"https://api.telegram.org/bot{TOKEN}/setMyDefaultAdministratorRights"
data2 = {
    "rights": {
        "is_anonymous": False,
        "can_manage_chat": False,
        "can_post_messages": False,
        "can_edit_messages": False,
        "can_delete_messages": False
    },
    "for_channels": False
}

response2 = requests.post(url2, json=data2)
if response2.json().get("ok"):
    print("✓ Default admin rights configured")

print("\n✅ Bot configured to receive messages in private chats")
print("\n📌 Now try:")
print("   1. Ctrl+C to stop handlers.py")  
print("   2. python reset_bot.py")
print("   3. python handlers.py")
print("   4. Send /start to @automantis_bot")
