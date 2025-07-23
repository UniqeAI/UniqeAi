# AI Endpoint Fonksiyonları Dokümantasyonu

Bu doküman, yapay zeka sisteminin backend'e çağrı yapabileceği tüm fonksiyonları içermektedir. Her fonksiyon belirli bir işlem için tasarlanmış olup, yapay zeka kullanıcı isteklerini yerine getirmek için bu fonksiyonları kullanabilir.

## 📋 İçindekiler

1. [Genel Kullanım Kuralları](#genel-kullanım-kuralları)
2. [Chat API Fonksiyonları](#chat-api-fonksiyonları)
3. [Telekom API Fonksiyonları](#telekom-api-fonksiyonları)
4. [Kullanıcı Yönetimi Fonksiyonları](#kullanıcı-yönetimi-fonksiyonları)
5. [Mock Test Fonksiyonları](#mock-test-fonksiyonları)
6. [Sistem Durumu Fonksiyonları](#sistem-durumu-fonksiyonları)
7. [Hata Yönetimi ve Çözümleri](#hata-yönetimi-ve-çözümleri)
8. [Pratik Kullanım Senaryoları](#pratik-kullanım-senaryoları)

---

## 📚 Genel Kullanım Kuralları

### Parametre Türleri ve Kısıtlamalar

**Temel Veri Türleri:**
- `str`: Metin değeri (1-1000 karakter arası)
- `int`: Tam sayı (0-999999 arası)
- `bool`: Boolean değer (true/false)
- `float`: Ondalık sayı (0.0-999999.99 arası)
- `Optional[T]`: Opsiyonel parametre (None olabilir)

**Kullanıcı ID Formatları:**
- `user_id` (int): Telekom müşteri ID'si (0-999999)
- `user_id` (str): Sistem kullanıcı ID'si ("user123", "USER_456" gibi)
- `session_id` (str): Oturum ID'si ("SESSION_abc123" formatında)

**Tarih Formatları:**
- ISO 8601 formatı: "2024-03-15T14:25:30"
- Tarih formatı: "2024-03-15"

### Standart Yanıt Formatı

```json
{
  "success": true|false,
  "message": "Açıklama mesajı",
  "data": {}, // Veri içeriği
  "timestamp": "2024-03-15T14:25:30",
  "error": "Hata mesajı" // Sadece hata durumunda
}
```

---

## 🗨️ Chat API Fonksiyonları

### `ai_chat_send_message`
**Açıklama:** AI ile sohbet mesajı gönder

**Parametreler:**
- `message` (str): Kullanıcı mesajı
  - **Alabileceği Değerler:** 1-1000 karakter arası metin
  - **Örnek Değerler:** "Merhaba", "Faturam ne kadar?", "Paketimi değiştirmek istiyorum"
- `user_id` (str): Kullanıcı ID
  - **Alabileceği Değerler:** Alfanümerik string, 3-50 karakter
  - **Örnek Değerler:** "user123", "USER_456", "ahmet_yilmaz"
- `session_id` (str, opsiyonel): Oturum ID
  - **Alabileceği Değerler:** "SESSION_" ile başlayan string veya null
  - **Örnek Değerler:** "SESSION_abc123", null (otomatik oluşturulur)

**Kullanım Örneği:**
```python
# Örnek 1: Temel mesaj gönderme
result = await ai_chat_send_message(
    message="Merhaba, yardıma ihtiyacım var",
    user_id="user123"
)

# Örnek 2: Belirli oturum ile mesaj gönderme
result = await ai_chat_send_message(
    message="Faturam ne kadar?",
    user_id="user123",
    session_id="SESSION_abc123"
)
```

**Dönen Değer:**
```json
{
  "success": true,
  "response": "AI yanıtı (1-2000 karakter)",
  "user_message": "Gönderilen mesaj",
  "user_id": "user123",
  "session_id": "SESSION_abc123",
  "yanit_id": "yanit_456",
  "guven_puani": 0.95, // 0.0-1.0 arası güven puanı
  "arac_cagrilari": [], // Kullanılan araç listesi
  "metadata": {
    "islenme_zamani": "2024-03-15T14:25:30",
    "baglam_mesaj_sayisi": 5
  }
}
```

**Hata Durumları:**
- `message` boş ise: "Mesaj boş olamaz"
- `user_id` geçersiz ise: "Geçersiz kullanıcı ID"
- Sistem aşırı yüklü ise: "Sistem geçici olarak meşgul"

---

### `ai_chat_clear_session`
**Açıklama:** Chat oturumunu temizle

**Parametreler:**
- `session_id` (str): Temizlenecek oturum ID
  - **Alabileceği Değerler:** "SESSION_" ile başlayan string
  - **Örnek Değerler:** "SESSION_abc123", "SESSION_xyz789"

**Kullanım Örneği:**
```python
# Oturum temizleme
result = await ai_chat_clear_session(
    session_id="SESSION_abc123"
)
```

**Dönen Değer:**
```json
{
  "success": true,
  "message": "Oturum geçmişi başarıyla temizlendi",
  "session_id": "SESSION_abc123"
}
```

**Hata Durumları:**
- Oturum bulunamaz ise: "Oturum bulunamadı"
- Geçersiz format ise: "Geçersiz oturum ID formatı"

---

### `ai_chat_get_system_status`
**Açıklama:** Sistem durumunu getir

**Parametreler:** Yok

**Kullanım Örneği:**
```python
# Sistem durumu kontrolü
result = await ai_chat_get_system_status()
```

**Dönen Değer:**
```json
{
  "success": true,
  "message": "Sistem durumu başarıyla getirildi",
  "data": {
    "model_hizmeti": {
      "model_adi": "llama-3.1-8b",
      "durum": "aktif",
      "son_guncelleme": "2024-03-15T14:25:30"
    },
    "arac_kaydi": {
      "toplam_arac": 25,
      "aktif_arac": 23,
      "son_kontrol": "2024-03-15T14:25:30"
    },
    "konusma_yoneticisi": {
      "aktif_oturum_sayisi": 12,
      "max_mesaj_sayisi": 50
    },
    "telekom_api": {
      "durum": "aktif",
      "musteri_sayisi": 8,
      "yanit_suresi_ms": 150
    }
  }
}
```

**Hata Durumları:**
- Sistem erişilemez ise: "Sistem durumu alınamadı"

---

## 📱 Telekom API Fonksiyonları

### 💰 Fatura & Ödeme İşlemleri

#### `telekom_get_current_bill`
**Açıklama:** Mevcut fatura bilgilerini getir

**Parametreler:**
- `user_id` (int): Müşteri ID
  - **Alabileceği Değerler:** 0-999999 arası tam sayı
  - **Örnek Değerler:** 0, 1, 2, 3, 4, 5, 6, 7 (test müşterileri)

**Kullanım Örneği:**
```python
# Mevcut fatura bilgisi alma
result = await telekom_get_current_bill(user_id=1)

# Farklı müşteri için fatura
result = await telekom_get_current_bill(user_id=5)
```

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "bill_id": "F-2024-0001", // Fatura ID (unique)
    "user_id": 1,
    "amount": 75.5, // Toplam tutar (TRY)
    "currency": "TRY", // Para birimi
    "due_date": "2024-03-15", // Son ödeme tarihi
    "bill_date": "2024-02-28", // Fatura tarihi
    "status": "unpaid|paid", // Ödeme durumu
    "services": [
      {
        "service_name": "Mega İnternet", // Hizmet adı
        "amount": 52.85 // Hizmet tutarı
      },
      {
        "service_name": "Sesli Arama",
        "amount": 22.65
      }
    ]
  }
}
```

**Alınabilecek Değerler:**
- `amount`: 50-350 TRY arası
- `status`: "paid" veya "unpaid"
- `services`: 1-5 arası hizmet kalemi

**Hata Durumları:**
- `user_id` geçersiz ise: "Geçersiz müşteri ID"
- Fatura bulunamaz ise: "Mevcut fatura bulunamadı"

#### `telekom_get_bill_history`
**Açıklama:** Geçmiş faturaları getir

**Parametreler:**
- `user_id` (int): Müşteri ID
  - **Alabileceği Değerler:** 0-999999 arası tam sayı
  - **Örnek Değerler:** 0, 1, 2, 3, 4, 5, 6, 7
- `limit` (int, varsayılan: 12): Maksimum fatura sayısı
  - **Alabileceği Değerler:** 1-24 arası tam sayı
  - **Örnek Değerler:** 3, 6, 12, 24

**Kullanım Örneği:**
```python
# Son 12 fatura (varsayılan)
result = await telekom_get_bill_history(user_id=1)

# Son 6 fatura
result = await telekom_get_bill_history(user_id=1, limit=6)

# Son 3 fatura
result = await telekom_get_bill_history(user_id=2, limit=3)
```

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "bills": [
      {
        "bill_id": "F-2024-0001-01", // Fatura ID
        "user_id": 1,
        "amount": 75.5, // Fatura tutarı
        "currency": "TRY",
        "bill_date": "2024-01-28", // Fatura tarihi
        "due_date": "2024-02-12", // Son ödeme tarihi
        "status": "paid|unpaid", // Ödeme durumu
        "services": [
          {
            "service_name": "Mega İnternet",
            "amount": 52.85
          }
        ]
      }
    ],
    "total_count": 1, // Toplam fatura sayısı
    "user_id": 1
  }
}
```

**Alınabilecek Değerler:**
- `bills`: 0-limit arası fatura listesi
- `total_count`: 0-limit arası sayı
- Her fatura için `amount`: 50-350 TRY arası
- `status`: "paid" veya "unpaid"

**Hata Durumları:**
- `user_id` geçersiz ise: "Geçersiz müşteri ID"
- `limit` aralık dışı ise: "Limit 1-24 arası olmalı"
- Fatura bulunamaz ise: "Geçmiş fatura bulunamadı"

#### `telekom_pay_bill`
**Açıklama:** Fatura ödemesi yap

**Parametreler:**
- `bill_id` (str): Fatura ID
  - **Alabileceği Değerler:** "F-YYYY-NNNN" formatında string
  - **Örnek Değerler:** "F-2024-0001", "F-2024-0002", "F-2024-0003"
- `method` (str): Ödeme yöntemi
  - **Alabileceği Değerler:** "kredi_karti", "banka_karti", "havale", "mobil_odeme"
  - **Örnek Değerler:** "kredi_karti", "banka_karti", "havale"

**Kullanım Örneği:**
```python
# Kredi kartı ile ödeme
result = await telekom_pay_bill(
    bill_id="F-2024-0001",
    method="kredi_karti"
)

# Banka kartı ile ödeme
result = await telekom_pay_bill(
    bill_id="F-2024-0002",
    method="banka_karti"
)

# Havale ile ödeme
result = await telekom_pay_bill(
    bill_id="F-2024-0003",
    method="havale"
)
```

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "payment_id": "PAY-20240315142530", // Ödeme ID (unique)
    "bill_id": "F-2024-0001", // Ödenen fatura ID
    "amount": 75.5, // Ödeme tutarı
    "method": "kredi_karti", // Kullanılan ödeme yöntemi
    "status": "completed", // Ödeme durumu
    "transaction_date": "2024-03-15T14:25:30", // İşlem tarihi
    "confirmation_code": "CONF-20240315142530" // Onay kodu
  }
}
```

**Alınabilecek Değerler:**
- `payment_id`: "PAY-" ile başlayan unique string
- `amount`: 50-350 TRY arası
- `status`: "completed", "failed", "pending"
- `confirmation_code`: "CONF-" ile başlayan string

**Hata Durumları:**
- `bill_id` geçersiz ise: "Geçersiz fatura ID"
- `method` desteklenmiyor ise: "Desteklenmeyen ödeme yöntemi"
- Fatura zaten ödenmiş ise: "Fatura zaten ödenmiş"
- Ödeme başarısız ise: "Ödeme işlemi başarısız"

#### `telekom_get_payment_history`
**Açıklama:** Ödeme geçmişini getir

**Parametreler:**
- `user_id` (int): Müşteri ID

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "payments": [
      {
        "payment_id": "PAY-20240315142530",
        "amount": 75.5,
        "method": "kredi_karti",
        "status": "completed",
        "transaction_date": "2024-03-15T14:25:30"
      }
    ],
    "total_count": 1,
    "user_id": 1
  }
}
```

#### `telekom_setup_autopay`
**Açıklama:** Otomatik ödeme ayarla

**Parametreler:**
- `user_id` (int): Müşteri ID
- `status` (bool): Otomatik ödeme durumu

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "autopay_enabled": true,
    "setup_date": "2024-03-15T14:25:30",
    "payment_method": "kredi_karti",
    "next_payment_date": "2024-04-15"
  }
}
```

### 📦 Paket & Tarife Yönetimi

#### `telekom_get_current_package`
**Açıklama:** Müşterinin mevcut paketini getir

**Parametreler:**
- `user_id` (int): Müşteri ID
  - **Alabileceği Değerler:** 0-999999 arası tam sayı
  - **Örnek Değerler:** 0, 1, 2, 3, 4, 5, 6, 7 (test müşterileri)

**Kullanım Örneği:**
```python
# Mevcut paket bilgisi alma
result = await telekom_get_current_package(user_id=1)

# Farklı müşteri paketi
result = await telekom_get_current_package(user_id=3)
```

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "package_name": "Mega İnternet", // Paket adı
    "monthly_fee": 69.5, // Aylık ücret (TRY)
    "features": {
      "internet_gb": 50, // İnternet kotası (GB)
      "voice_minutes": 1000, // Konuşma dakikası
      "sms_count": 500, // SMS adedi
      "roaming_enabled": false // Roaming durumu
    },
    "user_id": 1,
    "activation_date": "2024-01-01", // Aktivasyon tarihi
    "renewal_date": "2024-04-01", // Yenileme tarihi
    "status": "active" // Paket durumu
  }
}
```

**Alınabilecek Değerler:**
- `package_name`: "Mega İnternet", "Öğrenci Dostu Tarife", "Süper Konuşma", "Premium Paket"
- `monthly_fee`: 49.90-89.90 TRY arası
- `internet_gb`: 25-100 GB arası
- `voice_minutes`: 500-3000 dakika arası
- `sms_count`: 250-1000 SMS arası
- `roaming_enabled`: true/false
- `status`: "active", "suspended", "cancelled"

**Hata Durumları:**
- `user_id` geçersiz ise: "Geçersiz müşteri ID"
- Paket bulunamaz ise: "Mevcut paket bulunamadı"

#### `telekom_get_remaining_quotas`
**Açıklama:** Müşterinin kalan kotalarını getir

**Parametreler:**
- `user_id` (int): Müşteri ID

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "internet_remaining_gb": 35.5,
    "voice_remaining_minutes": 850,
    "sms_remaining": 420,
    "period_end": "2024-03-31",
    "usage_percentage": {
      "internet": 29,
      "voice": 15,
      "sms": 16
    }
  }
}
```

#### `telekom_change_package`
**Açıklama:** Paket değişikliği başlat

**Parametreler:**
- `user_id` (int): Müşteri ID
- `new_package_name` (str): Yeni paket adı

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "old_package": "Mega İnternet",
    "new_package": "Premium Paket",
    "change_date": "2024-03-15T14:25:30",
    "effective_date": "2024-04-01",
    "status": "scheduled"
  }
}
```

