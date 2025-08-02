# UniqueAi Backend

Bu dizin, UniqueAi projesinin backend (FastAPI) bileşenini içerir.

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.12+
- pip

### Kurulum

```bash
# Virtual environment oluştur
python3 -m venv venv

# Virtual environment'ı aktifleştir
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### Çalıştırma

#### Mock AI Modu (Varsayılan)
```bash
# Mock AI ile çalıştır
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Gerçek AI Modu
```bash
# Gerçek Hugging Face modeli ile çalıştır
AI_MODEL_TYPE=real uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker ile Çalıştırma

```bash
# Build
docker build -t uniqueai-backend .

# Çalıştır
docker run -p 8000:8000 uniqueai-backend

# Gerçek AI ile çalıştır
docker run -p 8000:8000 -e AI_MODEL_TYPE=real uniqueai-backend
```

## 📁 Dizin Yapısı

```
backend/
├── app/
│   ├── api/v1/           # API endpoint'leri
│   ├── core/             # Konfigürasyon ve ayarlar
│   ├── schemas/          # Pydantic modelleri
│   └── services/         # İş mantığı ve AI servisleri
├── tests/                # Test dosyaları
├── Dockerfile           # Docker konfigürasyonu
├── requirements.txt     # Python bağımlılıkları
└── README.md           # Bu dosya
```

## 🔧 Konfigürasyon

### Environment Variables

| Değişken | Varsayılan | Açıklama |
|----------|------------|----------|
| `AI_MODEL_TYPE` | `mock` | AI model tipi (`mock` veya `real`) |
| `HUGGING_FACE_MODEL_NAME` | `Choyrens/ChoyrensAI-Telekom-Agent-v1-merged` | Hugging Face model adı |
| `BACKEND_HOST` | `0.0.0.0` | Backend host adresi |
| `BACKEND_PORT` | `8000` | Backend port numarası |
| `LOG_LEVEL` | `INFO` | Log seviyesi |

### AI Model Seçimi

#### Mock AI (Varsayılan)
- Hızlı başlangıç
- Bağımlılık gerektirmez
- Geliştirme için ideal

#### Gerçek AI
- Hugging Face modeli kullanır
- GPU gerektirebilir
- Production için uygun

## 🧪 Test

```bash
# Tüm testleri çalıştır
pytest

# Belirli test dosyasını çalıştır
pytest tests/test_main.py

# Coverage raporu oluştur
pytest --cov=app --cov-report=html tests/
```

## 📚 API Dokümantasyonu

Backend çalıştıktan sonra:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔗 Endpoint'ler

### Ana Endpoint'ler
- `GET /` - Ana sayfa
- `GET /api/v1/health` - Sağlık kontrolü
- `GET /api/v1/ai/model-info` - AI model bilgisi

### Chat Endpoint'leri
- `POST /api/v1/chat/` - Chat mesajı gönder
- `GET /api/v1/chat/health` - Chat servisi sağlık kontrolü

### Telekom API Endpoint'leri
- `POST /api/v1/telekom/billing/current` - Mevcut fatura
- `POST /api/v1/telekom/billing/history` - Fatura geçmişi
- `POST /api/v1/telekom/billing/pay` - Fatura ödeme
- `POST /api/v1/telekom/packages/current` - Mevcut paket
- `POST /api/v1/telekom/packages/quotas` - Kalan kotalar
- `POST /api/v1/telekom/support/tickets` - Destek talebi oluştur

## 🔍 Sorun Giderme

### Port 8000 kullanımda
```bash
# Port'u kontrol et
lsof -i :8000

# Process'i durdur
kill -9 <PID>
```

### Import hatası
```bash
# PYTHONPATH'i ayarla
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### AI model yükleme hatası
```bash
# Mock moda geç
export AI_MODEL_TYPE=mock
uvicorn app.main:app --reload
```

## 📝 Loglar

Loglar terminal'de görüntülenir. Log seviyesini değiştirmek için:

```bash
LOG_LEVEL=DEBUG uvicorn app.main:app --reload
```

## 🤝 Katkıda Bulunma

1. Feature branch oluştur
2. Değişiklikleri yap
3. Testleri çalıştır
4. Pull request oluştur

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 