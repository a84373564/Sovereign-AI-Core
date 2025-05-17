# v02_data_manager.py
import json
import os

CAPITAL_FILE = "/mnt/data/ai/capital_tracker.json"
SYMBOL_FILE = "/mnt/data/ai/top_symbols.json"

def load_capital_info():
    with open(CAPITAL_FILE, "r") as f:
        return json.load(f)

def load_top_symbols():
    if not os.path.exists(SYMBOL_FILE):
        return ["BTCUSDT"]
    with open(SYMBOL_FILE, "r") as f:
        return json.load(f)

def save_top_symbols(symbols):
    with open(SYMBOL_FILE, "w") as f:
        json.dump(symbols, f, indent=2)