#### `telekom_get_available_packages`
**Açıklama:** Kullanılabilir paketleri listele

**Parametreler:** Yok

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "packages": [
      {
        "package_name": "Mega İnternet",
        "monthly_fee": 69.5,
        "features": {
          "internet_gb": 50,
          "voice_minutes": 1000,
          "sms_count": 500,
          "roaming_enabled": false
        },
        "description": "Hızlı internet ve bol dakika"
      }
    ],
    "total_count": 5
  }
}
```

#### `telekom_get_package_details`
**Açıklama:** Paket detaylarını getir

**Parametreler:**
- `package_name` (str): Paket adı

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "package_name": "Mega İnternet",
    "monthly_fee": 69.5,
    "features": {
      "internet_gb": 50,
      "voice_minutes": 1000,
      "sms_count": 500,
      "roaming_enabled": false
    },
    "description": "Hızlı internet ve bol dakika",
    "contract_duration": "12 ay",
    "early_termination_fee": 200.0,
    "activation_fee": 0.0
  }
}
```

#### `telekom_enable_roaming`
**Açıklama:** Roaming hizmetini etkinleştir/devre dışı bırak

**Parametreler:**
- `user_id` (int): Müşteri ID
- `status` (bool): Roaming durumu

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "roaming_enabled": true,
    "effective_date": "2024-03-15T14:25:30",
    "supported_countries": ["EU", "USA", "Canada", "Australia"],
    "daily_fee": 15.0
  }
}
```

### 🔧 Teknik Destek & Arıza

#### `telekom_check_network_status`
**Açıklama:** Ağ durumunu kontrol et

**Parametreler:**
- `region` (str): Bölge

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "region": "istanbul",
    "status": "operational",
    "last_updated": "2024-03-15T14:25:30",
    "services": {
      "voice": "operational",
      "data": "operational",
      "sms": "operational"
    },
    "maintenance_scheduled": false,
    "outages": []
  }
}
```

