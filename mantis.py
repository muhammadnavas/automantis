import os
import random
import json
from datetime import datetime

import requests
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
QUESTION_COUNT = int(os.getenv("QUESTION_COUNT", "3"))
STREAK_STATE_FILE = os.getenv("STREAK_STATE_FILE", "streaks.json")
MAX_TRACKED_POLLS = int(os.getenv("MAX_TRACKED_POLLS", "300"))

QUESTION_BANK = {
    "Percentages": [
        {
            "question": "If 20% of a number is 80, find the number.",
            "options": ["320", "360", "400", "420"],
            "correct_option": 2,
            "explanation": "20% of x = 80 => x = 80 / 0.2 = 400",
        },
        {
            "question": "A value increases from 250 to 300. Find the percentage increase.",
            "options": ["10%", "15%", "20%", "25%"],
            "correct_option": 2,
            "explanation": "Increase = 50, percentage increase = (50/250)*100 = 20%",
        },
        {
            "question": "A shirt marked ₹1200 is sold at 15% discount. Find sale price.",
            "options": ["₹980", "₹1020", "₹1060", "₹1120"],
            "correct_option": 1,
            "explanation": "Discount = 15% of 1200 = 180, sale price = 1200 - 180 = 1020",
        },
    ],
    "Time and Work": [
        {
            "question": "If A can finish work in 10 days, how much work in 1 day?",
            "options": ["1/5", "1/10", "1/12", "1/20"],
            "correct_option": 1,
            "explanation": "Daily work rate = total work / days = 1/10",
        },
        {
            "question": "A can do a job in 12 days, B in 18 days. How many days together?",
            "options": ["6.2 days", "7.2 days", "8.0 days", "9.0 days"],
            "correct_option": 1,
            "explanation": "Combined rate = 1/12 + 1/18 = 5/36, time = 36/5 = 7.2 days",
        },
        {
            "question": "A is twice as efficient as B. If both finish in 9 days, B alone takes how many days?",
            "options": ["18 days", "24 days", "27 days", "30 days"],
            "correct_option": 2,
            "explanation": "Let B = x, A = 2x, together = 3x = 1/9 => x = 1/27",
        },
    ],
    "Time and Distance": [
        {
            "question": "A train 120m long crosses a pole in 6 sec. Find speed.",
            "options": ["15 m/s", "18 m/s", "20 m/s", "22 m/s"],
            "correct_option": 2,
            "explanation": "Speed = distance/time = 120/6 = 20 m/s",
        },
        {
            "question": "A car travels 150 km in 3 hours. Find speed in m/s.",
            "options": ["12.5 m/s", "13.8 m/s", "15.0 m/s", "16.7 m/s"],
            "correct_option": 1,
            "explanation": "150 km/3 h = 50 km/h = 13.8 m/s (approx)",
        },
        {
            "question": "Two trains move in opposite directions at 54 km/h and 36 km/h. Relative speed?",
            "options": ["72 km/h", "80 km/h", "90 km/h", "96 km/h"],
            "correct_option": 2,
            "explanation": "Opposite directions => add speeds: 54 + 36 = 90 km/h",
        },
    ],
    "Profit and Loss": [
        {
            "question": "A shopkeeper gains 20% on a product costing ₹500. Selling price?",
            "options": ["₹580", "₹600", "₹620", "₹650"],
            "correct_option": 1,
            "explanation": "SP = CP * 1.20 = 500 * 1.20 = 600",
        },
        {
            "question": "An item is sold for ₹840 at 5% loss. Find cost price.",
            "options": ["₹860", "₹880", "₹900", "₹920"],
            "correct_option": 2,
            "explanation": "SP = 95% of CP => CP = 840/0.95 = 884.21 (nearest: 900)",
        },
        {
            "question": "Cost price is ₹750 and selling price is ₹900. Find profit percent.",
            "options": ["15%", "20%", "25%", "30%"],
            "correct_option": 1,
            "explanation": "Profit = 150, profit% = (150/750)*100 = 20%",
        },
    ],
    "Simple Interest": [
        {
            "question": "Simple interest on ₹2000 at 5% for 2 years?",
            "options": ["₹180", "₹200", "₹220", "₹250"],
            "correct_option": 1,
            "explanation": "SI = (P*R*T)/100 = (2000*5*2)/100 = 200",
        },
        {
            "question": "Find principal if SI is ₹360 at 6% per annum for 3 years.",
            "options": ["₹1800", "₹2000", "₹2200", "₹2400"],
            "correct_option": 1,
            "explanation": "P = (SI*100)/(R*T) = (360*100)/(6*3) = 2000",
        },
        {
            "question": "At what rate will ₹1500 earn SI of ₹225 in 3 years?",
            "options": ["4%", "5%", "6%", "7%"],
            "correct_option": 1,
            "explanation": "R = (SI*100)/(P*T) = (225*100)/(1500*3) = 5%",
        },
    ],
}


def validate_config() -> None:
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing in .env")
    if not CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID is missing in .env")
    if QUESTION_COUNT <= 0:
        raise ValueError("QUESTION_COUNT must be greater than 0")
    if MAX_TRACKED_POLLS <= 0:
        raise ValueError("MAX_TRACKED_POLLS must be greater than 0")


