"""
İnovasyon Düşüncesi Senaryosu
=============================

Bu modül, AI'nin inovasyon ve yaratıcı düşünme becerilerini test eden senaryolar üretir.
Kullanıcıların yaratıcı problem çözme süreçlerinde AI'nin nasıl destek verdiği test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    CulturalContextResponse,
    GetAvailablePackagesResponse,
    GetPackageDetailsResponse,
    GetRemainingQuotasResponse,
    TestInternetSpeedResponse,
    CheckNetworkStatusResponse,
    Check5GCoverageResponse,
    LearningAdaptationResponse,
    ActivateEmergencyServiceResponse,
)


def generate_innovation_thinking_scenario() -> Dict[str, Any]:
    """İnovasyon düşüncesi senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.INNOVATIVE_DRIVE.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Startup'ım için çok hızlı internet gerekiyor ama ofisimizde 20 kişi var ve herkes farklı ihtiyaçlara sahip. Geleneksel paketler yetersiz kalıyor. Daha yaratıcı bir çözüm var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**İnovasyon laboratuvarı açılıyor!** 🚀 Startup deneyiminiz harika bir inovasyon fırsatı! Geleneksel 'herkes aynı paket' mantığını tamamen yıkıp, disruptive bir yaklaşım tasarlayalım.\n\n**Design Thinking başlıyor:** Önce kullanıcı deneyimini derin analiz edelim. 20 kişilik ekibinizin dijital DNA'sını çıkarıp, hyper-personalized bir altyapı kurabiliriz.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_cultural_context", "parametreler": {"user_id": generate_user_id()}}]},
            {"rol": "arac", "icerik": create_validated_response(CulturalContextResponse, override_data={"user_id": generate_user_id(), "cultural_profile": "innovation_oriented_startup"})},
            {"rol": "asistan", "icerik": "**İnovasyon sonuçları muhteşem!** 🎯 Analiz sistemimiz %95 inovasyon skoruyla 4 disruptive çözüm önerdi:\n\n🚀 **Çözüm 1: AI-Powered Smart Allocation**\n• Her çalışanın gerçek zamanlı ihtiyacına göre bandwidth dağıtımı\n• Developer compile işlemi → otomatik yüksek hız\n• Designer Figma upload → otomatik görsel optimizasyon\n• PM video meeting → otomatik latency minimizasyonu\n\n🚀 **Çözüm 2: Role-Based Network Layers**\n• Dev Layer: Ultra-hızlı (GitHub, AWS, deployment araçları)\n• Creative Layer: Görsel optimized (Adobe, Sketch, video tools)\n• Communication Layer: Meeting optimized (Zoom, Slack, video calls)\n• Research Layer: Balanced (web browsing, research, sosyal medya)\n\n💡 **Innovation Lab Tasarımı:**\n• 5G + Fiber hibrit altyapı\n• Edge computing integration\n• Real-time analytics dashboard\n• Collaborative bandwidth pooling\n\nHangi inovasyon daha çok ilginizi çekiyor? Detayına inelim!", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "AI-powered allocation çok ilginç! Nasıl çalışır? Maliyeti nasıl olur?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Yapay Zeka İnovasyon Derin Dalış! 🤖**\n\n**Sistem Mimarisi:**\n```\nKullanıcı Davranış Yapay Zeka Motoru\n├── Desen Tanıma (kullanım alışkanlıkları)\n├── Tahmine Dayalı Dağıtım (sonraki 30 dakika ihtiyaçları)\n├── Öncelik Matrisi (acilline vs. task importance)\n└── Dynamic Rebalancing (real-time optimization)\n```\n\n**Çalışma Prensibi:**\n🧠 **Machine Learning Layer:**\n• Her kullanıcının kod commit patterns'ini öğrenir\n• Meeting schedule'ları ile bandwidth ihtiyacını predict eder\n• Sprint deadline'larında otomatik priority boost\n• İş saatleri vs. break times için farklı algoritmalar\n\n⚡ **Real-time Decision Engine:**\n• Sarah video call başlatıyor → otomatik 50 Mbps allocation\n• Mehmet Docker build yapıyor → 100 Mbps temporary boost\n• Team lunch time → power user'lara extra bandwidth\n• Demo hazırlığı → presentation layer'a priority\n\n💰 **Disruptive Pricing Model:**\n• **Base:** 150 GB pool (20 kişi için)\n• **AI Premium:** +%40 efficiency = 210 GB effective\n• **Maliyet:** 1,200 TL/ay (kişi başı 60 TL)\n• **ROI:** Geleneksel 20x bireysel paket: 1,800 TL\n• **Tasarruf:** 600 TL/ay + %40 productivity boost\n\n**MVP Implementation (2 hafta):**\n1. Team usage audit (1 hafta)\n2. AI model training (3 gün)\n3. Soft deployment (4 gün)\n\nPilot testi başlatalım mı? 🚀", "arac_cagrilari": None}
        ]
    } 


