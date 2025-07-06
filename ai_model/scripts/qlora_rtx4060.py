#!/usr/bin/env python3
"""
🔥 QLoRA Fine-tuning Script - RTX 4060 Optimized
===============================================

Bu script QLoRA (Quantized Low-Rank Adaptation) kullanarak
Llama-3.1-8B-Instruct modelini RTX 4060 + 32GB RAM sisteminiz için
optimize edilmiş şekilde fine-tune eder.

QLoRA Features:
✅ 4-bit quantization (8x memory reduction)
✅ LoRA adapters (parameter efficient)
✅ Flash Attention 2 (RTX 4060 optimized)
✅ Gradient checkpointing (memory efficient)
✅ Optimized for your exact hardware

Kullanım:
    python qlora_rtx4060.py

Author: AI Assistant
Date: 2024
"""

import os
import gc
import sys
import json
import time
import torch
import psutil
import logging
import warnings
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# ML imports
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
    EarlyStoppingCallback,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig,
    get_peft_model,
    TaskType,
    prepare_model_for_kbit_training,
    PeftModel
)
from trl import SFTTrainer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("QLoRA-RTX4060")

class RTX4060QLoRAFineTuner:
    """
    RTX 4060 (8GB VRAM) + 32GB RAM için optimize edilmiş QLoRA Fine-tuner
    
    Bu sınıf özel olarak sizin sisteminiz için optimize edilmiştir:
    - AMD Ryzen 9 CPU (multi-core optimization)
    - NVIDIA RTX 4060 GPU (8GB VRAM optimal usage)
    - 32GB System RAM (efficient data loading)
    """
    
    def __init__(self, model_name: str = "meta-llama/Llama-3.1-8B-Instruct"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize model components
        self.model = None
        self.tokenizer = None
        self.peft_model = None
        
        # File paths
        self.data_path = "../data/complete_training_dataset.json"
        self.output_dir = "./fine_tuned_qlora_model"
        self.logs_dir = "./training_logs"
        
        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # RTX 4060 optimized configuration
        self.config = {
            # Model settings
            "max_seq_length": 2048,         # Full context length
            "quantization_bits": 4,          # 4-bit quantization
            
            # QLoRA settings (optimized for quality)
            "lora_r": 64,                   # High rank for quality
            "lora_alpha": 128,              # 2x rank (optimal scaling)
            "lora_dropout": 0.05,           # Low dropout for small dataset
            
            # Training settings (RTX 4060 optimized)
            "batch_size": 1,                # Safe for 8GB VRAM
            "gradient_accumulation": 32,     # Effective batch size = 32
            "learning_rate": 5e-5,          # Conservative for stability
            "num_epochs": 6,                # More epochs for 47 samples
            "warmup_ratio": 0.1,            # 10% warmup
            "weight_decay": 0.01,           # L2 regularization
            "max_grad_norm": 1.0,           # Gradient clipping
            
            # Memory optimization
            "gradient_checkpointing": True,  # Trade compute for memory
            "dataloader_num_workers": 4,     # Ryzen 9 parallelization
            "pin_memory": False,             # Prevent VRAM conflicts
            
            # Precision (RTX 4060 optimized)
            "bf16": True,                   # Native bfloat16 support
            "tf32": True,                   # TensorFloat-32 speedup
            "fp16": False,                  # Don't mix with bf16
        }
        
        logger.info("🔥 RTX 4060 QLoRA Fine-tuner initialized")
        logger.info(f"🤖 Model: {self.model_name}")
        logger.info(f"💾 Output: {self.output_dir}")
    
    def check_system_requirements(self) -> bool:
        """Comprehensive system requirements check"""
        logger.info("🔍 Checking system requirements...")
        
        requirements_met = True
        
        # Check CUDA
        if not torch.cuda.is_available():
            logger.error("❌ CUDA not available - GPU required for QLoRA")
            return False
        
        # Check GPU memory
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        gpu_name = torch.cuda.get_device_name(0)
        logger.info(f"🎮 GPU: {gpu_name} ({gpu_memory:.1f} GB)")
        
        if gpu_memory < 6.0:
            logger.error(f"❌ Insufficient VRAM: {gpu_memory:.1f}GB (minimum 6GB for QLoRA)")
            requirements_met = False
        else:
            logger.info("✅ GPU memory sufficient for QLoRA")
        
        # Check system RAM
        ram_total = psutil.virtual_memory().total / 1e9
        ram_available = psutil.virtual_memory().available / 1e9
        logger.info(f"🧠 RAM: {ram_available:.1f}/{ram_total:.1f} GB available")
        
        if ram_total < 16.0:
            logger.error(f"❌ Insufficient RAM: {ram_total:.1f}GB (minimum 16GB)")
            requirements_met = False
        else:
            logger.info("✅ System RAM sufficient")
        
        # Check training data
        if not os.path.exists(self.data_path):
            logger.error(f"❌ Training data not found: {self.data_path}")
            requirements_met = False
        else:
            logger.info(f"✅ Training data found: {self.data_path}")
        
        # Check PyTorch version
        torch_version = torch.__version__
        logger.info(f"🔥 PyTorch version: {torch_version}")
        
        if requirements_met:
            logger.info("✅ All system requirements met!")
        
        return requirements_met
    
    def optimize_pytorch_settings(self):
        """Optimize PyTorch for RTX 4060 + Ryzen 9"""
        logger.info("⚙️ Optimizing PyTorch settings...")
        
        # Enable TF32 for RTX 4060 (faster matrix operations)
        torch.backends.cuda.matmul.allow_tf32 = self.config["tf32"]
        torch.backends.cudnn.allow_tf32 = self.config["tf32"]
        torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction = True
        
        # Optimize for Ryzen 9 (multi-core CPU)
        cpu_cores = psutil.cpu_count(logical=False)
        optimal_threads = min(cpu_cores, 12)  # Cap for stability
        torch.set_num_threads(optimal_threads)
        
        # Memory management
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            # Reserve some VRAM for system
            torch.cuda.set_per_process_memory_fraction(0.95)
        
        logger.info(f"🧵 CPU threads: {torch.get_num_threads()}")
        logger.info(f"🔢 TF32 enabled: {self.config['tf32']}")
        logger.info(f"🗂️ BF16 enabled: {self.config['bf16']}")
        logger.info("✅ PyTorch optimization complete")
    
    def get_memory_info(self) -> Dict[str, float]:
        """Get current memory usage info"""
        info = {}
        
        # GPU memory
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated(0) / 1e9
            reserved = torch.cuda.memory_reserved(0) / 1e9
            total = torch.cuda.get_device_properties(0).total_memory / 1e9
            
            info.update({
                "gpu_total": total,
                "gpu_allocated": allocated,
                "gpu_reserved": reserved,
                "gpu_free": total - reserved
            })
        
        # System memory
        mem = psutil.virtual_memory()
        info.update({
            "ram_total": mem.total / 1e9,
            "ram_used": mem.used / 1e9,
            "ram_available": mem.available / 1e9
        })
        
        return info
    
    def log_memory_status(self, context: str = ""):
        """Log current memory status"""
        mem_info = self.get_memory_info()
        
        if context:
            logger.info(f"📊 Memory Status - {context}")
        else:
            logger.info("📊 Memory Status")
        
        if "gpu_total" in mem_info:
            logger.info(f"   GPU: {mem_info['gpu_allocated']:.1f}/{mem_info['gpu_total']:.1f} GB")
            logger.info(f"   VRAM Free: {mem_info['gpu_free']:.1f} GB")
        
        logger.info(f"   RAM: {mem_info['ram_used']:.1f}/{mem_info['ram_total']:.1f} GB")
    
    def setup_quantization_config(self) -> BitsAndBytesConfig:
        """Setup 4-bit quantization configuration for QLoRA"""
        logger.info("🔢 Setting up 4-bit quantization...")
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,                      # Enable 4-bit loading
            bnb_4bit_use_double_quant=True,         # Double quantization (extra compression)
            bnb_4bit_quant_type="nf4",              # NormalFloat4 (best quality)
            bnb_4bit_compute_dtype=torch.bfloat16,  # Computation in bfloat16
            bnb_4bit_quant_storage=torch.uint8,     # Storage in uint8
        )
        
        logger.info("✅ 4-bit quantization configuration:")
        logger.info(f"   💾 Quantization type: NF4 (best quality)")
        logger.info(f"   🔄 Double quantization: True (extra compression)")
        logger.info(f"   🧮 Compute dtype: bfloat16 (RTX 4060 native)")
        logger.info(f"   📦 Storage dtype: uint8")
        
        return bnb_config
    
    def load_and_prepare_dataset(self) -> Dataset:
        """Load and prepare training dataset"""
        logger.info("📊 Loading and preparing dataset...")
        
        # Load raw data
        with open(self.data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        logger.info(f"📈 Loaded {len(raw_data)} raw training samples")
        
        # Format data for instruction tuning
        formatted_samples = []
        for i, sample in enumerate(raw_data):
            # Create Alpaca-style format
            if sample["input"].strip():
                text = f"""### Instruction:
{sample['instruction']}

### Input:
{sample['input']}

### Response:
{sample['output']}"""
            else:
                text = f"""### Instruction:
{sample['instruction']}

### Response:
{sample['output']}"""
            
            formatted_samples.append({
                "text": text,
                "id": i,
                "length": len(text)
            })
        
        # Create HuggingFace Dataset
        dataset = Dataset.from_list(formatted_samples)
        
        # Log dataset statistics
        lengths = [s["length"] for s in formatted_samples]
        avg_length = sum(lengths) / len(lengths)
        max_length = max(lengths)
        
        logger.info(f"📊 Dataset statistics:")
        logger.info(f"   Total samples: {len(dataset)}")
        logger.info(f"   Average length: {avg_length:.0f} characters")
        logger.info(f"   Maximum length: {max_length} characters")
        logger.info(f"   Sample preview: {formatted_samples[0]['text'][:150]}...")
        
        return dataset
    
    def load_model_and_tokenizer(self) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
        """Load model with quantization and tokenizer"""
        logger.info(f"🤖 Loading model: {self.model_name}")
        
        # Setup quantization
        bnb_config = self.setup_quantization_config()
        
        # Log memory before loading
        self.log_memory_status("Before model loading")
        
        # Load tokenizer
        logger.info("📝 Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            padding_side="right",
        )
        
        # Fix tokenizer issues
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            tokenizer.pad_token_id = tokenizer.eos_token_id
        
        logger.info(f"✅ Tokenizer loaded (vocab size: {len(tokenizer)})")
        
        # Load model with quantization
        logger.info("🧠 Loading model with 4-bit quantization...")
        
        try:
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=bnb_config,
                device_map="auto",                    # Automatic device placement
                torch_dtype=torch.bfloat16,           # Use bfloat16
                trust_remote_code=True,
                low_cpu_mem_usage=True,               # Reduce CPU memory usage
                attn_implementation="flash_attention_2"  # Flash Attention 2
            )
        except Exception as e:
            logger.warning(f"⚠️ Flash Attention 2 failed, using standard attention: {e}")
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.bfloat16,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
        
        logger.info("✅ Model loaded successfully")
        self.log_memory_status("After model loading")
        
        return model, tokenizer
    
    def setup_qlora_config(self) -> LoraConfig:
        """Setup QLoRA configuration"""
        logger.info("🎯 Setting up QLoRA configuration...")
        
        # Llama-3.1 target modules
        target_modules = [
            # Attention layers (most important for fine-tuning)
            "q_proj", "k_proj", "v_proj", "o_proj",
            # MLP layers
            "gate_proj", "up_proj", "down_proj"
        ]
        
        lora_config = LoraConfig(
            r=self.config["lora_r"],                    # Rank (64 for high quality)
            lora_alpha=self.config["lora_alpha"],       # Alpha (128 = 2*rank)
            target_modules=target_modules,              # Which modules to adapt
            lora_dropout=self.config["lora_dropout"],   # Dropout (0.05 low)
            bias="none",                                # Don't adapt bias
            task_type=TaskType.CAUSAL_LM,               # Causal language modeling
            inference_mode=False,                       # Training mode
        )
        
        logger.info("✅ QLoRA configuration:")
        logger.info(f"   🎲 Rank (r): {lora_config.r}")
        logger.info(f"   📈 Alpha: {lora_config.lora_alpha}")
        logger.info(f"   🎯 Target modules: {len(target_modules)}")
        logger.info(f"   💧 Dropout: {lora_config.lora_dropout}")
        
        return lora_config
    
    def setup_training_arguments(self, dataset_size: int) -> TrainingArguments:
        """Setup training arguments optimized for RTX 4060"""
        logger.info("📋 Setting up training arguments...")
        
        # Calculate training steps
        steps_per_epoch = max(1, dataset_size // (
            self.config["batch_size"] * self.config["gradient_accumulation"]
        ))
        total_steps = steps_per_epoch * self.config["num_epochs"]
        warmup_steps = int(total_steps * self.config["warmup_ratio"])
        
        # Effective batch size
        effective_batch_size = (
            self.config["batch_size"] * self.config["gradient_accumulation"]
        )
        
        training_args = TrainingArguments(
            # Output and logging
            output_dir=self.output_dir,
            logging_dir=os.path.join(self.logs_dir, "tensorboard"),
            logging_steps=1,
            run_name=f"qlora-llama31-{datetime.now().strftime('%m%d_%H%M')}",
            
            # Training schedule
            num_train_epochs=self.config["num_epochs"],
            
            # Batch settings
            per_device_train_batch_size=self.config["batch_size"],
            gradient_accumulation_steps=self.config["gradient_accumulation"],
            
            # Learning rate
            learning_rate=self.config["learning_rate"],
            weight_decay=self.config["weight_decay"],
            warmup_steps=warmup_steps,
            lr_scheduler_type="cosine",
            
            # Optimization
            optim="paged_adamw_8bit",               # Memory-efficient AdamW
            max_grad_norm=self.config["max_grad_norm"],
            
            # Memory optimization
            gradient_checkpointing=self.config["gradient_checkpointing"],
            dataloader_pin_memory=self.config["pin_memory"],
            dataloader_num_workers=self.config["dataloader_num_workers"],
            
            # Precision
            bf16=self.config["bf16"],
            fp16=self.config["fp16"],
            tf32=self.config["tf32"],
            
            # Saving
            save_strategy="steps",
            save_steps=max(1, total_steps // 5),     # Save 5 times during training
            save_total_limit=3,                     # Keep only 3 checkpoints
            
            # Misc
            seed=42,
            remove_unused_columns=False,
            disable_tqdm=False,                     # Show progress
            report_to=[],                           # No external logging
        )
        
        logger.info("✅ Training arguments configured:")
        logger.info(f"   📊 Total epochs: {self.config['num_epochs']}")
        logger.info(f"   📈 Steps per epoch: {steps_per_epoch}")
        logger.info(f"   🔥 Warmup steps: {warmup_steps}")
        logger.info(f"   🎯 Effective batch size: {effective_batch_size}")
        logger.info(f"   📚 Learning rate: {self.config['learning_rate']}")
        
        return training_args
    
    def fine_tune(self) -> bool:
        """Main fine-tuning process"""
        start_time = time.time()
        
        try:
            # Setup logging
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(self.logs_dir, f"qlora_training_{timestamp}.log")
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s | %(levelname)s | %(message)s'
            ))
            logger.addHandler(file_handler)
            
            logger.info("🚀 QLoRA Fine-tuning Started")
            logger.info("=" * 60)
            
            # System checks
            if not self.check_system_requirements():
                logger.error("❌ System requirements not met")
                return False
            
            # Optimize PyTorch
            self.optimize_pytorch_settings()
            
            # Load dataset
            dataset = self.load_and_prepare_dataset()
            
            # Load model and tokenizer
            model, tokenizer = self.load_model_and_tokenizer()
            self.model = model
            self.tokenizer = tokenizer
            
            # Prepare model for QLoRA
            logger.info("🔧 Preparing model for QLoRA training...")
            model = prepare_model_for_kbit_training(model)
            
            # Setup QLoRA
            qlora_config = self.setup_qlora_config()
            model = get_peft_model(model, qlora_config)
            self.peft_model = model
            
            # Print trainable parameters
            trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
            total_params = sum(p.numel() for p in model.parameters())
            logger.info(f"🎯 Trainable parameters: {trainable_params:,} ({trainable_params/total_params*100:.2f}%)")
            
            # Setup training
            training_args = self.setup_training_arguments(len(dataset))
            
            # Create trainer
            logger.info("🏃 Creating SFT Trainer...")
            trainer = SFTTrainer(
                model=model,
                tokenizer=tokenizer,
                train_dataset=dataset,
                args=training_args,
                dataset_text_field="text",
                max_seq_length=self.config["max_seq_length"],
                packing=False,  # Don't pack for instruction tuning
                callbacks=[
                    EarlyStoppingCallback(early_stopping_patience=3)
                ]
            )
            
            # Log memory before training
            self.log_memory_status("Before training start")
            
            # Start training
            logger.info("🚀 Starting QLoRA fine-tuning...")
            logger.info("=" * 60)
            
            train_result = trainer.train()
            
            logger.info("=" * 60)
            logger.info("✅ Training completed successfully!")
            
            # Log results
            final_loss = train_result.training_loss
            training_time = train_result.metrics.get('train_runtime', 0)
            
            logger.info(f"📊 Training Results:")
            logger.info(f"   Final loss: {final_loss:.4f}")
            logger.info(f"   Training time: {training_time:.0f} seconds")
            
            # Save model
            logger.info("💾 Saving fine-tuned model...")
            trainer.save_model()
            tokenizer.save_pretrained(self.output_dir)
            
            # Save metadata
            metadata = {
                "timestamp": timestamp,
                "model_name": self.model_name,
                "config": self.config,
                "dataset_size": len(dataset),
                "final_loss": final_loss,
                "training_time": training_time,
                "total_time": time.time() - start_time
            }
            
            metadata_path = os.path.join(self.output_dir, "training_metadata.json")
            with open(metadata_path, "w", encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📁 Model saved to: {self.output_dir}")
            logger.info(f"⚙️ Metadata saved to: {metadata_path}")
            
            # Final memory status
            self.log_memory_status("After training completion")
            
            # Cleanup
            self.cleanup_memory()
            
            total_time = time.time() - start_time
            logger.info(f"🎉 Total training time: {total_time/60:.1f} minutes")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Training failed: {str(e)}")
            import traceback
            logger.error("Full traceback:")
            logger.error(traceback.format_exc())
            
            # Cleanup on failure
            self.cleanup_memory()
            return False
    
    def cleanup_memory(self):
        """Clean up memory after training"""
        logger.info("🧹 Cleaning up memory...")
        
        # Delete model references
        if hasattr(self, 'model') and self.model is not None:
            del self.model
        if hasattr(self, 'peft_model') and self.peft_model is not None:
            del self.peft_model
        if hasattr(self, 'tokenizer') and self.tokenizer is not None:
            del self.tokenizer
        
        # Python garbage collection
        gc.collect()
        
        # CUDA cleanup
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        
        logger.info("✅ Memory cleanup completed")
    
    def test_model(self, num_samples: int = 3):
        """Test the fine-tuned model"""
        logger.info(f"🧪 Testing fine-tuned model with {num_samples} samples...")
        
        try:
            # Load the fine-tuned model
            logger.info("📂 Loading fine-tuned model for testing...")
            
            # Load base model
            bnb_config = self.setup_quantization_config()
            base_model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.bfloat16,
            )
            
            # Load PEFT model
            model = PeftModel.from_pretrained(base_model, self.output_dir)
            model.eval()
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(self.output_dir)
            
            # Test prompts
            test_prompts = [
                "### Instruction:\nKullanıcı bilgilerini getir\n\n### Input:\nID'si 12345 olan kullanıcının bilgilerini al\n\n### Response:",
                "### Instruction:\nFatura detayını getir\n\n### Input:\nMüşteri 5551234567 numaralı hattının Ocak 2024 fatura detayını göster\n\n### Response:",
                "### Instruction:\nStok durumunu kontrol et\n\n### Input:\nTüm ürünlerin stok durumunu listele\n\n### Response:"
            ]
            
            # Generate responses
            for i, prompt in enumerate(test_prompts[:num_samples]):
                logger.info(f"\n--- Test {i+1} ---")
                logger.info(f"Input: {prompt.split('### Input:')[1].split('### Response:')[0].strip() if '### Input:' in prompt else prompt.split('### Instruction:')[1].split('### Response:')[0].strip()}")
                
                # Tokenize
                inputs = tokenizer(
                    prompt,
                    return_tensors="pt",
                    truncation=True,
                    max_length=1024
                ).to(self.device)
                
                # Generate
                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=150,
                        temperature=0.7,
                        do_sample=True,
                        top_p=0.9,
                        top_k=50,
                        repetition_penalty=1.1,
                        pad_token_id=tokenizer.eos_token_id
                    )
                
                # Decode response
                full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                response_part = full_response[len(prompt):].strip()
                
                logger.info(f"Response: {response_part}")
            
            # Cleanup
            del model, base_model, tokenizer
            torch.cuda.empty_cache()
            
            logger.info("✅ Model testing completed")
            
        except Exception as e:
            logger.error(f"❌ Model testing failed: {str(e)}")

