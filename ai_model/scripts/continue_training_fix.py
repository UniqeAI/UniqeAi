#!/usr/bin/env python3
"""
🔄 Continue Training Fix - Mevcut model üzerinden API doğruluğunu artırır
========================================================================

Model tool format'ını korumuş (100%) ama API'leri yanlış öğrenmiş.
Bu script mevcut model'i alıp sadece API doğruluğunu artırır.
"""

import os
import gc
import json
import torch
import logging
from datetime import datetime
from typing import Dict, Tuple

from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import PeftModel, get_peft_model, LoraConfig, TaskType

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

class ContinueTrainingFixer:
    def __init__(self):
        self.base_model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        self.fine_tuned_model_path = "./qlora_fine_tuned_model"
        self.output_dir = "./qlora_fixed_model"
        self.original_data_path = "../data/telekom_training_dataset_enhanced.json"
        
        # Continue training config - ÇOKTA CRITICAL!
        self.config = {
            "learning_rate": 1e-5,  # Çok düşük - mevcut format'ı bozmamak için
            "num_epochs": 2,        # Az epoch - overfitting önlemek için  
            "batch_size": 1,
            "gradient_accumulation": 16,  # Daha küçük - stable training
            "warmup_ratio": 0.1,    # Warm start
            "weight_decay": 0.01,   # Regularization
        }
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def setup_quantization(self) -> BitsAndBytesConfig:
        """4-bit quantization config"""
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
    
    def create_api_focused_dataset(self) -> Dataset:
        """Create dataset focused on correct APIs"""
        logger.info("📊 API-focused dataset oluşturuluyor...")
        
        # Load original data
        with open(self.original_data_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # API mapping for corrections
        api_corrections = {
            # Yanlış öğrendiği API'ler -> Doğru API'ler
            "get_faturation": "get_current_bill",
            "create_ariza": "create_fault_ticket", 
            "roaming_open": "enable_roaming",
            "profil_bilgiler": "get_customer_profile",
            "dondur_hattim": "suspend_line",
            "aktive_hatt": "reactivate_line",
            "change_phone_number": "update_customer_contact"
        }
        
        # Filter and enhance data
        api_focused_data = []
        
        # 1. Add original correct examples (full dataset)
        api_focused_data.extend(original_data)
        
        # 2. Add API correction examples
        for wrong_api, correct_api in api_corrections.items():
            # Create focused examples for each wrong->correct mapping
            api_focused_data.extend([
                {
                    "instruction": self.get_instruction_for_api(correct_api),
                    "input": self.get_sample_input_for_api(correct_api),
                    "output": f"<tool_code>print(backend_api.{correct_api}(user_id=1001))</tool_code>"
                } for _ in range(3)  # 3 copies per correction
            ])
        
        logger.info(f"📈 API-focused dataset: {len(api_focused_data)} örnekler")
        return Dataset.from_list(api_focused_data)
    
    def get_instruction_for_api(self, api_name: str) -> str:
        """Get instruction for API"""
        mapping = {
            "get_current_bill": "Get Current Bill",
            "create_fault_ticket": "Create Fault Ticket",
            "enable_roaming": "Enable Roaming", 
            "get_customer_profile": "Get Customer Profile",
            "suspend_line": "Suspend Line",
            "reactivate_line": "Reactivate Line",
            "update_customer_contact": "Update Customer Contact"
        }
        return mapping.get(api_name, "Unknown")
    
    def get_sample_input_for_api(self, api_name: str) -> str:
        """Get sample input for API"""
        mapping = {
            "get_current_bill": "Faturamı görmek istiyorum",
            "create_fault_ticket": "Arıza kaydı oluşturmak istiyorum",
            "enable_roaming": "Roaming açmak istiyorum",
            "get_customer_profile": "Profil bilgilerimi görmek istiyorum", 
            "suspend_line": "Hattımı dondurmak istiyorum",
            "reactivate_line": "Hattımı aktive etmek istiyorum",
            "update_customer_contact": "Telefon numaramı değiştirmek istiyorum"
        }
        return mapping.get(api_name, "Unknown request")
    
    def tokenize_function(self, examples, tokenizer):
        """Tokenize with format preservation"""
        # Format exactly like original training
        formatted_texts = []
        for item in examples:
            if 'text' in item:
                text = item['text']
            else:
                # Reconstruct from components
                if item.get("input", "").strip():
                    text = f"### Instruction:\n{item['instruction']}\n\n### Input:\n{item['input']}\n\n### Response:\n{item['output']}<|endoftext|>"
                else:
                    text = f"### Instruction:\n{item['instruction']}\n\n### Response:\n{item['output']}<|endoftext|>"
            formatted_texts.append(text)
        
        # Tokenize
        tokenized = tokenizer(
            formatted_texts,
            truncation=True,
            padding=False,
            max_length=2048,
            return_tensors=None
        )
        
        # Labels = input_ids for causal LM
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized
    
    def load_continue_model_and_tokenizer(self) -> Tuple[PeftModel, AutoTokenizer]:
        """Load existing fine-tuned model for continue training"""
        logger.info("🔄 Mevcut fine-tuned model yükleniyor...")
        
        # Quantization config
        bnb_config = self.setup_quantization()
        
        # Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.base_model_name,
            trust_remote_code=True
        )
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        
        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
        
        # Load existing fine-tuned model  
        model = PeftModel.from_pretrained(
            base_model,
            self.fine_tuned_model_path,
            device_map="auto"
        )
        
        # Make trainable again
        model.train()
        
        logger.info("✅ Mevcut model continue training için hazır")
        return model, tokenizer
    
    def continue_training(self) -> bool:
        """Continue training on API-focused dataset"""
        try:
            logger.info("🔄 Continue training başlatılıyor...")
            
            # Load model and tokenizer
            model, tokenizer = self.load_continue_model_and_tokenizer()
            
            # Create API-focused dataset
            dataset = self.create_api_focused_dataset()
            
            # Tokenize dataset
            logger.info("🔤 Dataset tokenize ediliyor...")
            tokenized_dataset = dataset.map(
                lambda x: self.tokenize_function(x, tokenizer),
                batched=True,
                remove_columns=dataset.column_names
            )
            
            # Data collator
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=tokenizer,
                mlm=False,
                pad_to_multiple_of=8
            )
            
            # Training arguments - VERY CONSERVATIVE
            training_args = TrainingArguments(
                output_dir=self.output_dir,
                num_train_epochs=self.config["num_epochs"],
                per_device_train_batch_size=self.config["batch_size"],
                gradient_accumulation_steps=self.config["gradient_accumulation"],
                learning_rate=self.config["learning_rate"],
                warmup_ratio=self.config["warmup_ratio"],
                weight_decay=self.config["weight_decay"],
                bf16=True,
                gradient_checkpointing=True,
                logging_steps=5,
                save_steps=100,
                save_total_limit=3,
                remove_unused_columns=False,
                dataloader_drop_last=True,
                dataloader_pin_memory=False,
                report_to=None  # No wandb
            )
            
            # Trainer
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=tokenized_dataset,
                data_collator=data_collator,
                tokenizer=tokenizer
            )
            
            logger.info("🔥 Continue training başlatıldı...")
            logger.info(f"📊 Config: LR={self.config['learning_rate']}, Epochs={self.config['num_epochs']}")
            
            trainer.train()
            
            # Save
            trainer.save_model()
            tokenizer.save_pretrained(self.output_dir)
            
            logger.info(f"✅ Continue training tamamlandı: {self.output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Continue training hatası: {e}")
            return False
        finally:
            # Cleanup
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()

def main():
    """Main function"""
    print("🔄 Continue Training Fix - API Doğruluğunu Artırır")
    print("=" * 60)
    print("✅ Model tool format'ını korur (100%)")
    print("🎯 API doğruluğunu artırır (11.1% -> 80%+)")
    print("⚡ 1-2 saat sürer (5 saat değil)")
    print("=" * 60)
    
    fixer = ContinueTrainingFixer()
    success = fixer.continue_training()
    
    if success:
        print("🎉 Continue training tamamlandı!")
        print("🧪 Test için: python model_analysis.py")
    else:
        print("❌ Continue training başarısız.")

if __name__ == "__main__":
    main() 