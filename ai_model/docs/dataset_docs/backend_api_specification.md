# 🔧 TELEKOM AI BACKEND API SPESİFİKASYONU

> **Backend Ekibi İçin Detaylı API Dökümantasyonu**  
> Bu belge, AI modelinin beklediği **tam** API formatını içerir.

## 📋 GENEL KURALLAR

### Request/Response Format
- **Content-Type**: `application/json`
- **Encoding**: UTF-8
- **HTTP Methods**: POST (tüm işlemler için)
- **Base URL**: `https://api.telekom.com/v1/`

### Error Handling
```json
{
  "success": false,
  "error": {
    "code": "INVALID_USER",
    "message": "Kullanıcı bulunamadı",
    "details": "User ID 1234 sistemde kayıtlı değil"
  }
}
```

---

## 🎯 API ENDPOINTLERİ

### 1. **FATURA & ÖDEME İŞLEMLERİ**

#### `get_current_bill(user_id: int)`
**Endpoint**: `/billing/current`

**Request:**
```json
{
  "user_id": 5108
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "bill_id": "F-2024-5108",
    "user_id": 5108,
    "amount": 89.50,
    "currency": "TRY",
    "due_date": "2024-03-15",
    "bill_date": "2024-02-28",
    "status": "unpaid",
    "services": [
      {
        "service_name": "Mega İnternet",
        "amount": 69.50
      },
      {
        "service_name": "Sesli Arama", 
        "amount": 20.00
      }
    ]
  }
}
```

#### `get_past_bills(user_id: int, limit: int)`
**Endpoint**: `/billing/history`

**Request:**
```json
{
  "user_id": 3680,
  "limit": 12
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "bills": [
      {
        "bill_id": "F-2024-01",
        "amount": 89.50,
        "bill_date": "2024-01-31",
        "status": "paid",
        "paid_date": "2024-02-05"
      }
    ],
    "total_count": 12,
    "total_amount_paid": 1074.00
  }
}
```

#### `pay_bill(bill_id: str, method: str)`
**Endpoint**: `/billing/pay`

**Request:**
```json
{
  "bill_id": "F-2024-4306",
  "method": "credit_card"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transaction_id": "TXN-2024-001234",
    "bill_id": "F-2024-4306", 
    "amount": 89.50,
    "method": "credit_card",
    "status": "completed",
    "timestamp": "2024-03-01T14:30:00Z"
  }
}
```

#### `get_payment_history(user_id: int)`
**Endpoint**: `/billing/payments`

**Request:**
```json
{
  "user_id": 1596
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "payments": [
      {
        "transaction_id": "TXN-001",
        "amount": 89.50,
        "method": "credit_card",
        "date": "2024-02-05T10:15:00Z",
        "bill_id": "F-2024-01"
      }
    ],
    "total_payments": 5,
    "total_amount": 447.50
  }
}
```

#### `setup_autopay(user_id: int, status: bool)`
**Endpoint**: `/billing/autopay`

**Request:**
```json
{
  "user_id": 3100,
  "status": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 3100,
    "autopay_enabled": true,
    "payment_method": "credit_card_ending_1234",
    "next_payment_date": "2024-03-15"
  }
}
```

---

### 2. **PAKET & TARİFE YÖNETİMİ**

#### `get_customer_package(user_id: int)`
**Endpoint**: `/packages/current`

**Request:**
```json
{
  "user_id": 9408
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "package_name": "Mega İnternet",
    "monthly_fee": 69.50,
    "features": {
      "internet_gb": 50,
      "voice_minutes": 1000,
      "sms_count": 500,
      "roaming_enabled": false
    },
    "activation_date": "2024-01-01",
    "renewal_date": "2024-04-01"
  }
}
```

#### `get_remaining_quotas(user_id: int)`
**Endpoint**: `/packages/quotas`

**Request:**
```json
{
  "user_id": 9408
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "internet_remaining_gb": 42.5,
    "voice_remaining_minutes": 750,
    "sms_remaining": 450,
    "period_end": "2024-03-31",
    "usage_percentage": {
      "internet": 15,
      "voice": 25,
      "sms": 10
    }
  }
}
```

#### `change_package(user_id: int, new_package_name: str)`
**Endpoint**: `/packages/change`

