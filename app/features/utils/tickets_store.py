import json
from pathlib import Path

TICKET_FILE = Path(__file__).resolve().parents[2] / "tmp" / "last_ticket.json"

def save_ticket(date, amount):

    TICKET_FILE.parent.mkdir(exist_ok=True)

    with open(TICKET_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "date": date,
            "amount": amount
        }, f)


def load_ticket():

    if not TICKET_FILE.exists():
        return None

    try:
        with open(TICKET_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return None