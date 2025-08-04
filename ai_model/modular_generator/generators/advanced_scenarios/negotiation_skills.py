"""
Pazarlık ve Müzakere Becerileri Senaryosu
==========================================

Bu modül, AI'nin pazarlık ve müzakere becerilerini test eden senaryolar üretir.
Kullanıcıların farklı pazarlık stratejileri ve AI'nin bunlara nasıl yanıt verdiği test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import GetCustomerPackageResponse, GetRemainingQuotasResponse


def generate_negotiation_skills_scenario() -> Dict[str, Any]:
    """Pazarlık ve müzakere becerileri senaryosu"""
    user_id = generate_user_id()
    current_fee = round(random.uniform(80, 120), 2)
    desired_fee = round(current_fee * 0.75, 2) # %25 indirim talebi
    
    return {
        "id": f"negotiation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.NEGOTIATION_SKILLS.value,
        "personality_profile": "competitive_sales_professional",
        "cognitive_state": CognitiveState.NEGOTIATIVE.value,
        "emotional_context": EmotionalContext.COMPETITIVE.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": f"3 yıldır müşterinizim ve her ay {current_fee} TL ödüyorum. Rakip firmaların {desired_fee} TL'ye benzer paket verdiğini gördüm. Benim için bir çözüm bulabilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Müzakere yaklaşımı devrede:** Öncelikle 3 yıllık sadakatiniz için çok teşekkür ederim! Değerli bir müşterimiz olarak, sizin için en iyi çözümü bulalım. Mevcut paketinizi ve kullanım alışkanlıklarınızı inceleyerek, hem bütçenize uygun hem de ihtiyaçlarınızı karşılayacak seçenekler sunabilirim.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_customer_package", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerPackageResponse, override_data={"monthly_fee": current_fee})},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, override_data={"usage_percentage": {"internet": 80, "voice": 40, "sms": 20}})},
            {"rol": "asistan", "icerik": "**Win-win çözüm analizi:** Kullanım paternlerinizi incelediğimde çok ilginç bir durum görüyorum! İnternetinizin %80'ini kullanırken, konuşma ve SMS'leriniz oldukça düşük. Bu durumda size üç alternatif sunabilirim:\n\n💡 **Seçenek 1:** 'Akıllı İnternet' paketine geçiş (74.90 TL) - Internet kotanızı korur, konuşma/SMS'i azaltır\n💡 **Seçenek 2:** Mevcut paketinizde sadakat indirimi (%15) - 76.08 TL\n💡 **Seçenek 3:** Hibrit çözüm - 69.90 TL'ye özel paket tasarımı\n\n**Müzakere mantığım:** 3 yıllık sadakatinizi ve kullanım profilinizi değerlendirerek, rakip teklifleri de geçen bir çözüm sunmak istiyorum. Hangi yaklaşım size daha uygun?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "69.90 TL özel paket seçeneği ilgimi çekti. Nasıl bir paket bu?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Özel paket tasarımı:** Müzakere sürecimizde öğrendiğim verilerle sizin için optimize edilmiş bir paket:\n\n📦 **Size Özel 'Pro Gaming/Work' Paketi (69.90 TL):**\n• 80 GB yüksek hızlı internet (kullanımınızdan %7 fazla)\n• 800 dakika konuşma (ihtiyacınızın 2 katı)\n• 300 SMS (yeterli)\n• 5G öncelik (yoğunlukta hız garantisi)\n• Oyun/iş uygulamaları için özel optimizasyon\n\n**Müzakere sonucu:** Bu paket normal 79.90 TL ama sadakat programınız ve doğru iletişiminiz sayesinde 69.90 TL. Ayrıca ilk 3 ay %50 gaming boost hediye!\n\n**Kazan-kazan durumu:** Siz hedef bütçenize ulaştınız, biz de değerli müşterimizi koruduk. Paketi aktif edelim mi?", "arac_cagrilari": None}
        ]
    } 