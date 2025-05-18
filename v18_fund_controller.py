# v18_資金決策器_fund_controller.py（實戰模擬分配引擎）

import json
from pathlib import Path

CAPITAL_PATH = "/mnt/data/capital_tracker.json"
RECOMM_PATH = "/mnt/data/ai/recommendations.json"
FUND_PLAN_PATH = "/mnt/data/ai/fund_plan.json"

MIN_ALLOC_USDT = 5.0  # 單一模組最低分配門檻

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def fund_allocation():
    capital_data = load_json(CAPITAL_PATH)
    recommend_list = load_json(RECOMM_PATH)
    total_capital = capital_data.get("capital", 0)

    if total_capital <= 0 or not recommend_list:
        print("[fund_controller] No capital or recommendations available.")
        save_json({}, FUND_PLAN_PATH)
        return

    # 評分加權配置
    scores = [r["score"] for r in recommend_list]
    score_sum = sum(scores)
    if score_sum == 0:
        save_json({}, FUND_PLAN_PATH)
        return

    plan = {}
    for r in recommend_list:
        pct = r["score"] / score_sum
        alloc = round(pct * total_capital, 2)
        if alloc >= MIN_ALLOC_USDT:
            plan[r["module"]] = {
                "alloc_usdt": alloc,
                "symbol": r["symbol"],
                "multi_symbol": r.get("multi_symbol", False)
            }

    save_json(plan, FUND_PLAN_PATH)
    print(f"[fund_controller] Fund plan generated for {len(plan)} modules.")

if __name__ == "__main__":
    fund_allocation()
