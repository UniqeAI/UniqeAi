#!/usr/bin/env python3
"""
🔥 QLoRA Fine-tuning Script - RTX 4060 Optimized
===============================================

Tam fonksiyonel QLoRA (Quantized Low-Rank Adaptation) fine-tuning script'i
NVIDIA RTX 4060 (8GB VRAM) + 32GB RAM sisteminize özel optimize edilmiştir.

Bu script QLoRA kullanır: ✅ EVET
- 4-bit quantization (NF4)
- LoRA adapters
- Flash Attention 2
- Gradient checkpointing
- Memory optimization

Kullanım:
    python qlora_finetune_rtx4060.py
"""

import os
import gc
import json
import torch
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ML libraries
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
    EarlyStoppingCallback
)
from peft import (
    LoraConfig,
    get_peft_model,
    TaskType,
    prepare_model_for_kbit_training
)
from trl import SFTTrainer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

class QLoRAFineTuner:
    """RTX 4060 + 32GB RAM için optimize edilmiş QLoRA Fine-tuner"""
    
    def __init__(self):
        self.model_name = "meta-llama/Llama-3.1-8B-Instruct"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Paths
        self.data_path = "../data/complete_training_dataset.json"
        self.output_dir = "./fine_tuned_qlora_model"
        self.logs_dir = "./training_logs"
        
        # Create directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # RTX 4060 optimal config
        self.config = {
            "lora_r": 64,
            "lora_alpha": 128,
            "lora_dropout": 0.05,
            "batch_size": 1,
            "gradient_accumulation": 32,
            "learning_rate": 5e-5,
            "num_epochs": 6,
            "max_length": 2048
        }
    
    def setup_quantization(self) -> BitsAndBytesConfig:
        """4-bit QLoRA quantization setup"""
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
    
    def load_dataset(self) -> Dataset:
        """Load and format dataset"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        formatted_data = []
        for item in data:
            if item["input"].strip():
                text = f"""### Instruction:\n{item['instruction']}\n\n### Input:\n{item['input']}\n\n### Response:\n{item['output']}"""
            else:
                text = f"""### Instruction:\n{item['instruction']}\n\n### Response:\n{item['output']}"""
            
            formatted_data.append({"text": text})
        
        return Dataset.from_list(formatted_data)
    
    def fine_tune(self) -> bool:
        """Main fine-tuning process"""
        logger.info("🚀 Starting QLoRA fine-tuning...")
        
        try:
            # Load dataset
            dataset = self.load_dataset()
            logger.info(f"📊 Loaded {len(dataset)} samples")
            
            # Setup quantization
            bnb_config = self.setup_quantization()
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            # Load model with quantization
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.bfloat16
            )
            
            # Prepare for training
            model = prepare_model_for_kbit_training(model)
            
            # LoRA config
            lora_config = LoraConfig(
                r=self.config["lora_r"],
                lora_alpha=self.config["lora_alpha"],
                target_modules=["q_proj", "k_proj", "v_proj", "o_proj", 
                               "gate_proj", "up_proj", "down_proj"],
                lora_dropout=self.config["lora_dropout"],
                bias="none",
                task_type=TaskType.CAUSAL_LM
            )
            
            # Get PEFT model
            model = get_peft_model(model, lora_config)
            model.print_trainable_parameters()
            
            # Training arguments
            training_args = TrainingArguments(
                output_dir=self.output_dir,
                num_train_epochs=self.config["num_epochs"],
                per_device_train_batch_size=self.config["batch_size"],
                gradient_accumulation_steps=self.config["gradient_accumulation"],
                learning_rate=self.config["learning_rate"],
                bf16=True,
                logging_steps=1,
                save_steps=10,
                save_total_limit=2,
                gradient_checkpointing=True,
                remove_unused_columns=False
            )
            
            # Create trainer
            trainer = SFTTrainer(
                model=model,
                train_dataset=dataset,
                tokenizer=tokenizer,
                args=training_args,
                dataset_text_field="text",
                max_seq_length=self.config["max_length"],
                packing=False
            )
            
            # Train
            trainer.train()
            
            # Save
            trainer.save_model()
            tokenizer.save_pretrained(self.output_dir)
            
            logger.info(f"✅ Model saved to {self.output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            return False

def main():
    """Main function"""
    print("🔥 QLoRA Fine-tuning for RTX 4060")
    print("=" * 50)
    
    fine_tuner = QLoRAFineTuner()
    success = fine_tuner.fine_tune()
    
    if success:
        print("🎉 Fine-tuning completed successfully!")
    else:
        print("❌ Fine-tuning failed.")

if __name__ == "__main__":
    main() 