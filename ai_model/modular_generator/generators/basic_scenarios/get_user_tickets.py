"""
Kullanıcı Destek Talepleri Senaryosu
=====================================

Bu modül, kullanıcının mevcut destek taleplerini listeleyen senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import GetUsersTicketsResponse


def generate_get_user_tickets_scenario() -> Dict[str, Any]:
    """Kullanıcının mevcut destek taleplerini listeleyen senaryo."""
    user_id = generate_user_id()
    return {
        "id": f"get_user_tickets_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.GET_USER_TICKETS.value,
        "personality_profile": "systematic_professional",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Açtığım destek taleplerimin durumunu kontrol edebilir miyim?"},
            {"rol": "asistan", "icerik": "Tabii ki! Mevcut destek taleplerrinizi listeliyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_users_tickets", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetUsersTicketsResponse, override_data={"user_id": user_id})},
            {"rol": "asistan", "icerik": "İşte mevcut destek taleplerrinizin listesi. Her birinin durumunu ve tahmini çözüm süresini görebilirsiniz."}
        ]
    } 