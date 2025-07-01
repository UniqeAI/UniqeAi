# 🤖 UniqeAi

Modern ve akıllı telekom müşteri hizmetleri AI agent'i. Bu proje, bireysel telekom müşterilerine 7/24 destek sağlayan, duygusal zeka sahibi ve tahmine dayalı mesajlaşma yapabilen gelişmiş bir AI assistant'tır.

## 🎯 Proje Özellikleri

### Core Features
- 🧠 **Akıllı Sohbet**: Doğal dil işleme ile müşteri sorularını anlama
- 😊 **Duygu Analizi**: Müşteri duygularını tespit etme ve buna göre yanıt verme
- 🔮 **Tahmine Dayalı Mesajlaşma**: Gelecek müşteri ihtiyaçlarını öngörme
- ⚡ **Real-time İşlemler**: Anlık fatura, paket ve destek işlemleri
- 📊 **Kapsamlı Dashboard**: Yönetici paneli ve analytics

### Telekom İşlemleri
- 📱 Fatura sorgulama ve ödeme
- 📦 Paket değişimi ve yönetimi
- 🔧 Teknik destek ve arıza bildirimi
- 💰 Kampanya ve promosyon yönetimi
- 📞 Hat işlemleri ve numarahanı
- 🌐 İnternet ve Wi-Fi destek

## 🛠 Technology Stack

### Backend
- **Python 3.11+** - Core backend language
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **Pydantic** - Data validation
- **Alembic** - Database migrations

### AI & ML
- **Ollama** - Local LLM inference
- **Llama 3.1** - Base language model
- **Transformers** - Hugging Face model library
- **Sentence-Transformers** - Embedding generation
- **Scikit-learn** - Traditional ML algorithms
- **NLTK/spaCy** - Natural language processing

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **React Query** - Server state management
- **Zustand** - Client state management
- **React Hook Form** - Form handling

### DevOps & Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-service orchestration
- **Railway** - Cloud deployment platform
- **GitHub Actions** - CI/CD pipeline
- **Nginx** - Reverse proxy (production)
- **Redis** - Caching and session storage

## 🏗 Proje Mimarisi

```
telekom-ai-agent/
├── backend/                 # Python backend
│   ├── app/
│   │   ├── core/           # Core configurations
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── schemas/        # Pydantic schemas
│   │   └── utils/          # Utility functions
│   ├── alembic/            # Database migrations
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── store/          # State management
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utility functions
│   ├── public/             # Static files
│   └── package.json        # Node dependencies
├── mock-api/               # Mock telekom API
├── ai-models/              # AI model files
├── docs/                   # Documentation
├── scripts/                # Development scripts
└── docker-compose.yml      # Development environment
```

## 🚀 Hızlı Başlangıç

### Gereksinimler
- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose**
- **Git**

### Kurulum
```bash
# Repository'yi klonla
git clone <repository-url>
cd telekom-ai-agent

# Environment variables ayarla
cp .env.example .env

# Docker ile tüm servisleri başlat
docker-compose up -d

# Ya da manuel kurulum:
# Backend kurulum
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend kurulum
cd frontend
npm install
npm run dev
```

## 👥 Ekip Rolleri ve Odak Alanları

Projenin farklı fazlarında ekip üyeleri çeşitli görevlere odaklanacaktır.

1.  **Tech Lead**: Proje mimarisi, fazlar arası koordinasyon ve nihai entegrasyon.
2.  **AI Specialist 1 (Fine-Tuning & Core Logic)**: Llama 3.1 modelinin senaryolara özel eğitimi, prompt mühendisliği ve temel AI mantığı.
3.  **AI Specialist 2 (NLP & Advanced Features)**: Zemberek entegrasyonu, duygu analizi ve tahminsel mesajlaşma gibi ileri seviye özellikler.
4.  **Backend Developer 1 (API & DB)**: FastAPI ile core API geliştirme, PostgreSQL entegrasyonu ve veritabanı yönetimi.
5.  **Backend Developer 2 (Mock API & Services)**: Ön sunum için mock telekom API'sinin geliştirilmesi ve diğer servis entegrasyonları.
6.  **Frontend Developer (UI/UX)**: React ile kullanıcı arayüzünün ve yönetici panelinin geliştirilmesi.
7.  **QA & DevOps Engineer**: Test senaryolarının yazılması, Docker yönetimi, CI/CD pipeline kurulumu ve dokümantasyon.

## 📅 Geliştirme Yol Haritası (6 Hafta)

### **Faz 1: Ön Sunum MVP'si (Hafta 1-2)**

**Hedef:** Jüriye sunulabilecek, temel bir senaryoyu (fatura sorgulama) baştan sona çalıştıran bir prototip oluşturmak. Arayüz bu aşamada `FastAPI`'nin otomatik `/docs` sayfası olacaktır.

