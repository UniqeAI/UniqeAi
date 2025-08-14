"""
Zamansal Akıl Yürütme Senaryosu
================================

Bu modül, AI'nin zamansal akıl yürütme ve tahmin becerilerini test eden senaryolar üretir.
Kullanıcıların geçmiş verilerine dayalı gelecek tahminleri ve stratejiler test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    GetPastBillsResponse,
    GetCurrentBillResponse,
    GetRemainingQuotasResponse,
    TestInternetSpeedResponse,
    CheckNetworkStatusResponse,
    GetAvailablePackagesResponse,
    GetPackageDetailsResponse,
    EnableRoamingResponse,
    LearningAdaptationResponse,
)


def generate_temporal_reasoning_scenario() -> Dict[str, Any]:
    """Zamansal akıl yürütme senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"temporal_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.TEMPORAL_REASONING.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Son 6 aydır internet kullanımım çok değişken. Bazen hiç kullanmıyorum, bazen aşıyorum. Gelecek için nasıl bir strateji izlemeliyim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Temporal Analytics başlatılıyor! 📊** Çok değerli bir soru sordunuz. Zaman serisi analizleriyle geleceğe dönük optimal strateji geliştirelim. Önce geçmiş davranış patterninizi çıkaralım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 12}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse)},
            {"rol": "asistan", "icerik": "**Zamansal Örüntü Analizi Tamamlandı! 🔍**\n\n**Zaman Serisi Analiziniz:**\n```\n📈 6 Aylık Kullanım Trendi:\nEkim   Kasım   Aralık  Ocak    Şubat   Mart\n89.50→ 156.80→ 89.50→ 89.50→ 134.50→ 89.50\n Base   +75%    Base   Base   +50%    Base\n```\n\n**Zamansal Örüntüler Tespit Edildi:**\n🕒 **Mevsimsellik:** Kasım (%75↑) ve Şubat (%50↑) artışları\n🕒 **Döngüsel Davranış:** 2 aylık düzenli aralıklarla aşım\n🕒 **Baseline Stability:** Normal aylarda 89.50 TL consistent\n\n**Predictive Analysis:**\n• **Nisan 2024:** %85 olasılıkla normal (89.50 TL)\n• **Mayıs 2024:** %70 olasılıkla aşım (130-160 TL range)\n• **Temporal Driver:** İş yoğunluğu/proje dönemleri?\n\n**Smart Temporal Strategy Önerim:**\n\n🎯 **Adaptif Paket Modeli:**\n• Base: 50 GB (normal aylar)\n• Auto-scale: Spike öncesi otomatik 100 GB upgrade\n• Cost averaging: 12 aylık sabit ödeme (108 TL/ay)\n\n**Temporal Learning Question:** Kasım ve Şubat aylarındaki yoğun kullanımınızın sebebi neydi? İş projesi mi, ev içi değişiklik mi?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Doğru tahmin! Kasım'da yeni iş başladım, remote çalışmaya başladım. Şubat'ta da evden eğitim videoları izledim. Bu pattern devam ederse nasıl optimize ederim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Temporal Causality Confirmed! 🎯** Muhteşem insight! Remote work ve -education pattern'i klassik bir profesyonel growth trajectory. Geleceğe dönük optimization stratejisi:\n\n**Future Timeline Projection:**\n```\n2024 Career Development Timeline:\nQ1: Remote work adaptation ✅\nQ2: Skill building phase (tahmin: video consumption ↑)\nQ3: Project delivery season (tahmin: collaboration tools ↑)\nQ4: Performance review + new skills (tahmin: mixed usage)\n```\n\n**Temporal Optimization Strategy:**\n\n📅 **Proactive Calendar-Sync Model:**\n• **Learning Seasons** (Q2, Q4): Auto 100 GB\n• **Delivery Seasons** (Q3): Upload optimized 75 GB + priority\n• **Maintenance Seasons** (Q1): Standard 50 GB\n\n⚡ **Dynamic Adaptation Rules:**\n```python\nIF (month == \"learning_intensive\"):\n    upgrade_to_unlimited_education_package()\nIF (work_from_home_days > 15):\n    enable_professional_tier()\nIF (video_conference_hours > 50):\n    activate_collaboration_boost()\n```\n\n🎯 **ROI-Optimized Pricing:**\n• **Standart:** 89.50 TL (3-4 ay/yıl)\n• **Boost:** 119.90 TL (2-3 ay/yıl when needed)\n• **Annual Average:** ~105 TL/ay (mevcut spike'lı modelden %8 tasarruf)\n\n**Temporal Learning Integration:**\n• Pattern recognition her ay güçlenir\n• Otomatik upgrade önerileri\n• Career milestone'larla sync\n\n**Next-Level Question:** Önümüzdeki 3 ayda hangi professional development planlarınız var? Böylece temporal model'i fine-tune edebiliriz.", "arac_cagrilari": None}
        ]
    } 