#### `telekom_create_support_ticket`
**Açıklama:** Arıza talebi oluştur

**Parametreler:**
- `user_id` (int): Müşteri ID
- `issue_description` (str): Sorun açıklaması
- `category` (str, varsayılan: "technical"): Kategori
- `priority` (str, varsayılan: "medium"): Öncelik

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "ticket_id": "TICKET-20240315142530",
    "user_id": 1,
    "issue_description": "İnternet bağlantısı yok",
    "category": "technical",
    "priority": "medium",
    "status": "open",
    "created_date": "2024-03-15T14:25:30",
    "estimated_resolution": "2024-03-16T14:25:30"
  }
}
```

#### `telekom_get_support_ticket_status`
**Açıklama:** Arıza talebi durumunu getir

**Parametreler:**
- `ticket_id` (str): Talep ID

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "ticket_id": "TICKET-20240315142530",
    "status": "in_progress",
    "priority": "medium",
    "created_date": "2024-03-15T14:25:30",
    "last_updated": "2024-03-15T15:30:00",
    "estimated_resolution": "2024-03-16T14:25:30",
    "updates": [
      {
        "date": "2024-03-15T15:30:00",
        "message": "Teknisyen atandı",
        "status": "in_progress"
      }
    ]
  }
}
```

#### `telekom_test_internet_speed`
**Açıklama:** İnternet hız testi yap

