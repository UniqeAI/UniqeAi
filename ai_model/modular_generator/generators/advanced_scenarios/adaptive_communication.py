"""
Adaptif İletişim Senaryosu
===========================

Bu modül, AI'nin adaptif iletişim ve kullanıcı tercihlerine göre iletişim tarzını ayarlama becerilerini test eden senaryolar üretir.
Farklı kullanıcı profillerine göre iletişim tarzını nasıl değiştirdiği test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response


def generate_adaptive_communication_scenario1() -> Dict[str, Any]:
    """Adaptif iletişim senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"adaptive_communication_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "personality_profile": "busy_executive",
        "cognitive_state": CognitiveState.EFFICIENT.value,
        "emotional_context": EmotionalContext.PRESSURED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Hızlıca paketimi değiştirmek istiyorum. Detaylara girmeden sadece ne yapmam gerekiyor?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Efficient Mode Activated! ⚡**\n\n**Quick Action Required:**\n1. Paket adı söyleyin\n2. Onay verin\n3. 2 dakikada tamamlanır\n\nHangi pakete geçmek istiyorsunuz?", "arac_cagrilari": None}
        ]
    } 

def generate_adaptive_communication_scenario() -> Dict[str, Any]:
    """Adaptif iletişim senaryosu"""
    user_id = generate_user_id()
    return {
        "id": f"adaptive_comm_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "personality_profile": "creative_artist_freelancer",
        "cognitive_state": CognitiveState.INTUITIVE.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ben görsel öğrenim tipiyim. Teknik şeyleri anlatırken görsel kullanabilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Visual Communication Mode Activated! 🎨**\n\nTabii ki! Sizin öğrenme stilinize uygun görsel açıklamalar yapacağım:\n\n📊 **İnternet Kotası Visualized:**\n```\n🟦🟦🟦🟦🟦🟦🟦⬜⬜⬜  (70% kullanıldı)\n|------ 35 GB ------|  |10GB|\n     Kullanılan         Kalan\n```\n\n🎯 Bu şekilde devam edelim mi? Hangi konuyu görsel olarak açıklamamı istersiniz?", "arac_cagrilari": None}
        ]
    }