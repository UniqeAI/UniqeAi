# 📊 KAYITLI 6 KULLANICI İÇİN VERİ ANALİZİ

## 👥 Kullanıcı Profilleri

### **User ID: 0 - Enes Faruk Aydın**
```json
{
  "name": "Enes Faruk Aydın",
  "phone_numbers": [{"number": "+905551234567", "type": "mobile", "status": "active"}],
  "email": "enes.faruk.aydin@email.com",
  "address": "Ankara, Çankaya",
  "registration_date": "2022-06-15",
  "customer_tier": "premium"
}
```

### **User ID: 1 - Nisa Nur Özkal**
```json
{
  "name": "Nisa Nur Özkal",
  "phone_numbers": [{"number": "+905559876543", "type": "mobile", "status": "active"}],
  "email": "nisa.nur.ozkal@email.com",
  "address": "İstanbul, Beşiktaş",
  "registration_date": "2023-03-20",
  "customer_tier": "gold"
}
```

### **User ID: 2 - Sedat Kılıçoğlu**
```json
{
  "name": "Sedat Kılıçoğlu",
  "phone_numbers": [{"number": "+905551112223", "type": "mobile", "status": "active"}],
  "email": "sedat.kilicoglu@email.com",
  "address": "İzmir, Konak",
  "registration_date": "2021-11-10",
  "customer_tier": "silver"
}
```

### **User ID: 3 - Erkan Tanrıöver**
```json
{
  "name": "Erkan Tanrıöver",
  "phone_numbers": [{"number": "+905554445556", "type": "mobile", "status": "active"}],
  "email": "erkan.tanriover@email.com",
  "address": "Bursa, Nilüfer",
  "registration_date": "2023-08-05",
  "customer_tier": "gold"
}
```

### **User ID: 4 - Ahmet Nazif Gemalmaz**
```json
{
  "name": "Ahmet Nazif Gemalmaz",
  "phone_numbers": [{"number": "+905557778889", "type": "mobile", "status": "active"}],
  "email": "ahmet.nazif.gemalmaz@email.com",
  "address": "Antalya, Muratpaşa",
  "registration_date": "2022-12-01",
  "customer_tier": "premium"
}
```

### **User ID: 5 - Ziişan Şahin**
```json
{
  "name": "Ziişan Şahin",
  "phone_numbers": [{"number": "+905557771234", "type": "mobile", "status": "active"}],
  "email": "ziisan.sahin@email.com",
  "address": "istanbul, eminönü",
  "registration_date": "2024-12-01",
  "customer_tier": "diomand"
}
```

## 💰 Fatura Verileri

### **Mevcut Fatura (get_current_bill)**
Her kullanıcı için farklı tutar:
- **User 0:** 50 TL (50 + 0%50)
- **User 1:** 51 TL (50 + 1%50)
- **User 2:** 52 TL (50 + 2%50)
- **User 3:** 53 TL (50 + 3%50)
- **User 4:** 54 TL (50 + 4%50)
- **User 5:** 99 TL (50 + 5%50)

**Ödeme Durumu:**
- **User 0:** unpaid (0%3 == 0)
- **User 1:** paid (1%3 != 0)
- **User 2:** paid (2%3 != 0)
- **User 3:** unpaid (3%3 == 0)
- **User 4:** paid (4%3 != 0)
- **User 5:** paid (5%3 != 0)

### **Geçmiş Faturalar (get_past_bills)**
Her kullanıcı için 12 adet fatura:
- **User 0:** 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105 TL
- **User 1:** 51, 56, 61, 66, 71, 76, 81, 86, 91, 96, 101, 106 TL
- **User 2:** 52, 57, 62, 67, 72, 77, 82, 87, 92, 97, 102, 107 TL
- **User 3:** 53, 58, 63, 68, 73, 78, 83, 88, 93, 98, 103, 108 TL
- **User 4:** 54, 59, 64, 69, 74, 79, 84, 89, 94, 99, 104, 109 TL
- **User 5:** 99, 104, 109, 114, 119, 124, 129, 134, 139, 144, 149, 154 TL

## 📦 Paket Verileri

### **Mevcut Paket (get_current_package)**
4 farklı paket türü (user_id % 4):

**User 0:** Mega İnternet
```json
{
  "package_name": "Mega İnternet",
  "monthly_fee": 69.50,
  "features": {
    "internet_gb": 50,
    "voice_minutes": 1000,
    "sms_count": 500,
    "roaming_enabled": false
  }
}
```

**User 1:** Öğrenci Dostu Tarife
```json
{
  "package_name": "Öğrenci Dostu Tarife",
  "monthly_fee": 49.90,
  "features": {
    "internet_gb": 30,
    "voice_minutes": 500,
    "sms_count": 250,
    "roaming_enabled": false
  }
}
```

**User 2:** Süper Konuşma
```json
{
  "package_name": "Süper Konuşma",
  "monthly_fee": 59.90,
  "features": {
    "internet_gb": 25,
    "voice_minutes": 2000,
    "sms_count": 1000,
    "roaming_enabled": true
  }
}
```

