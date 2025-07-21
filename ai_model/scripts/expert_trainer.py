"""
🚀 Uzman Seviye QLoRA Eğitim Script'i (Expert-Level QLoRA Trainer) - v2 (Format Düzeltildi)
=============================================================================================

Bu script, "olağanüstü" bir AI modeli hedefiyle, Llama-3-Instruct
modellerini QLoRA tekniği ile verimli ve profesyonel bir şekilde
eğitmek için tasarlanmıştır.

BU VERSİYONDAKİ KRİTİK DÜZELTME:
- ✅ **NİHAİ FORMATLAMA DÜZELTMESİ:** `_format_dialogue` fonksiyonu,
  eğitim verisini Llama-3'ün araç çağırma formatına %100 doğru şekilde
  çevirecek şekilde yeniden yazıldı. Önceki "None" ve "birbirine karışmış metin"
  hataları tamamen giderildi. Bu, eğitimin başarılı olması için en kritik adımdır.
"""

import os
import gc
import json
import torch
import logging
import uuid
from datetime import datetime
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
    SchedulerType,
    TrainerCallback,
    TrainerState,
    TrainerControl
)
from transformers.trainer_utils import get_last_checkpoint
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# --- 1. Yapılandırma (Configuration) ---

@dataclass
class ModelAndDataConfig:
    model_name: str = field(default="meta-llama/Meta-Llama-3-8B-Instruct", metadata={"help": "Hugging Face model adı."})
    data_paths: List[str] = field(
        default_factory=lambda: [
            "UniqeAi/ai_model/data/expert_tool_chaining_data_v2_validated.json",
            "UniqeAi/ai_model/data/ultra_disambiguation_data_v1_validated.json"
        ],
        metadata={"help": "Eğitim için kullanılacak JSON veri dosyaları."}
    )
    test_size: float = field(default=0.1, metadata={"help": "Değerlendirme seti yüzdesi."})
    lora_r: int = field(default=16, metadata={"help": "LoRA rank."})
    lora_alpha: int = field(default=32, metadata={"help": "LoRA alpha."})
    lora_dropout: float = field(default=0.05, metadata={"help": "LoRA dropout."})
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        metadata={"help": "LoRA uygulanacak modüller."}
    )
    wandb_project: str = field(default="ChoyrensAI-Telekom-Agent-v2", metadata={"help": "Weights & Biases proje adı."})
    use_wandb: bool = field(default="WANDB_API_KEY" in os.environ, metadata={"help": "W&B entegrasyonunu etkinleştir."})

@dataclass
class TrainingArguments(HfTrainingArguments):
    output_dir: str = "UniqeAi/ai_model/final-model_v2" # Son model ve checkpoint'ler için yeni klasör
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 1
    per_device_eval_batch_size: int = 1
    gradient_accumulation_steps: int = 4
    gradient_checkpointing: bool = True
    learning_rate: float = 2e-5
    logging_strategy: str = "steps"
    logging_steps: int = 10
    save_strategy: str = "steps"
    save_steps: int = 25
    eval_strategy: str = "steps"
    eval_steps: int = 25
    bf16: bool = True
    load_best_model_at_end: bool = True
    metric_for_best_model: str = "eval_loss"
    save_total_limit: int = 2
    lr_scheduler_type: SchedulerType = "cosine"
    optim: str = "paged_adamw_8bit"
    report_to: str = "wandb" if "WANDB_API_KEY" in os.environ else "none"
    max_seq_length: int = 2048
    dataset_text_field: str = "text"
    packing: bool = True

def setup_huggingface_token():
    dotenv_path = PROJECT_ROOT / ".env"
    load_dotenv(dotenv_path=dotenv_path)
    token = os.getenv('HUGGINGFACE_HUB_TOKEN')
    if not token:
        logger.error("HUGGINGFACE_HUB_TOKEN bulunamadı.")
        return False
    os.environ['HF_TOKEN'] = token
    logger.info("✅ Hugging Face token başarıyla kuruldu.")
    return True

