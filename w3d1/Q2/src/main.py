import json
from pathlib import Path

TASKS = json.load(open(Path("../tasks/tasks.json")))
PROMPT = Path("../prompts/initial_prompt.txt").read_text()

def simulate_trees_of_thought(task, n_paths=3):
    return [f"[Thought path {i+1} for: {task['description']}]" for i in range(n_paths)]

def aggregate_answers(paths):
    return {"consensus": "Simulated Answer", "paths": paths}

def run_pipeline():
    results = []
    for task in TASKS:
        paths = simulate_trees_of_thought(task)
        result = aggregate_answers(paths)
        results.append({
            "task": task["description"],
            "expected": task["solution"],
            "generated": result["consensus"],
            "paths": result["paths"]
        })
    Path("../logs/reasoning_logs.json").write_text(json.dumps(results, indent=2))
    print("Reasoning paths generated and logged.")

if __name__ == "__main__":
    run_pipeline()
