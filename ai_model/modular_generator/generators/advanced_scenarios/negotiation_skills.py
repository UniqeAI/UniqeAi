"""
Pazarlık ve Müzakere Becerileri Senaryosu
==========================================

Bu modül, AI'nin pazarlık ve müzakere becerilerini test eden senaryolar üretir.
Kullanıcıların farklı pazarlık stratejileri ve AI'nin bunlara nasıl yanıt verdiği test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    GetCustomerPackageResponse,
    GetRemainingQuotasResponse,
    GetAvailablePackagesResponse,
    ChangePackageResponse,
    GetPackageDetailsResponse,
    GetCurrentBillResponse,
    SetupAutopayResponse,
    TestInternetSpeedResponse,
    EnableRoamingResponse,
    UpdateCustomerContactResponse,
)


def generate_negotiation_skills_scenarios() -> List[Dict[str, Any]]:
    """Müzakere (negotiation) becerileri temasında 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) Sadakat indirimi müzakeresi
    user_id = generate_user_id()
    current_fee = round(random.uniform(80, 120), 2)
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "competitive_sales_professional",
        "cognitive_state": CognitiveState.NEGOTIATIVE.value,
        "emotional_context": EmotionalContext.COMPETITIVE.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": f"3 yıldır müşterinizim, {current_fee} TL ödüyorum. Sadakat indirimi alabilir miyim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Paket ve kullanımınızı inceleyip size özel teklif çıkarıyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_customer_package", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerPackageResponse, {"user_id": user_id, "monthly_fee": current_fee})},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 75, "voice": 30, "sms": 15}})},
            {"rol": "asistan", "icerik": "Sadakat indirimi + düşük ses/SMS kullanımına göre uygun paketle toplam maliyeti düşürebiliriz.", "arac_cagrilari": None}
        ]
    })

    # 2) Rakip fiyat eşleştirme
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "bargain_hunter",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Rakip firma aynı içeriği daha ucuza veriyor. Eşleştirir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Mevcut paketleri listeliyorum; eşdeğer içeriğe özel teklif yapacağım.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [
                {"name": "Eşleştir-Plus", "monthly_fee": 99.9, "features": {"internet_gb": 40, "voice_minutes": 2000, "sms_count": 1000}},
                {"name": "Eşleştir-Pro", "monthly_fee": 109.9, "features": {"internet_gb": 60, "voice_minutes": 3000, "sms_count": 2000}}
            ]})},
            {"rol": "asistan", "icerik": "Eşdeğer paketi eşleştirdim; ayrıca ilk 3 ay %10 ek indirim sunabilirim.", "arac_cagrilari": None}
        ]
    })

    # 3) Paket değişimi ile bütçe optimizasyonu
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "confused_indecisive",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Aylık faturamı 20 TL düşürmek istiyorum; ne yapabiliriz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Paket değişimi ile aylık ücretinizi düşürebiliriz. Uygun değişikliği planlıyorum.", "arac_cagrilari": [{"fonksiyon": "change_package", "parametreler": {"user_id": generate_user_id(), "new_package_name": "Akıllı İnternet"}}]},
            {"rol": "arac", "icerik": create_validated_response(ChangePackageResponse, {"to_package": "Akıllı İnternet", "fee_difference": -20.0, "status": "scheduled"})},
            {"rol": "asistan", "icerik": "Paket değişimi sonraki fatura döneminde geçerli olacak; yaklaşık 20 TL tasarruf sağlanır.", "arac_cagrilari": None}
        ]
    })

    # 4) Lansmana özel paket içeriği müzakeresi
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Upload ağırlıklı lansman haftası için uygun içerik isterim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Paket detaylarını kontrol edip upload odaklı öneri hazırlıyorum.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Launch Pro"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Launch Pro", "features": {"internet_gb": 150, "voice_minutes": 2000, "sms_count": 2000, "international_minutes": 300}})},
            {"rol": "asistan", "icerik": "Launch Pro için lansmana özel %15 indirimle ilerleyebiliriz.", "arac_cagrilari": None}
        ]
    })

    # 5) Otomatik ödeme ile indirim pazarlığı
    user_id = generate_user_id()
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "busy_multitasking",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Otomatik ödeme talimatı verirsem indirim olur mu?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hem faturayı kontrol ediyorum hem de talimatı aktifleştiriyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "setup_autopay", "parametreler": {"user_id": user_id, "status": True}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"user_id": user_id, "status": "unpaid"})},
            {"rol": "arac", "icerik": create_validated_response(SetupAutopayResponse, {"user_id": user_id, "autopay_enabled": True})},
            {"rol": "asistan", "icerik": "Talimat aktif. Otomatik ödeme indirimi +1 ay ek data kampanyası sunabilirim.", "arac_cagrilari": None}
        ]
    })

    # 6) Ping şikayeti eşliğinde indirim/maliyet müzakeresi
    user_id = generate_user_id()
    download = round(random.uniform(20.0, 60.0), 1)
    ping = random.randint(30, 120)
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "impatient_tech_savvy",
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ping yüksek; oyun oynayamıyorum. Fiyatı düşürmezseniz taşınırım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hız testini yapıp, performans iyileştirmesi + ücret önerisi sunacağım.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id, "download_speed_mbps": download, "ping_ms": ping})},
            {"rol": "asistan", "icerik": "Rota optimizasyonu + kablolu öneri ile ping'i düşürelim; ayrıca 3 ay %20 indirim sunuyorum.", "arac_cagrilari": None}
        ]
    })

    # 7) Roaming için fiyat/menfaat müzakeresi
    user_id = generate_user_id()
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "anxious_traveler",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Yurt dışına çıkıyorum; roaming fiyatı yüksek. Avantajlı teklifiniz var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Roaming'i aktif edip uygun paketleri önereceğim.", "arac_cagrilari": [{"fonksiyon": "enable_roaming", "parametreler": {"user_id": user_id, "status": True}}]},
            {"rol": "arac", "icerik": create_validated_response(EnableRoamingResponse, {"user_id": user_id, "roaming_enabled": True})},
            {"rol": "asistan", "icerik": "Roaming aktif. Günlük ücrette indirim + hediye data içeren teklif sunabilirim.", "arac_cagrilari": None}
        ]
    })

    # 8) İletişim kanalı değişimi ile retention teklifi
    user_id = generate_user_id()
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "security_conscious",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Telefon yerine e-postadan iletişim kurarsanız kalmayı düşünebilirim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Tercihinizi kaydediyorum; iletişim kanalınızı güncelliyorum.", "arac_cagrilari": [{"fonksiyon": "update_customer_contact", "parametreler": {"user_id": user_id, "contact_type": "email", "new_value": "kullanici@example.com"}}]},
            {"rol": "arac", "icerik": create_validated_response(UpdateCustomerContactResponse, {"user_id": user_id, "contact_type": "email", "new_value": "kullanici@example.com", "verification_required": True})},
            {"rol": "asistan", "icerik": "E-posta iletişimi aktif. Sadakat indirimi + hediye 5 GB ile devam edelim mi?", "arac_cagrilari": None}
        ]
    })

    # 9) İçerik odaklı paket detay müzakeresi
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "content_creator",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Video ağırlıklı çalışıyorum; upload ve uluslararası dakika önemli.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Paket detaylarını getirip ihtiyaca göre özelleştireceğim.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Creators+"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Creators+", "features": {"internet_gb": 100, "voice_minutes": 1500, "sms_count": 1000, "international_minutes": 200}})},
            {"rol": "asistan", "icerik": "Creators+ üzerinde upload avantajı ve uluslararası dakika artışı için özel fiyat sunabilirim.", "arac_cagrilari": None}
        ]
    })

    # 10) Aşırı kullanım dönemlerinde kota/fiyat balansı
    user_id = generate_user_id()
    scenarios.append({
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "planning",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ayda birkaç gün aşırı kullanıyorum; fiyatı artırmadan nasıl çözebiliriz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kalan kotaları kontrol edip yoğun günler için esnek kota önereceğim.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"internet_remaining_gb": 8.0, "usage_percentage": {"internet": 60, "voice": 20, "sms": 10}})},
            {"rol": "asistan", "icerik": "Aşırı kullanım günlerine özel esnek kota + düşük ücretli add-on ile fiyat artmadan yönetebiliriz.", "arac_cagrilari": None}
        ]
    })

    return scenarios


def generate_negotiation_skills_scenario() -> List[Dict[str, Any]]:
    """Havuzdaki 10 müzakere senaryosunu döndürür (üst katman sampling yapar)."""
    return generate_negotiation_skills_scenarios()
    if not all_scenarios:
        return []
    return all_scenarios