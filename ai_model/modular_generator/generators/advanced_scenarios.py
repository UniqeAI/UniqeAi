# -*- coding: utf-8 -*-
"""
🚀 GELİŞMİŞ SENARYO ÜRETİCİLERİ
================================

Bu modül, SupremeHumanLevelDatasetGenerator için gelişmiş senaryo üreticilerini içerir.
"""

import uuid
import random
from typing import Dict, Any
from ..models import ScenarioType, CognitiveState, EmotionalContext
from ..utils import generate_user_id, create_validated_response
from telekom_api_schema import (
    GetCustomerPackageResponse, GetRemainingQuotasResponse, CulturalContextResponse,
    GetPastBillsResponse
)

def generate_negotiation_skills_scenario() -> Dict[str, Any]:
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
            {"rol": "arac", "icerik": create_validated_response(GetCustomerPackageResponse, override_data={
                "user_id": user_id,
                "monthly_fee": current_fee
            })},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, override_data={
                "user_id": user_id,
                "internet_remaining_gb": 20.0,
                "voice_remaining_minutes": 300,
                "sms_remaining": 100,
                "period_end": "2024-08-31T23:59:59",
                "usage_percentage": {"internet": 80, "voice": 40, "sms": 20}
            })},
            {"rol": "asistan", "icerik": "**Win-win çözüm analizi:** Kullanım paternlerinizi incelediğimde çok ilginç bir durum görüyorum! İnternetinizin %80'ini kullanırken, konuşma ve SMS'leriniz oldukça düşük. Bu durumda size üç alternatif sunabilirim:\n\n💡 **Seçenek 1:** 'Akıllı İnternet' paketine geçiş (74.90 TL) - Internet kotanızı korur, konuşma/SMS'i azaltır\n💡 **Seçenek 2:** Mevcut paketinizde sadakat indirimi (%15) - 76.08 TL\n💡 **Seçenek 3:** Hibrit çözüm - 69.90 TL'ye özel paket tasarımı\n\n**Müzakere mantığım:** 3 yıllık sadakatinizi ve kullanım profilinizi değerlendirerek, rakip teklifleri de geçen bir çözüm sunmak istiyorum. Hangi yaklaşım size daha uygun?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "69.90 TL özel paket seçeneği ilgimi çekti. Nasıl bir paket bu?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Özel paket tasarımı:** Müzakere sürecimizde öğrendiğim verilerle sizin için optimize edilmiş bir paket:\n\n📦 **Size Özel 'Pro Gaming/Work' Paketi (69.90 TL):**\n• 80 GB yüksek hızlı internet (kullanımınızdan %7 fazla)\n• 800 dakika konuşma (ihtiyacınızın 2 katı)\n• 300 SMS (yeterli)\n• 5G öncelik (yoğunlukta hız garantisi)\n• Oyun/iş uygulamaları için özel optimizasyon\n\n**Müzakere sonucu:** Bu paket normal 79.90 TL ama sadakat programınız ve doğru iletişiminiz sayesinde 69.90 TL. Ayrıca ilk 3 ay %50 gaming boost hediye!\n\n**Kazan-kazan durumu:** Siz hedef bütçenize ulaştınız, biz de değerli müşterimizi koruduk. Paketi aktif edelim mi?", "arac_cagrilari": None}
        ]
    }

