"""
İnternet Hız Testi Senaryosu
=============================

Bu modül, internet hız testini başlatan senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import TestInternetSpeedResponse


def generate_test_internet_speed_scenario() -> Dict[str, Any]:
    """İnternet hız testini başlatan senaryo."""
    user_id = generate_user_id()
    return {
        "id": f"test_internet_speed_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.TEST_INTERNET_SPEED.value,
        "personality_profile": "tech_savvy_gamer",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "İnternetim çok yavaş geliyor, hız testi yapabilir misiniz?"},
            {"rol": "asistan", "icerik": "Elbette! Hemen internet hız testinizi başlatıyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, override_data={"user_id": user_id})},
            {"rol": "asistan", "icerik": "Hız testi tamamlandı! İndirme ve yükleme hızlarınızı, ping değerlerinizi görebilirsiniz."}
        ]
    } 