# v15_策略圖譜分析器_strategy_mapper.py（戰略導向增強版）

import json
from pathlib import Path
from statistics import mean

GRAPH_PATH = "/mnt/data/ai/memory_graph.json"
SCORE_PATH = "/mnt/data/ai/module_scores.json"
DECISION_PATH = "/mnt/data/ai/decisions.json"
MAP_PATH = "/mnt/data/ai/strategy_map.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def analyze():
    graph = load_json(GRAPH_PATH)
    scores = load_json(SCORE_PATH)
    decisions = load_json(DECISION_PATH)

    lineage_stats = {}
    gen_scores = {}
    multi_count = {"multi": 0, "single": 0}

    for mod, meta in graph.items():
        score = scores.get(mod, {}).get("score", -1)
        typ = meta.get("type", "unknown")
        gen = meta.get("generation", 1)
        multi = decisions.get(mod, {}).get("multi_symbol", False)

        # 統計血統平均分數
        if typ not in lineage_stats:
            lineage_stats[typ] = []
        if score >= 0:
            lineage_stats[typ].append(score)

        # 統計世代績效
        if gen not in gen_scores:
            gen_scores[gen] = []
        if score >= 0:
            gen_scores[gen].append(score)

        # 統計多幣比例
        if multi:
            multi_count["multi"] += 1
        else:
            multi_count["single"] += 1

    map_result = {
        "lineage_score_avg": {k: round(mean(v), 4) for k, v in lineage_stats.items()},
        "generation_score_avg": {str(k): round(mean(v), 4) for k, v in gen_scores.items()},
        "symbol_support_ratio": multi_count
    }

    save_json(map_result, MAP_PATH)
    print(f"[strategy_mapper] Strategy map updated. Bloodlines analyzed: {len(lineage_stats)}")

if __name__ == "__main__":
    analyze()
