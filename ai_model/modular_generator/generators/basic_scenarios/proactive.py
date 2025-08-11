"""
Proaktif Senaryo
================

Bu modül, AI'ın proaktif olarak bir sonraki adımı önerdiği senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import GetRemainingQuotasResponse


def generate_proactive_scenario() -> Dict[str, Any]:
    """AI'ın proaktif olarak bir sonraki adımı önerdiği senaryo."""
    user_id = generate_user_id()
    
    return {
        "id": f"proactive_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PROACTIVE.value,
        "personality_profile": "busy_working_parent",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": f"Yine internetim bitmek üzere, bu ay ne kadar kalmış?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hemen kontrol ediyorum...", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, override_data={"internet_remaining_gb": 1.5, "usage_percentage": {"internet": 98, "voice": 50, "sms": 75}})},
            {"rol": "asistan", "icerik": "Sadece 1.5 GB internetiniz kalmış ve dönem sonuna 3 gün var. Ay sonunu getirmekte zorlanabilirsiniz. **Proaktif Öneri:** Size özel, sadece bu aya mahsus 10 GB'lık ek paketi %50 indirimle tanımlayabilirim. İster misiniz?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Harika olur, lütfen tanımlayın!", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Ek paketiniz hattınıza başarıyla tanımlanmıştır.", "arac_cagrilari": None}
        ]
    } 