import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SUBSCRIBERS_FILE = os.getenv("SUBSCRIBERS_FILE", "subscribers.json")


def load_subscribers():
    """Load subscribers from file"""
    if not os.path.exists(SUBSCRIBERS_FILE):
        print(f"DEBUG: {SUBSCRIBERS_FILE} doesn't exist yet")
        return {}
    
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            users = data.get("users", {})
            print(f"DEBUG: Loaded {len(users)} subscribers from {SUBSCRIBERS_FILE}")
            return users
    except (json.JSONDecodeError, OSError) as e:
        print(f"DEBUG: Error loading {SUBSCRIBERS_FILE}: {e}")
        return {}


def save_subscribers(users):
    """Save subscribers to file"""
    try:
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
            json.dump({"users": users}, f, indent=2)
        print(f"✓ Saved {len(users)} subscribers to {SUBSCRIBERS_FILE}")
    except Exception as e:
        print(f"ERROR saving subscribers: {e}")


def handle_message(update):
    """Handle incoming messages and commands"""
    print(f"DEBUG: Received update: {update}")
    
    message = update.get("message", {})
    if not message:
        print("DEBUG: No 'message' in update, skipping")
        return
    
    text = message.get("text", "").lower().strip()
    user = message.get("from", {})
    user_id = str(user.get("id"))
    chat_id = str(message.get("chat", {}).get("id"))
    
    print(f"DEBUG: text='{text}', user_id='{user_id}', chat_id='{chat_id}'")
    
    if not user_id or not chat_id:
        print("DEBUG: Missing user_id or chat_id, skipping")
        return
    
    username = user.get("username") or user.get("first_name") or user_id
    
    subscribers = load_subscribers()

    if text == "/start":
        # Add subscriber
        if user_id not in subscribers:
            subscribers[user_id] = {
                "chat_id": chat_id,
                "username": username,
                "subscribed_at": datetime.now().isoformat(),
                "active": True
            }
            print(f"→ New subscriber: {username} (ID: {user_id})")
            save_subscribers(subscribers)
            
            # Send welcome message
            welcome_msg = f"""🎯 <b>Welcome {username}!</b>

Thank you for subscribing to <b>Daily Aptitude Quiz</b>! 📘

<b>Here's what you'll get:</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 3 questions daily at 8 AM IST
✅ Topics: Percentages, Profit &amp; Loss, Time &amp; Work, Distance
✅ Instant feedback on your answers
✅ Track your streak and improve daily
✅ Compete with other subscribers

📊 <b>Your Streak:</b>
   Current: 0
   Best: 0

<b>Commands:</b>
   /stop - Unsubscribe anytime
   /stats - View your stats (coming soon)

Good luck! Let's build your skills! 🚀"""
            
            print(f"→ Sending welcome message to {chat_id}")
            send_message(chat_id, welcome_msg)
        else:
            print(f"→ User {user_id} already subscribed")
            send_message(chat_id, f"✅ You're already subscribed! Type /stop to unsubscribe.")

    elif text == "/stop":
        # Remove subscriber
        if user_id in subscribers:
            subscribers[user_id]["active"] = False
            save_subscribers(subscribers)
            send_message(chat_id, "❌ You've unsubscribed. Type /start to subscribe again.")
        else:
            send_message(chat_id, "❌ You're not subscribed.")

    elif text == "/list":
        # Admin command to see subscriber count
        active_count = sum(1 for u in subscribers.values() if u.get("active"))
        send_message(user_id, f"📊 Total active subscribers: {active_count}")


def send_message(chat_id, text):
    """Send a message via Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    print(f"DEBUG: Sending message to chat_id={chat_id}")
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("ok"):
            print(f"✓ Message sent to {chat_id}")
        else:
            print(f"Telegram API error: {result.get('description')}")
    except requests.exceptions.Timeout:
        print(f"Timeout sending message to {chat_id}")
    except Exception as e:
        print(f"Error sending message to {chat_id}: {e}")


def process_updates(offset=None):
    """Process incoming updates from Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {}  # Remove allowed_updates restriction
    
    if offset:
        params["offset"] = offset
    
    print(f"DEBUG: Fetching updates with offset={offset}...")
    
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        print(f"DEBUG: API response ok={data.get('ok')}")
        
        if data.get("ok"):
            updates = data.get("result", [])
            print(f"DEBUG: Got {len(updates)} update(s)")
            if updates:
                print(f"📨 Processing {len(updates)} update(s)...")
            for update in updates:
                print(f"DEBUG: Processing update_id={update.get('update_id')}, types: {list(update.keys())}")
                handle_message(update)
                offset = update.get("update_id") + 1
            
            return offset
        else:
            print(f"Telegram API error: {data.get('description')}")
    except Exception as e:
        print(f"Error processing updates: {e}")
        import traceback
        traceback.print_exc()
    
    return offset


def main():
    """Run the message handler (can be deployed as webhook or polling bot)"""
    if not TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN not set in .env file")
        return
    
    print(f"🚀 Starting Telegram message handler...")
    print(f"📁 Subscribers file: {SUBSCRIBERS_FILE}")
    print(f"🔐 TOKEN loaded: {TOKEN[:10]}...{TOKEN[-10:] if len(TOKEN) > 20 else ''}")
    print(f"📝 Testing bot connectivity...")
    
    # Test if token works by getting bot info
    try:
        test_url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        test_response = requests.get(test_url, timeout=10)
        if test_response.json().get("ok"):
            bot_info = test_response.json().get("result", {})
            print(f"✓ Bot connected: @{bot_info.get('username')} (ID: {bot_info.get('id')})")
        else:
            print(f"❌ Bot token issue: {test_response.json().get('description')}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to Telegram: {e}")
        return
    
    offset = None
    
    while True:
        try:
            offset = process_updates(offset)
            time.sleep(1)  # Poll every 1 second to prevent high CPU usage
        except KeyboardInterrupt:
            print("\n✋ Stopped.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)  # Wait longer before retrying on error


if __name__ == "__main__":
    main()
