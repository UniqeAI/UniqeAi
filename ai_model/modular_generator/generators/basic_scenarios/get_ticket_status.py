"""
Destek Talebi Durumu Senaryosu
==============================

Bu modül, belirli bir destek talebinin durumunu sorgulayan senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import GetFaultTicketStatusResponse


def generate_get_ticket_status_scenario() -> Dict[str, Any]:
    """Belirli bir destek talebinin durumunu sorgulayan senaryo."""
    ticket_id = f"T-{random.randint(100000, 999999)}"
    return {
        "id": f"get_ticket_status_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.GET_TICKET_STATUS.value,
        "personality_profile": "impatient_customer",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": f"{ticket_id} numaralı destek talebimin durumu nedir?"},
            {"rol": "asistan", "icerik": "Hemen kontrol ediyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_fault_ticket_status", "parametreler": {"ticket_id": ticket_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetFaultTicketStatusResponse, override_data={"ticket_id": ticket_id})},
            {"rol": "asistan", "icerik": f"'{ticket_id}' numaralı talebinizin güncel durumu ve teknisyen notlarını görebilirsiniz."}
        ]
    } 