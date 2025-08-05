"""
Adaptif İletişim Senaryosu
===========================

Bu modül, AI'nin adaptif iletişim ve kullanıcı tercihlerine göre iletişim tarzını ayarlama becerilerini test eden senaryolar üretir.
Farklı kullanıcı profillerine göre iletişim tarzını nasıl değiştirdiği test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response

def generate_adaptive_communication_scenarios() -> List[Dict[str, Any]]:
    """
    50 adet uzman seviyesi adaptif iletişim senaryosu üretir.
    """
    scenarios = []

    # 1. Sabırsız ve Teknik Bilgisi Yüksek Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "personality_profile": "impatient_tech_savvy",
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "İnternetim yine yavaş, hız testi yapın ve sonucu söyleyin. Teknik detaylarla boğmayın.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Hızlı Mod Aktif!** ⚡\nAnlaşıldı, hemen hız testi başlatıyorum.", "arac_cagrilari": [
                {"fonksiyon": "test_internet_speed", "parametreler": {"user_id": generate_user_id()}}
            ]},
            {"rol": "arac", "icerik": create_validated_response("TestInternetSpeedResponse", {"download_speed_mbps": 12.5, "upload_speed_mbps": 2.1, "ping_ms": 45})},
            {"rol": "asistan", "icerik": "Hız testiniz tamamlandı. İndirme: 12.5 Mbps, Yükleme: 2.1 Mbps. Bu değerler normalin altında. Hemen arıza kaydı oluşturalım mı?", "arac_cagrilari": None}
        ]
    })

    # 2. Yaşlı ve Teknolojiden Anlamayan Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "personality_profile": "elderly_non_tech",
        "cognitive_state": CognitiveState.CONFUSED.value,
        "emotional_context": EmotionalContext.ANXIOUS.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Evladım, bu fatura çok karışık. Ne kadar ödeyeceğim ben şimdi?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Basit Anlatım Modu Aktif!** ☕\nMerhabalar teyzeciğim, hiç merak etmeyin, ben size yardımcı olacağım. Faturanızı hemen kontrol ediyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_current_bill", "parametreler": {"user_id": generate_user_id()}}
            ]},
            {"rol": "arac", "icerik": create_validated_response("GetCurrentBillResponse", {"amount": 85.50, "due_date": "2024-08-20"})},
            {"rol": "asistan", "icerik": "Toplam borcunuz 85.50 TL. Son ödeme tarihiniz de 20 Ağustos. Başka bir konuda yardımcı olabilir miyim?", "arac_cagrilari": None}
        ]
    })

    # 3. Şüpheci ve Detaycı Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "personality_profile": "skeptical_detail_oriented",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.DISTRUSTFUL.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Paketimde ne kadar internet kaldığını tam olarak GB ve MB cinsinden öğrenmek istiyorum. Bana yuvarlak rakamlar vermeyin.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Detaylı Bilgi Modu Aktif!** 🔍\nTabii ki, kalan kullanım haklarınızı en ince ayrıntısına kadar iletiyorum.", "arac_cagrilari": [
                {"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": generate_user_id()}}
            ]},
            {"rol": "arac", "icerik": create_validated_response("GetRemainingQuotasResponse", {"internet_remaining_gb": 15.7, "voice_remaining_minutes": 342, "sms_remaining": 876})},
            {"rol": "asistan", "icerik": "Kalan kullanım haklarınız tam olarak: 15.7 GB (yani 16076.8 MB) internet, 342 dakika konuşma ve 876 SMS. Bu veriler anlıktır.", "arac_cagrilari": None}
        ]
    })
    
    # ... (Buraya 47 senaryo daha eklenecek) ...

    # 50. Yurt Dışına Çıkacak ve Endişeli Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "personality_profile": "anxious_traveler",
        "cognitive_state": CognitiveState.PLANNING.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Yarın yurt dışına çıkıyorum ve faturamın çok yüksek gelmesinden korkuyorum. Ne yapmam lazım?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Güven Verici Mod Aktif!** ✅\nEndişelenmenize hiç gerek yok, yurt dışı kullanımınız için en uygun çözümleri birlikte bulacağız. Hattınızda yurt dışı kullanım (roaming) aktif mi, hemen kontrol edelim.", "arac_cagrilari": [
                {"fonksiyon": "enable_roaming", "parametreler": {"user_id": generate_user_id(), "status": True}}
            ]},
            {"rol": "arac", "icerik": create_validated_response("EnableRoamingResponse", {"roaming_enabled": True, "daily_fee": 25.0})},
            {"rol": "asistan", "icerik": "Evet, hattınız yurt dışı kullanımına açık. Sürpriz faturalarla karşılaşmamanız için size özel yurt dışı paketlerimizi önerebilirim. İster misiniz?", "arac_cagrilari": None}
        ]
    })
    
    return scenarios

# Bu ana fonksiyon, core_generator tarafından çağrılacak
def generate_adaptive_communication_scenario() -> Dict[str, Any]:
    """
    Havuzdan rastgele bir adaptif iletişim senaryosu seçer ve döndürür.
    """
    all_scenarios = generate_adaptive_communication_scenarios()
    return random.choice(all_scenarios)
