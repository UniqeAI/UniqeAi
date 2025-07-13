# -*- coding: utf-8 -*-
"""
🚀 Uzman Seviye QLoRA Eğitim Script'i (Expert-Level QLoRA Trainer)
===================================================================

Bu script, "olağanüstü" bir AI modeli hedefiyle, Llama-3-Instruct
modellerini QLoRA tekniği ile verimli ve profesyonel bir şekilde
eğitmek için tasarlanmıştır.

Önceki script'in eksikliklerini giderir ve en iyi pratikleri uygular:
- ✅ **Doğru Chat Template:** Llama 3'ün native sohbet ve araç çağırma
  formatını kullanarak modelin tam potansiyelini açığa çıkarır.
- ✅ **Dinamik Veri Yönetimi:** Eğitilecek veri dosyalarını bir liste
  olarak alarak aşamalı eğitimi (phased training) destekler.
- ✅ **Train/Validation Split:** Veri setini otomatik olarak eğitim ve
  değerlendirme setlerine ayırarak overfitting'i izler ve en iyi modeli
  kaydeder.
- ✅ **SFTTrainer:** Hugging Face'in modern ve verimli Supervised
  Fine-tuning Trainer'ını kullanır.
- ✅ **W&B Entegrasyonu:** Weights & Biases ile eğitim metriklerinin
  izlenmesini sağlar (opsiyonel).
- ✅ **Modüler Yapılandırma:** Tüm parametreler tek bir `TrainingConfig`
  sınıfında toplanarak deney yönetimini kolaylaştırır.
"""

import os
import gc
import json
import torch
import logging
import uuid  # UUID kütüphanesini ekliyoruz
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path  # pathlib'i ekliyoruz
from dotenv import load_dotenv

# ML Kütüphaneleri
from datasets import Dataset, load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments as HfTrainingArguments, # Orijinalini yeniden adlandırıyoruz
    BitsAndBytesConfig,
    HfArgumentParser, 
    SchedulerType
)
# HATA ÇÖZÜMÜ: Checkpoint kontrolü için bu yardımcı fonksiyonu ekliyoruz
from transformers.trainer_utils import get_last_checkpoint
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Proje Kök Dizini Tanımlaması ---
# Script'in nerede çalıştırıldığından bağımsız olarak, her zaman doğru yolları bulmasını sağlar.
# expert_trainer.py -> scripts -> ai_model -> UniqeAi -> tddi_proje_planlama (KÖK DİZİN)
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# --- 1. Yapılandırma (Configuration) ---

@dataclass
class ModelAndDataConfig:
    """
    Model, tokenizer ve veri ile ilgili temel yapılandırmayı tanımlar.
    Bu parametreler komut satırından override edilebilir.
    """
    # Model ve Tokenizer Ayarları
    model_name: str = field(
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        metadata={"help": "Kullanılacak Hugging Face modelinin adı."}
    )
    
    # Veri Seti Ayarları
    data_paths: List[str] = field(
        default_factory=lambda: [
            "UniqeAi/ai_model/data/expert_tool_chaining_data_v2_validated.json",
            "UniqeAi/ai_model/data/ultra_disambiguation_data_v1_validated.json"
        ],
        metadata={"help": "Eğitim için kullanılacak JSON veri dosyalarının proje kökünden göreli yolları."}
    )
    test_size: float = field(
        default=0.1,
        metadata={"help": "Değerlendirme seti için ayrılacak veri yüzdesi."}
    )

    # QLoRA Ayarları (RTX 4060 için optimize)
    lora_r: int = field(default=16, metadata={"help": "LoRA rank."})
    lora_alpha: int = field(default=32, metadata={"help": "LoRA alpha."})
    lora_dropout: float = field(default=0.05, metadata={"help": "LoRA dropout."})
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        metadata={"help": "LoRA uygulanacak modüller."}
    )
    
    # W&B Entegrasyonu
    wandb_project: str = field(default="ChoyrensAI-Telekom-Agent", metadata={"help": "Weights & Biases proje adı."})
    use_wandb: bool = field(default="WANDB_API_KEY" in os.environ, metadata={"help": "W&B entegrasyonunu etkinleştir."})

