"""
Stratejik Planlama Senaryosu
============================

Bu modül, AI'nin stratejik planlama ve uzun vadeli düşünme becerilerini test eden senaryolar üretir.
Kullanıcıların gelecek odaklı ihtiyaçlarını nasıl analiz ettiği test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    LearningAdaptationResponse,
    GetAvailablePackagesResponse,
    GetPackageDetailsResponse,
    CheckNetworkStatusResponse,
    TestInternetSpeedResponse,
    GetRemainingQuotasResponse,
    GetCurrentBillResponse,
    GetPastBillsResponse,
    GetCustomerPackageResponse,
)


def generate_strategic_planning_scenario() -> Dict[str, Any]:
    """Stratejik planlama senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "İş modelimiz değişiyor. Önümüzdeki 2 yıl içinde ekibi 3 kişiden 25 kişiye çıkaracağız. Hem remote hem office hybrid çalışma olacak. Uzun vadeli telecom stratejisi nasıl olmalı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Strategic Planning Mode Activated! 📊** Mükemmel bir büyüme hikayesi! 8x büyüme + hybrid model = kompleks ama heyecan verici bir strategic planning challenge. Predictive modeling ile 2-yıllık roadmap tasarlayalım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "update_learning_adaptation", "parametreler": {"user_id": generate_user_id()}}]},
            {"rol": "arac", "icerik": create_validated_response(LearningAdaptationResponse, override_data={"user_id": generate_user_id(), "personalization_level": "strategic_growth"})},
            {"rol": "asistan", "icerik": "**Stratejik Yol Haritası Oluşturuldu! 🎯**\n\n**2-Yıllık Büyüme Stratejisi Çerçevesi:**\n\n```\n📈 Ölçeklendirme Zaman Çizelgesi:\nÇ1-Ç2 2024: 3→8 kişi (Temel Aşama)\nÇ3-Ç4 2024: 8→15 kişi (Büyüme Aşaması)  \nÇ1-Ç2 2025: 15→20 kişi (Maturity Phase)\nQ3-Q4 2025: 20→25 kişi (Optimization Phase)\n```\n\n**Phase-Gate Telecom Architecture:**\n\n🏗️ **Foundation Phase (Q1-Q2):**\n• Base Infrastructure: 500 GB business pool\n• Hybrid Setup: Office fiber + remote LTE backup\n• Cost: 850 TL/ay (kişi başı 106 TL)\n• KPI: <2ms office latency, >50 Mbps remote\n\n📊 **Growth Phase (Q3-Q4):**\n• Scaling Infrastructure: 1.2 TB adaptive pool\n• Smart Allocation: AI-driven bandwidth management\n• Cost: 1,650 TL/ay (kişi başı 110 TL) - efficiency gain\n• KPI: 99.5% uptime, predictive scaling accuracy\n\n🚀 **Maturity + Optimization (2025):**\n• Enterprise Infrastructure: Unlimited strategic pool\n• Advanced Analytics: Performance prediction models\n• Cost: 2,200 TL/ay (kişi başı 88 TL) - scale economies\n• KPI: Proactive issue resolution, 360° connectivity\n\n**Strategic Innovation Elements:**\n• **Predictive Scaling:** Hiring prediction → automatic capacity increase\n• **Hybrid Optimization:** AI learns office/remote patterns\n• **Cost Intelligence:** Dynamic pricing based on actual usage\n• **Future-Proofing:** 6G readiness, IoT integration capability\n\n**ROI Projections:**\n• Traditional approach: 3,500 TL/ay by 2025\n• Strategic approach: 2,200 TL/ay by 2025\n• Net savings: 15,600 TL/year + 40% productivity boost\n\nHangi phase'den başlayalım? Detailed implementation plan oluşturalım mı?", "arac_cagrilari": None}
        ]
    }  


