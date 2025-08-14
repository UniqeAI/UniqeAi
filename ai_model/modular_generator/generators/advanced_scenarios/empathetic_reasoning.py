"""
Empatik Akıl Yürütme Senaryosu
===============================

Bu modül, AI'nin empatik akıl yürütme ve duygusal zeka becerilerini test eden senaryolar üretir.
Kullanıcıların duygusal durumlarını anlama ve uygun yanıt verme becerisi test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    GetCurrentBillResponse,
    GetCustomerProfileResponse,
    GetPaymentHistoryResponse,
    UpdateCustomerContactResponse,
    CreateFaultTicketResponse,
    GetFaultTicketStatusResponse,
    TestInternetSpeedResponse,
    CheckNetworkStatusResponse,
    SuspendLineResponse,
    ReactivateLineResponse,
    SetupAutopayResponse,
)


def generate_empathetic_reasoning_scenarios() -> List[Dict[str, Any]]:
    """Empatik (vurgulu) muhakeme temalı 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) Hasta yakını için fatura kaygısı (basit anlatım + fatura)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "empathetic_healthcare_worker",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Annem hasta, faturam kabarık geldi. Onu üzmeden çözmek istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Sizi ve annenizi önemsiyorum. Önce faturayı kontrol edip, sonra uygun bir çözüm bulalım.", "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"user_id": user_id, "status": "unpaid"})},
            {"rol": "asistan", "icerik": "Faturanızı birlikte sade bir dille gözden geçirelim ve uygun taksit/indirim seçeneklerine bakalım.", "arac_cagrilari": None}
        ]
    })

    # 2) Yakın kaybı sonrası işlemler (profil bakımı, hassas iletişim)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "empathetic_healthcare_worker",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.GRIEF.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Babamı kaybettim, abonelik işlemlerini nasıl halledeceğimi bilmiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Başınız sağ olsun. Süreci sizin temponuzda, en hassas biçimde yöneteceğim. Önce profil bilgilerini kontrol ediyorum.", "arac_cagrilari": [{"fonksiyon": "get_customer_profile", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerProfileResponse, {"user_id": user_id})},
            {"rol": "asistan", "icerik": "Faturalandırmayı durdurabilir, hattı anı olarak bir süre saklayabiliriz. Hazır olduğunuzda ilerleriz.", "arac_cagrilari": None}
        ]
    })

    # 3) Kaygı azaltma: Otomatik ödeme ayarı
    user_id = generate_user_id()
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "busy_multitasking",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.OVERWHELMED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ödemeleri hep unutuyorum, stres oluyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Stresinizi azaltmak için otomatik ödeme talimatı oluşturuyorum.", "arac_cagrilari": [{"fonksiyon": "setup_autopay", "parametreler": {"user_id": user_id, "status": True}}]},
            {"rol": "arac", "icerik": create_validated_response(SetupAutopayResponse, {"user_id": user_id, "autopay_enabled": True})},
            {"rol": "asistan", "icerik": "Tamamdır. Artık son ödeme tarihi kaygısı olmadan içiniz rahat olabilir.", "arac_cagrilari": None}
        ]
    })

    # 4) Duygusal yük altında hız sorunu (terapi/online görüşme)
    user_id = generate_user_id()
    download = round(random.uniform(8.0, 25.0), 1)
    ping = random.randint(60, 150)
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "security_conscious",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.ANXIOUS.value if hasattr(EmotionalContext, 'ANXIOUS') else EmotionalContext.WORRIED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Online terapi görüşmelerimde bağlantı kopuyor, çok kaygılanıyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Sizi anlıyorum. Hemen hız testini başlatıp durumu birlikte çözelim.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id, "download_speed_mbps": download, "ping_ms": ping})},
            {"rol": "asistan", "icerik": "Görüşme saatlerinizi daha stabil saatlere kaydırmanızı ve mümkünse kablolu bağlantı kullanmanızı öneriyorum.", "arac_cagrilari": None}
        ]
    })

    # 5) Uzun süren arıza—duygusal yıpranma (kayıt + durum takibi)
    user_id = generate_user_id()
    ticket_id = f"TKT-{random.randint(100000, 999999)}"
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "sarcastic_ironic",
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Günlerdir internet yok, işimi yapamıyorum. Çok yoruldum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Haklısınız, bu çok yıpratıcı. Hemen acil öncelikli bir kayıt açıyorum.", "arac_cagrilari": [{"fonksiyon": "create_fault_ticket", "parametreler": {"user_id": user_id, "issue_description": "Uzun süren kesinti", "category": "connection_loss", "priority": "urgent"}}]},
            {"rol": "arac", "icerik": create_validated_response(CreateFaultTicketResponse, {"ticket_id": ticket_id, "priority": "urgent"})},
            {"rol": "asistan", "icerik": "Kaydınızı açtım. Şimdi durumunuzu da takip ediyorum.", "arac_cagrilari": [{"fonksiyon": "get_fault_ticket_status", "parametreler": {"ticket_id": ticket_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetFaultTicketStatusResponse, {"ticket_id": ticket_id, "status": "in_progress"})},
            {"rol": "asistan", "icerik": "Takipteyim; gelişmeleri düzenli olarak paylaşacağım. Önceliğiniz bizde.", "arac_cagrilari": None}
        ]
    })

    # 6) Göç—geçici dondurma talebi (yük azaltma)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "planning",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "3 ay yurt dışındayım; masrafları azaltmak için hattı dondurmak istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Elbette, dönüşünüze kadar güvenle donduralım.", "arac_cagrilari": [{"fonksiyon": "suspend_line", "parametreler": {"user_id": user_id, "reason": "Geçici yurt dışı"}}]},
            {"rol": "arac", "icerik": create_validated_response(SuspendLineResponse, {"user_id": user_id, "suspension_reason": "Geçici yurt dışı"})},
            {"rol": "asistan", "icerik": "Hattınız güvenle donduruldu. Döndüğünüzde tek dokunuşla aktifleştiririz.", "arac_cagrilari": None}
        ]
    })

    # 7) Dönüş—yumuşak yeniden başlatma (reaktivasyon kaygısız)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "happy_satisfied",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Döndüm, hattımı sorunsuz açmak istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hoş geldiniz! Hemen aktifleştiriyorum.", "arac_cagrilari": [{"fonksiyon": "reactivate_line", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(ReactivateLineResponse, {"user_id": user_id, "reactivation_fee": 0.0})},
            {"rol": "asistan", "icerik": "Hattınız ek ücret olmadan aktifleştirildi. İyi dönüşler!", "arac_cagrilari": None}
        ]
    })

    # 8) Hassas veri—iletişim kanalı güncelleme (güvende hissettirme)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "security_conscious",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Telefonla aranmak beni geriyor; e-postayı tercih ediyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Tercihinizi saygıyla kaydediyorum; e-posta iletişimini etkinleştiriyorum.", "arac_cagrilari": [{"fonksiyon": "update_customer_contact", "parametreler": {"user_id": user_id, "contact_type": "email", "new_value": "kullanici@example.com"}}]},
            {"rol": "arac", "icerik": create_validated_response(UpdateCustomerContactResponse, {"user_id": user_id, "contact_type": "email", "new_value": "kullanici@example.com", "verification_required": True})},
            {"rol": "asistan", "icerik": "Artık sizi yalnızca e-posta üzerinden bilgilendireceğiz.", "arac_cagrilari": None}
        ]
    })

    # 9) Birikmiş ödeme stresi—şeffaflık ve çözüm
    user_id = generate_user_id()
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "confused_indecisive",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.ANXIOUS.value if hasattr(EmotionalContext, 'ANXIOUS') else EmotionalContext.WORRIED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ödemelerim birikti, ne kadar borcum kaldığını bilemiyorum ve panik oluyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Sizi anlıyorum. Önce geçmiş ödemelerinizi kontrol edip net bir tablo çıkarıyorum.", "arac_cagrilari": [{"fonksiyon": "get_payment_history", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPaymentHistoryResponse, {"payments": []})},
            {"rol": "asistan", "icerik": "Tüm rakamları açıkça paylaşacağım ve size en düşük stresli ödeme planını önereceğim.", "arac_cagrilari": None}
        ]
    })

    # 10) Bölgesel sorun—duygusal güvence (durum bilgilendirmesi)
    scenarios.append({
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "elderly_non_tech",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.CONFUSED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Mahallede herkes bağlantıdan şikayetçi, endişelendim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Sizi rahatlatmak için bölge durumunu kontrol edip açıkça anlatacağım.", "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Üsküdar"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Üsküdar", "status": "operational"})},
            {"rol": "asistan", "icerik": "Altyapı çalışıyor. Her şeyi anlaşılır bir dille adım adım anlatacağım; dilediğinizde arayabilirsiniz.", "arac_cagrilari": None}
        ]
    })

    return scenarios

def generate_empathetic_reasoning_scenario() -> List[Dict[str, Any]]:
    """Havuzdaki 10 empatik senaryoyu döndürür (üst katman sampling yapar)."""
    return generate_empathetic_reasoning_scenarios()
    if not all_scenarios:
        return []
    return all_scenarios