# v01_start_guard.py
import os
import json

CAPITAL_PATH = "/mnt/data/ai/capital_tracker.json"
DEFAULT_CAPITAL = 70.51
DEFAULT_MODE = "simulate"

def ensure_capital_file():
    if not os.path.exists(CAPITAL_PATH):
        capital_info = {"capital": DEFAULT_CAPITAL, "mode": DEFAULT_MODE}
        with open(CAPITAL_PATH, "w") as f:
            json.dump(capital_info, f)
        print(f"[start_guard] capital_tracker.json created: {capital_info}")
    else:
        print("[start_guard] capital_tracker.json exists.")

def ensure_module_dir():
    if not os.path.exists("/mnt/data/ai/modules"):
        os.makedirs("/mnt/data/ai/modules")
        print("[start_guard] modules/ directory created.")
    else:
        print("[start_guard] modules/ directory exists.")

def ensure_logs_dir():
    if not os.path.exists("/mnt/data/ai/logs"):
        os.makedirs("/mnt/data/ai/logs")
        print("[start_guard] logs/ directory created.")
    else:
        print("[start_guard] logs/ directory exists.")

if __name__ == "__main__":
    ensure_capital_file()
    ensure_module_dir()
    ensure_logs_dir()