def generate_teaching_mentoring_scenario() -> Dict[str, Any]:
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
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, override_data={
                "user_id": user_id,
                "internet_remaining_gb": 12.5,
                "voice_remaining_minutes": 450,
                "sms_remaining": 475,
                "period_end": "2024-08-31T23:59:59",
                "usage_percentage": {"internet": 75, "voice": 10, "sms": 5}
            })},
            {"rol": "asistan", "icerik": "**Öğrenme hikayeniz:** Bakın, şu anda durumunuz çok iyi! Size öğretici bir analiz yapayım:\n\n📚 **Ders 1 - Mevcut Durumunuz:**\n• 50 GB kotanızın 37.5 GB'ını kullanmışsınız (%75)\n• Geriye 12.5 GB kaldı (ayın sonuna 10 gün var)\n• Günde ortalama 1.25 GB kullanabilirsiniz\n\n📚 **Ders 2 - Bu Ne Demek:**\n• WhatsApp mesajları: günde yüzlerce (çok az veri)\n• Fotoğraf göndermek: 1 MB (orta)\n• Video izlemek: saatte 1 GB (en çok veri)\n\n**Öğretici soru:** Video izlemeyi çok kullanıyor musunuz? Youtube, Netflix, Instagram videoları?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Evet, torunlarımın videolarını WhatsApp'ta izliyorum. Bir de akşamları haber izliyorum internetten. Bu çok mu veri harcar?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Öğrenme ilerliyor - mükemmel gözlem!** Şimdi size pratik hayattan örneklerle açıklayayım:\n\n📚 **Ders 3 - Video Tüketimi Analizi:**\n\n👶 **Torun videoları (WhatsApp):**\n• 1 dakikalık video ≈ 10-15 MB\n• Günde 10 video izlerseniz ≈ 150 MB\n• Ayda ≈ 4.5 GB (bu normal ve tatlı!)\n\n📺 **Haber izleme:**\n• 1 saat canlı haber ≈ 1 GB\n• Günde 2 saat ≈ 60 GB/ay (işte asıl tüketim burada!)\n\n**Öğretici çözüm:** Size özel 'Büyükanne/Büyükbaba Stratejisi' önerebilirim:\n\n💡 **Akıllı İzleme Yöntemi:**\n• Haberleri Wi-Fi'da izleyin (evde internetten)\n• Torun videolarını mobil veriyle izleyin (her yerde)\n• Wi-Fi yoksa haber kalitesini 'düşük' yapın (yarı veri harcar)\n\n**Öğrenme sorusu:** Evinizde Wi-Fi internet var mı? Telefonu Wi-Fi'a bağlamayı biliyor musunuz?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Wi-Fi var ama nasıl bağlanacağımı bilmiyorum. Öğretir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Ders 4 - Wi-Fi Bağlantısı (Adım Adım):**\n\nTabii ki öğretirim! En basit yöntemle:\n\n🔧 **Telefonunuzda (Android için):**\n1️⃣ **Ayarlar** uygulamasını açın (dişli simgesi)\n2️⃣ **Wi-Fi** yazısına dokunun (genelde en üstte)\n3️⃣ Wi-Fi'ı **AÇIN** (kapalıysa)\n4️⃣ Evinizin adını bulun (router/modem üzerinde yazıyor)\n5️⃣ Şifreyi girin (yine router üzerinde yazıyor)\n\n📍 **Router/Modem nerede?** Genelde televizyonun yanında, ışıklı küçük kutu\n\n**Öğrenme tüyosu:** Bir kere bağlandıktan sonra telefon hep hatırlar! Bir daha yapmaya gerek yok.\n\n**Ders 5 - Başarı Kontrolü:**\n• Wi-Fi bağlıyken sol üstte Wi-Fi simgesi görünür\n• Artık video izlerken kota harcamazsınız!\n• Torun videolarını istediğiniz kadar izleyebilirsiniz 💕\n\n**Mentorluk sorusu:** Bu adımları deneyip sonucu bana söyler misiniz? Takıldığınız nokta olursa yardım ederim!"}
        ]
    }

