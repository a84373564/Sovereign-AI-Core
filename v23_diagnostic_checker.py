# v23_整體診斷器_diagnostic_checker.py（最猛版本）

import json
from pathlib import Path
from statistics import mean

POOL_PATH = "/mnt/data/ai/module_pool.json"
SCORE_PATH = "/mnt/data/ai/module_scores.json"
HEAL_PATH = "/mnt/data/ai/healing_log.json"
TRUST_PATH = "/mnt/data/ai/trust_index.json"
REPORT_PATH = "/mnt/data/ai/diagnostic_report.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def generate_report():
    pool = load_json(POOL_PATH).get("modules", [])
    scores = load_json(SCORE_PATH)
    healing = load_json(HEAL_PATH)
    trust = load_json(TRUST_PATH)

    total = len(pool)
    failed = sum(1 for m in pool if healing.get(m, {}).get("status") == "fail")
    empty = sum(1 for m in pool if scores.get(m, {}).get("score", -1) < 0)
    trust_vals = [v["trust_score"] for v in trust.values() if v["trust_score"] >= 0]

    report = {
        "total_modules": total,
        "syntax_failed_modules": failed,
        "empty_score_modules": empty,
        "avg_score": round(mean([s["score"] for s in scores.values() if s["score"] >= 0]), 4) if scores else 0,
        "avg_trust": round(mean(trust_vals), 4) if trust_vals else 0,
        "high_trust_count": sum(1 for v in trust_vals if v >= 0.85),
        "trust_distribution": {
            "≥0.9": sum(1 for v in trust_vals if v >= 0.9),
            "0.7–0.89": sum(1 for v in trust_vals if 0.7 <= v < 0.9),
            "<0.7": sum(1 for v in trust_vals if v < 0.7)
        }
    }

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("\n=== AI 系統診斷報告 ===")
    print(f"模組總數：{report['total_modules']}")
    print(f"語法錯誤模組數：{report['syntax_failed_modules']}")
    print(f"績效評分失敗模組數：{report['empty_score_modules']}")
    print(f"平均模組得分：{report['avg_score']}")
    print(f"平均信心指數：{report['avg_trust']}")
    print(f"高信心模組（trust ≥ 0.85）：{report['high_trust_count']}")
    print(f"信心分布：{report['trust_distribution']}")
    print("========================\n")

if __name__ == "__main__":
    generate_report()