def generate_innovation_thinking_scenarios() -> List[Dict[str, Any]]:
    """Yenilikçi düşünce temalı 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) Startup için AI tabanlı bant genişliği tahsisi
    user_id = generate_user_id()
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.INNOVATIVE_DRIVE.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "20 kişilik startup için akıllı bant genişliği tahsisi istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Önce mevcut performansı ve ağ durumunu ölçüyorum.", "arac_cagrilari": [
                {"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "check_network_status", "parametreler": {"region": "Levent"}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id})},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Levent"})},
            {"rol": "asistan", "icerik": "AI tabanlı dinamik tahsis ile yoğun anlarda önceliklendirme yapacağız.", "arac_cagrilari": None}
        ]
    })

    # 2) 5G + Fiber hibrit failover kurgusu
    user_id = generate_user_id()
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "planning",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Kesintisiz internet için hibrit 5G+Fiber öneriniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Konumunuzda 5G elverişliliğini kontrol ediyorum.", "arac_cagrilari": [{"fonksiyon": "check_5g_coverage", "parametreler": {"user_id": user_id, "location": "ofis"}}]},
            {"rol": "arac", "icerik": create_validated_response(Check5GCoverageResponse, {"user_id": user_id, "coverage_status": "available", "coverage_percentage": 92})},
            {"rol": "asistan", "icerik": "5G elverişli. Fiber kesintisinde 5G otomatik devreye girecek bir failover tasarlıyorum.", "arac_cagrilari": None}
        ]
    })

    # 3) Rol bazlı paket katmanları
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Developer/Designer/PM için ayrı katmanlı plan önerisi isterim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Mevcut paketleri rol bazlı ihtiyaca göre listeliyorum.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Dev Ultra", "monthly_fee": 249.9, "features": {"internet_gb": 200, "voice_minutes": 2000, "sms_count": 1000}}, {"name": "Design Pro", "monthly_fee": 199.9, "features": {"internet_gb": 150, "voice_minutes": 1500, "sms_count": 1000}}, {"name": "PM Meet", "monthly_fee": 149.9, "features": {"internet_gb": 100, "voice_minutes": 3000, "sms_count": 3000}}]})},
            {"rol": "asistan", "icerik": "Rol bazlı katmanlar ile kaynaklar optimize edilir.", "arac_cagrilari": None}
        ]
    })

    # 4) Pitch günü ultra düşük gecikme
    user_id = generate_user_id()
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "impatient_tech_savvy",
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Yatırımcı sunumu için en düşük ping istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Anlık performansı ölçüp düşürme stratejisi önereceğim.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id})},
            {"rol": "asistan", "icerik": "Saat dilimi optimizasyonu ve kablolu bağlantı ile ping'i düşüreceğiz.", "arac_cagrilari": None}
        ]
    })

    # 5) Spiky kullanım için kota dengeleme
    user_id = generate_user_id()
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "busy_multitasking",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ayın ortasında kullanım çok artıyor, çözüm?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kalan kotaları kontrol edip dengeleme önerisi sunuyorum.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"internet_remaining_gb": 12.0, "usage_percentage": {"internet": 65, "voice": 35, "sms": 20}})},
            {"rol": "asistan", "icerik": "AI ile tahmin temelli dengeleme yapacağız; yoğun günlerde ek kota tanımlayacağız.", "arac_cagrilari": None}
        ]
    })

    # 6) Öğrenen ağ: davranışa göre uyarlama
    user_id = generate_user_id()
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ağım kullanım alışkanlıklarına göre kendini öğrensin istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Öğrenme adaptasyonunu güncelliyorum.", "arac_cagrilari": [{"fonksiyon": "update_learning_adaptation", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(LearningAdaptationResponse, {"user_id": user_id})},
            {"rol": "asistan", "icerik": "Kişiselleştirme seviyesi artırıldı; başarı stratejileri kaydedildi.", "arac_cagrilari": None}
        ]
    })

    # 7) Uluslararası ekipler için kültür-dostu paketleme
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "philosophical_academic",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Farklı kültürlerden ekibimiz var; onlara uygun plan isteriz.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Mevcut paketleri kültür-dostu parametrelerle listeliyorum.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Global Harmony", "monthly_fee": 189.9, "features": {"internet_gb": 120, "voice_minutes": 2500, "sms_count": 2000}, "target_audience": "multicultural_teams"}]})},
            {"rol": "asistan", "icerik": "Global Harmony paketi çok kültürlü ekipler için idealdir.", "arac_cagrilari": None}
        ]
    })

    # 8) Afet planı: İletişim sürekliliği
    user_id = generate_user_id()
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "security_conscious",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Afet durumunda kesintisiz iletişim isteriz.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Acil durum servisini pilot olarak aktive ediyorum.", "arac_cagrilari": [{"fonksiyon": "activate_emergency_service", "parametreler": {"user_id": user_id, "emergency_type": "disaster_continuity"}}]},
            {"rol": "arac", "icerik": create_validated_response(ActivateEmergencyServiceResponse, {"user_id": user_id, "emergency_type": "disaster_continuity"})},
            {"rol": "asistan", "icerik": "Acil modda data/aramalar önceliklendirilir; kritik hatlar korunur.", "arac_cagrilari": None}
        ]
    })

    # 9) Ürün lansmanı: spesifik paket detayı
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Lansman haftası için yüksek upload paket lazım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Paket detaylarını getiriyorum.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Launch Pro"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Launch Pro", "features": {"internet_gb": 150, "voice_minutes": 2000, "sms_count": 2000, "international_minutes": 300}})},
            {"rol": "asistan", "icerik": "Launch Pro, upload ağırlıklı iş akışlarınıza uygundur.", "arac_cagrilari": None}
        ]
    })

    # 10) AI destekli kullanım tahmini ile kapasite planlama
    user_id = generate_user_id()
    scenarios.append({
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Kapasite planlaması için AI tabanlı tahmin istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Geçmiş kullanım ve mevcut kota durumunu birlikte değerlendiriyorum.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"user_id": user_id, "usage_percentage": {"internet": 40, "voice": 25, "sms": 10}})},
            {"rol": "asistan", "icerik": "Tahmin modeline göre yoğun saatlerde kapasiteyi %20 artıracağız.", "arac_cagrilari": None}
        ]
    })

    return scenarios


# LATER OVERRIDE: Tekil fonksiyon artık 10'lu listeyi döndürür
def generate_innovation_thinking_scenario() -> List[Dict[str, Any]]:
    return generate_innovation_thinking_scenarios()
    if not all_scenarios:
        return []
    return all_scenarios