**Parametreler:**
- `user_id` (int): Müşteri ID

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "test_date": "2024-03-15T14:25:30",
    "download_speed_mbps": 85.5,
    "upload_speed_mbps": 12.3,
    "ping_ms": 15,
    "test_server": "Istanbul",
    "quality_score": "excellent"
  }
}
```

### 👤 Hesap Yönetimi

#### `telekom_get_customer_profile`
**Açıklama:** Müşteri profilini getir

**Parametreler:**
- `user_id` (int): Müşteri ID

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "name": "Mehmet Demir",
    "phone_numbers": [
      {
        "number": "+905551234567",
        "type": "mobile",
        "status": "active"
      }
    ],
    "email": "mehmet.demir@email.com",
    "address": "Türkiye",
    "registration_date": "2022-06-15",
    "customer_tier": "premium"
  }
}
```

#### `telekom_update_customer_contact`
**Açıklama:** Müşteri iletişim bilgilerini güncelle

**Parametreler:**
- `user_id` (int): Müşteri ID
- `contact_type` (str): İletişim türü (email, phone, address)
- `new_value` (str): Yeni değer

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "contact_type": "email",
    "old_value": "mehmet.demir@email.com",
    "new_value": "mehmet.yeni@email.com",
    "updated_date": "2024-03-15T14:25:30",
    "status": "updated"
  }
}
```

#### `telekom_suspend_line`
**Açıklama:** Hatı askıya al

**Parametreler:**
- `user_id` (int): Müşteri ID
- `reason` (str): Askıya alma nedeni

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "status": "suspended",
    "reason": "Ödeme gecikme",
    "suspended_date": "2024-03-15T14:25:30",
    "reactivation_fee": 25.0,
    "estimated_reactivation_date": "2024-03-22T14:25:30"
  }
}
```