class SafeAdapterSaveCallback(TrainerCallback):
    def on_save(self, args: HfTrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        model = kwargs["model"]
        checkpoint_dir = os.path.join(args.output_dir, f"checkpoint-{state.global_step}")
        adapter_backup_dir = os.path.join(checkpoint_dir, "adapter_backup")
        if state.is_world_process_zero:
            try:
                os.makedirs(adapter_backup_dir, exist_ok=True)
                model.save_pretrained(adapter_backup_dir)
                logger.info(f"✅ Hafif adaptör yedeği kaydedildi: '{adapter_backup_dir}'")
            except Exception as e:
                logger.error(f"Hafif adaptör yedeği kaydedilirken hata oluştu: {e}", exc_info=True)

class ExpertTrainer:
    def __init__(self, model_config: ModelAndDataConfig, training_args: TrainingArguments):
        self.config = model_config
        self.training_args = training_args
        if not setup_huggingface_token():
            raise ValueError("Eğitim için Hugging Face token'ı gereklidir.")
        self.training_args.output_dir = str(PROJECT_ROOT / self.training_args.output_dir)
        os.makedirs(self.training_args.output_dir, exist_ok=True)

    def _format_dialogue(self, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        JSON formatımızı Llama-3'ün Chat Template formatına DÜZGÜN bir şekilde dönüştürür.
        
        KRİTİK DÜZELTME v2: `tool_calls` JSON yapısı yerine, Llama-3'ün anladığı
        doğrudan metin formatı `<|begin_of_tool_code|>...` oluşturulur.
        """
        dialogue = []
        for turn in item["donguler"]:
            role = turn["rol"]
            content = turn.get("icerik")
            tool_calls_data = turn.get("arac_cagrilari")

            if role == "kullanici":
                dialogue.append({"role": "user", "content": content})
            
            elif role == "asistan":
                # Asistanın konuşacak bir şeyi mi var, yoksa araç mı çağıracak?
                if content:
                    # Normal metin cevabı varsa, onu ekle
                    dialogue.append({"role": "assistant", "content": content})

                if tool_calls_data:
                    # Eğer araç çağrısı varsa, bunu Llama-3'ün beklediği metin formatına çevir
                    tool_code_string = "<|begin_of_tool_code|>\n"
                    for call in tool_calls_data:
                        # Argümanları `anahtar="değer"` veya `anahtar=sayı` formatına getir
                        args_list = []
                        for key, value in call["parametreler"].items():
                            if isinstance(value, str):
                                # String değerleri çift tırnak içine al ve kaçış karakterlerini yönet
                                formatted_value = json.dumps(value)
                                args_list.append(f"{key}={formatted_value}")
                            else:
                                # Sayısal, boolean veya null değerler olduğu gibi kalır
                                args_list.append(f"{key}={json.dumps(value)}")
                        
                        args_str = ", ".join(args_list)
                        tool_code_string += f"print({call['fonksiyon']}({args_str}))\n"
                    
                    tool_code_string += "<|end_of_tool_code|>"
                    
                    # Bu özel formatlanmış metni içeren bir asistan mesajı ekle
                    dialogue.append({"role": "assistant", "content": tool_code_string})

            elif role == "arac":
                # Llama-3, araç çıktısını "tool" rolüyle bekler.
                # Önceki asistan mesajında bir araç çağrısı olduğunu varsayar.
                dialogue.append({
                    "role": "tool", 
                    "content": content,
                })
        return dialogue


    def _load_and_prepare_dataset(self, tokenizer: AutoTokenizer) -> Dataset:
        logger.info(f"💾 Veri setleri yükleniyor: {self.config.data_paths}")
        all_data = []
        for path in self.config.data_paths:
            full_path = PROJECT_ROOT / path
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)
        
        logger.info(f"📄 Toplam {len(all_data)} adet diyalog yüklendi.")
        
        formatted_texts = []
        for item in all_data:
            dialogue = self._format_dialogue(item)
            try:
                formatted_text = tokenizer.apply_chat_template(
                    dialogue, 
                    tokenize=False, 
                    add_generation_prompt=False
                )
                formatted_texts.append({"text": formatted_text})
            except Exception as e:
                logger.error(f"Bir diyalog formatlanırken hata oluştu. Veri ID: {item.get('id', 'N/A')}. Hata: {e}")
                logger.error(f"Hatalı diyalog yapısı: {json.dumps(dialogue, indent=2)}")


        dataset = Dataset.from_list(formatted_texts)
        logger.info("✅ Veri seti Llama-3 formatına dönüştürüldü.")
        return dataset.train_test_split(test_size=self.config.test_size)

    def run(self):
        logger.info("🚀 Uzman seviye eğitim süreci (v2) başlatılıyor...")
        
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True,
        )

        model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
        model.config.use_cache = False
        
        logger.info("✅ Model ve tokenizer yüklendi.")

        split_dataset = self._load_and_prepare_dataset(tokenizer)
        
        model = prepare_model_for_kbit_training(model)
        lora_config = LoraConfig(
            r=self.config.lora_r, lora_alpha=self.config.lora_alpha,
            target_modules=self.config.lora_target_modules,
            lora_dropout=self.config.lora_dropout,
            bias="none", task_type="CAUSAL_LM",
        )
        model = get_peft_model(model, lora_config)
        
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in model.parameters())
        logger.info(f"🎯 Eğitilebilir parametreler: {trainable_params:,} / {total_params:,} ({100 * trainable_params / total_params:.2f}%)")

        trainer = SFTTrainer(
            model=model,
            args=self.training_args,
            train_dataset=split_dataset["train"],
            eval_dataset=split_dataset["test"],
            tokenizer=tokenizer,
            callbacks=[SafeAdapterSaveCallback()],
            # --- EKSİK ARGÜMANLAR EKLENDİ ---
            packing=self.training_args.packing,
            dataset_text_field=self.training_args.dataset_text_field,
            max_seq_length=self.training_args.max_seq_length,
        )

        logger.info("🔥 Eğitim başlıyor...")
        # Checkpoint'ten devam etme mantığı burada basitleştirilebilir veya olduğu gibi kalabilir
        last_checkpoint = get_last_checkpoint(self.training_args.output_dir)
        trainer.train(resume_from_checkpoint=last_checkpoint)

        logger.info("💾 En iyi model kaydediliyor...")
        final_model_path = os.path.join(self.training_args.output_dir, "final_model")
        trainer.save_model(final_model_path)
        tokenizer.save_pretrained(final_model_path)
        
        logger.info(f"🎉 Eğitim tamamlandı! Model '{final_model_path}' dizinine kaydedildi.")
        del model, trainer
        gc.collect()
        torch.cuda.empty_cache()

def main():
    parser = HfArgumentParser((ModelAndDataConfig, TrainingArguments))
    model_config, training_args = parser.parse_args_into_dataclasses()

    if model_config.use_wandb:
        run_name = f"core-engine-v2-{datetime.now().strftime('%Y%m%d-%H%M')}"
        training_args.run_name = run_name
        os.environ["WANDB_PROJECT"] = model_config.wandb_project

    try:
        trainer = ExpertTrainer(model_config, training_args)
        trainer.run()
    except Exception as e:
        logger.error(f"Eğitim sırasında beklenmedik bir hata oluştu: {e}", exc_info=True)

if __name__ == "__main__":
    main()