@dataclass
class TrainingArguments(HfTrainingArguments):
    """
    Eğitim argümanları için varsayılan değerlerimizi burada tanımlıyoruz.
    Bunların hepsi komut satırından override edilebilir.
    """
    output_dir: str = "UniqeAi/ai_model/results"
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 1
    per_device_eval_batch_size: int = 1
    gradient_accumulation_steps: int = 4
    gradient_checkpointing: bool = True
    learning_rate: float = 2e-5
    logging_strategy: str = "steps"
    logging_steps: int = 10
    save_strategy: str = "steps"
    save_steps: int = 50
    eval_strategy: str = "steps"
    eval_steps: int = 50
    bf16: bool = True
    load_best_model_at_end: bool = True
    metric_for_best_model: str = "eval_loss"
    save_total_limit: int = 2
    # Daha iyi yakınsama için kosinüs öğrenme oranı zamanlayıcısı
    lr_scheduler_type: SchedulerType = "cosine"
    # Daha bellek verimli bir optimizer
    optim: str = "paged_adamw_8bit"
    report_to: str = "wandb" if "WANDB_API_KEY" in os.environ else "none"

    # UYARI GİDERME: SFTTrainer için eskime uyarısı veren parametreleri buraya taşıyoruz.
    max_seq_length: int = 2048
    dataset_text_field: str = "text"
    packing: bool = True

def setup_huggingface_token():
    """Hugging Face token'ını .env dosyasından veya ortam değişkeninden kurar."""
    # Proje kök dizinindeki .env dosyasını yüklemeyi dener
    dotenv_path = PROJECT_ROOT / ".env"
    
    # python-dotenv'i kullanarak .env dosyasını yükle
    load_dotenv(dotenv_path=dotenv_path)
    
    token = os.getenv('HUGGINGFACE_HUB_TOKEN')
    if not token:
        logger.error("HUGGINGFACE_HUB_TOKEN, .env dosyasında veya ortam değişkenlerinde bulunamadı.")
        logger.error("Lütfen proje ana dizininde bir .env dosyası oluşturup içine HUGGINGFACE_HUB_TOKEN='hf_...' satırını ekleyin.")
        return False
        
    os.environ['HF_TOKEN'] = token
    logger.info("✅ Hugging Face token başarıyla kuruldu.")
    return True


