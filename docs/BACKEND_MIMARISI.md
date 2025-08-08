# Backend Mimarisi ve Yapı Rehberi

Bu doküman, UniqeAi-18.07-backend projesinin backend mimarisini, dosya yapısını ve her bileşenin nasıl çalıştığını açıklar. Backend kısmını daha önce görmemiş geliştiriciler için hazırlanmıştır.

## 📋 İçindekiler

1. [Genel Mimari](#genel-mimari)
2. [Teknoloji Stack](#teknoloji-stack)
3. [Klasör Yapısı](#klasör-yapısı)
4. [Dosya Açıklamaları](#dosya-açıklamaları)
5. [Veri Akışı](#veri-akışı)
6. [API Endpoint'leri](#api-endpointleri)
7. [Servis Katmanı](#servis-katmanı)
8. [Yapay Zeka Entegrasyonu](#yapay-zeka-entegrasyonu)
9. [Test Yapısı](#test-yapısı)
10. [Nasıl Çalıştırılır](#nasıl-çalıştırılır)

---

## 🏗️ Genel Mimari

Backend, **katmanlı mimari** (layered architecture) prensibini kullanır:

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client (Frontend)                         │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  │
│  │  Chat API   │  │ Telekom API │  │  User API   │  │Mock API │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘  │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                       Service Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │AI Orchestr. │  │ Telekom API │  │User Service │  │Mock Tools│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └──────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                     Data Layer (Schemas)                         │
│           Pydantic modelleri ile veri doğrulama                  │
└──────────────────────────────────────────────────────────────────┘
```

### Mimarinin Avantajları:

- **Modülerlik**: Her katman bağımsız olarak geliştirilebilir
- **Ölçeklenebilirlik**: Yeni özellikler kolayca eklenebilir
- **Test Edilebilirlik**: Her katman ayrı ayrı test edilebilir
- **Bakım Kolaylığı**: Kod düzenli ve anlaşılır
- **Yeniden Kullanılabilirlik**: Servisler farklı API'ler tarafından kullanılabilir

---

## 🔧 Teknoloji Stack

### Backend Framework
- **FastAPI**: Modern, hızlı Python web framework
- **Pydantic**: Veri doğrulama ve serileştirme
- **Asyncio**: Asenkron programlama desteği

### Yapay Zeka
- **Llama 3.1**: Dil modeli
- **Custom AI Orchestrator**: Yapay zeka yönetimi
- **Tool Integration**: Araç entegrasyonu

### Geliştirme Araçları
- **Python 3.8+**: Programlama dili
- **Poetry/Pip**: Paket yönetimi
- **Pytest**: Test framework
- **Docker**: Konteynerleştirme

---

## 📁 Klasör Yapısı

```
backend/
├── app/                          # Ana uygulama klasörü
│   ├── main.py                   # 🚀 Ana uygulama dosyası
│   ├── api/                      # API endpoint'leri
│   │   └── v1/                   # API versiyon 1
│   │       ├── chat.py           # 💬 Chat API endpoint'leri
│   │       ├── telekom.py        # 📞 Telekom API endpoint'leri
│   │       ├── user.py           # 👤 Kullanıcı API endpoint'leri
│   │       └── mock_test.py      # 🧪 Test API endpoint'leri
│   ├── services/                 # İş mantığı servisleri
│   │   ├── ai_orchestrator.py    # 🤖 Yapay zeka yöneticisi
│   │   ├── ai_endpoint_functions.py # 🔧 AI fonksiyonları
│   │   ├── telekom_api.py        # 📡 Telekom API servisi
│   │   ├── user_service.py       # 👥 Kullanıcı servisi
│   │   └── mock_tools.py         # 🛠️ Mock araçları
│   ├── schemas/                  # Veri modelleri
│   │   ├── chat.py               # 💬 Chat veri modelleri
│   │   └── user.py               # 👤 Kullanıcı veri modelleri
│   └── core/                     # Çekirdek konfigürasyonlar
├── docs/                         # Dokümantasyon
├── tests/                        # Test dosyaları
├── requirements.txt              # Python bağımlılıkları
├── Dockerfile                    # Docker konfigürasyonu
└── README.md                     # Proje açıklaması
```

---

## 📄 Dosya Açıklamaları

### 🚀 Ana Dosyalar

#### `backend/app/main.py`
**Ne yapar:** Uygulamanın giriş noktası
**İçeriği:**
- FastAPI uygulamasını başlatır
- CORS middleware'i ekler
- Tüm router'ları (endpoint grupları) dahil eder
- Temel monitoring endpoint'leri sağlar

**Önemli kod parçaları:**
```python
app = FastAPI(title="Agent-Llama Backend")
app.add_middleware(CORSMiddleware)  # CORS desteği
app.include_router(chat.router)     # Chat endpoint'leri
```

#### `backend/requirements.txt`
**Ne yapar:** Python paket bağımlılıklarını listeler
**İçeriği:** FastAPI, Pydantic, asyncio ve diğer gerekli paketler

#### `backend/Dockerfile`
**Ne yapar:** Docker konteyner konfigürasyonu
**İçeriği:** Uygulamanın Docker'da çalıştırılması için gerekli adımlar

### 🔗 API Endpoint'leri (`backend/app/api/v1/`)

#### `chat.py` - Chat API 💬
**Ne yapar:** Yapay zeka ile sohbet endpoint'leri
**Ana fonksiyonlar:**
- `POST /api/v1/chat/` - AI ile mesaj gönderme
- `POST /api/v1/chat/session/clear` - Oturum temizleme
- `GET /api/v1/chat/system/status` - Sistem durumu

**Örnek kullanım:**
```bash
POST /api/v1/chat/
{
  "message": "Merhaba, yardıma ihtiyacım var",
  "user_id": "user123"
}
```

#### `telekom.py` - Telekom API 📞
**Ne yapar:** Telekom operasyonları için endpoint'ler
**Ana fonksiyonlar:**
- Fatura işlemleri (görüntüleme, ödeme)
- Paket yönetimi (değiştirme, görüntüleme)
- Müşteri profili işlemleri
- Teknik destek talepleri

**Örnek kullanım:**
```bash
GET /api/v1/telekom/bill/1
# Müşteri 1'in faturasını getirir
```

#### `user.py` - Kullanıcı API 👤
**Ne yapar:** Kullanıcı yönetimi endpoint'leri
**Ana fonksiyonlar:**
- `POST /api/v1/user/login` - Kullanıcı giriş
- `GET /api/v1/user/current` - Geçerli kullanıcı bilgisi
- `PUT /api/v1/user/current` - Kullanıcı bilgisi güncelleme
- `POST /api/v1/user/logout` - Çıkış yapma

#### `mock_test.py` - Test API 🧪
**Ne yapar:** Test amaçlı endpoint'ler
**Ana fonksiyonlar:** Mock verilerle test işlemleri

### 🔧 Servis Katmanı (`backend/app/services/`)

#### `ai_orchestrator.py` - Yapay Zeka Yöneticisi 🤖
**Ne yapar:** Yapay zeka işlemlerini yönetir
**Ana sınıflar:**
- `YapayZekaOrkestratori`: Ana yönetici sınıf
- `KonusmaYoneticisi`: Konuşma geçmişi yönetimi
- `TelekomAracKaydi`: Telekom araçlarının kaydı

**Önemli özellikler:**
- Kullanıcı mesajlarını işler
- Araç çağrılarını yönetir
- Konuşma bağlamını tutar
- AI modeliyle iletişim kurar

#### `ai_endpoint_functions.py` - AI Fonksiyonları 🔧
**Ne yapar:** AI'nın kullanabileceği tüm fonksiyonlar
**İçeriği:**
- 25+ farklı fonksiyon
- Telekom API fonksiyonları
- Chat API fonksiyonları
- Kullanıcı yönetimi fonksiyonları

#### `telekom_api.py` - Telekom API Servisi 📡
**Ne yapar:** Telekom operasyonlarının iş mantığı
**Ana sınıflar:**
- `TelekomAPIService`: Ana servis sınıf
- Mock müşteri verileri
- Fatura, paket, destek işlemleri

#### `user_service.py` - Kullanıcı Servisi 👥
**Ne yapar:** Kullanıcı bilgilerini yönetir
**Ana sınıflar:**
- `UserService`: Kullanıcı işlemleri
- Bellek içi kullanıcı saklama
- Oturum yönetimi

#### `mock_tools.py` - Mock Araçları 🛠️
**Ne yapar:** Test amaçlı mock veriler ve fonksiyonlar
**İçeriği:** Test verileri ve basit fonksiyonlar

### 📊 Veri Modelleri (`backend/app/schemas/`)

#### `chat.py` - Chat Veri Modelleri 💬
**Ne yapar:** Chat API'si için veri yapıları
**Ana sınıflar:**
- `ChatMessage`: Kullanıcı mesajı
- `ChatResponse`: AI yanıtı
- `ErrorResponse`: Hata yanıtı

#### `user.py` - Kullanıcı Veri Modelleri 👤
**Ne yapar:** Kullanıcı API'si için veri yapıları
**Ana sınıflar:**
- `UserInfo`: Kullanıcı bilgileri
- `UserLogin`: Giriş bilgileri
- `UserResponse`: API yanıtı

### 🧪 Test Dosyaları (`backend/tests/`)

#### `test_ai_endpoint_functions.py`
**Ne yapar:** AI fonksiyonlarını test eder

#### `test_post_endpoints.py`
**Ne yapar:** POST endpoint'lerini test eder

#### `test_telekom_api.html`
**Ne yapar:** Telekom API'sini HTML formatında test eder

---

## 🔄 Veri Akışı

### Tipik Bir İstek Akışı:

```
1. İstek Gelir
   ↓
2. FastAPI Router (API Layer)
   ↓
3. Endpoint Fonksiyonu
   ↓
4. Pydantic ile Veri Doğrulama
   ↓
5. Servis Katmanı Çağrılır
   ↓
6. İş Mantığı İşlenir
   ↓
7. Veri Hazırlanır
   ↓
8. Pydantic ile Yanıt Hazırlanır
   ↓
9. JSON Yanıt Döndürülür
```

### AI İstek Akışı:

```
1. Chat Mesajı Gelir
   ↓
2. Chat API Endpoint
   ↓
3. AI Orchestrator
   ↓
4. Mesaj Ön İşleme
   ↓
5. Konuşma Bağlamı Ekleme
   ↓
6. AI Model Çağrısı
   ↓
7. Araç Çağrıları (Telekom API, User API)
   ↓
8. Final Yanıt Hazırlama
   ↓
9. Kullanıcıya Yanıt Gönderme
```

---

## 🌐 API Endpoint'leri

### Chat API (`/api/v1/chat/`)
- `POST /` - Mesaj gönderme
- `POST /session/clear` - Oturum temizleme
- `GET /system/status` - Sistem durumu

### Telekom API (`/api/v1/telekom/`)
- `GET /bill/{user_id}` - Fatura görüntüleme
- `POST /bill/pay` - Fatura ödeme
- `GET /package/{user_id}` - Paket bilgisi
- `POST /package/change` - Paket değiştirme
- `GET /customer/{user_id}` - Müşteri profili

### User API (`/api/v1/user/`)
- `POST /login` - Kullanıcı giriş
- `GET /current` - Geçerli kullanıcı
- `PUT /current` - Kullanıcı güncelleme
- `POST /logout` - Çıkış yapma

### Mock Test API (`/api/v1/mock-test/`)
- `GET /user/{user_id}` - Test kullanıcı
- `GET /packages` - Test paketler
- `GET /invoice/{user_id}` - Test fatura

---

## 🛠️ Servis Katmanı

### AI Orchestrator Bileşenleri:

#### 1. **Konuşma Yöneticisi**
- Kullanıcı mesajlarını saklar
- Konuşma bağlamını yönetir
- Oturum geçmişini tutar

#### 2. **Araç Kayıt Sistemi**
- Kullanılabilir araçları listeler
- Araç parametrelerini kontrol eder
- Araç çağrılarını yönetir

#### 3. **Model Hizmeti**
- AI modeli ile iletişim
- Yanıt üretimi
- Güven puanı hesaplama

### Servis Katmanı Avantajları:

- **Bağımsızlık**: API'den bağımsız iş mantığı
- **Yeniden Kullanılabilirlik**: Farklı API'ler aynı servisi kullanabilir
- **Test Edilebilirlik**: Servisler ayrı ayrı test edilebilir
- **Bakım Kolaylığı**: İş mantığı tek yerde toplanır

---

## 🤖 Yapay Zeka Entegrasyonu

### AI Orchestrator Mimarisi:

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI Orchestrator                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Mesaj     │  │  Konuşma    │  │    Araç     │  │  Model  │ │
│  │  İşleme     │  │  Yönetimi   │  │   Kayıt     │  │ Hizmeti │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI Fonksiyonları                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Telekom   │  │    Chat     │  │    User     │  │  Mock   │ │
│  │   API (20)  │  │   API (3)   │  │   API (1)   │  │ API (1) │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### AI Fonksiyon Kategorileri:

1. **Fatura & Ödeme** (5 fonksiyon)
2. **Paket & Tarife** (6 fonksiyon)
3. **Teknik Destek** (4 fonksiyon)
4. **Hesap Yönetimi** (5 fonksiyon)
5. **Kullanıcı Bilgileri** (1 fonksiyon)

---

## 🧪 Test Yapısı

### Test Türleri:

#### 1. **Unit Tests**
- Servis fonksiyonlarını test eder
- İş mantığını doğrular
- Hata durumlarını kontrol eder

#### 2. **Integration Tests**
- API endpoint'lerini test eder
- Servis entegrasyonlarını kontrol eder
- Veri akışını doğrular

#### 3. **Mock Tests**
- Harici bağımlılıkları simüle eder
- Test verilerini kullanır
- Hızlı test çalışması sağlar

### Test Dosya Yapısı:

```
tests/
├── test_ai_endpoint_functions.py    # AI fonksiyon testleri
├── test_post_endpoints.py           # POST endpoint testleri
└── test_telekom_api.html           # Telekom API testleri
```

---

## 🚀 Nasıl Çalıştırılır

### 1. Gereksinimler

```bash
# Python 3.8+ gerekli
python --version

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2. Geliştirme Ortamında Çalıştırma

```bash
# Backend klasörüne git
cd backend

# Uvicorn ile çalıştır
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Docker ile Çalıştırma

```bash
# Docker image oluştur
docker build -t uniqeai-backend .

# Docker container çalıştır
docker run -p 8000:8000 uniqeai-backend
```

### 4. API Dokümantasyonu

Uygulama çalıştıktan sonra:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 5. Test Çalıştırma

```bash
# Tüm testleri çalıştır
pytest

# Spesifik test dosyası
pytest tests/test_ai_endpoint_functions.py

# Verbose output
pytest -v
```

---

## 📈 Performans ve Ölçeklenebilirlik

### Performans Özellikleri:

- **Asenkron İşleme**: FastAPI'nin async/await desteği
- **Hafif Memory Kullanımı**: Efficient Python servisleri
- **Hızlı Yanıt Süreleri**: 100-1000ms arası
- **Concurrent Requests**: Eş zamanlı istek desteği

### Ölçeklenebilirlik:

- **Horizontal Scaling**: Birden fazla instance
- **Load Balancing**: Nginx ile yük dağıtımı
- **Microservices**: Servis bazlı bölünebilirlik
- **Docker Support**: Konteyner tabanlı deployment

---

## 🔧 Geliştirme Kılavuzu

### Yeni Endpoint Ekleme:

1. **API Endpoint** oluştur (`app/api/v1/`)
2. **Servis Fonksiyonu** ekle (`app/services/`)
3. **Veri Modeli** tanımla (`app/schemas/`)
4. **Router'ı** main.py'ye ekle
5. **Test** yaz (`tests/`)

### Yeni AI Fonksiyonu Ekleme:

1. **Fonksiyon** yazılır (`ai_endpoint_functions.py`)
2. **Araç Kayıt** eklenir (`ai_orchestrator.py`)
3. **Mapping** güncellenir
4. **Dokümantasyon** eklenir

### Kod Standartları:

- **Type Hints**: Tüm fonksiyonlar için
- **Docstrings**: Açıklayıcı dokümantasyon
- **Error Handling**: Kapsamlı hata yönetimi
- **Logging**: Detaylı loglama
- **Testing**: Yüksek test kapsamı

---

## 🎯 Özet

Bu backend mimarisi:

✅ **Modüler**: Her bileşen bağımsız çalışır
✅ **Ölçeklenebilir**: Kolayca genişletilebilir
✅ **Test Edilebilir**: Kapsamlı test desteği
✅ **Bakım Kolay**: Düzenli ve anlaşılır kod
✅ **Performanslı**: Hızlı ve verimli
✅ **Güvenli**: Hata yönetimi ve doğrulama

**Yeni geliştiriciler için tavsiyeler:**
1. Önce `main.py` dosyasını inceleyin
2. API endpoint'lerini keşfedin
3. Servis katmanını anlayın
4. Testleri çalıştırın
5. Swagger UI ile API'yi test edin

Bu dokümantasyon ile backend mimarisini tam olarak anlayabilir ve geliştirmeye başlayabilirsiniz! 🚀 