# Prompt Engineering Pipeline – Multi-Path Reasoning + Prompt Optimization

## 🔍 Objective
This project builds a reasoning pipeline with:
- Tree-of-Thought (multi-path reasoning)
- Self-Consistency (majority voting)
- Prompt Optimization (via feedback)

## 📁 Structure
- `tasks/` – Problem statements and expected answers
- `prompts/` – Base prompt and optimizer prompt
- `src/main.py` – Main script for generating paths
- `logs/` – Reasoning logs per run
- `evaluation/` – Metrics and reflection

## ▶️ How to Run
1. Add your local LLM integration to `simulate_trees_of_thought()`
2. Run:
   ```
   cd src
   python main.py
   ```
3. Check `logs/reasoning_logs.json` for generated reasoning paths

## 🔄 Prompt Optimization
Use `prompts/optimizer_prompt.txt` to guide LLM on improving prompts based on past failure cases.
