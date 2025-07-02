"""
Llama-3.1-8B-Instruct Fine-tuning Script
========================================

Bu script, Türkçe çağrı merkezi senaryoları için Llama-3.1-8B-Instruct modelini
LoRA (Low-Rank Adaptation) kullanarak fine-tune eder.

Kullanım:
    python run_finetune.py

Gereksinimler:
    - CUDA destekli GPU (8GB+ VRAM önerilir)
    - complete_training_dataset.json dosyası
    - requirements.txt'teki tüm paketler
"""

import os
import json
import torch
import logging
from datetime import datetime
from typing import Dict, List, Optional

from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
    EarlyStoppingCallback
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from trl import SFTTrainer

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FineTuner:
    def __init__(self, model_name: str = "meta-llama/Llama-3.1-8B-Instruct"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        
        # Dosya yolları
        self.data_path = "../data/complete_training_dataset.json"
        self.output_dir = "./fine_tuned_model"
        self.logs_dir = "./training_logs"
        
        # Dizinleri oluştur
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
    def setup_logging(self):
        """Training loglarını ayarla"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.logs_dir, f"training_{timestamp}.log")
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"Training başlatıldı: {timestamp}")
        logger.info(f"Model: {self.model_name}")
        logger.info(f"Device: {self.device}")
        
    def check_gpu_memory(self):
        """GPU bellek durumunu kontrol et"""
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
            logger.info(f"GPU Bellek: {gpu_memory:.1f} GB")
            
            if gpu_memory < 8:
                logger.warning("⚠️ 8GB'den az GPU belleği detected. 4-bit quantization kullanılacak.")
                return True  # Quantization gerekli
            return False  # Quantization opsiyonel
        else:
            logger.warning("⚠️ CUDA bulunamadı. CPU kullanılacak (çok yavaş olacak).")
            return False

    def load_and_prepare_dataset(self) -> Dataset:
        """Veri setini yükle ve SFTTrainer formatına dönüştür"""
        logger.info("Veri seti yükleniyor...")
        
        # JSON dosyasını yükle
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Veri dosyası bulunamadı: {self.data_path}")
            
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Toplam {len(data)} veri noktası yüklendi")
        
        # Instruction tuning formatını tek metin alanına dönüştür
        formatted_data = []
        for item in data:
            # Alpaca formatı: Instruction, Input, Output'u birleştir
            if item["input"].strip():
                text = f"### Instruction:\n{item['instruction']}\n\n### Input:\n{item['input']}\n\n### Response:\n{item['output']}"
            else:
                text = f"### Instruction:\n{item['instruction']}\n\n### Response:\n{item['output']}"
                
            formatted_data.append({"text": text})
        
        # Dataset oluştur
        dataset = Dataset.from_list(formatted_data)
        
        # Örnek veriyi göster
        logger.info("Örnek veri noktası:")
        logger.info(f"Text: {formatted_data[0]['text'][:200]}...")
        
        return dataset

    def load_model_and_tokenizer(self, use_quantization: bool = True):
        """Model ve tokenizer'ı yükle"""
        logger.info("Model ve tokenizer yükleniyor...")
        
        # Quantization konfigürasyonu
        bnb_config = None
        if use_quantization and self.device == "cuda":
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            logger.info("4-bit quantization aktif")

        # Tokenizer yükle
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            padding_side="right"
        )
        
        # Llama modellerinde pad token eksik
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            
        logger.info("Tokenizer yüklendi")

        # Model yükle
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32,
            attn_implementation="flash_attention_2" if self.device == "cuda" else None
        )
        
        logger.info("Model yüklendi")
        
        # Quantized model için ek hazırlık
        if use_quantization and self.device == "cuda":
            self.model = prepare_model_for_kbit_training(self.model)
            logger.info("Model quantization için hazırlandı")

    def setup_lora_config(self) -> LoraConfig:
        """LoRA konfigürasyonunu ayarla"""
        logger.info("LoRA konfigürasyonu ayarlanıyor...")
        
        lora_config = LoraConfig(
            r=16,  # Rank - daha yüksek = daha fazla parameter
            lora_alpha=32,  # Alpha - learning rate scaling
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj"
            ],
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.CAUSAL_LM,
        )
        
        logger.info(f"LoRA rank: {lora_config.r}")
        logger.info(f"LoRA alpha: {lora_config.lora_alpha}")
        
        return lora_config

    def setup_training_arguments(self, dataset_size: int) -> TrainingArguments:
        """Eğitim argümanlarını ayarla"""
        logger.info("Eğitim parametreleri ayarlanıyor...")
        
        # Veri boyutuna göre epoch sayısını ayarla
        if dataset_size < 50:
            num_epochs = 3
        elif dataset_size < 100:
            num_epochs = 2
        else:
            num_epochs = 1
            
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=8,  # Effective batch size = 8
            learning_rate=1e-4,
            warmup_steps=5,
            logging_steps=1,
            save_steps=max(5, dataset_size // 10),  # Her %10'da bir kaydet
            eval_steps=max(5, dataset_size // 10),
            save_total_limit=2,
            remove_unused_columns=False,
            dataloader_pin_memory=False,
            bf16=True if self.device == "cuda" else False,
            fp16=False,
            gradient_checkpointing=True,
            optim="adamw_bnb_8bit" if self.device == "cuda" else "adamw_hf",
            lr_scheduler_type="cosine",
            report_to="none",  # Wandb vs. kullanmıyoruz
            run_name=f"llama-finetune-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        logger.info(f"Epoch sayısı: {num_epochs}")
        logger.info(f"Batch size: {training_args.per_device_train_batch_size}")
        logger.info(f"Gradient accumulation: {training_args.gradient_accumulation_steps}")
        logger.info(f"Learning rate: {training_args.learning_rate}")
        
        return training_args

    def fine_tune(self):
        """Ana fine-tuning süreci"""
        try:
            # Kurulum
            self.setup_logging()
            use_quantization = self.check_gpu_memory()
            
            # Veri setini hazırla
            dataset = self.load_and_prepare_dataset()
            
            # Model ve tokenizer'ı yükle
            self.load_model_and_tokenizer(use_quantization)
            
            # LoRA konfigürasyonu
            lora_config = self.setup_lora_config()
            
            # Eğitim argümanları
            training_args = self.setup_training_arguments(len(dataset))
            
            # LoRA modelini hazırla
            self.model = get_peft_model(self.model, lora_config)
            self.model.print_trainable_parameters()
            
            logger.info("SFTTrainer oluşturuluyor...")
            
            # Trainer oluştur
            trainer = SFTTrainer(
                model=self.model,
                train_dataset=dataset,
                tokenizer=self.tokenizer,
                args=training_args,
                dataset_text_field="text",
                max_seq_length=1024,
                packing=False,  # Veri seti küçük olduğu için packing kullanma
                callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
            )
            
            logger.info("🚀 Eğitim başlatılıyor...")
            
            # Eğitimi başlat
            trainer.train()
            
            logger.info("✅ Eğitim tamamlandı!")
            
            # Modeli kaydet
            logger.info("Model kaydediliyor...")
            trainer.save_model()
            self.tokenizer.save_pretrained(self.output_dir)
            
            # Eğitim loglarını kaydet
            with open(os.path.join(self.output_dir, "training_log.json"), "w") as f:
                json.dump(trainer.state.log_history, f, indent=2)
            
            logger.info(f"Model kaydedildi: {self.output_dir}")
            
            # GPU bellek temizliği
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            return True
            
        except Exception as e:
            logger.error(f"Eğitim sırasında hata: {str(e)}")
            return False

    def test_model(self, test_prompts: Optional[List[str]] = None):
        """Eğitilmiş modeli test et"""
        if test_prompts is None:
            test_prompts = [
                "### Instruction:\nKullanıcı bilgilerini getir\n\n### Input:\nID'si 12345 olan kullanıcının bilgilerini al\n\n### Response:",
                "### Instruction:\nFatura detayını getir\n\n### Input:\nMüşteri 5551234567 numaralı hattının Ocak 2024 fatura detayını göster\n\n### Response:"
            ]
        
        logger.info("Model test ediliyor...")
        
        for i, prompt in enumerate(test_prompts):
            logger.info(f"\n--- Test {i+1} ---")
            logger.info(f"Prompt: {prompt[:100]}...")
            
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=100,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.info(f"Response: {response[len(prompt):]}")

def main():
    """Ana fonksiyon"""
    print("🔥 Llama-3.1-8B-Instruct Fine-tuning Başlatılıyor...")
    print("=" * 60)
    
    # Fine-tuner oluştur
    fine_tuner = FineTuner()
    
    # Fine-tuning işlemini başlat
    success = fine_tuner.fine_tune()
    
    if success:
        print("\n🎉 Fine-tuning başarıyla tamamlandı!")
        print(f"📁 Model lokasyonu: {fine_tuner.output_dir}")
        
        # Modeli test et (opsiyonel)
        response = input("\nModeli test etmek istiyor musunuz? (y/n): ")
        if response.lower() == 'y':
            fine_tuner.test_model()
    else:
        print("\n❌ Fine-tuning başarısız oldu. Logları kontrol edin.")

if __name__ == "__main__":
    main() 