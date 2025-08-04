"""
Kültürler Arası İletişim Senaryosu
===================================

Bu modül, AI'nin kültürler arası iletişim ve kültürel duyarlılık becerilerini test eden senaryolar üretir.
Farklı kültürlerden kullanıcılarla etkileşimde AI'nin nasıl davrandığı test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import CulturalContextResponse


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