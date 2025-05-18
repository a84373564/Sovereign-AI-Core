# v12_AI 決策器_ai_decider.py（終極增強版）

import os
import json
from pathlib import Path

SCORE_PATH = "/mnt/data/ai/module_scores.json"
POOL_PATH = "/mnt/data/ai/module_pool.json"
DECISION_PATH = "/mnt/data/ai/decisions.json"
MODULE_DIR = "/mnt/data/ai/modules"

# 實戰門檻標準
MIN_SCORE = 2.5
MIN_WIN_RATE = 0.7
MIN_PROFIT = 0.8
MIN_DRAWDOWN = -1.8
MIN_SHARPE = 1.2

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def check_multisymbol(path):
    try:
        with open(path, "r") as f:
            content = f.read()
            return "get_best_symbols" in content
    except:
        return False

def meets_live_criteria(metrics):
    return (
        metrics.get("score", 0) >= MIN_SCORE and
        metrics.get("win_rate", 0) >= MIN_WIN_RATE and
        metrics.get("profit", 0) >= MIN_PROFIT and
        metrics.get("drawdown", 0) >= MIN_DRAWDOWN and
        metrics.get("sharpe", 0) >= MIN_SHARPE
    )

def decide():
    scores = load_json(SCORE_PATH)
    pool = load_json(POOL_PATH).get("modules", [])
    decisions = {}

    for mod in pool:
        path = os.path.join(MODULE_DIR, mod)
        metrics = scores.get(mod, {})
        if not metrics or metrics.get("score", -1) < 0:
            continue

        multisym = check_multisymbol(path)
        eligible = meets_live_criteria(metrics)

        decisions[mod] = {
            "score": metrics["score"],
            "win_rate": metrics["win_rate"],
            "profit": metrics["profit"],
            "drawdown": metrics["drawdown"],
            "sharpe": metrics["sharpe"],
            "multi_symbol": multisym,
            "live_candidate": eligible
        }

    save_json(decisions, DECISION_PATH)
    print(f"[ai_decider] Decisions saved for {len(decisions)} modules.")

if __name__ == "__main__":
    decide()