def generate_strategic_planning_scenarios() -> List[Dict[str, Any]]:
    """Stratejik planlama temalı 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) Startup ölçekleme (2 yıl strateji) + öğrenme adaptasyonu
    su1 = generate_user_id()
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ekibimiz 2 yılda 3→25 kişi olacak; hybrid çalışma. Uzun vadeli telecom stratejisi?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Strateji motoru devrede. Öğrenme adaptasyonunuzu güncelliyorum.", "arac_cagrilari": [{"fonksiyon": "update_learning_adaptation", "parametreler": {"user_id": su1}}]},
            {"rol": "arac", "icerik": create_validated_response(LearningAdaptationResponse, {"user_id": su1})},
            {"rol": "asistan", "icerik": "Foundation→Growth→Optimization fazlarıyla ölçeklenebilir, hibrit dostu plan öneriyorum.", "arac_cagrilari": None}
        ]
    })

    # 2) Kurumsal ofis + remote politika (hız testi + ağ durumu)
    su2 = generate_user_id()
    dl = round(random.uniform(50.0, 150.0), 1)
    ping = random.randint(8, 25)
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "enterprise_it_manager",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Remote+ofis modelde SLA hedeflerini belirleyelim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Ölçüm ve bölgesel ağı kontrol ederek politika tasarlayacağım.", "arac_cagrilari": [
                {"fonksiyon": "test_internet_speed", "parametreler": {"user_id": su2}},
                {"fonksiyon": "check_network_status", "parametreler": {"region": "Maslak"}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": su2, "download_speed_mbps": dl, "ping_ms": ping})},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Maslak"})},
            {"rol": "asistan", "icerik": "Öneri SLA: down>100 Mbps, ping<20 ms; yoğun saatlerde QoS ve rota yedekleme.", "arac_cagrilari": None}
        ]
    })

    # 3) Paket sepeti stratejisi (mevcut + alternatifler)
    su3 = generate_user_id()
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "strategic_procurement",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ekipler için paket sepeti nasıl olmalı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Mevcut paketi ve alternatifleri kıyaslıyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_customer_package", "parametreler": {"user_id": su3}},
                {"fonksiyon": "get_available_packages", "parametreler": {}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerPackageResponse)},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse)},
            {"rol": "asistan", "icerik": "Çekirdek + modüler eklenti yaklaşımı ile esnek sepet öneriyorum.", "arac_cagrilari": None}
        ]
    })

    # 4) Bütçe planlama (güncel+geçmiş fatura)
    su4 = generate_user_id()
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "finance_controller",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Önümüzdeki yıl için telecom bütçe tahmini çıkaralım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Güncel ve geçmiş faturaya bakıp trend oluşturuyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_current_bill", "parametreler": {"user_id": su4}},
                {"fonksiyon": "get_past_bills", "parametreler": {"user_id": su4, "limit": 12}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"user_id": su4})},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse)},
            {"rol": "asistan", "icerik": "Aylık ortalama + mevsimsellik ile yıllık bütçe; %10 güvenlik payı önerilir.", "arac_cagrilari": None}
        ]
    })

    # 5) Kota stratejisi (kalan haklar)
    su5 = generate_user_id()
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "operations_planner",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Kota kullanımını ay bazında optimize edelim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kalan hakları kontrol edip çerçeve plan çıkarıyorum.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": su5}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 45, "voice": 20, "sms": 15}})},
            {"rol": "asistan", "icerik": "Haftalık hedefler + yoğunluk saatleri için esnek politika öneriyorum.", "arac_cagrilari": None}
        ]
    })

    # 6) 5G/FTTH geçiş planı (paket detayı)
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "technology_lead",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "5G/FTTH geçişi için uygun paket detayı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Örnek ileri seviye paket detayını getiriyorum.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Enterprise Fiber 5G"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Enterprise Fiber 5G", "monthly_fee": 249.90, "setup_fee": 0.0, "features": {"internet_gb": 200, "voice_minutes": 3000, "sms_count": 2000, "international_minutes": 300}, "contract_duration": 24, "cancellation_fee": 150.0})},
            {"rol": "asistan", "icerik": "Geçişte köprü çözümü; kurumsal SLA uyumlu.", "arac_cagrilari": None}
        ]
    })

    # 7) Bölge bazlı kapasite planlama (ağ durumu)
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "regional_manager",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "3 bölgede yeni ofis açacağız, kapasite planı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Bölgesel ağ durumunu kontrol ediyorum.", "arac_cagrilari": [
                {"fonksiyon": "check_network_status", "parametreler": {"region": "Ankara"}},
                {"fonksiyon": "check_network_status", "parametreler": {"region": "İzmir"}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Ankara"})},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "İzmir"})},
            {"rol": "asistan", "icerik": "Ankara: sabit fiber; İzmir: hibrit çözüm öneriyorum.", "arac_cagrilari": None}
        ]
    })

    # 8) Uzaktan çalışma için hız politikası
    su8 = generate_user_id()
    spd = round(random.uniform(30.0, 100.0), 1)
    pms = random.randint(15, 40)
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "people_ops",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Remote çalışanlar için minimum hız/ping hedefleri?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Örnek ölçüm alıp eşik belirliyorum.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": su8}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": su8, "download_speed_mbps": spd, "ping_ms": pms})},
            {"rol": "asistan", "icerik": "Öneri: down≥50 Mbps, ping≤25 ms; altı otomatik eskalasyon.", "arac_cagrilari": None}
        ]
    })

    # 9) Yıl ortası paket revizyonu (liste + detay)
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "product_owner",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Yıl ortası paket revizyonu için öneriniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Paketleri ve örnek detayını paylaşıyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_available_packages", "parametreler": {}},
                {"fonksiyon": "get_package_details", "parametreler": {"package_name": "Strategic Plus"}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse)},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Strategic Plus", "monthly_fee": 179.90, "setup_fee": 0.0, "features": {"internet_gb": 100, "voice_minutes": 2000, "sms_count": 1000, "international_minutes": 100}, "contract_duration": 12, "cancellation_fee": 90.0})},
            {"rol": "asistan", "icerik": "Strategic Plus büyüyen ekipler için dengeli bir seçim.", "arac_cagrilari": None}
        ]
    })

    # 10) Sürdürülebilirlik ve maliyet verimliliği
    su10 = generate_user_id()
    scenarios.append({
        "id": f"strategic_planning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.STRATEGIC_PLANNING.value,
        "personality_profile": "sustainability_lead",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Sürdürülebilirlik ile maliyet verimliliğini dengeleyelim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kalan kotalar ve geçmiş faturaya bakarak plan çıkarıyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": su10}},
                {"fonksiyon": "get_past_bills", "parametreler": {"user_id": su10, "limit": 6}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 40, "voice": 18, "sms": 10}})},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse)},
            {"rol": "asistan", "icerik": "Yıllık %15 tasarruf hedefi gerçekçi; kaliteyi koruyarak optimizasyon yapılabilir.", "arac_cagrilari": None}
        ]
    })

    return scenarios


def generate_strategic_planning_scenario() -> List[Dict[str, Any]]:
    """Havuzdaki 10 stratejik planlama senaryosunu döndürür (üst katman sampling yapar)."""
    return generate_strategic_planning_scenarios()