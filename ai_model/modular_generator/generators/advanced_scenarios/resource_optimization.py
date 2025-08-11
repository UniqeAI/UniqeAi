"""
Kaynak Optimizasyonu Senaryosu
==============================

Bu modül, AI'nin kaynak optimizasyonu ve verimlilik artırma becerilerini test eden senaryolar üretir.
Kullanıcıların mevcut kaynaklarını nasıl optimize ettiği test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response


def generate_resource_optimization_scenario1() -> Dict[str, Any]:
    """Kaynak optimizasyonu senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "efficiency_conscious_manager",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.AMBITIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Mevcut paketimdeki kaynakları daha verimli kullanmak istiyorum. Nasıl optimize edebilirim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Resource Optimization Engine Activated! ⚙️**\n\n**Current Usage Analysis:**\n• Internet: %80 kullanım (20% israf)\n• Voice: %30 kullanım (70% israf)\n• SMS: %10 kullanım (90% israf)\n\n**Optimization Strategy:**\n• Internet kotasını %100 kullan\n• Voice dakikalarını azalt\n• SMS yerine WhatsApp kullan\n\n**Expected Savings:** %25 maliyet azalması", "arac_cagrilari": None}
        ]
    } 

def generate_resource_optimization_scenario() -> Dict[str, Any]:
    """Kaynak optimizasyonu senaryosu"""
    user_id = generate_user_id()
    return {
        "id": f"resource_opt_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.AMBITIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Şirketimizde 15 farklı hat var ve maliyetler çok yüksek. Kaynak optimizasyonu yapabilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Kaynak Optimizasyon Motoru! ⚡**\n\n15 hat için verimlilik analizi başlatıyorum. Akıllı birleştirme ve maliyet optimizasyonu stratejileri geliştireceğim:\n\n🎯 **Optimizasyon Hedefleri:**\n• Maliyet azaltma: %25-40\n• Kullanım verimliliği: %90+\n• Yönetim basitleştirme\n\nDetaylı analiz yapayım...", "arac_cagrilari": None}
        ]
    }