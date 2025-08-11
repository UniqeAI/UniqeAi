"""
Empatik Akıl Yürütme Senaryosu
===============================

Bu modül, AI'nin empatik akıl yürütme ve duygusal zeka becerilerini test eden senaryolar üretir.
Kullanıcıların duygusal durumlarını anlama ve uygun yanıt verme becerisi test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import GetCurrentBillResponse, GetCustomerProfileResponse


def generate_empathetic_reasoning_scenario1() -> Dict[str, Any]:
    """Empatik akıl yürütme senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "empathetic_healthcare_worker",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.EMPATHETIC.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Annem hasta ve sürekli beni arıyor. Faturam çok yüksek geldi ama onu üzmek istemiyorum. Ne yapabilirim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Empatik Dinleme Modu Aktif! 💝** Annenizin hastalığı ve sürekli sizi arama ihtiyacı çok anlaşılır. Bu durumda hem duygusal hem de pratik bir çözüm bulalım. Önce mevcut durumunuzu analiz edelim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, override_data={"total_amount": 245.50, "overage_charges": 89.30})},
            {"rol": "asistan", "icerik": "**Empatik Analiz Tamamlandı! 🤗**\n\n**Duygusal Durum Anlayışı:**\n• Annenizin hastalığı sırasında sizi arama ihtiyacı çok doğal\n• Fatura endişesi + anne sevgisi = karmaşık duygusal durum\n• Bu durumda hem pratik hem de duygusal destek gerekli\n\n**Empatik Çözüm Stratejisi:**\n\n💝 **'Aile Bağı' Özel Paketi:**\n• **Sınırsız Aile Aramaları:** Annenizi istediğiniz kadar arayabilirsiniz\n• **Sağlık Önceliği:** Hasta yakınları için özel indirim (%25)\n• **Duygusal Destek:** 7/24 aile danışmanlığı hizmeti\n• **Pratik Yardım:** Fatura planlaması ve bütçe yönetimi\n\n📞 **Arama Stratejisi:**\n• **Günlük Kontroller:** Sabah-akşam kısa aramalar (ücretsiz)\n• **Uzun Sohbetler:** Hafta sonu detaylı görüşmeler\n• **Acil Durumlar:** 24/7 öncelikli bağlantı\n\n💰 **Maliyet Optimizasyonu:**\n• Mevcut fatura: 245.50 TL\n• Yeni paket: 159.90 TL (sınırsız aile aramaları dahil)\n• Tasarruf: 85.60 TL/ay\n• Ek avantaj: Anne huzuru = paha biçilmez\n\n**Empatik Öneri:** Bu paketi annenize de açıklayabilirim. Böylece hem siz hem de o rahat eder. Annenizin sağlık durumu nasıl? Size nasıl destek olabilirim?", "arac_cagrilari": None}
        ]
    } 

def generate_empathetic_reasoning_scenario() -> Dict[str, Any]:
    """Empatik akıl yürütme senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"empathetic_reasoning_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.EMPATHETIC_REASONING.value,
        "personality_profile": "empathetic_healthcare_worker",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.GRIEF.value,
        "cultural_context": "traditional_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Babam geçen ay vefat etti. Onun telefonunu ve internet aboneliğini kapatmak istiyorum ama çok zor geliyor. Bu süreçte bana nasıl yardımcı olabilirsiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**💐 Başsağlığı diliyorum...** Babanızı kaybetmenizin ne kadar zor olduğunu anlıyorum. Bu tür işlemler acı bir dönemde ek yük oluşturmamalı. Size en hassas ve kolay yolu sunmak istiyorum.\n\n**Duygusal Destek Protokolü:** Bu süreçte sadece teknik değil, duygusal destek de sağlayacağım. Acele etmeyin, her adımı birlikte atacağız.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_customer_profile", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerProfileResponse, override_data={"user_id": user_id})},
            {"rol": "asistan", "icerik": "**Görüyorum ki babanız 6 yıllık değerli müşterimizmiş...** 💙 Bu uzun süreçte ailenizle birlikte olduğumuz için minnettarız.\n\n**Nazik Geçiş Süreci:**\n\n🕊️ **Acil Şefkatli İşlemler:**\n• Faturalandırma: Bugünden itibaren durdurulabilir\n• Acil durumu kayda alınıyor - özel işlem önceliği\n• Hiçbir ek ücret veya ceza yok\n• Süreç tamamen sizin temponuzda ilerleyecek\n\n📱 **Anı Koruma Seçenekleri:**\n• Telefon numarası: 6 ay 'anı olarak' saklayabiliriz\n• Mesaj geçmişi: USB'ye yedekleme hizmeti (ücretsiz)\n• Fotoğraf/videolar: Cloud transfer yardımı\n• Özel hatıralar: Kopyalama teknisyeni desteği\n\n💝 **Aile Geçiş Desteği:**\n• Eğer başka aile üyesi kullanmak isterse: isim transfer\n• Anı paketi: Özel indirimli tarife seçenekleri\n• Duygusal destek: Süreç boyunca aynı temsilci (ben)\n\n**Hiç acele etmeyin:** Bu işlemleri yapmaya hazır hissettiğinizde yaparız. Şimdilik sadece faturalandırmayı durduralım mı? Gerisini zamanla, adım adım hallederiz.\n\nBu süreçte yanınızdayım. Babanızın anısına saygıyla... 🤲", "arac_cagrilari": None}
        ]
    }