class ExpertTrainer:
    def __init__(self, model_config: ModelAndDataConfig, training_args: TrainingArguments):
        self.config = model_config
        self.training_args = training_args
        if not setup_huggingface_token():
            raise ValueError("Eğitimi başlatmak için Hugging Face token'ı gereklidir.")
        
        # Çıktı dizinini mutlak yola çevirerek "kayıp checkpoint" sorununu çözüyoruz.
        self.training_args.output_dir = str(PROJECT_ROOT / self.training_args.output_dir)
        os.makedirs(self.training_args.output_dir, exist_ok=True)

    def _format_dialogue(self, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Bizim JSON formatımızı Llama-3'ün Chat Template formatına dönüştürür.
        Bu fonksiyon, bu script'in en kritik parçasıdır.
        """
        dialogue = []
        for turn in item["donguler"]:
            role = turn["rol"]
            content = turn.get("icerik")

            if role == "kullanici":
                dialogue.append({"role": "user", "content": content})
            
            elif role == "asistan":
                if content: # Eğer asistanın sözlü yanıtı varsa
                    dialogue.append({"role": "assistant", "content": content})
                
                if "arac_cagrilari" in turn and turn["arac_cagrilari"]:
                    # Llama 3 tool call formatı
                    tool_calls = []
                    for call in turn["arac_cagrilari"]:
                        # DAHA SAĞLAM: Her çağrı için çakışması imkansız bir UUID kullanıyoruz.
                        tool_call_id = str(uuid.uuid4())
                        tool_calls.append({
                            "id": tool_call_id,
                            "type": "function",
                            "function": {
                                "name": call["fonksiyon"],
                                "arguments": json.dumps(call["parametreler"])
                            }
                        })
                    dialogue.append({"role": "assistant", "content": None, "tool_calls": tool_calls})

            elif role == "arac":
                # Llama 3 tool response formatı
                # MEVCUT VARSAYIM: Veri setimizde her "arac" yanıtı, bir önceki "asistan"
                # mesajındaki ilk ve tek araç çağrısına karşılık gelir.
                # GELECEK İÇİN NOT: Paralel araç çağırma (multi-tool-call) senaryoları için
                # veri setinde aracın hangi 'tool_call_id'ye yanıt verdiğini belirten
                # bir anahtar eklenmesi ve buradaki mantığın güncellenmesi gerekecektir.
                try:
                    last_tool_call_id = dialogue[-1]["tool_calls"][0]["id"]
                    dialogue.append({
                        "role": "tool", 
                        "content": content,
                        "tool_call_id": last_tool_call_id
                    })
                except (KeyError, IndexError):
                    logger.warning(f"Bir araç yanıtı için geçerli bir araç çağrısı bulunamadı. Veri ID: {item.get('id', 'N/A')}")

        return dialogue

    def _load_and_prepare_dataset(self, tokenizer: AutoTokenizer) -> Dataset:
        """Verilen yollardan veri setlerini yükler, birleştirir ve formatlar."""
        logger.info(f"💾 Veri setleri yükleniyor: {self.config.data_paths}")
        
        all_data = []
        for path in self.config.data_paths:
            # Veri yolu artık proje köküne göre, mutlak yola çeviriyoruz.
            full_path = PROJECT_ROOT / path
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)
        
        logger.info(f"📄 Toplam {len(all_data)} adet diyalog yüklendi.")
        
        # Llama-3'ün ChatML formatını kullanarak her bir diyaloğu formatla
        formatted_texts = []
        for item in all_data:
            dialogue = self._format_dialogue(item)
            formatted_text = tokenizer.apply_chat_template(
                dialogue, 
                tokenize=False, 
                add_generation_prompt=False
            )
            formatted_texts.append({"text": formatted_text})

        dataset = Dataset.from_list(formatted_texts)
        logger.info("✅ Veri seti Llama-3 formatına dönüştürüldü.")
        
        return dataset.train_test_split(test_size=self.config.test_size)

    def run(self):
        """Eğitim sürecini başlatır ve yönetir."""
        logger.info("🚀 Uzman seviye eğitim süreci başlatılıyor...")
        
        # 1. Tokenizer ve Modelin Yüklenmesi
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        # Llama-3'ün pad token'ı yok, eos_token'ı kullanıyoruz
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )

        model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.bfloat16, # RTX 40xx serisi için float16 daha iyi
        )
        model.config.use_cache = False
        
        logger.info("✅ Model ve tokenizer başarıyla yüklendi.")

        # 2. Veri Setinin Yüklenmesi ve Hazırlanması
        split_dataset = self._load_and_prepare_dataset(tokenizer)
        train_dataset = split_dataset["train"]
        eval_dataset = split_dataset["test"]
        logger.info(f"Split: {len(train_dataset)} train, {len(eval_dataset)} eval.")

        # 3. QLoRA Yapılandırması
        model = prepare_model_for_kbit_training(model)
        lora_config = LoraConfig(
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            target_modules=self.config.lora_target_modules,
            lora_dropout=self.config.lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
        )
        model = get_peft_model(model, lora_config)
        
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in model.parameters())
        logger.info(f"🎯 Eğitilebilir parametreler: {trainable_params:,} / {total_params:,} ({100 * trainable_params / total_params:.2f}%)")

        # 4. SFTTrainer'ın Oluşturulması
        trainer = SFTTrainer(
            model=model,
            args=self.training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer,
            # UYARI GİDERME: Bu parametreler artık `training_args` içinden okunuyor.
            # dataset_text_field="text",
            # max_seq_length=self.config.max_seq_length,
            # packing=True, 
        )

        # 5. Eğitimin Başlatılması
        logger.info("🔥 Eğitim başlıyor...")
        
        # HATA ÇÖZÜMÜ: output_dir içinde bir checkpoint olup olmadığını akıllıca kontrol et.
        # Varsa, oradan devam et. Yoksa, sıfırdan başla.
        last_checkpoint = get_last_checkpoint(self.training_args.output_dir)
        if last_checkpoint:
            logger.info(f"✅ Geçerli bir checkpoint bulundu, eğitim '{last_checkpoint}' adresinden devam edecek.")
        else:
            logger.info("ℹ️ Geçerli bir checkpoint bulunamadı, eğitim sıfırdan başlıyor.")

        trainer.train(resume_from_checkpoint=last_checkpoint)


        # 6. Modelin Kaydedilmesi
        logger.info("💾 En iyi model kaydediliyor...")
        final_model_path = os.path.join(self.training_args.output_dir, "final_model")
        trainer.save_model(final_model_path)
        tokenizer.save_pretrained(final_model_path)
        
        logger.info(f"🎉 Eğitim tamamlandı! Model '{final_model_path}' dizinine kaydedildi.")

        # Temizlik
        del model
        del trainer
        gc.collect()
        torch.cuda.empty_cache()


def main():
    """
    Ana fonksiyonu çalıştırır. Argümanları komut satırından alır,
    eğitimi yapılandırır ve başlatır.
    """
    logger.info("--- Strateji 1 & 2 için 'Core-Engine' Modeli Eğitimi ---")

    # UZMAN SEVİYESİ GÜNCELLEMESİ:
    # Argümanları iki ayrı, mantıksal gruba ayırıyoruz ve HfArgumentParser
    # ile komut satırından okuyoruz. Bu en temiz ve doğru yöntemdir.
    parser = HfArgumentParser((ModelAndDataConfig, TrainingArguments))
    model_config, training_args = parser.parse_args_into_dataclasses()

    # W&B için dinamik olarak bir çalıştırma adı oluşturuyoruz
    if model_config.use_wandb:
        training_args.run_name = f"core-engine-{datetime.now().strftime('%Y-%m-%d-%H-%M')}"

    try:
        trainer = ExpertTrainer(model_config, training_args)
        trainer.run()
    except Exception as e:
        logger.error(f"Eğitim sırasında beklenmedik bir hata oluştu: {e}", exc_info=True)

if __name__ == "__main__":
    main()