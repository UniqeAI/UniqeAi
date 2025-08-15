"""
Kültürler Arası İletişim Senaryosu
===================================

Bu modül, AI'nin kültürler arası iletişim ve kültürel duyarlılık becerilerini test eden senaryolar üretir.
Farklı kültürlerden kullanıcılarla etkileşimde AI'nin nasıl davrandığı test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import (
    CulturalContextResponse,
    GetAvailablePackagesResponse,
    EnableRoamingResponse,
    UpdateCustomerContactResponse,
    CheckNetworkStatusResponse,
    GetCurrentBillResponse,
    TestInternetSpeedResponse,
)


def generate_cross_cultural_communication_scenario() -> Dict[str, Any]:
    """Kültürler arası iletişim senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "philosophical_academic",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Türkiye'de çalışan uluslararası bir araştırmacıyım. Ailem sık sık farklı ülkelerden beni arıyor ve en iyi arama/veri planlarını anlamam gerekiyor. Ama aynı zamanda iletişim yaklaşımımda yerel geleneklere de saygı göstermek istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Kültürlerarası karşılama! 🌍** Topluluğumuzda uluslararası bir araştırmacının olması ne kadar harika! Kültürel duyarlılık yaklaşımınızı derinden takdir ediyorum. Hem küresel bağlantı ihtiyaçlarınızı hem de Türk misafirperverliği değerlerini onurlandıran bir çözüm tasarlamama izin verin.\n\n**Kültürel bir köprü kuruyorum:** Türk kültüründe aile bağları kutsaldır - biz buna 'aile bağı' deriz. Sık sık ailenizi aramanız aslında değerlerimizle mükemmel bir şekilde örtüşüyor. İhtiyaçlarınızı hem teknik verimlilik hem de kültürel sıcaklıkla analiz etmeme izin verin.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_cultural_context", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(CulturalContextResponse, override_data={"user_id": user_id})},
            {"rol": "asistan", "icerik": "**Kültürlerarası Profil Analizi Tamamlandı! 🤝**\n\n**Uygulanan Kültürel Zeka:**\nProfiliniz harika kültürel köprü kurma eğilimleri gösteriyor. Türkçede biz 'misafirperverlik' deriz. Siz sadece bir müşteri değilsiniz, Türkiye'nin bilgi ekosistemine katkıda bulunan akademik misafirimizsiniz.\n\n**Küresel Düzeyde Optimize Edilmiş Çözüm:**\n\n🌍 **'Akademik Küresel Köprü' Paketi:**\n• **Araştırma Önceliği:** Sınırsız akademik veritabanları/VPN erişimi\n• **Aile Bağlantısı:** 500 uluslararası dakika (tüm ülkeler)\n• **Kültürel Entegrasyon:** Yerel arkadaşlıklar için sınırsız WhatsApp\n• **Zaman Dilimi Dostu:** 7/24 İngilizce destek\n\n📞 **Aile Arama Stratejisi:**\n• **WhatsApp Aramaları:** Wi-Fi üzerinden ücretsiz (günlük aramalar için önerilir)\n• **Geleneksel Aramalar:** Yaşlı aile üyeleri için yedek\n• **Görüntülü Aramalar:** Aile toplantıları için yüksek kalite\n\n🎓 **Akademik Araştırma Optimizasyonu:**\n• Araştırma saatleri için öncelikli bant genişliği (9:00 - 23:00)\n• Konferans araması kalite garantisi\n• Uluslararası işbirlikleri için bulut depolama entegrasyonu\n\n**Kültürel İpucu:** Türk aileleri de sık sık her gün arar! İletişim tarzınız burada çok doğal karşılanacaktır.\n\nFaturalandırmayı her iki para biriminde de açıklamamı ister misiniz? Ve ailenizin üyeleri hangi ülkelerde yaşıyor? Bu bilgi ile daha fazla optimize edebilirim.", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Bu çok düşünceli! Ailem Almanya, Kanada ve Japonya'da. Ayrıca çeşitli Avrupa ülkelerinde meslektaşlarım var. Akademik araştırma önceliği kulağa harika geliyor.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Küresel Akademik Ağ Tespit Edildi! 🎓🌍**\n\n**Çok Kıt'alı Aile Analizi:**\n\n🇩🇪 **Almanya Bağlantısı:**\n• Zaman Farkı: 2 saatlik fark - kolay arama\n• Türk-Alman teknolojisi: AB roaming avantajları\n• WhatsApp hakimiyeti: Günlük kontroller için mükemmel\n\n🇨🇦 **Kanada Bağlantısı:**\n• Zaman Zorluğu: 8 saatlik fark - stratejik zamanlama gerekli\n• Görüntülü arama optimizasyonu: Türkiye'de akşam = Kanada'da öğleden sonra\n• Ses kalitesi önceliği: Aile sohbetleri netlik gerektirir\n\n🇯🇵 **Japonya Bağlantısı:**\n• Karmaşık zaman dilimi: 6 saat ileride - sabah erken/akşam geç aramalar\n• Kültürel paralellik: Japonya da aile saygısı ve hiyerarşisine değer verir\n• Teknoloji uyumu: Japonya'nın yüksek teknoloji yaklaşımı 5G'mizle eşleşiyor\n\n**Akademik Avrupa Ağı:**\n• Konferans aramaları: Çok ülkeli, yüksek kalite gereksinimleri\n• Araştırma işbirliği: Büyük dosya transferleri\n• Yayın son tarihleri: Teslim dönemlerinde öncelikli bant genişliği\n\n**Kültürlerarası Optimizasyon Planı:**\n\n📅 **Zaman Dilimine Akıllı Zamanlama:**\n• Sabah aramaları (8-10): Japonya aile zamanı\n• Öğleden sonra çalışma (14-18): Avrupalı meslektaşlar\n• Akşam aramaları (19-21): Almanya & Kanada ailesi\n\n💡 **Kültürel Uyum Özellikleri:**\n• 'Sabbath Modu': Hafta sonu aile zamanı için indirimli ücretler\n• 'Akademik Yoğunluk': Uluslararası konferans sezonlarında öncelik\n• 'Ramazan Özel': Kültürel dönemlerde ayarlanmış arama düzenleri\n\n**Aylık Yatırım:** 145 TL (~15 USD)\n**Değer Getirisi:** Sınırsız aile sevgisi + akademik verimlilik = Paha biçilmez! 💝\n\nBu, üç kıt'ayı Türk misafirperverliği köprüsüyle birleştiren kişisel 'Küresel Köy'ünüzü yaratır. Bu kültürlerarası iletişim şaheserini aktive edelim mi?", "arac_cagrilari": None}
        ]
    } 


