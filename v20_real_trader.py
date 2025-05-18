# v20_實戰執行器_real_trader.py（最猛版本）

import json
from pathlib import Path
from datetime import datetime

LIVE_POOL_PATH = "/mnt/data/ai/live_pool.json"
FUND_PLAN_PATH = "/mnt/data/ai/fund_plan.json"
CAPITAL_PATH = "/mnt/data/capital_tracker.json"
TRADE_LOG_PATH = "/mnt/data/ai/trade_log.json"

# 模擬與實戰切換（建議保持 simulate，改 live 才執行實單）
MODE = "simulate"  # or "live"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def execute_trades():
    pool = load_json(LIVE_POOL_PATH)
    funds = load_json(FUND_PLAN_PATH)
    capital = load_json(CAPITAL_PATH).get("capital", 0)
    log = []

    for mod, info in pool.items():
        alloc_info = funds.get(mod)
        if not alloc_info:
            continue

        trade = {
            "module": mod,
            "symbol": alloc_info.get("symbol", "BTCUSDT"),
            "amount_usdt": alloc_info.get("alloc_usdt", 0),
            "multi_symbol": alloc_info.get("multi_symbol", False),
            "mode": MODE,
            "timestamp": str(datetime.utcnow())
        }

        if MODE == "simulate":
            trade["status"] = "simulated"
        elif MODE == "live":
            # 真正下單請在此整合交易所 API
            # 這裡僅做佔位符
            trade["status"] = "executed"
            trade["order_id"] = f"order_{mod}_{datetime.utcnow().timestamp()}"
        else:
            trade["status"] = "skipped"

        log.append(trade)

    save_json(log, TRADE_LOG_PATH)
    print(f"[real_trader] Trade execution complete. Mode: {MODE} | Orders: {len(log)}")

if __name__ == "__main__":
    execute_trades()
