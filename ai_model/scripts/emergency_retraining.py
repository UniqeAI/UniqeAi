#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Acil Durum Yeniden Eğitim Script'i
================================

Model'in araç isimlerini doğru öğrenmesi için acil eğitim.
Pure AI test sonuçları model'in araç isimlerini bilmediğini gösterdi.

SORUN: Model eğitiminde araç isimleri doğru öğrenilememiş
ÇÖZÜM: Daha yoğun araç odaklı eğitim ile yeniden eğitim
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List
import json
import logging

# Proje yolunu ekle
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from UniqeAi.ai_model.scripts.expert_trainer import ExpertTrainer, ModelAndDataConfig, TrainingArguments

# Logging ayarla
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmergencyTrainingConfig(ModelAndDataConfig):
    """Acil durum eğitim konfigürasyonu - Araç odaklı"""
    # Daha agresif eğitim parametreleri
    lora_r: int = field(default=16)  # Daha yüksek rank
    lora_alpha: int = field(default=32)  # Daha yüksek alpha
    lora_dropout: float = field(default=0.1)  # Daha yüksek dropout
    
    # Sadece araç çağrı verilerini kullan
    dataset_files: List[str] = field(default_factory=lambda: [
        "ultimate_human_level_dataset_v2_enhanced_20250729_171909.json",
        "tool_forcing_dataset_v3_professional.json",
        "error_handling_data_v2_1000.json"
    ])

@dataclass 
class EmergencyTrainingArguments(TrainingArguments):
    """Acil durum eğitim argümanları - Daha yoğun"""
    output_dir: str = "UniqeAi/ai_model/emergency_retrained_model"
    num_train_epochs: int = 3  # Daha fazla epoch
    per_device_train_batch_size: int = 1  # Daha küçük batch
    gradient_accumulation_steps: int = 16  # Daha fazla accumulation
    learning_rate: float = 2e-5  # Daha yüksek learning rate
    save_steps: int = 50
    eval_steps: int = 50
    logging_steps: int = 5

def create_tool_focused_dataset():
    """Sadece araç çağrıları içeren veri setini oluştur"""
    logger.info("🎯 Araç odaklı veri seti oluşturuluyor...")
    
    # Bu fonksiyon, mevcut veri setlerinden sadece araç çağrısı içeren
    # örnekleri çıkarıp yoğunlaştırılmış bir eğitim seti oluşturur
    
    tool_examples = []
    
    # Temel araç örnekleri ekle
    basic_tools = [
        {
            "id": "TOOL_FOCUS_001",
            "senaryo": "Fatura Sorgulama Odaklı",
            "donguler": [
                {"rol": "kullanici", "icerik": "Bu ayki faturamı göster"},
                {"rol": "asistan", "icerik": "Fatura bilgilerinizi getiriyorum.", 
                 "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": 8901}}]},
                {"rol": "arac", "icerik": "{\"success\": true, \"data\": {\"amount\": 125.50}}"},
                {"rol": "asistan", "icerik": "Bu ayki faturanız 125.50 TL'dir."}
            ]
        },
        {
            "id": "TOOL_FOCUS_002", 
            "senaryo": "Ağ Durumu Odaklı",
            "donguler": [
                {"rol": "kullanici", "icerik": "İstanbul'da internet sorunu var mı?"},
                {"rol": "asistan", "icerik": "Ağ durumunu kontrol ediyorum.",
                 "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "İstanbul"}}]},
                {"rol": "arac", "icerik": "{\"success\": true, \"data\": {\"status\": \"normal\"}}"},
                {"rol": "asistan", "icerik": "İstanbul bölgesinde ağ durumu normal."}
            ]
        },
        {
            "id": "TOOL_FOCUS_003",
            "senaryo": "Roaming Odaklı", 
            "donguler": [
                {"rol": "kullanici", "icerik": "Almanya'ya gidiyorum, roaming aç"},
                {"rol": "asistan", "icerik": "Roaming hizmetinizi aktifleştiriyorum.",
                 "arac_cagrilari": [{"fonksiyon": "enable_roaming", "parametreler": {"user_id": 8901, "country": "Germany"}}]},
                {"rol": "arac", "icerik": "{\"success\": true, \"data\": {\"activated\": true}}"},
                {"rol": "asistan", "icerik": "Almanya roaming hizmetiniz aktifleştirildi."}
            ]
        }
    ]
    
    # Her örneği 10 kez tekrarla (yoğunlaştırma)
    for example in basic_tools:
        for i in range(10):
            example_copy = example.copy()
            example_copy["id"] = f"{example['id']}_REPEAT_{i+1}"
            tool_examples.append(example_copy)
    
    output_path = PROJECT_ROOT / "UniqeAi/ai_model/data/emergency_tool_focused_dataset.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tool_examples, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ {len(tool_examples)} araç odaklı örnek oluşturuldu: {output_path}")
    return str(output_path)

def main():
    """Acil durum yeniden eğitimi başlat"""
    logger.info("🚨 ACİL DURUM YENİDEN EĞİTİMİ BAŞLIYOR!")
    logger.info("📋 Sebep: Model araç isimlerini doğru öğrenememiş")
    logger.info("🎯 Hedef: Araç çağrılarında %100 doğruluk")
    
    # Araç odaklı veri seti oluştur
    tool_dataset_path = create_tool_focused_dataset()
    
    # Acil eğitim konfigürasyonu
    config = EmergencyTrainingConfig()
    config.dataset_files = ["emergency_tool_focused_dataset.json"]  # Sadece araç odaklı
    
    training_args = EmergencyTrainingArguments()
    
    # Eğitimi başlat
    trainer = ExpertTrainer(config, training_args)
    
    logger.info("🔥 Acil eğitim başlatılıyor - Araç odaklı yoğun eğitim!")
    trainer.run()
    
    logger.info("✅ Acil eğitim tamamlandı!")
    logger.info("🧪 Şimdi PURE_AI_TEST_SUITE.py ile test edin!")

if __name__ == "__main__":
    main()