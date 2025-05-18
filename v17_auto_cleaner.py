# v17_清除機制_auto_cleaner.py（極致防雜版）

import os
import json
from pathlib import Path

MODULE_DIR = "/mnt/data/ai/modules"
POOL_PATH = "/mnt/data/ai/module_pool.json"
SCORE_PATH = "/mnt/data/ai/module_scores.json"
SIM_PATH = "/mnt/data/ai/sim_results.json"
HEAL_LOG = "/mnt/data/ai/healing_log.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def should_delete(mod, score_data, sim_data, heal_log):
    score = score_data.get(mod, {}).get("score", -1)
    win_rate = score_data.get(mod, {}).get("win_rate", 0)
    sim_list = sim_data.get(mod, [])
    heal_info = heal_log.get(mod, {})

    if score < 0:
        return True
    if any(x.get("status") == "fail" for x in sim_list):
        return True
    if score < 1.0 and win_rate < 0.5:
        return True
    if heal_info.get("status") == "fail":
        return True
    return False

def clean_modules():
    pool_data = load_json(POOL_PATH)
    score_data = load_json(SCORE_PATH)
    sim_data = load_json(SIM_PATH)
    heal_log = load_json(HEAL_LOG)

    modules = pool_data.get("modules", [])
    retained = []

    for mod in modules:
        if should_delete(mod, score_data, sim_data, heal_log):
            mod_path = os.path.join(MODULE_DIR, mod)
            if os.path.exists(mod_path):
                os.remove(mod_path)
                print(f"[auto_cleaner] Removed low-quality module: {mod}")
        else:
            retained.append(mod)

    # 更新 pool
    pool_data["modules"] = retained
    save_json(pool_data, POOL_PATH)

    print(f"[auto_cleaner] Cleaning done. Retained: {len(retained)} modules.")

if __name__ == "__main__":
    clean_modules()
