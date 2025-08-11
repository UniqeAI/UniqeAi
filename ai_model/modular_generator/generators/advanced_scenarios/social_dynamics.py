"""
Sosyal Dinamikler Senaryosu
============================

Bu modül, AI'nin sosyal dinamikleri anlama ve topluluk odaklı çözüm üretme becerilerini test eden senaryolar üretir.
Kullanıcıların sosyal ihtiyaçlarını ve topluluk çözümlerini nasıl ele aldığı test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import CheckNetworkStatusResponse


def generate_social_dynamics_scenario() -> Dict[str, Any]:
    """Sosyal dinamikler senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "busy_working_parent",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.OVERWHELMED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ev internetimiz sürekli yavaş ve çocuklar online derslerde zorlanıyor. Eşim de ev ofisinden çalışıyor. Komşularla konuştum, onların da aynı problemi var. Mahallemiz için toplu bir çözüm olabilir mi?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Community-Centered Solution Approach! 👨‍👩‍👧‍👦** Çok değerli bir yaklaşım sergiliyorsunuz! Komşularla iş birliği yapmak hem Türk kültürünün güzel bir yanı hem de teknik açıdan çok akıllıca bir strateji. Sosyal çözüm odaklı yaklaşalım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Kadıköy Merkez"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, override_data={"status": "degraded"})},
            {"rol": "asistan", "icerik": "**Toplumsal Sorun Doğrulandı! 🏘️** Analiz sonuçları komşularınızın gözlemlerini doğruluyor. Mahallenizde fiber altyapı yoğunluğu sorunu var. Bu durumda bireysel çözümler yerine toplumsal çözüm çok daha mantıklı!\n\n**Social Dynamics Strategy:**\n\n👥 **Neighborhood Alliance Package:**\n• 10+ haneli toplu başvuruda %30 indirim\n• Ortak fiber altyapı yatırımı (maliyeti paylaşımlı)\n• 'Mahalle Wi-Fi' backup sistemi\n• Çocuk online eğitimi öncelik algoritması\n\n🏠 **Family-Centric Features:**\n• Ders saatleri (9-17) bandwidth guarantee\n• Ebeveyn kontrol sistemi (ücretsiz)\n• Ev ofisi quality assurance\n• Aile paylaşım kotası\n\n👫 **Community Building Benefits:**\n• Komşular arası tech support network\n• Ortak sorun çözme WhatsApp grubu\n• Mahalle etkinlikleri için ücretsiz hotspot\n\n**Action Plan:**\n1. Komşu listesi (min 8-10 hane)\n2. Toplu survey (ihtiyaç analizi)\n3. Özel mahalle paketi tasarımı\n4. Fiber altyapı upgrade timeline\n\nKomşularınızla bu planı konuşup geri dönüş yapar mısınız? 'Dijital mahalle' projesi başlatalım! 🚀", "arac_cagrilari": None}
        ]
    } 