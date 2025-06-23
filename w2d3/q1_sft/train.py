from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
import torch

# Model name
model_name = "distilgpt2"

# Load tokenizer and model (4-bit)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float32
)

# Prepare for LoRA training
# model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["c_attn"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)

# Load dataset
dataset = load_dataset("json", data_files="dataset.jsonl")["train"]

# Tokenization
def tokenize(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=256)

tokenized_dataset = dataset.map(tokenize, batched=True)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Training arguments
fp16_flag = torch.cuda.is_available()
training_args = TrainingArguments(
    output_dir="./sft_model",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    learning_rate=5e-5,
    logging_dir="./logs",
    save_total_limit=1,
    save_strategy="epoch",
    fp16=fp16_flag,
    bf16=not fp16_flag  # Use bf16 if not using fp16 (for CPU or newer hardware)
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Train the model
trainer.train()

# Save the final model
model.save_pretrained("./sft_model")
