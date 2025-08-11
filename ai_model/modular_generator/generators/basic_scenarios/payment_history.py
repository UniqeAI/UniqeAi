"""
Ödeme Geçmişi Senaryosu
========================

Bu modül, kullanıcının geçmiş ödeme bilgilerini sorguladığı senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import GetPaymentHistoryResponse


def generate_payment_history_scenario() -> Dict[str, Any]:
    """Kullanıcının geçmiş ödeme bilgilerini sorguladığı senaryo."""
    user_id = generate_user_id()
    return {
        "id": f"payment_history_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PAYMENT_HISTORY.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Son 3 ay içerisindeki ödeme geçmişimi kontrol edebilir miyim?"},
            {"rol": "asistan", "icerik": "Elbette, hemen ödeme geçmişinizi kontrol ediyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_payment_history", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPaymentHistoryResponse)},
            {"rol": "asistan", "icerik": "Son 3 ayda toplam 3 adet ödeme yapmışsınız. Detayları listeliyorum..."}
        ]
    } 