def generate_innovation_thinking_scenario() -> Dict[str, Any]:
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
            {"rol": "arac", "icerik": create_validated_response(CulturalContextResponse, override_data={
                "user_id": generate_user_id(),
                "cultural_profile": "innovation_oriented_startup",
                "communication_preferences": {"style": "direct", "formality": "casual"},
                "service_adaptations": ["multilingual", "flexible"],
                "language_preference": "turkish",
                "accessibility_needs": []
            })},
            {"rol": "asistan", "icerik": "**İnovasyon sonuçları muhteşem!** 🎯 Analiz sistemimiz %95 inovasyon skoruyla 4 disruptive çözüm önerdi:\n\n🚀 **Çözüm 1: AI-Powered Smart Allocation**\n• Her çalışanın gerçek zamanlı ihtiyacına göre bandwidth dağıtımı\n• Developer compile işlemi → otomatik yüksek hız\n• Designer Figma upload → otomatik görsel optimizasyon\n• PM video meeting → otomatik latency minimizasyonu\n\n🚀 **Çözüm 2: Role-Based Network Layers**\n• Dev Layer: Ultra-hızlı (GitHub, AWS, deployment araçları)\n• Creative Layer: Görsel optimized (Adobe, Sketch, video tools)\n• Communication Layer: Meeting optimized (Zoom, Slack, video calls)\n• Research Layer: Balanced (web browsing, research, sosyal medya)\n\n💡 **Innovation Lab Tasarımı:**\n• 5G + Fiber hibrit altyapı\n• Edge computing integration\n• Real-time analytics dashboard\n• Collaborative bandwidth pooling\n\nHangi inovasyon daha çok ilginizi çekiyor? Detayına inelim!", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "AI-powered allocation çok ilginç! Nasıl çalışır? Maliyeti nasıl olur?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Yapay Zeka İnovasyon Derin Dalış! 🤖**\n\n**Sistem Mimarisi:**\n```\nKullanıcı Davranış Yapay Zeka Motoru\n├── Desen Tanıma (kullanım alışkanlıkları)\n├── Tahmine Dayalı Dağıtım (sonraki 30 dakika ihtiyaçları)\n├── Öncelik Matrisi (acilline vs. task importance)\n└── Dynamic Rebalancing (real-time optimization)\n```\n\n**Çalışma Prensibi:**\n🧠 **Machine Learning Layer:**\n• Her kullanıcının kod commit patterns'ini öğrenir\n• Meeting schedule'ları ile bandwidth ihtiyacını predict eder\n• Sprint deadline'larında otomatik priority boost\n• İş saatleri vs. break times için farklı algoritmalar\n\n⚡ **Real-time Decision Engine:**\n• Sarah video call başlatıyor → otomatik 50 Mbps allocation\n• Mehmet Docker build yapıyor → 100 Mbps temporary boost\n• Team lunch time → power user'lara extra bandwidth\n• Demo hazırlığı → presentation layer'a priority\n\n💰 **Disruptive Pricing Model:**\n• **Base:** 150 GB pool (20 kişi için)\n• **AI Premium:** +%40 efficiency = 210 GB effective\n• **Maliyet:** 1,200 TL/ay (kişi başı 60 TL)\n• **ROI:** Geleneksel 20x bireysel paket: 1,800 TL\n• **Tasarruf:** 600 TL/ay + %40 productivity boost\n\n**MVP Implementation (2 hafta):**\n1. Team usage audit (1 hafta)\n2. AI model training (3 gün)\n3. Soft deployment (4 gün)\n\nPilot testi başlatalım mı? 🚀", "arac_cagrilari": None}
        ]
    }

