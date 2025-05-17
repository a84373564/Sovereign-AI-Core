# v08_evolution_builder.py
import os
import json
import random
import shutil

MODULE_DIR = "/mnt/data/ai/modules"
TEMPLATE_FILE = "/mnt/data/ai/template_logic.py"
MEMORY_PATH = "/mnt/data/ai/memory_graph.json"

def load_template():
    with open(TEMPLATE_FILE, "r") as f:
        return f.read()

def mutate_logic(template_code):
    lines = template_code.split("\n")
    if "threshold" in template_code:
        lines = [line.replace("threshold = 0.8", f"threshold = {round(random.uniform(0.6, 0.95), 2)}") for line in lines]
    if "multiplier" in template_code:
        lines = [line.replace("multiplier = 1.0", f"multiplier = {round(random.uniform(0.8, 1.5), 2)}") for line in lines]
    return "\n".join(lines)

def generate_module():
    base_code = load_template()
    mutated_code = mutate_logic(base_code)

    filename = f"mod_{random.randint(10000,99999)}.py"
    full_path = os.path.join(MODULE_DIR, filename)
    with open(full_path, "w") as f:
        f.write(mutated_code)

    print(f"[evolution_builder] 建立新模組：{filename}")
    update_memory(filename)
    return filename

def update_memory(filename):
    if not os.path.exists(MEMORY_PATH):
        memory = {"origin": []}
    else:
        with open(MEMORY_PATH, "r") as f:
            memory = json.load(f)

    memory["origin"].append({"name": filename, "type": "mutation"})
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def run():
    ensure_dirs()
    for _ in range(3):  # 預設每輪產生 3 個模組
        generate_module()

def ensure_dirs():
    os.makedirs(MODULE_DIR, exist_ok=True)
    if not os.path.exists(TEMPLATE_FILE):
        raise FileNotFoundError("[evolution_builder] 缺少 template_logic.py 模板檔案")

if __name__ == "__main__":
    run()
