import sys
import os
import json
import logging

logger = logging.getLogger(__name__)

def train(dataset_path: str = "backend/dataset.json", output_dir: str = "backend/fine_tuning/lora_model"):
    """
    Fine-tunes a Llama 3 model using Unsloth.
    """
    try:
        from unsloth import FastLanguageModel
        from trl import SFTTrainer
        from transformers import TrainingArguments
        from datasets import load_dataset
        import torch
    except ImportError:
        logger.error("Error: 'unsloth' or 'trl' is not installed. Training cannot proceed.")
        logger.error("Please install dependencies suited for your CUDA version.")
        return {"status": "error", "message": "Unsloth/TRL not installed."}

    logger.info(f"Starting training with dataset: {dataset_path}")

    max_seq_length = 2048 
    dtype = None 
    load_in_4bit = True 

    try:
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name = "unsloth/llama-3-8b-bnb-4bit",
            max_seq_length = max_seq_length,
            dtype = dtype,
            load_in_4bit = load_in_4bit,
        )

        model = FastLanguageModel.get_peft_model(
            model,
            r = 16, 
            target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                            "gate_proj", "up_proj", "down_proj",],
            lora_alpha = 16,
            lora_dropout = 0,
            bias = "none",  
            use_gradient_checkpointing = "unsloth", 
            random_state = 3407,
            use_rslora = False,
            loftq_config = None,
        )

        # Load dataset
        if not os.path.exists(dataset_path):
             return {"status": "error", "message": f"Dataset file not found: {dataset_path}"}
             
        dataset = load_dataset("json", data_files=dataset_path, split="train")

        alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

        def formatting_prompts_func(examples):
            instructions = examples["instruction"]
            inputs       = examples["input"]
            outputs      = examples["output"]
            texts = []
            for instruction, input, output in zip(instructions, inputs, outputs):
                text = alpaca_prompt.format(instruction, input, output) + tokenizer.eos_token
                texts.append(text)
            return { "text" : texts, }

        training_args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            max_steps = 60, 
            learning_rate = 2e-4,
            fp16 = not torch.cuda.is_bf16_supported(),
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = "outputs",
        )

        trainer = SFTTrainer(
            model = model,
            tokenizer = tokenizer,
            train_dataset = dataset,
            dataset_text_field = "text",
            max_seq_length = max_seq_length,
            dataset_num_proc = 2,
            packing = False, 
            formatting_func = formatting_prompts_func,
            args = training_args,
        )

        logger.info("Starting training loop...")
        trainer_stats = trainer.train()
        logger.info("Training complete.")
        
        # Save model
        os.makedirs(output_dir, exist_ok=True)
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        logger.info(f"Model saved to {output_dir}")
        return {"status": "success", "message": "Training completed successfully."}
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    train()
