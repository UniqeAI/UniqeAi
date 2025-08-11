"""
Tahmine Dayalı Analitik Senaryosu
==================================

Bu modül, AI'nin tahmine dayalı analitik ve gelecek tahminleri yapma becerilerini test eden senaryolar üretir.
Kullanıcı verilerine dayalı gelecek tahminleri ve öneriler test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import GetPastBillsResponse


def generate_predictive_analytics_scenario1() -> Dict[str, Any]:
    """Tahmine dayalı analitik senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Gelecek ay internet kullanımım nasıl olacak? Tahmin yapabilir misin?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Predictive Analytics Engine Activated! 📊**\n\n**Historical Data Analysis:**\n• Son 6 ay kullanım trendi analiz ediliyor\n• Mevsimsellik faktörleri hesaplanıyor\n• Anomali tespiti yapılıyor\n\n**Prediction Model:**\n• Gelecek ay tahmini: 85-95 GB\n• %90 güven aralığı\n• Peak kullanım: 15-20 GB/hafta\n\n**Recommendation:**\n100 GB paket önerilir (güvenli marj)", "arac_cagrilari": None}
        ]
    } 

def generate_predictive_analytics_scenario() -> Dict[str, Any]:
    """Öngörüsel analitik senaryosu"""
    user_id = generate_user_id()
    return {
        "id": f"predictive_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.AMBITIOUS.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Veri tüketim trendlerimi analiz ederek gelecek ay ne kadar kullanacağımı tahmin edebilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Öngörüsel Analitik Motoru Başlatılıyor! 📈**\n\nMakine öğrenmesi modelleriyle gelecek tahmini yapabilirim. Önce geçmiş verilerinizi analiz edeyim...", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 12}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse), "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Öngörüsel Model Sonuçları! 🎯**\n\n```\n📊 6-Aylık Trend Analizi:\nGelecek ay tahmini: 52 GB (±8 GB)\nGüven aralığı: %85\nTrend: ↗️ %12 artış\n```\n\nBu tahmine göre paket önerisi yapalım mı?", "arac_cagrilari": None}
        ]
    }