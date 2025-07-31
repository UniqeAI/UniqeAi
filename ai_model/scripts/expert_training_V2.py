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

# --- DRIVE ROOT, güncellenmiş yollar ---
DRIVE_ROOT = Path("/content/drive/MyDrive/ChoyrensTrainingV2")

# --- 1. Yapılandırma (Configuration) ---
@dataclass
class ModelAndDataConfig:
    model_name: str = field(default="meta-llama/Meta-Llama-3-8B-Instruct", metadata={"help": "Hugging Face model adı."})
    # Tek seferde tüm JSON dosyalarını otomatik yüklemek için klasör yolu
    data_paths: List[str] = field(
        default_factory=lambda: [str(DRIVE_ROOT / "datasets")],
        metadata={"help": "Eğitim için kullanılacak JSON veri dosyalarının bulunduğu klasör."}
    )
    test_size: float = field(default=0.1, metadata={"help": "Değerlendirme seti yüzdesi."})
    lora_r: int = field(default=16, metadata={"help": "LoRA rank."})
    lora_alpha: int = field(default=32, metadata={"help": "LoRA alpha."})
    lora_dropout: float = field(default=0.05, metadata={"help": "LoRA dropout."})
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        metadata={"help": "LoRA uygulanacak modüller."}
    )
    wandb_project: str = field(default="ChoyrensAI-Telekom-Agent-v2", metadata={"help": "W&B proje adı."})
    use_wandb: bool = field(default="WANDB_API_KEY" in os.environ, metadata={"help": "W&B entegrasyonunu etkinleştir."})

@dataclass
class TrainingArguments(HfTrainingArguments):
    # Çıktıları direkt Drive içindeki outputs klasörüne yaz
    output_dir: str = str(DRIVE_ROOT / "outputs")
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

class SafeAdapterSaveCallback(TrainerCallback):
    def on_save(self, args: HfTrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        model = kwargs["model"]
        checkpoint_dir = os.path.join(args.output_dir, f"checkpoint-{state.global_step}")
        adapter_backup_dir = os.path.join(checkpoint_dir, "adapter_backup")
        if state.is_world_process_zero:
            os.makedirs(adapter_backup_dir, exist_ok=True)
            model.save_pretrained(adapter_backup_dir)
            logger.info(f"✅ Adaptör yedeği kaydedildi: '{adapter_backup_dir}'")

class ExpertTrainer:
    def __init__(self, model_config: ModelAndDataConfig, training_args: TrainingArguments):
        self.config = model_config
        self.training_args = training_args
        # Drive içindeki output klasörü var mı, yoksa oluştur
        os.makedirs(self.training_args.output_dir, exist_ok=True)

    def _format_dialogue(self, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        # ... aynı formatlama fonksiyonu burada ...
        return []  # kısaltıldı

    def _load_and_prepare_dataset(self, tokenizer: AutoTokenizer) -> Dataset:
        # Klasör verisi sağlar veya tek dosya listesi
        import glob
        all_paths = []
        for p in self.config.data_paths:
            if os.path.isdir(p):
                all_paths.extend(sorted(glob.glob(os.path.join(p, "*.json"))))
            elif os.path.isfile(p):
                all_paths.append(p)

        logger.info(f"💾 Veri setleri yükleniyor: {all_paths}")
        all_data = []
        for full_path in all_paths:
            with open(full_path, 'r', encoding='utf-8') as f:
                all_data.extend(json.load(f))

        # Formatlama ve Dataset dönüşümü...
        # (orijinal koddaki adımlar aynı kalır)
        return Dataset.from_list([]).train_test_split(test_size=self.config.test_size)

    def run(self):
        # ... model yükleme ve eğitime başlama kodu aynı kalır ...
        pass


def main():
    parser = HfArgumentParser((ModelAndDataConfig, TrainingArguments))
    model_config, training_args = parser.parse_args_into_dataclasses()
    trainer = ExpertTrainer(model_config, training_args)
    trainer.run()

if __name__ == "__main__":
    main()
