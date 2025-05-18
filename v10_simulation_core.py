# v10_模擬核心_simulation_core.py（極限增強版）

import os
import json
import importlib.util
import traceback
from pathlib import Path
from datetime import datetime

MODULE_DIR = "/mnt/data/ai/modules"
RESULT_PATH = "/mnt/data/ai/sim_results.json"
POOL_PATH = "/mnt/data/ai/module_pool.json"
DATA_PATH = "/mnt/data/ai/recent_data.json"
HISTORY_PATH = "/mnt/data/ai/history_data.json"
CAPITAL_PATH = "/mnt/data/capital_tracker.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def simulate_module(module_path, data, capital, history):
    try:
        spec = importlib.util.spec_from_file_location("mod", module_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if hasattr(mod, "run"):
            result = mod.run(data, capital, history)
            assert isinstance(result, dict), "Module output must be a dict"
            result["status"] = "ok"
        else:
            raise Exception("Missing run()")
    except Exception as e:
        result = {
            "status": "fail",
            "error": str(e),
            "traceback": traceback.format_exc()
        }
    return result

def get_symbols():
    # 支援多幣演化，如果失敗則 fallback
    try:
        from symbol_screener_prime import get_best_symbols
        symbols = get_best_symbols()
        return symbols if isinstance(symbols, list) and symbols else ["BTCUSDT"]
    except:
        return ["BTCUSDT"]

def simulate_all():
    pool = load_json(POOL_PATH)
    modules = pool.get("modules", [])
    capital = load_json(CAPITAL_PATH).get("capital", 70.0)
    data = load_json(DATA_PATH)
    history = load_json(HISTORY_PATH)
    symbols = get_symbols()

    results = {}

    for mod_file in modules:
        mod_path = os.path.join(MODULE_DIR, mod_file)
        results[mod_file] = []

        for sym in symbols:
            sim_data = data.get(sym, {})
            sim_hist = history.get(sym, [])
            output = simulate_module(mod_path, sim_data, capital, sim_hist)

            output.update({
                "symbol": sym,
                "sim_time": str(datetime.utcnow())
            })

            results[mod_file].append(output)

    save_json(results, RESULT_PATH)
    print(f"[simulation_core] Simulation completed. Modules: {len(modules)} | Symbols: {symbols}")

if __name__ == "__main__":
    simulate_all()