**Request:**
```json
{
  "user_id": 9509,
  "new_package_name": "Öğrenci Dostu Tarife"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "change_id": "CHG-2024-001",
    "from_package": "Mega İnternet",
    "to_package": "Öğrenci Dostu Tarife",
    "effective_date": "2024-04-01",
    "fee_difference": -20.00,
    "status": "scheduled"
  }
}
```

#### `get_available_packages()`
**Endpoint**: `/packages/available`

**Request:**
```json
{}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "packages": [
      {
        "name": "Öğrenci Dostu Tarife",
        "monthly_fee": 49.90,
        "features": {
          "internet_gb": 30,
          "voice_minutes": 500,
          "sms_count": 250
        },
        "target_audience": "students"
      },
      {
        "name": "Mega İnternet",
        "monthly_fee": 69.50,
        "features": {
          "internet_gb": 50,
          "voice_minutes": 1000,
          "sms_count": 500
        }
      }
    ]
  }
}
```

#### `get_package_details(package_name: str)`
**Endpoint**: `/packages/details`

**Request:**
```json
{
  "package_name": "Süper Konuşma"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "Süper Konuşma",
    "monthly_fee": 59.90,
    "setup_fee": 0,
    "features": {
      "internet_gb": 25,
      "voice_minutes": 2000,
      "sms_count": 1000,
      "international_minutes": 100
    },
    "contract_duration": 24,
    "cancellation_fee": 50.00
  }
}
```

#### `enable_roaming(user_id: int, status: bool)`
**Endpoint**: `/services/roaming`

**Request:**
```json
{
  "user_id": 8763,
  "status": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 8763,
    "roaming_enabled": true,
    "activation_time": "2024-03-01T15:00:00Z",
    "daily_fee": 25.00,
    "data_package": "1GB/day"
  }
}
```

---

### 3. **TEKNİK DESTEK & ARIZA**

#### `check_network_status(region: str)`
**Endpoint**: `/network/status`

**Request:**
```json
{
  "region": "Güneydoğu Anadolu"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "region": "Güneydoğu Anadolu",
    "status": "operational",
    "coverage_percentage": 95,
    "active_outages": [
      {
        "area": "Diyarbakır Merkez",
        "issue": "Planlı bakım",
        "start_time": "2024-03-01T02:00:00Z",
        "estimated_end": "2024-03-01T06:00:00Z"
      }
    ],
    "last_updated": "2024-03-01T14:30:00Z"
  }
}
```
#### `close_fault_ticket(ticket_id: sting)`
**Endpoint**: `/support/tickets/close`

**Request:**
```json
{
  "ticket_id": "T-2024-001234",
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ticket_id": "T-2024-001234",
    "user_id": 7477,
    "issue_description": "Ev internetimin hızı çok yavaşladı, neredeyse hiç bir site açılmıyor.",
    "category": "internet_speed",
    "priority": "medium",
    "status": "close",
    "created_at": "2024-03-01T14:30:00Z",
    "estimated_resolution": "2024-03-02T14:30:00Z"
  }
}
```

#### `create_fault_ticket(user_id: int, issue_description: str, category: str, priority: str)`
**Endpoint**: `/support/tickets/open`


**Request:**
```json
{
  "user_id": 7477,
  "issue_description": "Ev internetimin hızı çok yavaşladı, neredeyse hiç bir site açılmıyor.",
  "category": "internet_speed",
  "priority": "medium"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ticket_id": "T-2024-001234",
    "user_id": 7477,
    "issue_description": "Ev internetimin hızı çok yavaşladı, neredeyse hiç bir site açılmıyor.",
    "category": "internet_speed",
    "priority": "medium",
    "status": "open",
    "created_at": "2024-03-01T14:30:00Z",
    "estimated_resolution": "2024-03-02T14:30:00Z"
  }
}
```

#### `get_users_tickets(user_id: int)`

**Endpoint**: `/packages/tickets/user`

