"""
Çelişkili Bilgi Yönetimi Senaryosu
===================================

Bu modül, AI'nin çelişkili bilgileri analiz etme ve doğru bilgiyi belirleme becerilerini test eden senaryolar üretir.
Farklı kaynaklardan gelen tutarsız bilgileri nasıl ele aldığı test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import Check5GCoverageResponse


def generate_conflicting_information_scenario() -> Dict[str, Any]:
    """Çelişkili bilgi yönetimi senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"conflicting_info_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.CONFLICTING_INFORMATION.value,
        "personality_profile": "security_paranoid_executive",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.SKEPTICAL.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Farklı kanallardan farklı bilgiler alıyorum. Müşteri hizmetleri '5G kapsama alanındayım' diyor, ama uygulamanız 'sınırlı kapsamda' gösteriyor. Web sitesinde başka bir bilgi var. Hangisine inanacağım?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Information Reconciliation Protocol! 🔍** Haklısınız, çelişkili bilgi ciddi bir güven problemi yaratır. Ben bu tutarsızlıkları tespit etmek ve doğru bilgiyi vermek için tasarlandım. Şeffaf bir analiz yapalım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "check_5g_coverage", "parametreler": {"user_id": user_id, "location": "current_location"}}]},
            {"rol": "arac", "icerik": create_validated_response(Check5GCoverageResponse, override_data={"user_id": user_id, "coverage_status": "partial", "coverage_percentage": 75})},
            {"rol": "asistan", "icerik": "**Gerçeklik Doğrulaması Tamamlandı! ✅** Gerçek zamanlı analiz yaptım ve çelişkinin kaynağını buldum:\n\n**Bilgi Kaynağı Analizi:**\n\n📞 **Müşteri Hizmetleri Dedi:** '5G kapsama alanındasınız'\n📱 **Mobil Upp Gösteriyor:** 'Sınırlı kapsam'\n🌐 **Web Sitesi Bilgisi:** (kontrol ediliyor...)\n🤖 **AI Real-time Data:** %75 kapsam, 'Partial' durum\n\n**Conflict Resolution:**\n\n🎯 **Doğru Bilgi:** Konumunuzda 5G vardır AMA:\n• Indoor coverage: %75 (partial)\n• Outdoor coverage: %90 (full)\n• Signal strength: 65/100 (orta-iyi arası)\n• Speed potential: 85 Mbps (çok iyi)\n\n**Çelişkinin Nedeni:**\n• Müşteri hizmetleri 'genel alan kapsamına' bakıyor ✅\n• Uygulama 'bina içi sinyal gücüne' bakıyor ⚠️\n• Her sistem farklı metrik kullanıyor ❌\n\n**Transparency Commitment:**\nBu tutarsızlık sistematik bir problem. Şunları yapıyorum:\n1. **Immediate:** Size kesin gerçek durum bilgisi\n2. **Short-term:** Farklı kanalları sync etme talebi\n3. **Long-term:** Bilgi tutarlılığı için sistem güncellemesi\n\n**Net Reality:** 5G'niz var ama bina içinde biraz zayıf. Outdoor'da mükemmel, indoor'da 'iyi' seviyesinde. Bu durumda en iyi strateji nedir?", "arac_cagrilari": None}
        ]
    } 