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
from typing import List, Dict, Any, Optional
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
            "UniqeAi/ai_model/data/ultimate_human_level_dataset_v2_enhanced_20250805_210650.json"
        ],
        metadata={"help": "Eğitim için kullanılacak NİHAİ ve tek veri dosyası."}
    )
    test_size: float = field(default=0.1, metadata={"help": "Değerlendirme seti yüzdesi."})
    lora_r: int = field(default=16, metadata={"help": "LoRA rank."})
    lora_alpha: int = field(default=32, metadata={"help": "LoRA alpha."})
    lora_dropout: float = field(default=0.05, metadata={"help": "LoRA dropout."})
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        metadata={"help": "LoRA uygulanacak modüller."}
    )
    wandb_project: str = field(default="ChoyrensAI-Telekom-Agent-v3-BF16", metadata={"help": "Weights & Biases proje adı."})
    use_wandb: bool = field(default="WANDB_API_KEY" in os.environ, metadata={"help": "W&B entegrasyonunu etkinleştir."})
    use_bf16_training: bool = field(
        default=True, 
        metadata={"help": "True ise tam BF16 (A100/H100 için), False ise 4-bit QLoRA (T4/4060 için)."}
    )

@dataclass
class TrainingArguments(HfTrainingArguments):
    output_dir: str = "UniqeAi/ai_model/final-model_v5_bf16" # Son model ve checkpoint'ler için yeni klasör
    num_train_epochs: int = 3
    # UZMAN SEVİYESİ OPTİMİZASYON: A100 (40GB) OOM hatasını çözmek için anlık yığın boyutu mutlak minimuma (1) indirildi.
    per_device_train_batch_size: int = 1
    per_device_eval_batch_size: int = 1
    # UZMAN SEVİYESİ OPTİMİZASYON: Anlık yığın boyutu azaldığı için, efektif yığın boyutunu (1*16=16) korumak amacıyla biriktirme adımları artırıldı.
    gradient_accumulation_steps: int = 16
    gradient_checkpointing: bool = True
    gradient_checkpointing_kwargs: dict = field(
        default_factory=lambda: {"use_reentrant": False},
        metadata={"help": "torch.utils.checkpoint için kwargs, UserWarning'i bastırmak için."}
    )
    learning_rate: float = 2e-5
    logging_strategy: str = "steps"
    logging_steps: int = 100 # Büyük veri seti için optimize edildi (önceki: 10)
    save_strategy: str = "steps"
    save_steps: int = 100 # Büyük veri seti için optimize edildi (önceki: 25)
    eval_strategy: str = "steps"
    eval_steps: int = 100 # Büyük veri seti için optimize edildi (önceki: 25)
    bf16: bool = True # Varsayılan olarak False, A100 modu için dinamik olarak True yapılır.
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
        self.tokenizer = None

    def _normalize_dialogue_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Farklı jenerasyonlardan (örn: grandmaster_v3) gelen veri formatlarını 
        standart 'donguler' formatına çevirir. Bu, eğitim script'ini evrensel hale getirir.
        """
        # Format 1: Zaten standart olan 'donguler' formatı
        if "donguler" in item and isinstance(item["donguler"], list):
            return item

        # Format 2: 'grandmaster_dataset_10k_v3.json' gibi 'conversation' formatı
        elif "conversation" in item and isinstance(item["conversation"], list):
            normalized_donguler = []
            for turn in item["conversation"]:
                # Rol anahtarlarını çevir ('user' -> 'kullanici', vb.)
                role = turn.get("role")
                if role == "user":
                    rol = "kullanici"
                elif role == "assistant":
                    rol = "asistan"
                elif role == "tool":
                    rol = "arac"
                else:
                    rol = role

                new_turn = {
                    "rol": rol,
                    "icerik": turn.get("content")
                }

                # Araç çağrılarını çevir ('tool_calls' -> 'arac_cagrilari')
                if "tool_calls" in turn and turn["tool_calls"]:
                    arac_cagrilari = []
                    for call in turn["tool_calls"]:
                        if not isinstance(call, dict): continue
                        arac_cagrilari.append({
                            "fonksiyon": call.get("name"),
                            "parametreler": call.get("arguments", {})
                        })
                    new_turn["arac_cagrilari"] = arac_cagrilari
                
                normalized_donguler.append(new_turn)
            
            # Orijinal item'ı dönüştürülmüş veriyle güncelle
            item["donguler"] = normalized_donguler
            return item
        
        # Eğer bilinen bir format değilse, None döndür ve logla
        return None

    def _format_dialogue(self, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        KRİTİK GÜNCELLEME v3: JSON formatımızı, Llama-3'ün beklediği standart
        araç çağırma (tool-calling) formatına %100 uyumlu hale getirir. Manuel metin
        oluşturma (`<|begin_of_tool_code|>`) yerine, `tokenizer.apply_chat_template`'in
        doğrudan işleyebileceği yapısal bir sözlük (dictionary) listesi döndürür.
        Bu, modelin araç çağırmayı kavramsal olarak öğrenmesi için en doğru yaklaşımdır.
        """
        dialogue = []
        # Bir asistan dönüşündeki araç çağrı ID'lerini bir sonraki araç yanıtı için sakla
        pending_tool_call_ids = []

        for turn in item["donguler"]:
            role = turn["rol"]
            content = turn.get("icerik")
            tool_calls_data = turn.get("arac_cagrilari")

            if role == "kullanici":
                dialogue.append({"role": "user", "content": content or ""})

            elif role == "asistan":
                assistant_message = {"role": "assistant", "content": content or ""}
                
                if tool_calls_data:
                    tool_calls = []
                    current_turn_ids = []
                    for call in tool_calls_data:
                        # Her araç çağrısı için benzersiz bir ID oluştur
                        tool_call_id = f"call_{uuid.uuid4().hex[:8]}"
                        current_turn_ids.append(tool_call_id)
                        tool_calls.append({
                            "id": tool_call_id,
                            "type": "function",
                            "function": {
                                "name": call["fonksiyon"],
                                # Argümanlar JSON string formatında olmalı
                                "arguments": json.dumps(call.get("parametreler", {}), ensure_ascii=False),
                            },
                        })
                    
                    assistant_message["tool_calls"] = tool_calls
                    # Bu ID'leri bir sonraki 'arac' dönüşü için sakla
                    pending_tool_call_ids = current_turn_ids
                
                dialogue.append(assistant_message)

            elif role == "arac":
                # Eğer bekleyen bir araç ID'si varsa, onu bu yanıta ata
                if pending_tool_call_ids:
                    # Genellikle bir önceki asistan dönüşünde tek bir çağrı olur,
                    # bu yüzden ilk ID'yi kullanmak çoğu senaryo için yeterlidir.
                    # Çoklu çağrı durumlarında bu mantığın genişletilmesi gerekebilir.
                    tool_call_id = pending_tool_call_ids.pop(0)
                    dialogue.append({
                        "role": "tool",
                        "content": content or "",
                        "tool_call_id": tool_call_id,
                    })
                else:
                    # Bu durum, veri setinde bir tutarsızlık olduğunu gösterir (yanıtsız çağrı)
                    # Ancak şimdilik uyarı verip devam ediyoruz.
                    logger.warning(
                        f"Bir 'arac' yanıtı bulundu ancak eşleşecek bekleyen 'asistan' "
                        f"araç çağrısı yok. Veri: {str(item)[:100]}"
                    )
                    # Yine de veriyi ekleyelim, ancak ID olmadan.
                    dialogue.append({ "role": "tool", "content": content or ""})
        return dialogue


    def _load_and_prepare_dataset(self, tokenizer: AutoTokenizer) -> Dataset:
        logger.info(f"💾 Veri setleri yükleniyor: {self.config.data_paths}")
        all_data = []
        for path in self.config.data_paths:
            full_path = PROJECT_ROOT / path
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)
        
        logger.info(f"📄 Toplam {len(all_data)} adet ham veri yüklendi.")
        
        formatted_texts = []
        skipped_count = 0
        for i, item in enumerate(all_data):
            # 1. Adım: Veriyi standart formata normalize et
            normalized_item = self._normalize_dialogue_item(item)
            
            if not normalized_item:
                logger.warning(f"Veri #{i+1}: Tanınmayan format, atlanıyor. Veri: {str(item)[:150]}...")
                skipped_count += 1
                continue

            # 2. Adım: Standart formattaki veriyi işle
            dialogue = self._format_dialogue(normalized_item)
            try:
                formatted_text = tokenizer.apply_chat_template(
                    dialogue, 
                    tokenize=False, 
                    add_generation_prompt=False
                )
                formatted_texts.append({"text": formatted_text})
            except Exception as e:
                item_id = normalized_item.get('id', 'N/A')
                logger.error(f"Bir diyalog formatlanırken hata oluştu. Veri ID: {item_id}. Hata: {e}")
                logger.error(f"Hatalı diyalog yapısı: {json.dumps(dialogue, indent=2)}")

        logger.info(f"✅ {len(formatted_texts)} adet diyalog başarıyla formatlandı.")
        if skipped_count > 0:
            logger.warning(f"⚠️ {skipped_count} adet diyalog tanınmayan format nedeniyle atlandı.")

        if not formatted_texts:
            logger.error("❌ EĞİTİM BAŞARISIZ: Hiçbir geçerli veri bulunamadı. Lütfen veri dosyalarınızın formatını kontrol edin.")
            raise ValueError("Oluşturulan eğitim verisi boş. Lütfen veri formatlarını kontrol edin.")

        dataset = Dataset.from_list(formatted_texts)
        logger.info("✅ Veri seti Llama-3 formatına dönüştürüldü.")
        return dataset.train_test_split(test_size=self.config.test_size)

    def run(self):
        logger.info("🚀 Uzman seviye eğitim süreci (v3 - H100 BF16 Stratejisi) başlatılıyor...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # --- H100/A100 için BF16 veya 4060 gibi kartlar için QLoRA arasında seçim ---
        model_kwargs = {
            "device_map": "auto",
            "torch_dtype": torch.bfloat16,
        }

        if self.config.use_bf16_training:
            logger.info("🔥 Strateji: Tam hassasiyetli BF16. (A100/H100 için optimize)")
            # Quantization config KULLANILMIYOR.
            self.training_args.bf16 = True
        else:
            logger.info("⚙️ Strateji: 4-bit QLoRA. (T4/4060 gibi GPU'lar için optimize)")
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_quant_type="nf4",
                # UZMAN SEVİYESİ İYİLEŞTİRME: T4 gibi kartlar bfloat16'yı tam desteklemez,
                # bu nedenle QLoRA modunda float16 kullanmak daha güvenli ve uyumludur.
                bnb_4bit_compute_dtype=torch.float16, 
                bnb_4bit_use_double_quant=True,
            )
            model_kwargs["quantization_config"] = quantization_config
            # KRİTİK HATA DÜZELTMESİ: QLoRA için bf16 flag'ı Trainer'da False olmalı.
            self.training_args.bf16 = False

        model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            **model_kwargs
        )
        model.config.use_cache = False
        
        logger.info("✅ Model ve tokenizer yüklendi.")

        split_dataset = self._load_and_prepare_dataset(self.tokenizer)
        
        # `prepare_model_for_kbit_training` ismi kafa karıştırıcı olabilir, 
        # ama BF16 eğitiminde de gradient checkpointing gibi optimizasyonları etkinleştirmek için kullanışlıdır.
        model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=self.training_args.gradient_checkpointing)
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
            tokenizer=self.tokenizer,
            callbacks=[SafeAdapterSaveCallback()],
            # --- EKSİK ARGÜMANLAR EKLENDİ ---
            packing=self.training_args.packing,
            dataset_text_field=self.training_args.dataset_text_field,
            max_seq_length=self.training_args.max_seq_length,
        )

        logger.info("🔥 Eğitim başlıyor...")
        # UZMAN SEVİYESİ İYİLEŞTİRME: Colab gibi ortamlarda eğitimin yarıda kesilmesine karşı
        # sistemi dayanıklı hale getirmek için otomatik olarak son checkpoint'ten devam etme.
        last_checkpoint = get_last_checkpoint(self.training_args.output_dir)
        if last_checkpoint:
            logger.info(f"✅ Bulunan son checkpoint'ten devam ediliyor: {last_checkpoint}")
        
        trainer.train(resume_from_checkpoint=last_checkpoint)

        logger.info("💾 En iyi model kaydediliyor...")
        final_model_path = os.path.join(self.training_args.output_dir, "final_model_bf16" if self.config.use_bf16_training else "final_model_qlora")
        trainer.save_model(final_model_path)
        self.tokenizer.save_pretrained(final_model_path)
        
        logger.info(f"🎉 Eğitim tamamlandı! Model '{final_model_path}' dizinine kaydedildi.")
        del model, trainer
        gc.collect()
        torch.cuda.empty_cache()

def main():
    parser = HfArgumentParser((ModelAndDataConfig, TrainingArguments))
    model_config, training_args = parser.parse_args_into_dataclasses()

    if model_config.use_wandb:
        run_name = f"core-engine-v3-bf16-{datetime.now().strftime('%Y%m%d-%H%M')}"
        training_args.run_name = run_name
        os.environ["WANDB_PROJECT"] = model_config.wandb_project

    try:
        trainer = ExpertTrainer(model_config, training_args)
        trainer.run()
    except Exception as e:
        logger.error(f"Eğitim sırasında beklenmedik bir hata oluştu: {e}", exc_info=True)

if __name__ == "__main__":
    main()