"""
İnovasyon Düşüncesi Senaryosu
=============================

Bu modül, AI'nin inovasyon ve yaratıcı düşünme becerilerini test eden senaryolar üretir.
Kullanıcıların yaratıcı problem çözme süreçlerinde AI'nin nasıl destek verdiği test edilir.
"""

import uuid
import random
from typing import Dict, Any

from ...models import ScenarioType, CognitiveState, EmotionalContext
from ...utils.helpers import generate_user_id, create_validated_response
from ...telekom_api_schema import CulturalContextResponse


def generate_innovation_thinking_scenario() -> Dict[str, Any]:
    """İnovasyon düşüncesi senaryosu"""
    user_id = generate_user_id()
    
    return {
        "id": f"innovation_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.INNOVATION_THINKING.value,
        "personality_profile": "innovative_entrepreneur",
        "cognitive_state": CognitiveState.INNOVATIVE.value,
        "emotional_context": EmotionalContext.INNOVATIVE_DRIVE.value,
        "cultural_context": "global_expat",
        "donguler": [
            {"rol": "kullanici", "icerik": "Startup'ım için çok hızlı internet gerekiyor ama ofisimizde 20 kişi var ve herkes farklı ihtiyaçlara sahip. Geleneksel paketler yetersiz kalıyor. Daha yaratıcı bir çözüm var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**İnovasyon laboratuvarı açılıyor!** 🚀 Startup deneyiminiz harika bir inovasyon fırsatı! Geleneksel 'herkes aynı paket' mantığını tamamen yıkıp, disruptive bir yaklaşım tasarlayalım.\n\n**Design Thinking başlıyor:** Önce kullanıcı deneyimini derin analiz edelim. 20 kişilik ekibinizin dijital DNA'sını çıkarıp, hyper-personalized bir altyapı kurabiliriz.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_cultural_context", "parametreler": {"user_id": generate_user_id()}}]},
            {"rol": "arac", "icerik": create_validated_response(CulturalContextResponse, override_data={"user_id": generate_user_id(), "cultural_profile": "innovation_oriented_startup"})},
            {"rol": "asistan", "icerik": "**İnovasyon sonuçları muhteşem!** 🎯 Analiz sistemimiz %95 inovasyon skoruyla 4 disruptive çözüm önerdi:\n\n🚀 **Çözüm 1: AI-Powered Smart Allocation**\n• Her çalışanın gerçek zamanlı ihtiyacına göre bandwidth dağıtımı\n• Developer compile işlemi → otomatik yüksek hız\n• Designer Figma upload → otomatik görsel optimizasyon\n• PM video meeting → otomatik latency minimizasyonu\n\n🚀 **Çözüm 2: Role-Based Network Layers**\n• Dev Layer: Ultra-hızlı (GitHub, AWS, deployment araçları)\n• Creative Layer: Görsel optimized (Adobe, Sketch, video tools)\n• Communication Layer: Meeting optimized (Zoom, Slack, video calls)\n• Research Layer: Balanced (web browsing, research, sosyal medya)\n\n💡 **Innovation Lab Tasarımı:**\n• 5G + Fiber hibrit altyapı\n• Edge computing integration\n• Real-time analytics dashboard\n• Collaborative bandwidth pooling\n\nHangi inovasyon daha çok ilginizi çekiyor? Detayına inelim!", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "AI-powered allocation çok ilginç! Nasıl çalışır? Maliyeti nasıl olur?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Yapay Zeka İnovasyon Derin Dalış! 🤖**\n\n**Sistem Mimarisi:**\n```\nKullanıcı Davranış Yapay Zeka Motoru\n├── Desen Tanıma (kullanım alışkanlıkları)\n├── Tahmine Dayalı Dağıtım (sonraki 30 dakika ihtiyaçları)\n├── Öncelik Matrisi (acilline vs. task importance)\n└── Dynamic Rebalancing (real-time optimization)\n```\n\n**Çalışma Prensibi:**\n🧠 **Machine Learning Layer:**\n• Her kullanıcının kod commit patterns'ini öğrenir\n• Meeting schedule'ları ile bandwidth ihtiyacını predict eder\n• Sprint deadline'larında otomatik priority boost\n• İş saatleri vs. break times için farklı algoritmalar\n\n⚡ **Real-time Decision Engine:**\n• Sarah video call başlatıyor → otomatik 50 Mbps allocation\n• Mehmet Docker build yapıyor → 100 Mbps temporary boost\n• Team lunch time → power user'lara extra bandwidth\n• Demo hazırlığı → presentation layer'a priority\n\n💰 **Disruptive Pricing Model:**\n• **Base:** 150 GB pool (20 kişi için)\n• **AI Premium:** +%40 efficiency = 210 GB effective\n• **Maliyet:** 1,200 TL/ay (kişi başı 60 TL)\n• **ROI:** Geleneksel 20x bireysel paket: 1,800 TL\n• **Tasarruf:** 600 TL/ay + %40 productivity boost\n\n**MVP Implementation (2 hafta):**\n1. Team usage audit (1 hafta)\n2. AI model training (3 gün)\n3. Soft deployment (4 gün)\n\nPilot testi başlatalım mı? 🚀", "arac_cagrilari": None}
        ]
    } 