# 🔧 TELEKOM API TEST REHBERİ

Bu rehber, implement edilen Telekom API endpoint'lerini nasıl test edeceğinizi açıklar.

## 🚀 HIZLI BAŞLANGIÇ

### 1. Uygulamayı Çalıştırın
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test Sayfasını Açın
Tarayıcınızda şu adresi açın:
```
file:///path/to/backend/test_telekom_api.html
```

## 📡 TEST YÖNTEMLERİ

### 1. **Tarayıcıda Doğrudan Test (GET Endpoint'leri)**

Bu endpoint'ler tarayıcıda doğrudan açılabilir:

- **Test Endpoint**: `http://localhost:8000/api/v1/telekom/test`
- **Fatura Bilgisi**: `http://localhost:8000/api/v1/telekom/billing/current/5108`
- **Paket Bilgisi**: `http://localhost:8000/api/v1/telekom/packages/current/9408`
- **Müşteri Profili**: `http://localhost:8000/api/v1/telekom/customers/profile/2122`

### 2. **HTML Test Sayfası**

`test_telekom_api.html` dosyasını tarayıcıda açarak tüm endpoint'leri test edebilirsiniz.

### 3. **cURL ile Test**

#### GET İstekleri
```bash
# Test endpoint
curl http://localhost:8000/api/v1/telekom/test

# Fatura bilgisi (User 0 - Mehmet Demir)
curl http://localhost:8000/api/v1/telekom/billing/current/0

# Paket bilgisi (User 1 - Ayşe Kaya)
curl http://localhost:8000/api/v1/telekom/packages/current/1

# Müşteri profili (User 2 - Ali Özkan)
curl http://localhost:8000/api/v1/telekom/customers/profile/2
```

#### POST İstekleri
```bash
# Müşteri profili (User 0 - Mehmet Demir)
curl -X POST "http://localhost:8000/api/v1/telekom/customers/profile" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 0}'

# Fatura bilgisi (User 1 - Ayşe Kaya)
curl -X POST "http://localhost:8000/api/v1/telekom/billing/current" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'

# Kalan kotalar (User 2 - Ali Özkan)
curl -X POST "http://localhost:8000/api/v1/telekom/packages/quotas" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2}'

# Hız testi (User 3 - Fatma Şahin)
curl -X POST "http://localhost:8000/api/v1/telekom/diagnostics/speed-test" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3}'

# Paket değişikliği (User 4 - Mustafa Yılmaz)
curl -X POST "http://localhost:8000/api/v1/telekom/packages/change" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 4, "new_package_name": "Öğrenci Dostu Tarife"}'

# Arıza talebi (User 0 - Mehmet Demir)
curl -X POST "http://localhost:8000/api/v1/telekom/support/tickets" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 0, "issue_description": "Ev internetimin hızı çok yavaşladı"}'
```

### 4. **Python ile Test**

```python
import requests
import json

# Test endpoint
response = requests.get("http://localhost:8000/api/v1/telekom/test")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# POST isteği
data = {"user_id": 5108}
response = requests.post(
    "http://localhost:8000/api/v1/telekom/billing/current",
    json=data
)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 5. **Pytest ile Test**

```bash
cd backend
pytest tests/test_telekom_api.py -v
```

## 🎯 MEVCUT ENDPOINT'LER

### GET Endpoint'leri (Tarayıcıda Test)
| Endpoint | Açıklama | Örnek |
|----------|----------|-------|
| `/api/v1/telekom/test` | Test endpoint'i | `http://localhost:8000/api/v1/telekom/test` |
| `/api/v1/telekom/billing/current/{user_id}` | Fatura bilgisi | `http://localhost:8000/api/v1/telekom/billing/current/0` |
| `/api/v1/telekom/packages/current/{user_id}` | Paket bilgisi | `http://localhost:8000/api/v1/telekom/packages/current/1` |
| `/api/v1/telekom/customers/profile/{user_id}` | Müşteri profili | `http://localhost:8000/api/v1/telekom/customers/profile/2` |

### Mock Veri Örnekleri
| User ID | Müşteri Adı | Tier | Telefon |
|---------|-------------|------|---------|
| 0 | Mehmet Demir | Premium | +905551234567 |
| 1 | Ayşe Kaya | Gold | +905559876543 |
| 2 | Ali Özkan | Silver | +905551112223 |
| 3 | Fatma Şahin | Gold | +905554445556 |
| 4 | Mustafa Yılmaz | Premium | +905557778889 |

