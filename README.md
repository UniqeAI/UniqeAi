# 🤖 UniqueAi Projesi

> **Proje Durumu:** ✅ Tam Entegrasyon Tamamlandı  
> **Backend:** FastAPI + AI Model (Mock/Real)  
> **Frontend:** Streamlit + API Client  
> **AI Model:** Mock AI / Hugging Face Model

## 🚀 Hızlı Başlangıç

### 1. Docker Compose ile Tüm Sistemi Başlat
```bash
# Proje kök dizininde
# (İlk defa çalıştırıyorsan)
docker-compose build
# Servisleri başlat
docker-compose up
```
- Backend: http://localhost:8000
- Frontend: http://localhost:8501

### 2. Manuel Başlatma (Geliştiriciler için)
#### Backend
```bash
cd backend
pip install -r requirements.txt
# Mock AI ile (varsayılan)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Gerçek AI ile
AI_MODEL_TYPE=real uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
#### Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 3. Tarayıcıda Aç
```
http://localhost:8501
```

## 🧑‍💻 Test Kullanıcıları
- **Müşteri:**
  - Ad Soyad: Müşteri Müşteri
  - E-posta: musteri@choyrens.com
  - Telefon: 01234567890
  - Şifre: testşifre
- (Kendi kaydınızı da oluşturabilirsiniz)

## 📋 Özellikler

### ✅ Tamamlanan Entegrasyonlar
- **Backend → AI Model**: Hugging Face model entegrasyonu (mock/real)
- **Frontend → Backend**: API client ile tam entegrasyon
- **Chat Sistemi**: Gerçek zamanlı AI sohbet
- **Telekom API**: Fatura, paket, destek işlemleri
- **Health Checks**: Sistem durumu kontrolü
- **Çerezli Oturum Yönetimi**: Girişte oturum çerezde saklanır, sayfa yenilense bile oturum açık kalır

### 🤖 AI Entegrasyonu (Gerçek Model)
1. Gerekli paketleri yükle:
   ```bash
   pip install transformers torch accelerate bitsandbytes datasets peft trl
   ```
2. `backend/app/services/ai_orchestrator.py` dosyasında şu satırı değiştir:
   ```python
   # Mock AI (varsayılan):
   from .ai_orchestrator_real import MockInferenceService as InferenceService
   # Gerçek AI için:
   from .ai_orchestrator_real import HuggingFaceInferenceService as InferenceService
   InferenceService = HuggingFaceInferenceService
   ```
3. Gerekirse model adını ve parametreleri `backend/app/core/config.py`'de ayarla.
4. Backend'i gerçek AI ile başlat:
   ```bash
   AI_MODEL_TYPE=real uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Chat endpointini test et.

### 💻 Frontend Özellikleri
- **Modern UI**: Streamlit ile responsive tasarım
- **Gerçek Zamanlı Chat**: Anlık mesajlaşma
- **Çerezli Oturum**: Girişte oturum çerezde saklanır, sayfa yenilense bile oturum açık kalır
- **API Adresi Ayarı**: `frontend/utils/api_client.py` içinde `base_url` ile backend adresini değiştirebilirsin.

### 🏗️ Mimari
```
[Streamlit Frontend] ←→ [FastAPI Backend] ←→ [AI Model (Mock/Real)]
      (HTTP API)              (AI Orchestrator)        (Telekom API)
```

## 📁 Proje Yapısı
```
UniqeAi-feature-backend-correction/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── chat.py          # Chat endpoints
│   │   │   ├── telekom.py       # Telekom API
│   │   │   └── user.py          # User management
│   │   ├── services/
│   │   │   ├── ai_orchestrator.py  # AI model entegrasyonu
│   │   │   ├── telekom_api.py      # Telekom API
│   │   │   └── user_service.py     # User service
│   │   └── main.py              # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── app.py                   # Streamlit app
│   ├── utils/
│   │   └── api_client.py        # API client
│   └── requirements.txt
├── docker-compose.yml           # Tüm sistemi başlatır
└── README.md
```

## 🔧 API Adresi Ayarı (Frontend)
- `frontend/utils/api_client.py` dosyasında:
  ```python
  class TelekomAPIClient:
      def __init__(self, base_url: str = "http://localhost:8000"):
          self.base_url = base_url
  ```
- Eğer frontend ve backend farklı makinelerde ise, burada backend'in IP adresini girin.

## 🗄️ Kullanıcı Verisi ve Kalıcılık
- **Şu an:** Kullanıcılar RAM'de tutulur, backend yeniden başlatılırsa silinir.
- **Kalıcı veri için:** SQLite, PostgreSQL gibi bir veritabanı entegre edilebilir.
- Geliştirme/test için uygundur, prod ortamda veritabanı önerilir.

## 🧪 Test

### Entegrasyon Testi
```bash
python test_integration.py
```

### Manuel Test
1. Backend'i başlat
2. Frontend'i başlat
3. Tarayıcıda chat sayfasına git
4. Test mesajları gönder:
   - "Faturamı gösterir misin?"
   - "Hangi paketi kullanıyorum?"
   - "İnternetimde sorun var"

## 📞 Destek
- **Backend Sorunları**: `backend/app/main.py`
- **Frontend Sorunları**: `frontend/app.py`
- **AI Model Sorunları**: `backend/app/services/ai_orchestrator.py`
- **API Sorunları**: `test_integration.py`

## 🎯 Gelecek Geliştirmeler
- [ ] WebSocket ile gerçek zamanlı chat
- [ ] Kullanıcı kimlik doğrulama
- [ ] Çoklu dil desteği
- [ ] Ses tanıma entegrasyonu
- [ ] Mobil uygulama
- [ ] Analytics dashboard

---

**🎉 Entegrasyon Tamamlandı!** Sistem kullanıma hazır. 