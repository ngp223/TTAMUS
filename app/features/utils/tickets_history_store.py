import json
from pathlib import Path

TICKET_FILE = Path(__file__).resolve().parents[2] / "tmp" / "last_ticket_history.json"

def save_ticket_history(date, amount):
    TICKET_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TICKET_FILE, "w", encoding="utf-8") as f:
        json.dump({"date": date, "amount": amount}, f, ensure_ascii=False, indent=2)

def load_ticket_history():
    if not TICKET_FILE.exists():
        return None
    with open(TICKET_FILE, "r", encoding="utf-8") as f:
        return json.load(f)