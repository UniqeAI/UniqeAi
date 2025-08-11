"""
Roaming Aktifleştirme Senaryosu
================================

Bu modül, kullanıcının roaming hizmetini aktive ettiği senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import EnableRoamingResponse


def generate_enable_roaming_scenario() -> Dict[str, Any]:
    """Kullanıcının roaming hizmetini aktive ettiği senaryo."""
    user_id = generate_user_id()
    return {
        "id": f"enable_roaming_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ENABLE_ROAMING.value,
        "personality_profile": "frequent_traveler",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Yarın yurt dışına çıkıyorum, roaming'i aktif edebilir misiniz?"},
            {"rol": "asistan", "icerik": "Elbette! Hemen roaming hizmetinizi aktive ediyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "enable_roaming", "parametreler": {"user_id": user_id, "status": True}}]},
            {"rol": "arac", "icerik": create_validated_response(EnableRoamingResponse, override_data={"user_id": user_id, "roaming_enabled": True})},
            {"rol": "asistan", "icerik": "Roaming hizmetiniz başarıyla aktive edildi! İyi yolculuklar."}
        ]
    } 