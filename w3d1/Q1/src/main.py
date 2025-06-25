import json
import requests
from pathlib import Path
PROMPT_DIR = Path("prompts")
EVALUATION_DIR = Path("evaluation")
INPUT_FILE = EVALUATION_DIR / "input_queries.json"
OUTPUT_FILE = EVALUATION_DIR / "output_logs.json"
# Load all input test queries
INPUT_QUERIES = json.load(open(INPUT_FILE))
PROMPT_TYPES = ["zero_shot", "few_shot", "cot_prompt", "meta_prompt"]
# Load base prompt file based on prompt type
def load_prompt(prompt_type):
    return PROMPT_DIR.joinpath(f"{prompt_type}.txt").read_text()
# Actual call to local LLM Studio server
def call_local_model(prompt: str) -> str:
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "phi-2",  # Change this if your model has a different ID
            "messages": [
                {"role": "system", "content": "You are a helpful math tutor."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 512
        }
    )
    return response.json()['choices'][0]['message']['content']
# Run the test for each prompt type and query
def run_test():
    output_log = []
    for query in INPUT_QUERIES:
        entry = {"query": query, "results": {}}
        for prompt_type in PROMPT_TYPES:
            base_prompt = load_prompt(prompt_type)
            full_prompt = f"{base_prompt}\n\nQ: {query}"
            print(f"\n:arrow_forward: Testing [{prompt_type}] → \"{query}\"")
            response = call_local_model(full_prompt)
            entry["results"][prompt_type] = {
                "response": response.strip(),
                "accuracy": None,  # You can evaluate later
                "hallucination": None,
                "reasoning": None
            }
        output_log.append(entry)
    OUTPUT_FILE.write_text(json.dumps(output_log, indent=2))
    print(f"\n:white_check_mark: Prompt tests complete.\n:memo: Output saved to: {OUTPUT_FILE}")
if __name__ == "__main__":
    run_test()