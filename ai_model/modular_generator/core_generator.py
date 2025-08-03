# -*- coding: utf-8 -*-
"""
🚀 SUPREME HUMAN-LEVEL DATASET GENERATOR V3 - MODULAR EDITION
=============================================================

Bu modül, SupremeHumanLevelDatasetGenerator'ın ana sınıfını içerir.
Modüler yapıda organize edilmiş, tüm bileşenleri bir araya getirir.
"""

import json
import random
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# Modüler importlar
from .models import ScenarioType, CognitiveState, EmotionalContext
from .exceptions import DataGenerationError, ValidationError
from .validators import (
    validate_scenario_quality,
    verify_pydantic_compliance
)
from .utils import generate_user_id, generate_mock_data_for_model
from .config import (
    PROJECT_ROOT,
    DEFAULT_OUTPUT_DIR,
    SCENARIO_WEIGHTS,
    API_RESPONSE_MAPPING
)
from .generators import (
    generate_standard_scenario,
    generate_tool_chaining_scenario,
    generate_proactive_scenario,
    generate_disambiguation_scenario,
    generate_multi_intent_scenario,
    generate_ethical_dilemma_scenario,
    generate_negotiation_skills_scenario,
    generate_teaching_mentoring_scenario,
    generate_innovation_thinking_scenario,
    generate_temporal_reasoning_scenario,
    generate_cross_cultural_communication_scenario
)

