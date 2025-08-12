# 🚀 Proje Kurulum Rehberi (Windows)

Bu doküman, projeyi **venv klasörü olmadan** teslim aldığınızda, Windows bilgisayarınızda sıfırdan nasıl çalıştıracağınızı adım adım anlatır.

---

## 1. Gerekli Programlar

- **Python 3.9+** (https://www.python.org/downloads/) - Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
- **Node.js 18+ ve npm** (https://nodejs.org/) - LTS versiyonunu indirin
- **Git** (https://git-scm.com/) - Varsayılan ayarlarla kurun

---

## 2. Projeyi İndir

Projeyi bir klasöre çıkar veya aşağıdaki gibi klonla:

```cmd
git clone <proje-linki>
cd <proje-klasörü>
```

---

## 3. Backend (API) Kurulumu

### a) Command Prompt'u Yönetici Olarak Aç
- Windows tuşu + R → `cmd` yaz → Ctrl + Shift + Enter

### b) Sanal Ortam Oluştur

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
```

### c) Gerekli Python Paketlerini Yükle

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### d) Ortam Değişkenlerini Ayarla (Gerekirse)
- `.env` dosyası gerekiyorsa örneğine bak: `backend\.env.example`

### e) Backend'i Başlat

```cmd
python start_backend.py
```

- API dökümantasyonu: [http://localhost:8000/docs](http://localhost:8000/docs)
- Sağlık kontrolü: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 4. Frontend (Arayüz) Kurulumu

### a) Yeni Command Prompt Penceresi Aç
- Windows tuşu + R → `cmd` yaz → Enter

```cmd
cd <proje-klasörü>\frontend
npm install
```

### b) Ortam Değişkenlerini Ayarla (Gerekirse)
- `.env` dosyası gerekiyorsa örneğine bak: `frontend\env.example`

### c) Frontend'i Başlat

```cmd
npm run dev
```

- Arayüz: [http://localhost:5173](http://localhost:5173)

---

## 5. Kullanım

- Frontend arayüzünden giriş yapabilir, chat ve diğer özellikleri test edebilirsiniz.
- Backend ve frontend loglarını Command Prompt'tan takip edebilirsiniz.

---

## 6. Windows'a Özel Sık Karşılaşılan Sorunlar

### **Python Komutları Çalışmıyor**
- Python'u PATH'e eklediğinizden emin olun
- `python --version` komutu ile kontrol edin
- Gerekirse `py` komutunu deneyin: `py -m venv venv`

### **Port Çakışması**
- 8000 (backend) ve 5173 (frontend) portlarının boş olduğundan emin olun
- Port kullanımda ise: `netstat -ano | findstr :8000` ile kontrol edin

### **Paket Kurulum Hataları**
- Visual Studio Build Tools gerekebilir: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- `pip install --upgrade pip` komutunu çalıştırın
- Antivirüs programınızı geçici olarak devre dışı bırakın

### **CORS Hatası**
- Backend ve frontend aynı makinede ve doğru portlarda çalışmalı
- Windows Firewall'u kontrol edin

### **AI Model Yüklenmiyor**
- Model dosyalarının ve internet bağlantısının olduğundan emin olun
- Windows Defender'ı geçici olarak devre dışı bırakın

### **Command Prompt Sorunları**
- Yönetici olarak çalıştırın
- `chcp 65001` komutu ile UTF-8 kodlamasını etkinleştirin

---

## 7. Windows PowerShell Kullanımı (Alternatif)

Command Prompt yerine PowerShell kullanmak isterseniz:

```powershell
# Sanal ortam oluşturma
python -m venv venv
.\venv\Scripts\Activate.ps1

# Paket kurulumu
pip install -r requirements.txt

# Backend başlatma
python start_backend.py
```

---

## 8. Ekstra

- Geliştirici dökümantasyonu için: `README.md`, `ENDPOINT_LISTESI.md` ve diğer dokümanlara bakabilirsiniz.
- Sorun yaşarsanız, Command Prompt'taki hata mesajlarını paylaşarak destek alabilirsiniz.
- Windows Event Viewer'dan sistem loglarını kontrol edebilirsiniz.

---

**Başarıyla kurulum tamamlandığında, projeyi tam fonksiyonlu olarak kullanabilirsiniz!** 🎉

**Not:** Windows'ta çalıştırırken antivirüs programlarının ve Windows Defender'ın bazı işlemleri engelleyebileceğini unutmayın. Gerekirse geçici olarak devre dışı bırakın. 