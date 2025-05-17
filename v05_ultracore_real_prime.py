# v05_ultracore_real_prime.py
import time
import importlib
import os
from v04_capital_manager_prime import load_capital
from v03_symbol_screener_prime import get_best_symbols

MODULE_PATH = "/mnt/data/ai/modules/"
LOOP_INTERVAL = 60  # 每分鐘檢查一次

def run_module(module_name, symbol, capital):
    try:
        module = importlib.import_module(f"modules.{module_name}")
        result = module.run(symbol=symbol, capital=capital)
        print(f"[ultracore] {module_name}({symbol}) 結果：{result}")
    except Exception as e:
        print(f"[ultracore] 執行 {module_name} 發生錯誤：{e}")

def main_loop():
    print("[ultracore] 主控核心已啟動")
    capital = load_capital()
    symbols = get_best_symbols()
    while True:
        files = [f for f in os.listdir(MODULE_PATH) if f.endswith(".py")]
        for module_file in files:
            module_name = module_file.replace(".py", "")
            for symbol in symbols:
                run_module(module_name, symbol, capital)
        print("[ultracore] 完成一輪模組執行，休息中...")
        time.sleep(LOOP_INTERVAL)

if __name__ == "__main__":
    main_loop()
