"""
Belirsizlik Giderme Senaryosu
==============================

Bu modül, AI'ın belirsiz bir talebi netleştirdiği senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import CreateFaultTicketResponse


def generate_disambiguation_scenario() -> Dict[str, Any]:
    """AI'ın belirsiz bir talebi netleştirdiği senaryo."""
    user_id = generate_user_id()

    return {
        "id": f"disambiguation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.DISAMBIGUATION.value,
        "personality_profile": "cautious_senior",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CONFUSED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Hattımla ilgili bir sorun var, bir şeyler yapmak istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Elbette size yardımcı olmak için buradayım. Ancak talebiniz biraz belirsiz. **Netleştirmek için soruyorum:** 'Bir şeyler yapmak' ile tam olarak neyi kastediyorsunuz? \n1. Faturanızı mı ödemek istiyorsunuz?\n2. Tarifenizi mi değiştirmek istiyorsunuz?\n3. Bir arıza mı bildirmek istiyorsunuz?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Ha evet, doğru. Arıza bildirecektim, internetim çok yavaş.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Anladım, teşekkür ederim. Hemen internet yavaşlığıyla ilgili bir arıza kaydı oluşturuyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "create_fault_ticket", "parametreler": {"user_id": user_id, "issue_description": "İnternet çok yavaş.", "category": "internet_speed", "priority": "medium"}}]},
            {"rol": "arac", "icerik": create_validated_response(CreateFaultTicketResponse, override_data={"user_id": user_id, "issue_description": "İnternet çok yavaş.", "category": "internet_speed", "priority": "high", "status": "open"})},
            {"rol": "asistan", "icerik": "Arıza kaydınız başarıyla oluşturulmuştur.", "arac_cagrilari": None}
        ]
    } 