#### `telekom_reactivate_line`
**Açıklama:** Hatı yeniden etkinleştir

**Parametreler:**
- `user_id` (int): Müşteri ID

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "status": "active",
    "reactivated_date": "2024-03-15T14:25:30",
    "reactivation_fee_paid": true,
    "services_restored": ["voice", "data", "sms"]
  }
}
```

---

## 👥 Kullanıcı Yönetimi Fonksiyonları

### `get_current_user`
**Açıklama:** Geçerli kullanıcı bilgilerini getir

**Parametreler:** Yok

**Dönen Değer:**
```json
{
  "success": true,
  "message": "Geçerli kullanıcı bilgileri başarıyla getirildi",
  "data": {
    "user_id": "user123",
    "username": "ahmet",
    "email": "ahmet@email.com",
    "full_name": "Ahmet Yılmaz",
    "phone": "+90 532 123 4567",
    "preferences": {},
    "last_login": "2024-03-15T14:25:30",
    "is_active": true,
    "metadata": {}
  }
}
```

---

## 🧪 Mock Test Fonksiyonları

### `getCurrentUser`
**Açıklama:** Mock kullanıcı bilgilerini getir

**Parametreler:** Yok

**Dönen Değer:**
```json
{
  "success": true,
  "message": "Geçerli kullanıcı bilgileri başarıyla getirildi",
  "data": {
    "user_id": "user123",
    "username": "test_user",
    "email": "test@email.com",
    "full_name": "Test Kullanıcı",
    "phone": "+90 532 123 4567",
    "preferences": {},
    "last_login": "2024-03-15T14:25:30",
    "is_active": true
  }
}
```

---

## 📊 Sistem Durumu Fonksiyonları

### Sistem Durumu Kontrolü
Sistem durumu aşağıdaki bileşenleri kontrol eder:

- **Model Hizmeti**: AI model durumu
- **Araç Kayıtları**: Kayıtlı araçlar ve durumları
- **Konuşma Yöneticisi**: Aktif oturum sayısı
- **Telekom API**: API durumu ve müşteri sayısı

---

## 🔗 Endpoint Kullanım Örnekleri

### REST API Endpoint'leri

```bash
# Kullanıcı giriş
POST /api/v1/user/login