def load_state() -> dict:
    default_state = {
        "last_update_id": 0,
        "polls": {},
        "users": {},
    }
    if not os.path.exists(STREAK_STATE_FILE):
        return default_state

    try:
        with open(STREAK_STATE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return default_state

    if not isinstance(data, dict):
        return default_state

    data.setdefault("last_update_id", 0)
    data.setdefault("polls", {})
    data.setdefault("users", {})
    return data


def save_state(state: dict) -> None:
    with open(STREAK_STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)


def get_poll_answer_updates(offset: int | None = None) -> list[dict]:
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = [("allowed_updates", json.dumps(["poll_answer"]))]
    if offset is not None:
        params.append(("offset", str(offset)))

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("ok"):
        raise RuntimeError(f"Telegram getUpdates error: {payload}")
    return payload.get("result", [])


def upsert_user_streak(state: dict, user: dict, is_correct: bool) -> None:
    user_id = str(user.get("id"))
    if not user_id or user_id == "None":
        return

    display_name = (
        user.get("username")
        or user.get("first_name")
        or user.get("last_name")
        or user_id
    )
    users = state["users"]
    entry = users.setdefault(
        user_id,
        {
            "name": display_name,
            "current_streak": 0,
            "best_streak": 0,
            "correct_answers": 0,
            "wrong_answers": 0,
            "updated_at": "",
        },
    )

    entry["name"] = display_name
    entry["updated_at"] = datetime.now().isoformat(timespec="seconds")

    if is_correct:
        entry["correct_answers"] += 1
        entry["current_streak"] += 1
        if entry["current_streak"] > entry["best_streak"]:
            entry["best_streak"] = entry["current_streak"]
    else:
        entry["wrong_answers"] += 1
        entry["current_streak"] = 0


def process_pending_poll_answers(state: dict) -> int:
    offset = state["last_update_id"] + 1 if state["last_update_id"] else None
    updates = get_poll_answer_updates(offset)
    processed = 0

    for update in updates:
        update_id = update.get("update_id", 0)
        if update_id > state["last_update_id"]:
            state["last_update_id"] = update_id

        poll_answer = update.get("poll_answer")
        if not poll_answer:
            continue

        poll_id = poll_answer.get("poll_id")
        poll_info = state["polls"].get(poll_id)
        if not poll_info:
            continue

        selected = poll_answer.get("option_ids", [])
        selected_option = selected[0] if selected else None
        is_correct = selected_option == poll_info.get("correct_option_id")
        upsert_user_streak(state, poll_answer.get("user", {}), is_correct)
        processed += 1

    return processed


def trim_poll_history(state: dict) -> None:
    polls = state["polls"]
    if len(polls) <= MAX_TRACKED_POLLS:
        return

    ordered_poll_ids = sorted(
        polls,
        key=lambda poll_id: polls[poll_id].get("created_at", ""),
    )
    remove_count = len(polls) - MAX_TRACKED_POLLS
    for poll_id in ordered_poll_ids[:remove_count]:
        polls.pop(poll_id, None)


def build_streak_summary(state: dict) -> list[str]:
    users = state.get("users", {})
    current_user = users.get(str(CHAT_ID))
    if not current_user:
        return ["🔥 Your current streak: 0"]

    return [
        f"🔥 {current_user['name']}",
        f"Current streak: {current_user['current_streak']}",
    ]


def build_question_pool() -> list[dict]:
    pool = []
    for topic, questions in QUESTION_BANK.items():
        for question in questions:
            item = dict(question)
            item["topic"] = topic
            pool.append(item)
    return pool


def generate_daily_questions() -> list[dict]:
    pool = build_question_pool()
    count = min(QUESTION_COUNT, len(pool))
    return random.sample(pool, count)


def build_message(selected_questions: list[dict], streak_lines: list[str]) -> str:
    today = datetime.now().strftime("%d %b %Y")
    lines = [
        "📘 Daily Aptitude Quiz",
        f"📅 {today}",
        "",
        *streak_lines,
        "",
        "",
    ]
    lines.append("Good luck!")
    return "\n".join(lines)


def send_telegram_message(message: str) -> dict:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": message},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    if not payload.get("ok"):
        raise RuntimeError(f"Telegram API error: {payload}")
    return payload


def send_quiz_poll(item: dict, index: int) -> dict:
    url = f"https://api.telegram.org/bot{TOKEN}/sendPoll"
    payload = {
        "chat_id": CHAT_ID,
        "question": f"Q{index}. [{item['topic']}] {item['question']}",
        "options": item["options"],
        "type": "quiz",
        "correct_option_id": item["correct_option"],
        "is_anonymous": False,
        "explanation": item["explanation"],
    }
    response = requests.post(url, json=payload, timeout=20)
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram poll API error: {data}")
    return data


def main() -> None:
    validate_config()
    state = load_state()
    processed_answers = process_pending_poll_answers(state)

    questions = generate_daily_questions()
    streak_lines = build_streak_summary(state)
    header = build_message(questions, streak_lines)
    header_payload = send_telegram_message(header)
    header_message_id = header_payload.get("result", {}).get("message_id")

    sent_count = 0
    for index, item in enumerate(questions, start=1):
        poll_payload = send_quiz_poll(item, index)
        poll_id = poll_payload.get("result", {}).get("poll", {}).get("id")
        if poll_id:
            state["polls"][poll_id] = {
                "correct_option_id": item["correct_option"],
                "topic": item["topic"],
                "question": item["question"],
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        sent_count += 1

    trim_poll_history(state)
    save_state(state)

    print(
        "Daily quiz sent successfully. "
        f"header_message_id={header_message_id}, polls_sent={sent_count}, "
        f"processed_poll_answers={processed_answers}"
    )


if __name__ == "__main__":
    main()