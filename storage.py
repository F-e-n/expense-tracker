import json
from pathlib import Path

# Where expenses are saved: a "data" folder next to this file.
DATA_FILE = Path(__file__).parent / "data" / "expenses.json"


def load_expenses():
    """Read expenses from the file. Returns an empty list if there is no file yet."""
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # The file is damaged. Keep a copy so nothing is lost, then start fresh.
        backup = DATA_FILE.with_suffix(".json.bak")
        DATA_FILE.replace(backup)
        print(f"Warning: expenses file was unreadable. Saved a copy as {backup.name}.")
        return []


def save_expenses(expenses):
    """Write the full list of expenses to the file."""
    DATA_FILE.parent.mkdir(exist_ok=True)  # create the data folder if missing
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)