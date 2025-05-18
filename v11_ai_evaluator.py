# v11_AI 評估核心_ai_evaluator.py（終極增強版）

import json
from pathlib import Path
from statistics import mean, stdev

SIM_PATH = "/mnt/data/ai/sim_results.json"
SCORE_PATH = "/mnt/data/ai/module_scores.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def safe_div(x, y):
    try:
        return x / y if y != 0 else 0
    except:
        return 0

def calculate_metrics(results):
    wins, profits, drawdowns, sharpes = 0, [], [], []
    total = 0

    for r in results:
        if r.get("status") != "ok":
            continue
        p = r.get("PnL", 0)
        d = r.get("drawdown", 0)
        s = r.get("sharpe", 0)
        profits.append(p)
        drawdowns.append(d)
        sharpes.append(s)
        if p > 0:
            wins += 1
        total += 1

    if total == 0:
        return {
            "win_rate": 0,
            "profit": 0,
            "drawdown": 0,
            "sharpe": 0,
            "score": -1
        }

    win_rate = round(safe_div(wins, total), 4)
    profit = round(mean(profits), 4)
    drawdown = round(mean(drawdowns), 4)
    sharpe = round(mean(sharpes), 4)

    # 自定義分數公式（可在 v15 策略圖譜優化）
    score = round(
        2 * win_rate +
        1.5 * profit +
        0.5 * sharpe +
        drawdown, 4
    )

    return {
        "win_rate": win_rate,
        "profit": profit,
        "drawdown": drawdown,
        "sharpe": sharpe,
        "score": score
    }

def evaluate_all():
    sim_data = load_json(SIM_PATH)
    summary = {}

    for mod_name, result_list in sim_data.items():
        metrics = calculate_metrics(result_list)
        summary[mod_name] = metrics

    with open(SCORE_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"[ai_evaluator] Score evaluation completed. {len(summary)} modules scored.")

if __name__ == "__main__":
    evaluate_all()
