import json
from pathlib import Path

TMP_DIR = Path(__file__).resolve().parents[2] / "tmp"
TICKET_FILE = TMP_DIR / "last_ticket.json"
CLOSURE_FILE = TMP_DIR / "last_closure.json"


def _save(file_path, date, amount):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"date": date, "amount": amount}, f, ensure_ascii=False, indent=2)


def _load(file_path):
    if not file_path.exists():
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def save_ticket(date, amount):
    _save(TICKET_FILE, date, amount)


def load_ticket():
    return _load(TICKET_FILE)


def save_closure(date, amount):
    _save(CLOSURE_FILE, date, amount)


def load_closure():
    return _load(CLOSURE_FILE)