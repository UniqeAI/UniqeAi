"""
Paket Detayları Senaryosu
==========================

Bu modül, kullanıcının paket detaylarını sorguladığı senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import GetPackageDetailsResponse


def generate_package_details_scenario() -> Dict[str, Any]:
    """Kullanıcının paket detaylarını sorguladığı senaryo."""
    package_name = random.choice(["Mega Internet", "Sınırsız Konuşma", "Fiber Evde", "Mobil Pro"])
    return {
        "id": f"package_details_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PACKAGE_DETAILS.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "donguler": [
            {"rol": "kullanici", "icerik": f"'{package_name}' paketinin detaylarını öğrenebilir miyim?"},
            {"rol": "asistan", "icerik": f"Tabii ki! '{package_name}' paketinin tüm detaylarını getiriyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": package_name}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, override_data={"name": package_name})},
            {"rol": "asistan", "icerik": f"'{package_name}' paketinin tüm detayları burada. Aylık ücret, özellikler ve sözleşme koşulları dahil."}
        ]
    } 