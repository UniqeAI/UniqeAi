"""
Standart Senaryo
================

Bu modül, basit, tek adımlı araç çağırma senaryolarını üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import GetRemainingQuotasResponse
from ...lazy_loading import personality_profiles_property


def generate_standard_scenario() -> Dict[str, Any]:
    """Basit, tek adımlı bir araç çağırma senaryosu."""
    user_id = generate_user_id()
    # Lazy loading'den personality profiles'ı çek
    from ...initializers import initialize_enhanced_personality_profiles
    personality_profiles = list(initialize_enhanced_personality_profiles().keys())
    profile_key = random.choice(personality_profiles)
    
    return {
        "id": f"standard_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STANDARD.value,
        "personality_profile": profile_key,
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": f"{user_id} numaralı hattımın kalan internet kotasını öğrenebilir miyim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Elbette, hemen kontrol ediyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, override_data={
                "internet_remaining_gb": round(random.uniform(1, 50), 2),
                "usage_percentage": {
                    "internet": random.randint(20, 95),
                    "voice": random.randint(10, 90), 
                    "sms": random.randint(5, 85)
                }
            })},
            {"rol": "asistan", "icerik": "Mevcut döneminiz için 25.4 GB internetiniz kalmıştır.", "arac_cagrilari": None}
        ]
    } 