-   **Hafta 1: Kurulum ve Temel Entegrasyon**
    -   [ ] Proje iskeletinin ve `docker-compose.yml` dosyasının oluşturulması.
    -   [ ] `FastAPI` ile temel API endpoint'lerinin ve `Pydantic` şemalarının hazırlanması.
    -   [ ] Sahte müşteri ve fatura verilerini sunacak `Mock API`'nin geliştirilmesi.
    -   [ ] `Llama 3.1` modelinin `Transformers` ile yerel olarak çalıştırılıp API'ye bağlanması.
-   **Hafta 2: İlk Senaryo ve Sunum Hazırlığı**
    -   [ ] **"Fatura Sorgulama" Senaryosu:**
        -   [ ] Kullanıcı girdisini `Zemberek` ile işleme.
        -   [ ] Prompt mühendisliği ile kullanıcının "fatura sorma" niyetini tespit etme.
        -   [ ] AI'ın Mock API'den veri alıp anlamlı bir cevap üretmesini sağlama.
    -   [ ] Ön sunum için baştan sona testler ve dokümantasyonun hazırlanması.

### **Faz 2: Çekirdek Ürün Geliştirme (Hafta 3-4)**

**Hedef:** Prototipi, tam özellikli bir backend ve çalışan bir frontend ile gerçek bir uygulamaya dönüştürmeye başlamak.

-   **Hafta 3: Sağlam Backend ve Veritabanı**
    -   [ ] `SQLite`'tan `PostgreSQL`'e geçiş, `SQLAlchemy` modellerinin ve `Alembic` ile migration'ların oluşturulması.
    -   [ ] Gelişmiş API mantığı (kullanıcı yönetimi, daha karmaşık işlemler).
    -   [ ] `React` ve `TypeScript` ile frontend projesinin temel kurulumu, `Vite` ve `Tailwind CSS` konfigürasyonu.
-   **Hafta 4: Frontend ve Gelişmiş AI Senaryoları**
    -   [ ] Temel frontend bileşenlerinin (sohbet penceresi, login sayfası) geliştirilmesi.
    -   [ ] Frontend'in `React Query` ile backend API'sine bağlanması.
    -   [ ] **"Tarife Değişikliği" Senaryosu:** Bağlam yönetimi gerektiren çok adımlı diyalog akışlarının geliştirilmesi.
    -   [ ] Duygu analizi için ilk denemelerin yapılması.

### **Faz 3: İleri Seviye Özellikler ve Optimizasyon (Hafta 5-6)**

**Hedef:** Projeyi jüriyi etkileyecek gelişmiş özelliklerle donatmak, test etmek ve sunuma hazır hale getirmek.

-   **Hafta 5: Tam Entegrasyon ve "Wow" Özellikleri**
    -   [ ] Frontend ve backend'in tam entegrasyonu, UI/UX iyileştirmeleri (`Framer Motion`).
    -   [ ] Duygu analizi modelinin entegre edilerek ajanın cevaplarının dinamikleştirilmesi.
    -   [ ] Tahmine dayalı mesajlaşma özelliğinin prototipinin geliştirilmesi.
    -   [ ] Kapsamlı backend ve frontend testlerinin yazılması.
-   **Hafta 6: Optimizasyon, Dağıtım ve Final Hazırlık**
    -   [ ] Performans optimizasyonu (API yanıt süreleri, veritabanı sorguları).
    -   [ ] `GitHub Actions` ile temel bir CI/CD pipeline'ı kurma.
    -   [ ] `Railway` veya benzeri bir platforma dağıtım denemeleri.
    -   [ ] Güvenlik kontrolleri ve son rötuşlar.
    -   [ ] Nihai proje sunumunun ve teknik dokümantasyonun hazırlanması.

## 🧪 Test Edilecek Senaryolar

### Temel İşlemler
- Fatura sorgulama ve ödeme
- Paket değişimi
- Teknik destek talepleri
- Arıza bildirimi

### Duygusal Durumlar
- Müşteri memnuniyetsizliği
- Acil durum talepleri
- Şikayet yönetimi
- Pozitif feedback

### Kompleks Senaryolar
- Multi-step işlemler
- Kampanya önerileri
- Upselling/cross-selling
- Escalation durumları

## 📈 Success Metrics

- **Response Time**: < 2 saniye
- **Accuracy**: > 90% doğru yanıt
- **Customer Satisfaction**: > 8/10
- **Issue Resolution**: > 85% first contact
- **Emotion Detection**: > 80% accuracy

## 🔒 Security & Compliance

- End-to-end encryption
- GDPR compliance
- Data anonymization
- Secure API authentication
- Audit logging

---

**Not**: Bu proje AI assistance ile geliştirilmektedir. Her commit professional standartlarda kod review'dan geçmektedir. 