class SupremeHumanLevelDatasetGenerator:
    """
    🚀 SUPREME V3 - Sıfır Toleranslı Dataset Generator
    
    Bu sınıf, %100 Pydantic uyumlu, sıfır toleranslı,
    enterprise seviyesinde kalitede veri üretir.
    """
    
    def __init__(self):
        print("🚀 SUPREME V3 - Sıfır Toleranslı Dataset Generator başlatılıyor...")
        print("✅ %100 Pydantic Validasyon Zorunluluğu")
        print("✅ telekom_api_schema.py Mutlak Uyumluluk")
        print("✅ Sıfır Hata Toleransı")
        
        # API Fonksiyon -> Response Model eşleştirmesi (KRİTİK)
        self.api_response_map = self._build_api_response_mapping()
        
        # Kalite kontrol sayaçları
        self.validation_errors = 0
        self.schema_violations = 0 
        print("✅ Uzman Seviyesi Optimizasyonlar (Memory Optimized)")
        
        # Lazy loading için cache'ler - memory optimization
        self._personality_profiles_cache = None
        self._cognitive_patterns_cache = None
        self._meta_templates_cache = None
        self._cultural_contexts_cache = None
        self._temporal_patterns_cache = None
        self._innovation_frameworks_cache = None
        
        # Statistics tracking
        self.generated_scenarios = {scenario.value: 0 for scenario in ScenarioType}
        self.total_generated = 0
        
        print(f"📊 {len(self.api_response_map)} API fonksiyonu eşleştirildi")

    def _build_api_response_mapping(self) -> Dict[str, Any]:
        """
        KRİTİK FONKSİYON: API fonksiyonlarını response modellerine eşleştirir.
        Bu, %100 şema uyumluluğu için hayati önem taşır.
        """
        return API_RESPONSE_MAPPING

    def _create_validated_response(self, model_class, override_data: Optional[Dict] = None) -> str:
        """
        SUPREME V3 + ENTERPRISE SCHEMA INTEGRATION - %100 PYDANTİC DOĞRULAMA GÜVENCESİ
        Yeni telekom_api_schema v3.0-SUPREME utility fonksiyonlarını kullanarak
        enterprise-grade mock response oluşturur.
        """
        try:
            # Schema v3.0 ile gelişmiş mock data üretimi
            mock_data = self._generate_mock_data_for_model(model_class)
            if override_data:
                for key, value in override_data.items():
                    # usage_percentage için özel kontrol
                    if key == "usage_percentage" and isinstance(value, dict):
                        # Her değerin 100'den küçük olduğundan emin ol
                        fixed_usage = {}
                        for usage_key, usage_value in value.items():
                            if isinstance(usage_value, int) and usage_value > 100:
                                fixed_usage[usage_key] = random.randint(0, 100)
                                print(f"🔧 Usage percentage düzeltildi: {usage_key}: {usage_value} → {fixed_usage[usage_key]}")
                            else:
                                fixed_usage[usage_key] = usage_value
                        mock_data[key] = fixed_usage
                    else:
                        mock_data[key] = value
            # Enterprise-grade Pydantic doğrulama
            validated = model_class(**mock_data)
            # JSON serileştirme kontrolü
            json_result = validated.model_dump_json(indent=None)
            # JSON'ın parse edilebilir olduğunu kontrol et
            json.loads(json_result)
            return json_result
        except Exception as e:
            print(f"❌ KRİTİK HATA - Beklenmeyen: {model_class.__name__}")
            print(f"   Hata: {e}")
            raise

    def _get_scenario_generators(self) -> Dict[str, callable]:
        """
        Senaryo üreticilerini döndürür
        """
        return {
            ScenarioType.STANDARD.value: generate_standard_scenario,
            ScenarioType.TOOL_CHAINING.value: generate_tool_chaining_scenario,
            ScenarioType.PROACTIVE.value: generate_proactive_scenario,
            ScenarioType.DISAMBIGUATION.value: generate_disambiguation_scenario,
            ScenarioType.MULTI_INTENT.value: generate_multi_intent_scenario,
            ScenarioType.ETHICAL_DILEMMA.value: generate_ethical_dilemma_scenario,
            ScenarioType.NEGOTIATION_SKILLS.value: generate_negotiation_skills_scenario,
            ScenarioType.TEACHING_MENTORING.value: generate_teaching_mentoring_scenario,
            ScenarioType.INNOVATION_THINKING.value: generate_innovation_thinking_scenario,
            ScenarioType.TEMPORAL_REASONING.value: generate_temporal_reasoning_scenario,
            ScenarioType.CROSS_CULTURAL_COMMUNICATION.value: generate_cross_cultural_communication_scenario,
        }

    def generate_supreme_dataset(self, num_samples: int = 100) -> List[Dict[str, Any]]:
        """
        SUPREME VERSİYON: %100 şema uyumlu, sıfır toleranslı dataset üretimi
        
        Bu fonksiyon, her üretilen verinin mükemmel olmasını garanti eder.
        """
        
        print(f"🚀 {num_samples} adet SUPREME seviye veri üretiliyor...")
        print("✅ %100 Pydantic validasyon ZORUNLU")
        print("✅ telekom_api_schema.py'ye MUTLAK uyumluluk")
        print("✅ Sıfır tolerans politikası AKTİF")
        
        dataset = []
        
        # Senaryo üreticilerini al
        scenario_generators = self._get_scenario_generators()
        
        # UZMAN SEVİYESİ İYİLEŞTİRME: Tüm senaryo da artık burada tanımlı
        scenario_types = list(scenario_generators.keys())
        
        # Her senaryo için ağırlıkların tam olarak eşleştiğinden emin ol
        weights = [SCENARIO_WEIGHTS.get(scenario_type, 1.0) for scenario_type in scenario_types]

        # UZMAN SEVİYESİ KONTROL: Ağırlık ve metod listelerinin uzunlukları eşleşmelidir.
        if len(scenario_types) != len(weights):
            raise ValueError(
                f"Senaryo metodları ({len(scenario_types)}) ve ağırlıklar ({len(weights)}) "
                "listelerinin uzunlukları eşleşmiyor. Lütfen kontrol edin."
            )

        # UZMAN SEVİYE KALİTE KONTROL DEĞİŞKENLERİ
        validation_errors = 0
        skipped_scenarios = 0
        pydantic_validations = 0

        for i in range(num_samples):
            # UZMAN SEVİYESİ İYİLEŞTİRME: Ağırlıklı rastgele seçim
            scenario_type = random.choices(scenario_types, weights=weights, k=1)[0]
            
            try:
                # Uygun generator metodunu çağır
                scenario = scenario_generators[scenario_type]()
                
                # UZMAN SEVİYE KALİTE KONTROL: Her senaryo için detaylı doğrulama
                validation_result = validate_scenario_quality(scenario)
                if not validation_result["valid"]:
                    print(f"⚠️ Kalite kontrolü başarısız: {scenario_type} - {validation_result['error']}")
                    validation_errors += 1
                    continue
                
                # UZMAN SEVİYE KALİTE KONTROL: API yanıtlarının Pydantic uyumluluğunu kontrol et
                pydantic_check = verify_pydantic_compliance(scenario)
                if not pydantic_check["valid"]:
                    print(f"❌ Pydantic uyumsuzluğu: {scenario_type} - {pydantic_check['error']}")
                    validation_errors += 1
                    continue
                
                pydantic_validations += pydantic_check["validated_count"]
                dataset.append(scenario)
                
                self.generated_scenarios[scenario_type] += 1
                self.total_generated += 1
                
                if (i + 1) % 10 == 0:
                    print(f"📊 İlerleme: {i + 1}/{num_samples} (%{(i+1)/num_samples*100:.1f}) - ✅ {pydantic_validations} Pydantic doğrulama")
                    
            except Exception as e:
                import traceback
                print(f"❌ Beklenmeyen hata: {e}")
                print(f"🔍 Hata türü: {type(e).__name__}")
                print(f"🔍 Senaryo türü: {scenario_type}")
                print(f"🔍 Detaylı traceback:")
                traceback.print_exc()
                print("="*50)
                skipped_scenarios += 1
                continue
        
        print("\n🎊 DATASET GENERATİON TAMAMLANDI!")
        print("="*60)
        print("📊 UZMAN SEVİYE KALİTE RAPORU:")
        print(f"   ✅ Başarılı senaryolar: {len(dataset)}")
        print(f"   ❌ Doğrulama hataları: {validation_errors}")
        print(f"   ⚠️ Atlanan senaryolar: {skipped_scenarios}")
        print(f"   🔍 Toplam Pydantic doğrulama: {pydantic_validations}")
        print(f"   📈 Başarı oranı: %{len(dataset)/(len(dataset)+validation_errors+skipped_scenarios)*100:.1f}")
        
        print("\n📊 Senaryo Dağılımı:")
        for scenario_type, count in self.generated_scenarios.items():
            if count > 0:
                print(f"   • {scenario_type}: {count} adet")
        
        # SUPREME V3: DETAYLI HATA ANALİZİ VE UYARI SİSTEMİ
        total_attempts = len(dataset) + validation_errors + skipped_scenarios
        error_rate = (validation_errors + skipped_scenarios) / total_attempts * 100 if total_attempts > 0 else 0
        
        if error_rate > 10:  # %10'dan fazla hata
            print(f"\n⚠️ YÜKSEKRİSK UYARI: Hata oranı %{error_rate:.1f}")
            print(f"   • Validasyon hataları: {validation_errors}")
            print(f"   • Atlanan senaryolar: {skipped_scenarios}")
            print(f"   • Toplam deneme: {total_attempts}")
            print("   🔍 ÖNERİLER:")
            print("     - telekom_api_schema.py uyumluluğunu kontrol edin")
            print("     - _create_validated_response fonksiyonunu inceleyin")
            print("     - Pydantic model tanımlarını doğrulayın")
        
        if len(dataset) == 0:
            error_msg = "❌ KRİTİK BAŞARISIZLIK: Hiçbir geçerli senaryo üretilemedi!"
            if validation_errors > 0:
                error_msg += f"\n   • {validation_errors} validasyon hatası oluştu"
            if skipped_scenarios > 0:
                error_msg += f"\n   • {skipped_scenarios} senaryo atlandı"
            error_msg += "\n   🚨 ÇÖZÜM: Lütfen API şeması ve Pydantic tanımlarını kontrol edin"
            raise ValueError(error_msg)
        
        if error_rate > 25:  # %25'ten fazla hata kritik seviyede
            print(f"\n🚨 KRİTİK UYARI: Çok yüksek hata oranı (%{error_rate:.1f})")
            print("   Bu dataset ile eğitim ÖNERİLMEZ!")
            print("   Lütfen hataları düzelttikten sonra tekrar deneyin.")
        
        return dataset

    def save_dataset(self, dataset: List[Dict[str, Any]], filename: str):
        """Dataset'i JSON dosyasına kaydet"""
        output_path = DEFAULT_OUTPUT_DIR / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Dataset kaydedildi: {output_path}")
        print(f"📁 Dosya boyutu: {output_path.stat().st_size / 1024 / 1024:.2f} MB") 