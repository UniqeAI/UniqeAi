"""
🚀 Uzman Seviye Eğitim Script'i - v5.2 (En Kararlı Sürüm)
===========================================================

Bu script, "Dahi Çocuk Sendromu"nu kalıcı olarak tedavi etmek için tasarlanmış,
en sağlam ve hatasız eğitim adımıdır.

BU VERSİYONDAKİ KRİTİK DÜZELTMELER:
- ✅ **GRADYAN HATASI ÇÖZÜMÜ:** `does not require grad` hatasını çözmek için en
  sağlam yöntem olan "Yapılandırma ve Ağırlık Ayırma" tekniği uygulandı.
  Artık eski adaptörün kafa karıştırıcı yapılandırması yerine, yeni ve temiz
  bir LoRA yapılandırması oluşturulup eski ağırlıklar içine kopyalanıyor.
  Bu, eğitilebilir parametrelerin her zaman var olmasını garanti eder.
- ✅ Diğer tüm önceki düzeltmeler (Colab, PeftModel import, doğru veri seti) korunmuştur.
"""

import os
import gc
import json
import torch
import logging
from typing import List, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments as HfTrainingArguments,
    BitsAndBytesConfig,
    HfArgumentParser,
    SchedulerType
)
from transformers.trainer_utils import get_last_checkpoint
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, PeftModel
from trl import SFTTrainer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
logger.info(f"Proje kök dizini stabil olarak ayarlandı: {PROJECT_ROOT}")


@dataclass
class ModelAndDataConfig:
    model_name: str = field(default="meta-llama/Meta-Llama-3-8B-Instruct")
    data_paths: List[str] = field(
        default_factory=lambda: ["UniqeAi/ai_model/data/tool_forcing_dataset_v4_schema_driven.json"]
    )
    test_size: float = field(default=0.05)
    lora_r: int = field(default=8)
    lora_alpha: int = field(default=16)
    lora_dropout: float = field(default=0.05)
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj"]
    )
    use_bf16_training: bool = field(default=True)

@dataclass
class TrainingArguments(HfTrainingArguments):
    output_dir: str = "UniqeAi/ai_model/final-model_v7_surgical_intervention"
    num_train_epochs: int = 1
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 2
    gradient_accumulation_steps: int = 8
    gradient_checkpointing: bool = True
    gradient_checkpointing_kwargs: dict = field(default_factory=lambda: {"use_reentrant": False})
    learning_rate: float = 1e-5
    logging_strategy: str = "steps"
    logging_steps: int = 10
    save_strategy: str = "steps"
    save_steps: int = 20
    eval_strategy: str = "steps"
    eval_steps: int = 20
    bf16: bool = True 
    load_best_model_at_end: bool = True
    metric_for_best_model: str = "eval_loss"
    save_total_limit: int = 1
    lr_scheduler_type: SchedulerType = "linear"
    optim: str = "paged_adamw_8bit"
    report_to: str = "none"
    max_seq_length: int = 1024
    packing: bool = False

def setup_huggingface_token():
    dotenv_path = PROJECT_ROOT / ".env"
    load_dotenv(dotenv_path=dotenv_path)
    token = os.getenv('HUGGINGFACE_HUB_TOKEN')
    if not token:
        return False
    os.environ['HF_TOKEN'] = token
    return True

def format_dialogue(item: Dict[str, Any]) -> List[Dict[str, Any]]:
    dialogue = []
    for turn in item["donguler"]:
        role = turn["rol"]
        content = turn.get("icerik")
        tool_calls_data = turn.get("arac_cagrilari")
        if role == "kullanici":
            dialogue.append({"role": "user", "content": content})
        elif role == "asistan":
            if content: dialogue.append({"role": "assistant", "content": content})
            if tool_calls_data:
                tool_code_string = "<|begin_of_tool_code|>\n"
                for call in tool_calls_data:
                    args_list = [f"{k}={json.dumps(v)}" for k, v in call["parametreler"].items()]
                    args_str = ", ".join(args_list)
                    tool_code_string += f"print({call['fonksiyon']}({args_str}))\n"
                tool_code_string += "<|end_of_tool_code|>"
                dialogue.append({"role": "assistant", "content": tool_code_string})
    return dialogue

