"""
Öğretim ve Mentorluk Senaryosu
==============================

Bu modül, AI'nin öğretim ve mentorluk becerilerini test eden senaryolar üretir.
Kullanıcıların öğrenme süreçlerinde AI'nin nasıl rehberlik ettiği test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    GetRemainingQuotasResponse,
    TestInternetSpeedResponse,
    GetCurrentBillResponse,
    GetAvailablePackagesResponse,
    GetPackageDetailsResponse,
    SetupAutopayResponse,
    UpdateCustomerContactResponse,
    GetCustomerProfileResponse,
    CheckNetworkStatusResponse,
    EnableRoamingResponse,
    LearningAdaptationResponse,
)


def generate_teaching_mentoring_scenarios() -> List[Dict[str, Any]]:
    """Öğretim ve mentorluk temasında 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) Kota nedir? (temel öğretim) + kalan kotalar
    user_id = generate_user_id()
    scenarios.append({
        "id": f"teaching_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.TEACHING_MENTORING.value,
        "personality_profile": "empathetic_healthcare_worker",
        "cognitive_state": CognitiveState.EDUCATIONAL.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "'İnternet kotası' nedir? Nasıl kontrol ederim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kota, belirli dönemde kullanabileceğiniz veri hakkıdır. Kalan haklarınıza bakalım.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 75, "voice": 10, "sms": 5}})},
            {"rol": "asistan", "icerik": "Video en çok veri harcar; metin ve ses daha az. Günlük hedef belirleyelim (ör. 1.2 GB).", "arac_cagrilari": None}
        ]
    })

    return scenarios


def generate_teaching_mentoring_scenario() -> List[Dict[str, Any]]:
    """Havuzdaki 10 öğretim & mentorluk senaryosunu döndürür (üst katman sampling yapar)."""
    return generate_teaching_mentoring_scenarios()