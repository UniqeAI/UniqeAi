# API Endpointleri Açıklama Dökümanı

Bu dökümanda projede tanımlı olan tüm API endpointleri, açıklamaları ve parametreleri listelenmiştir. Ayrıca Swagger arayüzüne erişim bilgisi de yer almaktadır.

---

## Chat API (backend/app/api/v1/chat.py)

### 1. Sohbet Başlat / Mesaj Gönder
- **Yöntem:** POST
- **URL:** `/chat/`
- **Açıklama:** Kullanıcıdan gelen mesajı yapay zekaya iletir ve yanıt döner.
- **Request Body:**
  - `message` (str): Kullanıcı mesajı
  - `user_id` (str): Kullanıcı ID
  - `session_id` (str, opsiyonel): Oturum ID (yoksa otomatik oluşturulur)
- **Response:**
  - AI yanıtı, güven puanı, araç çağrısı bilgileri ve oturum detayları

### 2. Oturum Geçmişini Temizle
- **Yöntem:** POST
- **URL:** `/chat/session/clear`
- **Açıklama:** Belirtilen oturumun konuşma geçmişini temizler.
- **Request Body:**
  - `session_id` (str): Temizlenecek oturumun ID'si
- **Response:**
  - Başarı durumu ve oturum ID

### 3. Sistem Durumu
- **Yöntem:** GET
- **URL:** `/chat/system/status`
- **Açıklama:** Sistem ve model durumu hakkında bilgi verir.
- **Response:**
  - Model, araçlar, konuşma yöneticisi ve telekom API durumu

---

## Mock Test API (backend/app/api/v1/mock_test.py)

### 1. Kullanıcı Bilgisi Getir
- **Yöntem:** GET
- **URL:** `/mock-test/user/{user_id}`
- **Açıklama:** Belirtilen kullanıcı ID'si için kullanıcı bilgilerini döner.

### 2. Kullanılabilir Paketler
- **Yöntem:** GET
- **URL:** `/mock-test/packages`
- **Açıklama:** Tüm kullanılabilir paketleri listeler.

### 3. Fatura Bilgisi Getir
- **Yöntem:** GET
- **URL:** `/mock-test/invoice/{user_id}`
- **Açıklama:** Belirtilen kullanıcıya ait fatura bilgilerini döner.

### 4. Müşteri Bilgisi Getir
- **Yöntem:** GET
- **URL:** `/mock-test/customer/{user_id}`
- **Açıklama:** Müşteri bilgilerini döner.

### 5. Ödeme Geçmişi
- **Yöntem:** GET
- **URL:** `/mock-test/payments/{user_id}`
- **Açıklama:** Kullanıcının ödeme geçmişini döner.

### 6. Abonelik Durumu
- **Yöntem:** GET
- **URL:** `/mock-test/subscription/{user_id}`
- **Açıklama:** Kullanıcının abonelik durumunu döner.

### 7. Destek Talepleri
- **Yöntem:** GET
- **URL:** `/mock-test/support/{user_id}`
- **Açıklama:** Kullanıcının destek taleplerini döner.

### 8. Adres Bilgisi
- **Yöntem:** GET
- **URL:** `/mock-test/address/{user_id}`
- **Açıklama:** Kullanıcının adres bilgilerini döner.

### 9. Kampanyalar
- **Yöntem:** GET
- **URL:** `/mock-test/campaigns`
- **Açıklama:** Tüm kampanyaları listeler.


Herhangi bir sorunuz olursa teknik ekibe danışabilirsiniz. 