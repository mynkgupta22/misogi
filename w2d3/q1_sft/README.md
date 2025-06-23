# Tiny Supervised Fine-Tuning (SFT)

## Objective
Fine-tune a base LLM (e.g., Meta-Llama-3-8B) to become a polite, helpful assistant using only 20–30 training examples with LoRA (PEFT).

---

## Folder Structure
```
q1/
├── dataset.jsonl       # Training examples (~25)
├── train.py            # Script to run LoRA fine-tuning
├── before_after.md     # Results comparing model before vs after fine-tuning
└── README.md           # Project overview
```

---

## Dataset
Includes:
- 3 factual Q&A
- 3 polite-tone requests
- 2 long vs short answers
- 2 refusal cases
- 15+ additional helpful assistant-style responses

Each sample is wrapped in `<|user|>` and `<|assistant|>` tokens.

---

## Model & Training
- **Base model**: `NousResearch/Meta-Llama-3-8B-Instruct` or smaller
- **Fine-tuning method**: LoRA (via HuggingFace + PEFT)
- **Precision**: 4-bit via bitsandbytes
- **Epochs**: 3
- **Learning Rate**: 5e-5
- **Batch size**: 4 (adjust if needed)

---

## Training Script (train.py)
Uses HuggingFace `Trainer`, `LoRAConfig`, and 4-bit loading to reduce memory usage. Run:

```bash
python train.py
```

Model checkpoints are saved in `./sft_model`.

---

## Evaluation
We evaluate by running 5 fixed prompts before and after training and comparing the outputs side-by-side in `before_after.md`.

---

## Example Prompt
```text
<|user|>What is the capital of France?<|assistant|>The capital of France is Paris.
```

---

## Requirements
- transformers
- peft
- accelerate
- bitsandbytes
- datasets

Install via:
```bash
pip install transformers peft accelerate bitsandbytes datasets
```

---

## License
For educational and research use only.
