import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

questions=[
"If 20% of a number is 80, find the number.",
"A train 120m long crosses a pole in 6 sec. Find speed.",
"Simple interest on ₹2000 at 5% for 2 years?",
"If A can finish work in 10 days, how much work in 1 day?",
"A shopkeeper gains 20% on a product costing ₹500. Selling price?"
]

selected=random.sample(questions,2)

message="📘 Daily Aptitude Practice\n\n"

for i,q in enumerate(selected,1):
    message+=f"{i}. {q}\n\n"

url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url,data={
"chat_id":CHAT_ID,
"text":message
})