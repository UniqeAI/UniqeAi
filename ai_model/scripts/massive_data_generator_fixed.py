"""
🚀 MASSIVE TELEKOM DIALOGS GENERATOR - FIXED EDITION
====================================================

Bu script, tool call problemlerini çözen ve modular_generator ile entegre olan
büyük ölçekli veri üreticisidir.

📋 ÖZELLİKLER:
• Tool call validation hatalarını çözer
• Modular generator entegrasyonu
• Büyük ölçekli veri üretimi (1000+ seed)
• Paralel işleme desteği
• Gelişmiş mock data generation
"""

import json
import csv
import random
import re
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed

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

class MassiveDataGeneratorFixed:
    """
    🚀 FIXED Büyük Ölçekli Telekom Diyalog Üreticisi
    
    Tool call problemlerini çözen ve modular_generator ile entegre olan büyük ölçekli sınıf.
    """
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.output_file = self.project_root / "ai_model" / "data" / "massive_telekom_dialogs_fixed.jsonl"
        
        # Gelişmiş paraphrasing templates
        self.advanced_templates = {
            "greetings": [
                "Merhaba", "Selam", "İyi günler", "Günaydın", "Merhabalar",
                "Hoş geldiniz", "Nasılsınız", "Merhaba, size nasıl yardımcı olabilirim?",
                "Selamlar", "İyi akşamlar", "Hoş buldum", "Merhaba efendim",
                "Günaydın, nasılsınız?", "İyi günler, size nasıl yardımcı olabilirim?"
            ],
            "farewells": [
                "Başka bir konuda yardımcı olabilir miyim?", "Başka bir sorunuz var mı?",
                "Başka bir konuda destek almak ister misiniz?", "Başka bir işleminiz var mı?",
                "Başka bir konuda yardıma ihtiyacınız var mı?", "Başka bir konuda sorunuz var mı?",
                "Başka bir konuda yardım ister misiniz?", "Başka bir konuda destek almak istiyor musunuz?",
                "Başka bir konuda işleminiz var mı?", "Başka bir konuda yardıma ihtiyacınız var mı?"
            ],
            "processing": [
                "Kontrol ediyorum", "Bakıyorum", "İnceliyorum", "Araştırıyorum",
                "Kontrol ediyorum", "Bilgilerinizi kontrol ediyorum", "Sistemde arıyorum",
                "Sistemde kontrol ediyorum", "Bilgilerinizi inceliyorum", "Sistemde araştırıyorum",
                "Kontrol ediyorum efendim", "Bakıyorum hemen", "İnceliyorum şimdi",
                "Araştırıyorum sistemde", "Kontrol ediyorum bilgilerinizi"
            ]
        }
        
        # Gelişmiş augmentation patterns
        self.advanced_augmentation = {
            "punctuation": [".", "!", "?", "...", "!!", "??", "?!", "!?", "..", "..."],
            "noise_words": [
                "efendim", "şey", "yani", "işte", "bakın", "anlıyorsunuz",
                "efendim", "şey", "yani", "işte", "bakın", "anlıyorsunuz",
                "efendim", "şey", "yani", "işte", "bakın", "anlıyorsunuz"
            ],
            "fillers": [
                "bir dakika", "bir saniye", "hemen", "şimdi", "az önce",
                "biraz önce", "az önce", "hemen bakıyorum", "şimdi bakıyorum",
                "hemen kontrol ediyorum", "şimdi kontrol ediyorum", "az önce kontrol ettim",
                "biraz önce baktım", "hemen inceliyorum", "şimdi araştırıyorum"
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
        
        logger.info("🚀 MassiveDataGeneratorFixed başlatıldı")

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

    def generate_massive_seed_dialogs(self, num_seeds: int = 1000) -> List[Dict[str, Any]]:
        """Büyük miktarda seed diyalog üretir"""
        
        # Temel senaryo kalıpları
        base_scenarios = {
            "billing": [
                ("Fatura bilgilerimi öğrenmek istiyorum", "Fatura bilgilerinizi kontrol ediyorum"),
                ("Faturamı ödemek istiyorum", "Fatura ödeme işleminizi yapıyorum"),
                ("Geçmiş faturalarımı görmek istiyorum", "Geçmiş faturalarınızı listeliyorum"),
                ("Fatura ödeme planı yapmak istiyorum", "Taksitli ödeme planı oluşturuyorum"),
                ("Fatura tarihini değiştirmek istiyorum", "Fatura tarihini güncelliyorum"),
                ("Otomatik ödeme kurmak istiyorum", "Otomatik ödeme sistemini kuruyorum"),
                ("Fatura ödememi yaptım ama görünmüyor", "Ödemenizi kontrol ediyorum"),
                ("Fatura indirimi var mı?", "Mevcut indirimleri kontrol ediyorum"),
                ("Fatura şikayetim var", "Şikayetinizi kayıt altına alıyorum"),
                ("Fatura detaylarını görmek istiyorum", "Fatura detaylarını açıklıyorum")
            ],
            "technical_support": [
                ("İnternet hızım yavaş", "İnternet hızınızı test ediyorum"),
                ("İnternet bağlantım kesiliyor", "Bağlantı sorununuzu kontrol ediyorum"),
                ("SMS gönderemiyorum", "SMS sorununuzu inceliyorum"),
                ("Arama yapamıyorum", "Arama sorununuzu kontrol ediyorum"),
                ("Sinyal sorunu yaşıyorum", "Sinyal durumunuzu kontrol ediyorum"),
                ("Modem sorunum var", "Modem sorununuzu inceliyorum"),
                ("Arıza kaydım var", "Arıza kaydınızı kontrol ediyorum"),
                ("Teknik destek istiyorum", "Teknik destek ekibini yönlendiriyorum"),
                ("İnternet kotam bitti", "Kota durumunuzu kontrol ediyorum"),
                ("Hız testi yapmak istiyorum", "Hız testini başlatıyorum")
            ],
            "package_management": [
                ("Paketimi değiştirmek istiyorum", "Paket değişikliği yapıyorum"),
                ("Yeni paket almak istiyorum", "Mevcut paketleri gösteriyorum"),
                ("Paket iptal etmek istiyorum", "Paket iptali işlemini yapıyorum"),
                ("Paket fiyatlarını öğrenmek istiyorum", "Paket fiyatlarını listeliyorum"),
                ("Roaming aktif etmek istiyorum", "Roaming hizmetinizi aktif ediyorum"),
                ("Kalan dakikamı öğrenmek istiyorum", "Kalan dakikanızı kontrol ediyorum"),
                ("Paket detaylarını görmek istiyorum", "Paket detaylarını açıklıyorum"),
                ("Paket yenileme yapmak istiyorum", "Paket yenileme işlemini yapıyorum"),
                ("Paket karşılaştırması yapmak istiyorum", "Paketleri karşılaştırıyorum"),
                ("Özel paket teklifi istiyorum", "Özel teklifleri kontrol ediyorum")
            ],
            "account_management": [
                ("Hesap bilgilerimi güncellemek istiyorum", "Hesap bilgilerinizi güncelliyorum"),
                ("Telefon numaramı değiştirmek istiyorum", "Numara değişikliği yapıyorum"),
                ("Hat dondurma işlemi yapmak istiyorum", "Hat dondurma işlemini yapıyorum"),
                ("Hat transfer işlemi yapmak istiyorum", "Hat transfer işlemini başlatıyorum"),
                ("Hesap şifremi değiştirmek istiyorum", "Şifre değişikliği yapıyorum"),
                ("Hesap kapatmak istiyorum", "Hesap kapatma işlemini başlatıyorum"),
                ("Hesap bilgilerimi görmek istiyorum", "Hesap bilgilerinizi gösteriyorum"),
                ("Hat çalındı, ne yapmalıyım?", "Hemen hat dondurma işlemi yapıyorum"),
                ("Hesap güvenliği için ne yapabilirim?", "Güvenlik önerilerini açıklıyorum"),
                ("Hesap erişim sorunu yaşıyorum", "Erişim sorununuzu çözüyorum")
            ],
            "advanced_services": [
                ("5G kapsama alanında mıyım?", "5G kapsama alanınızı kontrol ediyorum"),
                ("Acil durum servisi aktif etmek istiyorum", "Acil durum servisinizi aktif ediyorum"),
                ("Kültürel tercihlerimi güncellemek istiyorum", "Kültürel tercihlerinizi güncelliyorum"),
                ("Özel hizmet paketi almak istiyorum", "Özel hizmet paketlerini gösteriyorum"),
                ("Kurumsal hizmet teklifi istiyorum", "Kurumsal teklifleri hazırlıyorum"),
                ("VIP müşteri hizmetleri istiyorum", "VIP hizmetlerinizi aktif ediyorum"),
                ("Özel teknik destek istiyorum", "Özel teknik desteği yönlendiriyorum"),
                ("Gelişmiş güvenlik hizmeti istiyorum", "Güvenlik hizmetlerini açıklıyorum"),
                ("Özel veri paketi istiyorum", "Özel veri paketlerini gösteriyorum"),
                ("Premium hizmet paketi almak istiyorum", "Premium paketleri listeliyorum")
            ]
        }
        
        seed_dialogs = []
        
        for i in range(1, num_seeds + 1):
            # Rastgele senaryo seç
            scenario_type = random.choice(list(base_scenarios.keys()))
            scenario_templates = base_scenarios[scenario_type]
            
            # Rastgele template seç
            input_template, response_template = random.choice(scenario_templates)
            
            # Template'i varyasyonlarla zenginleştir
            user_input = self._vary_template(input_template)
            response_text = self._vary_template(response_template)
            
            # Karmaşıklık seviyesi belirle
            complexity = random.choice(["basic", "medium", "advanced"])
            
            seed_dialogs.append({
                'id': i,
                'input_text': user_input,
                'response_text': response_text,
                'scenario_type': scenario_type,
                'complexity_level': complexity
            })
        
        logger.info(f"✅ {len(seed_dialogs)} adet seed diyalog üretildi")
        return seed_dialogs

    def _vary_template(self, template: str) -> str:
        """Template'i çeşitli varyasyonlarla zenginleştirir"""
        variations = [
            template,
            f"{random.choice(self.advanced_templates['greetings'])}, {template}",
            f"{template} {random.choice(['efendim', 'lütfen', 'acaba', 'belki'])}",
            f"{template} {random.choice(['olabilir mi?', 'mümkün mü?', 'yapabilir misiniz?'])}",
            f"{random.choice(['Merhaba, ', 'Selam, ', 'İyi günler, '])}{template}",
            f"{template} {random.choice(['yardımcı olur musunuz?', 'bakabilir misiniz?', 'kontrol edebilir misiniz?'])}"
        ]
        return random.choice(variations)

    def generate_massive_dataset(self, num_seeds: int = 1000, variants_per_seed: int = 20) -> List[Dict[str, Any]]:
        """Büyük ölçekli dataset üretir"""
        logger.info(f"🚀 Massive dataset üretimi başlatılıyor...")
        logger.info(f"📊 {num_seeds} seed × {variants_per_seed} varyant = {num_seeds * variants_per_seed} toplam diyalog")
        
        # Seed diyalogları üret
        seed_dialogs = self.generate_massive_seed_dialogs(num_seeds)
        
        # Paralel işleme için chunk'lara böl
        chunk_size = 100
        chunks = [seed_dialogs[i:i + chunk_size] for i in range(0, len(seed_dialogs), chunk_size)]
        
        all_dialogues = []
        
        # Her chunk'ı paralel işle
        with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
            futures = []
            for chunk in chunks:
                future = executor.submit(self._process_chunk, chunk, variants_per_seed)
                futures.append(future)
            
            # Sonuçları topla
            for future in as_completed(futures):
                try:
                    chunk_dialogues = future.result()
                    all_dialogues.extend(chunk_dialogues)
                    logger.info(f"✅ Chunk işlendi: {len(chunk_dialogues)} diyalog")
                except Exception as e:
                    logger.error(f"❌ Chunk işlenirken hata: {e}")
        
        logger.info(f"✅ Toplam {len(all_dialogues)} adet diyalog üretildi")
        return all_dialogues

    def _process_chunk(self, seed_chunk: List[Dict[str, Any]], variants_per_seed: int) -> List[Dict[str, Any]]:
        """Bir chunk'ı işler (paralel işleme için)"""
        chunk_dialogues = []
        
        for seed_dialog in seed_chunk:
            # Her seed için çok sayıda varyant üret
            for i in range(variants_per_seed):
                # Input ve response varyantları üret
                input_variant = self._generate_advanced_variant(seed_dialog['input_text'])
                response_variant = self._generate_advanced_variant(seed_dialog['response_text'])
                
                # Tool call olasılığı
                use_tool_call = random.random() < 0.6  # %60 olasılık
                
                if use_tool_call:
                    dialogue = self._create_advanced_tool_call_dialogue(
                        seed_dialog['scenario_type'],
                        input_variant,
                        response_variant
                    )
                else:
                    dialogue = self._create_simple_dialogue(input_variant, response_variant)
                
                # Gelişmiş augmentation uygula
                dialogue = self._apply_advanced_augmentation(dialogue)
                
                # Metadata ekle
                dialogue.update({
                    "id": f"{seed_dialog['id']}_{i+1}",
                    "seed_id": seed_dialog['id'],
                    "scenario_type": seed_dialog['scenario_type'],
                    "complexity_level": seed_dialog['complexity_level'],
                    "variant_number": i + 1,
                    "has_tool_call": use_tool_call,
                    "generated_at": datetime.now().isoformat(),
                    "augmentation_applied": True,
                    "massive_generation": True,
                    "generator_version": "fixed"
                })
                
                chunk_dialogues.append(dialogue)
        
        return chunk_dialogues

    def _generate_advanced_variant(self, text: str) -> str:
        """Gelişmiş varyant üretimi"""
        variant = text
        
        # Greeting değişiklikleri
        for greeting in self.advanced_templates["greetings"]:
            if any(g in variant for g in ["Merhaba", "Selam", "İyi günler"]):
                variant = re.sub(r'(Merhaba|Selam|İyi günler)[^!]*', greeting, variant, count=1)
                break
        
        # Processing değişiklikleri
        for processing in self.advanced_templates["processing"]:
            if any(p in variant for p in ["Kontrol ediyorum", "Bakıyorum", "İnceliyorum"]):
                variant = re.sub(r'(Kontrol ediyorum|Bakıyorum|İnceliyorum)', processing, variant, count=1)
                break
        
        # Noktalama varyasyonları
        if random.random() < 0.4:
            variant = variant.replace(".", random.choice(self.advanced_augmentation["punctuation"]))
        
        # Gürültü kelimeleri ekleme
        if random.random() < 0.3:
            noise_word = random.choice(self.advanced_augmentation["noise_words"])
            variant = f"{noise_word}, {variant}"
        
        # Filler phrases ekleme
        if random.random() < 0.25:
            filler = random.choice(self.advanced_augmentation["fillers"])
            variant = f"{filler}, {variant}"
        
        return variant

    def _create_advanced_tool_call_dialogue(self, scenario_type: str, user_input: str, response_text: str) -> Dict[str, Any]:
        """Gelişmiş tool call diyalogu oluşturur (düzeltilmiş)"""
        # Scenario type'a göre uygun API fonksiyonunu seç
        available_functions = self.api_function_mappings.get(scenario_type, [])
        if not available_functions:
            return self._create_simple_dialogue(user_input, response_text)
        
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
            return self._create_simple_dialogue(user_input, response_text)

    def _create_simple_dialogue(self, user_input: str, response_text: str) -> Dict[str, Any]:
        """Basit diyalog oluşturur"""
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

    def _apply_advanced_augmentation(self, dialogue: Dict[str, Any]) -> Dict[str, Any]:
        """Gelişmiş augmentation uygular"""
        augmented_dialogue = dialogue.copy()
        
        for turn in augmented_dialogue["donguler"]:
            if turn["rol"] == "kullanici":
                content = turn["icerik"]
                
                # Token masking
                if random.random() < 0.15:
                    words = content.split()
                    if len(words) > 3:
                        mask_index = random.randint(0, len(words) - 1)
                        words[mask_index] = "[MASK]"
                        content = " ".join(words)
                
                # Noktalama varyasyonları
                if random.random() < 0.2:
                    content = content.replace(".", random.choice(self.advanced_augmentation["punctuation"]))
                
                # Gürültü ekleme
                if random.random() < 0.15:
                    noise_word = random.choice(self.advanced_augmentation["noise_words"])
                    content = f"{noise_word}, {content}"
                
                turn["icerik"] = content
            
            elif turn["rol"] == "asistan":
                content = turn["icerik"]
                
                # Filler phrases ekleme
                if random.random() < 0.15:
                    filler = random.choice(self.advanced_augmentation["fillers"])
                    content = f"{filler}, {content}"
                
                # Noktalama varyasyonları
                if random.random() < 0.15:
                    content = content.replace(".", random.choice(self.advanced_augmentation["punctuation"]))
                
                turn["icerik"] = content
        
        return augmented_dialogue

    def save_massive_dataset(self, dataset: List[Dict[str, Any]]):
        """Büyük dataset'i kaydeder"""
        # Output dizinini oluştur
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # JSON Lines formatında kaydet
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for dialogue in dataset:
                f.write(json.dumps(dialogue, ensure_ascii=False) + '\n')
        
        logger.info(f"💾 Massive dataset kaydedildi: {self.output_file}")
        logger.info(f"📊 Toplam {len(dataset)} adet diyalog")

def main():
    """Ana çalıştırma fonksiyonu"""
    logger.info("🚀 Massive Telekom Dialogs Generator Fixed başlatılıyor...")
    
    # Generator'ı başlat
    generator = MassiveDataGeneratorFixed()
    
    # Büyük dataset üret (1000 seed × 20 varyant = 20,000 diyalog)
    dataset = generator.generate_massive_dataset(
        num_seeds=1000,
        variants_per_seed=20
    )
    
    if not dataset:
        logger.error("❌ Massive dataset üretilemedi!")
        return
    
    # Dataset'i kaydet
    generator.save_massive_dataset(dataset)
    
    logger.info("🎉 Massive Telekom Dialogs Generator Fixed tamamlandı!")
    logger.info(f"📁 Çıktı: {generator.output_file}")
    logger.info(f"📊 Toplam: {len(dataset)} diyalog")

if __name__ == "__main__":
    main() 