# Subscription Feature Setup Guide

## What Changed

Your bot now supports **multiple subscribers**. Users can run `/start` to subscribe and `/stop` to unsubscribe from the daily quiz.

## Files Added/Modified

- **subscribers.json** - Stores subscriber information (auto-created, don't edit manually)
- **handlers.py** - Handles `/start` and `/stop` commands
- **mantis.py** - Modified to send quizzes to all subscribers (fallback to CHAT_ID if no subscribers)

## How It Works

### Option 1: Default Mode (Keep Current Setup)
If no subscribers.json file exists or has no active subscribers, the bot defaults to sending to `TELEGRAM_CHAT_ID` (your group chat).

### Option 2: Subscription Mode (Recommended)
1. Users can message the bot `/start` to subscribe
2. Users can message the bot `/stop` to unsubscribe
3. Daily quiz is sent to all active subscribers at 8 AM IST

## Deployment

### For Subscription Mode to Work, You Have Two Options:

**Option A: Continuous Server (Recommended)**
```bash
# Deploy handlers.py on a server (Heroku, AWS, etc.)
# Run it continuously:
python handlers.py
```

This will listen for `/start` and `/stop` commands in real-time.

**Option B: Webhook Approach**
Set up a Telegram webhook on your server and forward updates to handlers.py

**Option C: Keep GitHub Actions Only**
- Your bot works as is (sends to CHAT_ID only)
- Users who click `/start` won't receive anything
- Just update TELEGRAM_CHAT_ID to your group chat ID

## Current Workflow (GitHub Actions)

The workflow runs daily at 8 AM IST and:
1. Processes previous poll answers (streaks)
2. Generates 3 random questions
3. **Sends to all active subscribers** (or CHAT_ID if none exist)
4. Saves poll data for streak tracking

## Testing

### Test locally:
```bash
# 1. Make sure subscribers.json exists
# 2. Run the bot
python mantis.py

# View generated questions in console
```

## Environment Variables

Add these to your `.env` file:
```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_default_chat_id
SUBSCRIBERS_FILE=subscribers.json
```

## Subscribers File Format

```json
{
  "users": {
    "123456": {
      "chat_id": "123456",
      "username": "john_doe",
      "subscribed_at": "2026-04-04T10:30:00",
      "active": true
    },
    "654321": {
      "chat_id": "-98765432",
      "username": "group_name",
      "subscribed_at": "2026-04-04T09:15:00",
      "active": false
    }
  }
}
```

## Commands

### User Commands (via Telegram)
- `/start` - Subscribe to daily quiz
- `/stop` - Unsubscribe from daily quiz

### Admin Commands (Optional)
- `/list` - Show subscriber count (only works when running handlers.py)

## Troubleshooting

**Quiz only goes to CHAT_ID?**
- subscribers.json might not have active subscribers
- Make sure handlers.py is running to receive `/start` commands

**handlers.py not receiving messages?**
- It needs to be running continuously on a server
- Or set up a webhook with Telegram

**"No active subscribers" error?**
- Check if subscribers.json is valid JSON
- Make sure TELEGRAM_CHAT_ID is set as fallback

## Next Steps

1. **Test current setup** - Run `python mantis.py` to verify it works
2. **Choose deployment** - Decide on continuous server or webhook
3. **Deploy handlers.py** - Set it up on your server (Heroku, EC2, etc.)
4. **Test subscription** - Message the bot `/start` and verify it gets added
5. **Monitor streaks** - Check if streaks are tracking correctly across subscribers
