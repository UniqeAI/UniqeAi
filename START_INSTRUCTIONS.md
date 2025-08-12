# 🚀 UniqueAI Frontend & Backend Başlatma Rehberi

## 📋 Gereksinimler
- Python 3.11+ kurulu olmalı
- Node.js kurulu olmalı
- Tüm bağımlılıklar yüklenmiş olmalı

## 🔧 Adım Adım Kurulum

### 1️⃣ Backend Başlatma

**İlk Terminal:**
```powershell
# Proje ana dizinine git
cd "C:\Users\NUR\Desktop\UniqeAi-feature-backend-correction (2)\UniqeAi-feature-backend-correction"

# Backend dizinine git  
cd backend

# Python path'i ayarla ve serveri başlat
$env:PYTHONPATH = "."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2️⃣ Frontend Başlatma

**İkinci Terminal:**
```powershell
# Proje ana dizinine git
cd "C:\Users\NUR\Desktop\UniqeAi-feature-backend-correction (2)\UniqeAi-feature-backend-correction"

# Frontend dizinine git
cd frontend

# Development server'ı başlat
npm run dev
```

## 🌐 Erişim Adresleri

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Dokümantasyonu**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 🛠️ Alternatif Backend Başlatma

Eğer yukarıdaki komut çalışmazsa:

```powershell
cd backend
python start_backend.py
```

## 🔍 Sorun Giderme

### Backend Çalışmıyor mu?
```powershell
# Python sürümünü kontrol et
python --version

# Gerekli paketleri yükle
pip install -r requirements.txt

# Port kullanımını kontrol et
netstat -an | findstr :8000
```

### Frontend Çalışmıyor mu?
```powershell
# Node.js sürümünü kontrol et
node --version

# Bağımlılıkları yeniden yükle
npm install

# Port kullanımını kontrol et
netstat -an | findstr :5173
```

## ✅ Başarılı Kurulum Kontrolü

Her iki servis de çalıştığında:

1. **Backend Test**: http://localhost:8000 adresini tarayıcıda açın
2. **Frontend Test**: http://localhost:5173 adresini tarayıcıda açın
3. **API Test**: http://localhost:8000/docs adresinde Swagger UI'yi görebilmelisiniz

## 🚨 Önemli Notlar

- Her iki servisi ayrı terminal pencerelerinde çalıştırın
- Backend önce başlatılmalı (frontend backend'e bağlanır)
- Herhangi bir değişiklik yaptığınızda hot reload otomatik çalışır
- Servisleri durdurmak için terminal'de `Ctrl+C` tuşlayın
