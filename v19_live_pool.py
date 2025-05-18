# v19_實戰候選池_live_pool.py（最猛版本）

import json
from pathlib import Path

DECISIONS_PATH = "/mnt/data/ai/decisions.json"
LIVE_POOL_PATH = "/mnt/data/ai/live_pool.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def build_live_pool():
    decisions = load_json(DECISIONS_PATH)
    live_pool = {}

    for mod, info in decisions.items():
        if info.get("live_candidate"):
            live_pool[mod] = {
                "score": info["score"],
                "win_rate": info["win_rate"],
                "profit": info["profit"],
                "drawdown": info["drawdown"],
                "sharpe": info["sharpe"],
                "multi_symbol": info["multi_symbol"],
                "live_flag": True
            }

    save_json(live_pool, LIVE_POOL_PATH)
    print(f"[live_pool] Live pool created: {len(live_pool)} modules eligible.")

if __name__ == "__main__":
    build_live_pool()
