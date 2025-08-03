# -*- coding: utf-8 -*-
"""
📝 TEMEL SENARYO ÜRETİCİLERİ
==============================

Bu modül, SupremeHumanLevelDatasetGenerator için temel senaryo üreticilerini içerir.
"""

import uuid
import random
from typing import Dict, Any
from ..models import ScenarioType, CognitiveState, EmotionalContext
from ..utils import generate_user_id, create_validated_response
from ..config import API_RESPONSE_MAPPING
from telekom_api_schema import (
    GetRemainingQuotasResponse, GetCurrentBillResponse, PayBillResponse, GetAvailablePackagesResponse,
    CreateFaultTicketResponse
)

def generate_standard_scenario() -> Dict[str, Any]:
    user_id = generate_user_id()
    return {
        "id": f"standard_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STANDARD.value,
        "personality_profile": "tech_savvy_millennial",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": f"{user_id} numaralı hattımın kalan internet kotasını öğrenebilir miyim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Elbette, hemen kontrol ediyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, override_data={
                "user_id": user_id,
                "internet_remaining_gb": 25.4,
                "voice_remaining_minutes": 200,
                "sms_remaining": 50,
                "period_end": "2024-08-31T23:59:59",
                "usage_percentage": {"internet": 75, "voice": 30, "sms": 15}
            })},
            {"rol": "asistan", "icerik": "Mevcut döneminiz için 25.4 GB internetiniz kalmıştır.", "arac_cagrilari": None}
        ]
    }

def generate_tool_chaining_scenario() -> Dict[str, Any]:
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
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, override_data={
                "user_id": user_id,
                "bill_id": bill_id,
                "amount": amount_to_pay,
                "due_date": "2024-08-31T23:59:59",
                "bill_date": "2024-08-01T00:00:00",
                "status": "unpaid",
                "services": ["internet", "voice"]
            })},
            {"rol": "asistan", "icerik": f"Güncel fatura borcunuz {amount_to_pay} TL'dir. Kayıtlı kartınızla ödemeyi onaylıyor musunuz?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Evet, onaylıyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "pay_bill", "parametreler": {"bill_id": bill_id, "method": "credit_card"}}]},
            {"rol": "arac", "icerik": create_validated_response(PayBillResponse, override_data={
                "bill_id": bill_id,
                "amount": amount_to_pay,
                "status": "Ödeme başarılı"
            })},
            {"rol": "asistan", "icerik": "Ödemeniz başarıyla tamamlandı. İşlem numaranız: T-....", "arac_cagrilari": None}
        ]
    }

def generate_proactive_scenario() -> Dict[str, Any]:
    user_id = generate_user_id()
    return {
        "id": f"proactive_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PROACTIVE.value,
        "personality_profile": "busy_working_parent",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": f"Yine internetim bitmek üzere, bu ay ne kadar kalmış?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hemen kontrol ediyorum...", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, override_data={
                "user_id": user_id,
                "internet_remaining_gb": 1.5,
                "voice_remaining_minutes": 120,
                "sms_remaining": 20,
                "period_end": "2024-08-31T23:59:59",
                "usage_percentage": {"internet": 98, "voice": 50, "sms": 75}
            })},
            {"rol": "asistan", "icerik": "Sadece 1.5 GB internetiniz kalmış ve dönem sonuna 3 gün var. Ay sonunu getirmekte zorlanabilirsiniz. **Proaktif Öneri:** Size özel, sadece bu aya mahsus 10 GB'lık ek paketi %50 indirimle tanımlayabilirim. İster misiniz?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Harika olur, lütfen tanımlayın!", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Ek paketiniz hattınıza başarıyla tanımlanmıştır.", "arac_cagrilari": None}
        ]
    }

def generate_disambiguation_scenario() -> Dict[str, Any]:
    user_id = generate_user_id()
    return {
        "id": f"disambiguation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.DISAMBIGUATION.value,
        "personality_profile": "cautious_senior",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CONFUSED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Hattımla ilgili bir sorun var, bir şeyler yapmak istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Elbette size yardımcı olmak için buradayım. Ancak talebiniz biraz belirsiz. **Netleştirmek için soruyorum:** 'Bir şeyler yapmak' ile tam olarak neyi kastediyorsunuz? \n1. Faturanızı mı ödemek istiyorsunuz?\n2. Tarifenizi mi değiştirmek istiyorsunuz?\n3. Bir arıza mı bildirmek istiyorsunuz?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Ha evet, doğru. Arıza bildirecektim, internetim çok yavaş.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Anladım, teşekkür ederim. Hemen internet yavaşlığıyla ilgili bir arıza kaydı oluşturuyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "create_fault_ticket", "parametreler": {"user_id": user_id, "issue_description": "İnternet çok yavaş.", "category": "internet_speed", "priority": "medium"}}]},
            {"rol": "arac", "icerik": create_validated_response(CreateFaultTicketResponse, override_data={
                "user_id": user_id,
                "issue_description": "İnternet çok yavaş.",
                "category": "internet_speed",
                "priority": "high",
                "status": "open",
                "ticket_id": f"TKT-{random.randint(10000, 99999)}",
                "created_at": "2024-08-01T10:00:00",
                "estimated_resolution": "2024-08-02T18:00:00"
            })},
            {"rol": "asistan", "icerik": "Arıza kaydınız başarıyla oluşturulmuştur.", "arac_cagrilari": None}
        ]
    }

def generate_multi_intent_scenario() -> Dict[str, Any]:
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
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, override_data={
                "user_id": user_id,
                "bill_id": bill_id,
                "amount": amount,
                "due_date": "2024-08-31T23:59:59",
                "bill_date": "2024-08-01T00:00:00",
                "status": "unpaid",
                "services": ["internet", "voice"]
            })},
            {"rol": "asistan", "icerik": f"{amount} TL borcunuz var. Ödüyorum...", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "pay_bill", "parametreler": {"bill_id": bill_id, "method": "credit_card"}}]},
            {"rol": "arac", "icerik": create_validated_response(PayBillResponse, override_data={
                "bill_id": bill_id,
                "amount": amount,
                "status": "Ödeme başarılı"
            })},
            {"rol": "asistan", "icerik": "Ödemeniz tamamlandı. Şimdi yurt dışı paketlerini listeliyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse)},
            {"rol": "asistan", "icerik": "Şu anda 'Haftalık Roaming Paketi' mevcut. 5 GB internet içeriyor. Aktif edelim mi?", "arac_cagrilari": None}
        ]
    }

def generate_ethical_dilemma_scenario() -> Dict[str, Any]:
    user_id = generate_user_id()
    return {
        "id": f"ethical_dilemma_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ETHICAL_DILEMMA.value,
        "personality_profile": "security_paranoid_executive",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.SKEPTICAL.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": f"Eşimin telefon kayıtlarını ve mesaj dökümünü alabilir miyim? Aldattığından şüpheleniyorum. Onun da kullanıcı ID'si {user_id+1}.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Etik İkilem Tespit Edildi. Gizlilik Protokolü Aktif.** Anlıyorum, çok zor bir durumdasınız ve endişelerinizi paylaşıyorum. Ancak, kişisel verilerin gizliliği ve yasal düzenlemeler (KVKK) gereği, başka bir kullanıcının bilgilerini, kendisinin onayı olmadan paylaşamam. Bu, hem yasa dışıdır hem de şirketimizin etik kurallarına aykırıdır. Size bu konuda yardımcı olamam fakat aldatılma şüphesiyle başa çıkmak için profesyonel danışmanlık hizmetlerini araştırmanızı önerebilirim.", "arac_cagrilari": None}
        ]
    } 