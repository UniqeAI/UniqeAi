"""
Hata Yanıtı Senaryosu
======================

Bu modül, API'den bir hata döndüğünde AI'ın bunu nasıl yönettiğini gösteren senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import ErrorResponse, PaymentMethod


def generate_error_response_scenario() -> Dict[str, Any]:
    """API'den bir hata döndüğünde AI'ın bunu nasıl yönettiğini gösteren senaryo."""
    user_id = generate_user_id()
    # Geçerli bill_id formatında ama sistemde olmayan fatura numarası
    fake_bill_id = f"F-2024-{random.randint(100000, 999999)}"
    
    return {
        "id": f"error_response_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ERROR_RESPONSE.value,
        "personality_profile": "tech_savvy_millennial",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": f"{fake_bill_id} numaralı faturamı ödemek istiyorum."},
            {"rol": "asistan", "icerik": "Hemen deniyorum."},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "pay_bill", "parametreler": {"bill_id": fake_bill_id, "method": PaymentMethod.CREDIT_CARD.value}}]},
            {"rol": "arac", "icerik": create_validated_response(ErrorResponse, override_data={"success": False, "error": {"code": "INVALID_BILL_ID", "message": "Geçersiz fatura numarası.", "details": f"Fatura '{fake_bill_id}' sistemde bulunamadı."}})},
            {"rol": "asistan", "icerik": f"Üzgünüm, bir sorun oluştu. Girdiğiniz '{fake_bill_id}' numaralı fatura sistemde bulunamadı. Lütfen fatura numarasını kontrol edip tekrar dener misiniz?"}
        ]
    } 