**User 3:** Premium Paket
```json
{
  "package_name": "Premium Paket",
  "monthly_fee": 89.90,
  "features": {
    "internet_gb": 100,
    "voice_minutes": 3000,
    "sms_count": 1000,
    "roaming_enabled": true
  }
}
```

**User 4:** Mega İnternet (tekrar)
**User 5:** Öğrenci Dostu Tarife (tekrar)

## 📊 Kota Verileri

### **Kalan Kotalar (get_remaining_quotas)**
Her kullanıcı için farklı kotalar:

**User 0:**
```json
{
  "internet_remaining_gb": 50,
  "voice_remaining_minutes": 1000,
  "sms_remaining": 500,
  "usage_percentage": {
    "internet": 10,
    "voice": 5,
    "sms": 5
  }
}
```

**User 1:**
```json
{
  "internet_remaining_gb": 49,
  "voice_remaining_minutes": 999,
  "sms_remaining": 499,
  "usage_percentage": {
    "internet": 11,
    "voice": 6,
    "sms": 6
  }
}
```

**User 2:**
```json
{
  "internet_remaining_gb": 48,
  "voice_remaining_minutes": 998,
  "sms_remaining": 498,
  "usage_percentage": {
    "internet": 12,
    "voice": 7,
    "sms": 7
  }
}
```

**User 3:**
```json
{
  "internet_remaining_gb": 47,
  "voice_remaining_minutes": 997,
  "sms_remaining": 497,
  "usage_percentage": {
    "internet": 13,
    "voice": 8,
    "sms": 8
  }
}
```

**User 4:**
```json
{
  "internet_remaining_gb": 46,
  "voice_remaining_minutes": 996,
  "sms_remaining": 496,
  "usage_percentage": {
    "internet": 14,
    "voice": 9,
    "sms": 9
  }
}
```

**User 5:**
```json
{
  "internet_remaining_gb": 20,
  "voice_remaining_minutes": 600,
  "sms_remaining": 300,
  "usage_percentage": {
    "internet": 30,
    "voice": 25,
    "sms": 25
  }
}
```

## 🛠️ Destek Verileri

### **Destek Talepleri (create_fault_ticket)**
Her kullanıcı için farklı ticket ID'leri:
- **User 0:** TICKET-0001
- **User 1:** TICKET-0002
- **User 2:** TICKET-0003
- **User 3:** TICKET-0004
- **User 4:** TICKET-0005
- **User 5:** TICKET-0006

## ⚙️ Sistem Verileri

### **İnternet Hız Testi (test_internet_speed)**
Her kullanıcı için farklı hızlar:
- **User 0:** 100 Mbps download, 50 Mbps upload
- **User 1:** 95 Mbps download, 48 Mbps upload
- **User 2:** 90 Mbps download, 45 Mbps upload
- **User 3:** 85 Mbps download, 42 Mbps upload
- **User 4:** 80 Mbps download, 40 Mbps upload
- **User 5:** 75 Mbps download, 37 Mbps upload

### **Ağ Durumu (check_network_status)**
Bölge bazlı durum:
- **İstanbul:** Excellent
- **Ankara:** Good
- **İzmir:** Fair
- **Bursa:** Good
- **Antalya:** Excellent

## 📈 Veri Özeti

### **Kullanıcı Tipleri:**
- **Premium:** User 0, User 4
- **Gold:** User 1, User 3
- **Silver:** User 2
- **Diamond:** User 5

### **Paket Dağılımı:**
- **Mega İnternet:** User 0, User 4
- **Öğrenci Dostu:** User 1, User 5
- **Süper Konuşma:** User 2
- **Premium Paket:** User 3

### **Fatura Durumu:**
- **Ödenmemiş:** User 0, User 3
- **Ödenmiş:** User 1, User 2, User 4, User 5

### **Kota Kullanımı:**
- **En Yüksek:** User 5 (30% internet, 25% konuşma, 25% SMS)
- **En Düşük:** User 0 (10% internet, 5% konuşma, 5% SMS)

## 🎯 Test Senaryoları

### **Farklı Kullanıcı Tipleri:**
1. **Premium Kullanıcı (User 0):** Yüksek kota, ödenmemiş fatura
2. **Gold Kullanıcı (User 1):** Orta kota, ödenmiş fatura
3. **Silver Kullanıcı (User 2):** Düşük kota, ödenmiş fatura
4. **Diamond Kullanıcı (User 5):** En yüksek kullanım, ödenmiş fatura

### **Farklı Paket Türleri:**
1. **Mega İnternet:** 50GB internet, 1000dk konuşma
2. **Öğrenci Dostu:** 30GB internet, 500dk konuşma
3. **Süper Konuşma:** 25GB internet, 2000dk konuşma
4. **Premium Paket:** 100GB internet, 3000dk konuşma

**Tüm veriler user_id'ye göre dinamik olarak hesaplanıyor! 🚀** 