def generate_temporal_reasoning_scenario() -> Dict[str, Any]:
    user_id = generate_user_id()
    return {
        "id": f"temporal_scenario_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.TEMPORAL_REASONING.value,
        "personality_profile": "data_driven_analyst",
        "cognitive_state": CognitiveState.PREDICTIVE.value,
        "emotional_context": EmotionalContext.CONTEMPLATIVE.value,
        "cultural_context": "modern_urban_turkish",
        "donguler": [
            {"rol": "kullanici", "icerik": "Son 6 aydır internet kullanımım çok değişken. Bazen hiç kullanmıyorum, bazen aşıyorum. Gelecek için nasıl bir strateji izlemeliyim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Temporal Analytics başlatılıyor! 📊** Çok değerli bir soru sordunuz. Zaman serisi analizleriyle geleceğe dönük optimal strateji geliştirelim. Önce geçmiş davranış patterninizi çıkaralım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": None, "arac_cagrilari": [{"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 12}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse, override_data={
                "user_id": user_id,
                "bills": [
                    {"amount": 89.50}, {"amount": 156.80}, {"amount": 89.50}, 
                    {"amount": 89.50}, {"amount": 134.50}, {"amount": 89.50}
                ]
            })},
            {"rol": "asistan", "icerik": "**Zamansal Örüntü Analizi Tamamlandı! 🔍**\n\n**Zaman Serisi Analiziniz:**\n```\n📈 6 Aylık Kullanım Trendi:\nEkim   Kasım   Aralık  Ocak    Şubat   Mart\n89.50→ 156.80→ 89.50→ 89.50→ 134.50→ 89.50\n Base   +75%    Base   Base   +50%    Base\n```\n\n**Zamansal Örüntüler Tespit Edildi:**\n🕒 **Mevsimsellik:** Kasım (%75↑) ve Şubat (%50↑) artışları\n🕒 **Döngüsel Davranış:** 2 aylık düzenli aralıklarla aşım\n🕒 **Baseline Stability:** Normal aylarda 89.50 TL consistent\n\n**Predictive Analysis:**\n• **Nisan 2024:** %85 olasılıkla normal (89.50 TL)\n• **Mayıs 2024:** %70 olasılıkla aşım (130-160 TL range)\n• **Temporal Driver:** İş yoğunluğu/proje dönemleri?\n\n**Smart Temporal Strategy Önerim:**\n\n🎯 **Adaptif Paket Modeli:**\n• Base: 50 GB (normal aylar)\n• Auto-scale: Spike öncesi otomatik 100 GB upgrade\n• Cost averaging: 12 aylık sabit ödeme (108 TL/ay)\n\n**Temporal Learning Question:** Kasım ve Şubat aylarındaki yoğun kullanımınızın sebebi neydi? İş projesi mi, ev içi değişiklik mi?", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Doğru tahmin! Kasım'da yeni iş başladım, remote çalışmaya başladım. Şubat'ta da evden eğitim videoları izledim. Bu pattern devam ederse nasıl optimize ederim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Temporal Causality Confirmed! 🎯** Muhteşem insight! Remote work ve self-education pattern'i klassik bir profesyonel growth trajectory. Geleceğe dönük optimization stratejisi:\n\n**Future Timeline Projection:**\n```\n2024 Career Development Timeline:\nQ1: Remote work adaptation ✅\nQ2: Skill building phase (tahmin: video consumption ↑)\nQ3: Project delivery season (tahmin: collaboration tools ↑)\nQ4: Performance review + new skills (tahmin: mixed usage)\n```\n\n**Temporal Optimization Strategy:**\n\n📅 **Proactive Calendar-Sync Model:**\n• **Learning Seasons** (Q2, Q4): Auto 100 GB\n• **Delivery Seasons** (Q3): Upload optimized 75 GB + priority\n• **Maintenance Seasons** (Q1): Standard 50 GB\n\n⚡ **Dynamic Adaptation Rules:**\n```python\nIF (month == \"learning_intensive\"):\n    upgrade_to_unlimited_education_package()\nIF (work_from_home_days > 15):\n    enable_professional_tier()\nIF (video_conference_hours > 50):\n    activate_collaboration_boost()\n```\n\n🎯 **ROI-Optimized Pricing:**\n• **Standart:** 89.50 TL (3-4 ay/yıl)\n• **Boost:** 119.90 TL (2-3 ay/yıl when needed)\n• **Annual Average:** ~105 TL/ay (mevcut spike'lı modelden %8 tasarruf)\n\n**Temporal Learning Integration:**\n• Pattern recognition her ay güçlenir\n• Otomatik upgrade önerileri\n• Career milestone'larla sync\n\n**Next-Level Question:** Önümüzdeki 3 ayda hangi professional development planlarınız var? Böylece temporal model'i fine-tune edebiliriz.", "arac_cagrilari": None}
        ]
    }

