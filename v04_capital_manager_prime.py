# v04_capital_manager_prime.py
import os
import json

CAPITAL_PATH = "/mnt/data/ai/capital_tracker.json"

def load_capital():
    if not os.path.exists(CAPITAL_PATH):
        return 0.0
    with open(CAPITAL_PATH, "r") as f:
        data = json.load(f)
    return data.get("capital", 0.0)

def save_capital(amount):
    with open(CAPITAL_PATH, "w") as f:
        json.dump({"capital": round(amount, 4)}, f)

def update_capital(profit_delta):
    current = load_capital()
    new_capital = current + profit_delta
    save_capital(new_capital)
    print(f"[capital_manager] 資金已更新：{current} → {new_capital}")
