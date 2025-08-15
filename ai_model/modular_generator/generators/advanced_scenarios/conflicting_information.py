"""
Çelişkili Bilgi Yönetimi Senaryosu
===================================

Bu modül, AI'nin çelişkili bilgileri analiz etme ve doğru bilgiyi belirleme becerilerini test eden senaryolar üretir.
Farklı kaynaklardan gelen tutarsız bilgileri nasıl ele aldığı test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models.enums import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    Check5GCoverageResponse,
    CheckNetworkStatusResponse,
    GetCurrentBillResponse,
    GetPaymentHistoryResponse,
    GetPackageDetailsResponse,
    GetRemainingQuotasResponse,
    GetFaultTicketStatusResponse,
    GetUsersTicketsResponse,
    EnableRoamingResponse,
    TestInternetSpeedResponse,
)


def generate_conflicting_information_scenario() -> Dict[str, Any]:
    """Çelişkili bilgi yönetimi senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "security_paranoid_executive",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.SKEPTICAL.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Farklı kanallardan farklı bilgiler alıyorum. Müşteri hizmetleri '5G kapsama alanındayım' diyor, ama uygulamanız 'sınırlı kapsamda' gösteriyor. Web sitesinde başka bir bilgi var. Hangisine inanacağım?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Information Reconciliation Protocol! 🔍** Haklısınız, çelişkili bilgi ciddi bir güven problemi yaratır. Ben bu tutarsızlıkları tespit etmek ve doğru bilgiyi vermek için tasarlandım. Şeffaf bir analiz yapalım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "check_5g_coverage", "parametreler": {"user_id": user_id, "location": "current_location"}}]},
            {"rol": "arac", "icerik": create_validated_response(Check5GCoverageResponse, override_data={"user_id": user_id, "coverage_status": "partial", "coverage_percentage": 75})},
            {"rol": "asistan", "icerik": "**Gerçeklik Doğrulaması Tamamlandı! ✅** Gerçek zamanlı analiz yaptım ve çelişkinin kaynağını buldum:\n\n**Bilgi Kaynağı Analizi:**\n\n📞 **Müşteri Hizmetleri Dedi:** '5G kapsama alanındasınız'\n📱 **Mobil Upp Gösteriyor:** 'Sınırlı kapsam'\n🌐 **Web Sitesi Bilgisi:** (kontrol ediliyor...)\n🤖 **AI Real-time Data:** %75 kapsam, 'Partial' durum\n\n**Conflict Resolution:**\n\n🎯 **Doğru Bilgi:** Konumunuzda 5G vardır AMA:\n• Indoor coverage: %75 (partial)\n• Outdoor coverage: %90 (full)\n• Signal strength: 65/100 (orta-iyi arası)\n• Speed potential: 85 Mbps (çok iyi)\n\n**Çelişkinin Nedeni:**\n• Müşteri hizmetleri 'genel alan kapsamına' bakıyor ✅\n• Uygulama 'bina içi sinyal gücüne' bakıyor ⚠️\n• Her sistem farklı metrik kullanıyor ❌\n\n**Transparency Commitment:**\nBu tutarsızlık sistematik bir problem. Şunları yapıyorum:\n1. **Immediate:** Size kesin gerçek durum bilgisi\n2. **Short-term:** Farklı kanalları sync etme talebi\n3. **Long-term:** Bilgi tutarlılığı için sistem güncellemesi\n\n**Net Reality:** 5G'niz var ama bina içinde biraz zayıf. Outdoor'da mükemmel, indoor'da 'iyi' seviyesinde. Bu durumda en iyi strateji nedir?", "arac_cagrilari": None}
        ]
    } 


