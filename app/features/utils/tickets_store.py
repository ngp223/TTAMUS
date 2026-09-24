import json
from pathlib import Path

FILE = Path("tmp/last_ticket.json")


def save_ticket(date, amount):

    FILE.parent.mkdir(exist_ok=True)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump({
            "date": date,
            "amount": amount
        }, f)


def load_ticket():

    if not FILE.exists():
        return None

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return None