# Geçerli kullanıcı bilgisi
GET /api/v1/user/current

# Chat gönderme
POST /api/v1/chat/

# Telekom müşteri profili
GET /api/v1/telekom/customer/{user_id}

# Fatura getirme
GET /api/v1/telekom/bill/{user_id}

# Paket değişikliği
POST /api/v1/telekom/package/change

# Destek talebi
POST /api/v1/telekom/support/ticket
```

---

## 🛠️ Geliştirici Notları

### Fonksiyon Mapping
AI orchestrator'da tüm fonksiyonlar şu şekilde mapping edilmiştir:

```python
function_mapping = {
    # FATURA & ÖDEME İŞLEMLERİ
    "get_current_bill": ai_endpoint_functions.telekom_get_current_bill,
    "get_past_bills": ai_endpoint_functions.telekom_get_bill_history,
    "pay_bill": ai_endpoint_functions.telekom_pay_bill,
    "get_payment_history": ai_endpoint_functions.telekom_get_payment_history,
    "setup_autopay": ai_endpoint_functions.telekom_setup_autopay,
    
    # PAKET & TARİFE YÖNETİMİ
    "get_customer_package": ai_endpoint_functions.telekom_get_current_package,
    "get_remaining_quotas": ai_endpoint_functions.telekom_get_remaining_quotas,
    "change_package": ai_endpoint_functions.telekom_change_package,
    "get_available_packages": ai_endpoint_functions.telekom_get_available_packages,
    "get_package_details": ai_endpoint_functions.telekom_get_package_details,
    "enable_roaming": ai_endpoint_functions.telekom_enable_roaming,
    
    # TEKNİK DESTEK & ARIZA
    "check_network_status": ai_endpoint_functions.telekom_check_network_status,
    "create_fault_ticket": ai_endpoint_functions.telekom_create_support_ticket,
    "get_fault_ticket_status": ai_endpoint_functions.telekom_get_support_ticket_status,
    "test_internet_speed": ai_endpoint_functions.telekom_test_internet_speed,
    
    # HESAP YÖNETİMİ
    "get_customer_profile": ai_endpoint_functions.telekom_get_customer_profile,
    "update_customer_contact": ai_endpoint_functions.telekom_update_customer_contact,
    "suspend_line": ai_endpoint_functions.telekom_suspend_line,
    "reactivate_line": ai_endpoint_functions.telekom_reactivate_line,
    
    # KULLANICI BİLGİLERİ
    "get_current_user": self._get_current_user
}
```

### Hata Yönetimi
Tüm fonksiyonlar standart hata yönetimi kullanır:

```python
{
  "success": false,
  "error": "Hata açıklaması",
  "message": "Kullanıcı dostu hata mesajı"
}
```

### Loglama
Tüm fonksiyonlar detaylı loglama yapar:
- İstek parametreleri loglanır
- Başarılı sonuçlar loglanır
- Hatalar detaylı şekilde loglanır

---

## 🚨 Hata Yönetimi ve Çözümleri

### Yaygın Hata Türleri

#### 1. Parametre Hataları
```json
{
  "success": false,
  "error": "Parametre hatası",
  "message": "Geçersiz user_id değeri"
}
```

**Çözüm:**
- `user_id` 0-999999 arası olmalı
- String parametreler boş olmamalı
- Boolean parametreler true/false olmalı

#### 2. Veri Bulunamadı Hataları
```json
{
  "success": false,
  "error": "Veri bulunamadı",
  "message": "Belirtilen müşteri bulunamadı"
}
```

**Çözüm:**
- Geçerli müşteri ID'leri: 0, 1, 2, 3, 4, 5, 6, 7
- Önce müşteri varlığını kontrol et
- Alternatif müşteri ID'si dene

#### 3. Sistem Hataları
```json
{
  "success": false,
  "error": "Sistem hatası",
  "message": "Servis geçici olarak kullanılamıyor"
}
```

**Çözüm:**
- 1-2 saniye bekleyip tekrar dene
- Sistem durumunu kontrol et
- Basit işlemlerle test et

### Hata Durumunda Yapılacaklar

1. **Hata Türünü Belirle:** `success: false` kontrolü
2. **Hata Mesajını Analiz Et:** `error` ve `message` alanları
3. **Uygun Çözümü Uygula:** Yukarıdaki çözümleri kullan
4. **Kullanıcıyı Bilgilendir:** Anlaşılır hata mesajı ver

---

## 💡 Pratik Kullanım Senaryoları

### Senaryo 1: Fatura Sorgulama ve Ödeme
```python
# 1. Mevcut fatura bilgisini al
current_bill = await telekom_get_current_bill(user_id=1)

