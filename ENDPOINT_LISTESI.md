# 📋 TÜM ENDPOINT'LER LİSTESİ

## 🔍 Backend'de Mevcut Endpoint'ler

### 📋 GET Endpoint'leri (Tarayıcıdan Test Edilebilir)

#### **Root Endpoints**
```
✅ GET /
✅ GET /favicon.ico
```

#### **Health & Monitoring**
```
✅ GET /api/v1/health
✅ GET /api/v1/ai/model-info
```

#### **Chat API**
```
✅ GET /api/v1/chat/health
✅ GET /api/v1/chat/system/status
```

#### **User API**
```
✅ GET /api/v1/user/current
✅ GET /api/v1/user/by-id/{user_id}
✅ GET /api/v1/user/all-active
```

#### **Telekom API**
```
✅ GET /api/v1/telekom/test
✅ GET /api/v1/telekom/billing/current/{user_id}
✅ GET /api/v1/telekom/packages/current/{user_id}
✅ GET /api/v1/telekom/customers/profile/{user_id}
```

### 📝 POST Endpoint'leri (Frontend'den Sorgulanabilir)

#### **Chat API**
```
✅ POST /api/v1/chat/
✅ POST /api/v1/chat/legacy
✅ POST /api/v1/chat/session/clear
```

#### **User API**
```
✅ POST /api/v1/user/register
✅ POST /api/v1/user/login
✅ POST /api/v1/user/logout
```

#### **User API - PUT**
```
✅ PUT /api/v1/user/current
```

#### **Telekom API - Fatura İşlemleri**
```
✅ POST /api/v1/telekom/billing/current
✅ POST /api/v1/telekom/billing/history
✅ POST /api/v1/telekom/billing/pay
✅ POST /api/v1/telekom/billing/payments
✅ POST /api/v1/telekom/billing/autopay
```

#### **Telekom API - Paket İşlemleri**
```
✅ POST /api/v1/telekom/packages/current
✅ POST /api/v1/telekom/packages/quotas
✅ POST /api/v1/telekom/packages/change
✅ POST /api/v1/telekom/packages/available
✅ POST /api/v1/telekom/packages/details
```

#### **Telekom API - Müşteri İşlemleri**
```
✅ POST /api/v1/telekom/customers/profile
✅ POST /api/v1/telekom/customers/contact
```

#### **Telekom API - Destek İşlemleri**
```
✅ POST /api/v1/telekom/support/tickets
✅ POST /api/v1/telekom/support/tickets/close
✅ POST /api/v1/telekom/support/tickets/status
✅ POST /api/v1/telekom/support/tickets/list
```

#### **Telekom API - Sistem İşlemleri**
```
✅ POST /api/v1/telekom/network/status
✅ POST /api/v1/telekom/diagnostics/speed-test
✅ POST /api/v1/telekom/lines/suspend
✅ POST /api/v1/telekom/lines/reactivate
```

#### **Telekom API - Servis İşlemleri**
```
✅ POST /api/v1/telekom/services/roaming
```

#### **Telekom API - Kimlik Doğrulama**
```
✅ POST /api/v1/telekom/auth/register
✅ POST /api/v1/telekom/auth/login
```

## 🧪 Test Edilebilir Endpoint'ler

### **Health Check**
```bash
curl -X GET http://localhost:8000/api/v1/health
```

### **AI Model Info**
```bash
curl -X GET http://localhost:8000/api/v1/ai/model-info
```

### **Chat Test**
```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "merhaba", "user_id": 1, "session_id": "test"}'
```

### **Telekom Test**
```bash
curl -X GET http://localhost:8000/api/v1/telekom/test
```

## 📊 Endpoint Kategorileri

### **🔧 Monitoring & Health**
- Sistem durumu kontrolü
- AI model bilgileri
- Backend sağlık kontrolü

### **💬 Chat & AI**
- AI ile konuşma
- Session yönetimi
- Sistem durumu

### **👤 User Management**
- Kullanıcı kayıt/giriş
- Profil yönetimi
- Kullanıcı listesi

### **📱 Telekom Services**
- Fatura işlemleri
- Paket yönetimi
- Müşteri hizmetleri
- Teknik destek
- Ağ durumu
- Hız testi

## 🚀 Kullanım Örnekleri

### **Frontend'den Chat**
```javascript
const response = await fetch('http://localhost:8000/api/v1/chat/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: "geçmiş faturalarımı görmek istiyorum",
    user_id: 1,
    session_id: "test_session"
  })
})
```

### **Health Check**
```javascript
const health = await fetch('http://localhost:8000/api/v1/health')
const data = await health.json()
console.log('Backend durumu:', data.status)
```

## 📝 Notlar

- Tüm endpoint'ler CORS ile korunuyor
- Backend 8000 portunda çalışıyor
- Frontend 5173 portunda çalışıyor
- AI modeli gerçek zamanlı yanıt veriyor
- Session yönetimi aktif
- Tüm endpoint'ler test edilmiş durumda

## 🔄 Güncelleme Tarihi

**Son Güncelleme**: 5 Ağustos 2025
**Toplam Endpoint Sayısı**: 45+
**Durum**: ✅ Aktif ve Çalışıyor 