**Request:**
```json
{
  "user_id": 9408
}
```
**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "9408",
    "tickets": [
      {
        "ticket_id": "T-2024-001234",
        "issue_description": "Ev internetimin hızı çok yavaşladı, neredeyse hiç bir site açılmıyor.",
        "category": "internet_speed",
        "priority": "medium",
        "status": "open",
        "created_at": "2024-03-01T14:30:00Z",
        "estimated_resolution": "2024-03-02T14:30:00Z"
      },
      {
        "ticket_id": "T-2024-001234",
        "issue_description": "Ev internetimin hızı çok yavaşladı, neredeyse hiç bir site açılmıyor.",
        "category": "internet_speed",
        "priority": "medium",
        "status": "open",
        "created_at": "2024-03-01T14:30:00Z",
        "estimated_resolution": "2024-03-02T14:30:00Z"
      }
    ]
  }
}
```

#### `get_fault_ticket_status(ticket_id: str)`
**Endpoint**: `/support/tickets/status`

**Request:**
```json
{
  "ticket_id": "T-75671"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ticket_id": "T-75671",
    "status": "resolved",
    "resolution": "Bölgesel sinyal sorunu giderildi",
    "created_at": "2024-02-28T10:00:00Z",
    "resolved_at": "2024-03-01T09:15:00Z",
    "technician_notes": "Antenna ayarlaması yapıldı"
  }
}
```

#### `test_internet_speed(user_id: int)`
**Endpoint**: `/diagnostics/speed-test`

**Request:**
```json
{
  "user_id": 1975
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 1975,
    "download_speed_mbps": 47.5,
    "upload_speed_mbps": 12.3,
    "ping_ms": 18,
    "test_timestamp": "2024-03-01T14:30:00Z",
    "test_server": "Istanbul-1",
    "quality_rating": "good"
  }
}
```

---

### 4. **HESAP YÖNETİMİ**

#### `get_customer_profile(user_id: int)`
**Endpoint**: `/customers/profile`

**Request:**
```json
{
  "user_id": 2122
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 2122,
    "name": "Ahmet Yılmaz",
    "phone_numbers": [
      {
        "number": "+905551234567",
        "type": "mobile",
        "status": "active"
      }
    ],
    "email": "ahmet@example.com",
    "address": "İstanbul, Kadıköy",
    "registration_date": "2023-01-15",
    "customer_tier": "gold"
  }
}
```

#### `update_customer_contact(user_id: int, contact_type: str, new_value: str)`
**Endpoint**: `/customers/contact`

**Request:**
```json
{
  "user_id": 1939,
  "contact_type": "phone",
  "new_value": "0056-829 6157"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 1939,
    "contact_type": "phone",
    "old_value": "+905551234567",
    "new_value": "0056-829 6157",
    "updated_at": "2024-03-01T14:30:00Z",
    "verification_required": true
  }
}
```

#### `suspend_line(user_id: int, reason: str)`
**Endpoint**: `/lines/suspend`

**Request:**
```json
{
  "user_id": 6102,
  "reason": "geçici durdurma"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 6102,
    "line_number": "+905551234567",
    "suspension_reason": "geçici durdurma",
    "suspended_at": "2024-03-01T14:30:00Z",
    "reactivation_fee": 0,
    "max_suspension_days": 90
  }
}
```

#### `reactivate_line(user_id: int)`
**Endpoint**: `/lines/reactivate`

**Request:**
```json
{
  "user_id": 1434
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 1434,
    "line_number": "+905551234567",
    "reactivated_at": "2024-03-01T14:30:00Z",
    "suspension_duration_days": 15,
    "reactivation_fee": 0
  }
}
```

---

## 🚀 BACKEND EKİBİ İÇİN GÖREVLER

### 1. **Öncelik Sırası**
1. ✅ **Authentication** sistemi (JWT token based)
2. ✅ **Database** schema design 
3. ✅ **Core endpoint'ler** (yukarıdaki formatına uygun)
4. ✅ **Error handling** standardı
5. ✅ **Rate limiting** & **Security**

### 2. **AI Entegrasyonu**
- AI model, response'ları **print()** formatında bekliyor
- Backend'den gelen JSON response'u AI formatına çevirebiliriz
- Real-time communication için **WebSocket** düşünebilir

### 3. **Test Scenarios** 
1699 örnekteki **tüm parameter kombinasyonları** test edilmeli!

---

## 📞 İLETİŞİM & SYNC

### Haftalık Sync Meetings:
- **Pazartesi**: API endpoint review
- **Çarşamba**: Integration testing
- **Cuma**: Performance & deployment

### Kritik Kararlar:
- [ ] Authentication token format
- [ ] Rate limiting rules  
- [ ] Database choice (PostgreSQL öneriyoruz)
- [ ] Deployment environment

Bu spesifikasyon **1699 veri örneğinden** çıkarılmıştır ve %100 uyumludur! 🎯 