# v25_復原設定檔 recovery_generator.py（最猛版本）

import json
from pathlib import Path
from statistics import mean

POOL_PATH = "/mnt/data/ai/module_pool.json"
CAPITAL_PATH = "/mnt/data/capital_tracker.json"
RECOMM_PATH = "/mnt/data/ai/recommendations.json"
SCORE_PATH = "/mnt/data/ai/module_scores.json"
TRUST_PATH = "/mnt/data/ai/trust_index.json"
RECOVERY_PATH = "/mnt/data/ai/recovery_prime.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def generate_recovery_snapshot():
    pool = load_json(POOL_PATH)
    capital = load_json(CAPITAL_PATH)
    recomms = load_json(RECOMM_PATH)
    scores = load_json(SCORE_PATH)
    trust = load_json(TRUST_PATH)

    score_vals = [v["score"] for v in scores.values() if v.get("score", -1) >= 0]
    trust_vals = [v["trust_score"] for v in trust.values() if v.get("trust_score", -1) >= 0]

    recovery = {
        "capital": capital.get("capital", 0),
        "modules": pool.get("modules", []),
        "recommended_modules": [r["module"] for r in recomms],
        "avg_score": round(mean(score_vals), 4) if score_vals else 0,
        "avg_trust": round(mean(trust_vals), 4) if trust_vals else 0,
        "high_trust_count": sum(1 for v in trust_vals if v >= 0.85)
    }

    save_json(recovery, RECOVERY_PATH)
    print(f"[recovery_generator] Recovery snapshot saved. Modules: {len(recovery['modules'])}")

if __name__ == "__main__":
    generate_recovery_snapshot()
