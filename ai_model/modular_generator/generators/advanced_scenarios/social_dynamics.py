"""
Sosyal Dinamikler Senaryosu
============================

Bu modül, AI'nin sosyal dinamikleri anlama ve topluluk odaklı çözüm üretme becerilerini test eden senaryolar üretir.
Kullanıcıların sosyal ihtiyaçlarını ve topluluk çözümlerini nasıl ele aldığı test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    CheckNetworkStatusResponse,
    CreateFaultTicketResponse,
    GetUsersTicketsResponse,
    GetFaultTicketStatusResponse,
    GetAvailablePackagesResponse,
    GetPackageDetailsResponse,
    TestInternetSpeedResponse,
    GetCurrentBillResponse,
    GetPastBillsResponse,
)


def generate_social_dynamics_scenario() -> Dict[str, Any]:
    """Sosyal dinamikler senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "busy_working_parent",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.OVERWHELMED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ev internetimiz sürekli yavaş ve çocuklar online derslerde zorlanıyor. Eşim de ev ofisinden çalışıyor. Komşularla konuştum, onların da aynı problemi var. Mahallemiz için toplu bir çözüm olabilir mi?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Community-Centered Solution Approach! 👨‍👩‍👧‍👦** Çok değerli bir yaklaşım sergiliyorsunuz! Komşularla iş birliği yapmak hem Türk kültürünün güzel bir yanı hem de teknik açıdan çok akıllıca bir strateji. Sosyal çözüm odaklı yaklaşalım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Kadıköy Merkez"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, override_data={"status": "degraded"})},
            {"rol": "asistan", "icerik": "**Toplumsal Sorun Doğrulandı! 🏘️** Analiz sonuçları komşularınızın gözlemlerini doğruluyor. Mahallenizde fiber altyapı yoğunluğu sorunu var. Bu durumda bireysel çözümler yerine toplumsal çözüm çok daha mantıklı!\n\n**Social Dynamics Strategy:**\n\n👥 **Neighborhood Alliance Package:**\n• 10+ haneli toplu başvuruda %30 indirim\n• Ortak fiber altyapı yatırımı (maliyeti paylaşımlı)\n• 'Mahalle Wi-Fi' backup sistemi\n• Çocuk online eğitimi öncelik algoritması\n\n🏠 **Family-Centric Features:**\n• Ders saatleri (9-17) bandwidth guarantee\n• Ebeveyn kontrol sistemi (ücretsiz)\n• Ev ofisi quality assurance\n• Aile paylaşım kotası\n\n👫 **Community Building Benefits:**\n• Komşular arası tech support network\n• Ortak sorun çözme WhatsApp grubu\n• Mahalle etkinlikleri için ücretsiz hotspot\n\n**Action Plan:**\n1. Komşu listesi (min 8-10 hane)\n2. Toplu survey (ihtiyaç analizi)\n3. Özel mahalle paketi tasarımı\n4. Fiber altyapı upgrade timeline\n\nKomşularınızla bu planı konuşup geri dönüş yapar mısınız? 'Dijital mahalle' projesi başlatalım! 🚀", "arac_cagrilari": None}
        ]
    } 


