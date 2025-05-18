# v13_AI 建議器_ai_recommender.py（終極增強版）

import json
from pathlib import Path

DECISION_PATH = "/mnt/data/ai/decisions.json"
RECOMMEND_PATH = "/mnt/data/ai/recommendations.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def recommend():
    decisions = load_json(DECISION_PATH)
    candidates = []

    for mod, info in decisions.items():
        if info.get("live_candidate"):
            candidates.append({
                "module": mod,
                "score": info.get("score", 0),
                "win_rate": info.get("win_rate", 0),
                "profit": info.get("profit", 0),
                "sharpe": info.get("sharpe", 0),
                "drawdown": info.get("drawdown", 0),
                "multi_symbol": info.get("multi_symbol", False)
            })

    # 根據 score + profit + win_rate 排序
    sorted_list = sorted(
        candidates,
        key=lambda x: (x["score"], x["win_rate"], x["profit"]),
        reverse=True
    )

    save_json(sorted_list, RECOMMEND_PATH)
    print(f"[ai_recommender] Top {len(sorted_list)} modules recommended.")

if __name__ == "__main__":
    recommend()
