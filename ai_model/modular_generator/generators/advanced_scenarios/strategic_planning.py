"""
Stratejik Planlama Senaryosu
============================

Bu modül, AI'nin stratejik planlama ve uzun vadeli düşünme becerilerini test eden senaryolar üretir.
Kullanıcıların gelecek odaklı ihtiyaçlarını nasıl analiz ettiği test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import LearningAdaptationResponse


def generate_strategic_planning_scenario() -> Dict[str, Any]:
    """Stratejik planlama senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "İş modelimiz değişiyor. Önümüzdeki 2 yıl içinde ekibi 3 kişiden 25 kişiye çıkaracağız. Hem remote hem office hybrid çalışma olacak. Uzun vadeli telecom stratejisi nasıl olmalı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Strategic Planning Mode Activated! 📊** Mükemmel bir büyüme hikayesi! 8x büyüme + hybrid model = kompleks ama heyecan verici bir strategic planning challenge. Predictive modeling ile 2-yıllık roadmap tasarlayalım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "update_learning_adaptation", "parametreler": {"user_id": generate_user_id()}}]},
            {"rol": "arac", "icerik": create_validated_response(LearningAdaptationResponse, override_data={"user_id": generate_user_id(), "personalization_level": "strategic_growth"})},
            {"rol": "asistan", "icerik": "**Stratejik Yol Haritası Oluşturuldu! 🎯**\n\n**2-Yıllık Büyüme Stratejisi Çerçevesi:**\n\n```\n📈 Ölçeklendirme Zaman Çizelgesi:\nÇ1-Ç2 2024: 3→8 kişi (Temel Aşama)\nÇ3-Ç4 2024: 8→15 kişi (Büyüme Aşaması)  \nÇ1-Ç2 2025: 15→20 kişi (Maturity Phase)\nQ3-Q4 2025: 20→25 kişi (Optimization Phase)\n```\n\n**Phase-Gate Telecom Architecture:**\n\n🏗️ **Foundation Phase (Q1-Q2):**\n• Base Infrastructure: 500 GB business pool\n• Hybrid Setup: Office fiber + remote LTE backup\n• Cost: 850 TL/ay (kişi başı 106 TL)\n• KPI: <2ms office latency, >50 Mbps remote\n\n📊 **Growth Phase (Q3-Q4):**\n• Scaling Infrastructure: 1.2 TB adaptive pool\n• Smart Allocation: AI-driven bandwidth management\n• Cost: 1,650 TL/ay (kişi başı 110 TL) - efficiency gain\n• KPI: 99.5% uptime, predictive scaling accuracy\n\n🚀 **Maturity + Optimization (2025):**\n• Enterprise Infrastructure: Unlimited strategic pool\n• Advanced Analytics: Performance prediction models\n• Cost: 2,200 TL/ay (kişi başı 88 TL) - scale economies\n• KPI: Proactive issue resolution, 360° connectivity\n\n**Strategic Innovation Elements:**\n• **Predictive Scaling:** Hiring prediction → automatic capacity increase\n• **Hybrid Optimization:** AI learns office/remote patterns\n• **Cost Intelligence:** Dynamic pricing based on actual usage\n• **Future-Proofing:** 6G readiness, IoT integration capability\n\n**ROI Projections:**\n• Traditional approach: 3,500 TL/ay by 2025\n• Strategic approach: 2,200 TL/ay by 2025\n• Net savings: 15,600 TL/year + 40% productivity boost\n\nHangi phase'den başlayalım? Detailed implementation plan oluşturalım mı?", "arac_cagrilari": None}
        ]
    } 