def generate_social_dynamics_scenarios() -> List[Dict[str, Any]]:
    """Sosyal dinamikler temalı 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) Mahalle genelinde hız düşüşü → toplu çözüm
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "busy_working_parent",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.OVERWHELMED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ev internetimiz hep yavaş; komşular da aynı. Toplu çözüm var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Bölge ağ durumunu kontrol edip toplu çözüm önereceğim.", "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Kadıköy Merkez"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Kadıköy Merkez", "status": "degraded"})},
            {"rol": "asistan", "icerik": "Yoğunluk tespit edildi. Komşularla birlikte 'Neighborhood Alliance' planı öneriyorum: toplu başvuruda indirim ve kapasite artırımı.", "arac_cagrilari": None}
        ]
    })

    # 2) Öğrenci yurdu için ders saatlerinde kapasite planı
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "student_union_rep",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Yurtta ders saatlerinde internet zorlanıyor. Çözüm öneriniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Ağ durumunu kontrol ediyor ve ders saatleri için plan öneriyorum.", "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Üniversite Kampüsü A"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Üniversite Kampüsü A"})},
            {"rol": "asistan", "icerik": "09:00-17:00 arası yoğunluk var. Çalışma salonlarına ek erişim noktası ve QoS ayarı öneriyorum.", "arac_cagrilari": None}
        ]
    })

    # 3) Mahalle festivali için geçici kapasite ve paket detayı
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "community_event_organizer",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Mahalle festivalinde canlı yayın için ek kapasite lazım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Etkinlik paketi detayına bakalım.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Event Pack"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Event Pack", "monthly_fee": 0.0, "setup_fee": 0.0, "features": {"internet_gb": 200, "voice_minutes": 0, "sms_count": 0, "international_minutes": 0}, "contract_duration": 1, "cancellation_fee": 0.0})},
            {"rol": "asistan", "icerik": "Event Pack ile yayın için yeterli bant genişliği sağlanır. Kurulum ücretsiz.", "arac_cagrilari": None}
        ]
    })

    # 4) Toplu arıza kaydı ve koordinasyon
    user_id = generate_user_id()
    ticket_id = f"TKT-{random.randint(100000, 999999)}"
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "neighborhood_leader",
        "cognitive_state": CognitiveState.COLLABORATIVE.value,
        "emotional_context": EmotionalContext.URGENT.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Sokakta birden çok hanede internet tamamen gitti. Toplu kayıt açalım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Toplu arıza kaydı açıyorum ve takip edeceğim.", "arac_cagrilari": [{"fonksiyon": "create_fault_ticket", "parametreler": {"user_id": user_id, "issue_description": "Mahalle genelinde kesinti", "category": "outage", "priority": "urgent"}}]},
            {"rol": "arac", "icerik": create_validated_response(CreateFaultTicketResponse, {"ticket_id": ticket_id, "status": "open"})},
            {"rol": "asistan", "icerik": f"{ticket_id} açıldı. Komşular için durumu tek kanaldan yöneteceğim.", "arac_cagrilari": None}
        ]
    })

    # 5) Site yönetimi adına destek talepleri görünümü
    user_group_id = generate_user_id()
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "apartment_manager",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Sitemizdeki aktif destek kayıtlarını tek ekranda görebilir miyiz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Site kullanıcıları adına kayıtları listeliyorum.", "arac_cagrilari": [{"fonksiyon": "get_users_tickets", "parametreler": {"user_id": user_group_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetUsersTicketsResponse, {"user_id": user_group_id})},
            {"rol": "asistan", "icerik": "Aktif kayıtlarınızı tek panelden takip edebilirsiniz; ortak iletişimle çözüm hızlanır.", "arac_cagrilari": None}
        ]
    })

    # 6) Toplu indirime uygun paketler (komünite bazlı)
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "bargain_hunter_group",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.HOPEFUL.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Mahallece daha uygun bir toplu paket var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Toplu kullanım için uygun paketleri listeliyorum.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Community Fiber 100", "monthly_fee": 159.90, "features": {"internet_gb": 100, "voice_minutes": 500, "sms_count": 200}, "target_audience": "communities"}]})},
            {"rol": "asistan", "icerik": "Community Fiber 100 toplu sözleşmede ek %20 indirim destekler.", "arac_cagrilari": None}
        ]
    })

    # 7) Ortak çalışma alanında kalite sorunları (ölçüm + öneri)
    cowork_user = generate_user_id()
    dl = round(random.uniform(25.0, 80.0), 1)
    ping = random.randint(20, 70)
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "coworking_admin",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ortak alanda video aramalar sık kopuyor; topluluk için çözüm?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hız testi yapıp eşiklere göre öneri sunacağım.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": cowork_user}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": cowork_user, "download_speed_mbps": dl, "ping_ms": ping})},
            {"rol": "asistan", "icerik": "AP konumlandırması ve QoS ile toplulukta kaliteyi stabilize ederiz; yoğun saatlerde 720p önerilir.", "arac_cagrilari": None}
        ]
    })

    # 8) Toplu fatura şoku analizi (güncel + geçmiş karşılaştırma)
    account_id = generate_user_id()
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "community_center_treasurer",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.SKEPTICAL.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Topluluk merkezinin faturası bu ay çok artmış. Neden?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Güncel ve geçmiş faturanızı karşılaştırıyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_current_bill", "parametreler": {"user_id": account_id}},
                {"fonksiyon": "get_past_bills", "parametreler": {"user_id": account_id, "limit": 6}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"user_id": account_id})},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse)},
            {"rol": "asistan", "icerik": "Ek hizmetler ve veri tüketimi artmış. Grup içi kullanım kuralları ve kota yönetimi öneririm.", "arac_cagrilari": None}
        ]
    })

    # 9) Ortak kayıt takibi: durum sorgulama
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "neighborhood_leader",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.ANTICIPATION.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Geçen hafta açılan mahalle kaydımızın durumu ne?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kayıt durumunu kontrol ediyorum.", "arac_cagrilari": [{"fonksiyon": "get_fault_ticket_status", "parametreler": {"ticket_id": "TKT-NEIGH-001"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetFaultTicketStatusResponse, {"ticket_id": "TKT-NEIGH-001", "status": "in_progress", "technician_notes": "Bölgesel kapasite artırımı planlanıyor"})},
            {"rol": "asistan", "icerik": "Kayıt incelemede. Kapasite artırımı planı teknik ekipte. Gelişmeleri sizinle paylaşacağım.", "arac_cagrilari": None}
        ]
    })

    # 10) Komşu erişimi için uygun paket taraması
    scenarios.append({
        "id": f"social_dynamics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.SOCIAL_DYNAMICS.value,
        "personality_profile": "community_volunteer",
        "cognitive_state": CognitiveState.COLLABORATIVE.value,
        "emotional_context": EmotionalContext.HOPEFUL.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Yaşlı komşular için uygun ve basit bir paket önerir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Yaşlı kullanıcılar için basit içerikli paket detayına bakıyorum.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Simple Care"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Simple Care", "monthly_fee": 79.90, "setup_fee": 0.0, "features": {"internet_gb": 10, "voice_minutes": 500, "sms_count": 200, "international_minutes": 0}, "contract_duration": 12, "cancellation_fee": 15.0})},
            {"rol": "asistan", "icerik": "Simple Care yaşlı komşular için idealdir: düşük maliyet, basit kullanım.", "arac_cagrilari": None}
        ]
    })

    return scenarios


def generate_social_dynamics_scenario() -> List[Dict[str, Any]]:
    """Havuzdaki 10 sosyal dinamikler senaryosunu döndürür (üst katman sampling yapar)."""
    return generate_social_dynamics_scenarios()