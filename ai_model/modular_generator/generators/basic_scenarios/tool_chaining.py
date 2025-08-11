"""
Tool Chaining Senaryosu
=======================

Bu modül, bir aracın çıktısının diğerine girdi olduğu zincirleme senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import GetCurrentBillResponse, PayBillResponse, PaymentMethod


def generate_tool_chaining_scenario() -> Dict[str, Any]:
    """Bir aracın çıktısının diğerine girdi olduğu zincirleme senaryo."""
    user_id = generate_user_id()
    bill_id = f"F-2024-{user_id}"
    amount_to_pay = round(random.uniform(150, 450), 2)

    return {
        "id": f"chaining_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.TOOL_CHAINING.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.URGENT.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": f"{user_id} numaralı hattımın güncel faturasını ödemek istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Tabii, önce güncel fatura tutarınızı kontrol ediyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, override_data={"user_id": user_id, "bill_id": bill_id, "amount": amount_to_pay, "status": "unpaid"})},
            {"rol": "asistan", "icerik": f"Güncel fatura borcunuz {amount_to_pay} TL'dir. Kayıtlı kartınızla ödemeyi onaylıyor musunuz?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Evet, onaylıyorum.", "arac_cagrilari": None},

            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "pay_bill", "parametreler": {"bill_id": bill_id, "method": PaymentMethod.CREDIT_CARD.value}}]},
            {"rol": "arac", "icerik": create_validated_response(PayBillResponse, override_data={"bill_id": bill_id, "amount": amount_to_pay, "status": "Ödeme başarılı"})},
            {"rol": "asistan", "icerik": "Ödemeniz başarıyla tamamlandı. İşlem numaranız: T-....", "arac_cagrilari": None}
        ]
    } 