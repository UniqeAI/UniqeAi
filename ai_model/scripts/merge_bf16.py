# -*- coding: utf-8 -*-
"""
🚀 LoRA Adaptör Birleştirme Script'i (v2.2 - Nihai Offload Düzeltmesi)
======================================================================

Bu script, PEFT ile eğitilmiş bir LoRA adaptörünü, orijinal base model
ile birleştirir.

YENİ GÜNCELLEME: Bu versiyon, hem base modelin yüklenmesi hem de
LoRA adaptörünün onun üzerine uygulanması sırasında `offload_folder`
belirterek, inatçı `ValueError`'ı kesin olarak çözer.
"""

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from pathlib import Path
import logging
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Yapılandırma ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except NameError:
    PROJECT_ROOT = Path.cwd()

# Model ve adaptör yolları
BASE_MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
ADAPTER_MODEL_PATH = PROJECT_ROOT / "UniqeAi/ai_model/results/final_model_bf16"
MERGED_MODEL_OUTPUT_PATH = PROJECT_ROOT / "UniqeAi/ai_model/merged_model_fp16_v5"
OFFLOAD_DIR = PROJECT_ROOT / "temp_offload" # Geçici dosyalar için klasör

def main():
    """Ana birleştirme fonksiyonu."""
    
    if OFFLOAD_DIR.exists():
        logger.warning(f"Eski geçici klasör '{OFFLOAD_DIR}' bulunup siliniyor...")
        shutil.rmtree(OFFLOAD_DIR)
    os.makedirs(OFFLOAD_DIR, exist_ok=True)
    
    logger.info(f"🚀 Güvenli birleştirme işlemi başlıyor (Çıktı: FP16)...")
    logger.info(f"🔹 Çıktı Klasörü: {MERGED_MODEL_OUTPUT_PATH}")
    logger.info(f"🔹 Geçici Offload Klasörü: {OFFLOAD_DIR}")

    # 1. Base modeli yükle
    logger.info("1/4 - Orijinal base model (FP16 formatında) yükleniyor...")
    
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        torch_dtype=torch.float16,
        device_map="auto",
        offload_folder=str(OFFLOAD_DIR), 
        low_cpu_mem_usage=True
    )
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)

    # 2. PeftModel'i (adaptör ile birlikte) yükle
    logger.info("2/4 - LoRA adaptörü base model üzerine yükleniyor...")
    
    # NİHAİ DÜZELTME: `offload_folder` parametresini buraya da ekliyoruz.
    merged_model = PeftModel.from_pretrained(
        base_model, 
        str(ADAPTER_MODEL_PATH),
        offload_folder=str(OFFLOAD_DIR) # Hatanın asıl kaynağını çözen satır.
    )

    # 3. Modelleri birleştir
    logger.info("3/4 - Ağırlıklar birleştiriliyor (merge)...")
    merged_model = merged_model.merge_and_unload()
    logger.info("✅ Birleştirme tamamlandı.")

    # 4. Birleştirilmiş tam modeli ve tokenizer'ı kaydet
    logger.info(f"4/4 - Birleştirilmiş model '{MERGED_MODEL_OUTPUT_PATH}' klasörüne kaydediliyor...")
    merged_model.save_pretrained(str(MERGED_MODEL_OUTPUT_PATH))
    tokenizer.save_pretrained(str(MERGED_MODEL_OUTPUT_PATH))
    logger.info("✅ Model ve tokenizer başarıyla kaydedildi.")

    # Son olarak geçici klasörü tekrar temizle
    logger.info(f"Geçici offload klasörü '{OFFLOAD_DIR}' temizleniyor...")
    shutil.rmtree(OFFLOAD_DIR)
    logger.info("✅ Temizlik tamamlandı.")


if __name__ == "__main__":
    main()
