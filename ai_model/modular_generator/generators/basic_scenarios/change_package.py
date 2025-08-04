"""
Paket Değiştirme Senaryosu
===========================

Bu modül, kullanıcının mevcut tarife paketini değiştirdiği senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import ChangePackageResponse


def generate_change_package_scenario() -> Dict[str, Any]:
    """Kullanıcının mevcut tarife paketini değiştirdiği senaryo."""
    user_id = generate_user_id()
    new_package = "Mega İnternet Paketi"
    return {
        "id": f"change_package_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CHANGE_PACKAGE.value,
        "personality_profile": "tech_savvy_millennial",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": f"Merhaba, mevcut paketimi '{new_package}' ile değiştirmek istiyorum."},
            {"rol": "asistan", "icerik": f"Tabii ki. '{new_package}' için geçiş işlemlerinizi başlatıyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "new_package_name": new_package}}]},
            {"rol": "arac", "icerik": create_validated_response(ChangePackageResponse, override_data={"to_package": new_package, "status": "pending_activation"})},
            {"rol": "asistan", "icerik": f"Paket değişikliği talebiniz alınmıştır. Yeni paketiniz önümüzdeki fatura döneminde aktif olacaktır."}
        ]
    } 