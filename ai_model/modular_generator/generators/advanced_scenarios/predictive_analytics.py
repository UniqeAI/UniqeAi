"""
Tahmine Dayalı Analitik Senaryosu
==================================

Bu modül, AI'nin tahmine dayalı analitik ve gelecek tahminleri yapma becerilerini test eden senaryolar üretir.
Kullanıcı verilerine dayalı gelecek tahminleri ve öneriler test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    GetPastBillsResponse,
    GetPaymentHistoryResponse,
    GetRemainingQuotasResponse,
    GetCurrentBillResponse,
    TestInternetSpeedResponse,
    CheckNetworkStatusResponse,
)


def generate_predictive_analytics_scenario1() -> Dict[str, Any]:
    """Tahmine dayalı analitik senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Gelecek ay internet kullanımım nasıl olacak? Tahmin yapabilir misin?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Predictive Analytics Engine Activated! 📊**\n\n**Historical Data Analysis:**\n• Son 6 ay kullanım trendi analiz ediliyor\n• Mevsimsellik faktörleri hesaplanıyor\n• Anomali tespiti yapılıyor\n\n**Prediction Model:**\n• Gelecek ay tahmini: 85-95 GB\n• %90 güven aralığı\n• Peak kullanım: 15-20 GB/hafta\n\n**Recommendation:**\n100 GB paket önerilir (güvenli marj)", "arac_cagrilari": None}
        ]
    } 

def generate_predictive_analytics_scenario() -> Dict[str, Any]:
    """Öngörüsel analitik senaryosu"""
    user_id = generate_user_id()
    return {
        "id": f"predictive_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.AMBITIOUS.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Veri tüketim trendlerimi analiz ederek gelecek ay ne kadar kullanacağımı tahmin edebilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Öngörüsel Analitik Motoru Başlatılıyor! 📈**\n\nMakine öğrenmesi modelleriyle gelecek tahmini yapabilirim. Önce geçmiş verilerinizi analiz edeyim...", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 12}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse), "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Öngörüsel Model Sonuçları! 🎯**\n\n```\n📊 6-Aylık Trend Analizi:\nGelecek ay tahmini: 52 GB (±8 GB)\nGüven aralığı: %85\nTrend: ↗️ %12 artış\n```\n\nBu tahmine göre paket önerisi yapalım mı?", "arac_cagrilari": None}
        ]
    }


