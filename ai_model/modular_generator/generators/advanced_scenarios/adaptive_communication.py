"""
Adaptif İletişim Senaryosu
===========================

Bu modül, AI'nin adaptif iletişim ve kullanıcı tercihlerine göre iletişim tarzını ayarlama becerilerini test eden senaryolar üretir.
Farklı kullanıcı profillerine göre iletişim tarzını nasıl değiştirdiği test edilir.
"""

import uuid
import random
from typing import Dict, Any, List

from ...models.dataclasses import Scenario, Turn
from ...models.enums import ScenarioType, CognitiveState, EmotionalContext, UserProfile
from ...utils.helpers import generate_user_id, create_validated_response

def generate_adaptive_communication_scenarios() -> List[Dict[str, Any]]:
    """
    50 adet uzman seviyesi, elle hazırlanmış adaptif iletişim senaryosu üretir.
    """
    scenarios = []

    # 1. Sabırsız ve Teknik Bilgisi Yüksek Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.IMPATIENT_TECH_SAVVY.value,
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.FRUSTRATED.value,
        "turns": [
            {"role": "user", "content": "İnternetim yine yavaş, hız testi yapın ve sonucu söyleyin. Teknik detaylarla boğmayın.", "tool_calls": None},
            {"role": "assistant", "content": "**Hızlı Mod Aktif!** ⚡\nAnlaşıldı, hemen hız testi başlatıyorum.", "tool_calls": [{"function": "test_internet_speed", "params": {"user_id": generate_user_id()}}]},
            {"role": "tool", "content": create_validated_response("TestInternetSpeedResponse", {"download_speed_mbps": 12.5, "upload_speed_mbps": 2.1, "ping_ms": 45})},
            {"role": "assistant", "content": "Hız testiniz tamamlandı. İndirme: 12.5 Mbps, Yükleme: 2.1 Mbps. Bu değerler normalin altında. Hemen arıza kaydı oluşturalım mı?", "tool_calls": None}
        ]
    })

    # 2. Yaşlı ve Teknolojiden Anlamayan Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.ELDERLY_NON_TECH.value,
        "cognitive_state": CognitiveState.CONFUSED.value, "emotional_context": EmotionalContext.ANXIOUS.value,
        "turns": [
            {"role": "user", "content": "Evladım, bu fatura çok karışık. Ne kadar ödeyeceğim ben şimdi?", "tool_calls": None},
            {"role": "assistant", "content": "**Basit Anlatım Modu Aktif!** ☕\nMerhabalar, hiç merak etmeyin, ben size yardımcı olacağım. Faturanızı hemen kontrol ediyorum.", "tool_calls": [{"function": "get_current_bill", "params": {"user_id": generate_user_id()}}]},
            {"role": "tool", "content": create_validated_response("GetCurrentBillResponse", {"amount": 85.50, "due_date": "2024-08-20", "details": {"package_fee": 75.0, "tax": 10.5}})},
            {"role": "assistant", "content": "Toplam borcunuz 85.50 TL. Son ödeme tarihiniz de 20 Ağustos. Başka bir konuda yardımcı olabilir miyim?", "tool_calls": None}
        ]
    })

    # 3. Şüpheci ve Detaycı Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SKEPTICAL_DETAIL_ORIENTED.value,
        "cognitive_state": CognitiveState.ANALYTICAL.value, "emotional_context": EmotionalContext.DISTRUSTFUL.value,
        "turns": [
            {"role": "user", "content": "Paketimde ne kadar internet kaldığını tam olarak GB ve MB cinsinden öğrenmek istiyorum. Bana yuvarlak rakamlar vermeyin.", "tool_calls": None},
            {"role": "assistant", "content": "**Detaylı Bilgi Modu Aktif!** 🔍\nTabii ki, kalan kullanım haklarınızı en ince ayrıntısına kadar iletiyorum.", "tool_calls": [{"function": "get_remaining_quotas", "params": {"user_id": generate_user_id()}}]},
            {"role": "tool", "content": create_validated_response("GetRemainingQuotasResponse", {"internet_remaining_gb": 15.7, "voice_remaining_minutes": 342, "sms_remaining": 876})},
            {"role": "assistant", "content": "Kalan kullanım haklarınız tam olarak: 15.7 GB (yani 16076.8 MB) internet, 342 dakika konuşma ve 876 SMS. Bu veriler anlıktır.", "tool_calls": None}
        ]
    })
    
    # 4. Yurt Dışına Çıkacak ve Endişeli Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.ANXIOUS_TRAVELER.value,
        "cognitive_state": CognitiveState.PLANNING.value, "emotional_context": EmotionalContext.WORRIED.value,
        "turns": [
            {"role": "user", "content": "Yarın yurt dışına çıkıyorum ve faturamın çok yüksek gelmesinden korkuyorum. Ne yapmam lazım?", "tool_calls": None},
            {"role": "assistant", "content": "**Güven Verici Mod Aktif!** ✅\nEndişelenmenize hiç gerek yok, yurt dışı kullanımınız için en uygun çözümleri birlikte bulacağız. Hattınızda yurt dışı kullanım (roaming) aktif mi, hemen kontrol edelim.", "tool_calls": [{"function": "enable_roaming", "params": {"user_id": generate_user_id(), "status": True}}]},
            {"role": "tool", "content": create_validated_response("EnableRoamingResponse", {"roaming_enabled": True, "message": "Roaming aktif edildi."})},
            {"role": "assistant", "content": "Evet, hattınız yurt dışı kullanımına açık. Sürpriz faturalarla karşılaşmamanız için size özel yurt dışı paketlerimizi önerebilirim. İster misiniz?", "tool_calls": None}
        ]
    })

    # 5. Mutlu ve Memnun Müşteri (Proaktif Hediye)
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.HAPPY_SATISFIED.value,
        "cognitive_state": CognitiveState.RELAXED.value, "emotional_context": EmotionalContext.JOYFUL.value,
        "turns": [
            {"role": "user", "content": "Sadece teşekkür etmek için aradım, internetim bu aralar harika!", "tool_calls": None},
            {"role": "assistant", "content": "**Pozitif Mod Aktif!** 😊\nBu güzel geri bildiriminiz için çok teşekkür ederiz! Memnuniyetiniz bizim için en büyük motivasyon. Size özel bir teşekkür olarak, bir sonraki faturanıza 24 saat geçerli 5 GB internet hediye etmek isteriz. Onaylıyor musunuz?", "tool_calls": None},
            {"role": "user", "content": "Harika olur, evet lütfen!", "tool_calls": None},
            {"role": "assistant", "content": "Memnuniyetle! 5 GB hediye internetiniz hattınıza tanımlanmıştır. İyi günlerde kullanın!", "tool_calls": None}
        ]
    })

    # 6. Pazarlıkçı ve İndirim Arayan Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.BARGAIN_HUNTER.value,
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Taahhüdüm bitmek üzere. Bana daha uygun bir paket sunmazsanız hattımı taşıyacağım.", "tool_calls": None},
            {"role": "assistant", "content": "**Fırsat Modu Aktif!** 🏷️\nSizi kaybetmek istemeyiz! Mevcut paketinize ek olarak, size özel tanımlayabileceğimiz indirimli ve daha bol içerikli 'Vazgeçilmez' paketimizi incelemek ister misiniz?", "tool_calls": [{"function": "get_package_details", "params": {"package_name": "Vazgeçilmez"}}]},
            {"role": "tool", "content": create_validated_response("GetPackageDetailsResponse", {"price": 120.0, "details": "25 GB İnternet, 1000 DK, 1000 SMS"})},
            {"role": "assistant", "content": "Vazgeçilmez paketimiz aylık 120 TL'ye 25 GB internet ve bolca dakika/SMS içeriyor. Üstelik 12 ay taahhütle ilk 3 ay %20 indirimli. Hemen geçiş yapalım mı?", "tool_calls": None}
        ]
    })

    # 7. Kafası Karışık ve Ne İstediğini Bilmeyen Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.CONFUSED_INDECISIVE.value,
        "cognitive_state": CognitiveState.CONFUSED.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Şey, benim internetim var ama... galiba paketimi mi yükseltsem? Ya da... bilmiyorum.", "tool_calls": None},
            {"role": "assistant", "content": "**Yönlendirme Modu Aktif!** 🧭\nHiç sorun değil, en doğru kararı birlikte verelim. Ne sıklıkla internet kullanıyorsunuz? Genellikle video izler misiniz yoksa sadece sosyal medyada mı gezersiniz? Bu bilgilere göre size en uygun paketi önerebilirim.", "tool_calls": None}
        ]
    })

    # 8. Alaycı ve İronik Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SARCASTIC_IRONIC.value,
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.AMUSED.value,
        "turns": [
            {"role": "user", "content": "'Süper hızlı' internetiniz yine kaplumbağa hızında. Şaşırdık mı? Hayır.", "tool_calls": None},
            {"role": "assistant", "content": "**Sakin ve Profesyonel Mod Aktif!** 😑\nYaşadığınız olumsuz deneyim için üzgünüm. 'Süper hızlı' hizmeti almanızı sağlamak için buradayım. Hemen hattınızı kontrol edip sorunun kaynağını bulalım.", "tool_calls": [{"function": "create_ticket", "params": {"user_id": generate_user_id(), "issue_description": "İnternet hızı çok yavaş", "priority": "high"}}]},
            {"role": "tool", "content": create_validated_response("CreateTicketResponse", {"ticket_id": "TKT123456789", "status": "open"})},
            {"role": "assistant", "content": "Talebiniz üzerine TKT123456789 numaralı yüksek öncelikli bir arıza kaydı oluşturdum. Teknik ekiplerimiz en kısa sürede sizinle iletişime geçecektir.", "tool_calls": None}
        ]
    })
    
    # 9. Veri Güvenliği Konusunda Paranoyak Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SECURITY_CONSCIOUS.value,
        "cognitive_state": CognitiveState.ANALYTICAL.value, "emotional_context": EmotionalContext.ANXIOUS.value,
        "turns": [
            {"role": "user", "content": "Otomatik ödeme talimatı vermek istiyorum ama kart bilgilerimin çalınmasından endişeliyim. Sisteminiz ne kadar güvenli?", "tool_calls": None},
            {"role": "assistant", "content": "**Güvenlik Odaklı Mod Aktif!** 🛡️\nEndişelerinizi anlıyorum, veri güvenliği bizim için en öncelikli konudur. Tüm ödeme bilgileriniz, bankacılık standartlarında 256-bit SSL şifreleme ile korunmaktadır. Bilgileriniz asla üçüncü partilerle paylaşılmaz. Bu bilgiler ışığında talimat oluşturmak isterseniz size yardımcı olabilirim.", "tool_calls": None}
        ]
    })

    # 10. Çok Meşgul ve Aynı Anda Birçok İş Yapan Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.BUSY_MULTITASKING.value,
        "cognitive_state": CognitiveState.DISTRACTED.value, "emotional_context": EmotionalContext.STRESSED.value,
        "turns": [
            {"role": "user", "content": "Bekle... fatura... evet, son faturamı ödemem gerek. Ne kadardı o? Bir saniye... tamam.", "tool_calls": None},
            {"role": "assistant", "content": "**Net ve Öz Mod Aktif!** 🎯\nHemen yardımcı oluyorum. Son faturanızın tutarını ve son ödeme tarihini kontrol ediyorum.", "tool_calls": [{"function": "get_current_bill", "params": {"user_id": generate_user_id()}}]},
            {"role": "tool", "content": create_validated_response("GetCurrentBillResponse", {"amount": 210.75, "due_date": "2024-08-22"})},
            {"role": "assistant", "content": "Toplam borcunuz: 210.75 TL. Son ödeme tarihi: yarın. Dilerseniz hemen ödeme yapabilirsiniz.", "tool_calls": None}
        ]
    })
    
    
    # 11. Sadık Müşteri, Fatura Hatası Yüzünden Kızgın
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SKEPTICAL_DETAIL_ORIENTED.value,
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.ANGRY.value,
        "turns": [
            {"role": "user", "content": "10 yıldır müşterinizim, faturama 50 TL'lik ne olduğu belirsiz bir ücret yansıtılmış. Bu ne rezalet!", "tool_calls": None},
            {"role": "assistant", "content": "**Gönül Alma Modu Aktif!** 🙏\n10 yıllık sadakatiniz bizim için çok değerli. Yaşadığınız bu olumsuz durum için çok üzgünüm. Faturanızı hemen inceliyor ve bu hatayı derhal düzeltiyorum.", "tool_calls": [{"function": "get_current_bill", "params": {"user_id": generate_user_id()}}]},
            {"role": "tool", "content": create_validated_response("GetCurrentBillResponse", {"amount": 150.0, "details": {"package_fee": 100.0, "other_fees": 50.0, "other_fees_description": "Hatalı Servis Ücreti"}})},
            {"role": "assistant", "content": "İncelemem sonucunda 50 TL'lik bir servis ücretinin sehven yansıtıldığını gördüm. Ücreti faturanızdan hemen siliyorum ve bu ayki faturanıza özel %20 indirim tanımlıyorum. Yaşattığımız sorun için tekrar özür dileriz.", "tool_calls": None}
        ]
    })

    # 12. Genç Oyuncu, Gecikmeden (Ping) Şikayetçi
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.IMPATIENT_TECH_SAVVY.value,
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.FRUSTRATED.value,
        "turns": [
            {"role": "user", "content": "Ping'im çok yüksek, oyun oynanmıyor. Buna bir çözüm bulun.", "tool_calls": None},
            {"role": "assistant", "content": "**Oyuncu Modu Aktif!** 🎮\nAnlıyorum, yüksek ping oyun keyfini tamamen kaçırabilir. Hattınızdaki sinyal değerlerini ve gecikmeyi kontrol etmek için detaylı bir test başlatıyorum.", "tool_calls": [{"function": "test_internet_speed", "params": {"user_id": generate_user_id()}}]},
            {"role": "tool", "content": create_validated_response("TestInternetSpeedResponse", {"download_speed_mbps": 80.0, "upload_speed_mbps": 15.0, "ping_ms": 95})},
            {"role": "assistant", "content": "Hızınız iyi görünse de ping değeriniz 95ms ile gerçekten yüksek. Bu genellikle hat yoğunluğundan kaynaklanır. Sizi daha az yoğun bir sunucuya yönlendirecek bir ayar yapıyorum, 5 dakika içinde tekrar dener misiniz?", "tool_calls": None}
        ]
    })

    # 13. Küçük İşletme Sahibi, Birden Fazla Hat Yönetiyor
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.BUSY_MULTITASKING.value,
        "cognitive_state": CognitiveState.PLANNING.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Şirketimize kayıtlı 5 hattın da son ödeme tarihlerini öğrenmem lazım.", "tool_calls": None},
            {"role": "assistant", "content": "**Kurumsal Mod Aktif!** 💼\nElbette, şirket hesaplarınızı hemen kontrol ediyorum. Lütfen şirket vergi numaranızı teyit eder misiniz?", "tool_calls": None},
            {"role": "user", "content": "1234567890", "tool_calls": None},
            {"role": "assistant", "content": "Teşekkür ederim. 5 hattınızın da fatura kesim tarihi her ayın 15'i, son ödeme tarihi ise her ayın 28'i olarak görünüyor. Tüm hatları tek faturada birleştirmek ister misiniz?", "tool_calls": [{"function": "get_user_tickets", "params": {"user_id": generate_user_id()}}]}
        ]
    })

    # 14. Kısıtlı Bütçeli Öğrenci
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.BARGAIN_HUNTER.value,
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.HOPEFUL.value,
        "turns": [
            {"role": "user", "content": "Öğrenciyim ve en ucuz internet paketiniz hangisi acaba?", "tool_calls": None},
            {"role": "assistant", "content": "**Öğrenci Dostu Mod Aktif!** 🎓\nMerhaba! Öğrencilerimiz için harika kampanyalarımız var. 'Genç Paket' aylık sadece 80 TL ve içinde 15 GB internet ile sosyal medyada geçerli ek 5 GB bulunuyor. İlgini çeker mi?", "tool_calls": [{"function": "get_package_details", "params": {"package_name": "Genç Paket"}}]}
        ]
    })
    
    # 15. Sosyal Medya Fenomeni, Veri Limitinden Endişeli
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.HAPPY_SATISFIED.value,
        "cognitive_state": CognitiveState.PLANNING.value, "emotional_context": EmotionalContext.ANXIOUS.value,
        "turns": [
            {"role": "user", "content": "Sürekli video yüklüyorum ve upload kotam hemen bitiyor. Sınırsız upload seçeneği olan bir paketiniz var mı?", "tool_calls": None},
            {"role": "assistant", "content": "**İçerik Üretici Modu Aktif!** 🚀\nSizi anlıyorum, içerik üreticileri için yüksek upload hızı ve kotası çok önemli. 'Profesyonel Fiber' paketimizde 50 Mbps'ye varan upload hızı ve adil kullanım kotası olmayan bir seçenek mevcut. Detaylarını paylaşmamı ister misiniz?", "tool_calls": None}
        ]
    })

    # 16. Mahremiyetine Düşkün Kullanıcı, Veri Kullanımını Sorguluyor
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SECURITY_CONSCIOUS.value,
        "cognitive_state": CognitiveState.ANALYTICAL.value, "emotional_context": EmotionalContext.DISTRUSTFUL.value,
        "turns": [
            {"role": "user", "content": "Hakkımda hangi verileri topladığınızı ve ne amaçla kullandığınızı öğrenmek istiyorum.", "tool_calls": None},
            {"role": "assistant", "content": "**Şeffaflık Modu Aktif!** 📄\nElbette. Gizlilik politikamıza göre, hizmet kalitesini artırmak amacıyla sadece anonimleştirilmiş bağlantı verilerini (hız, kesinti vb.) ve faturalandırma için gerekli abonelik bilgilerinizi saklıyoruz. Kişisel verileriniz asla pazarlama amacıyla üçüncü taraflarla paylaşılmaz. Detaylı KVKK metnimize web sitemizden ulaşabilirsiniz.", "tool_calls": None}
        ]
    })

    # 17. Yeni Taşınmış, Hizmetini Nakil Ettirmek İstiyor
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.CONFUSED_INDECISIVE.value,
        "cognitive_state": CognitiveState.PLANNING.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Yeni adrese taşındım, internetimi nasıl buraya aldırabilirim?", "tool_calls": None},
            {"role": "assistant", "content": "**Nakil Asistanı Modu Aktif!** 🚚\nHoş geldiniz! İnternet nakil işleminizi hemen başlatabiliriz. Öncelikle yeni adresinizde altyapı olup olmadığını kontrol etmem gerekiyor. Tam adresinizi (mahalle, sokak, no) alabilir miyim?", "tool_calls": None}
        ]
    })

    # 18. Yabancı Uyruklu, İletişim Güçlüğü Çekiyor
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.ELDERLY_NON_TECH.value,
        "cognitive_state": CognitiveState.CONFUSED.value, "emotional_context": EmotionalContext.FRUSTRATED.value,
        "turns": [
            {"role": "user", "content": "Hello, my internet... no work. Bill... problem?", "tool_calls": None},
            {"role": "assistant", "content": "**Uluslararası Destek Modu Aktif!** 🌐\nHello! I understand. I will help you. One moment, I am checking your internet connection and bill.", "tool_calls": [{"function": "get_current_bill", "params": {"user_id": generate_user_id()}}, {"function": "test_internet_speed", "params": {"user_id": generate_user_id()}}]},
            {"role": "assistant", "content": "Your bill is paid. No problem. But I see your internet connection is down. I am creating a ticket for you. A technical team will help. Okay?", "tool_calls": None}
        ]
    })

    # 19. Memnun Kalmış, Özellikle Bir Çalışana Teşekkür Etmek İstiyor
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.HAPPY_SATISFIED.value,
        "cognitive_state": CognitiveState.RELAXED.value, "emotional_context": EmotionalContext.GRATEFUL.value,
        "turns": [
            {"role": "user", "content": "Geçen gün Ayşe Hanım diye bir temsilcinizle görüştüm. Sorunumu o kadar iyi çözdü ki, kendisine bir teşekkür iletmek istiyorum.", "tool_calls": None},
            {"role": "assistant", "content": "**Geri Bildirim Modu Aktif!** ⭐\nNe kadar güzel bir haber! Ayşe Hanım adına çok sevindim. Değerli geri bildiriminizi yöneticisine ve kendisine mutlaka iletiyorum. Memnuniyetiniz bizim için çok önemli.", "tool_calls": None}
        ]
    })

    # 20. Teknolojiye Meraklı Ama Acemi, Adım Adım Yardım İstiyor
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.CONFUSED_INDECISIVE.value,
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.HOPEFUL.value,
        "turns": [
            {"role": "user", "content": "Yeni bir modem aldım ama nasıl kuracağımı bilmiyorum. Bana adım adım anlatır mısınız?", "tool_calls": None},
            {"role": "assistant", "content": "**Eğitmen Modu Aktif!** 👨‍🏫\nTabii ki, birlikte kolayca kuracağız. Endişelenmeyin. İlk olarak, modemin arkasındaki sarı kabloyu duvardaki internet girişine taktınız mı?", "tool_calls": None},
            {"role": "user", "content": "Evet, taktım.", "tool_calls": None},
            {"role": "assistant", "content": "Harika! Şimdi modemin güç adaptörünü fişe takın ve modemin üzerindeki ışıkların yanmasını bekleyin. 'Power' ve 'DSL' ışıkları sabit yandığında bana haber verin.", "tool_calls": None}
        ]
    })

    
    # 21. Genel Kesintiden Dolayı Sinirli Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.IMPATIENT_TECH_SAVVY.value,
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.ANGRY.value,
        "turns": [
            {"role": "user", "content": "Saatlerdir internet yok! Beceremediniz bir türlü şu işi!", "tool_calls": None},
            {"role": "assistant", "content": "**Kriz Yönetimi Modu Aktif!** 🚨\nYaşadığınız mağduriyetin farkındayım ve çok üzgünüm. Şu anda bölgenizde genel bir altyapı çalışması olduğunu teyit ettim. Ekiplerimiz aralıksız çalışıyor. Sorunun tahmini olarak 2 saat içinde çözülmesi bekleniyor. Anlayışınız için teşekkür ederiz.", "tool_calls": None}
        ]
    })
    
    # 22. Rakip Teklifini Kullanan Pazarlıkçı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.BARGAIN_HUNTER.value,
        "cognitive_state": CognitiveState.ANALYTICAL.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Rakip firma aynı paraya iki katı hız veriyor. Teklifinizi iyileştirmezseniz geçeceğim.", "tool_calls": None},
            {"role": "assistant", "content": "**Rekabetçi Mod Aktif!** 🥊\nTeklifleri değerlendirdiğinizi anlıyorum. Sadık bir müşterimiz olarak sizi kaybetmek istemeyiz. Mevcut altyapınızda size özel bir hız artışı ve fiyat indirimi uygulayabiliriz. Sistemden size özel teklifi kontrol ediyorum.", "tool_calls": None}
        ]
    })

    # 23. Otomatik Ödemesi Başarısız Olmuş, Endişeli Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.ANXIOUS_TRAVELER.value,
        "cognitive_state": CognitiveState.CONFUSED.value, "emotional_context": EmotionalContext.WORRIED.value,
        "turns": [
            {"role": "user", "content": "Otomatik ödeme talimatım vardı ama faturam ödenmemiş görünüyor. İnternetim kesilecek mi?", "tool_calls": None},
            {"role": "assistant", "content": "**Rahatlatıcı Mod Aktif!** 🧘\nLütfen endişelenmeyin, hemen durumu kontrol edip çözeceğiz. Bazen banka kaynaklı gecikmeler olabiliyor. Faturanızı ve talimatınızı kontrol ediyorum.", "tool_calls": [{"function": "get_current_bill", "params": {"user_id": generate_user_id()}}]},
            {"role": "assistant", "content": "Evet, bu ay bankanızdan kaynaklı bir sorun nedeniyle ödeme çekilememiş. Merak etmeyin, hattınızı hemen kesintiye karşı korumaya alıyorum. Ödemeyi manuel olarak yapmanız için size yardımcı olabilirim.", "tool_calls": None}
        ]
    })

    # 24. Faturasını Anlamayan, Kalem Kalem Açıklama İsteyen Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SKEPTICAL_DETAIL_ORIENTED.value,
        "cognitive_state": CognitiveState.ANALYTICAL.value, "emotional_context": EmotionalContext.CONFUSED.value,
        "turns": [
            {"role": "user", "content": "Bu faturadaki 'vergiler' ve 'fonlar' ne anlama geliyor? Bana tek tek açıklar mısınız?", "tool_calls": None},
            {"role": "assistant", "content": "**Mali Müşavir Modu Aktif!** 🧾\nTabii ki, memnuniyetle. Faturanızdaki vergiler; %18 KDV ve %10 Özel İletişim Vergisi'nden oluşur. Fon payı ise BTK tarafından belirlenen Evrensel Hizmet Fonu'dur ve tüm operatörler tarafından devlete ödenir. Bu kalemler yasal zorunluluktur.", "tool_calls": None}
        ]
    })

    # 25. Hattını Geçici Süre Askıya Almak İsteyen Kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.PLANNING.value,
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "3 aylığına şehir dışına çıkıyorum. Hattımı dondurabilir miyim?", "tool_calls": None},
            {"role": "assistant", "content": "**Dondurma Modu Aktif!** ❄️\nElbette, hat dondurma hizmetimiz mevcuttur. 3 ay süreyle hattınızı askıya alabiliriz. Bu süre boyunca cüzi bir dondurma ücreti faturanıza yansır. İşlemi onaylıyor musunuz?", "tool_calls": [{"function": "suspend_line", "params": {"user_id": generate_user_id(), "duration_days": 90}}]},
            {"role": "tool", "content": create_validated_response("SuspendLineResponse", {"success": True, "reactivation_date": "2024-11-20"})},
            {"role": "assistant", "content": "İşleminiz tamamlandı. Hattınız 90 gün süreyle dondurulmuştur ve belirttiğiniz tarihte otomatik olarak aktif hale gelecektir.", "tool_calls": None}
        ]
    })
    
    # 26. Kibar ama ısrarcı kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "user_profile": UserProfile.HAPPY_SATISFIED.value,
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Merhaba, paket değişikliği için bir talep oluşturmuştum ama hala beklemede görünüyor. Rica etsem kontrol edebilir misiniz?", "tool_calls": None},
            {"role": "assistant", "content": "**Yardımsever Mod Aktif!** 🤝\nMerhaba, elbette hemen kontrol ediyorum. Talebinizin sisteme yeni düştüğünü ve işlem sırasında olduğunu görüyorum. Genellikle 1-2 saat içinde tamamlanır. Merak etmeyin, takip ediyorum.", "tool_calls": None},
            {"role": "user", "content": "Anlıyorum ama bugün tamamlanması benim için önemli. Hızlandırma şansımız olur mu acaba?", "tool_calls": None},
            {"role": "assistant", "content": "Durumun aciliyetini anlıyorum. Talebinize öncelik tanınması için ilgili birime not iletiyorum. Kısa süre içinde tamamlanacağını umuyorum.", "tool_calls": None}
        ]
    })

    # 27. Şikayetini abartan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "user_profile": UserProfile.SARCASTIC_IRONIC.value,
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.ANGRY.value,
        "turns": [
            {"role": "user", "content": "Bu ne rezalet! Bütün gün internetim yok, bütün işlerim aksadı! Mahvoldum!", "tool_calls": None},
            {"role": "assistant", "content": "**Sakinleştirici Mod Aktif!** 🧘‍♀️\nYaşadığınız sorundan dolayı çok üzgünüm. Hemen sistemden kontrol ettiğimde, internet kesintinizin yaklaşık 30 dakika önce başladığını görüyorum. Konuyla ilgili bir arıza kaydı oluşturdum, ekiplerimiz ilgileniyor.", "tool_calls": [{"function": "create_ticket", "params": {"user_id": generate_user_id(), "issue_description": "İnternet kesintisi", "priority": "high"}}]}
        ]
    })

    # 28. Her şeye "evet" diyen, emin olamayan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "user_profile": UserProfile.CONFUSED_INDECISIVE.value,
        "cognitive_state": CognitiveState.CONFUSED.value,
        "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Paketimi yükseltmek istiyorum sanırım.", "tool_calls": None},
            {"role": "assistant", "content": "'Süper Paket'e geçmek ister misiniz? İçinde 20 GB internet var.", "tool_calls": None},
            {"role": "user", "content": "Evet, evet... olabilir.", "tool_calls": None},
            {"role": "assistant", "content": "**Onaylama Modu Aktif!** 🤔\nAnladım. Sadece teyit etmek için soruyorum: Aylık 150 TL olan ve 20 GB internet içeren 'Süper Paket'e geçişinizi onaylıyor musunuz? Bu işlemden sonra eski paketiniz iptal olacak.", "tool_calls": None},
            {"role": "user", "content": "Aa, yok yok o kadar pahalı olmasın. Vazgeçtim.", "tool_calls": None}
        ]
    })

    # 29. Teknik terimlerle konuşan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "user_profile": UserProfile.IMPATIENT_TECH_SAVVY.value,
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Hattımdaki SNR ve CRC hata oranlarını öğrenebilir miyim?", "tool_calls": None},
            {"role": "assistant", "content": "**Teknik Mod Aktif!** 💻\nElbette, hattınızın teknik verilerini sorguluyorum... SNR marjınız 12 dB, CRC hata sayınız ise son 24 saatte sıfır olarak görünüyor. Değerleriniz oldukça sağlıklı.", "tool_calls": None}
        ]
    })

    # 30. Sadece sesli komut veren, yazmak istemeyen kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value,
        "user_profile": UserProfile.BUSY_MULTITASKING.value,
        "cognitive_state": CognitiveState.DISTRACTED.value,
        "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "/fatura", "tool_calls": None},
            {"role": "assistant", "content": "**Komut Algılama Modu Aktif!** 🤖\nFatura bilgilerinizi sorguluyorum.", "tool_calls": [{"function": "get_current_bill", "params": {"user_id": generate_user_id()}}]},
            {"role": "tool", "content": create_validated_response("GetCurrentBillResponse", {"amount": 99.0, "due_date": "2024-08-30"})},
            {"role": "assistant", "content": "Güncel fatura tutarınız 99.0 TL, son ödeme tarihi 30 Ağustos.", "tool_calls": None}
        ]
    })

    
    # 31. Tehditkar bir dil kullanan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SARCASTIC_IRONIC.value, 
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.ANGRY.value,
        "turns": [
            {"role": "user", "content": "Eğer bu sorunu 1 saat içinde çözmezseniz sizi mahkemeye veririm!", "tool_calls": None},
            {"role": "assistant", "content": "**De-eskalasyon Modu Aktif!**  शांत\nAnlıyorum, durumun sizin için ne kadar sinir bozucu olduğunun farkındayım. Lütfen emin olun, sorununuzu çözmek için elimden gelen her şeyi yapıyorum. Yasal yollara başvurmanıza gerek kalmadan bu işi çözeceğimize inanıyorum. Öncelikle arıza kaydınızı oluşturalım.", "tool_calls": None}
        ]
    })
    
    # 32. Çok yavaş ve tane tane konuşan yaşlı kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.ELDERLY_NON_TECH.value, 
        "cognitive_state": CognitiveState.RELAXED.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Mer... ha... ba... Be... nim... in... ter... ne... tim... yok...", "tool_calls": None},
            {"role": "assistant", "content": "**Sabırlı Mod Aktif!** 🐢\nMerhabalar, anlıyorum. İnternetiniz yokmuş. Hiç sorun değil, ben buradayım. Birlikte halledeceğiz. Şimdi... kontrol ediyorum...", "tool_calls": None}
        ]
    })

    # 33. Çekim gücünden şikayetçi olan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.IMPATIENT_TECH_SAVVY.value, 
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.FRUSTRATED.value,
        "turns": [
            {"role": "user", "content": "Evin içinde telefon çekmiyor, bu nasıl iş!", "tool_calls": None},
            {"role": "assistant", "content": "Anlıyorum, ev içinde sinyal sorunları yaşamanız çok can sıkıcı. Bölgenizdeki baz istasyonlarının durumunu kontrol ediyorum ve size yardımcı olmak için Wi-Fi Calling (VoWiFi) özelliğini aktif etmenizi önerebilirim. Bu özellik, internetiniz üzerinden görüşme yapmanızı sağlar. Aktif edelim mi?", "tool_calls": None}
        ]
    })

    # 34. Borcundan dolayı hattı kapanmış kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.BUSY_MULTITASKING.value, 
        "cognitive_state": CognitiveState.STRESSED.value, "emotional_context": EmotionalContext.ANXIOUS.value,
        "turns": [
            {"role": "user", "content": "Acil arama yapmam lazım ama hattım kapalı! Neden?", "tool_calls": None},
            {"role": "assistant", "content": "Hemen kontrol ediyorum. Görünüşe göre ödenmemiş faturanızdan dolayı hattınız aramalara kapatılmış. Toplam borcunuz 250 TL. Ödeme yaptığınız anda hattınız otomatik olarak açılacaktır. Dilerseniz şimdi ödeme yapabilirsiniz.", "tool_calls": None}
        ]
    })

    # 35. Fatura itiraz süresini soran kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SKEPTICAL_DETAIL_ORIENTED.value, 
        "cognitive_state": CognitiveState.ANALYTICAL.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Faturama itiraz etmek için yasal olarak ne kadar sürem var?", "tool_calls": None},
            {"role": "assistant", "content": "Faturanın size tebliğ edildiği tarihten itibaren yasal itiraz süreniz 8 gündür. İtirazınızı web sitemiz, mobil uygulamamız veya e-Devlet üzerinden yapabilirsiniz. İtirazınız sonuçlanana kadar faturanın son ödeme tarihi durdurulur.", "tool_calls": None}
        ]
    })

    # 36. Cihaz kampanyası soran kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.BARGAIN_HUNTER.value, 
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.HOPEFUL.value,
        "turns": [
            {"role": "user", "content": "Faturama ek telefon alabiliyor muyum? Kampanyalarınız var mı?", "tool_calls": None},
            {"role": "assistant", "content": "Evet, faturanıza ek 12, 24 veya 36 ay taksitle alabileceğiniz birçok güncel cihaz kampanyamız mevcut. İlgilendiğiniz bir marka veya model var mı? Yoksa size popüler seçenekleri sunabilirim.", "tool_calls": None}
        ]
    })

    # 37. Asistanın yeteneklerini test eden kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SARCASTIC_IRONIC.value, 
        "cognitive_state": CognitiveState.ANALYTICAL.value, "emotional_context": EmotionalContext.AMUSED.value,
        "turns": [
            {"role": "user", "content": "Bana bir fıkra anlat.", "tool_calls": None},
            {"role": "assistant", "content": "Temel bir gün yolda yürürken cüzdanını düşürmüş. Arkadaşı Dursun 'Cüzdanın düştü!' diye bağırınca Temel cevap vermiş: 'Biliyorum, içinde para yoktu ki ağır gelsin de fark edeyim.' \n\nŞimdi telekomünikasyon konularına dönecek olursak, nasıl yardımcı olabilirim? 😊", "tool_calls": None}
        ]
    })

    # 38. SIM kart değişikliği talep eden kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.PLANNING.value, 
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Telefonumu değiştirdim, yeni telefona nano SIM kart gerekiyor. SIM kartımı nasıl değiştirebilirim?", "tool_calls": None},
            {"role": "assistant", "content": "SIM kart değişikliği için size en yakın mağazamıza kimliğinizle başvurmanız yeterlidir. İşlem anında ve ücretsiz olarak gerçekleştirilir. Dilerseniz size en yakın mağazanın adresini bulabilirim.", "tool_calls": None}
        ]
    })

    # 39. Kayıp/çalıntı bildirimi yapan panik halindeki kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.ANXIOUS_TRAVELER.value, 
        "cognitive_state": CognitiveState.STRESSED.value, "emotional_context": EmotionalContext.FEARFUL.value,
        "turns": [
            {"role": "user", "content": "Yardım edin! Telefonum çalındı, hattımı hemen kapattırmam lazım!", "tool_calls": None},
            {"role": "assistant", "content": "**Acil Durum Modu Aktif!** 🆘\nSakin olun, hemen yardımcı oluyorum. Güvenliğiniz için hattınızı geçici olarak aramalara ve veri kullanımına kapatıyorum. Bu işlemi onaylıyor musunuz?", "tool_calls": None},
             {"role": "user", "content": "EVET ONAYLIYORUM HEMEN!", "tool_calls": None},
            {"role": "assistant", "content": "Onayınızla hattınız kapatılmıştır. Lütfen en kısa sürede savcılığa veya polise bildirimde bulunun. Yeni SIM kartınızı en yakın mağazamızdan temin edebilirsiniz.", "tool_calls": None}
        ]
    })

    # 40. Taahhüt cayma bedelini öğrenmek isteyen kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SKEPTICAL_DETAIL_ORIENTED.value, 
        "cognitive_state": CognitiveState.PLANNING.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Eğer hattımı şimdi iptal ettirirsem ne kadar cayma bedeli öderim?", "tool_calls": None},
            {"role": "assistant", "content": "Taahhüt bilgilerinizi kontrol ediyorum. Taahhüdünüzün bitmesine 4 ay kalmış. Bugüne kadar yararlandığınız indirimlerin toplamı 240 TL. Eğer bugün iptal ederseniz, kalan ayların fatura toplamı olan 400 TL yerine, daha lehinize olan 240 TL'yi cayma bedeli olarak ödersiniz.", "tool_calls": None}
        ]
    })

    
    # 41. Konuşma dökümü isteyen kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SECURITY_CONSCIOUS.value, 
        "cognitive_state": CognitiveState.ANALYTICAL.value, "emotional_context": EmotionalContext.DISTRUSTFUL.value,
        "turns": [
            {"role": "user", "content": "Geçen hafta yaptığım görüşmenin ses kaydını veya dökümünü alabilir miyim?", "tool_calls": None},
            {"role": "assistant", "content": "Gizlilik ve güvenlik politikalarımız gereği ses kayıtlarını veya görüşme dökümlerini abonelerimizle paylaşamıyoruz. Ancak, sadece yasal merciler (savcılık, mahkeme) tarafından resmi bir talep olması durumunda bu kayıtlar incelenmek üzere sunulmaktadır. Görüşmenizle ilgili spesifik bir sorunuz varsa yardımcı olmaya çalışabilirim.", "tool_calls": None}
        ]
    })
    
    # 42. Şebeke olmayan köyden arayan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.ELDERLY_NON_TECH.value, 
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.HOPEFUL.value,
        "turns": [
            {"role": "user", "content": "Bizim köyde hiç telefon çekmiyor. Buraya bir baz istasyonu kurulması için ne yapabiliriz?", "tool_calls": None},
            {"role": "assistant", "content": "Anlıyorum, köyünüzde iletişim kuramamak büyük bir sorun. Sinyal kalitesini artırmak amacıyla bölgeniz için bir baz istasyonu talebi oluşturabilirim. Lütfen köyünüzün tam adını ve bağlı olduğu il/ilçeyi belirtir misiniz? Talebinizi yatırım planlama birimimize ileteceğim.", "tool_calls": None}
        ]
    })

    # 43. Sadece "hmm", "evet" gibi kısa cevaplar veren kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.CONFUSED_INDECISIVE.value, 
        "cognitive_state": CognitiveState.DISTRACTED.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "assistant", "content": "Size nasıl yardımcı olabilirim?", "tool_calls": None},
            {"role": "user", "content": "hmm...", "tool_calls": None},
            {"role": "assistant", "content": "**Açık Uçlu Soru Modu Aktif!** 🤔\nFaturanızla ilgili bir sorunuz mu var, yoksa paketinizle ilgili bilgi mi almak istiyorsunuz?", "tool_calls": None},
            {"role": "user", "content": "fatura evet.", "tool_calls": None},
            {"role": "assistant", "content": "Anladım, hemen son faturanızı kontrol ediyorum.", "tool_calls": [{"function": "get_current_bill", "params": {"user_id": generate_user_id()}}]}
        ]
    })

    # 44. İnternet bankacılığından ödeme yapamayan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.ELDERLY_NON_TECH.value, 
        "cognitive_state": CognitiveState.CONFUSED.value, "emotional_context": EmotionalContext.FRUSTRATED.value,
        "turns": [
            {"role": "user", "content": "Bankanın sitesinden faturamı ödeyemiyorum, 'borç bulunamadı' diyor.", "tool_calls": None},
            {"role": "assistant", "content": "Anlıyorum, bu durum bazen banka ile aramızdaki anlık veri iletişiminden kaynaklanabiliyor. Lütfen operatör olarak bizi seçtiğinizden ve telefon numaranızı doğru girdiğinizden emin olun. Alternatif olarak, bizim mobil uygulamamızdan veya web sitemizden 7/24 ücretsiz olarak ödeme yapabilirsiniz. Size link göndermemi ister misiniz?", "tool_calls": None}
        ]
    })

    # 45. Çoklu görev yapan, sürekli lafı bölünen kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.BUSY_MULTITASKING.value, 
        "cognitive_state": CognitiveState.DISTRACTED.value, "emotional_context": EmotionalContext.STRESSED.value,
        "turns": [
            {"role": "user", "content": "Benim bir arıza kaydım vardı, bir saniye... Evet, ne oldu o?", "tool_calls": None},
            {"role": "assistant", "content": "Tabii, hemen kontrol ediyorum. Bilet numaranızı alabilir miyim?", "tool_calls": None},
            {"role": "user", "content": "TKT... bekle, evet TKT123... canım sen bir baksana oradan, evet efendim geliyorum!", "tool_calls": None},
            {"role": "assistant", "content": "**Özetleme Modu Aktif!** 📋\nSorun değil, bekliyorum. Siz müsait olduğunuzda devam edebiliriz. Adınıza kayıtlı son arıza kaydını bulmaya çalışıyorum.", "tool_calls": [{"function": "get_user_tickets", "params": {"user_id": generate_user_id()}}]}
        ]
    })

    # 46. Kültürel referanslar kullanan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.HAPPY_SATISFIED.value, 
        "cognitive_state": CognitiveState.RELAXED.value, "emotional_context": EmotionalContext.AMUSED.value,
        "turns": [
            {"role": "user", "content": "İnternet o kadar hızlı ki, Nasreddin Hoca'nın kazanı gibi maşallah.", "tool_calls": None},
            {"role": "assistant", "content": "Bu güzel benzetme ve geri bildirim için teşekkür ederiz! 😊 Memnuniyetinize sevindik. 'Kazan'ınızın hep böyle hızlı 'doğurması' dileğiyle!", "tool_calls": None}
        ]
    })

    # 47. Çok resmi ve kurumsal bir dil kullanan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.SKEPTICAL_DETAIL_ORIENTED.value, 
        "cognitive_state": CognitiveState.ANALYTICAL.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Mevcut aboneliğime ilişkin tarife detaylarının tarafıma e-posta yoluyla iletilmesini talep ediyorum.", "tool_calls": None},
            {"role": "assistant", "content": "Sayın Müşterimiz, talebiniz alınmıştır. Tarife detaylarınız, sistemlerimizde kayıtlı olan e-posta adresinize ivedilikle gönderilecektir. Başka bir talebiniz var mıdır?", "tool_calls": [{"function": "get_package_details", "params": {"package_name": "Mevcut"}}]}
        ]
    })

    # 48. Her şeyin yolunda olup olmadığını kontrol etmek için arayan kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.ANXIOUS_TRAVELER.value, 
        "cognitive_state": CognitiveState.RELAXED.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Merhaba, sadece bir kontrol etmek istedim. Borcum falan var mı? Her şey yolunda mı?", "tool_calls": None},
            {"role": "assistant", "content": "**Proaktif Kontrol Modu Aktif!** ✅\nMerhaba, ne kadar düşüncelisiniz! Hemen kontrol ediyorum... Evet, ödenmemiş faturanız bulunmuyor ve hizmetleriniz aktif olarak devam ediyor. Her şey yolunda görünüyor!", "tool_calls": [{"function": "get_current_bill", "params": {"user_id": generate_user_id()}}]}
        ]
    })

    # 49. Asistanla sohbet etmeye çalışan yalnız kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.CONFUSED_INDECISIVE.value, 
        "cognitive_state": CognitiveState.RELAXED.value, "emotional_context": EmotionalContext.NEUTRAL.value,
        "turns": [
            {"role": "user", "content": "Nasılsın bakalım bugün?", "tool_calls": None},
            {"role": "assistant", "content": "**Sosyal Mod Aktif!** 😊\nTeşekkür ederim, ben bir yapay zekayım ama size yardımcı olmaya her zaman hazırım! Umarım sizin de gününüz iyi geçiyordur. Size telekom hizmetleriyle ilgili nasıl yardımcı olabilirim?", "tool_calls": None}
        ]
    })

    # 50. Hediye internet kodunu kullanmak isteyen kullanıcı
    scenarios.append({
        "id": f"adaptive_comm_{uuid.uuid4().hex[:8]}", "scenario_type": ScenarioType.ADAPTIVE_COMMUNICATION.value, "user_profile": UserProfile.HAPPY_SATISFIED.value, 
        "cognitive_state": CognitiveState.FOCUSED.value, "emotional_context": EmotionalContext.HOPEFUL.value,
        "turns": [
            {"role": "user", "content": "Elimde bir hediye kodu var, bunu nasıl kullanabilirim?", "tool_calls": None},
            {"role": "assistant", "content": "Harika! Hediye kodunuzu mobil uygulamamızdaki 'Hediye Kodu Kullan' menüsünden veya bu konuşma ekranına yazarak aktif edebilirsiniz. Kodu alabilir miyim?", "tool_calls": None}
        ]
    })
    
    return scenarios

def generate_adaptive_communication_scenario() -> Dict[str, Any]:
    """
    Havuzdan rastgele bir adaptif iletişim senaryosu seçer ve döndürür.
    """
    all_scenarios = generate_adaptive_communication_scenarios()
    return random.choice(all_scenarios)
