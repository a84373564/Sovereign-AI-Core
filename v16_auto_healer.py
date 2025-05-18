# v16_修復核心_auto_healer.py（AST 結構修補強化版）

import ast
import os
import json
from pathlib import Path

MODULE_DIR = "/mnt/data/ai/modules"
HEALING_LOG = "/mnt/data/ai/healing_log.json"
POOL_PATH = "/mnt/data/ai/module_pool.json"

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def has_run_function(tree):
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "run":
            return True
    return False

def append_run_stub(code):
    stub = "\n\ndef run(data, capital, history):\n    return {'status': 'patched', 'score': 0}\n"
    return code + stub

def heal_module(path):
    with open(path, "r") as f:
        code = f.read()

    try:
        tree = ast.parse(code)
        if not has_run_function(tree):
            print(f"[auto_healer] Missing run(): {path}, auto-patching.")
            patched_code = append_run_stub(code)
            with open(path, "w") as f2:
                f2.write(patched_code)
            return {"status": "patched", "issue": "missing_run"}
        return {"status": "ok"}
    except SyntaxError as e:
        print(f"[auto_healer] Syntax error in {path}: {e}")
        return {"status": "fail", "error": str(e)}

def heal_all():
    pool = load_json(POOL_PATH).get("modules", [])
    log = {}

    for mod in pool:
        mod_path = os.path.join(MODULE_DIR, mod)
        if not os.path.exists(mod_path):
            continue
        result = heal_module(mod_path)
        log[mod] = result

    save_json(log, HEALING_LOG)
    print(f"[auto_healer] Healing complete. Checked: {len(pool)} modules.")

if __name__ == "__main__":
    heal_all()
