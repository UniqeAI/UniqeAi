# Çalıştırma ve Test Rehberi

Bu rehber, UniqueAi projesinin farklı bileşenlerini nasıl çalıştıracağınızı ve test edeceğinizi açıklar.

## 📋 İçindekiler

1. [Gereksinimler](#gereksinimler)
2. [Backend Çalıştırma](#backend-çalıştırma)
3. [Frontend Çalıştırma](#frontend-çalıştırma)
4. [Docker ile Çalıştırma](#docker-ile-çalıştırma)
5. [Test Çalıştırma](#test-çalıştırma)
6. [Sorun Giderme](#sorun-giderme)

---

## 🔧 Gereksinimler

### Sistem Gereksinimleri
- **Python**: 3.12 veya üzeri
- **Docker**: 20.10 veya üzeri (opsiyonel)
- **Git**: 2.30 veya üzeri

### Python Paketleri
```bash
# Backend için
pip install fastapi uvicorn pytest httpx

# Frontend için  
pip install streamlit pandas plotly Pillow svgwrite requests httpx python-dotenv
```

---

## 🚀 Backend Çalıştırma

### Yerel Geliştirme

```bash
# Backend dizinine geç
cd backend

# Virtual environment oluştur
python3 -m venv venv

# Virtual environment'ı aktifleştir
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Backend'i çalıştır
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker ile

```bash
# Backend Docker image'ını oluştur
cd backend
docker build -t uniqueai-backend .

# Backend container'ını çalıştır
docker run -p 8000:8000 uniqueai-backend
```

### Test

```bash
# Backend dizininde
cd backend

# Testleri çalıştır
pytest tests/

# Belirli test dosyasını çalıştır
pytest tests/test_main.py

# Coverage ile test et
pytest --cov=app tests/
```

---

## 🎨 Frontend Çalıştırma

### Yerel Geliştirme

```bash
# Frontend dizinine geç
cd frontend

# Virtual environment oluştur
python3 -m venv venv

# Virtual environment'ı aktifleştir
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Frontend'i çalıştır
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker ile

```bash
# Frontend Docker image'ını oluştur
cd frontend
docker build -t uniqueai-frontend .

# Frontend container'ını çalıştır
docker run -p 8501:8501 uniqueai-frontend
```

---

## 🐳 Docker ile Çalıştırma

### Tüm Servisleri Çalıştır

```bash
# Proje ana dizininde
docker-compose up --build

# Arka planda çalıştır
docker-compose up -d --build
```

### Servisleri Durdur

```bash
# Tüm servisleri durdur
docker-compose down

# Volume'ları da sil
docker-compose down -v
```

### Logları Görüntüle

```bash
# Tüm logları görüntüle
docker-compose logs

# Belirli servisin loglarını görüntüle
docker-compose logs backend
docker-compose logs frontend
```

---

## 🧪 Test Çalıştırma

### Backend Testleri

```bash
# Backend dizininde
cd backend

# Tüm testleri çalıştır
pytest

# Belirli test dosyasını çalıştır
pytest tests/test_main.py
pytest tests/test_chat.py
pytest tests/test_telekom.py

# Coverage raporu oluştur
pytest --cov=app --cov-report=html tests/

# Verbose mod
pytest -v tests/
```

### Frontend Testleri

```bash
# Frontend dizininde
cd frontend

# Streamlit test modu
streamlit run app.py --server.headless true
```

### API Testleri

```bash
# Backend çalışırken
curl http://localhost:8000/
curl http://localhost:8000/api/v1/health

# Chat endpoint testi
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Merhaba", "user_id": 1}'
```

---

## 🔍 Sorun Giderme

### Backend Sorunları

**Port 8000 kullanımda:**
```bash
# Port'u kontrol et
lsof -i :8000

# Process'i durdur
kill -9 <PID>
```

**Import hatası:**
```bash
# PYTHONPATH'i ayarla
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Virtual environment'ı kontrol et
which python
pip list
```

### Frontend Sorunları

**Port 8501 kullanımda:**
```bash
# Port'u kontrol et
lsof -i :8501

# Process'i durdur
kill -9 <PID>
```

**Streamlit başlamıyor:**
```bash
# Streamlit cache'ini temizle
streamlit cache clear

# Debug modunda çalıştır
streamlit run app.py --logger.level debug
```

### Docker Sorunları

**Image build hatası:**
```bash
# Docker cache'ini temizle
docker system prune -a

# Yeniden build et
docker-compose build --no-cache
```

**Container çalışmıyor:**
```bash
# Container loglarını kontrol et
docker-compose logs

# Container'a bağlan
docker-compose exec backend bash
docker-compose exec frontend bash
```

---

## 📊 Performans Testleri

### Backend Load Test

```bash
# Apache Bench ile test
ab -n 1000 -c 10 http://localhost:8000/api/v1/health

# wrk ile test
wrk -t12 -c400 -d30s http://localhost:8000/api/v1/health
```

### Frontend Load Test

```bash
# Streamlit performans testi
streamlit run app.py --server.headless true --server.port 8501
```

---

## 🔗 Erişim Linkleri

### Yerel Geliştirme
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:8501

### Docker
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:8501

---

## 📝 Notlar

1. **Backend çalışmadan frontend çalışmaz** - API bağlantısı gerekli
2. **Virtual environment kullanın** - Paket çakışmalarını önler
3. **Docker kullanırken volume'ları kontrol edin** - Kod değişiklikleri için
4. **Test coverage'ı %80'in üzerinde tutun** - Kod kalitesi için
5. **Logları takip edin** - Hata ayıklama için

Bu rehber ile projeyi sorunsuz çalıştırabilir ve test edebilirsiniz! 🚀 