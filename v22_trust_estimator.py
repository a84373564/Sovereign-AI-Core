# v22_信心演算法_trust_estimator.py（最猛版本）

import json
from pathlib import Path
from statistics import mean

GRAPH_PATH = "/mnt/data/ai/memory_graph.json"
SCORE_PATH = "/mnt/data/ai/module_scores.json"
HEAL_PATH = "/mnt/data/ai/healing_log.json"
TRUST_PATH = "/mnt/data/ai/trust_index.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 0
    return max(0, min(1, (value - min_val) / (max_val - min_val)))

def estimate_trust():
    graph = load_json(GRAPH_PATH)
    scores = load_json(SCORE_PATH)
    healing = load_json(HEAL_PATH)
    result = {}

    for mod in graph:
        score = scores.get(mod, {})
        heal = healing.get(mod, {})
        base = graph.get(mod, {})

        s = score.get("score", 0)
        wr = score.get("win_rate", 0)
        sh = score.get("sharpe", 0)
        gen = base.get("generation", 1)
        stable = heal.get("status") != "fail"

        # 規則：score+win_rate+sharpe 決定績效信心 (60%)
        perf_score = (
            normalize(s, 0, 4) * 0.4 +
            normalize(wr, 0, 1) * 0.3 +
            normalize(sh, 0, 2) * 0.3
        )

        # 來源與代數（20%）
        source_score = 0.2 if base.get("type") == "hybrid" else 0.1
        if gen >= 3:
            source_score += 0.1

        # 穩定性（20%）
        stable_score = 0.2 if stable else 0

        trust = round(perf_score + source_score + stable_score, 4)
        result[mod] = {"trust_score": trust}

    save_json(result, TRUST_PATH)
    print(f"[trust_estimator] Trust scores generated for {len(result)} modules.")

if __name__ == "__main__":
    estimate_trust()