def main():
    """Main execution function"""
    print("🔥 QLoRA Fine-tuning for RTX 4060 + 32GB RAM")
    print("=" * 50)
    print("🎯 Hardware Optimizations:")
    print("   - RTX 4060: 8GB VRAM optimal usage")
    print("   - AMD Ryzen 9: Multi-core CPU optimization")
    print("   - 32GB RAM: Efficient data loading")
    print("   - QLoRA: 4-bit quantization + LoRA adapters")
    print("=" * 50)
    
    # Create fine-tuner
    fine_tuner = RTX4060QLoRAFineTuner()
    
    # Start fine-tuning
    print("\n🚀 Starting QLoRA fine-tuning process...")
    success = fine_tuner.fine_tune()
    
    if success:
        print(f"\n🎉 QLoRA fine-tuning completed successfully!")
        print(f"📁 Model saved to: {fine_tuner.output_dir}")
        
        # Test the model
        test_choice = input("\n🧪 Test the fine-tuned model? (y/n): ").lower().strip()
        if test_choice in ['y', 'yes', 'evet']:
            fine_tuner.test_model()
        
        print("\n✅ QLoRA fine-tuning complete! Your model is ready for use.")
        return 0
    else:
        print("\n❌ QLoRA fine-tuning failed. Check logs for details.")
        return 1

if __name__ == "__main__":
    exit(main()) 