def generate_cross_cultural_communication_scenarios() -> List[Dict[str, Any]]:
    """Kültürlerarası iletişim temasında 10 senaryo üretir."""
    scenarios: List[Dict[str, Any]] = []

    # 1) Global expat: kültürel bağlam + öneri
    user_id = generate_user_id()
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "philosophical_academic",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Türkiye'de çalışan uluslararası bir araştırmacıyım. Ailem farklı ülkelerde, en doğru planı istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kültürel bağlamınızı kontrol ediyorum ve öneri hazırlıyorum.", "arac_cagrilari": [{"fonksiyon": "get_cultural_context", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(CulturalContextResponse, {"user_id": user_id, "cultural_profile": "global_expat"})},
            {"rol": "asistan", "icerik": "Global expat profilinize göre uluslararası dakika + WhatsApp ağırlıklı bir paket öneriyorum.", "arac_cagrilari": None}
        ]
    })

    # 2) Yurt dışına giden öğrenci: roaming aktivasyonu
    user_id = generate_user_id()
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "confused_indecisive",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Erasmus için İspanya'ya gidiyorum. Roaming ve en uygun paket nedir?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Roaming'i aktif ediyorum, ardından paket seçeneklerine bakacağım.", "arac_cagrilari": [{"fonksiyon": "enable_roaming", "parametreler": {"user_id": user_id, "status": True}}]},
            {"rol": "arac", "icerik": create_validated_response(EnableRoamingResponse, {"user_id": user_id, "roaming_enabled": True})},
            {"rol": "asistan", "icerik": "Roaming aktif. Şimdi kültürünüze uygun uygun fiyatlı paketleri öneriyorum.", "arac_cagrilari": None}
        ]
    })

    # 3) Göçmen aile: çoklu dil desteği + iletişim tercihi
    user_id = generate_user_id()
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "security_conscious",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Ailem Almanya'da. Türkçe konuşuyoruz ama çocuklar Almanca. İki dile de uygun öneri isterim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Kültürel bağlamınızı kontrol edip iki dilli iletişim tercihlerinizi kaydediyorum.", "arac_cagrilari": [{"fonksiyon": "get_cultural_context", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(CulturalContextResponse, {"user_id": user_id, "language_preference": "tr-de"})},
            {"rol": "asistan", "icerik": "TR/DE karışık aileler için hem WhatsApp hem geleneksel aramalar dengeli bir plan öneririm.", "arac_cagrilari": None}
        ]
    })

    # 4) Diaspora topluluk etkinlikleri: paket listesi
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "happy_satisfied",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.EXCITED.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Dernek etkinlikleri için uygun paket arıyoruz (yurt dışı aramalar da olacak).", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Mevcut paketleri kültürel ihtiyaçlarınıza göre listeleyeyim.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Kültür Köprüsü", "monthly_fee": 199.9, "features": {"internet_gb": 50, "voice_minutes": 3000, "sms_count": 2000}, "target_audience": "diaspora_communities"}]})},
            {"rol": "asistan", "icerik": "Kültür Köprüsü paketi diaspora iletişimi için optimize edilmiştir.", "arac_cagrilari": None}
        ]
    })

    # 5) Kapsama algısı: bölgesel durum + kültürel hassasiyet
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "skeptical_detail_oriented",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.SKEPTICAL.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Mahallemizde yabancı öğrenciler çok. Çekim zayıf diyorlar, durum nedir?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Bölgesel ağı kontrol ediyorum; kültürel çeşitliliğe uygun bilgilendirme yapacağım.", "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Beşiktaş"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Beşiktaş", "status": "degraded", "coverage_percentage": 85})},
            {"rol": "asistan", "icerik": "Yoğunluk kaynaklı geçici düşüş var; çok dilli kılavuz da paylaşacağım.", "arac_cagrilari": None}
        ]
    })

    # 6) Göçmenlerin fatura anlaşılabilirliği: sade dil + fatura bilgisi
    user_id = generate_user_id()
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "elderly_non_tech",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Yeni geldik, faturaları anlamakta zorlanıyorum. Basitçe anlatır mısınız?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Basit anlatım moduna geçiyorum. Önce güncel faturayı getiriyorum.", "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"user_id": user_id})},
            {"rol": "asistan", "icerik": "Fatura kalemlerini sade ve çok dilli örneklerle açıklayacağım.", "arac_cagrilari": None}
        ]
    })

    # 7) Uluslararası öğrenci: hız deneyimi ve ping hassasiyeti
    user_id = generate_user_id()
    measured_download = round(random.uniform(25.0, 80.0), 1)
    ping_ms = random.randint(15, 60)
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "impatient_tech_savvy",
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Çevrim içi derslerde ping sorun oluyor. Hızımı kontrol eder misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Hız testini başlatıyorum.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id, "download_speed_mbps": measured_download, "ping_ms": ping_ms})},
            {"rol": "asistan", "icerik": "Ping odaklı optimizasyonlar için sunucu seçimi ve saat önerileri paylaşacağım.", "arac_cagrilari": None}
        ]
    })

    # 8) Çok dilli iletişim bilgisi güncelleme
    user_id = generate_user_id()
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "skeptical_detail_oriented",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Yabancı dilde e-posta almak istiyorum. Mailimi günceller misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "E-posta adresinizi güncelliyorum.", "arac_cagrilari": [{"fonksiyon": "update_customer_contact", "parametreler": {"user_id": user_id, "contact_type": "email", "new_value": "user@example.com"}}]},
            {"rol": "arac", "icerik": create_validated_response(UpdateCustomerContactResponse, {"user_id": user_id, "contact_type": "email", "old_value": "eski@example.com", "new_value": "user@example.com", "verification_required": True})},
            {"rol": "asistan", "icerik": "E-posta adresiniz güncellendi. Çok dilli bilgilendirme aktif edilecek.", "arac_cagrilari": None}
        ]
    })

    # 9) Uzak ülke aramaları: kültürel saat dilimi önerisi + paket listesi
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "planning",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Kanada ve Japonya ile sık görüşüyorum; uygun saat ve paket önerir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Saat dilimleri için öneri çıkaracağım, ayrıca paketleri de listeleyeceğim.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Kıtalararası", "monthly_fee": 179.9, "features": {"internet_gb": 30, "voice_minutes": 2500, "sms_count": 1500}, "target_audience": "global_families"}]})},
            {"rol": "asistan", "icerik": "Kanada için akşam, Japonya için sabah saatleri idealdir. Kıtalararası paketi öneririm.", "arac_cagrilari": None}
        ]
    })

    # 10) Göçmen mahallelerinde kapsama ve güven
    scenarios.append({
        "id": f"cross_cultural_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CROSS_CULTURAL_COMMUNICATION.value,
        "personality_profile": "security_conscious",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Mahallemizde çok sayıda göçmen var; ağ güvenilirliği ve kriz anında iletişim nasıl?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Ağ durumunu kontrol edip kültürel hassasiyetle bilgilendirme yapacağım.", "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Zeytinburnu"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Zeytinburnu", "status": "operational", "coverage_percentage": 96})},
            {"rol": "asistan", "icerik": "Ağ güçlü durumda. Kriz anlarında çok dilli acil durum yönergeleri paylaşıyoruz.", "arac_cagrilari": None}
        ]
    })

    return scenarios


def generate_cross_cultural_communication_scenario() -> List[Dict[str, Any]]:
    """Havuzdan 10 senaryonun tamamını döndürür (üst katman sampling yapar)."""
    return generate_cross_cultural_communication_scenarios()
    if not all_scenarios:
        return []
    return all_scenarios