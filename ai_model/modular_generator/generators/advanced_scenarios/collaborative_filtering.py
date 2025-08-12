"""
İşbirlikçi Filtreleme Senaryoları
==================================

Bu modül, benzer müşteri profillerine dayalı öneriler ve işbirlikçi filtreleme
yaklaşımlarını test eden günlük müşteri hizmetleri senaryolarını içerir.
"""

import uuid
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id

try:
    from ...telekom_api_schema import *
except ImportError:
    try:
        from ai_model.modular_generator.telekom_api_schema import *
    except ImportError:
        try:
            from ai_model.scripts.telekom_api_schema import *
        except ImportError:
            try:
                import sys
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.join(current_dir, '..', '..', '..')
                sys.path.insert(0, project_root)
                from ai_model.scripts.telekom_api_schema import *
            except ImportError as e:
                print(f"Telekom API şeması import hatası: {e}")
                raise

def generate_collaborative_filtering_scenarios() -> List[Dict[str, Any]]:
    """12 adet işbirlikçi filtreleme senaryosu üretir."""
    
    scenarios = []

    # === SENARYO 1: Benzer Kullanıcıların Paket Tercihleri ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "inquisitive_researcher",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "urban_professional",
        "donguler": [
            {"rol": "kullanici", "icerik": "Benimle aynı yaş grubundaki ve aynı bölgede yaşayan müşteriler hangi paketleri tercih ediyor? Bu bilgiye göre karar vermek istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Harika bir yaklaşım! Sizin demografik profilinize uygun müşteri tercihlerini analiz edebilirim. Önce mevcut paketleri göstereyim, sonra benzer profildeki müşterilerin tercihlerini paylaşacağım.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_mock_response("get_available_packages", packages=[{"name": "Genç Dinamik", "monthly_fee": 45.90, "features": {"internet_gb": 25, "voice_minutes": 1000, "sms_count": 500}, "target_audience": "youth"}, {"name": "Profesyonel Plus", "monthly_fee": 69.90, "features": {"internet_gb": 50, "voice_minutes": 2000, "sms_count": 1000}, "target_audience": "business"}, {"name": "Aile Paketi", "monthly_fee": 89.90, "features": {"internet_gb": 75, "voice_minutes": 3000, "sms_count": 1500}, "target_audience": "family"}]).model_dump_json()},
            {"rol": "asistan", "icerik": "📊 **Benzer Profil Analizi Tamamlandı!** \n\n25-35 yaş arası şehirli profesyonellerin tercihleri:\n• %68'i **Profesyonel Plus** paketini seçiyor\n• %24'ü **Genç Dinamik** ile başlayıp sonra yükseltiyor\n• Ortalama aylık kullanım: 42GB internet, 1200 dakika\n\n💡 **Öneri:** Profesyonel Plus paketi sizin profilinize en uygun görünüyor. Detaylarını görmek ister misiniz?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 2: Kullanım Alışkanlıklarına Göre Öneri ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "efficiency_seeker",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "cost_conscious",
        "donguler": [
            {"rol": "kullanici", "icerik": "Benim gibi çok internet kullanan ama az konuşan müşteriler hangi paketlerde mutlu? Gereksiz ödeme yapmak istemiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Akıllıca düşünüyorsunuz! Önce mevcut kullanımınızı kontrol edelim, sonra benzer kullanım alışkanlığına sahip müşterilerin tercihlerini paylaşayım.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": 10001}}]},
            {"rol": "arac", "icerik": create_mock_response("get_remaining_quotas", internet_remaining_gb=5.2, voice_remaining_minutes=850, sms_remaining=480, period_end="2024-03-31", usage_percentage={"internet": 85, "voice": 15, "sms": 4}).model_dump_json()},
            {"rol": "asistan", "icerik": "🎯 **Kullanım Profili Analizi:**\nSiz %85 internet, %15 konuşma kullanıyorsunuz.\n\n📈 **Benzer Kullanıcı Önerileri:**\n• Yoğun internet kullanıcıları %73 oranında **veri odaklı paketleri** tercih ediyor\n• Az konuşanlar için **Mega İnternet Paketi** (%89 memnuniyet)\n• Ortalama %30 tasarruf sağlıyorlar\n\nSize özel paket önerilerini göstereyim mi?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 3: Aile Profilindeki Müşteri Tercihleri ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "family_oriented",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "traditional_family",
        "donguler": [
            {"rol": "kullanici", "icerik": "4 kişilik ailem var, çocuklar sürekli internette. Benzer ailelerin hangi çözümleri tercih ettiğini öğrenmek istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Aile ihtiyaçlarını çok iyi anlıyorum! Benzer büyüklükteki ailelerin tercihlerini analiz edeyim. Önce aile paketlerini göstereyim.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Aile Paketi"}}]},
            {"rol": "arac", "icerik": create_mock_response("get_package_details", name="Aile Paketi", monthly_fee=89.90, setup_fee=0, features={"internet_gb": 75, "voice_minutes": 3000, "sms_count": 1500, "international_minutes": 200}, contract_duration=24, cancellation_fee=50.00).model_dump_json()},
            {"rol": "asistan", "icerik": "👨‍👩‍👧‍👦 **4 Kişilik Aile Analizi:**\n\n📊 **Benzer Ailelerin Tercihleri:**\n• %78'i Aile Paketi ile başlıyor\n• %45'i ek internet paketi alıyor (çocuklar için)\n• %67'si ebeveyn kontrol özelliklerini aktif ediyor\n\n💡 **Popüler Eklentiler:**\n• Çocuk güvenlik paketi (%89 memnuniyet)\n• Sınırsız sosyal medya (%76 kullanım)\n\nAile paketinizi bu önerilere göre özelleştirelim mi?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 4: İş Dünyasından Benzer Profiller ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "business_executive",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.AMBITIOUS.value,
        "cultural_context": "corporate_environment",
        "donguler": [
            {"rol": "kullanici", "icerik": "Şirket müdürü olarak sürekli seyahatteyim. Benzer pozisyondaki yöneticiler hangi servisleri kullanıyor?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Üst düzey yöneticilerin ihtiyaçlarını çok iyi biliyoruz! Benzer profildeki müşterilerimizin tercihlerini analiz edeyim. Önce roaming durumunuzu kontrol edelim.", "arac_cagrilari": [{"fonksiyon": "check_5g_coverage", "parametreler": {"user_id": 10003, "location": "current_location"}}]},
            {"rol": "arac", "icerik": create_mock_response("check_5g_coverage", user_id=10003, location="İstanbul Merkez", coverage_status="available", signal_strength=92, download_speed_estimate_mbps=850.0, upload_speed_estimate_mbps=180.0, latency_estimate_ms=4, network_quality="excellent", coverage_percentage=96).model_dump_json()},
            {"rol": "asistan", "icerik": "🏢 **Yönetici Profili Analizi:**\n\n📈 **Benzer Pozisyondaki Yöneticilerin Tercihleri:**\n• %89'u Premium Business paketini kullanıyor\n• %76'sı uluslararası roaming'i sürekli aktif tutuyor\n• %92'si 5G öncelikli bölgelerde çalışıyor\n\n✈️ **Seyahat Odaklı Hizmetler:**\n• Global roaming paketi (%94 memnuniyet)\n• Öncelikli müşteri hattı (%98 çözüm oranı)\n• VIP lounge erişimi\n\nSize özel yönetici paketini hazırlayalım mı?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 5: Öğrenci Topluluğu Önerileri ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "budget_conscious_student",
        "cognitive_state": CognitiveState.CREATIVE.value,
        "emotional_context": EmotionalContext.HOPEFUL.value,
        "cultural_context": "student_community",
        "donguler": [
            {"rol": "kullanici", "icerik": "Üniversite öğrencisiyim, bütçem kısıtlı. Diğer öğrenciler hangi paketleri tercih ediyor, en uygun fiyatlı hangisi?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Öğrenci dostu çözümlerimiz var! Sizin gibi bütçe bilincli öğrencilerin tercihlerini analiz edeyim. Önce öğrenci paketlerini göstereyim.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_mock_response("get_available_packages", packages=[{"name": "Öğrenci Dostu", "monthly_fee": 29.90, "features": {"internet_gb": 15, "voice_minutes": 500, "sms_count": 300}, "target_audience": "students"}, {"name": "Genç Dinamik", "monthly_fee": 45.90, "features": {"internet_gb": 25, "voice_minutes": 1000, "sms_count": 500}, "target_audience": "youth"}, {"name": "Sosyal Medya+", "monthly_fee": 35.90, "features": {"internet_gb": 20, "voice_minutes": 750, "sms_count": 400}, "target_audience": "social"}]).model_dump_json()},
            {"rol": "asistan", "icerik": "🎓 **Öğrenci Topluluğu Analizi:**\n\n📚 **Öğrenci Tercih İstatistikleri:**\n• %67'si **Öğrenci Dostu** ile başlıyor\n• %34'ü sınavdan sonra **Sosyal Medya+** a geçiyor\n• %89'u sosyal medya sınırsız özelliğini seviyor\n\n💰 **Tasarruf İpuçları:**\n• Öğrenci indirimi ile %40 tasarruf\n• Arkadaş referansı ile ek %15 indirim\n• Yaz tatili dondurma seçeneği\n\nSize en uygun paketi bulalım!", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 6: Emekli Müşteri Profili ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "retired_professional",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "retirement_community",
        "donguler": [
            {"rol": "kullanici", "icerik": "Emekli olduktan sonra ihtiyaçlarım değişti. Benimle aynı durumda olan emekli müşteriler genellikle hangi paketleri tercih ediyor?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Emeklilik dönemi farklı ihtiyaçlar getirir, çok doğru düşünüyorsunuz. Emekli müşterilerimizin tercihlerini analiz edelim. Önce mevcut faturanızı kontrol edelim.", "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": 10005}}]},
            {"rol": "arac", "icerik": create_mock_response("get_current_bill", bill_id=f"F-2024-{random.randint(100000, 999999)}", user_id=10005, amount=45.50, due_date=(datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'), bill_date=datetime.now().strftime('%Y-%m-%d'), status=BillStatus.UNPAID, services=[{"service_name": "Emekli Paketi", "amount": 45.50}]).model_dump_json()},
            {"rol": "asistan", "icerik": "👴 **Emekli Müşteri Analizi:**\n\n📞 **Emekli Profil Tercihleri:**\n• %88'i **konuşma odaklı** paketleri tercih ediyor\n• %79'u **sabit ve düşük aylık ücret** istiyor\n• %94'ü **karmaşık özelliklerden** kaçınıyor\n\n🏡 **Emeklilik Özel Hizmetleri:**\n• Emekli indirimi %25 (%97 memnuniyet)\n• Sağlık acil durum hattı (%89 kullanım)\n• Büyük yazılı faturalar\n\nSize özel emekli paketi düzenleyelim mi?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 7: Ödeme Geçmişi Analizi ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "financial_analyst",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "budget_conscious",
        "donguler": [
            {"rol": "kullanici", "icerik": "Benimle aynı harcama alışkanlığına sahip müşteriler hangi ödeme yöntemlerini tercih ediyor? Geçmiş ödemelerime bakarak analiz yapabilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Finansal analiz yapmak harika bir yaklaşım! Benzer harcama profiline sahip müşterilerimizin tercihlerini inceleyelim. Önce ödeme geçmişinizi kontrol edeyim.", "arac_cagrilari": [{"fonksiyon": "get_payment_history", "parametreler": {"user_id": 10010}}]},
            {"rol": "arac", "icerik": create_mock_response("get_payment_history", payments=[{"transaction_id": "TXN-001", "amount": 89.50, "method": PaymentMethod.CREDIT_CARD, "date": "2024-02-05T10:15:00Z", "bill_id": "F-2024-001"}], total_payments=5, total_amount=447.50).model_dump_json()},
            {"rol": "asistan", "icerik": "💳 **Ödeme Profili Analizi:**\n\n📊 **Benzer Müşteri Tercihleri:**\n• %76'sı **kredi kartı** ile ödeme yapıyor\n• %68'i **otomatik ödeme** sistemini kullanıyor\n• Ortalama aylık harcama: 89.50 TL\n\n🎯 **Tasarruf Önerileri:**\n• Otomatik ödeme ile %5 indirim\n• Yıllık ödeme ile %10 tasarruf\n\nSize özel ödeme planı hazırlayalım mı?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 8: Yaşlı Kullanıcı Profili Önerileri ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "senior_citizen",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.CONFUSED.value,
        "cultural_context": "traditional_elder",
        "donguler": [
            {"rol": "kullanici", "icerik": "65 yaşındayım, çok karmaşık paketler istemiyorum. Benim yaştaki insanlar genellikle ne kullanıyor?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Çok haklısınız, basitlik önemli! Sizin yaş grubundaki değerli müşterilerimizin tercihlerini inceleyeyim. Önce mevcut paketinizi kontrol edelim.", "arac_cagrilari": [{"fonksiyon": "get_customer_package", "parametreler": {"user_id": 10006}}]},
            {"rol": "arac", "icerik": create_mock_response("get_customer_package", package_name="Basit Paket", monthly_fee=39.90, features={"internet_gb": 10, "voice_minutes": 1500, "sms_count": 200, "roaming_enabled": False, "international_minutes": 50}, activation_date="2024-01-01", renewal_date="2024-04-01").model_dump_json()},
            {"rol": "asistan", "icerik": "👴👵 **65+ Yaş Grubu Analizi:**\n\n📞 **Benzer Yaştaki Müşteri Tercihleri:**\n• %82'si **konuşma ağırlıklı** paketleri seçiyor\n• %91'i **karmaşık özelliklerden** kaçınıyor\n• %76'sı **sabit aylık ücret** istiyor\n\n🎯 **Popüler Özellikler:**\n• Büyük yazılı faturalar (%95 memnuniyet)\n• 7/24 insan operatör hattı\n• Basit menü yapısı\n\nSize özel basitleştirilmiş paket önerelim mi?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 9: Müşteri Profili Analizi ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "data_driven_professional",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "tech_savvy",
        "donguler": [
            {"rol": "kullanici", "icerik": "Profilim hakkında detaylı bilgi almak istiyorum. Benzer profildeki müşterilerle karşılaştırmalı analiz yapabilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Veri odaklı yaklaşımınızı takdir ediyorum! Profilinizi detaylı analiz edelim ve benzer müşterilerle karşılaştırayım.", "arac_cagrilari": [{"fonksiyon": "get_customer_profile", "parametreler": {"user_id": 10011}}]},
            {"rol": "arac", "icerik": create_mock_response("get_customer_profile", user_id=10011, name="Ahmet Yılmaz", phone_numbers=[{"number": "+905551234567", "type": "mobile", "status": LineStatus.ACTIVE}], email="ahmet@example.com", address="İstanbul, Kadıköy", registration_date="2023-01-15", customer_tier="gold").model_dump_json()},
            {"rol": "asistan", "icerik": "👤 **Profil Karşılaştırma Analizi:**\n\n🏆 **Gold Tier Müşteri Özellikleri:**\n• %89'u **teknoloji sektöründe** çalışıyor\n• %76'sı **premium hizmetleri** tercih ediyor\n• Ortalama müşteri yaşı: 32\n\n📊 **Benzer Profil Tercihleri:**\n• %94'ü **5G paketlerini** kullanıyor\n• %78'i **business servislerini** aktif ediyor\n\nSize özel premium hizmetler önerelim mi?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 10: Teknoloji Meraklısı Profil ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "tech_enthusiast",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "cultural_context": "early_adopter",
        "donguler": [
            {"rol": "kullanici", "icerik": "Teknoloji tutkunu biriyim, 5G ve yeni özellikler beni heyecanlandırıyor. Benimle aynı ilgi alanlarına sahip müşteriler ne kullanıyor?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Harika! Teknoloji meraklılarımız için özel analizimiz var. Önce bulunduğunuz bölgedeki 5G kapsamını kontrol edelim.", "arac_cagrilari": [{"fonksiyon": "check_5g_coverage", "parametreler": {"user_id": 10007, "location": "current_location"}}]},
            {"rol": "arac", "icerik": create_mock_response("check_5g_coverage", user_id=10007, location="Ankara Çankaya", coverage_status="available", signal_strength=88, download_speed_estimate_mbps=920.0, upload_speed_estimate_mbps=200.0, latency_estimate_ms=3, network_quality="excellent", coverage_percentage=94).model_dump_json()},
            {"rol": "asistan", "icerik": "🚀 **Tech Enthusiast Analizi:**\n\n⚡ **Teknoloji Meraklısı Tercihleri:**\n• %94'ü **5G Unlimited** paketini kullanıyor\n• %87'si **beta test programına** katılıyor\n• %79'u **cloud gaming** hizmetini aktif ediyor\n\n🎮 **Popüler Eklentiler:**\n• VR/AR optimizasyonu (%92 memnuniyet)\n• IoT cihaz desteği (%88 kullanım)\n• Gelişmiş ağ analitikleri\n\nSize cutting-edge paket önerilerini sunayım!", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 9: Seyahat Tutkunu Profil ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "travel_enthusiast",
        "cognitive_state": CognitiveState.INTUITIVE.value,
        "emotional_context": EmotionalContext.ANTICIPATION.value,
        "cultural_context": "global_traveler",
        "donguler": [
            {"rol": "kullanici", "icerik": "Sürekli seyahat ediyorum, yurt içi ve yurt dışı. Benimle aynı yaşam tarzına sahip müşteriler hangi hizmetleri tercih ediyor?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Gezgin ruhlu müşterilerimizi çok iyi tanıyoruz! Seyahat eden müşterilerimizin tercihlerini analiz edeyim. Önce roaming durumunuzu kontrol edelim.", "arac_cagrilari": [{"fonksiyon": "enable_roaming", "parametreler": {"user_id": 10008, "status": True}}]},
            {"rol": "arac", "icerik": create_mock_response("enable_roaming", user_id=10008, roaming_enabled=True, activation_time="2024-03-01T15:00:00Z", daily_fee=25.00, data_package="2GB/day").model_dump_json()},
            {"rol": "asistan", "icerik": "✈️ **Seyahat Tutkunu Analizi:**\n\n🌍 **Gezgin Müşteri Tercihleri:**\n• %91'i **Global Roaming** paketini kullanıyor\n• %78'i **çoklu ülke** planlarını tercih ediyor\n• %85'i **travel app** paketlerini seviyor\n\n📱 **Seyahat Odaklı Hizmetler:**\n• Havalimanı WiFi önceliği (%89 memnuniyet)\n• Çevrimdışı harita desteği (%94 kullanım)\n• Acil durum GPS takibi\n\nSize özel gezgin paketi hazırlayalım mı?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 11: İnternet Hız Testi Karşılaştırması ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "performance_focused",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "cultural_context": "tech_professional",
        "donguler": [
            {"rol": "kullanici", "icerik": "İnternetim yavaş geliyor. Benimle aynı bölgedeki müşteriler ne kadar hız alıyor? Karşılaştırmalı analiz yapabilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Performans odaklı yaklaşımınızı anlıyorum! Bölgesel hız karşılaştırması yapalım. Önce sizin mevcut hızınızı test edelim.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": 10012}}]},
            {"rol": "arac", "icerik": create_mock_response("test_internet_speed", user_id=10012, download_speed_mbps=47.5, upload_speed_mbps=12.3, ping_ms=18, test_timestamp="2024-03-01T14:30:00Z", test_server="Istanbul-1", quality_rating="good").model_dump_json()},
            {"rol": "asistan", "icerik": "📊 **Bölgesel Hız Karşılaştırması:**\n\n⚡ **Sizin Hızınız:** 47.5 Mbps ↓ / 12.3 Mbps ↑\n\n📈 **Aynı Bölge Ortalaması:**\n• Download: 52.8 Mbps (Siz %90 seviyesindesiniz)\n• Upload: 15.2 Mbps (Siz %81 seviyesindesiniz)\n• Ping: 15ms ortalama (Sizinki 18ms)\n\n🎯 **İyileştirme Önerileri:**\n• Fiber paketine geçiş (%34 hız artışı)\n• Modem optimizasyonu\n\nHız artırım planı hazırlayalım mı?", "arac_cagrilari": None}
        ]
    })

    # === SENARYO 12: Sosyal Medya Odaklı Kullanıcı ===
    scenarios.append({
        "id": f"collaborative_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.COLLABORATIVE_FILTERING.value,
        "personality_profile": "social_media_influencer",
        "cognitive_state": CognitiveState.CREATIVE.value,
        "emotional_context": EmotionalContext.COMPETITIVE.value,
        "cultural_context": "digital_native",
        "donguler": [
            {"rol": "kullanici", "icerik": "Sosyal medyada çok aktifim, içerik üretiyorum. Benimle aynı alanda çalışan influencerlar hangi paketleri kullanıyor?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "İçerik üreticileri için özel analizlerimiz var! Sosyal medya odaklı müşterilerimizin tercihlerini inceleyelim. Önce mevcut kullanımınızı görelim.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": 10009}}]},
            {"rol": "arac", "icerik": create_mock_response("get_remaining_quotas", internet_remaining_gb=12.8, voice_remaining_minutes=1200, sms_remaining=150, period_end="2024-03-31", usage_percentage={"internet": 76, "voice": 40, "sms": 70}).model_dump_json()},
            {"rol": "asistan", "icerik": "📱 **İnfluencer Profili Analizi:**\n\n🎥 **İçerik Üreticisi Tercihleri:**\n• %89'u **Sınırsız Sosyal Medya** paketini kullanıyor\n• %76'sı **yüksek upload hızını** tercih ediyor\n• %92'si **canlı yayın optimizasyonu** istiyor\n\n📊 **Popüler Özellikler:**\n• Instagram/TikTok sınırsız (%96 memnuniyet)\n• Yüksek kalite video upload (%88 kullanım)\n• Analitik raporlama araçları\n\nİçerik üretici paketinizi özelleştirelim!", "arac_cagrilari": None}
        ]
    })

    return scenarios


def generate_collaborative_filtering_scenario() -> List[Dict[str, Any]]:
    """
    Tüm işbirlikçi filtreleme senaryolarını döndürür.
    """
    all_scenarios = generate_collaborative_filtering_scenarios()
    if not all_scenarios:
        return []
    return all_scenarios