def generate_cross_cultural_communication_scenario() -> Dict[str, Any]:
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
            {"rol": "arac", "icerik": create_validated_response(CulturalContextResponse, override_data={
                "user_id": user_id,
                "cultural_profile": "international_researcher",
                "communication_preferences": {"style": "formal", "formality": "professional"},
                "service_adaptations": ["multilingual", "international"],
                "language_preference": "english",
                "accessibility_needs": []
            })},
            {"rol": "asistan", "icerik": "**Kültürlerarası Profil Analizi Tamamlandı! 🤝**\n\n**Uygulanan Kültürel Zeka:**\nProfiliniz harika kültürel köprü kurma eğilimleri gösteriyor. Türkçede biz 'misafirperverlik' deriz. Siz sadece bir müşteri değilsiniz, Türkiye'nin bilgi ekosistemine katkıda bulunan akademik misafirimizsiniz.\n\n**Küresel Düzeyde Optimize Edilmiş Çözüm:**\n\n🌍 **'Akademik Küresel Köprü' Paketi:**\n• **Araştırma Önceliği:** Sınırsız akademik veritabanları/VPN erişimi\n• **Aile Bağlantısı:** 500 uluslararası dakika (tüm ülkeler)\n• **Kültürel Entegrasyon:** Yerel arkadaşlıklar için sınırsız WhatsApp\n• **Zaman Dilimi Dostu:** 7/24 İngilizce destek\n\n📞 **Aile Arama Stratejisi:**\n• **WhatsApp Aramaları:** Wi-Fi üzerinden ücretsiz (günlük aramalar için önerilir)\n• **Geleneksel Aramalar:** Yaşlı aile üyeleri için yedek\n• **Görüntülü Aramalar:** Aile toplantıları için yüksek kalite\n\n🎓 **Akademik Araştırma Optimizasyonu:**\n• Araştırma saatleri için öncelikli bant genişliği (9:00 - 23:00)\n• Konferans araması kalite garantisi\n• Uluslararası işbirlikleri için bulut depolama entegrasyonu\n\n**Kültürel İpucu:** Türk aileleri de sık sık her gün arar! İletişim tarzınız burada çok doğal karşılanacaktır.\n\nFaturalandırmayı her iki para biriminde de açıklamamı ister misiniz? Ve ailenizin üyeleri hangi ülkelerde yaşıyor? Bu bilgi ile daha fazla optimize edebilirim.", "arac_cagrilari": None},
            {"rol": "kullanici", "icerik": "Bu çok düşünceli! Ailem Almanya, Kanada ve Japonya'da. Ayrıca çeşitli Avrupa ülkelerinde meslektaşlarım var. Akademik araştırma önceliği kulağa harika geliyor.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "**Küresel Akademik Ağ Tespit Edildi! 🎓🌍**\n\n**Çok Kıt'alı Aile Analizi:**\n\n🇩🇪 **Almanya Bağlantısı:**\n• Zaman Farkı: 2 saatlik fark - kolay arama\n• Türk-Alman teknolojisi: AB roaming avantajları\n• WhatsApp hakimiyeti: Günlük kontroller için mükemmel\n\n🇨🇦 **Kanada Bağlantısı:**\n• Zaman Zorluğu: 8 saatlik fark - stratejik zamanlama gerekli\n• Görüntülü arama optimizasyonu: Türkiye'de akşam = Kanada'da öğleden sonra\n• Ses kalitesi önceliği: Aile sohbetleri netlik gerektirir\n\n🇯🇵 **Japonya Bağlantısı:**\n• Karmaşık zaman dilimi: 6 saat ileride - sabah erken/akşam geç aramalar\n• Kültürel paralellik: Japonya da aile saygısı ve hiyerarşisine değer verir\n• Teknoloji uyumu: Japonya'nın yüksek teknoloji yaklaşımı 5G'mizle eşleşiyor\n\n**Akademik Avrupa Ağı:**\n• Konferans aramaları: Çok ülkeli, yüksek kalite gereksinimleri\n• Araştırma işbirliği: Büyük dosya transferleri\n• Yayın son tarihleri: Teslim dönemlerinde öncelikli bant genişliği\n\n**Kültürlerarası Optimizasyon Planı:**\n\n📅 **Zaman Dilimine Akıllı Zamanlama:**\n• Sabah aramaları (8-10): Japonya aile zamanı\n• Öğleden sonra çalışma (14-18): Avrupalı meslektaşlar\n• Akşam aramaları (19-21): Almanya & Kanada ailesi\n\n💡 **Kültürel Uyum Özellikleri:**\n• 'Sabbath Modu': Hafta sonu aile zamanı için indirimli ücretler\n• 'Akademik Yoğunluk': Uluslararası konferans sezonlarında öncelik\n• 'Ramazan Özel': Kültürel dönemlerde ayarlanmış arama düzenleri\n\n**Aylık Yatırım:** 145 TL (~15 USD)\n**Değer Getirisi:** Sınırsız aile sevgisi + akademik verimlilik = Paha biçilmez! 💝\n\nBu, üç kıt'ayı Türk misafirperverliği köprüsüyle birleştiren kişisel 'Küresel Köy'ünüzü yaratır. Bu kültürlerarası iletişim şaheserini aktive edelim mi?", "arac_cagrilari": None}
        ]
    } 