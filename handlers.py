import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SUBSCRIBERS_FILE = os.getenv("SUBSCRIBERS_FILE", "subscribers.json")


def load_subscribers():
    """Load subscribers from file"""
    if not os.path.exists(SUBSCRIBERS_FILE):
        return {}
    
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("users", {})
    except (json.JSONDecodeError, OSError):
        return {}


def save_subscribers(users):
    """Save subscribers to file"""
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, indent=2)


def handle_message(update):
    """Handle incoming messages and commands"""
    message = update.get("message", {})
    text = message.get("text", "").lower().strip()
    user = message.get("from", {})
    user_id = str(user.get("id"))
    chat_id = str(message.get("chat", {}).get("id"))
    
    if not user_id or not chat_id:
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
            save_subscribers(subscribers)
            
            # Send welcome message
            welcome_msg = f"""🎯 Welcome {username}!

Thank you for subscribing to **Daily Aptitude Quiz**! 📘

Here's what you'll get:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 3 questions daily at 8 AM IST
✅ Topics: Percentages, Profit & Loss, Time & Work, Distance
✅ Instant feedback on your answers
✅ Track your streak and improve daily
✅ Compete with other subscribers

📊 Your Streak:
   Current: 0
   Best: 0

Commands:
   /stop - Unsubscribe anytime
   /stats - View your stats (coming soon)

Good luck! Let's build your skills! 🚀"""
            
            send_message(chat_id, welcome_msg)
        else:
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
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")


def process_updates(offset=None):
    """Process incoming updates from Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"allowed_updates": ["message"]}
    
    if offset:
        params["offset"] = offset
    
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            for update in data.get("result", []):
                handle_message(update)
                offset = update.get("update_id") + 1
            
            return offset
    except Exception as e:
        print(f"Error processing updates: {e}")
    
    return offset


def main():
    """Run the message handler (can be deployed as webhook or polling bot)"""
    print("Starting Telegram message handler...")
    offset = None
    
    while True:
        try:
            offset = process_updates(offset)
        except KeyboardInterrupt:
            print("Stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
