# v14_記憶圖譜記錄器_memory_graph.py（超級強化版）

import json
from pathlib import Path
from datetime import datetime

GRAPH_PATH = "/mnt/data/ai/memory_graph.json"
POOL_PATH = "/mnt/data/ai/module_pool.json"
DECISION_PATH = "/mnt/data/ai/decisions.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def update_graph():
    graph = load_json(GRAPH_PATH)
    pool = load_json(POOL_PATH).get("modules", [])
    decisions = load_json(DECISION_PATH)

    updated = 0

    for mod in pool:
        if mod not in graph:
            # 新模組記錄
            graph[mod] = {
                "type": "unknown",
                "parents": [],
                "generation": 1,
                "created": str(datetime.utcnow()),
                "recommended": False
            }
            updated += 1
        else:
            # 補上推薦標記
            if decisions.get(mod, {}).get("live_candidate"):
                graph[mod]["recommended"] = True

    save_json(graph, GRAPH_PATH)
    print(f"[memory_graph] Graph updated. New entries: {updated}, total: {len(graph)}")

if __name__ == "__main__":
    update_graph()
