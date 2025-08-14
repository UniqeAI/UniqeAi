"""
🚀 TELEKOM DIALOGS GENERATOR - FIXED EDITION
============================================

Bu script, tool call problemlerini çözen ve modular_generator ile entegre olan
düzeltilmiş versiyondur.

📋 ÖZELLİKLER:
• Tool call validation hatalarını çözer
• Modular generator entegrasyonu
• Gelişmiş mock data generation
• Schema compliance
• JSON Lines output format
"""

import json
import csv
import random
import re
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import logging

# Import modular_generator schema
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "modular_generator"))
from telekom_api_schema import (
    API_MAP, REQUEST_MODELS, RESPONSE_MODELS,
    get_request_model, get_response_model,
    create_mock_request, create_mock_response,
    validate_api_function, get_all_function_names
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TelekomDialogsGeneratorFixed:
    """
    🚀 FIXED Telekom Diyalog Üreticisi
    
    Tool call problemlerini çözen ve modular_generator ile entegre olan sınıf.
    """
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.seed_file = self.project_root / "ai_model" / "data" / "dialogs_seed.csv"
        self.output_file = self.project_root / "ai_model" / "data" / "telekom_dialogs_fixed.jsonl"
        
        # Paraphrasing templates
        self.paraphrasing_templates = {
            "greeting": [
                "Merhaba", "Selam", "İyi günler", "Günaydın", "Merhabalar",
                "Hoş geldiniz", "Nasılsınız", "Merhaba, size nasıl yardımcı olabilirim?"
            ],
            "farewell": [
                "Başka bir konuda yardımcı olabilir miyim?", "Başka bir sorunuz var mı?",
                "Başka bir konuda destek almak ister misiniz?", "Başka bir işleminiz var mı?",
                "Başka bir konuda yardıma ihtiyacınız var mı?"
            ],
            "confirmation": [
                "Tamam", "Anladım", "Evet", "Tabii", "Elbette", "Kesinlikle",
                "Tabii ki", "Evet, tabii", "Anladım, devam edin"
            ],
            "processing": [
                "Kontrol ediyorum", "Bakıyorum", "İnceliyorum", "Araştırıyorum",
                "Kontrol ediyorum", "Bilgilerinizi kontrol ediyorum", "Sistemde arıyorum"
            ]
        }
        
        # Augmentation patterns
        self.augmentation_patterns = {
            "punctuation_variations": [".", "!", "?", "...", "!!", "??"],
            "noise_words": ["efendim", "şey", "yani", "işte", "bakın", "anlıyorsunuz"],
            "filler_phrases": [
                "bir dakika", "bir saniye", "hemen", "şimdi", "az önce",
                "biraz önce", "az önce", "hemen bakıyorum"
            ]
        }
        
        # API function mappings for tool calls (düzeltilmiş)
        self.api_function_mappings = {
            "billing": ["get_current_bill", "get_past_bills", "get_payment_history"],
            "technical_support": ["check_network_status", "test_internet_speed"],
            "package_management": ["get_customer_package", "get_available_packages"],
            "account_management": ["get_customer_profile"],
            "advanced_services": ["check_5g_coverage"]
        }
        
        # Mock data generators for complex fields
        self.mock_data_generators = {
            "user_id": lambda: random.randint(1000, 999999),
            "bill_id": lambda: f"F-2024-{random.randint(100000, 999999)}",
            "ticket_id": lambda: f"TKT-2024-{random.randint(100000, 999999)}",
            "transaction_id": lambda: f"TXN-2024-{random.randint(100000, 999999)}",
            "amount": lambda: round(random.uniform(10.0, 500.0), 2),
            "limit": lambda: random.randint(5, 50),
            "region": lambda: random.choice(["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"]),
            "location": lambda: random.choice(["İstanbul Merkez", "Ankara Merkez", "İzmir Merkez"]),
            "issue_description": lambda: random.choice([
                "İnternet hızı yavaş", "Bağlantı sorunu", "Sinyal problemi",
                "Fatura ödeme sorunu", "Paket değişikliği"
            ]),
            "category": lambda: random.choice([
                "internet_speed", "connection_issue", "billing", "package_change"
            ]),
            "priority": lambda: random.choice(["low", "medium", "high"]),
            "status": lambda: random.choice([True, False]),
            "emergency_type": lambda: random.choice(["medical", "fire", "police"]),
            "package_name": lambda: random.choice([
                "Mega İnternet", "Öğrenci Dostu Tarife", "Süper Konuşma"
            ]),
            "new_package_name": lambda: random.choice([
                "Mega İnternet", "Öğrenci Dostu Tarife", "Süper Konuşma"
            ]),
            "reason": lambda: random.choice([
                "geçici durdurma", "ödeme sorunu", "müşteri talebi"
            ]),
            "method": lambda: random.choice(["credit_card", "bank_transfer", "digital_wallet"]),
            "payment_method": lambda: random.choice(["credit_card", "bank_transfer", "digital_wallet"]),
            "contact_type": lambda: random.choice(["phone", "email", "address"]),
            "new_value": lambda: random.choice([
                "+905551234567", "test@example.com", "İstanbul, Kadıköy"
            ])
        }
        
        logger.info("🚀 TelekomDialogsGeneratorFixed başlatıldı")
        logger.info(f"📁 Seed dosyası: {self.seed_file}")
        logger.info(f"📁 Çıktı dosyası: {self.output_file}")

    def load_seed_dialogs(self) -> List[Dict[str, Any]]:
        """Seed diyalogları CSV dosyasından yükler"""
        if not self.seed_file.exists():
            logger.warning(f"Seed dosyası bulunamadı: {self.seed_file}")
            return []
        
        dialogs = []
        with open(self.seed_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dialogs.append({
                    'id': int(row['id']),
                    'input_text': row['input_text'],
                    'response_text': row['response_text'],
                    'scenario_type': row['scenario_type'],
                    'complexity_level': row['complexity_level']
                })
        
        logger.info(f"✅ {len(dialogs)} adet seed diyalog yüklendi")
        return dialogs

    def generate_paraphrase_variants(self, text: str, num_variants: int = 5) -> List[str]:
        """Metin için paraphrase varyantları üretir"""
        variants = [text]  # Orijinal metni de dahil et
        
        for _ in range(num_variants - 1):
            variant = text
            
            # Greeting değişiklikleri
            for greeting in self.paraphrasing_templates["greeting"]:
                if any(g in variant for g in ["Merhaba", "Selam", "İyi günler"]):
                    variant = re.sub(r'(Merhaba|Selam|İyi günler)[^!]*', greeting, variant, count=1)
                    break
            
            # Processing değişiklikleri
            for processing in self.paraphrasing_templates["processing"]:
                if any(p in variant for p in ["Kontrol ediyorum", "Bakıyorum", "İnceliyorum"]):
                    variant = re.sub(r'(Kontrol ediyorum|Bakıyorum|İnceliyorum)', processing, variant, count=1)
                    break
            
            # Farewell değişiklikleri
            for farewell in self.paraphrasing_templates["farewell"]:
                if any(f in variant for f in ["Başka bir konuda yardımcı olabilir miyim?", "Başka bir sorunuz var mı?"]):
                    variant = re.sub(r'(Başka bir konuda yardımcı olabilir miyim\?|Başka bir sorunuz var mı\?)', farewell, variant, count=1)
                    break
            
            # Noktalama değişiklikleri
            if random.random() < 0.3:
                variant = variant.replace(".", random.choice(self.augmentation_patterns["punctuation_variations"]))
            
            # Gürültü kelimeleri ekleme
            if random.random() < 0.2:
                noise_word = random.choice(self.augmentation_patterns["noise_words"])
                variant = f"{noise_word}, {variant}"
            
            # Filler phrases ekleme
            if random.random() < 0.15:
                filler = random.choice(self.augmentation_patterns["filler_phrases"])
                variant = f"{filler}, {variant}"
            
            if variant not in variants:
                variants.append(variant)
        
        return variants[:num_variants]

    def create_mock_data_for_function(self, function_name: str, model_type: str = "request") -> Dict[str, Any]:
        """Fonksiyon için mock data oluşturur"""
        try:
            if model_type == "request":
                model_class = get_request_model(function_name)
            else:
                model_class = get_response_model(function_name)
            
            mock_data = {}
            
            # Her field için uygun mock data oluştur
            for field_name, field_info in model_class.model_fields.items():
                if field_name in self.mock_data_generators:
                    mock_data[field_name] = self.mock_data_generators[field_name]()
                elif hasattr(field_info, 'example') and field_info.example is not None:
                    mock_data[field_name] = field_info.example
                elif field_info.annotation == int:
                    mock_data[field_name] = random.randint(1, 1000)
                elif field_info.annotation == float:
                    mock_data[field_name] = round(random.uniform(1.0, 100.0), 2)
                elif field_info.annotation == str:
                    mock_data[field_name] = f"mock_{field_name}_{random.randint(1, 1000)}"
                elif field_info.annotation == bool:
                    mock_data[field_name] = random.choice([True, False])
                elif field_info.annotation == List:
                    # Basit liste oluştur
                    if "str" in str(field_info.annotation):
                        mock_data[field_name] = [f"item_{i}" for i in range(3)]
                    else:
                        mock_data[field_name] = []
                elif field_info.annotation == Dict:
                    mock_data[field_name] = {"key": "value"}
                else:
                    # Enum veya complex type için default değer
                    mock_data[field_name] = None
            
            return mock_data
            
        except Exception as e:
            logger.warning(f"Mock data oluşturulurken hata: {e}")
            return {"user_id": 12345}  # Fallback

    def create_tool_call_dialogue(self, scenario_type: str, user_input: str, response_text: str) -> Dict[str, Any]:
        """Tool call içeren diyalog oluşturur (düzeltilmiş)"""
        # Scenario type'a göre uygun API fonksiyonunu seç
        available_functions = self.api_function_mappings.get(scenario_type, [])
        if not available_functions:
            return self.create_simple_dialogue(user_input, response_text)
        
        selected_function = random.choice(available_functions)
        
        try:
            # Mock request data oluştur
            request_data = self.create_mock_data_for_function(selected_function, "request")
            mock_request = create_mock_request(selected_function, **request_data)
            
            # Mock response data oluştur
            response_data = self.create_mock_data_for_function(selected_function, "response")
            mock_response = create_mock_response(selected_function, **response_data)
            
            # Tool call parametrelerini hazırla
            tool_call_params = {}
            for field_name, field_value in mock_request.model_dump().items():
                if isinstance(field_value, (int, str, float, bool)) and field_value is not None:
                    tool_call_params[field_name] = field_value
            
            # Diyalog yapısını oluştur
            dialogue = {
                "donguler": [
                    {
                        "rol": "kullanici",
                        "icerik": user_input
                    },
                    {
                        "rol": "asistan",
                        "icerik": f"Bu işlem için {selected_function} fonksiyonunu çağırıyorum.",
                        "arac_cagrilari": [
                            {
                                "fonksiyon": selected_function,
                                "parametreler": tool_call_params
                            }
                        ]
                    },
                    {
                        "rol": "arac",
                        "icerik": json.dumps(mock_response.model_dump(), ensure_ascii=False)
                    },
                    {
                        "rol": "asistan",
                        "icerik": response_text
                    }
                ]
            }
            
            return dialogue
            
        except Exception as e:
            logger.warning(f"Tool call oluşturulurken hata: {e}")
            return self.create_simple_dialogue(user_input, response_text)

    def create_simple_dialogue(self, user_input: str, response_text: str) -> Dict[str, Any]:
        """Basit diyalog oluşturur (tool call olmadan)"""
        return {
            "donguler": [
                {
                    "rol": "kullanici",
                    "icerik": user_input
                },
                {
                    "rol": "asistan",
                    "icerik": response_text
                }
            ]
        }

    def apply_data_augmentation(self, dialogue: Dict[str, Any]) -> Dict[str, Any]:
        """Diyaloga gerçek zamanlı augmentation uygular"""
        augmented_dialogue = dialogue.copy()
        
        for turn in augmented_dialogue["donguler"]:
            if turn["rol"] == "kullanici":
                # Kullanıcı metnine augmentation
                content = turn["icerik"]
                
                # Token masking (10% olasılıkla)
                if random.random() < 0.1:
                    words = content.split()
                    if len(words) > 3:
                        mask_index = random.randint(0, len(words) - 1)
                        words[mask_index] = "[MASK]"
                        content = " ".join(words)
                
                # Noktalama varyasyonları
                if random.random() < 0.15:
                    content = content.replace(".", random.choice(self.augmentation_patterns["punctuation_variations"]))
                
                # Gürültü ekleme
                if random.random() < 0.1:
                    noise_word = random.choice(self.augmentation_patterns["noise_words"])
                    content = f"{noise_word}, {content}"
                
                turn["icerik"] = content
            
            elif turn["rol"] == "asistan":
                # Asistan metnine augmentation
                content = turn["icerik"]
                
                # Filler phrases ekleme
                if random.random() < 0.1:
                    filler = random.choice(self.augmentation_patterns["filler_phrases"])
                    content = f"{filler}, {content}"
                
                # Noktalama varyasyonları
                if random.random() < 0.1:
                    content = content.replace(".", random.choice(self.augmentation_patterns["punctuation_variations"]))
                
                turn["icerik"] = content
        
        return augmented_dialogue

    def generate_dataset(self, num_variants_per_seed: int = 10, apply_augmentation: bool = True) -> List[Dict[str, Any]]:
        """Ana dataset üretim fonksiyonu"""
        logger.info(f"🚀 Dataset üretimi başlatılıyor...")
        logger.info(f"📊 Seed başına {num_variants_per_seed} varyant")
        logger.info(f"🔧 Augmentation: {'Aktif' if apply_augmentation else 'Pasif'}")
        
        # Seed diyalogları yükle
        seed_dialogs = self.load_seed_dialogs()
        if not seed_dialogs:
            logger.error("❌ Seed diyaloglar yüklenemedi!")
            return []
        
        generated_dataset = []
        
        for seed_dialog in seed_dialogs:
            logger.info(f"🔄 Seed #{seed_dialog['id']} işleniyor: {seed_dialog['scenario_type']}")
            
            # Input text için paraphrase varyantları
            input_variants = self.generate_paraphrase_variants(
                seed_dialog['input_text'], 
                num_variants_per_seed
            )
            
            # Response text için paraphrase varyantları
            response_variants = self.generate_paraphrase_variants(
                seed_dialog['response_text'], 
                num_variants_per_seed
            )
            
            # Her varyant için diyalog oluştur
            for i, (input_variant, response_variant) in enumerate(zip(input_variants, response_variants)):
                # Tool call olasılığı (scenario type'a göre)
                use_tool_call = random.random() < 0.6  # %60 olasılık
                
                if use_tool_call:
                    dialogue = self.create_tool_call_dialogue(
                        seed_dialog['scenario_type'],
                        input_variant,
                        response_variant
                    )
                else:
                    dialogue = self.create_simple_dialogue(input_variant, response_variant)
                
                # Augmentation uygula
                if apply_augmentation:
                    dialogue = self.apply_data_augmentation(dialogue)
                
                # Metadata ekle
                dialogue.update({
                    "id": f"{seed_dialog['id']}_{i+1}",
                    "seed_id": seed_dialog['id'],
                    "scenario_type": seed_dialog['scenario_type'],
                    "complexity_level": seed_dialog['complexity_level'],
                    "variant_number": i + 1,
                    "has_tool_call": use_tool_call,
                    "generated_at": datetime.now().isoformat(),
                    "augmentation_applied": apply_augmentation,
                    "generator_version": "fixed"
                })
                
                generated_dataset.append(dialogue)
        
        logger.info(f"✅ Toplam {len(generated_dataset)} adet diyalog üretildi")
        return generated_dataset

    def save_dataset(self, dataset: List[Dict[str, Any]], output_path: Optional[Path] = None):
        """Dataset'i JSON Lines formatında kaydeder"""
        if output_path is None:
            output_path = self.output_file
        
        # Output dizinini oluştur
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for dialogue in dataset:
                f.write(json.dumps(dialogue, ensure_ascii=False) + '\n')
        
        logger.info(f"💾 Dataset kaydedildi: {output_path}")
        logger.info(f"📊 Toplam {len(dataset)} adet diyalog")

    def validate_dataset_schema(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Dataset'in şema uyumluluğunu kontrol eder"""
        validation_results = {
            "total_dialogues": len(dataset),
            "valid_dialogues": 0,
            "invalid_dialogues": 0,
            "errors": [],
            "tool_call_count": 0,
            "simple_dialogue_count": 0
        }
        
        for i, dialogue in enumerate(dataset):
            try:
                # Temel yapı kontrolü
                if "donguler" not in dialogue:
                    raise ValueError("'donguler' alanı eksik")
                
                if not isinstance(dialogue["donguler"], list):
                    raise ValueError("'donguler' liste olmalı")
                
                # Her dönüş kontrolü
                for j, turn in enumerate(dialogue["donguler"]):
                    if "rol" not in turn or "icerik" not in turn:
                        raise ValueError(f"Dönüş #{j+1}: 'rol' veya 'icerik' eksik")
                    
                    if turn["rol"] not in ["kullanici", "asistan", "arac"]:
                        raise ValueError(f"Dönüş #{j+1}: Geçersiz rol: {turn['rol']}")
                    
                    # Tool call kontrolü
                    if turn["rol"] == "asistan" and "arac_cagrilari" in turn:
                        validation_results["tool_call_count"] += 1
                        for tool_call in turn["arac_cagrilari"]:
                            if "fonksiyon" not in tool_call:
                                raise ValueError(f"Tool call: 'fonksiyon' alanı eksik")
                            
                            # API fonksiyon geçerliliği kontrolü
                            if not validate_api_function(tool_call["fonksiyon"]):
                                raise ValueError(f"Geçersiz API fonksiyonu: {tool_call['fonksiyon']}")
                
                validation_results["valid_dialogues"] += 1
                if "arac_cagrilari" not in str(dialogue):
                    validation_results["simple_dialogue_count"] += 1
                
            except Exception as e:
                validation_results["invalid_dialogues"] += 1
                validation_results["errors"].append(f"Diyalog #{i+1}: {str(e)}")
        
        return validation_results

def main():
    """Ana çalıştırma fonksiyonu"""
    logger.info("🚀 Telekom Dialogs Generator Fixed başlatılıyor...")
    
    # Generator'ı başlat
    generator = TelekomDialogsGeneratorFixed()
    
    # Dataset üret
    dataset = generator.generate_dataset(
        num_variants_per_seed=10,
        apply_augmentation=True
    )
    
    if not dataset:
        logger.error("❌ Dataset üretilemedi!")
        return
    
    # Şema doğrulaması
    validation_results = generator.validate_dataset_schema(dataset)
    
    logger.info("📊 Validation Sonuçları:")
    logger.info(f"   Toplam Diyalog: {validation_results['total_dialogues']}")
    logger.info(f"   Geçerli: {validation_results['valid_dialogues']}")
    logger.info(f"   Geçersiz: {validation_results['invalid_dialogues']}")
    logger.info(f"   Tool Call: {validation_results['tool_call_count']}")
    logger.info(f"   Basit Diyalog: {validation_results['simple_dialogue_count']}")
    
    if validation_results['errors']:
        logger.warning("⚠️ Validation Hataları:")
        for error in validation_results['errors'][:5]:  # İlk 5 hatayı göster
            logger.warning(f"   {error}")
    
    # Dataset'i kaydet
    generator.save_dataset(dataset)
    
    logger.info("🎉 Telekom Dialogs Generator Fixed tamamlandı!")
    logger.info(f"📁 Çıktı: {generator.output_file}")

if __name__ == "__main__":
    main() 