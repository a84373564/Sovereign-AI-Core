# v09_演化引擎_evolution_core.py（極限增強版）

import os
import json
import random
import hashlib
from pathlib import Path
from datetime import datetime

MODULE_DIR = "/mnt/data/ai/modules"
TEMPLATE_PATH = "/mnt/data/ai/template_logic.py"
MEMORY_GRAPH_PATH = "/mnt/data/ai/memory_graph.json"
POOL_PATH = "/mnt/data/ai/module_pool.json"

def hash_content(content):
    return hashlib.md5(content.encode()).hexdigest()[:8]

def load_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()

def load_json(path):
    if Path(path).exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_pool():
    return load_json(POOL_PATH)

def save_pool(pool):
    save_json(pool, POOL_PATH)

def load_memory_graph():
    return load_json(MEMORY_GRAPH_PATH)

def save_memory_graph(graph):
    save_json(graph, MEMORY_GRAPH_PATH)

def hybrid_logic(logic1, logic2):
    lines1 = logic1.splitlines()
    lines2 = logic2.splitlines()
    mid = len(lines1) // 2
    return "\n".join(lines1[:mid] + lines2[mid:])

def create_module_file(code, label):
    gen_hash = hash_content(code)
    filename = f"mod_{label}_{gen_hash}.py"
    path = os.path.join(MODULE_DIR, filename)
    with open(path, "w") as f:
        f.write(code)
    return filename

def evolve():
    os.makedirs(MODULE_DIR, exist_ok=True)
    template = load_template()
    pool = get_pool()
    graph = load_memory_graph()

    modules = pool.get("modules", [])
    generation = pool.get("generation", 1)
    new_modules = []

    if len(modules) >= 2:
        parent1 = random.choice(modules)
        parent2 = random.choice([m for m in modules if m != parent1])
        try:
            with open(os.path.join(MODULE_DIR, parent1), "r") as f1, open(os.path.join(MODULE_DIR, parent2), "r") as f2:
                logic1 = f1.read()
                logic2 = f2.read()
            hybrid_code = hybrid_logic(logic1, logic2).replace("#__MUTATE__", str(random.randint(1, 9999)))
            filename = create_module_file(hybrid_code, "hybrid")
            new_modules.append(filename)

            # memory_graph 記錄
            graph[filename] = {
                "type": "hybrid",
                "parents": [parent1, parent2],
                "generation": generation,
                "created": str(datetime.utcnow())
            }
        except Exception as e:
            print(f"[evolution_core] Hybrid failed: {e}")

    else:
        # fallback：純突變
        mutated = template.replace("#__MUTATE__", str(random.randint(1, 9999)))
        filename = create_module_file(mutated, "mutate")
        new_modules.append(filename)
        graph[filename] = {
            "type": "mutate",
            "parents": [],
            "generation": generation,
            "created": str(datetime.utcnow())
        }

    # 更新模組池
    modules += new_modules
    modules = list(set(modules))[-50:]
    pool["modules"] = modules
    pool["generation"] = generation + 1

    save_pool(pool)
    save_memory_graph(graph)
    print(f"[evolution_core] New modules: {new_modules} | Generation: {generation}")

if __name__ == "__main__":
    evolve()
