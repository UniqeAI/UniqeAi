"""
Otomatik Ödeme Kurulumu Senaryosu
==================================

Bu modül, kullanıcının otomatik ödeme talimatı verdiği senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import SetupAutopayResponse


def generate_setup_autopay_scenario() -> Dict[str, Any]:
    """Kullanıcının otomatik ödeme talimatı verdiği senaryo."""
    user_id = generate_user_id()
    return {
        "id": f"setup_autopay_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SETUP_AUTOPAY.value,
        "personality_profile": "busy_working_parent",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Faturalarımı sürekli unutuyorum, otomatik ödeme talimatı vermek istiyorum."},
            {"rol": "asistan", "icerik": "Harika bir fikir! Kayıtlı kredi kartınızla otomatik ödeme talimatı oluşturuyorum, onaylıyor musunuz?"},
            {"rol": "kullanici", "icerik": "Evet, onaylıyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "setup_autopay", "parametreler": {"user_id": user_id, "status": True}}]},
            {"rol": "arac", "icerik": create_validated_response(SetupAutopayResponse, override_data={"user_id": user_id, "autopay_enabled": True})},
            {"rol": "asistan", "icerik": "Otomatik ödeme talimatınız başarıyla oluşturulmuştur. Artık faturalarınız son ödeme tarihinde kartınızdan otomatik olarak çekilecektir."}
        ]
    } 