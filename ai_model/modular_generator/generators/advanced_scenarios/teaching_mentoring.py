"""
Öğretim ve Mentorluk Senaryosu
==============================

Bu modül, AI'nin öğretim ve mentorluk becerilerini test eden senaryolar üretir.
Kullanıcıların öğrenme süreçlerinde AI'nin nasıl rehberlik ettiği test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import GetRemainingQuotasResponse


def generate_teaching_mentoring_scenario() -> Dict[str, Any]:
    """Öğretim ve mentorluk senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"teaching_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.TEACHING_MENTORING.value,
        "personality_profile": "empathetic_healthcare_worker",
        "cognitive_state": CognitiveState.EDUCATIONAL.value,
        "emotional_context": EmotionalContext.CURIOUS.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Teknoloji konusunda pek iyi değilim. Bu 'internet kotası' dediğiniz şey nedir? Nasıl kontrol ederim? Sürekli yetmiyor gibi hissediyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Öğretim modu aktif:** Çok güzel bir soru sordunuz! İnternet kotasını en basit şekilde anlatayım ve birlikte öğrenelim. Teknoloji herkesi korkutabilir, ama adım adım gittiğimizde çok kolay hale gelir.\n\n**Benzetme ile açıklayayım:** İnternet kotası, cep telefonu dakikası gibi düşünün. Eskiden 'kaç dakika konuştum?' diye merak ederdiniz, değil mi? İnternet kotası da aynı mantık - sadece konuşma yerine 'veri kullanımı' ölçüyoruz.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, override_data={"usage_percentage": {"internet": 75, "voice": 10, "sms": 5}})},
            {"rol": "asistan", "icerik": "**Öğrenme hikayeniz:** Bakın, şu anda durumunuz çok iyi! Size öğretici bir analiz yapayım:\n\n📚 **Ders 1 - Mevcut Durumunuz:**\n• 50 GB kotanızın 37.5 GB'ını kullanmışsınız (%75)\n• Geriye 12.5 GB kaldı (ayın sonuna 10 gün var)\n• Günde ortalama 1.25 GB kullanabilirsiniz\n\n📚 **Ders 2 - Bu Ne Demek:**\n• WhatsApp mesajları: günde yüzlerce (çok az veri)\n• Fotoğraf göndermek: 1 MB (orta)\n• Video izlemek: saatte 1 GB (en çok veri)\n\n**Öğretici soru:** Video izlemeyi çok kullanıyor musunuz? Youtube, Netflix, Instagram videoları?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Evet, torunlarımın videolarını WhatsApp'ta izliyorum. Bir de akşamları haber izliyorum internetten. Bu çok mu veri harcar?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Öğrenme ilerliyor - mükemmel gözlem!** Şimdi size pratik hayattan örneklerle açıklayayım:\n\n📚 **Ders 3 - Video Tüketimi Analizi:**\n\n👶 **Torun videoları (WhatsApp):**\n• 1 dakikalık video ≈ 10-15 MB\n• Günde 10 video izlerseniz ≈ 150 MB\n• Ayda ≈ 4.5 GB (bu normal ve tatlı!)\n\n📺 **Haber izleme:**\n• 1 saat canlı haber ≈ 1 GB\n• Günde 2 saat ≈ 60 GB/ay (işte asıl tüketim burada!)\n\n**Öğretici çözüm:** Size özel 'Büyükanne/Büyükbaba Stratejisi' önerebilirim:\n\n💡 **Akıllı İzleme Yöntemi:**\n• Haberleri Wi-Fi'da izleyin (evde internetten)\n• Torun videolarını mobil veriyle izleyin (her yerde)\n• Wi-Fi yoksa haber kalitesini 'düşük' yapın (yarı veri harcar)\n\n**Öğrenme sorusu:** Evinizde Wi-Fi internet var mı? Telefonu Wi-Fi'a bağlamayı biliyor musunuz?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Wi-Fi var ama nasıl bağlanacağımı bilmiyorum. Öğretir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Ders 4 - Wi-Fi Bağlantısı (Adım Adım):**\n\nTabii ki öğretirim! En basit yöntemle:\n\n🔧 **Telefonunuzda (Android için):**\n1️⃣ **Ayarlar** uygulamasını açın (dişli simgesi)\n2️⃣ **Wi-Fi** yazısına dokunun (genelde en üstte)\n3️⃣ Wi-Fi'ı **AÇIN** (kapalıysa)\n4️⃣ Evinizin adını bulun (router/modem üzerinde yazıyor)\n5️⃣ Şifreyi girin (yine router üzerinde yazıyor)\n\n📍 **Router/Modem nerede?** Genelde televizyonun yanında, ışıklı küçük kutu\n\n**Öğrenme tüyosu:** Bir kere bağlandıktan sonra telefon hep hatırlar! Bir daha yapmaya gerek yok.\n\n**Ders 5 - Başarı Kontrolü:**\n• Wi-Fi bağlıyken sol üstte Wi-Fi simgesi görünür\n• Artık video izlerken kota harcamazsınız!\n• Torun videolarını istediğiniz kadar izleyebilirsiniz 💕\n\n**Mentorluk sorusu:** Bu adımları deneyip sonucu bana söyler misiniz? Takıldığınız nokta olursa yardım ederim!"}
        ]
    } 