def generate_predictive_analytics_scenarios() -> List[Dict[str, Any]]:
    """Öngörücü analiz (predictive analytics) temasında 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) Aylık veri tüketimi tahmini (geçmiş faturalar)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Gelecek ay toplam veri tüketimim ne olur?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Geçmiş faturalarınızı analiz ederek tahmin çıkaracağım.", "arac_cagrilari": [{"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 12}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse)},
            {"rol": "asistan", "icerik": "Trend artışına göre gelecek ay 80-95 GB arası tüketim bekleniyor. 100 GB paket yeterli olur.", "arac_cagrilari": None}
        ]
    })

    # 2) Ödeme davranışı ve gecikme riski (payment history)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "planning",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Gelecek ay faturamı geciktirme riskim var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Ödeme geçmişinizi analiz ediyorum.", "arac_cagrilari": [{"fonksiyon": "get_payment_history", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPaymentHistoryResponse)},
            {"rol": "asistan", "icerik": "Son 6 ayda iki kez gecikme var. Otomatik ödeme öneririm; risk %70'ten %15'e düşer.", "arac_cagrilari": None}
        ]
    })

    # 3) Kota bitme ihtimali (kalan kotalar + yüzdeler)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "busy_multitasking",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ay sonuna kadar kotam yeter mi?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kalan kotalarınızı kontrol ediyor ve tahmin modeli çalıştırıyorum.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 55, "voice": 20, "sms": 10}})},
            {"rol": "asistan", "icerik": "Mevcut hızla giderse kota %85 olasılıkla yetecek; yoğun günlerde ek 5 GB öneririm.", "arac_cagrilari": None}
        ]
    })

    # 4) Fatura tahmini (current bill + geçmiş)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.AMBITIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Bu ayki faturam yaklaşık ne kadar olur?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Güncel ve geçmiş faturanızı analiz ediyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 6}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"user_id": user_id})},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse)},
            {"rol": "asistan", "icerik": "Geçmiş ortalaması ve bu ayki kullanımınıza göre ~185 TL bekleniyor.", "arac_cagrilari": None}
        ]
    })

    # 5) Yoğun saatlerde ping tahmini (hız testi + ağ durumu)
    user_id = generate_user_id()
    measured = round(random.uniform(25.0, 75.0), 1)
    ping = random.randint(20, 90)
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "impatient_tech_savvy",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Akşam saatlerinde ping yükseliyor; tahmininiz nedir?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Şimdi ölçüm yapıp bölge durumunu kontrol edeceğim ve tahmin paylaşacağım.", "arac_cagrilari": [
                {"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "check_network_status", "parametreler": {"region": "Beşiktaş"}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id, "download_speed_mbps": measured, "ping_ms": ping})},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Beşiktaş"})},
            {"rol": "asistan", "icerik": "Yoğunlukta ping 40-80ms aralığına çıkabilir. Zamanlama/rota önerileri paylaşacağım.", "arac_cagrilari": None}
        ]
    })

    # 6) Fatura aşımı risk tahmini (kota yüzdesi + trend)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "confused_indecisive",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ek ücret riski var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kalan kotalarınızı ve kullanım trendinizi analiz ediyorum.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 70, "voice": 25, "sms": 15}})},
            {"rol": "asistan", "icerik": "Ek ücret riski düşüktür; %20 güvenli marj ile yeterli görünmektedir.", "arac_cagrilari": None}
        ]
    })

    # 7) İçerik üretimi için bant genişliği tahmini
    user_id = generate_user_id()
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "content_creator",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Önümüzdeki hafta video yüklemeleri için bant genişliği gereksinimim ne olur?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kalan kota ve önceki haftalara bakarak tahmin oluşturacağım.", "arac_cagrilari": [
                {"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 65, "voice": 10, "sms": 5}})},
            {"rol": "asistan", "icerik": "Video yükleme için ek 20 GB tavsiye ederim; upload saatlerini yoğun olmayan dilimlere alın.", "arac_cagrilari": None}
        ]
    })

    # 8) Çağrı merkezi yoğunluk saatleri tahmini (ağ durumu)
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "planning",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Yoğunluk nedeniyle kesinti olur mu?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Bölgesel ağı kontrol edip tahmin paylaşacağım.", "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Kadıköy"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Kadıköy"})},
            {"rol": "asistan", "icerik": "Önümüzdeki hafta bakım planı yok; akşam saatlerinde orta düzey yoğunluk bekleniyor.", "arac_cagrilari": None}
        ]
    })

    # 9) Fatura gününde sistem yoğunluk tahmini (hız testi)
    user_id = generate_user_id()
    measured = round(random.uniform(15.0, 50.0), 1)
    ping = random.randint(30, 110)
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "busy_multitasking",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Fatura gününde internet yoğun olur mu?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Anlık hız ölçümü ile birlikte tahmin paylaşacağım.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id, "download_speed_mbps": measured, "ping_ms": ping})},
            {"rol": "asistan", "icerik": "Gün ortasında hafif yoğunluk beklenir; 19:00 sonrası normale döner.", "arac_cagrilari": None}
        ]
    })

    # 10) Haftalık bütçe/tüketim planlama (geçmiş + kalan)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"predictive_analytics_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.PREDICTIVE_ANALYTICS.value,
        "personality_profile": "planning",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.HOPEFUL.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Haftaya bütçe ve kota hedefi koymak istiyorum; nasıl planlayalım?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Geçmiş ve mevcut durumunuza bakarak plan çıkarıyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 3}},
                {"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse)},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 50, "voice": 15, "sms": 10}})},
            {"rol": "asistan", "icerik": "Haftalık hedef: 20 GB; akşamları video yerine düşük veri modunu öneririm.", "arac_cagrilari": None}
        ]
    })

    return scenarios


def generate_predictive_analytics_scenario() -> List[Dict[str, Any]]:
    """Havuzdaki 10 öngörücü analiz senaryosunu döndürür (üst katman sampling yapar)."""
    return generate_predictive_analytics_scenarios()