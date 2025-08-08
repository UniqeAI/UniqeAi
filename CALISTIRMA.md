# 🚀 PROJE ÇALIŞTIRMA YÖNERGESİ

## 📋 Gereksinimler

### Sistem Gereksinimleri
- **Python**: 3.8 veya üzeri
- **Node.js**: 16 veya üzeri
- **npm**: 8 veya üzeri
- **RAM**: En az 4GB (AI model için)
- **Disk**: En az 2GB boş alan

### İşletim Sistemi
- ✅ Linux (Ubuntu 20.04+)
- ✅ Windows 10/11
- ✅ macOS 10.15+

## 🔧 Kurulum Adımları

### 1. Proje Klonlama
```bash
git clone <repository-url>
cd UniqeAi-feature-backend-correction
```

### 2. Backend Kurulumu

#### Python Sanal Ortam Oluşturma
```bash
cd backend
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

#### AI Model İndirme (İlk Çalıştırma)
```bash
# Model otomatik olarak indirilecek
# İlk çalıştırmada biraz zaman alabilir
```

### 3. Frontend Kurulumu

#### Bağımlılıkları Yükleme
```bash
cd ../frontend
npm install
```

## 🚀 Çalıştırma Adımları

### 1. Backend Başlatma

#### Terminal 1 - Backend
```bash
cd backend

# Sanal ortamı aktifleştir
source venv/bin/activate  # Linux/macOS
# veya
venv\Scripts\activate     # Windows

# Backend'i başlat
python start_backend.py
```

**Beklenen Çıktı:**
```
🚀 Telekom AI Backend başlatılıyor...
🧠 4-bit quantization ile Hugging Face modeli yüklenecek
📡 Server: http://0.0.0.0:8000
🔄 Hot Reload: true
🎯 Swagger UI: http://0.0.0.0:8000/docs
🩺 Health Check: http://0.0.0.0:8000/api/v1/health
🤖 Chat API: http://0.0.0.0:8000/api/v1/chat/
```

### 2. Frontend Başlatma

#### Terminal 2 - Frontend
```bash
cd frontend

# Frontend'i başlat
npm run dev
```

**Beklenen Çıktı:**
```
  VITE v4.5.14  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

## 🌐 Erişim URL'leri

### Backend
- **Ana Sayfa**: http://localhost:8000
- **API Dokümantasyonu**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **AI Model Info**: http://localhost:8000/api/v1/ai/model-info

### Frontend
- **Ana Uygulama**: http://localhost:5173
- **Chat Sayfası**: http://localhost:5173/chat
- **Ana Sayfa**: http://localhost:5173/

## 🧪 Test Etme

### 1. Backend Test
```bash
# Health check
curl -X GET http://localhost:8000/api/v1/health

# AI model info
curl -X GET http://localhost:8000/api/v1/ai/model-info

# Chat test
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "merhaba", "user_id": 1, "session_id": "test"}'
```

### 2. Frontend Test
1. Browser'da http://localhost:5173 adresine git
2. Chat sayfasına git
3. "merhaba" yaz ve gönder
4. AI yanıtını bekle

### 3. AI Araç Testleri
```
"mevcut paketim" → Paket bilgileri
"geçmiş faturalarımı görmek istiyorum" → Fatura listesi
"paketlerimi göster" → Tüm paketler
"kalan kotamı göster" → Kota bilgileri
"ağ durumumu kontrol et" → Ağ durumu
"hız testi yap" → İnternet hız testi
```

## ⚠️ Sorun Giderme

### Backend Sorunları

#### 1. Port 8000 Kullanımda
```bash
# Port'u kontrol et
lsof -i :8000

# Eğer kullanımdaysa, process'i sonlandır
kill -9 <PID>
```

#### 2. AI Model Yükleme Hatası
```bash
# Model cache'ini temizle
rm -rf ~/.cache/huggingface/

# Yeniden başlat
python start_backend.py
```

#### 3. Bağımlılık Hatası
```bash
# Sanal ortamı yeniden oluştur
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Sorunları

#### 1. Port 5173 Kullanımda
```bash
# Port'u kontrol et
lsof -i :5173

# Eğer kullanımdaysa, process'i sonlandır
kill -9 <PID>
```

#### 2. Node Modules Hatası
```bash
# node_modules'ı temizle ve yeniden yükle
rm -rf node_modules package-lock.json
npm install
```

#### 3. Build Hatası
```bash
# Cache'i temizle
npm run build --force
```

## 🔄 Geliştirme Modu

### Backend Hot Reload
```bash
# Backend otomatik olarak hot reload ile çalışır
# Kod değişikliklerinde otomatik yeniden başlar
```

### Frontend Hot Reload
```bash
# Frontend otomatik olarak hot reload ile çalışır
# Kod değişikliklerinde otomatik yenilenir
```

## 📊 Sistem Durumu Kontrolü

### Backend Durumu
```bash
curl -X GET http://localhost:8000/api/v1/health
```

**Beklenen Yanıt:**
```json
{
  "status": "ok",
  "ai_model_type": "real",
  "backend_version": "1.0.0"
}
```

### Frontend Durumu
- Browser'da http://localhost:5173 adresine git
- Status indicator yeşil olmalı
- "Bağlı" yazısı görünmeli

## 🛑 Durdurma

### Backend Durdurma
```bash
# Terminal 1'de Ctrl+C
# veya
pkill -f "python.*start_backend.py"
```

### Frontend Durdurma
```bash
# Terminal 2'de Ctrl+C
# veya
pkill -f "vite"
```

## 📝 Önemli Notlar

### Performans
- İlk başlatmada AI model yüklemesi 1-2 dakika sürebilir
- RAM kullanımı yüksek olabilir (AI model için)
- CPU kullanımı normal seviyede

### Güvenlik
- Backend sadece localhost'ta çalışır
- CORS ayarları sadece development için
- Production'da güvenlik ayarları yapılmalı

### Loglar
- Backend logları terminal'de görünür
- Frontend logları browser console'da görünür
- Hata durumunda logları kontrol edin

## 🎯 Hızlı Başlangıç

### Tek Komutla Başlatma (Geliştirici İçin)
```bash
# Terminal 1
cd backend && source venv/bin/activate && python start_backend.py &

# Terminal 2
cd frontend && npm run dev
```

### Docker ile Çalıştırma (Gelecekte)
```bash
docker-compose up
```

## 📞 Destek

### Sorun Durumunda
1. Logları kontrol edin
2. Port'ların boş olduğunu kontrol edin
3. Bağımlılıkların yüklü olduğunu kontrol edin
4. Sistem gereksinimlerini kontrol edin

### İletişim
- GitHub Issues: Proje sorunları için
- Email: Teknik destek için
- Discord: Topluluk desteği için

---

**Son Güncelleme**: 5 Ağustos 2025  
**Versiyon**: 1.0.0  
**Durum**: ✅ Test Edildi ve Çalışıyor 