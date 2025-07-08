#!/usr/bin/env python3
"""
🚀 HIZLI QLoRA Fine-tuning - RTX 4060 Optimize
==============================================

Bu script QLoRA eğitimini 30-45 dakikaya düşürür.

Ana Optimizasyonlar:
- Daha büyük batch size
- Daha az epoch 
- Daha küçük dataset sample
- Aggressive gradient accumulation
"""

import os
import gc
import json
import torch
import logging
from datetime import datetime
from typing import Dict, Tuple

# ML libraries
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig,
    get_peft_model,
    TaskType,
    prepare_model_for_kbit_training
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

def setup_huggingface_token():
    """Setup Hugging Face token from environment variable."""
    token = os.getenv('HUGGINGFACE_HUB_TOKEN')
    if token:
        logger.info("✅ Hugging Face token found in environment")
        os.environ['HF_TOKEN'] = token
        return True
    else:
        logger.warning("⚠️ HUGGINGFACE_HUB_TOKEN not found. Trying to use global login.")
        return False

class HizliQLoRAFineTuner:
    def __init__(self):
        setup_huggingface_token()
        self.model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        self.data_path = "../data/telekom_training_dataset_enhanced.json"
        self.output_dir = "./hizli_qlora_model"
        
        # 🚀 HIZLI RTX 4060 CONFIG
        self.config = {
            "lora_r": 32,  # Daha küçük rank - hızlı
            "lora_alpha": 64,  # Orantılı alpha
            "batch_size": 2,  # Batch size artırıldı
            "gradient_accumulation": 8,  # Azaltıldı (effective batch = 16)
            "learning_rate": 1e-4,  # Biraz daha yüksek
            "num_epochs": 1,  # Sadece 1 epoch!
            "max_samples": 500,  # Dataset'i 500 sample'a kısıt
            "max_seq_length": 1024  # Sequence length kısaltıldı
        }
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def setup_quantization(self) -> BitsAndBytesConfig:
        """4-bit QLoRA quantization"""
        logger.info("🔢 Setting up 4-bit QLoRA quantization...")
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
    
    def load_dataset(self) -> Dataset:
        """Load and format dataset - LIMITED TO 500 SAMPLES"""
        logger.info("📊 Loading dataset...")
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 🚀 SADECE İLK 500 SAMPLE AL
        data = data[:self.config["max_samples"]]
        
        formatted_data = []
        for item in data:
            if item["input"].strip():
                text = f"### Instruction:\n{item['instruction']}\n\n### Input:\n{item['input']}\n\n### Response:\n{item['output']}<|endoftext|>"
            else:
                text = f"### Instruction:\n{item['instruction']}\n\n### Response:\n{item['output']}<|endoftext|>"
            formatted_data.append({"text": text})
        
        logger.info(f"📈 Loaded {len(formatted_data)} samples (limited for speed)")
        return Dataset.from_list(formatted_data)
    
    def tokenize_function(self, examples, tokenizer):
        """Tokenize examples with proper padding and truncation"""
        # Tokenize texts
        tokenized = tokenizer(
            examples["text"],
            truncation=True,
            padding=False,  # Will be done by data collator
            max_length=self.config["max_seq_length"],  # Kısaltılmış
            return_tensors=None
        )
        
        # Labels are the same as input_ids for causal LM
        tokenized["labels"] = tokenized["input_ids"].copy()
        
        return tokenized
    
    def load_model_and_tokenizer(self) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
        """Load model with quantization and tokenizer"""
        logger.info(f"🤖 Loading {self.model_name}...")
        
        # Quantization config
        bnb_config = self.setup_quantization()
        
        # Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Set padding side to right for training
        tokenizer.padding_side = "right"
        
        # Model with 4-bit quantization
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
        
        logger.info("✅ Model and tokenizer loaded successfully")
        return model, tokenizer
    
    def setup_qlora(self, model) -> AutoModelForCausalLM:
        """Setup QLoRA adapters - SMALLER CONFIG"""
        logger.info("🎯 Setting up QLoRA adapters...")
        
        # Prepare for training
        model = prepare_model_for_kbit_training(model)
        
        # LoRA config - SMALLER FOR SPEED
        lora_config = LoraConfig(
            r=self.config["lora_r"],  # 32 instead of 64
            lora_alpha=self.config["lora_alpha"],  # 64 instead of 128
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Fewer targets
            lora_dropout=0.05,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        # Apply LoRA
        model = get_peft_model(model, lora_config)
        
        # Print trainable parameters
        trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total = sum(p.numel() for p in model.parameters())
        logger.info(f"🎯 Trainable: {trainable:,} / {total:,} ({100*trainable/total:.2f}%)")
        
        return model
    
    def fine_tune(self) -> bool:
        """Main fine-tuning process - FAST VERSION"""
        try:
            logger.info("🚀 Starting FAST QLoRA fine-tuning...")
            
            # Load dataset
            dataset = self.load_dataset()
            
            # Load model and tokenizer
            model, tokenizer = self.load_model_and_tokenizer()
            
            # Setup QLoRA
            model = self.setup_qlora(model)
            
            # Tokenize dataset
            logger.info("🔤 Tokenizing dataset...")
            tokenized_dataset = dataset.map(
                lambda x: self.tokenize_function(x, tokenizer),
                batched=True,
                remove_columns=dataset.column_names
            )
            
            # Data collator for padding
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=tokenizer,
                mlm=False,  # Causal LM, not masked LM
                pad_to_multiple_of=8
            )
            
            # 🚀 FAST Training arguments
            training_args = TrainingArguments(
                output_dir=self.output_dir,
                num_train_epochs=self.config["num_epochs"],  # Sadece 1 epoch!
                per_device_train_batch_size=self.config["batch_size"],  # 2 instead of 1
                gradient_accumulation_steps=self.config["gradient_accumulation"],  # 8 instead of 32
                learning_rate=self.config["learning_rate"],
                bf16=True,
                gradient_checkpointing=True,
                logging_steps=5,  # Daha az log
                save_steps=25,  # Daha az save
                save_total_limit=1,  # Sadece 1 checkpoint
                remove_unused_columns=False,
                dataloader_drop_last=True,
                dataloader_pin_memory=False,
                warmup_steps=10,  # Hızlı warmup
                max_grad_norm=1.0
            )
            
            # Create trainer with manual tokenization
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=tokenized_dataset,
                data_collator=data_collator,
                tokenizer=tokenizer
            )
            
            # Train
            logger.info("🔥 Training started...")
            start_time = datetime.now()
            trainer.train()
            end_time = datetime.now()
            
            duration = end_time - start_time
            logger.info(f"⏱️ Training completed in: {duration}")
            
            # Save
            trainer.save_model()
            tokenizer.save_pretrained(self.output_dir)
            
            logger.info(f"✅ Model saved to {self.output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            return False
        finally:
            # Cleanup
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()

def main():
    """Main function"""
    print("🚀 HIZLI QLoRA Fine-tuning for RTX 4060")
    print("=" * 50)
    print("⚡ Speed Optimizations:")
    print("   - 500 samples only")
    print("   - 1 epoch training")
    print("   - Larger batch size")
    print("   - Smaller LoRA rank")
    print("   - Shorter sequences")
    print("=" * 50)
    
    fine_tuner = HizliQLoRAFineTuner()
    success = fine_tuner.fine_tune()
    
    if success:
        print("🎉 HIZLI QLoRA fine-tuning completed!")
    else:
        print("❌ Fine-tuning failed.")

if __name__ == "__main__":
    main() 