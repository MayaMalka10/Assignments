import json
import random
from pathlib import Path


NAMES = ["Shirel", "Maya", "Yana", "Etai", "Keren", "Dvora"]
HISTORY_FILE = Path(__file__).with_name("lab_assignment_history.json")
COOLDOWN_PICKS = 4


def load_history():
    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        history = json.load(file)

    if not isinstance(history, list) or not all(
        isinstance(name, str) and name in NAMES for name in history
    ):
        raise ValueError(f"{HISTORY_FILE.name} contains an invalid assignment history.")

    return history[-COOLDOWN_PICKS:]


def choose_person():
    history = load_history()
    available_names = [name for name in NAMES if name not in history]

    chosen_name = random.choice(available_names)
    history.append(chosen_name)

    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history[-COOLDOWN_PICKS:], file, indent=2)

    return chosen_name


if __name__ == "__main__":
    print(f"This week's lab assignment goes to: {choose_person()}")
