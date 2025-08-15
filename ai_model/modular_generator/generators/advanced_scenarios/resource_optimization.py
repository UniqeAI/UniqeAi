"""
Kaynak Optimizasyonu Senaryosu
==============================

Bu modül, AI'nin kaynak optimizasyonu ve verimlilik artırma becerilerini test eden senaryolar üretir.
Kullanıcıların mevcut kaynaklarını nasıl optimize ettiği test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    GetRemainingQuotasResponse,
    GetAvailablePackagesResponse,
    GetCurrentBillResponse,
    GetPastBillsResponse,
    GetCustomerPackageResponse,
    CheckNetworkStatusResponse,
    TestInternetSpeedResponse,
    SetupAutopayResponse,
    GetPackageDetailsResponse,
)


def generate_resource_optimization_scenario1() -> Dict[str, Any]:
    """Kaynak optimizasyonu senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "efficiency_conscious_manager",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.AMBITIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Mevcut paketimdeki kaynakları daha verimli kullanmak istiyorum. Nasıl optimize edebilirim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Resource Optimization Engine Activated! ⚙️**\n\n**Current Usage Analysis:**\n• Internet: %80 kullanım (20% israf)\n• Voice: %30 kullanım (70% israf)\n• SMS: %10 kullanım (90% israf)\n\n**Optimization Strategy:**\n• Internet kotasını %100 kullan\n• Voice dakikalarını azalt\n• SMS yerine WhatsApp kullan\n\n**Expected Savings:** %25 maliyet azalması", "arac_cagrilari": None}
        ]
    } 

