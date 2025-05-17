# v03_symbol_screener_prime.py
import json
import os
import random

TOP_SYMBOLS_PATH = "/mnt/data/ai/top_symbols.json"

def get_top_symbols(limit=3):
    if not os.path.exists(TOP_SYMBOLS_PATH):
        default = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
        with open(TOP_SYMBOLS_PATH, "w") as f:
            json.dump(default, f)
        print(f"[symbol_screener] 建立預設 symbol 清單：{default}")
        return default[:limit]
    
    with open(TOP_SYMBOLS_PATH, "r") as f:
        try:
            symbols = json.load(f)
            if not isinstance(symbols, list) or len(symbols) == 0:
                raise ValueError
        except:
            symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
            print("[symbol_screener] 警告：symbol 清單損壞，使用預設值")
    
    selected = symbols[:limit]
    print(f"[symbol_screener] 使用前 {limit} 個 symbol：{selected}")
    return selected