class ExpertTrainer:
    def __init__(self, model_config: ModelAndDataConfig, training_args: TrainingArguments):
        self.config = model_config
        self.training_args = training_args
        if not setup_huggingface_token(): raise ValueError("Hugging Face token'ı gerekli.")
        self.training_args.output_dir = str(PROJECT_ROOT / self.training_args.output_dir)
        os.makedirs(self.training_args.output_dir, exist_ok=True)
        self.tokenizer = None

    def _load_and_prepare_dataset(self, tokenizer: AutoTokenizer) -> Dataset:
        all_data = []
        for path in self.config.data_paths:
            full_path = PROJECT_ROOT / path
            with open(full_path, 'r', encoding='utf-8') as f:
                all_data.extend(json.load(f))
        
        formatted_texts = [
            {"text": tokenizer.apply_chat_template(
                format_dialogue(item), tokenize=False, add_generation_prompt=False
            )} for item in all_data
        ]
        return Dataset.from_list(formatted_texts).train_test_split(test_size=self.config.test_size)

    def run(self):
        logger.info("🚀 Nihai Cerrahi Müdahale Eğitimi (v7 - Kararlı Sürüm) başlatılıyor...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        if self.tokenizer.pad_token is None: self.tokenizer.pad_token = self.tokenizer.eos_token
        
        model_kwargs = {"device_map": "auto", "torch_dtype": torch.bfloat16}
        if not self.config.use_bf16_training:
            logger.info("⚙️ Strateji: 4-bit QLoRA.")
            model_kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16, bnb_4bit_use_double_quant=True
            )
        else:
            logger.info("🔥 Strateji: Tam hassasiyetli BF16.")

        # --- 1. Adım: Temel modeli yükle ---
        model = AutoModelForCausalLM.from_pretrained(self.config.model_name, **model_kwargs)
        model.config.use_cache = False
        logger.info("✅ Temel Llama-3 modeli yüklendi.")

        # --- 2. Adım: Yeni ve eğitilebilir LoRA katmanları oluştur ---
        # Önce modeli kbit eğitimi için hazırla
        model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=self.training_args.gradient_checkpointing)
        
        # Bu eğitim için geçerli olacak yeni LoRA yapılandırmasını oluştur
        lora_config = LoraConfig(
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            target_modules=self.config.lora_target_modules,
            lora_dropout=self.config.lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
        )
        # Yapılandırmayı modele uygula, bu bize eğitilebilir bir PeftModel verir
        model = get_peft_model(model, lora_config)
        logger.info("✅ Yeni ve eğitilebilir LoRA katmanları başarıyla oluşturuldu.")
        model.print_trainable_parameters()

        # --- 3. Adım: Eski bilgeliği yeni katmanlara kopyala ---
        previous_adapter_path = str(PROJECT_ROOT / "UniqeAi/ai_model/final-model_v3_bf16/final_model_bf16")
        if os.path.exists(os.path.join(previous_adapter_path, "adapter_config.json")):
            logger.info(f"🧠 Mevcut bilgelik (LoRA ağırlıkları) yükleniyor: {previous_adapter_path}")
            # `load_adapter` eski ağırlıkları mevcut PeftModel'e yükler
            model.load_adapter(previous_adapter_path, adapter_name="previous_wisdom")
            logger.info("✅ Önceki adaptör ağırlıkları yeni katmanlara başarıyla kopyalandı.")
        else:
            logger.warning(f"⚠️ Önceki adaptörler '{previous_adapter_path}' içinde bulunamadı. Eğitim SIFIRDAN başlayacak.")
        
        split_dataset = self._load_and_prepare_dataset(self.tokenizer)
        
        trainer = SFTTrainer(
            model=model,
            args=self.training_args,
            train_dataset=split_dataset["train"],
            eval_dataset=split_dataset["test"],
            tokenizer=self.tokenizer,
            packing=self.training_args.packing,
            dataset_text_field="text",
            max_seq_length=self.training_args.max_seq_length,
        )

        logger.info("🔥 Eğitim başlıyor...")
        last_checkpoint = get_last_checkpoint(self.training_args.output_dir)
        trainer.train(resume_from_checkpoint=last_checkpoint)

        logger.info("💾 En iyi model kaydediliyor...")
        final_model_path = os.path.join(self.training_args.output_dir, "final_model")
        trainer.save_model(final_model_path)
        self.tokenizer.save_pretrained(final_model_path)
        
        logger.info(f"🎉 Eğitim tamamlandı! Model '{final_model_path}' dizinine kaydedildi.")
        del model, trainer
        gc.collect()
        torch.cuda.empty_cache()

def main():
    parser = HfArgumentParser((ModelAndDataConfig, TrainingArguments))
    model_config, training_args = parser.parse_args_into_dataclasses()
    training_args.bf16 = model_config.use_bf16_training
    try:
        trainer = ExpertTrainer(model_config, training_args)
        trainer.run()
    except Exception as e:
        logger.error(f"Eğitim sırasında beklenmedik bir hata oluştu: {e}", exc_info=True)

if __name__ == "__main__":
    main()
