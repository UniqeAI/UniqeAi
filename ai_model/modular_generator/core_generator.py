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
from .models import CulturalContext, PersonalityProfile

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
    generate_cross_cultural_communication_scenario,
    generate_advanced_error_recovery_scenario,
    generate_social_dynamics_scenario,
    generate_conflicting_information_scenario,
    generate_strategic_planning_scenario,
    generate_empathetic_reasoning_scenario,
    generate_adaptive_communication_scenario, # <-- GÜNCELLENDİ
    generate_predictive_analytics_scenario,
    generate_resource_optimization_scenario,
    generate_collaborative_filtering_scenario,
    generate_payment_history_scenario,
    generate_setup_autopay_scenario,
    generate_change_package_scenario,
    generate_suspend_line_scenario,
    generate_error_response_scenario,
    generate_package_details_scenario,
    generate_enable_roaming_scenario,
    generate_get_user_tickets_scenario,
    generate_get_ticket_status_scenario,
    generate_test_internet_speed_scenario
)

# Lazy loading ve initialize metodları için import
from .lazy_loading import (
    personality_profiles_property,
    cognitive_patterns_property,
    meta_templates_property,
    cultural_contexts_property,
    temporal_reasoning_patterns_property,
    innovation_frameworks_property
)

from .initializers import (
    initialize_enhanced_personality_profiles,
    initialize_advanced_cognitive_patterns,
    initialize_comprehensive_meta_templates,
    initialize_cultural_contexts,
    initialize_temporal_patterns,
    initialize_innovation_frameworks
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

    def _generate_mock_data_for_model(self, model_class) -> Dict[str, Any]:
        """
        Model sınıfı için mock data üretir
        """
        return generate_mock_data_for_model(model_class)

    def _create_validated_response(self, model_class, override_data: Optional[Dict] = None) -> str:
        """
        SUPREME V3 + ENTERPRISE SCHEMA INTEGRATION - %100 PYDANTİC DOĞRULAMA GÜVENCESİ
        
        Yeni telekom_api_schema v3.0-SUPREME utility fonksiyonlarını kullanarak
        enterprise-grade mock response oluşturur.
        """
        try:
            mock_data = self._generate_mock_data_for_model(model_class)
            if override_data:
                mock_data.update(override_data)
            validated = model_class(**mock_data)
            json_result = validated.model_dump_json(indent=None)
            json.loads(json_result)
            return json_result
        except Exception as e:
            # Hata yönetimi...
            raise

    def _get_scenario_generators(self) -> Dict[str, callable]:
        """
        Tüm senaryo üreticilerini ve onlara karşılık gelen senaryo tiplerini döndürür.
        Bu, ana `generate_supreme_dataset` fonksiyonunun ağırlıklara göre
        dinamik olarak senaryo seçmesini sağlar.
        """
        return {
            ScenarioType.STANDARD.value: generate_standard_scenario,
            ScenarioType.TOOL_CHAINING.value: generate_tool_chaining_scenario,
            ScenarioType.PROACTIVE_ASSISTANCE.value: generate_proactive_scenario,
            ScenarioType.DISAMBIGUATION.value: generate_disambiguation_scenario,
            ScenarioType.MULTI_INTENT.value: generate_multi_intent_scenario,
            ScenarioType.ETHICAL_DILEMMA.value: generate_ethical_dilemma_scenario,
            ScenarioType.NEGOTIATION_SKILLS.value: generate_negotiation_skills_scenario,
            ScenarioType.TEACHING_MENTORING.value: generate_teaching_mentoring_scenario,
            ScenarioType.INNOVATION_THINKING.value: generate_innovation_thinking_scenario,
            ScenarioType.TEMPORAL_REASONING.value: generate_temporal_reasoning_scenario,
            ScenarioType.CROSS_CULTURAL_COMMUNICATION.value: generate_cross_cultural_communication_scenario,
            ScenarioType.ADVANCED_ERROR_RECOVERY.value: generate_advanced_error_recovery_scenario,
            ScenarioType.SOCIAL_DYNAMICS.value: generate_social_dynamics_scenario,
            ScenarioType.CONFLICTING_INFORMATION.value: generate_conflicting_information_scenario,
            ScenarioType.STRATEGIC_PLANNING.value: generate_strategic_planning_scenario,
            ScenarioType.EMPATHETIC_REASONING.value: generate_empathetic_reasoning_scenario,
            ScenarioType.ADAPTIVE_COMMUNICATION.value: generate_adaptive_communication_scenario,
            ScenarioType.PREDICTIVE_ANALYTICS.value: generate_predictive_analytics_scenario,
            ScenarioType.RESOURCE_OPTIMIZATION.value: generate_resource_optimization_scenario,
            ScenarioType.COLLABORATIVE_FILTERING.value: generate_collaborative_filtering_scenario,
            ScenarioType.PAYMENT_HISTORY.value: generate_payment_history_scenario,
            ScenarioType.SETUP_AUTOPAY.value: generate_setup_autopay_scenario,
            ScenarioType.CHANGE_PACKAGE.value: generate_change_package_scenario,
            ScenarioType.SUSPEND_LINE.value: generate_suspend_line_scenario,
            ScenarioType.ERROR_RESPONSE.value: generate_error_response_scenario,
            ScenarioType.PACKAGE_DETAILS.value: generate_package_details_scenario,
            ScenarioType.ENABLE_ROAMING.value: generate_enable_roaming_scenario,
            ScenarioType.GET_USER_TICKETS.value: generate_get_user_tickets_scenario,
            ScenarioType.GET_TICKET_STATUS.value: generate_get_ticket_status_scenario,
            ScenarioType.TEST_INTERNET_SPEED.value: generate_test_internet_speed_scenario
        }

    @property
    def personality_profiles(self):
        return personality_profiles_property(self)
    
    # ... diğer property'ler ...

    def generate_adaptive_communication_scenario(self, num_samples: int) -> List[Dict[str, Any]]:
        """
        Belirtilen sayıda adaptif iletişim senaryosu üretir.
        """
        print(f"🚀 {num_samples} adet ADAPTIVE COMMUNICATION senaryosu üretiliyor...")
        dataset = []
        for _ in range(num_samples):
            try:
                # generate_adaptive_communication_scenario artık doğrudan senaryo döndürüyor
                scenario = generate_adaptive_communication_scenario()
                
                # Kalite ve şema kontrolleri
                validation_result = validate_scenario_quality(scenario)
                if not validation_result["valid"]:
                    print(f"⚠️ Kalite kontrolü başarısız: {validation_result['error']}")
                    continue

                pydantic_check = verify_pydantic_compliance(scenario)
                if not pydantic_check["valid"]:
                    print(f"❌ Pydantic uyumsuzluğu: {pydantic_check['error']}")
                    continue
                
                dataset.append(scenario)
                self.generated_scenarios[ScenarioType.ADAPTIVE_COMMUNICATION.value] += 1
                self.total_generated += 1

            except Exception as e:
                import traceback
                print(f"❌ Adaptif iletişim senaryosu üretilirken hata: {e}")
                traceback.print_exc()
                continue
        
        print(f"✅ {len(dataset)} adet adaptif iletişim senaryosu başarıyla üretildi.")
        return dataset


    def generate_supreme_dataset(self, num_samples: int = 100) -> List[Dict[str, Any]]:
        # ... (Bu fonksiyonun geri kalanı aynı)
        pass

    def save_dataset(self, dataset: List[Dict[str, Any]], filename: str):
        # ... (Bu fonksiyon aynı)
        pass
