import json
import re
from pathlib import Path

INPUT_FILE = Path("data/questions_from_pdf.json")
OUTPUT_FILE = Path("data/questions_from_pdf.json")


def normalize_spaces(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_question(text: str) -> str:
    text = normalize_spaces(text)
    text = re.sub(r"\s*\|\s*", " ", text)
    text = re.sub(r"\bq\.?\s*no\.?\b", "Q.No", text, flags=re.IGNORECASE)
    text = text.strip(" .")
    if text and text[-1] not in "?.!":
        text += "?"
    return text


def clean_option(text: str) -> str:
    text = normalize_spaces(text)
    text = re.sub(r"^[A-Da-d][\).:\-]\s*", "", text)
    text = re.sub(r"\s*\|\s*", " ", text)
    text = text.strip(" .")
    return text


def topic_explanation(topic: str) -> str:
    t = topic.lower()
    if "work" in t:
        return (
            "Use LCM method: assume total work as LCM of individual times, convert each rate per day, then combine and compute required time/work."
        )
    if "distance" in t:
        return "Use speed-distance-time relation: distance = speed x time, and convert units before calculation."
    if "interest" in t:
        return "Use SI/CI formulas carefully, substituting principal, rate, and time with consistent units."
    if "profit" in t or "loss" in t:
        return "Use cost price and selling price relation, then compute percentage on cost price unless stated otherwise."
    if "percentage" in t:
        return "Convert percentages to fractions/decimals first, then solve systematically."
    return "Read all options carefully, eliminate impossible choices, then verify the final answer."


def normalize_record(item: dict) -> dict | None:
    if not isinstance(item, dict):
        return None

    question = clean_question(str(item.get("question", "")))
    if len(question) < 8:
        return None

    options_raw = item.get("options", [])
    if not isinstance(options_raw, list):
        return None

    options = []
    for opt in options_raw:
        cleaned = clean_option(str(opt))
        if cleaned:
            options.append(cleaned)

    if len(options) < 2:
        return None

    topic = normalize_spaces(str(item.get("topic", "General Aptitude"))) or "General Aptitude"

    correct_option = item.get("correct_option")
    if isinstance(correct_option, int) and 0 <= correct_option < len(options):
        answer_available = True
        answer_key = chr(ord("A") + correct_option)
    else:
        correct_option = None
        answer_available = False
        answer_key = "PENDING"

    return {
        "topic": topic,
        "question": question,
        "options": options,
        "correct_option": correct_option,
        "answer_key": answer_key,
        "answer_available": answer_available,
        "explanation": topic_explanation(topic),
    }


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Expected a list of question objects")

    curated = []
    seen = set()
    for item in data:
        normalized = normalize_record(item)
        if not normalized:
            continue

        key = (normalized["question"], tuple(normalized["options"]))
        if key in seen:
            continue
        seen.add(key)
        curated.append(normalized)

    OUTPUT_FILE.write_text(
        json.dumps(curated, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with_answer = sum(1 for q in curated if q["answer_available"])
    without_answer = len(curated) - with_answer
    print(f"Curated questions: {len(curated)}")
    print(f"With answer keys: {with_answer}")
    print(f"Pending answer keys: {without_answer}")


if __name__ == "__main__":
    main()
