"""
Gelişmiş Hata Kurtarma Senaryosu
=================================

Bu modül, AI'nin gelişmiş hata kurtarma ve problem çözme becerilerini test eden senaryolar üretir.
Karmaşık teknik sorunlarda AI'nin nasıl sistematik çözüm ürettiği test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import GetCurrentBillResponse, CheckNetworkStatusResponse


def generate_advanced_error_recovery_scenario1() -> Dict[str, Any]:
    """Gelişmiş hata kurtarma senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"error_recovery_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "tech_savvy_millennial",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Üç kez fatura ödemeye çalıştım ama sistem hata veriyor. Çok sinirli olmaya başladım!", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Hata Kurtarma Protokolü başlatılıyor! 🔧** Anlıyorum, üç kez denemenize rağmen sistem hatası almak gerçekten sinir bozucu! Teknik sorunları çözmek benim uzmanlık alanım. Sistematik bir yaklaşımla sorunu çözelim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": "{'error': {'code': 'ODEME_GECIDI_HATASI', 'message': 'Ödeme geçidi geçici olarak kullanılamıyor', 'details': 'Geçit 30 saniye sonra zaman aşımına uğradı'}}", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Root Cause Analysis tamamlandı! ✅** Sorun sizde değil, sistemde! Ödeme gateway'inde geçici teknik problem var. İyi haber şu ki: bu tür sorunlar için çoklu backup sistemimiz var.\n\n**Advanced Recovery Strategy:**\n\n🔧 **Immediate Workaround:**\n• Alternatif ödeme yöntemi aktif ediliyor\n• 24 saat geçmişe dönük ödeme koruması\n• Manuel işlem öncelik kuyruğu\n\n🛡️ **Resilience Guarantee:**\n• Gateway hatası durumunda otomatik 48 saat ek süre\n• Geç ödeme faizi iptal\n• Sistem hatası tazminatı\n\n**Şimdi ne yapıyorum:**\n1. Alternatif sistem üzerinden manuel ödeme işlemi\n2. Hesabınıza 'sistem hatası' notu ekliyorum\n3. Önümüzdeki ödemeler için öncelik hesabı aktif ediyorum\n\nFaturanızı şimdi güvenli sistemden ödemek ister misiniz?", "arac_cagrilari": None}
        ]
    } 

def generate_advanced_error_recovery_scenario() -> Dict[str, Any]:
    """Sistem hatalarından kurtarma ve çözüm senaryosu."""
    user_id = generate_user_id()
    return {
        "id": f"advanced_error_recovery_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "tech_savvy_professional",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "cultural_context": "urban_professional",
        "donguler": [
            {"rol": "kullanici", "icerik": "Üçüncü kez deneme yapıyorum ama sistem sürekli hata veriyor. Bu sorunu nasıl çözebiliriz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Hata Kurtarma Protokolü başlatılıyor! 🔧** Anlıyorum, üç kez denemenize rağmen sistem hatası almak gerçekten sinir bozucu! Teknik sorunları çözmek benim uzmanlık alanım. Sistematik bir yaklaşımla sorunu teşhis edip çözelim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Güneydoğu Anadolu"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, override_data={"region": "Güneydoğu Anadolu", "status": "operational"})},
            {"rol": "asistan", "icerik": "Sistem durumunu kontrol ettim ve her şey normal görünüyor. Sorun geçici bir bağlantı problemi olabilir. Alternatif bir çözüm yolu deneyelim.", "arac_cagrilari": None}
        ]
    }