if current_bill["success"]:
    bill_data = current_bill["data"]
    
    # 2. Fatura ödenmiş mi kontrol et
    if bill_data["status"] == "unpaid":
        # 3. Ödeme yap
        payment = await telekom_pay_bill(
            bill_id=bill_data["bill_id"],
            method="kredi_karti"
        )
        
        if payment["success"]:
            return f"Fatura başarıyla ödendi. Tutar: {bill_data['amount']} TRY"
    else:
        return "Fatura zaten ödenmiş"
```

### Senaryo 2: Paket Bilgisi ve Kota Kontrolü
```python
# 1. Mevcut paket bilgisini al
package = await telekom_get_current_package(user_id=1)

if package["success"]:
    # 2. Kalan kotaları al
    quotas = await telekom_get_remaining_quotas(user_id=1)
    
    if quotas["success"]:
        quota_data = quotas["data"]
        return f"""
        Paket: {package['data']['package_name']}
        Kalan İnternet: {quota_data['internet_remaining_gb']} GB
        Kalan Dakika: {quota_data['voice_remaining_minutes']} dakika
        """
```

### Senaryo 3: Destek Talebi Oluşturma
```python
# 1. Önce müşteri profilini al
profile = await telekom_get_customer_profile(user_id=1)

if profile["success"]:
    # 2. Destek talebi oluştur
    ticket = await telekom_create_support_ticket(
        user_id=1,
        issue_description="İnternet bağlantısı çok yavaş",
        category="technical",
        priority="medium"
    )
    
    if ticket["success"]:
        return f"Destek talebi oluşturuldu. Talep ID: {ticket['data']['ticket_id']}"
