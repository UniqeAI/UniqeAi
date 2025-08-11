import json
import random
import uuid
from datetime import datetime
from collections import defaultdict, Counter

def load_api_schema():
    """API şemasını yükle"""
    try:
        with open('ai_model/scripts/telekom_api_schema.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # API fonksiyonlarını çıkar
        api_functions = []
        lines = content.split('\n')
        for line in lines:
            if 'class ' in line and 'Response' in line and '(BaseModel)' in line:
                func_name = line.split('class ')[1].split('Response')[0]
                # CamelCase'den snake_case'e çevir
                snake_case = ''.join(['_' + c.lower() if c.isupper() and i > 0 else c.lower() 
                                    for i, c in enumerate(func_name)]).lstrip('_')
                api_functions.append(snake_case)
        
        return list(set(api_functions))
    except:
        # Fallback API listesi
        return [
            'get_remaining_quotas', 'get_current_bill', 'pay_bill', 'get_available_packages',
            'change_package', 'get_package_details', 'check_network_status', 'create_fault_ticket',
            'get_fault_ticket_status', 'enable_roaming', 'disable_roaming', 'get_roaming_charges',
            'suspend_line', 'reactivate_line', 'get_past_bills', 'setup_autopay', 'cancel_autopay',
            'update_customer_contact', 'get_customer_profile', 'check_5g_coverage',
            'test_internet_speed', 'get_payment_history', 'add_payment_method',
            'remove_payment_method', 'get_usage_history', 'set_data_limit',
            'activate_emergency_service', 'deactivate_emergency_service'
        ]

def create_new_endpoint_scenarios():
    """Yeni endpoint kategorileri için senaryolar oluştur"""
    
    scenarios = {
        'kalan_kullanimlarim': {
            'messages': [
                'Bu ay ne kadar internetim kaldı?',
                'Kalan dakikalarımı görebilir miyim?',
                'SMS kotam ne durumda?',
                'Paket kullanım durumumu kontrol et',
                'Ne kadar veri hakkım var?',
                'Aylık kotamdan ne kadar kullandım?',
                'İnternet hızım neden yavaş?',
                'Kullanım geçmişimi göster',
                'Bu dönem ne kadar harcadım?',
                'Kalan haklarımı listele'
            ],
            'apis': ['get_remaining_quotas', 'get_usage_history', 'test_internet_speed']
        },
        
        'faturalarim': {
            'messages': [
                'Son 3 ayın faturalarını göster',
                'Geçmiş faturalarım nerede?',
                'Fatura detaylarını açıkla',
                'Bu ayki fatura neden yüksek?',
                'Ödenmemiş faturalarım var mı?',
                'Fatura kesim tarihi ne zaman?',
                'E-fatura nasıl alırım?',
                'Fatura itirazı yapmak istiyorum',
                'Fatura özetini mail at',
                'Taksitli ödeme yapabilir miyim?'
            ],
            'apis': ['get_current_bill', 'get_past_bills', 'pay_bill', 'get_payment_history']
        },
        
        'paket_servislerim': {
            'messages': [
                'Mevcut paketim nedir?',
                'Hangi servislere abonem?',
                'Ek hizmetlerimi listele',
                'Paket değişikliği yapmak istiyorum',
                'Daha ucuz paket var mı?',
                'Öğrenci indirimi alabilir miyim?',
                'Kampanyalı paketler neler?',
                'Paket yükseltmesi nasıl yapılır?',
                'Unlimited paketiniz var mı?',
                'Aile paketi seçenekleri neler?'
            ],
            'apis': ['get_package_details', 'get_available_packages', 'change_package']
        },
        
        'hat_islemleri': {
            'messages': [
                'Yeni hat açmak istiyorum',
                'İkinci hat alabilir miyim?',
                'Hat transferi nasıl yapılır?',
                'Hattımı başkasına devredebilir miyim?',
                'Numara taşıma işlemi nasıl?',
                'Hat sahibi değişikliği gerekiyor',
                'Ek hat için gerekli belgeler neler?',
                'Kurumsal hat açabilir miyim?',
                'Hat iptal etmek istiyorum',
                'Geçici hat dondurma yapılır mı?'
            ],
            'apis': ['suspend_line', 'reactivate_line', 'get_customer_profile', 'update_customer_contact']
        },
        
        'iletisim_bilgileri': {
            'messages': [
                'Adres bilgilerimi güncellemek istiyorum',
                'Telefon numaram değişti',
                'E-mail adresimi değiştir',
                'İletişim tercihlerimi ayarla',
                'SMS bildirimleri gelmiyor',
                'Mail adresimi doğrula',
                'Acil durum kişisi ekleyebilir miyim?',
                'Kişisel bilgilerimi güncelle',
                'İletişim izinlerimi yönet',
                'Veri kullanım rızamı güncelle'
            ],
            'apis': ['update_customer_contact', 'get_customer_profile']
        },
        
        'hat_ayarlari': {
            'messages': [
                'Hattımın güvenlik ayarlarını kontrol et',
                'PIN kodumu değiştirmek istiyorum',
                'Hat blokajını kaldır',
                'Güvenlik şifremi unuttum',
                'Hattan gelen aramaları engelle',
                'Numaramı gizli göster',
                'Çağrı bekletme nasıl aktif edilir?',
                'Hat ayarlarımı fabrika ayarına döndür',
                'Otomatik yanıt mesajı kur',
                'Hat yönlendirme ayarla'
            ],
            'apis': ['get_customer_profile', 'update_customer_contact']
        },
        
        'internet_ayarlari': {
            'messages': [
                'İnternet APN ayarları neler?',
                'Mobil veri açılmıyor',
                'İnternet bağlantısı yavaş',
                'Wi-Fi şifremi unuttum',
                'Mobil hotspot nasıl açılır?',
                '5G ayarlarımı kontrol et',
                'Veri tasarrufu modunu aç',
                'İnternet hız testi yap',
                'Roaming ayarlarını kapat',
                'Veri sınırı koyabilir miyim?'
            ],
            'apis': ['test_internet_speed', 'check_5g_coverage', 'set_data_limit', 'check_network_status']
        },
        
        'yurtdisi_ayarlari': {
            'messages': [
                'Yurt dışı paketlerini aktif et',
                'Roaming ücretleri nedir?',
                'Avrupa\'da internet kullanımı',
                'Yurt dışı arama tarifesi',
                'Roaming ayarlarını kapat',
                'Seyahat paketi var mı?',
                'Yurt dışı SMS ücreti ne kadar?',
                'Roaming faturası yüksek geldi',
                'Hangi ülkelerde geçerli?',
                'Yurt dışı acil durum hattı'
            ],
            'apis': ['enable_roaming', 'disable_roaming', 'get_roaming_charges']
        },
        
        'fatura_ayarlari': {
            'messages': [
                'Otomatik ödeme talimatı ver',
                'Fatura kesim tarihini değiştir',
                'E-faturaya geç',
                'Kağıt fatura istemiyorum',
                'Fatura hatırlatması kur',
                'Ödeme yöntemimi güncelle',
                'Kredi kartımı kaydet',
                'Banka hesabından otomatik çekim',
                'Fatura adresini değiştir',
                'Taksitli ödeme seçeneği'
            ],
            'apis': ['setup_autopay', 'cancel_autopay', 'add_payment_method', 'remove_payment_method']
        },
        
        'sim_kart_islemleri': {
            'messages': [
                'SIM kartım çalışmıyor',
                'Yeni SIM kart istiyorum',
                'SIM kart değişikliği nasıl yapılır?',
                'Kayıp SIM kart bildirimi',
                'SIM kart bloke oldu',
                'Nano SIM\'e geçiş yapabilir miyim?',
                'SIM kart aktivasyonu',
                'Çoklu SIM kart alabilir miyim?',
                'SIM kart PIN kodu',
                'SIM kart hasarlı'
            ],
            'apis': ['suspend_line', 'reactivate_line', 'get_customer_profile']
        },
        
        'esim_islemleri': {
            'messages': [
                'eSIM nedir, nasıl alırım?',
                'eSIM aktivasyonu yapılır mı?',
                'Fiziksel SIM\'den eSIM\'e geçiş',
                'eSIM QR kodu gönder',
                'eSIM destekleyen cihazlar',
                'eSIM ile yurt dışı kullanımı',
                'eSIM profili silindi, ne yapmalıyım?',
                'Çoklu eSIM profili kullanabilir miyim?',
                'eSIM yedekleme nasıl yapılır?',
                'eSIM ile numara taşıma'
            ],
            'apis': ['get_customer_profile', 'update_customer_contact']
        },
        
        'ev_interneti': {
            'messages': [
                'Evime internet bağlatmak istiyorum',
                'Fiber altyapı var mı bölgemde?',
                'ADSL\'den fibere geçiş',
                'İnternet hız paketleri neler?',
                'Modem kurulumu nasıl yapılır?',
                'İnternet bağlantısı kesilmeye devam ediyor',
                'Wi-Fi şifremi değiştirmek istiyorum',
                'İnternet hızım düşük',
                'Sabit IP adresi alabilir miyim?',
                'İnternet + TV paketi var mı?'
            ],
            'apis': ['check_network_status', 'test_internet_speed', 'get_available_packages']
        },
        
        'mobil_imza': {
            'messages': [
                'Mobil imza nasıl alınır?',
                'Mobil imza şifremi unuttum',
                'Mobil imza sertifikası yenileme',
                'E-imza ile mobil imza arasındaki fark',
                'Mobil imza ile hangi işlemler yapılır?',
                'Mobil imza güvenli mi?',
                'Mobil imza aktivasyon kodu',
                'Mobil imza iptal etmek istiyorum',
                'Mobil imza kullanım ücreti',
                'Mobil imza teknik destek'
            ],
            'apis': ['get_customer_profile', 'update_customer_contact']
        }
    }
    
    return scenarios

def generate_conversation_turn(message, api_function, scenario_type):
    """Tek bir konuşma turunu oluştur"""
    
    user_id = random.randint(1000, 9999)
    
    # Çeşitli asistan yanıtları
    assistant_responses = [
        f"Tabii ki! {message.lower()} konusunda size yardımcı olayım. Hemen kontrol ediyorum.",
        f"Elbette, bu konuda size destek olabilirim. Bilgilerinizi kontrol ediyorum.",
        f"Anladım, {message.lower()} için gerekli işlemleri başlatıyorum.",
        f"Hemen yardımcı oluyorum. Sisteminizi kontrol ediyorum.",
        f"Tabii, bu konuda size en iyi çözümü sunmak için bilgilerinizi inceliyorum."
    ]
    
    # API yanıtları
    api_responses = {
        'get_remaining_quotas': f'{{"success": true, "data": {{"internet_remaining_gb": {random.uniform(1, 50):.1f}, "voice_remaining_minutes": {random.randint(100, 2000)}, "sms_remaining": {random.randint(50, 500)}}}}}',
        'get_current_bill': f'{{"success": true, "data": {{"bill_id": "F-2024-{user_id}", "amount": {random.uniform(50, 300):.2f}, "currency": "TRY", "status": "unpaid", "due_date": "2024-12-15"}}}}',
        'get_available_packages': '{"success": true, "data": {"packages": [{"name": "Süper Paket", "monthly_fee": 89.90, "features": {"internet_gb": 40, "voice_minutes": "Sınırsız"}}]}}',
        'test_internet_speed': f'{{"success": true, "data": {{"download_speed": {random.uniform(20, 100):.1f}, "upload_speed": {random.uniform(5, 50):.1f}, "ping": {random.randint(10, 50)}}}}}',
        'check_network_status': '{"success": true, "data": {"network_status": "Bölgenizde aktif arıza bulunmuyor", "signal_strength": "İyi"}}',
        'get_customer_profile': f'{{"success": true, "data": {{"customer_id": {user_id}, "name": "Sayın Müşteri", "status": "active", "registration_date": "2020-03-15"}}}}',
        'enable_roaming': '{"success": true, "data": {"roaming_enabled": true, "daily_fee": 25.00, "status": "Yurt dışı kullanım hizmeti aktif edildi"}}',
        'setup_autopay': '{"success": true, "data": {"autopay_enabled": true, "payment_method": "Kredi Kartı", "status": "Otomatik ödeme talimatı verildi"}}'
    }
    
    # Kapanış mesajları
    closing_responses = [
        "İşleminiz tamamlandı. Başka bir konuda yardımcı olabilir miyim?",
        "Talebiniz başarıyla gerçekleştirildi. Teşekkür ederim, başka bir şey var mı?",
        "İşlem başarıyla tamamlandı. Size yardımcı olabildiğim için memnunum.",
        "Tamamlandı! Başka bir konuda destek olmamı ister misiniz?",
        "İşleminiz hazır. Teşekkür ederim, başka sorunuz var mı?"
    ]
    
    conversation = [
        {
            "rol": "kullanici",
            "icerik": message,
            "arac_cagrilari": None
        },
        {
            "rol": "asistan", 
            "icerik": random.choice(assistant_responses),
            "arac_cagrilari": None
        },
        {
            "rol": "asistan",
            "icerik": None,
            "arac_cagrilari": [
                {
                    "fonksiyon": api_function,
                    "parametreler": {"user_id": user_id}
                }
            ]
        },
        {
            "rol": "arac",
            "icerik": api_responses.get(api_function, '{"success": true, "data": {"message": "İşlem başarılı"}}'),
            "arac_cagrisi_kimligi": f"{api_function}_{uuid.uuid4().hex[:8]}"
        },
        {
            "rol": "asistan",
            "icerik": random.choice(closing_responses),
            "arac_cagrilari": None
        }
    ]
    
    return conversation

def complete_20k_dataset():
    """16,743 kayıtlı veri setini 20K'ya tamamla"""
    
    # Mevcut temizlenmiş veri setini yükle
    balanced_file = "real_balanced_dataset_20250808_104846.json"
    
    with open(balanced_file, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    print("🚀 20K VERİ SETİ TAMAMLAMA BAŞLIYOR")
    print("="*60)
    print(f"📊 Mevcut kayıt: {len(existing_data):,}")
    
    target_count = 20000
    needed_count = target_count - len(existing_data)
    print(f"🎯 Hedef: {target_count:,} kayıt")
    print(f"➕ Eklenecek: {needed_count:,} kayıt")
    
    # Yeni senaryoları yükle
    scenarios = create_new_endpoint_scenarios()
    api_functions = load_api_schema()
    
    print(f"📋 Yeni senaryo kategorisi: {len(scenarios)}")
    print(f"🔧 Kullanılabilir API: {len(api_functions)}")
    
    # Kategori başına eşit dağılım
    records_per_category = needed_count // len(scenarios)
    extra_records = needed_count % len(scenarios)
    
    print(f"⚖️ Kategori başına kayıt: {records_per_category}")
    print(f"➕ Ekstra kayıt: {extra_records}")
    
    new_records = []
    category_stats = {}
    
    for i, (category, scenario_data) in enumerate(scenarios.items()):
        category_count = records_per_category
        if i < extra_records:
            category_count += 1
        
        category_stats[category] = category_count
        
        print(f"\n🏗️ {category.upper()} kategorisi oluşturuluyor... ({category_count} kayıt)")
        
        for j in range(category_count):
            # Rastgele mesaj ve API seç
            message = random.choice(scenario_data['messages'])
            api_function = random.choice(scenario_data['apis'])
            
            # Konuşma oluştur
            conversation = generate_conversation_turn(message, api_function, category)
            
            # Kayıt oluştur
            record = {
                "id": f"new_endpoint_{category}_{uuid.uuid4().hex[:12]}",
                "scenario_type": f"new_{category}",
                "personality_profile": random.choice([
                    "helpful_customer_service", "technical_support", "friendly_assistant",
                    "professional_advisor", "patient_guide", "solution_focused"
                ]),
                "cognitive_state": random.choice([
                    "analytical", "empathetic", "focused", "creative", "systematic"
                ]),
                "emotional_context": random.choice([
                    "supportive", "understanding", "encouraging", "calm", "positive"
                ]),
                "cultural_context": "turkish_telecom_customer",
                "donguler": conversation
            }
            
            new_records.append(record)
    
    print(f"\n📊 YENİ KAYIT İSTATİSTİKLERİ:")
    for category, count in category_stats.items():
        print(f"   • {category}: {count} kayıt")
    
    # Veri setlerini birleştir
    complete_dataset = existing_data + new_records
    
    print(f"\n🎯 FINAL VERİ SETİ:")
    print(f"   • Mevcut kayıt: {len(existing_data):,}")
    print(f"   • Yeni kayıt: {len(new_records):,}")
    print(f"   • Toplam kayıt: {len(complete_dataset):,}")
    
    # Kaydet
    output_filename = f"complete_balanced_20k_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(complete_dataset, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 20K VERİ SETİ TAMAMLANDI!")
    print(f"   • Dosya: {output_filename}")
    print(f"   • Boyut: {len(complete_dataset):,} kayıt")
    print(f"   • Yeni endpoint kategorisi: {len(scenarios)}")
    
    # Final kontrol
    final_message_check = defaultdict(int)
    for record in complete_dataset:
        for dongu in record.get('donguler', []):
            if dongu.get('rol') == 'kullanici':
                message = dongu.get('icerik', '').strip()
                final_message_check[message] += 1
                break
    
    max_repeats = max(final_message_check.values())
    unique_messages = len(final_message_check)
    
    print(f"\n📈 FINAL TEKRAR KONTROLÜ:")
    print(f"   • Benzersiz mesaj: {unique_messages:,}")
    print(f"   • Max tekrar: {max_repeats} kez")
    print(f"   • Ortalama tekrar: {len(complete_dataset) / unique_messages:.1f} kez")
    
    # En çok tekrarlananları göster
    most_repeated = sorted(final_message_check.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"   • En çok tekrarlanan 5 mesaj:")
    for msg, count in most_repeated:
        print(f"     - {count} kez: '{msg[:50]}{'...' if len(msg) > 50 else ''}'")
    
    return output_filename, complete_dataset

if __name__ == "__main__":
    output_file, final_dataset = complete_20k_dataset()
