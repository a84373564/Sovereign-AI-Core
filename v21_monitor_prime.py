# v21_monitor_prime.py（最猛版本）

import json
from pathlib import Path

SCORE_PATH = "/mnt/data/ai/module_scores.json"
DECISION_PATH = "/mnt/data/ai/decisions.json"
RECOMM_PATH = "/mnt/data/ai/recommendations.json"
LIVE_POOL_PATH = "/mnt/data/ai/live_pool.json"
CAPITAL_PATH = "/mnt/data/capital_tracker.json"
FUND_PATH = "/mnt/data/ai/fund_plan.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def display_module_info():
    scores = load_json(SCORE_PATH)
    decisions = load_json(DECISION_PATH)
    recommends = load_json(RECOMM_PATH)
    live_pool = load_json(LIVE_POOL_PATH)
    capital = load_json(CAPITAL_PATH).get("capital", 0)
    fund_plan = load_json(FUND_PATH)

    print("\n====== Sovereign AI Monitoring Center ======\n")
    print(f"Total Capital: {capital:.2f} USDT\n")

    for mod, score in scores.items():
        dec = decisions.get(mod, {})
        is_live = mod in live_pool
        alloc = fund_plan.get(mod, {}).get("alloc_usdt", 0)
        recommend = any(r.get("module") == mod for r in recommends)

        line = f"{mod:<35} | "
        line += f"Score: {score['score']:.2f} | WinRate: {score['win_rate']:.2%} | "
        line += f"Profit: {score['profit']:.2f} | Sharpe: {score['sharpe']:.2f} | "

        flags = []
        if dec.get("multi_symbol"):
            flags.append("Multi")
        if is_live:
            flags.append("LIVE")
        if recommend:
            flags.append("RECOMMENDED")
        if alloc > 0:
            flags.append(f"ALLOC:{alloc:.2f}")

        line += "Flags: [" + ", ".join(flags) + "]"
        print(line)

    print("\n============================================\n")

if __name__ == "__main__":
    display_module_info()