### POST Endpoint'leri (JSON ile Test)
| Endpoint | Açıklama | JSON Örneği |
|----------|----------|-------------|
| `/api/v1/telekom/billing/current` | Mevcut fatura | `{"user_id": 0}` |
| `/api/v1/telekom/billing/history` | Geçmiş faturalar | `{"user_id": 1, "limit": 12}` |
| `/api/v1/telekom/billing/payments` | Ödeme geçmişi | `{"user_id": 2}` |
| `/api/v1/telekom/billing/pay` | Fatura ödemesi | `{"bill_id": "F-2024-0001", "method": "credit_card"}` |
| `/api/v1/telekom/billing/autopay` | Otomatik ödeme ayarla | `{"user_id": 3, "status": true}` |
| `/api/v1/telekom/packages/current` | Mevcut paket | `{"user_id": 4}` |
| `/api/v1/telekom/packages/quotas` | Kalan kotalar | `{"user_id": 0}` |
| `/api/v1/telekom/packages/change` | Paket değişikliği | `{"user_id": 1, "new_package_name": "Öğrenci Dostu Tarife"}` |
| `/api/v1/telekom/services/roaming` | Yurtdışı kullanımı etkinleştir | `{"user_id": 2, "status": true}` |
| `/api/v1/telekom/support/tickets` | Arıza talebi | `{"user_id": 3, "issue_description": "İnternet hızı çok yavaş"}` |
| `/api/v1/telekom/customers/profile` | Müşteri profili | `{"user_id": 4}` |
| `/api/v1/telekom/diagnostics/speed-test` | Hız testi | `{"user_id": 0}` |
| `/api/v1/telekom/customers/contact` | İletişim bilgilerini güncelle | `{"user_id": 1, "contact_type": "email", "new_value": "yeni@email.com"}` |
| `/api/v1/telekom/lines/suspend` | Hattı askıya al | `{"user_id": 2, "reason": "Ödeme gecikmesi"}` |
| `/api/v1/telekom/lines/reactivate` | Hattı yeniden aktifleştir | `{"user_id": 3}` |

## 🔍 BEKLENEN YANITLAR

### Başarılı Yanıt Formatı
```json
{
  "success": true,
  "data": {
    // Endpoint'e özel veri
  }
}
```

### Hata Yanıt Formatı
```json
{
  "detail": "Hata mesajı"
}
```

## 🚨 YAYGIN SORUNLAR VE ÇÖZÜMLERİ

### 1. "Method Not Allowed" Hatası
**Sorun**: Tarayıcıda POST endpoint'ine GET isteği gönderiyorsunuz.
**Çözüm**: 
- GET endpoint'lerini kullanın: `/api/v1/telekom/billing/current/5108`
- Veya POST istekleri için cURL/Postman kullanın

### 2. CORS Hatası
**Sorun**: Tarayıcı CORS politikası nedeniyle isteği engelliyor.
**Çözüm**: CORS middleware zaten eklenmiş durumda. Eğer hala sorun yaşıyorsanız:
```python
# app/main.py'de CORS ayarlarını kontrol edin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. "Connection Refused" Hatası
**Sorun**: Uygulama çalışmıyor.
**Çözüm**: 
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. "Module Not Found" Hatası
**Sorun**: Gerekli paketler yüklü değil.
**Çözüm**:
```bash
cd backend
pip install -r requirements.txt
```

## 📊 PERFORMANS TESTİ

### Yanıt Süreleri
```bash
# Yanıt süresini ölçmek için
time curl http://localhost:8000/api/v1/telekom/test
```

### Eşzamanlı İstekler
```bash
# 10 eşzamanlı istek
for i in {1..10}; do
  curl http://localhost:8000/api/v1/telekom/test &
done
wait
```

## 🔧 GELİŞTİRİCİ ARAÇLARI

### FastAPI Docs
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Loglama
Uygulama çalışırken terminal'de logları görebilirsiniz:
```
INFO:     Mevcut fatura sorgulanıyor: User ID 5108
INFO:     Telekom API yanıtı: {'success': True, 'data': {...}}
```

## 📞 DESTEK

Sorun yaşarsanız:
1. Terminal loglarını kontrol edin
2. FastAPI docs'u kullanın: `http://localhost:8000/docs`
3. Test dosyalarını çalıştırın: `pytest tests/test_telekom_api.py -v`

---

**Son Güncelleme**: 2024-03-01  
**Versiyon**: 1.0.0 