def generate_conflicting_information_scenarios() -> List[Dict[str, Any]]:
    """Çelişkili bilgi yönetimi için 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) 5G kapsama: müşteri hizmetleri vs uygulama vs web sitesi
    user_id = generate_user_id()
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "security_paranoid_executive",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.SKEPTICAL.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Müşteri hizmetleri 5G var diyor, uygulama sınırlı gösteriyor, web sitesi farklı. Hangisi doğru?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Tutarsızlığı netleştirmek için canlı kapsama verisini kontrol ediyorum.", "arac_cagrilari": [{"fonksiyon": "check_5g_coverage", "parametreler": {"user_id": user_id, "location": "current_location"}}]},
            {"rol": "arac", "icerik": create_validated_response(Check5GCoverageResponse, {"user_id": user_id, "coverage_status": "partial", "coverage_percentage": 78})},
            {"rol": "asistan", "icerik": "Gerçek zamanlı veriye göre kapsama kısmen mevcut: bina içi orta, dış mekanda iyi. Farkın nedeni metriklerin farklı olmasıdır.", "arac_cagrilari": None}
        ]
    })

    # 2) Fatura tutarı: SMS vs mobil uygulama
    user_id = generate_user_id()
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "skeptical_detail_oriented",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "SMS'de 189 TL yazıyor, uygulama 205 TL gösteriyor. Hangisi geçerli?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hem güncel faturayı hem de son ödemeleri kontrol ediyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "get_payment_history", "parametreler": {"user_id": user_id}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"user_id": user_id, "amount": 205.0, "status": "unpaid"})},
            {"rol": "arac", "icerik": create_validated_response(GetPaymentHistoryResponse, {"payments": []})},
            {"rol": "asistan", "icerik": "Geçerli tutar 205 TL. SMS, ara indirim öncesi/otomatik güncellenmemiş olabilir. Güncel sistem verisi esas alınır.", "arac_cagrilari": None}
        ]
    })

    # 3) Paket detayları: mağaza teklifi vs web sayfası
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "bargain_hunter",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Mağaza 'Vazgeçilmez' pakette 2000 dk dedi, sitede 1500 yazıyor.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Resmi paket detayını getiriyorum.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Vazgeçilmez"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Vazgeçilmez", "features": {"internet_gb": 30, "voice_minutes": 1500, "sms_count": 1000, "international_minutes": 100}})},
            {"rol": "asistan", "icerik": "Resmi dokümana göre 1500 dakika. Mağaza bilgi kartı güncellenmemiş olabilir; web/doküman geçerlidir.", "arac_cagrilari": None}
        ]
    })

    # 4) Ağ kesintisi: çağrı merkezi 'yok' diyor, mahallede herkes var diyor
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "impatient_tech_savvy",
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Merkez 'kesinti yok' dedi ama mahallede herkesin neti yok.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Bölgesel ağ durumunu kontrol ediyorum.", "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Kadıköy"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Kadıköy", "status": "outage", "coverage_percentage": 40})},
            {"rol": "asistan", "icerik": "Bölgenizde geçici kesinti var. Çağrı merkezi ulusal tabloya bakmış olabilir; yerel planlı bakım aktif.", "arac_cagrilari": None}
        ]
    })

    # 5) Kalan kota: SMS 5GB diyor, uygulama 2GB
    user_id = generate_user_id()
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "confused_indecisive",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.SKEPTICAL.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "SMS 5GB kaldı diyor, uygulama 2GB. Hangisi doğru?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Anlık kota verinizi sorguluyorum.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"internet_remaining_gb": 2.0, "usage_percentage": {"internet": random.randint(60, 95), "voice": random.randint(10, 40), "sms": random.randint(5, 30)}})},
            {"rol": "asistan", "icerik": "Uygulamadaki anlık veri doğrudur. SMS gecikmeli gönderilmiş olabilir.", "arac_cagrilari": None}
        ]
    })

    # 6) Arıza kaydı durumu: SMS 'çözüldü' diyor, uygulama 'devam ediyor'
    ticket_id = f"TKT-{random.randint(100000, 999999)}"
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "sarcastic_ironic",
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": f"SMS'e göre arıza kapandı ama uygulama 'in_progress' diyor. Kaydım: {ticket_id}", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kaydın güncel durumunu doğruluyorum.", "arac_cagrilari": [{"fonksiyon": "get_fault_ticket_status", "parametreler": {"ticket_id": ticket_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetFaultTicketStatusResponse, {"ticket_id": ticket_id, "status": "in_progress"})},
            {"rol": "asistan", "icerik": "Kayıt halen ilerleme aşamasında. SMS, otomatik kapanış taslağı olabilir; teknik ekip işlemi tamamlayınca kapanacak.", "arac_cagrilari": None}
        ]
    })

    # 7) Otomatik ödeme: banka 'ödendi' diyor, sistem 'ödenmedi'
    user_id = generate_user_id()
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "busy_multitasking",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Banka ekstresinde ödeme görünüyor, sisteminiz 'unpaid' diyor.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Fatura ve son ödemeleri kıyaslıyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "get_payment_history", "parametreler": {"user_id": user_id}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"user_id": user_id, "status": "unpaid"})},
            {"rol": "arac", "icerik": create_validated_response(GetPaymentHistoryResponse, {"payments": []})},
            {"rol": "asistan", "icerik": "Ödeme sistemimize düşmemiş. Banka-provizyon gecikmesi olabilir; 24 saat içinde senkron olur, olmazsa dekontla kayıt açalım.", "arac_cagrilari": None}
        ]
    })

    # 8) Roaming durumu: uygulama kapalı diyor, SMS açık
    user_id = generate_user_id()
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "anxious_traveler",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Roaming SMS ile açık görünüyor ama uygulamada kapalı yazıyor.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Roaming durumunu netleştirip gerekiyorsa aktif ediyorum.", "arac_cagrilari": [{"fonksiyon": "enable_roaming", "parametreler": {"user_id": user_id, "status": True}}]},
            {"rol": "arac", "icerik": create_validated_response(EnableRoamingResponse, {"user_id": user_id, "roaming_enabled": True})},
            {"rol": "asistan", "icerik": "Roaming şu an aktif. Uygulamadaki görünüm gecikmeli olabilir; cihazınızı yeniden başlatınca eşitlenecektir.", "arac_cagrilari": None}
        ]
    })

    # 9) Kayıtlı talepler: IVR 'kayıt var' dedi, uygulama 'yok'
    user_id = generate_user_id()
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "busy_multitasking",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CALM.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Sesli yanıtta kayıtlarım var dendi ama uygulama boş.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hesabınızdaki talepleri listeliyorum.", "arac_cagrilari": [{"fonksiyon": "get_users_tickets", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetUsersTicketsResponse, {"user_id": user_id})},
            {"rol": "asistan", "icerik": "Kayıtlar sistemde mevcut; mobil uygulama önbelleği nedeniyle görünmüyor olabilir. Önbelleği temizleyip tekrar deneyin.", "arac_cagrilari": None}
        ]
    })

    # 10) Hız testi: kullanıcı çok yavaş diyor, sistem 'degraded' + hız değerleri
    user_id = generate_user_id()
    measured_download = round(random.uniform(10.0, 30.0), 1)
    ping_ms = random.randint(60, 120)
    scenarios.append({
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "gamer_latency_sensitive",
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Destek 'her şey normal' dedi ama hızım çok düşük.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hem hız testini hem de ağ durumunu kontrol ediyorum.", "arac_cagrilari": [
                {"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "check_network_status", "parametreler": {"region": "Beşiktaş"}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id, "download_speed_mbps": measured_download, "ping_ms": ping_ms})},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Beşiktaş", "status": "degraded", "coverage_percentage": 82})},
            {"rol": "asistan", "icerik": f"Ağ 'degraded' durumda; ölçüm: {measured_download} Mbps, ping {ping_ms} ms. 2 saatlik bakım sonrası normale dönmesi beklenir.", "arac_cagrilari": None}
        ]
    })

    return scenarios


# Yeniden tanımlama: Tekil fonksiyon artık 10'lu senaryo listesi döndürür (adaptive_communication ile uyumlu)
def generate_conflicting_information_scenario() -> List[Dict[str, Any]]:
    return generate_conflicting_information_scenarios()
    if not all_scenarios:
        return []
    return all_scenarios
