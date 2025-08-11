"""
Hat Askıya Alma Senaryosu
==========================

Bu modül, kullanıcının hattını geçici olarak dondurduğu senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import SuspendLineResponse


def generate_suspend_line_scenario() -> Dict[str, Any]:
    """Kullanıcının hattını geçici olarak dondurduğu senaryo."""
    user_id = generate_user_id()
    return {
        "id": f"suspend_line_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SUSPEND_LINE.value,
        "personality_profile": "cautious_senior",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Yurt dışına çıkacağım için hattımı 3 aylığına dondurmak istiyorum."},
            {"rol": "asistan", "icerik": "Anladım, hattınızı geçici olarak askıya alıyorum. Bu süre içinde arama yapamayacağınızı ve alamayacağınızı unutmayın."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "suspend_line", "parametreler": {"user_id": user_id, "reason": "user_request_abroad"}}]},
            {"rol": "arac", "icerik": create_validated_response(SuspendLineResponse, override_data={"user_id": user_id})},
            {"rol": "asistan", "icerik": "Hattınız başarıyla askıya alınmıştır. İyi yolculuklar!"}
        ]
    } 