def generate_resource_optimization_scenarios() -> List[Dict[str, Any]]:
    """Kaynak optimizasyonu temasında 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) Aşırı kullanılmayan SMS/dakika → daha uygun paket önerisi
    user_id = generate_user_id()
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "efficiency_conscious_manager",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Dakika ve SMS’leri neredeyse kullanmıyorum. Daha uygun pakete geçebilir miyim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kalan kotalarınızı kontrol ediyorum, ardından uygun paketleri önereceğim.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 60, "voice": 5, "sms": 3}})},
            {"rol": "asistan", "icerik": "Dakika/SMS kullanımınız çok düşük. Daha internet ağırlıklı paketlere bakalım.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Data Focus 50GB", "monthly_fee": 129.90, "features": {"internet_gb": 50, "voice_minutes": 250, "sms_count": 100}, "target_audience": "data_heavy_users"}]})},
            {"rol": "asistan", "icerik": "Data Focus 50GB ile maliyet düşer, israf azalır. İster misiniz?", "arac_cagrilari": None}
        ]
    })

    # 2) Ay sonu kota yetme analizi ve optimizasyon önerisi
    user_id = generate_user_id()
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "planning",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ay bitmeden internetim bitecek gibi. Optimizasyon öneriniz var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kalan kotaları inceliyorum.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 85, "voice": 30, "sms": 20}})},
            {"rol": "asistan", "icerik": "Yoğun günler için 10 GB ek paket öneririm; video kaliteyi ‘otomatik’ yapın.", "arac_cagrilari": None}
        ]
    })

    # 3) Aylık fatura düşürme (geçmiş ve güncel fatura karşılaştırması)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.AMBITIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Aylık toplam maliyeti %20 azaltmak istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Güncel ve geçmiş faturanızı analiz ederek tasarruf fırsatlarını belirleyeceğim.", "arac_cagrilari": [
                {"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 6}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"user_id": user_id})},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse)},
            {"rol": "asistan", "icerik": "Daha düşük ücretli, benzer içerikte paket ile %18-25 arası tasarruf mümkün.", "arac_cagrilari": None}
        ]
    })

    # 4) Mevcut paket uyum kontrolü ve alternatif öneri
    user_id = generate_user_id()
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "confused_indecisive",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Paketim bana uygun mu emin değilim. Ne önerirsiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Mevcut paketinizi ve kullanımınızı karşılaştıracağım.", "arac_cagrilari": [
                {"fonksiyon": "get_customer_package", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerPackageResponse, {"package_name": "Süper Paket"})},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 40, "voice": 10, "sms": 5}})},
            {"rol": "asistan", "icerik": "Daha düşük dakikalı, yüksek verili pakete geçiş tasarruf sağlar.", "arac_cagrilari": None}
        ]
    })

    # 5) Yoğun saatlerde bant genişliği planlama (ağ durumu + hız testi)
    user_id = generate_user_id()
    speed = round(random.uniform(30.0, 90.0), 1)
    ping = random.randint(15, 70)
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "impatient_tech_savvy",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Akşam video toplantılarında kalite düşüyor; nasıl optimize ederiz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Anlık hız testi ve bölge ağ durumuna bakıp zamanlama önerisi yapacağım.", "arac_cagrilari": [
                {"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "check_network_status", "parametreler": {"region": "Beşiktaş"}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id, "download_speed_mbps": speed, "ping_ms": ping})},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Beşiktaş"})},
            {"rol": "asistan", "icerik": "18:30-20:00 arası yoğun. Toplantıları 20:30 sonrası planlayın; HD yerine 720p önerilir.", "arac_cagrilari": None}
        ]
    })

    # 6) Otomatik ödeme ile kesinti riskini azaltma (operasyonel optimizasyon)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "busy_multitasking",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.HOPEFUL.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ödeme unutunca hat kesiliyor. Bunu optimize edebilir miyiz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Otomatik ödeme tanımlayarak kesinti riskini sıfıra yaklaştırabiliriz.", "arac_cagrilari": [{"fonksiyon": "setup_autopay", "parametreler": {"user_id": user_id, "status": True}}]},
            {"rol": "arac", "icerik": create_validated_response(SetupAutopayResponse, {"user_id": user_id, "autopay_enabled": True})},
            {"rol": "asistan", "icerik": "Otomatik ödeme aktif. Operasyonel verimlilik ve memnuniyet artacak.", "arac_cagrilari": None}
        ]
    })

    # 7) Uluslararası dakikalar israfını azaltma (paket uyarlama)
    user_id = generate_user_id()
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "planning",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Uluslararası dakika kullanmıyorum. Daha uygun bir kombinasyon var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Mevcut paketinizi ve kalan haklarınızı kontrol ediyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_customer_package", "parametreler": {"user_id": user_id}},
                {"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}
            ]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerPackageResponse)},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"usage_percentage": {"internet": 35, "voice": 8, "sms": 5}})},
            {"rol": "asistan", "icerik": "Uluslararası dakika içeriği düşük bir pakete geçişle tasarruf edersiniz.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Local Focus 30GB", "monthly_fee": 109.90, "features": {"internet_gb": 30, "voice_minutes": 500, "sms_count": 200}, "target_audience": "local_users"}]})},
            {"rol": "asistan", "icerik": "Local Focus 30GB uygun görünüyor. Geçiş yapmak ister misiniz?", "arac_cagrilari": None}
        ]
    })

    # 8) Bakım/yoğunluk takvimi ile kesinti riskini azaltma
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "strategic_planner",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Planlı bakım dönemlerinde işimi aksatmamak için öneri isterim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Bölgesel ağ durumuna göre saatlik planlama önereceğim.", "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Kadıköy"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Kadıköy"})},
            {"rol": "asistan", "icerik": "Bakım pencere saatlerinde büyük yüklemelerden kaçının; işlemleri sabah erken saate alın.", "arac_cagrilari": None}
        ]
    })

    # 9) Ofis içi Wi‑Fi/Cellular kullanım dengesini optimize etme (hız testi)
    user_id = generate_user_id()
    dl = round(random.uniform(20.0, 60.0), 1)
    ping = random.randint(25, 90)
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "efficiency_conscious_manager",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Mobil veri ve Wi‑Fi arasında en verimli strateji ne olur?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hız testi ile tespite bakıp eşik bazlı öneri sunacağım.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id, "download_speed_mbps": dl, "ping_ms": ping})},
            {"rol": "asistan", "icerik": "Wi‑Fi 25 Mbps üzeri ise mobil veriyi yedek tutun; ping yükselirse video kalitesini düşürün.", "arac_cagrilari": None}
        ]
    })

    # 10) Eğitim/uzaktan çalışma için uygun paket detay karşılaştırması
    scenarios.append({
        "id": f"resource_optimization_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.RESOURCE_OPTIMIZATION.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.HOPEFUL.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Uzaktan eğitim için en verimli paket hangisi? Detaylarıyla karşılaştırır mısınız?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Uygun bir paket örneğinin detaylarını gösteriyorum.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Edu Max"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Edu Max", "monthly_fee": 139.90, "setup_fee": 0.0, "features": {"internet_gb": 50, "voice_minutes": 1000, "sms_count": 500, "international_minutes": 0}, "contract_duration": 12, "cancellation_fee": 25.0})},
            {"rol": "asistan", "icerik": "Edu Max uzaktan eğitim için yeterli bant genişliği sunar; maliyet/verim dengesi iyidir.", "arac_cagrilari": None}
        ]
    })

    return scenarios


def generate_resource_optimization_scenario() -> List[Dict[str, Any]]:
    """Havuzdaki 10 kaynak optimizasyonu senaryosunu döndürür (üst katman sampling yapar)."""
    return generate_resource_optimization_scenarios()