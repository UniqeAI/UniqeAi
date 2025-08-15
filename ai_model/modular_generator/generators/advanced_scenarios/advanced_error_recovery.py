"""
Gelişmiş hata kurtarma senaryoları üreticisi - Günlük telekom müşteri sorunları
"""
import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from ...utils.helpers import create_validated_response
from ...models.enums import ScenarioType, CognitiveState, EmotionalContext

# Telekom API şeması import'u
try:
    from ...telekom_api_schema import *
except ImportError:
    try:
        from ai_model.modular_generator.telekom_api_schema import *
    except ImportError:
        try:
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.join(current_dir, '..', '..', '..')
            sys.path.insert(0, project_root)
            from ai_model.modular_generator.telekom_api_schema import *
        except ImportError as e:
            print(f"Telekom API şeması import hatası: {e}")
            raise


def generate_advanced_error_recovery_scenarios() -> List[Dict[str, Any]]:
    """
    20 adet günlük telekom müşteri sorunu senaryosu üretir.
    """
    scenarios = []
    user_id_pool = [10000 + i for i in range(50)]

    # 1. Fatura Ödeme Problemi
    user_id = user_id_pool[0]
    scenarios.append({
        "id": f"payment_issue_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "busy_customer",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.URGENT.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Kredi kartımla ödeme yapmaya çalışıyorum ama sürekli reddediliyor! Kartımda sorun yok, başka yerlerde çalışıyor.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Ödeme sorunu yaşamanız çok can sıkıcı. Hemen faturanızı kontrol edip alternatif ödeme seçenekleri sunayım.", "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"bill_id": f"F-2024-{random.randint(100000, 999999)}", "user_id": user_id, "amount": 125.50, "due_date": (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'), "bill_date": datetime.now().strftime('%Y-%m-%d'), "status": BillStatus.UNPAID, "services": [{"service_name": "Aylık Paket", "amount": 125.50}]})},
            {"rol": "asistan", "icerik": "**Ödeme Sorunu Çözümü** 💳\n\n💰 **Faturanız:** 125.50 TL (10 gün vadeli)\n⚠️ **Sorun:** Ödeme ağ geçidi geçici arızası\n\n**Alternatif Ödeme Yöntemleri:**\n🏦 **Havale/EFT:** Anında yansır\n📱 **Dijital Cüzdan:** PayPal, Apple Pay\n🏪 **Bayiiler:** En yakın bayi ile ödeme\n💳 **Farklı Kart:** Başka kredi kartı deneyin\n\n**Hızlı Çözüm:** Dijital cüzdan ile ödemeyi deneyebiliriz. Hangi yöntemi tercih edersiniz?", "arac_cagrilari": None}
        ]
    })

    # 2. İnternet Hızı Düşük
    user_id = user_id_pool[1]
    scenarios.append({
        "id": f"slow_internet_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "streaming_user",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "İnternetim çok yavaş! Netflix izlerken sürekli duraksıyor, Zoom toplantılarında ses gidiyor geliyor.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Streaming ve video konferans için hız çok önemli. Hemen internet hızınızı test edip sorunu çözelim.", "arac_cagrilari": [{"fonksiyon": "test_internet_speed", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(TestInternetSpeedResponse, {"user_id": user_id, "download_speed_mbps": 8.5, "upload_speed_mbps": 2.1, "ping_ms": 45, "test_timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'), "test_server": "Istanbul-1", "quality_rating": "poor"})},
            {"rol": "asistan", "icerik": "**Hız Testi Sonuçları** 📊\n\n📉 **İndirme:** 8.5 Mbps (düşük)\n📤 **Yükleme:** 2.1 Mbps\n⏱️ **Gecikme:** 45 ms\n📍 **Test Sunucu:** İstanbul-1\n\n**Sorun Analizi:**\n⚠️ Streaming için minimum 25 Mbps gerekli\n📺 Netflix 4K için 25+ Mbps öneriliyor\n💻 Zoom HD için 10+ Mbps ideal\n\n**Çözüm Önerileri:**\n🔄 **Modem Reset:** Fişten çekip 30 saniye bekleyin\n📡 **WiFi Optimizasyonu:** 5GHz bandına geçin\n📈 **Hız Yükseltme:** Daha yüksek paket seçenekleri\n🎯 **Teknik Destek:** Saha ekibi gönderebiliriz\n\nHangi çözümle başlayalım?", "arac_cagrilari": None}
        ]
    })

    # 3. Paket Değiştirme İsteği
    user_id = user_id_pool[2]
    scenarios.append({
        "id": f"package_change_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "budget_conscious_customer",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Mevcut paketim çok pahalı geliyor, daha ucuz bir seçenek var mı? Kullanımımı analiz edip öneri verebilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Bütçe planlaması önemli! Önce kullanım alışkanlıklarınızı analiz edip size en uygun paketi bulalım.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"internet_remaining_gb": 18.5, "voice_remaining_minutes": 650, "sms_remaining": 180, "period_end": (datetime.now() + timedelta(days=12)).strftime('%Y-%m-%d'), "usage_percentage": {"internet": 25, "voice": 30, "sms": 15}})},
            {"rol": "asistan", "icerik": "**Kullanım Analizi** 📊\n\n📱 **İnternet:** %25 kullanılmış (18.5 GB kaldı)\n📞 **Konuşma:** %30 kullanılmış (650 dk kaldı)\n💬 **SMS:** %15 kullanılmış (180 adet kaldı)\n📅 **Dönem:** 12 gün kaldı\n\n**Sonuç:** Paketinizi tam kullanmıyorsunuz!\n\n**Daha Ekonomik Seçenekler:**\n💰 **Ekonomik Paket:** 79.90 TL (15 GB + 500 dk)\n🎯 **Temel Paket:** 59.90 TL (10 GB + 300 dk)\n📱 **Sadece İnternet:** 49.90 TL (12 GB)\n\n**Tahmini Tasarruf:** Aylık 40-50 TL\nHangisi size daha uygun?", "arac_cagrilari": None}
        ]
    })

    # 4. Kota Bitti
    user_id = user_id_pool[3]
    scenarios.append({
        "id": f"data_quota_exceeded_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "heavy_data_user",
        "cognitive_state": CognitiveState.FOCUSED.value,
        "emotional_context": EmotionalContext.URGENT.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "İnternetim bitti! Çok önemli bir toplantıya girecektim, hemen ek paket lazım!", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Acil durumu anlıyorum! Hemen ek paket seçeneklerini göstereyim.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Acil 5GB Paketi", "monthly_fee": 19.90, "features": {"internet_gb": 5, "voice_minutes": 0, "sms_count": 0}}, {"name": "Süper 15GB Paketi", "monthly_fee": 39.90, "features": {"internet_gb": 15, "voice_minutes": 0, "sms_count": 0}}]})},
            {"rol": "asistan", "icerik": "**Acil Ek Paket Seçenekleri** ⚡\n\n🚀 **Acil 5GB:** 19.90 TL\n• Anında aktivasyon\n• Toplantı için yeterli\n• SMS onayı ile aktif\n\n💪 **Süper 15GB:** 39.90 TL\n• Bol kullanım\n• Ay sonuna kadar yeter\n• Daha ekonomik (GB başına)\n\n**Aktivasyon Süreci:**\n⚡ SMS onayı → 30 saniye\n📱 Otomatik aktivasyon\n✅ Hemen kullanıma hazır\n\nHangisini tercih edersiniz? Toplantınız için 5GB yeterli olacaktır.", "arac_cagrilari": None}
        ]
    })

    # 5. Roaming Sorunu
    user_id = user_id_pool[4]
    scenarios.append({
        "id": f"roaming_issue_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "international_traveler",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Almanya'ya geldim ama internetim çalışmıyor! Roaming aktif mi kontrol edebilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Yurt dışında internet sorunu çok can sıkıcı. Hemen durumunuzu kontrol edeyim.", "arac_cagrilari": [{"fonksiyon": "get_package_details", "parametreler": {"package_name": "Mevcut Paket"}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPackageDetailsResponse, {"name": "Standart Paket", "monthly_fee": 99.90, "setup_fee": 0.0, "features": {"internet_gb": 20, "voice_minutes": 750, "sms_count": 300, "international_minutes": 50}, "contract_duration": 24, "cancellation_fee": 50.0})},
            {"rol": "asistan", "icerik": "**Roaming Durumu** 🌍\n\n❌ **Sorun:** Paketinizde roaming yok\n📍 **Konum:** Almanya (AB)\n📦 **Mevcut:** Standart Paket (sadece Türkiye)\n\n**Hızlı Çözüm:**\n🇪🇺 **AB Roaming:** 7 gün - 89 TL\n• 5 GB internet + 100 dakika\n• 15 dakikada aktif\n• WhatsApp/Telegram sınırsız\n\n⚡ **Aktivasyon:**\n• SMS: *123*1# çevirin\n• Otomatik başlama\n• Kullanım takibi\n\nHemen aktif edelim mi?", "arac_cagrilari": None}
        ]
    })

    # 6. Bölgesel Arıza
    user_id = user_id_pool[5]
    scenarios.append({
        "id": f"regional_outage_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "concerned_resident",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "İnternetim 3 saattir çalışmıyor, komşular da aynı sorunu yaşıyor. Bölgesel arıza var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Bölgesel arıza şüphenizi anlıyorum. Hemen durumu kontrol edeyim.", "arac_cagrilari": [{"fonksiyon": "check_network_status", "parametreler": {"region": "Istanbul"}}]},
            {"rol": "arac", "icerik": create_validated_response(CheckNetworkStatusResponse, {"region": "Istanbul", "status": "degraded", "coverage_percentage": 75, "active_outages": [{"area": "Beşiktaş-Şişli", "issue": "Fiber kablo kesintisi", "start_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'), "estimated_end": (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')}], "last_updated": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')})},
            {"rol": "asistan", "icerik": "**Bölgesel Arıza Doğrulandı** ⚠️\n\n🗺️ **Etkilenen:** Beşiktaş-Şişli\n🔧 **Sorun:** Fiber kablo kesintisi\n⏰ **Süre:** 3 saat\n🎯 **Çözüm:** 2 saat içinde\n\n**Geçici Çözümler:**\n📱 5GB hotspot kredisi\n💰 Kesinti tazminatı\n📞 SMS güncellemeleri\n\nHotspot kredisini aktif edeyim mi?", "arac_cagrilari": None}
        ]
    })

    # 7. Otomatik Ödeme
    user_id = user_id_pool[6]
    scenarios.append({
        "id": f"autopay_setup_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "forgetful_customer",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.HOPEFUL.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Sürekli fatura ödemeyi unutuyorum, otomatik ödeme kurabilir miyiz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Otomatik ödeme harika çözüm! Fatura stresini ortadan kaldırır.", "arac_cagrilari": [{"fonksiyon": "setup_autopay", "parametreler": {"user_id": user_id, "status": True}}]},
            {"rol": "arac", "icerik": create_validated_response(SetupAutopayResponse, {"user_id": user_id, "autopay_enabled": True, "payment_method": "credit_card_ending_1234", "next_payment_date": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')})},
            {"rol": "asistan", "icerik": "**Otomatik Ödeme Aktif!** 💳\n\n✅ **Durum:** Hazır\n💳 **Kart:** ****1234\n📅 **İlk Ödeme:** 15 gün sonra\n💰 **İndirim:** %5 otomatik ödeme\n\n**Avantajlar:**\n⏰ Hiç unutmayacaksınız\n📧 3 gün önceden hatırlatma\n🛡️ Güvenli işlem\n\nArtık fatura stresi yok! 🎉", "arac_cagrilari": None}
        ]
    })

    # 8. Telefon Numarası Güncelleme
    user_id = user_id_pool[7]
    scenarios.append({
        "id": f"phone_update_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "detail_oriented_customer",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.HOPEFUL.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Telefon numaramı değiştirdim, sistemdeki bilgileri güncelleyebilir misiniz?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "İletişim bilgilerini güncellemek önemli. Önce mevcut profilinizi kontrol edeyim.", "arac_cagrilari": [{"fonksiyon": "get_customer_profile", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerProfileResponse, {"user_id": user_id, "name": "Detaycı Müşteri", "phone_numbers": [{"number": "+905551234567", "type": "mobile", "status": LineStatus.ACTIVE}], "email": "musteri@example.com", "address": "Ankara", "registration_date": "2020-03-15", "customer_tier": "standard"})},
            {"rol": "asistan", "icerik": "**Profil Güncelleme** 📝\n\n👤 **Mevcut:** +905551234567\n📧 **E-posta:** musteri@example.com\n🏠 **Adres:** Ankara\n\n**Güncelleme Süreci:**\n1️⃣ Yeni numara söyleyin\n2️⃣ SMS doğrulama\n3️⃣ Anında aktif\n\n**Güvenlik:** Çift doğrulama\nYeni numaranızı söyleyebilir misiniz?", "arac_cagrilari": None}
        ]
    })

    # 9. Hat Dondurma
    user_id = user_id_pool[8]
    scenarios.append({
        "id": f"line_suspension_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "temporary_traveler",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.CALM.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "3 ay yurt dışında olacağım, hattımı dondurmak istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "3 aylık seyahat için hat dondurma mantıklı. Size seçenekleri göstereyim.", "arac_cagrilari": [{"fonksiyon": "suspend_line", "parametreler": {"user_id": user_id, "duration_months": 3}}]},
            {"rol": "arac", "icerik": create_validated_response(SuspendLineResponse, {"user_id": user_id, "line_number": "+905551234567", "suspension_reason": "geçici durdurma", "suspended_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'), "reactivation_fee": 0.0, "max_suspension_days": 90})},
            {"rol": "asistan", "icerik": "**Hat Dondurma Planlandı** ❄️\n\n📅 **Süre:** 90 gün\n💰 **Ücret:** 9.90 TL/ay (270 TL tasarruf)\n🔄 **Açma:** Ücretsiz\n\n**Korunur:** Numara, paket, indirimler\n**Çalışmaz:** Arama, SMS, internet\n**Acil:** 112 çalışır\n\nOnaylıyor musunuz?", "arac_cagrilari": None}
        ]
    })

    # 10. Şikayet ve Tazminat
    user_id = user_id_pool[9]
    scenarios.append({
        "id": f"compensation_claim_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "demanding_customer",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "3 gündür internetim yok, işimi yapamıyorum! Tazminat istiyorum.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "3 günlük kesinti kabul edilemez. Hemen tazminat sürecini başlatıyorum.", "arac_cagrilari": [{"fonksiyon": "create_fault_ticket", "parametreler": {"user_id": user_id, "issue_description": "3 günlük kesinti - tazminat talebi", "category": "service_interruption", "priority": "high"}}]},
            {"rol": "arac", "icerik": create_validated_response(CreateFaultTicketResponse, {"ticket_id": f"TKT-{random.randint(100000, 999999)}", "user_id": user_id, "issue_description": "3 günlük kesinti - tazminat talebi", "category": "service_interruption", "priority": TicketPriority.HIGH, "status": TicketStatus.OPEN, "created_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'), "estimated_resolution": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ')})},
            {"rol": "asistan", "icerik": f"**Şikayet Kaydedildi** 📝\n\n🎫 **No:** TKT-{random.randint(100000, 999999)}\n⚡ **Öncelik:** Yüksek\n📅 **Çözüm:** 2 gün\n\n**Tazminat:** Fatura indirimi\n**Takip:** 24 saat içinde arama\nÖzür dileriz, telafi edeceğiz!", "arac_cagrilari": None}
        ]
    })

    # 11. 5G Kapsama Sorunu
    user_id = user_id_pool[10]
    scenarios.append({
        "id": f"5g_coverage_issue_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "tech_enthusiast_customer",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.CONFUSED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Yeni iPhone 15 aldım, 5G özelliği var ama hiç 5G çekmiyor. Hep 4G görünüyor. Bölgemde 5G var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Yeni telefonunuz için 5G deneyimi önemli! Hemen kapsama durumunu kontrol edeyim.", "arac_cagrilari": [{"fonksiyon": "check_5g_coverage", "parametreler": {"user_id": user_id, "location": "current_location"}}]},
            {"rol": "arac", "icerik": create_validated_response(Check5GCoverageResponse, {"user_id": user_id, "location": "İstanbul Beşiktaş", "coverage_status": "available", "signal_strength": 78, "download_speed_estimate_mbps": 450.0, "upload_speed_estimate_mbps": 85.0, "latency_estimate_ms": 8, "network_quality": "excellent", "coverage_percentage": 85})},
            {"rol": "asistan", "icerik": "**5G Kapsama Durumu** 📶\n\n✅ **Bölgenizde 5G var!** %85 kapsama\n📊 **Beklenen Hızlar:**\n• İndirme: 450 Mbps\n• Yükleme: 85 Mbps\n• Gecikme: 8 ms\n\n**Telefon Ayarları:**\n📱 Ayarlar > Hücresel > 5G Açık\n🔄 Ağ ayarlarını sıfırlayın\n📍 Konum servislerini açın\n\n5G aktif olduktan sonra test edelim!", "arac_cagrilari": None}
        ]
    })

    # 12. Fatura Geçmişi - Vergi Beyannamesi
    user_id = user_id_pool[11]
    scenarios.append({
        "id": f"bill_history_tax_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "business_customer",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.URGENT.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Vergi beyannamem için 2023 yılının tüm fatura geçmişine ihtiyacım var. Muhasebecim istiyor.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Vergi beyannamesi için fatura geçmişi önemli. Hemen 2023 faturalarınızı getireyim.", "arac_cagrilari": [{"fonksiyon": "get_past_bills", "parametreler": {"user_id": user_id, "limit": 12}}]},
            {"rol": "arac", "icerik": create_validated_response(GetPastBillsResponse, {"bills": [{"bill_id": "F-2023-001", "amount": 125.50, "bill_date": "2023-01-31", "status": BillStatus.PAID, "paid_date": "2023-02-05"}, {"bill_id": "F-2023-012", "amount": 125.50, "bill_date": "2023-12-31", "status": BillStatus.PAID, "paid_date": "2024-01-02"}], "total_count": 12, "total_amount_paid": 1506.00})},
            {"rol": "asistan", "icerik": "**2023 Fatura Özeti** 📊\n\n📄 **Toplam:** 12 fatura\n💰 **Tutar:** 1,506.00 TL\n✅ **Durum:** Tümü ödenmiş\n\n**Vergi İçin:**\n📧 PDF dökümü e-postanıza geliyor\n📝 KDV ayrıştırılmış\n🏢 İşletme gideri olarak gösterebilirsiniz\n\n5 dakika içinde e-postanızda!", "arac_cagrilari": None}
        ]
    })

    # 13. Uluslararası Arama Ücretleri
    user_id = user_id_pool[12]
    scenarios.append({
        "id": f"international_charges_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "frequent_traveler",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.FRUSTRATED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "İngiltere'de 1 hafta kaldım, sadece birkaç arama yaptım ama fatura 800 TL geldi! Bu normal mi?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "800 TL gerçekten yüksek! Hemen fatura detaylarını inceleyelim.", "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"bill_id": f"F-2024-{random.randint(100000, 999999)}", "user_id": user_id, "amount": 823.75, "due_date": (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'), "bill_date": datetime.now().strftime('%Y-%m-%d'), "status": BillStatus.UNPAID, "services": [{"service_name": "Uluslararası Arama", "amount": 645.50}, {"service_name": "Roaming İnternet", "amount": 178.25}]})},
            {"rol": "asistan", "icerik": "**Yüksek Fatura Analizi** 💸\n\n📊 **Toplam:** 823.75 TL\n☎️ **Uluslararası:** 645.50 TL\n📱 **Roaming:** 178.25 TL\n\n**Sorun:** Roaming paketi yokmuş\n💰 **Dakika başı:** 15 TL ücret\n\n**Çözüm:**\n🎯 Roaming paketi retroaktif uygulayabilirim\n💳 ~350 TL'ye düşebilir\n🔄 3 taksit seçeneği\n\nİndirim işlemini başlatayım mı?", "arac_cagrilari": None}
        ]
    })

    # 14. Aile Paketi - Çocuk Kontrolü
    user_id = user_id_pool[13]
    scenarios.append({
        "id": f"family_control_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "concerned_parent",
        "cognitive_state": CognitiveState.EMPATHETIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Aile paketimizde 3 hat var, çocuklarım sürekli oyun oynuyor ve internet bitiriyor. Kontrol edebilir miyim?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Aile internet yönetimi önemli. Kullanım durumunu kontrol edip aile kontrol seçeneklerini göstereyim.", "arac_cagrilari": [{"fonksiyon": "get_remaining_quotas", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetRemainingQuotasResponse, {"internet_remaining_gb": 5.2, "voice_remaining_minutes": 2500, "sms_remaining": 800, "period_end": (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d'), "usage_percentage": {"internet": 89, "voice": 15, "sms": 10}})},
            {"rol": "asistan", "icerik": "**Aile Paketi Durumu** 👨‍👩‍👧‍👦\n\n📊 **İnternet:** %89 kullanılmış (5.2 GB kaldı)\n📞 **Konuşma:** %15 (2500 dk kaldı)\n📅 **8 gün** kaldı\n\n**Aile Kontrol Seçenekleri:**\n👶 Her hat için ayrı limit\n⏰ Gece 22:00-07:00 kısıtlama\n🎮 Oyun sitelerini engelleme\n📱 TikTok/YouTube sınırlama\n\n**Önerim:** Çocuklar için günlük 2GB limit\n💡 Eğitim siteleri sınırsız\n\nAile kontrol aktif edelim mi?", "arac_cagrilari": None}
        ]
    })

    # 15. Yaşlı Müşteri - Basit Telefon
    user_id = user_id_pool[14]
    scenarios.append({
        "id": f"elderly_simple_phone_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "elderly_customer",
        "cognitive_state": CognitiveState.INTUITIVE.value,
        "emotional_context": EmotionalContext.OVERWHELMED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Bu akıllı telefon çok karışık. Sadece arama yapabileceğim basit telefon istiyorum. 75 yaşındayım.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Sizi çok iyi anlıyorum. Basit çözümler daha iyi. Size uygun paketleri bulalım.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Yaşlı Dostu Paket", "monthly_fee": 39.90, "features": {"internet_gb": 2, "voice_minutes": 500, "sms_count": 100}}, {"name": "Sadece Konuşma", "monthly_fee": 29.90, "features": {"internet_gb": 0, "voice_minutes": 1000, "sms_count": 50}}]})},
            {"rol": "asistan", "icerik": "**Basit Paketler** 📞\n\n👴 **Yaşlı Dostu:** 39.90 TL\n• 500 dakika konuşma\n• 100 SMS\n• Büyük tuşlu telefon hediye\n\n📞 **Sadece Konuşma:** 29.90 TL\n• 1000 dakika\n• SOS butonu\n• Karışıklık yok\n\n**Özel Hizmetler:**\n🏥 Tek tuşla ambulans\n👨‍⚕️ Ücretsiz doktor danışma\n🔊 İşitme dostu yüksek ses\n\nHangisi daha uygun?", "arac_cagrilari": None}
        ]
    })

    # 16. Öğrenci Bütçe Paketi
    user_id = user_id_pool[15]
    scenarios.append({
        "id": f"student_budget_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "budget_student",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Üniversite öğrencisiyim, çok kısıtlı bütçem var. En ucuz ama yeterli paketiniz var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Öğrenci bütçesi önemli. Size özel öğrenci paketlerini göstereyim.", "arac_cagrilari": [{"fonksiyon": "get_available_packages", "parametreler": {}}]},
            {"rol": "arac", "icerik": create_validated_response(GetAvailablePackagesResponse, {"packages": [{"name": "Öğrenci Ekonomik", "monthly_fee": 49.90, "features": {"internet_gb": 20, "voice_minutes": 300, "sms_count": 200}}, {"name": "Kampüs Özel", "monthly_fee": 69.90, "features": {"internet_gb": 35, "voice_minutes": 500, "sms_count": 300}}]})},
            {"rol": "asistan", "icerik": "**Öğrenci Paketleri** 🎓\n\n💰 **Ekonomik:** 49.90 TL\n• 20 GB (dersler için yeterli)\n• 300 dakika\n• Öğrenci belgesi ile %20 indirim\n\n📚 **Kampüs Özel:** 69.90 TL\n• 35 GB\n• WiFi entegrasyonu\n\n**Avantajlar:**\n🎯 Eğitim siteleri sınırsız\n📖 Online kütüphane sayılmaz\n🎁 İlk ay ücretsiz\n\nÖğrenci belgeniz var mı?", "arac_cagrilari": None}
        ]
    })

    # 17. İş Yeri Çoklu Hat
    user_id = user_id_pool[16]
    scenarios.append({
        "id": f"business_multiple_lines_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "business_owner",
        "cognitive_state": CognitiveState.STRATEGIC.value,
        "emotional_context": EmotionalContext.AMBITIOUS.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "İşletmem büyüyor, 5 çalışanım için ayrı hatlar lazım. Kurumsal paket var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "İşletme büyümesi harika! Kurumsal çözümlerimizle tam ihtiyacınıza uygun paket hazırlayabiliriz.", "arac_cagrilari": [{"fonksiyon": "get_customer_profile", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerProfileResponse, {"user_id": user_id, "name": "İşletme Sahibi", "phone_numbers": [{"number": "+905551234567", "type": "business", "status": LineStatus.ACTIVE}], "email": "isletme@example.com", "address": "İstanbul", "registration_date": "2020-08-15", "customer_tier": "business"})},
            {"rol": "asistan", "icerik": "**Kurumsal Profil** 🏢\n\n👨‍💼 **İşletme Sahibi**\n📍 İstanbul\n🏆 Kurumsal müşteri\n\n**5 Hatlık Paket:**\n💼 **Toplam:** 399 TL/ay\n📊 **Her Hat:** 25 GB + 750 dk\n📞 **Dahili:** Ücretsiz konuşma\n📧 **Tek Fatura**\n\n**Avantajlar:**\n📈 CRM entegrasyonu\n☁️ 100 GB bulut depolama\n🎧 7/24 öncelikli destek\n\nKurulumu başlatalım mı?", "arac_cagrilari": None}
        ]
    })

    # 18. Evli Çift Ortak Paket
    user_id = user_id_pool[17]
    scenarios.append({
        "id": f"couple_shared_plan_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "married_couple",
        "cognitive_state": CognitiveState.COLLABORATIVE.value,
        "emotional_context": EmotionalContext.HOPEFUL.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Eşimle beraber paket kullanmak istiyoruz. İkimizin de ayrı hattı var ama ortak olsun.", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Çift paketi harika seçenek! Hem tasarruf edersiniz hem paylaşırsınız.", "arac_cagrilari": [{"fonksiyon": "change_package", "parametreler": {"user_id": user_id, "new_package_name": "Çift Paketi"}}]},
            {"rol": "arac", "icerik": create_validated_response(ChangePackageResponse, {"change_id": f"CHG-{random.randint(1000, 9999)}", "from_package": "Bireysel", "to_package": "Çift Paketi", "effective_date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), "fee_difference": -35.00, "status": "scheduled"})},
            {"rol": "asistan", "icerik": "**Çift Paketi Aktif!** 💑\n\n💕 **İki hat, tek paket**\n📊 60 GB + 1500 dk + 500 SMS\n💰 159.90 TL (35 TL tasarruf!)\n🔄 Otomatik paylaşım\n\n**Avantajlar:**\n📱 Esnek kullanım\n💬 Aranızda sınırsız\n📧 Tek fatura\n🎁 Özel gün hediyesi\n\nYarından aktif! 🎉", "arac_cagrilari": None}
        ]
    })

    # 19. Teknik Sorun - Hat Çalışmıyor
    user_id = user_id_pool[18]
    scenarios.append({
        "id": f"line_not_working_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "frustrated_user",
        "cognitive_state": CognitiveState.ANALYTICAL.value,
        "emotional_context": EmotionalContext.URGENT.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Telefonum hiç çalışmıyor! Ne arama yapabiliyor ne alabiliyorum. Acil durumum var!", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Acil durum! Hemen hat durumunu kontrol edip çözelim. Panik yapmayın.", "arac_cagrilari": [{"fonksiyon": "get_customer_profile", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerProfileResponse, {"user_id": user_id, "name": "Acil Durum Müşterisi", "phone_numbers": [{"number": "+905551234567", "type": "mobile", "status": LineStatus.SUSPENDED}], "email": "musteri@example.com", "address": "Ankara", "registration_date": "2021-03-10", "customer_tier": "standard"})},
            {"rol": "asistan", "icerik": "**Sorun Bulundu!** ⚠️\n\n🚫 **Hat askıya alınmış**\n📱 +905551234567\n⏰ **Neden:** Ödeme gecikmesi\n\n**Hızlı Çözüm:**\n1️⃣ Fatura ödemesi\n2️⃣ 15 dakikada aktif\n3️⃣ Test arama\n\n**Geçici:**\n📞 112, 155, 156 çalışıyor\n📱 WiFi ile WhatsApp\n\nFatura durumunu kontrol edeyim:", "arac_cagrilari": [{"fonksiyon": "get_current_bill", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCurrentBillResponse, {"bill_id": f"F-2024-{random.randint(100000, 999999)}", "user_id": user_id, "amount": 89.90, "due_date": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), "bill_date": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'), "status": BillStatus.OVERDUE, "services": [{"service_name": "Aylık Paket", "amount": 89.90}]})},
            {"rol": "asistan", "icerik": "**Geciken Fatura** 💡\n\n💳 89.90 TL (5 gün geçmiş)\n📅 Vade dolmuş\n\n**Hızlı Çözüm:**\n⚡ Şimdi öderseniz 15 dakikada açılır\n💳 Kredi kartı/havale kabul\n📱 Ödeme sonrası test\n\nÖdemeyi yapalım mı?", "arac_cagrilari": None}
        ]
    })

    # 20. Emekli Ekonomik Paket
    user_id = user_id_pool[19]
    scenarios.append({
        "id": f"retiree_budget_{uuid.uuid4().hex[:8]}",
        "scenario_type": ScenarioType.ADVANCED_ERROR_RECOVERY.value,
        "personality_profile": "retiree_customer",
        "cognitive_state": CognitiveState.SYSTEMATIC.value,
        "emotional_context": EmotionalContext.WORRIED.value,
        "donguler": [
            {"rol": "kullanici", "icerik": "Emekliyim, maaşım 5000 TL. Telefon faturası çok yüksek, daha ekonomik paket var mı?", "arac_cagrilari": None},
            {"rol": "asistan", "icerik": "Emekli bütçesi önemli. Size en uygun ekonomik paketi bulalım.", "arac_cagrilari": [{"fonksiyon": "get_customer_package", "parametreler": {"user_id": user_id}}]},
            {"rol": "arac", "icerik": create_validated_response(GetCustomerPackageResponse, {"package_name": "Standart Paket", "monthly_fee": 129.90, "features": {"internet_gb": 30, "voice_minutes": 750, "sms_count": 300, "roaming_enabled": False, "international_minutes": 0}, "activation_date": "2020-05-15", "renewal_date": "2024-05-15"})},
            {"rol": "asistan", "icerik": "**Mevcut Paket Analizi** 💰\n\n📦 **Standart:** 129.90 TL/ay\n📊 30 GB + 750 dk + 300 SMS\n💸 Maaşınızın %2.6'sı\n\n**Emekli Alternatifleri:**\n👴 **Emekli Özel:** 59.90 TL\n• 15 GB + 500 dk\n• %25 emekli indirimi\n\n📞 **Sadece Konuşma:** 39.90 TL\n• 1000 dk + 50 SMS\n\n**Avantajlar:**\n🏥 Ücretsiz doktor hattı\n📱 Büyük tuşlu telefon\n🆘 Acil buton\n\n**Tasarruf:** 70 TL/ay!", "arac_cagrilari": None}
        ]
    })

    return scenarios


def generate_advanced_error_recovery_scenario() -> Dict[str, Any]:
    """
    Havuzdan rastgele bir gelişmiş hata kurtarma senaryosu seçer ve döndürür.
    """
    all_scenarios = generate_advanced_error_recovery_scenarios()
    if not all_scenarios:
        return []
    return all_scenarios