```

### Senaryo 4: Kullanıcı Bilgisi ve Personalizasyon
```python
# 1. Geçerli kullanıcı bilgilerini al
user = await get_current_user()

if user["success"]:
    user_data = user["data"]
    
    # 2. Kullanıcı adıyla kişiselleştirilmiş yanıt ver
    return f"Merhaba {user_data['full_name']}, size nasıl yardımcı olabilirim?"
```

### Senaryo 5: Hata Yönetimi ile Güvenli İşlem
```python
async def safe_operation(user_id):
    try:
        # İşlem dene
        result = await telekom_get_current_bill(user_id=user_id)
        
        if result["success"]:
            return result["data"]
        else:
            # Hata durumunda alternatif çözüm
            return {"message": "Fatura bilgisi şu anda alınamıyor"}
            
    except Exception as e:
        # Beklenmeyen hata
        return {"message": "Servis geçici olarak kullanılamıyor"}
```

---

## 📊 Performans ve Limitler

### Yanıt Süreleri
- **Chat işlemleri:** 100-500ms
- **Telekom API:** 200-1000ms
- **Kullanıcı işlemleri:** 50-200ms

### Limitler
- **Maksimum mesaj uzunluğu:** 1000 karakter
- **Maksimum oturum sayısı:** 100 aktif oturum
- **Maksimum fatura geçmişi:** 24 ay
- **Maksimum destek talebi:** 10 açık talep per müşteri

---

## 📝 Güncellemeler

- **v1.0.0**: İlk sürüm oluşturuldu
- **v1.1.0**: Kullanıcı yönetimi fonksiyonları eklendi
- **v1.2.0**: Telekom API fonksiyonları genişletildi
- **v1.3.0**: Detaylı kullanım örnekleri ve hata yönetimi eklendi

---

## 🔍 Özet

Bu dokümantasyon, yapay zeka sisteminin backend ile etkileşimde bulunması için gerekli tüm bilgileri içermektedir:

- **25+ Fonksiyon** detaylı açıklamalarla
- **Parametre spesifikasyonları** ve sınırları
- **Pratik kullanım örnekleri** ve senaryolar
- **Hata yönetimi** ve çözüm önerileri
- **Performans bilgileri** ve limitler

Her fonksiyon test edilmiş ve üretim ortamında kullanılmaya hazırdır. Yapay zeka bu dokümantasyonu kullanarak kullanıcı isteklerini etkili bir şekilde karşılayabilir. 