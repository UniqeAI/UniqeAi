"""
Çoklu Amaç Senaryosu
=====================

Bu modül, kullanıcının tek mesajda birden fazla talepte bulunduğu senaryoları üretir.
"""

import uuid
import random
from typing import Dict, Any
from ...models import ScenarioType, CognitiveState, EmotionalContext, PersonalityProfile
from ...utils import generate_user_id, create_validated_response
from ...config import API_RESPONSE_MAPPING
from ...telekom_api_schema import GetCurrentBillResponse, PayBillResponse, GetAvailablePackagesResponse, PaymentMethod


def generate_multi_intent_scenario() -> Dict[str, Any]:
    """Kullanıcının tek mesajda birden fazla talepte bulunduğu senaryo."""
    user_id = generate_user_id()
    bill_id = f"F-2024-{user_id}"
    amount = round(random.uniform(200, 300), 2)
    
    return {
        "id": f"multi_intent_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.MULTI_INTENT.value,
        "personality_profile": "tech_savvy_millennial",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.URGENT.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Selam, acil olarak hem faturamı ödemem hem de yurt dışı paketlerini öğrenmem gerekiyor. Haftaya seyahatim var.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Anladım, iki talebinizi de sırayla ve hızlıca hallediyorum. Önce fatura ödemenizle başlayalım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, override_data={"user_id": user_id, "bill_id": bill_id, "amount": amount, "status": "unpaid"})},
            {"rol": "asistan", "icerik": f"{amount} TL borcunuz var. Ödüyorum...", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "pay_bill", "parametreler": {"bill_id": bill_id, "method": PaymentMethod.CREDIT_CARD.value}}]},
            {"rol": "arac", "icerik": create_validated_response(PayBillResponse, override_data={"bill_id": bill_id, "amount": amount, "status": "Ödeme başarılı"})},
            {"rol": "asistan", "icerik": "Ödemeniz tamamlandı. Şimdi yurt dışı paketlerini listeliyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse)},
            {"rol": "asistan", "icerik": "Şu anda 'Haftalık Roaming Paketi' mevcut. 5 GB internet içeriyor. Aktif edelim mi?", "arac_cagrilari": None}
        ]
    } 