"""
İşbirlikçi Filtreleme Senaryosu
================================

Bu modül, AI'nin işbirlikçi filtreleme ve benzer kullanıcı profillerine dayalı öneriler sunma becerilerini test eden senaryolar üretir.
Kullanıcı davranışlarına dayalı kişiselleştirilmiş öneriler test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response


def generate_collaborative_filtering_scenario1() -> Dict[str, Any]:
    """İşbirlikçi filtreleme senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"collaborative_filtering_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "tech_savvy_millennial",
        "cognitive_state": CognitiveState.CURIOUS.value,
        "emotional_context": EmotionalContext.INTERESTED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Benim gibi kullanıcılar hangi paketleri tercih ediyor?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Collaborative Filtering Engine Activated! 🎯**\n\n**Similar User Analysis:**\n• Profiliniz: Tech-savvy, 25-35 yaş, urban\n• Benzer kullanıcılar: 15,432 kişi\n• Ortak tercihler analiz ediliyor\n\n**Top Recommendations:**\n1. **Gaming Pro Package** (%78 tercih)\n2. **Streaming Unlimited** (%65 tercih)\n3. **Work-From-Home Plus** (%72 tercih)\n\n**Personalized Match:**\nGaming Pro Package sizin için %92 uyumluluk gösteriyor!", "arac_cagrilari": None}
        ]
    } 

def generate_collaborative_filtering_scenario() -> Dict[str, Any]:
    """İş birlikçi filtreleme senaryosu"""
    user_id = generate_user_id()
    return {
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "competitive_sales_professional",
        "cognitive_state": CognitiveState.COLLABORATIVE.value,
        "emotional_context": EmotionalContext.COLLABORATIVE_MOOD.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Benzer profildeki kullanıcılar hangi paketleri tercih ediyor? Onların deneyimlerinden yararlanabilir miyim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Collaborative Intelligence Active! 🤝**\n\nBenzer profildeki kullanıcıların tercihlerini analiz ediyorum:\n\n👥 **Similar User Profile Analysis:**\n• %67'si Pro Business paketini tercih ediyor\n• %45'i international calling ekliyor\n• Ortalama memnuniyet: 4.2/5\n\n💡 **Community Recommendations:**\n• Gaming boost %78 satisfaction\n• Family sharing %89 approval\n\nSize özel recommendation matrix oluşturayım mı?", "arac_cagrilari": None}
        ]
    }